# -*- coding: utf-8 -*-
# :Project:   metapensiero.extjs.desktop
# :Created:   mer 03 ott 2012 17:33:20 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2012, 2013, 2014, 2016, 2018 Lele Gaifax
#

"""
Javascript and CSS sources minification
=======================================

This script minifies and packs all JS/CSS sources into a single monolithic
file, for faster load and obfuscation.
"""

from io import open
import logging
from os import unlink
from os.path import abspath, dirname, join, normpath
from re import compile, DOTALL, MULTILINE
from subprocess import PIPE, Popen, call
from tempfile import mktemp

from yuicompressor import get_jar_filename

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


DBG_RX = compile(r"^[ \t]*//[ \t]*<debug>[ \t]*$"
                 r".*?"
                 r"^[ \t]*//[ \t]*</debug>[ \t]*$", DOTALL | MULTILINE)


def minify_js(args, scripts):
    """Minify a list of ECMAScript sources into a single monolithic file.

    :param args: the command line options
    :param scripts: a list of ECMAScript sources paths

    Each ECMAScript source is preprocessed by ``sed`` to remove
    ``<debug>...</debug>`` sections and then fed to the Yahoo Compressor.
    """

    output = args.output_js

    logging.info("Compressing %d javascripts to %s... %s debug statements",
                 len(scripts), output, "keeping" if args.debug else "stripping")

    concat_fname = mktemp('.js')
    with open(concat_fname, 'w', encoding='utf-8') as concat:
        for script in scripts:
            try:
                with open(script, encoding='utf-8') as f:
                    src = f.read()
            except FileNotFoundError:
                logging.warning("Script %s not found!", script)
                continue
            if not args.debug:
                src = DBG_RX.sub("", src)
            concat.write(src)
            concat.write("\n")

    compressor_cmd = ['java', '-jar', get_jar_filename(),
                      "--type", "js",
                      "-o", output]

    if args.debug:
        compressor_cmd.extend(['--preserve-semi', '--line-break', '0'])

    compressor_cmd.append(concat_fname)

    returncode = call(compressor_cmd)

    if returncode:
        logging.warning("YUI Compressor exit status: %d", returncode)
        if args.debug:
            logging.debug("Uncompressed concatenated sources left in %s",
                          concat_fname)
        else:
            logging.warning("Run with --debug to obtain the concatenated uncompressed"
                            " sources")
    elif not args.debug:
        unlink(concat_fname)


URL_RX = compile(r"""url *\( *(["']?)(.+)\1 *\)""")


def absolutize_css_urls(basedir, css, map):
    """Replace relative url() with absolute paths.

    :param basedir: a string, the base directory non-absolute URLs refer to
    :param css: a string, the style sheet
    :param map: a dictionary containing a map between externally accessible
                prefixes and actual file system positions
    :rtype: a string, the new style sheet without relative URLs

    All ``url()`` referencing a local resource are replaced with the
    absolute location and eventually transformed in the externally
    visible path as specified by `map`.

    Example::

      absolutize_css_urls('/var/www/css', "url('../images/foo.png')",
                          {'/img/': '/var/www/images/'})
      => "url('/img/foo.png')"
    """

    def replace_url(match):
        delim = match.group(1)
        fpath = match.group(2)
        apath = abspath(normpath(join(basedir, fpath)))
        for prefix, base in map.items():
            if apath.startswith(base):
                apath = join(prefix, apath[len(base):])
                break
        return "url(%s%s%s)" % (delim, apath, delim)

    return URL_RX.sub(replace_url, css)


IMPORT_RX = compile(r"""@import *(["'])(.+)\1 *;""")


def resolve_css_imports(fname, map):
    """Resolve @import directive referring to local filesystem sheets.

    :param fname: a string, the file name containing the CSS
    :param map: a dictionary
    :rtype: a string, the flattened CSS

    This will replace all @import directives with the content of the
    referenced style sheet, when it is on the local filesystem. It
    will also absolutize all ``url()``, calling
    :function:`absolutize_css_urls` with the specified `map`
    dictionary
    """

    basedir = dirname(fname)

    with open(fname, encoding='utf-8') as f:
        css = absolutize_css_urls(basedir, f.read(), map)

    if '@import' in css:
        def replace_import(match):
            try:
                from urllib.parse import splittype
            except ImportError:
                # Python 2.7
                from urllib import splittype
            uri = match.group(2)
            utype, upath = splittype(uri)
            if utype is None:
                ipath = abspath(normpath(join(basedir, upath)))
                return resolve_css_imports(ipath, map)
            return match.group(0)
        css = IMPORT_RX.sub(replace_import, css)

    return css


def minify_css(args, styles, map):
    """Minify a list of CSS style sheets into a single monolithic file.

    :param args: the command line options
    :param styles: a list of CSS sheets paths
    :param map: a dictionary

    Each style sheet is preprocessed with :function:`resolve_css_imports`
    and then fed to the Yahoo Compressor.
    """

    output = args.output_css

    logging.info("Compressing %d stylesheets to %s...", len(styles), output)

    compressor_cmd = ['java', '-jar', get_jar_filename(),
                      "--type", "css",
                      "-o", output]

    compressor = Popen(compressor_cmd, stdin=PIPE)

    if args.debug:
        concat_fname = mktemp('.css')
        concat_output = open(concat_fname, 'wb')

    for style in styles:
        css = resolve_css_imports(style, map).encode('utf-8')
        compressor.stdin.write(css)
        if args.debug:
            concat_output.write(css)

    compressor.stdin.close()
    if args.debug:
        concat_output.close()

    compressor.communicate()

    if compressor.returncode:
        logging.warning("YUI Compressor exit status: %d", compressor.returncode)
        if args.debug:
            logging.debug("Uncompressed concatenated sources left in %s",
                          concat_fname)
        else:
            logging.warning("Run with --debug to obtain the concatenated uncompressed"
                            " sources")
    elif args.debug:
        unlink(concat_fname)


def absolutize(paths, prefix_map):
    """Transform each partial path into its absolute full path.

    :param paths: a list of partial paths
    :param prefix_map: a dictionary, where each key is a possible prefix and its value
                       is the absolute position on the filesystem
    :rtype: a list of absolute paths

    Example::

      absolutize(['/img/foo.png', '/js/bar.js'],
                 {'/img/': '/var/www/images/',
                  '/js/': '/var/www/sources/'})
      => ['/var/www/images/foo.png', '/var/www/sources/bar.js']
    """

    abspaths = []
    for path in paths:
        if '/' in path:
            for prefix, base in prefix_map.items():
                if path.startswith(prefix):
                    abspaths.append(join(base, path[len(prefix):]))
                    break
            else:
                abspaths.append(path)
        else:
            abspaths.append(path)
    return abspaths


def main():
    from argparse import ArgumentParser
    import json
    import pickle

    parser = ArgumentParser(description="JS/CSS packer.",
                            epilog="Minimize and pack all needed"
                            " JS or CSS sources in a single monolithic"
                            " obfuscated module for faster load.")

    parser.add_argument('manifest', default='manifest.json', nargs='?',
                        help="The file containing a JSON encoded list of"
                        " sources to be minified (defaults to %(default)s)")
    parser.add_argument('--output-js', default="static/all-classes.js",
                        help="Output file with compressed JS sources"
                        " (defaults to %(default)s)")
    parser.add_argument('--output-css', default="static/all-styles.css",
                        help="Output file with compressed CSS sources"
                        " (defaults to %(default)s)")
    parser.add_argument('--list-js', default=False, action="store_true",
                        help="Just list the JS sources in the right order")
    parser.add_argument('--list-css', default=False, action="store_true",
                        help="Just list the CSS sources in the right order")
    parser.add_argument('--prefix-map', action='append', default=[],
                        help="Add a map between a prefix and a"
                        " destination path, in the form “Some.prefix=dest/path”")
    parser.add_argument('--extjs-auto-deps', default=False, action="store_true",
                        help="Automatically extract ExtJS dependencies")
    parser.add_argument('--extjs-core-bundle', metavar="BUNDLE",
                        help="Assume core classes are loaded from the"
                        " specified bundle")
    parser.add_argument('--extjs-require', action='append', default=[],
                        metavar="CLASS",
                        help="Explicitly add CLASS (either an ExtJS class"
                        " name or a script file name) to the requirements")
    parser.add_argument('--debug', default=False, action="store_true",
                        help="Do not strip <debug></debug> snippets"
                        " in JS sources and, in case of errors, leave"
                        " concatenated uncompressed sources in a temporary"
                        " filename for inspection and emit debug messages")
    parser.add_argument("--verbose", default=False, action="store_true",
                        help="Emit informational noise.")

    args = parser.parse_args()

    if args.debug:
        level = logging.DEBUG
    elif args.verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level, format="[%(levelname).1s] %(message)s")

    prefix_map = dict()
    for item in args.prefix_map:
        prefix, base = item.split('=')
        prefix = prefix.strip()
        if '/' in prefix and not prefix.endswith('/'):
            prefix += '/'
        base = base.strip()
        if not base.endswith('/'):
            base += '/'
        prefix_map[prefix] = base

    with open(args.manifest) as f:
        sources = json.load(f)

    styles = absolutize(sources.get('styles', []), prefix_map)
    scripts = absolutize(sources.get('scripts', []), prefix_map)

    if args.extjs_auto_deps:
        from .extjs_deps import get_needed_sources
        scripts = get_needed_sources(args.extjs_require + scripts, prefix_map,
                                     bundle=args.extjs_core_bundle)

    if args.list_js or args.list_css:
        if args.list_css:
            for s in styles:
                print(s)
        if args.list_js:
            for s in scripts:
                print(s)
    else:
        if styles:
            minify_css(args, styles, prefix_map)
        if scripts:
            minify_js(args, scripts)


if __name__ == '__main__':
    main()
