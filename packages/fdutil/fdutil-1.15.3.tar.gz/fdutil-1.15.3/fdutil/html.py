# encoding: utf-8

import os
import codecs
import webbrowser
try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping
from future.utils import string_types
from dominate import document, tags
from .resources import (open_document_snippet,
                        enable_tooltip_snippet,
                        clickable_popover)
from .path_tools import ensure_path_exists

META_DIV_ID = u'_meta'
CSS_DIV_ID = u'_css'
SCRIPTS_DIV_ID = u'_scripts'

BOOTSTRAP_JS = [
    dict(src=u'https://code.jquery.com/jquery-3.3.1.slim.min.js',
         integrity=u'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
         crossorigin=u'anonymous'),
    dict(src=u'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
         integrity=u'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
         crossorigin=u'anonymous'),
    dict(src=u'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
         integrity=u'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
         crossorigin=u'anonymous')
]
BOOTSTRAP_CSS = [
    dict(rel=u'stylesheet',
         href=u'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
         integrity=u'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
         crossorigin=u'anonymous')
]

FONT_AWESOME_JS = dict(src=u'https://use.fontawesome.com/releases/v5.0.10/js/all.js',
                       integrity=u'sha384-slN8GvtUJGnv6ca26v8EzVaR9DC58QEwsIk9q1QXdCU8Yu8ck/tL/5szYlBbqmS+',
                       crossorigin=u'anonymous')

JS_SNIPPETS = []

for snippet in [
    open_document_snippet,
    enable_tooltip_snippet,
    clickable_popover
]:
    with codecs.open(snippet,
                     u'rb',
                     encoding=u'utf8') as js_fp:
        JS_SNIPPETS.append(u'{js}'.format(js=js_fp.read()))


def html_filepath(html_folder=None,
                  filename=None):
    path = html_folder + os.sep if html_folder else u''
    return path + u'{filename}.html'.format(filename=filename if filename else u'index')


def escape_html_text(html_string):
    return ((u'\\n'.join(html_string.splitlines()))
            .replace(u"'", u"\\x27")
            .replace(u'"', u"\\x22"))


def validate_input_list(script_list):
    if script_list is None:
        script_list = []

    if isinstance(script_list, string_types):
        # convert to list if we have a string (assumes single script)
        script_list = [script_list]

    if not isinstance(script_list, list):
        raise TypeError(u'Scripts/CSS entry should be a string or a list of strings, '
                        u'where each string is a single script/css.')

    return script_list


def uglify_script_or_css(script_text):
    return u' '.join(script_text.replace(u'\n', u' ').split())


def generate_html_document(title,
                           lang=u'en-GB',
                           charset=u'utf-8',
                           scripts=None,
                           inline_scripts=JS_SNIPPETS,
                           css=None,
                           inline_css=None,
                           include_bootstrap=True):

    """ Generate a document object.

    This builds a compliant HTML 5 document object including any scripts / css required for the page.
    The body is left empty to allow the user to add page HTML.

    :param title:               Document title
    :param lang:                Document language.  default: en-GB
    :param charset:             Character set to use.  default: utf-8
    :param scripts:             List of linked scripts to be used in this HTML document
    :param inline_scripts:      List of raw inline scripts to be used in this HTML document
    :param css:                 List of linked css to be used in this HTML document
    :param inline_css:          List of raw inline css to be used in this HTML document
    :param include_bootstrap:   Boolean to specify whether to include bootstrap libraries.  default: True
    :return:                    generated document object (dominate.document)
    """

    scripts = validate_input_list(scripts)
    inline_scripts = validate_input_list(inline_scripts)

    css = validate_input_list(css)
    inline_css = validate_input_list(inline_css)

    doc = document(title=title)

    # Check for bootstrap
    if include_bootstrap:
        scripts = BOOTSTRAP_JS + [FONT_AWESOME_JS] + scripts
        css = BOOTSTRAP_CSS + css

    if lang is not None:
        doc[u'lang'] = lang

    with doc.head:
        doc_meta = tags.div(id=META_DIV_ID)
        doc_css = tags.div(id=CSS_DIV_ID)
        doc_scripts = tags.div(id=SCRIPTS_DIV_ID)

    with doc_meta:
        tags.comment(u'Required meta tags')
        tags.meta(charset=charset)
        tags.meta(name=u'viewport',
                  content=u'width=device-width, initial-scale=1, shrink-to-fit=no')

    with doc_css:
        tags.comment(u'Bootstrap CSS')
        for style in css:
            if not isinstance(style, Mapping):
                style = dict(rel=u'stylesheet', href=style)

            tags.link(**style)

        for style in inline_css:
            tags.style(uglify_script_or_css(style))

    with doc_scripts:
        tags.comment(u'Javascript')
        for script in scripts:
            if not isinstance(script, Mapping):
                script = dict(type=u'text/javascript',
                              src=script)

            tags.script(**script)

        for script in inline_scripts:
            tags.script(uglify_script_or_css(script))

    return doc


def write_to_html(html_document,
                  filename=None,
                  html_folder=None,
                  filehandle=None,
                  open_in_browser=False):

    """ Take a HTML dominate object and write it to specified file.

    :param html_document:   HTML Node (dominate html node object)
    :param filename:        HTML output filename
    :param html_folder:     Folder to save the file to
    :param filehandle:      File handle of the file to write the HTML to
                            NOTE: Either filehandle or filename & html_foler must be specified
    :param open_in_browser: Whether to open the written page in the default browser
    """

    if not ((filename and html_folder) or filehandle):
        raise ValueError(u'Must supply a filehandle or an html_folder and '
                         u'filename to write to html.')

    if not isinstance(html_document, document):
        raise TypeError(u'html_document is not a dominate.document class!')

    ensure_path_exists(html_folder)

    # Set file pointer
    if not filehandle:
        fp = codecs.open(html_filepath(html_folder=html_folder,
                                       filename=filename),
                         u'wb',
                         encoding=u'utf8')

    else:
        fp = filehandle

    fp.write(html_document.render())

    if filehandle is None:
        fp.close()

        if open_in_browser:

            html_path = html_filepath(html_folder=html_folder,
                                      filename=filename)

            if os.name == u"posix":
                html_path = u"file://" + html_path

            webbrowser.open(html_path)

    return fp.stream.name


if __name__ == u'__main__':
    html = generate_html_document(title=u'Test page')

    with html.body:
        tags.h1(u'Hello, world!')
    print(html.render())
