#!/usr/bin/env python3

import logging
import os
import shutil
import sys
import re
import argparse
from pathlib import Path

from sphinx.cmd.build import main as sphinx_main
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from distutils.dir_util import copy_tree

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
REPOS = os.path.join(ROOT, "repos")
CONTENT = os.path.join(ROOT, "content")
REPOS_ROOT = os.path.join(REPOS, "en/docs") # don't rely on this.

LOG = logging.getLogger(__name__)
ARGS = None

#  Loosely based on https://github.com/sixty-north/rst_to_md/
#  Getting this working inside sphinx and *debugging* is poorly documented
#  (aside from installing as an extension).
#  Easy to convert rst -> xml -> (hugo) markdown

def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)



""" Path-to-source is based on where we checked code in the get_repos.sh script """
def _path_to_github_url(path):
    relpath = str(path.replace(REPOS_ROOT, ""))
    repo = None
    if relpath.startswith("/corda-os/"):
        relpath = relpath.replace("/corda-os/", "release/os/")
        repo = "corda"
    elif relpath.startswith("/corda-enterprise/"):
        repo = "enterprise"
        relpath = relpath.replace("/corda-enterprise/", "release/ent/")
    elif relpath.startswith("/cenm/"):
        repo = "network-services"
        relpath = relpath.replace("/cenm/", "release/")
    else:
        assert False, "No such repo"

    return f"https://github.com/corda/{repo}/blob/{relpath}"


def _link_new_window(text, url):
    if not ARGS.md:
        return f'{{{{% link src="{url}" text="{text}" %}}}}'
     
    return f'[{text}]({url})' # + '{:target="_blank"}' for some types of md.




class Markdown:
    def image(self, url, alt):
        return f'![{alt}]({url} "{alt}")'

    def link(self, url, text):
        return f'[{text}]({url})'

    def comment(self, text):
        return f'<-- {text} -->'

    def toc(self):
        return self.comment("page table of contents removed")    

    def visit_emphasis(self):
        return '*'

    def depart_emphasis(self):
        return '*'

    def visit_strong(self):
        return '**'

    def depart_strong(self):
        return '**'

    def visit_subscript(self):
        return '<sub>'

    def depart_subscript(self): 
        return '</sub>'

    def visit_superscript(self):
        return '<sup>'

    def depart_superscript(self):
        return '</sup>'

    def visit_literal(self):
        return '`'

    def depart_literal(self):
        return '`'

    def visit_literal_block(self, lang):
        return f'```{lang}'

    def depart_literal_block(self):
        return '```'

    def visit_math(self):
        return '$'

    def depart_math(self):
        return '$'

    def visit_tab(self, lang):
        return f'<div class="r3-tab">\n\n'

    def depart_tab(self):
        return '\n\n</div>\n'

    def visit_tabs(self, idx):        
        return f'<div class="r3-tabs" id="tabs-{idx}">\n\n'

    def depart_tabs(self):
        return '\n</div>\n\n'

    def visit_note(self):
        return '<div class="r3-o-note" role="alert">\n\n'

    def depart_note(self):
        return '\n\n</div>\n\n'

    def visit_warning(self):
        return '<div class="r3-o-warning" role="alert">\n\n'

    def depart_warning(self):
        return '\n\n</div>\n\n'

    def visit_attention(self):
        return '<div class="r3-o-attention" role="alert">\n\n'

    def depart_attention(self):
        return '\n\n</div>\n\n'
        
    def visit_important(self):
        return '<div class="r3-o-important" role="alert">\n\n'

    def depart_important(self):
        return '\n\n</div>\n\n'

    def visit_topic(self):
        return '<div class="r3-o-topic" role="alert">\n\n'

    def depart_topic(self):
        return '\n\n</div>\n\n'


"""  Override raw Markdown with Hugo shortcodes  """
class Hugo(Markdown):
    def __init__(self, *args, **kwargs):
        super(Hugo, self).__init__(**kwargs)

    # def image(self, url, alt):
    #     f'{{{{< img src="{url}" alt="{alt}" >}}}}\n\n'

    def visit_tabs(self, idx):
        return f'\n{{{{< tabs name="tabs-{idx}" >}}}}\n'

    def depart_tabs(self):
        return "{{< /tabs >}}\n\n"

    def visit_tab(self, lang):
        return f'\n{{{{% tab name="{lang}" %}}}}\n'

    def depart_tab(self):
        return f'{{{{% /tab %}}}}\n'

    def comment(self, s):
        return f"\n{{{{/* {s} */}}}}\n"

    def visit_note(self):
        return "\n{{< note >}}"

    def depart_note(self):
        return "{{< /note >}}\n\n"

    def visit_warning(self):
        return "\n{{< warning >}}"

    def depart_warning(self):
        return "{{< /warning >}}\n\n"

    def visit_attention(self):
        return "\n{{< attention >}}\n"

    def depart_attention(self):
        return "\n{{< /attention >}}\n"

    def visit_important(self):
        return "\n{{< important >}}"

    def depart_important(self):
        return "\n{{< /important >}}\n"


class Context:
    def __init__(self):
        self.head = []
        self.body = []
        self.foot = []

    # You probably don't want this
    def put_head(self, text):
        self.head.append(text)

    def put_body(self, text):
        self.body.append(text)

    # You probably don't want this
    def put_foot(self, text):
        self.foot.append(text)

    def finalize(self):
        pass

    def __add__(self, other):
        self.head += other.head
        self.body += other.body
        self.foot += other.foot
        return self

    def astext(self):
        return ''.join(self.head + self.body + self.foot)


class TableContext(Context):
    def __init__(self, *args, **kwargs):
        super(TableContext, self).__init__(**kwargs)
        self.cols = []
        self.col_titles = []
        self.current_col = 0

    # def finalize(self):
    #     self.body = markdown_table


def _is_xml_padding(s):
    likely_xml_padding = s and s.startswith('\n') and s.strip() == ''
    return likely_xml_padding or not s


class Translator:
    def __init__(self, cms):
        self._context = [Context()]
        self.cms = cms

        # For determining h1/h2/h3 etc.
        self.section_depth = 0
        self.tabs_counter = 0
        self.title = None

        # We shouldn't have nested containers so this should be enough for tabbed code panes.
        self.in_tabs = False

        self._elements = [None]
        self._ordered_list = [0]

    """Returns the final document"""

    def astext(self):
        """Return the final formatted document as a string."""
        return self.top.astext()

    @property
    def top(self):
        return self._context[-1]

    def push_context(self, ctx):
        self._context.append(ctx)

    def pop_context(self):
        head = self._context[-1]
        head.finalize()
        self._context = self._context[:-1]
        self._context[-1] += head

    def push_element(self, e):
        self._elements.append(e)

    def pop_element(self):
        self._elements = self._elements[:-1]

    def _walk(self, parent):
        for e in parent:
            self.push_element(e.tag)
            visit_func = getattr(self, f'visit_{e.tag}', visit_unsupported)
            depart_func = getattr(self, f'depart_{e.tag}', visit_unsupported)

            self.push_context(Context())
            visit_func(e)
            likely_xml_padding = e.text and e.text.startswith('\n') and e.text.strip() == ''

            #  <tag>TAG_BODY<other>OTHER_BODY<other>OTHER_TAIL</tag>TAG_TAIL
            table_tags = ['entry', 'thead', 'tgroup', 'colspec', 'row', 'tbody']
            if likely_xml_padding:
                if e.tag not in table_tags:
                    self.top.put_body('\n')
                else:
                    pass  # chomp
            elif e.text:
                self.top.put_body(e.text)

            self._walk(e)
            depart_func(e)

            #  Half of this is XML formatting between elements

            inline_tags = ['literal', 'emphasis', 'strong', 'subscript', 'superscript',
                           'reference', 'inline' 'target']
            #
            # if e.tag in inline_tags and e.tail:  # and e.tail.strip() != '':
            #     self.top.put_body(e.tail)

            likely_xml_padding = e.tail and e.tail.startswith('\n    ') and e.tail.strip() == ''

            if likely_xml_padding and e.tag not in inline_tags:
                pass
            elif e.tail:
                self.top.put_body(e.tail)

            self.pop_context()
            self.pop_element()

    def walk(self, filename):
        tree = ET.parse(filename)
        self._walk([tree.getroot()])

    def _fix_up_javadoc(self, link):
        LOG.debug("TODO: fix up javadoc")
        return '#'

    ###########################################################################
    # Visitors
    ###########################################################################

    #  Some we use, but sphinx renderps into the simplified output (such as
    #  plain old 'emphasis'
    #
    # https://docutils.sourceforge.io/docs/user/rst/quickref.html#definition-lists
    #
    # https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links

    def visit_title_reference(self, node):
        self.top.put_body(self.cms.visit_emphasis())

    def depart_title_reference(self, node):
        self.top.put_body(self.cms.depart_emphasis())

    def visit_section(self, node):
        self.section_depth += 1

    def depart_section(self, node):
        self.section_depth -= 1

    def visit_title(self, node):
        h = self.section_depth * '#'
        self.top.put_body(h + ' ')

    def depart_title(self, node):
        if self.section_depth == 1 and not self.title:
            self.title = node.text

        self.top.put_body('\n')

    def visit_block_quote(self, node):
        class QuoteContext(Context):
            def finalize(self):
                quoted = ['> {}'.format(line) for line in self.body[:1]] + self.body[1:]
                quoted = [line.replace('\n', '\n> ') for line in quoted[:-1]] + quoted[-1:]
                self.body = quoted

        self.push_context(QuoteContext())

    def depart_block_quote(self, node):
        self.pop_context()

    def visit_raw(self, node):
        self.push_context(Context())

    def depart_raw(self, node):
        # Chomp....
        out = []
        for line in self.top.body:
            if not any([s in line for s in ['codesets.js', 'jquery.js']]):
                out.append(line)
        self.top.body = out
        self.pop_context()

    def visit_definition(self, node):
        pass

    def depart_definition(self, node):
        pass

    def visit_reference(self, node):
        self.top.put_body('[')

    def depart_reference(self, node):
        link = '#'
        if 'refuri' in node.attrib:
            uri = node.attrib['refuri']
            link = uri
            # Could be a local path or another page
            if not link.startswith('http'):
                __, ext = os.path.splitext(link)
                # If it doesn't have a suffix, it's another page
                if not ext:
                    #  we're targeting hugo-flavoured markdown
                    if not ARGS.md:
                        link = f'{{{{< relref "{link}" >}}}}'
                    else:
                        if '#' in link:
                            link = link.replace('#', '.md#')
                        else:
                            link = link + '.md'

            else:
                LOG.debug(f"Regular link: {link}")
                if 'javadoc' in link:
                    link = self._fix_up_javadoc(link)
                pass
        elif 'refid' in node.attrib:
            # Anchor link
            link = '#' + node.attrib['refid']

        self.top.put_body(f']({link})')

    def visit_definition_list_item(self, node):
        # we don't really do anything with this?
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_strong(self, node):
        self.top.put_body(self.cms.visit_strong())

    def depart_strong(self, node):
        self.top.put_body(self.cms.depart_strong())

    def visit_bullet_list(self, node):
        pass

    def depart_bullet_list(self, node):
        pass

    def visit_topic(self, node):
        if node.attrib.get('names', '') == 'contents':
            # replace table of contents with hugo version
            if ARGS.toc:
                self.top.put_body(self.cms.toc())
            self.push_context(Context())
        else:
            self.top.put_body(self.cms.visit_topic())

    def depart_topic(self, node):
        if node.attrib.get('names', '') == 'contents':
            self.top.body = []  # chomp the old table of contents
            self.pop_context()
        else:
            self.top.put_body(self.cms.depart_topic())

    def visit_emphasis(self, node):
        self.top.put_body(self.cms.visit_emphasis())

    def depart_emphasis(self, node):
        self.top.put_body(self.cms.depart_emphasis())

    def visit_literal_block(self, node):
        lang = node.attrib.get('language', '')
        if self.in_tabs:
            self.top.put_body(self.cms.visit_tab(lang))
        self.top.put_body(self.cms.visit_literal_block(lang) + '\n')

    def depart_literal_block(self, node):
        self.top.put_body('\n' + self.cms.depart_literal_block() + '\n')
        if self.in_tabs:
            self.top.put_body(self.cms.depart_tab())

        if node.attrib.get('source', None):
            src = node.attrib['source']

            if self.in_tabs:
                #  append each one in the footer so it appears beneath the 'tabs' collection, rather
                #  than under the tab
                self.top.put_foot(_link_new_window(os.path.basename(src), _path_to_github_url(src)))
            else:
                # not in a collection, put it straight under the 'tab' (which) doesn't exist
                self.top.put_body(_link_new_window(os.path.basename(src), _path_to_github_url(src)))

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    def visit_container(self, node):
        self.tabs_counter += 1
        self.push_context(Context())
        self.top.put_body(self.cms.visit_tabs(self.tabs_counter))
        self.in_tabs = True

    def depart_container(self, node):
        self.top.put_body(self.cms.depart_tabs())
        # Gather up any source code links, and add them to the end.
        if (self.top.foot):
            md = self.cms.image("github", "/images/svg/github.svg") + " " + " | ".join(self.top.foot) + "\n\n"
            self.top.body.append(md)
        # self.top.body.extend(f"*  {value}\n" for value in self.top.foot)
        self.top.foot = []
        self.pop_context()

        self.in_tabs = False

    def visit_definition_list(self, node):
        # We don't really seem to care about this - it will be emitted as a bullet list
        pass

    def depart_definition_list(self, node):
        pass

    def visit_target(self, node):
        pass

    def depart_target(self, node):
        #  Don't think we need this - we end up with a double link
        #  Typically handled by 'reference'
        # text = node.attrib.get('names', "FIXME")
        # link = node.attrib.get('refuri', "#")
        # self.top.put_body(f"[{text}]({link})")
        pass

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        if self._elements[-2] == "entry":
            return  # in a table

        self.top.put_body('\n\n')

    def visit_image(self, node):
        # Not using markdown, as some of the images are massive
        # and need rescaling.

        # TODO:  wrap image in <div aria-label="..."> ?
        # and make that a shortcode?
        if 'uri' not in node.attrib:
            url = '#'
            alt = 'missing'
        else:
            url = node.attrib.get('uri', '#')
            alt = os.path.splitext(os.path.basename(url))[0].replace('-', ' ').replace('_', ' ')

        self.top.put_body(self.cms.image(url, os.path.basename(alt)))            

    def depart_image(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def depart_enumerated_list(self, node):
        pass

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        pass

    def visit_warning(self, node):
        self.top.put_body(self.cms.visit_warning())

    def depart_warning(self, node):
        self.top.put_body(self.cms.depart_warning())

    def visit_literal(self, node):
        self.top.put_body(self.cms.visit_literal())

    def depart_literal(self, node):
        self.top.put_body(self.cms.visit_literal())

    def visit_note(self, node):
        self.top.put_body(self.cms.visit_note())

    def depart_note(self, node):
        self.top.put_body(self.cms.depart_note())

    def visit_list_item(self, node):
        self.push_context(Context())
        bullet_depth = sum([1 for e in self._elements if e == 'bullet_list']) - 1
        padding = '    ' * bullet_depth
        self.top.put_body(padding + '* ')

    def depart_list_item(self, node):
        if '\n' in self.top.body[1]:
            self.top.body[1] = self.top.body[1].replace('\n', '')
        self.top.put_body('\n')
        self.pop_context()

    def visit_term(self, node):
        LOG.debug('Not implemented term')

    def depart_term(self, node):
        LOG.debug('Not implemented term')

    def visit_comment(self, node):
        self.push_context(Context())

    def depart_comment(self, node):
        # chomp comments
        self.top.body = []
        self.pop_context()

    def visit_attention(self, node):
        self.top.put_body(self.cms.visit_attention())

    def depart_attention(self, node):
        self.top.put_body(self.cms.depart_attention())

    def visit_compact_paragraph(self, node):
        pass

    def depart_compact_paragraph(self, node):
        self.top.put_body('\n')

    def visit_compound(self, node):
        LOG.debug('Not implemented compound')

    def depart_compound(self, node):
        LOG.debug('Not implemented compound')

    def visit_field_list(self, node):
        LOG.debug('Not implemented field_list')

    def depart_field_list(self, node):
        LOG.debug('Not implemented field_list')

    def visit_field(self, node):
        LOG.debug('Not implemented field')

    def depart_field(self, node):
        LOG.debug('Not implemented field')

    def visit_field_body(self, node):
        LOG.debug('Not implemented field_body')

    def depart_field_body(self, node):
        LOG.debug('Not implemented field_body')

    def visit_field_name(self, node):
        LOG.debug('Not implemented field_name')

    def depart_field_name(self, node):
        LOG.debug('Not implemented field_name')

    def visit_important(self, node):
        self.top.put_body(self.cms.visit_important())

    def depart_important(self, node):
        self.top.put_body(self.cms.depart_important())

    def visit_problematic(self, node):
        LOG.debug('Not implemented problematic')

    def depart_problematic(self, node):
        LOG.debug('Not implemented problematic')

    def visit_line_block(self, node):
        LOG.debug('Not implemented line_block')

    def depart_line_block(self, node):
        LOG.debug('Not implemented line_block')

    def visit_line(self, node):
        LOG.debug('Not implemented line')

    def depart_line(self, node):
        LOG.debug('Not implemented line')

    def visit_table(self, node):
        self.top.put_body("\n{{< table >}}\n")
        self.push_context(TableContext())

    def depart_table(self, node):
        self.top.put_body("\n{{< /table >}}\n")
        self.pop_context()

    def visit_colspec(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        if not table_context:
            raise RuntimeError("Expected a TableContext on the stack")
        col_width = int(node.attrib.get('colwidth'), 0)
        assert col_width != 0, "No col width?"

        table_context.cols.append(col_width)

    def depart_colspec(self, node):
        pass

    def visit_tgroup(self, node):
        pass  # might need to do something here

    def depart_tgroup(self, node):
        pass

    def visit_row(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        table_context.current_col = 0
        self.top.put_body('|')

    def depart_row(self, node):
        self.top.put_body('\n')

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        self.top.put_body('|')
        for col_width in table_context.cols:
            delim = col_width * '-'
            delim += '|'
            self.top.put_body(delim)
        self.top.put_body('\n')

    def visit_tbody(self, node):
        LOG.debug('Not implemented tbody')

    def depart_tbody(self, node):
        LOG.debug('Not implemented tbody')

    def visit_entry(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        table_context.current_col += 1

    def depart_entry(self, node):
        self.top.put_body('|')

    def visit_caption(self, node):
        pass

    def depart_caption(self, node):
        self.top.put_body('\n')

    def visit_label(self, node):
        self.top.put_body("\[")

    def depart_label(self, node):
        self.top.put_body("\] ")

    def visit_footnote(self, node):
        d = node.attrib['docname']
        b = node.attrib['backrefs']
        link = f'\n\n<a name="{d}-{b}"></a>\n'
        self.top.put_body(link)
        pass

    def depart_footnote(self, node):
        pass

    def visit_footnote_reference(self, node):
        self.top.put_body("<sup>[\[")

    def depart_footnote_reference(self, node):
        d = node.attrib['docname']
        b = node.attrib['ids']
        link = f'#{d}-{b}'
        self.top.put_body(f"\]]({link})")

    def visit_transition(self, node):
        LOG.debug('Not implemented transition')

    def depart_transition(self, node):
        LOG.debug('Not implemented transition')

    def visit_classifier(self, node):
        LOG.debug('Not implemented classifier')

    def depart_classifier(self, node):
        LOG.debug('Not implemented classifier')

    def visit_figure(self, node):
        LOG.debug('Not implemented figure')

    def depart_figure(self, node):
        LOG.debug('Not implemented figure')

    #  RAW HTML ELEMENTS?
    def _raw_html(self, node):
        attribs = []
        for key in node.attrib:
            attribs.append(f' {key}="{node.attrib[key]}"')
        v = "".join(attribs)
        value = f"<{node.tag}{v}>"
        self.top.put_body(value)

    def visit_script(self, node):
        pass  # no scripts, we're not using the old sphinx stuff any more

    def depart_script(self, node):
        pass  # no scripts, thanks

    def visit_style(self, node):
        pass  # don't think we need the style sheets from sphinx either

    def depart_style(self, node):
        pass

    def visit_iframe(self, node):
        self._raw_html(node)

    def depart_iframe(self, node):
        self.top.put_body(f"</{node.tag}>\n\n")

    def visit_p(self, node):
        self._raw_html(node)

    def depart_p(self, node):
        self.top.put_body(f"</{node.tag}>\n")

    def visit_embed(self, node):
        self._raw_html(node)

    def depart_embed(self, node):
        self.top.put_body(f"</{node.tag}>\n\n")

    def visit_a(self, node):
        self._raw_html(node)

    def depart_a(self, node):
        self.top.put_body(f"</{node.tag}>")

    def visit_button(self, node):
        self._raw_html(node)

    def depart_button(self, node):
        self.top.put_body(f"</{node.tag}>")

    def visit_toctree(self, node):
            LOG.debug('Not implemented toctree')

    def depart_toctree(self, node):
            LOG.debug('Not implemented toctree')


# NOT A CLASS MEMBER
def visit_unsupported(self, node):
    print(f"Unsupported {node.tag}")


def configure_translator(filename):
    s = set()

    tree = ET.parse(filename)
    for e in tree.iter():
        s.add(e.tag)

    failed = False
    for tag in s:
        if hasattr(Translator, f'visit_{tag}'):
            continue

        # Not supported.
        setattr(Translator, f'visit_{tag}', visit_unsupported)

        #  Output what the user needs to implement to support it
        print("")
        print(f"\tdef visit_{tag}(self, node):\n\t\tLOG.debug('Not implemented {tag}')")
        print("")
        print(f"\tdef depart_{tag}(self, node):\n\t\tLOG.debug('Not implemented {tag}')")

        failed = True

    if failed:
        LOG.error(f"Add missing directives to continue.  Found when processing {filename}")
        sys.exit(1)


def write_frontmatter(f, title):
    f.write('---\n')
    f.write(f'title: "{title}"\n')
    f.write("date: 2020-01-08T09:59:25Z\n")
    f.write('---\n')


def convert_one_xml_to_hugo(filename):
    LOG.debug(f"Processing {filename}")
    if ARGS.md:
        cms = Markdown()
    else:
        cms = Hugo()

    try:
        configure_translator(filename)
        t = Translator(cms)
        t.walk(filename)

        md = str(filename).replace('.xml', '.md')
        with open(md, 'w') as f:
            write_frontmatter(f, t.title)
            f.write(t.astext())
    except ParseError as e:
        line, col = e.position
        LOG.error(f"When processing: {filename}:{line}")
        raise


def convert_xml_to_hugo():
    LOG.warning("Converting all xml => md")

    files = [x for x in Path(REPOS).rglob('xml/xml/**/*.xml')]
    for x in files:
        convert_one_xml_to_hugo(x)

    LOG.warning(f"Processed {len(files)} files")


def run_sphinx(src_dir):
    src = os.path.abspath(src_dir)
    dest = os.path.join(os.path.dirname(src), 'xml')

    #  Always rebuild (-a)
    #  Set xmlmode tag to pull out the rest of the HTML output
    args = ["-M", "xml", src, dest, "-a", "-t", "xmlmode"]
    retval = sphinx_main(args)
    if retval != 0:
        sys.exit(retval)

    return dest


def _search_and_replace(files, replacements):
    for file in files:
        LOG.debug(f"Checking {file}")
        lines = open(file, 'r').readlines()
        updated = False
        count = 0
        for line in lines:
            for (value, new_value) in replacements:
                if value in line:
                    line = line.replace(value, new_value)
                    lines[count] = line
                    updated = True
                    LOG.debug(f"Replaced! {value} with {new_value}")
            count += 1
        if updated:
            LOG.info(f"Rewritten file {file}")
            open(file, 'w').writelines(lines)


def preprocess(d):
    LOG.debug(f"Pre-processing {d}")
    replacements = [('.. raw:: html', '.. raw:: xml'), ('.. only:: html', '.. only:: xml')]
    files = [x for x in Path(d).rglob('*.rst')]
    _search_and_replace(files, replacements)


def postprocess(d):
    LOG.debug(f"Post-processing {d}")
    # Also matches: webkitallowfullscreen and mozallowfullscreen
    replacements = [
        ('allowfullscreen', 'allowfullscreen="true"'),
        ('&nbsp;', ' '),
        ('<br>', '')
    ]
    files = [x for x in Path(d).rglob('*.xml')]
    _search_and_replace(files, replacements)


def convert_rst_to_xml():
    LOG.warning("Converting all rst => xml using sphinx")
    dirs = [x for x in Path(REPOS).rglob('docs/source')]
    for d in dirs:
        LOG.warning(f"Converting {d}")
        preprocess(d)
        run_sphinx(d)

    _postprocess_xml()


def _postprocess_xml():
    for d in [x for x in Path(REPOS).rglob('xml/xml')]:
        postprocess(d)


def copy_to_content():
    LOG.warning("Copying all md to content/")

    dirs = []
    files = [x for x in Path(REPOS).rglob('xml/xml/**/*.md')]
    for src in files:
        dest = str(src).replace('docs/xml/xml/', '').replace(REPOS, CONTENT)
        src_filename = os.path.basename(src)
        index_md = os.path.join(os.path.dirname(dest), '_index.md')
        if src_filename == 'index.md':
            LOG.warning(f"Copying {src} to {dest}")
            dest = index_md # it was 'index.rst', copying to '_index.md'
        elif src_filename.endswith('index.md') and not os.path.exists(index_md):
            # was something-index.rst, copying to _index.md
            # fixes some of Ed's weird filenames
            LOG.warning(f"Copying {src} to {dest}")
            dest = index_md

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)

        LOG.debug(f"Copying {src} {dest}")
        shutil.copyfile(src, dest)
        if os.path.dirname(dest) not in dirs:
            dirs.append(os.path.dirname(dest))

    LOG.warning(f"Copied {len(files)} files")
    add_missing_index_md_files(dirs)


def add_missing_index_md_files(dirs):
    for dir in dirs:
        index_md = os.path.join(dir, '_index.md')
        if not os.path.exists(index_md):
            LOG.warning(f"Writing missing {index_md}")
            with open(index_md, 'w') as f:
                write_frontmatter(f, os.path.basename(dir))


def copy_resources_to_content():
    LOG.warning("Copying all resources to content/")

    for d in ['_static', 'resources']:
        dirs = [x for x in Path(REPOS).rglob(f'docs/source/{d}')]
        for src in dirs:
            dest = str(src).replace(f'docs/source/{d}', d).replace(REPOS, CONTENT)
            if not os.path.exists(dest):
                LOG.info(f"Copying {src} {dest}")
                copy_tree(src, dest)
            else:
                files = [str(p.parent) for p in Path(dest).rglob('*') if p.is_file()]
                #if len(files) == 0:
                LOG.info(f"Copying {src} {dest}")
                copy_tree(src, dest)
                # else:
                #     LOG.warning(f"Dest exists, not copying {src} to {dest}")

    LOG.warning(f"Copied resources")


def main():
    global ARGS
    desc = "Convert rst files to md using sphinx"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--toc", "-t", help="include table of contents in the page", default=False, action='store_true')
    parser.add_argument("--skip", "-s", help="skip rst conversion for speed if already done", default=False, action='store_true')
    parser.add_argument("--md", "-m", help="generate (commonmark) markdown with fewer hugo tags", default=False, action='store_true')
    ARGS = parser.parse_args()

    _setup_logging()

    LOG.warning(f"You need to clone the repositories you wish to convert to {REPOS}")
    LOG.warning(f"You also need to then git checkout the branch you want.")
    LOG.warning(f"There is a script that does this - get_repos.sh")

    if not ARGS.skip:
        convert_rst_to_xml()
    else:
        LOG.warning("Skipping rst-to-xml")
    convert_xml_to_hugo()

    # filename = "/home/barry/dev/r3/sphinx2hugo/repos/en/docs/corda-os/4.4/docs/xml/xml/key-concepts-notaries.xml"
    # filename = '/home/barry/dev/r3/sphinx2hugo/repos/en/docs/cenm/1.1/docs/xml/xml/cenm-support-matrix.xml'
    # filename = "/home/barry/dev/r3/sphinx2hugo/repos/en/docs/corda-os/4.4/docs/xml/xml/api-contracts.xml"
    filename = "/home/barry/dev/r3/sphinx2hugo/repos/en/docs/corda-os/4.4/docs/xml/xml/api-flows.xml"
    # # filename = "/home/barry/dev/r3/sphinx2hugo/repos/en/docs/corda-os/4.4/docs/xml/xml/key-concepts-contracts.xml"
    # convert_one_xml_to_hugo(filename)

    copy_to_content()
    copy_resources_to_content()


if __name__ == '__main__':
    main()
