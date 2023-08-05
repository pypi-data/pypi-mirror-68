# -*- coding: utf-8 -*-
# :Project:   metapensiero.extjs.desktop -- ExtJS parsing utils
# :Created:   sab 08 feb 2014 13:22:38 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2014, 2016, 2018 Lele Gaifax
#

from collections import deque
from glob import glob
from io import open
import logging
from os.path import exists, join

from calmjs.parse.asttypes import (Array, DotAccessor, FuncExpr, FunctionCall, GroupingOp,
                                   Object, String)
from calmjs.parse.parsers.es5 import Parser
from calmjs.parse.walkers import Walker

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


CORE_CLASSES = []


class Class(object):
    aliases = None

    def __init__(self, name):
        self.name = name
        self.superclass = self.override = self.uses = self.requires = self.mixins = None

    def setSuperClass(self, superclass):
        self.superclass = superclass

    def setUses(self, uses):
        self.uses = list(uses)

    def setRequires(self, requires):
        self.requires = list(requires)

    def setMixins(self, mixins):
        self.mixins = list(mixins)

    def setScript(self, script):
        self.script = script

    def setOverride(self, override):
        self.override = override

    def addAlias(self, alias):
        self.aliases[alias] = self.name

    def __repr__(self):
        return '%s(%s)' % (self.name, self.superclass)

    def __iter__(self):
        yield self.name
        if self.superclass is not None:
            yield self.superclass
        if self.override is not None:
            yield self.override
        if self.requires:
            for c in self.requires:
                yield c
        if self.mixins:
            for c in self.mixins:
                yield c
        if self.uses:
            for c in self.uses:
                yield c


class ClassDependencies(object):
    def __init__(self, queue, prefix_map):
        self.classes = []
        self.current = None
        self.queue = queue
        self.prefix_map = prefix_map
        self.seen_nodes = set()

    def __call__(self, node):
        walker = Walker()
        for node in walker.filter(node, lambda n:
                                  isinstance(n, FunctionCall)
                                  and isinstance(n.identifier, DotAccessor)):
            if node in self.seen_nodes:
                continue
            self.seen_nodes.add(node)

            fname = str(node.identifier)
            args = node.args.items
            if fname == 'Ext.define':
                if not isinstance(args[0], String):
                    logging.debug('Ignoring exotic definition: %s', args[0])
                else:
                    name = self.get_string(args[0])
                    try:
                        self.handle_define(name, args[1])
                    except Exception:
                        logging.exception('Could not handle definition of "%s": %s',
                                          name, args[1])
            elif fname == 'Ext.cmd.derive':
                name = self.get_string(args[0])
                base = self.get_string(args[1])
                self.handle_derive(name, base)
            elif fname == 'Ext.require':
                name = self.get_string(args[0])
                if name:
                    fn = args[1]
                    self.handle_require(name, fn)
            elif fname == 'Ext.ClassManager.addNameAlternateMappings':
                if isinstance(args[0], Object):
                    self.add_aliases(args[0])

    def get_string(self, node):
        if isinstance(node, String):
            return node.value[1:-1]
        elif isinstance(node, DotAccessor):
            return str(node)

    def add_aliases(self, obj):
        get_string = self.get_string
        aliases = Class.aliases
        for prop in obj.properties:
            classname = get_string(prop.left)
            for alias in prop.right:
                aliases[get_string(alias)] = classname

    def handle_require(self, name, fn):
        self.queue.append(_get_class_script(name, self.prefix_map))
        nclasses = len(self.classes)
        self(fn)
        for c in self.classes[nclasses:]:
            if c.requires is None:
                c.requires = []
            c.requires.append(name)

    def handle_derive(self, name, base):
        self.current = Class(name)
        self.classes.append(self.current)
        self.current.setSuperClass(base)

    def handle_define(self, name, data):
        self.current = Class(name)
        self.classes.append(self.current)

        if isinstance(data, GroupingOp):
            data = data.expr

        if isinstance(data, FuncExpr):
            # src/util/Observable.js:
            # Ext.define('foo', function(foo) {
            #   ...
            #   return {
            #     requires: ['bar']
            #   };
            # });
            data = data.children()[-1].expr
        elif isinstance(data, FunctionCall):
            # ext-4.2.1.883/src/dom/Helper.js
            # Ext.define('foo', (function(foo) {
            #   ...
            #   return {
            #     requires: ['bar']
            #   };
            # })());
            data = data.children()[0]
            if isinstance(data, GroupingOp):
                data = data.expr
            data = data.children()[-1].expr

        get_string = self.get_string

        for prop in data.properties:
            key = prop.left.value
            if key == 'extend':
                self.current.setSuperClass(get_string(prop.right))
            elif key == 'uses':
                if isinstance(prop.right, String):
                    self.current.setUses([get_string(prop.right)])
                else:
                    self.current.setUses(get_string(c) for c in prop.right.items)
            elif key == 'requires':
                if isinstance(prop.right, String):
                    self.current.setRequires([get_string(prop.right)])
                else:
                    self.current.setRequires(get_string(c) for c in prop.right.items)
            elif key == 'mixins':
                if isinstance(prop.right, String):
                    self.current.setMixins([get_string(prop.right)])
                elif isinstance(prop.right, Array):
                    self.current.setMixins(get_string(c) for c in prop.right.items)
                else:
                    self.current.setMixins(get_string(p.right) for p in prop.right.properties)
            elif key == 'override':
                self.current.setOverride(get_string(prop.right))
            elif key == 'alternateClassName':
                if isinstance(prop.right, String):
                    self.current.addAlias(get_string(prop.right))
                else:  # isinstance(prop.right, Array):
                    for alias in prop.right.items:
                        self.current.addAlias(get_string(alias))


def _extract_script_classes(script, queue, prefix_map):
    if not exists(script):
        raise FileNotFoundError(script)

    content = open(script, encoding='utf-8').read()

    logging.info("Extracting classes from script %s...", script)
    parser = Parser()
    tree = parser.parse(content)
    visitor = ClassDependencies(queue, prefix_map)
    visitor(tree)
    classes = visitor.classes
    for c in classes:
        c.setScript(script)

    return classes


def _get_class_script(classname, prefix_map):
    while classname in Class.aliases:
        classname = Class.aliases[classname]

    parts = classname.split('.')
    tail = []
    while len(parts) > 1:
        tail.insert(0, parts.pop())
        prefix = '.'.join(parts)
        if prefix in prefix_map:
            return join(prefix_map[prefix], *tail) + '.js'

    raise KeyError('Could not guess source script path for class "%s"' % classname)


def _get_needed_classes(classes, prefix_map):
    queue = deque(c if '/' in c else _get_class_script(c, prefix_map) for c in classes)
    seen_classes = set(CORE_CLASSES)
    all_classes = []
    done_scripts = set()

    while queue:
        script = queue.popleft()

        if '*' in script:
            scripts = glob(script)
            queue.extendleft(reversed(scripts))
            script = queue.popleft()

        if script in done_scripts:
            continue

        done_scripts.add(script)

        try:
            classes = _extract_script_classes(script, queue, prefix_map)
        except FileNotFoundError:
            logging.warning('Could not find script "%s"', script)
        except Exception as e:
            logging.exception('Could not parse script "%s": %s', script, e)
            break
        else:
            if not classes:
                logging.debug('NO CLASSES IN "%s"', script)
                placeholder = Class('placeholder')
                placeholder.setScript(script)
                all_classes.append(placeholder)

            seen_classes.update(c.name for c in classes)
            all_classes += classes
            for class_ in classes:
                for used_class in class_:
                    if used_class not in seen_classes:
                        script = _get_class_script(used_class, prefix_map)
                        if script not in done_scripts:
                            if '*' in script:
                                scripts = glob(script)
                                queue.extendleft(reversed(scripts))
                            else:
                                queue.append(script)

    return all_classes


def _extract_core_classes(bundle):
    aliases = Class.aliases
    seen = set()
    with open(bundle, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('* @class '):
                classname = line[9:]
                if classname not in seen and classname != 'Ext':
                    yield classname
                    seen.add(classname)
            elif line.startswith('* @alternateClassName '):
                alias = line[22:]
                aliases[alias] = classname
                yield alias
                seen.add(alias)


def get_needed_sources(classes, prefix_map, bundle=None):
    from sqlalchemy.util.topological import sort

    aliases = Class.aliases = {}

    if bundle is not None:
        CORE_CLASSES.extend(_extract_core_classes(bundle))
        classes.insert(0, bundle)

    all_classes = _get_needed_classes(classes, prefix_map)
    classes = dict((c.name, c) for c in all_classes)

    # SA topological sort relies on objects id()
    uniquified = {}

    def uniquify(t):
        return uniquified.setdefault(t, t)

    deps = []

    for c in all_classes:
        if c.script == bundle:
            continue

        added = False

        related_class_names = []

        if c.superclass and c.superclass not in CORE_CLASSES:
            related_class_names.append(c.superclass)

        if c.override:
            related_class_names.append(c.override)

        if c.requires:
            related_class_names.extend(c.requires)

        if c.mixins:
            related_class_names.extend(c.mixins)

        for cn in related_class_names:
            while cn in aliases:
                cn = aliases[cn]
            try:
                script = classes[cn].script
            except KeyError:
                if cn not in CORE_CLASSES:
                    logging.warning('Class "%s" not found!', cn)
            else:
                if script != bundle and script != c.script:
                    deps.append((uniquify(script), uniquify(c.script)))
                    added = True

        if not added:
            uniquify(c.script)

    return list(sort(deps, uniquified.keys()))
