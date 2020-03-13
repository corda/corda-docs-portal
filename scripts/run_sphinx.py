#!/usr/bin/env python3

import logging
import os
import shutil
import sys
import re
import argparse
from pathlib import Path
import toml
import yaml
import hashlib

from sphinx.cmd.build import main as sphinx_main
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from distutils.dir_util import copy_tree

from utils.parse_menus import parse_indexes, version, version_for_config
from utils.parse_literal_includes import parse_literal_includes, md_relpath, github_shortcode_for

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
REPOS = os.path.join(ROOT, "repos")
CONTENT = os.path.join(ROOT, "content")
REPOS_ROOT = os.path.join(REPOS, "en/docs") # don't rely on this.

LOG = logging.getLogger(__name__)
ARGS = None

# Menus that we'll read from the .rst files and add into hugo
MENU_FILES = {}
INCLUDES = {}

# If we're in one of these, don't add new lines.
NO_NEWLINE_ELEMENTS = ["bullet_list", "enumerated_list", "definition_list", "entry", "list_item"]

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


def _path_to_github_url(path):
    """ Path-to-source is based on where we checked code in the get_repos.sh script """

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
        assert False, f"No such repo: {relpath}"

    return f"https://github.com/corda/{repo}/blob/{relpath}"


class Markdown:
    """  All opening html elements *seem* to require a clear blank line between it and the content
    so all opening divs are suffixed with \n\n
    """

    def __init__(self):
        self.name = 'md'

    def image(self, url, alt):
        return f'![{alt}]({url} "{alt}")'

    def link(self, url, text):
        return f'[{text}]({url})'

    def comment(self, text):
        return f'<-- {text} -->'

    def toc(self):
        return self.comment("page table of contents tags_to_removed")

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
        return '\n</div>\n'

    def visit_tabs(self, idx):
        return f'<div class="r3-tabs" id="tabs-{idx}">\n\n'

    def depart_tabs(self):
        return '\n</div>\n'

    def visit_note(self):
        return '<div class="r3-o-note" role="alert"><span>Note: </span>\n\n'

    def depart_note(self):
        return '\n</div>\n'

    def visit_tip(self):
        return '<div class="r3-o-note" role="alert"><span>Note: </span>\n\n'

    def depart_tip(self):
        return '\n</div>\n'

    def visit_warning(self):
        return '<div class="r3-o-warning" role="alert"><span>Warning: </span>\n\n'

    def depart_warning(self):
        return '\n</div>\n'

    def visit_attention(self):
        return '<div class="r3-o-attention" role="alert"><span>Attention: </span>\n\n'

    def depart_attention(self):
        return '\n</div>\n'

    def visit_important(self):
        return '<div class="r3-o-important" role="alert"><span>Important: </span>\n\n'

    def depart_important(self):
        return '\n</div>\n'

    def visit_topic(self):
        return '<div class="r3-o-topic" role="alert"><span>Topic: </span>\n\n'

    def depart_topic(self):
        return '\n</div>\n'

    def visit_table(self):
        return '\n<div class="table table-sm table-striped table-hover">\n\n'

    def depart_table(self):
        return '\n</div>\n\n'

    def visit_tabs_header(self):
        return "<!-- tabs header end -->"

    def depart_tabs_header(self):
        return "<!-- tabs header end -->"

    def tab_header(self, label, idx):
        return f"<!-- tab header {label} {idx} -->"


class Gatsby(Markdown):
    """  Override raw Markdown with Hugo shortcodes  """

    def __init__(self, *args, **kwargs):
        super(Gatsby, self).__init__(**kwargs)
        self.name = 'gatsby'
        self.tab_index = 0

    def visit_tab(self, lang):
        return '<TabPanel value={value} index={' + str(self.tab_index) + '}>\n\n'

    def depart_tab(self):
        self.tab_index += 1
        return '\n</TabPanel>\n'

    def visit_tabs(self, idx):
        return f'<div>'

    def depart_tabs(self):
        self.tab_index = 0
        return '\n</div>\n'

    def visit_tabs_header(self):
        return '<Tabs value={value} aria-label="code tabs">'

    def depart_tabs_header(self):
        return "</Tabs>"

    def tab_header(self, label, idx):
        return f'<Tab label="{label}" />'


class Hugo(Markdown):
    """  Override raw Markdown with Hugo shortcodes  """

    def __init__(self, *args, **kwargs):
        super(Hugo, self).__init__(**kwargs)
        self.name = 'hugo'

    # def image(self, url, alt):
    #     f'{{{{< img src="{url}" alt="{alt}" >}}}}\n\n'

    def visit_tabs(self, idx):
        return f'{{{{< tabs name="tabs-{idx}" >}}}}'

    def depart_tabs(self):
        return "{{< /tabs >}}\n"

    def visit_tab(self, lang):
        return f'{{{{% tab name="{lang}" %}}}}\n'

    def depart_tab(self):
        return f'{{{{% /tab %}}}}\n'

    def comment(self, s):
        return f"\n{{{{/* {s} */}}}}\n"

    def visit_note(self):
        return "{{< note >}}"

    def depart_note(self):
        return "{{< /note >}}"

    def visit_warning(self):
        return "\n{{< warning >}}"

    def depart_warning(self):
        return "{{< /warning >}}\n\n"

    def visit_attention(self):
        return "\n{{< attention >}}\n"

    def depart_attention(self):
        return "\n{{< /attention >}}\n"

    def visit_tip(self):
        return "\n{{< attention >}}\n"

    def depart_tip(self):
        return "\n{{< /attention >}}\n"

    def visit_important(self):
        return "\n{{< important >}}"

    def depart_important(self):
        return "\n{{< /important >}}\n"

    def visit_topic(self):
        return "\n{{< topic >}}"

    def depart_topic(self):
        return "\n{{< /topic >}}"

    def visit_table(self):
        return "\n{{< table >}}\n"

    def depart_table(self):
        return "\n{{< /table >}}\n"

    def visit_tabs_header(self):
        return None

    def depart_tabs_header(self):
        return None

    def tab_header(self, label, idx):
        return None


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


class Translator:
    def __init__(self, cms):
        self._context = [Context()]
        self.cms = cms
        self.filename = None # populated by walk()

        # For determining h1/h2/h3 etc.
        self.section_depth = 0
        self.tabs_counter = 0

        # To look up the values from the original rst since XML doesn't preserve the info.
        self.literal_include_count = 0

        # We shouldn't have nested containers so this should be enough for tabbed code panes.
        self.in_tabs = False

        self._elements = [None]
        self._ordered_list = [0]

        self.front_matter = {"date": "2020-01-08T09:59:25Z"}

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

    """ reset some elements to contain exactly nothing so we don't
    render erroneous newlines """
    def _reset_element(self, e):
        e.text = ''
        e.tail = ''

    def _walk(self, parent):
        for e in parent:
            self.push_element(e.tag)
            visit_func = getattr(self, f'visit_{e.tag}', visit_unsupported)
            depart_func = getattr(self, f'depart_{e.tag}', visit_unsupported)

            self.push_context(Context())

            visit_func(e)

            if e.text:
                self.top.put_body(e.text)

            self._walk(e)

            depart_func(e)

            if e.tail:
                self.top.put_body(e.tail)

            self.pop_context()
            self.pop_element()

    def walk(self, filename):
        if os.path.basename(os.path.dirname(filename)) == "resources":
            LOG.info(f"Not processing {filename} as in wrong folder")
            return

        tree = ET.parse(filename)
        self.filename = filename
        self._walk([tree.getroot()])
        self._add_front_matter()

    def _fix_up_javadoc(self, link):
        LOG.debug("TODO: fix up javadoc")
        return '#'

    """ Add in some front-matter tags derived from the file """
    def _add_front_matter(self):
        dirs = str(self.filename).split("/")
        #  locate 'docs'
        while dirs[0] != "docs":
            dirs.pop(0)

        # "version" that this page is in/under, e.g. corda-os-4-3
        # we CANNOT have '.' in a 'toml' config section name - that implies hierarchy
        project_name = dirs[1]
        semantic_version = dirs[2]
        version = (project_name + "-" + semantic_version).replace(".", "-")
        filename_only = os.path.basename(os.path.splitext(self.filename)[0])
        dest_file = str(self.filename).replace('docs/xml/xml/', '').replace(".xml", ".md")
        html_relpath = "/" + "/".join(dirs[3:]).replace(".xml", ".html").replace('docs/xml/xml/', '')
        md_relpath = "/".join(dirs[3:]).replace(".xml", ".md").replace('docs/xml/xml/', '')

        self._add_aliases_to_front_matter(project_name, semantic_version, html_relpath)

        is_version_index = self._rewrite_index_title_in_front_matter(dest_file, filename_only)

        # Menu entries that this page should occur in:
        menu = self.front_matter.get("menu", {})

        # Try and automatically group together some pages to get us
        # started with hugo menus
        # Specifically figure out what this menu should be.
        # Add each menu as a dict
        menu_entry = {}
        files_for_version = MENU_FILES.get(version, {})
        parent = files_for_version.get(md_relpath, None)
        if parent:
            menu_entry = {"parent": parent}
        else:
            menu_entry = None
        #
        # if filename_only.startswith("api-"):
        #     menu_entry = { "parent": version + "-api" }
        # elif filename_only.startswith("key-concepts-"):
        #     menu_entry = { "parent": version + "-concepts" }
        # elif filename_only.startswith("node-"):
        #     menu_entry = { "parent": version + "-node" }
        # elif filename_only.startswith("tutorial-"):
        #     menu_entry = { "parent": version + "-tutorial" }
        # elif filename_only.startswith("config-"):
        #     menu_entry = { "parent": version + "-config" }

        # Are we a (project+version) section/index page? e.g. if 4.4/index
        if bool(is_version_index):
            LOG.info(f"Adding {self.filename} to 'versions' menu")
            versions_menu_entry = {}
            LOG.info(f"Adding parameter 'section_menu={version}' for this index page only'")
            self.front_matter["section_menu"] = version
            self.front_matter["version"] = semantic_version
            self.front_matter["project"] = project_name
            # Ordering in the versions menu
            if project_name == "cenm":
                versions_menu_entry["weight"] = (100 - int(float(semantic_version)*10)) + 1000
            elif project_name == "corda-os":
                versions_menu_entry["weight"] = (100 - int(float(semantic_version)*10)) + 500
            if project_name == "corda-enterprise":
                versions_menu_entry["weight"] = (100 - int(float(semantic_version)*10)) + 100
            menu["versions"] = versions_menu_entry

        # Add this page as a menu entry for the given
        # 'section menu', i.e. { "corda-os-4-3": { ... } }
        if menu_entry is not None:
            menu[version] = menu_entry

        # If all the menu values are empty dictionaries, we can safely use a list
        # of menus we belong to instead.  This more human-friendly.
        if all(not bool(v) for __, v in menu.items()):
            menu = [k for k, __ in menu.items()]

        # Add menu entry(-ies) to front matter
        self.front_matter["menu"] = menu

        # Finally, handle missing page titles, if any
        # use the filename (no extension) if the title is missing.
        if "title" not in self.front_matter:
            self.front_matter["title"] = filename_only

        self._front_matter_add_tags_and_categories(filename_only)

    def _rewrite_index_title_in_front_matter(self, dest_file, filename_only):
        dirname_only = os.path.basename(os.path.dirname(dest_file))
        project_only = os.path.basename(os.path.dirname(os.path.dirname(dest_file)))
        # Are we parsing the index file under <project>/MAJOR.MINOR?
        is_version_index = filename_only == "index" and bool(re.findall(r"\d\.\d", dirname_only))
        # Yes?  Rewrite the front matter titles to something consistent
        if bool(is_version_index):
            if project_only == "corda-os":
                self.front_matter["title"] = "Corda OS " + dirname_only
            elif project_only.startswith("corda-ent"):
                self.front_matter["title"] = "Corda Enterprise " + dirname_only
            elif project_only == "cenm":
                self.front_matter["title"] = "CENM " + dirname_only
            else:
                LOG.error(f"Could not rewrite section title for {project_only}")

        return bool(is_version_index)

    def _add_aliases_to_front_matter(self, project_name, semantic_version, relpath):
        #  Add page redirect aliases such as docs.corda.net alias in case we get deployed there.
        #  Oh joy.  Couldn't make it up really..
        if project_name == "corda-os":
            self.front_matter["aliases"] = ["/releases/release-V" + semantic_version + relpath]
            # don't add the open-source defaut-without-a-version links, because they're duplicated
            # by enterprise, so just redirect there instead.
        elif project_name.startswith("corda-ent"):
            self.front_matter["aliases"] = ["/releases/" + semantic_version + relpath]
            if semantic_version == "4.3":  # latest old release
                self.front_matter["aliases"].append(relpath)
        elif project_name.startswith("cenm"):  # latest old release
            self.front_matter["aliases"] = ["/releases/release-" + semantic_version + relpath]
            if semantic_version == "1.1":
                self.front_matter["aliases"].append(relpath)

    """  Add some tags based on the filename into the front matter
    and add some reasonable categories too """
    def _front_matter_add_tags_and_categories(self, filename_only):
        tags_to_remove = ['index', '_index', 'and', 'a', 'the', 'if', 'key', 'hello', 'world', 'toc', 'toctree', 'one', 'two', 'three', 'up', 'with', 'dir' 'docs', 'eta', 'non', 'reg', 'reqs', 'run', 'runs', 'sub', 'soft', 'tree', 'to', 'up', 'writing']

        tags = filename_only.split("-")
        for r in tags_to_remove:
            if r in tags: tags.remove(r)

        if tags:
            self.front_matter['tags'] = tags

    ###########################################################################
    # Visitors
    ###########################################################################

    #  Some we use, but sphinx renders into the simplified output (such as
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
        self._reset_element(node)

    def depart_section(self, node):
        self.section_depth -= 1

    def visit_title(self, node):
        h = self.section_depth * '#'
        self.top.put_body('\n' + h + ' ')

    def depart_title(self, node):
        if self.section_depth == 1 and 'title' not in self.front_matter:
            self.front_matter['title'] = node.text

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
        self._reset_element(node)

    def depart_definition(self, node):
        pass

    def visit_reference(self, node):
        self.push_context(Context())

    def depart_reference(self, node):
        text = "".join(self.top.body)
        self.top.body = []
        self.pop_context()

        link = '#'
        if 'refuri' in node.attrib:
            uri = node.attrib['refuri']
            link = uri
            # Could be a local path or another page
            if not link.startswith('http'):
                non_fragment = link.split('#')[0]
                __, ext = os.path.splitext(non_fragment)
                # If it doesn't have a suffix, it's another page
                if not ext:
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
            # Anchor link to the same page
            link = '#' + node.attrib['refid']

        self.top.put_body(self.cms.link(link, text))

    def visit_definition_list_item(self, node):
        self._reset_element(node)

    def depart_definition_list_item(self, node):
        pass

    def visit_strong(self, node):
        self.top.put_body(self.cms.visit_strong())

    def depart_strong(self, node):
        self.top.put_body(self.cms.depart_strong())

    def visit_bullet_list(self, node):
        self._reset_element(node)

    def depart_bullet_list(self, node):
        node.tail = '\n\n'

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

    """ convert to ```java  [lines]   ``` """
    def visit_literal_block(self, node):
        lang = node.attrib.get('language', '')
        if self.in_tabs:
            self.top.put_head(lang)
            self.top.put_body(self.cms.visit_tab(lang))
        self.top.put_body(self.cms.visit_literal_block(lang) + '\n')

    def depart_literal_block(self, node):
        self.top.put_body('\n' + self.cms.depart_literal_block() + '\n')
        if self.in_tabs:
            self.top.put_body(self.cms.depart_tab())

        if node.attrib.get('source', None):
            src = node.attrib['source']

            key = version_for_config(self.filename)
            lookup = INCLUDES[key] # now have a dict of relpath-md to [ literalinclude, ... ]
            relpath = md_relpath(self.filename)
            literal_includes = lookup.get(relpath, None)

            if literal_includes:
                self.top.put_body(github_shortcode_for(self.literal_include_count, literal_includes))

            if self.in_tabs:
                #  append each one in the footer so it appears beneath the 'tabs' collection, rather
                #  than under the tab
                self.top.put_foot(self.cms.link(_path_to_github_url(src), os.path.basename(src)))
            else:
                # not in a collection, put it straight under the 'tab' (which) doesn't exist
                self.top.put_body(self.cms.link(_path_to_github_url(src), os.path.basename(src)))

            self.literal_include_count += 1

    def visit_inline(self, node):
        pass

    def depart_inline(self, node):
        pass

    def visit_container(self, node):
        self.in_tabs = True
        self.tabs_counter += 1
        self.top.put_body(self.cms.visit_tabs(self.tabs_counter))
        # We are putting the links to the source in each tab in the footer.
        # Similarly we store the tab title in the header (even if we don't use it)
        self.push_context(Context())

    def depart_container(self, node):
        # Gather up any source code links, and add them to the end.
        if (self.top.foot):
            self.top.foot.append(self.cms.image("/images/svg/github.svg", "github"))
            md = "\n" + " | ".join(self.top.foot) + "\n\n"
        else:
            md = None

        tabs_header = []
        tabs_header.append(self.cms.visit_tabs_header())
        idx = 0
        for item in self.top.head:
            tabs_header.append(self.cms.tab_header(item, idx))
            idx += 1
        tabs_header.append(self.cms.depart_tabs_header())
        tabs_header = [x for x in tabs_header if x is not None]
        self.top.body = tabs_header + self.top.body

        self.top.foot = []
        self.top.head = []
        self.pop_context() # tab content was written to top which we're now popping.
        if md:
            self.top.body.append(md)

        self.top.put_body(self.cms.depart_tabs())
        self.in_tabs = False

    def visit_definition_list(self, node):
        self._reset_element(node)

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
        node.tail = ""

    def depart_paragraph(self, node):
        if not any([item in self._elements for item in NO_NEWLINE_ELEMENTS]):
            node.tail = "\n\n"

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
        self._reset_element(node)

    def depart_enumerated_list(self, node):
        node.tail = '\n\n'

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
        bullet_depth = sum([1 for e in self._elements if e in ['bullet_list']]) - 1
        padding = '    ' * bullet_depth

        bullet = '*'
        # lists = [e for e in reversed(self._elements) if e == "bullet_list" or e == "enumerated_list"]
        # if lists and lists[0] == "enumerated_list":
        #     bullet = '1.'

        self.top.put_body('\n' + padding + bullet + ' ')

        self._reset_element(node)

    def depart_list_item(self, node):
        # # Remove new line from 'previous' otherwise we end up with '*' and ' <words..>' on different lines in markdown
        # if '\n' in self.top.body[1]:
        #     self.top.body[1] = self.top.body[1].replace('\n', '')
        self.pop_context()

    def visit_term(self, node):
        self._reset_element(node)

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
        self.visit_paragraph

    def depart_compact_paragraph(self, node):
        self.depart_compact_paragraph

    def visit_compound(self, node):
        LOG.debug('Not implemented compound')

    def depart_compound(self, node):
        LOG.debug('Not implemented compound')

    def visit_field_list(self, node):
        self.visit_bullet_list(node)
        # LOG.debug('Not implemented field_list')

    def depart_field_list(self, node):
        self.depart_bullet_list(node)
        # LOG.debug('Not implemented field_list')

    def visit_field(self, node):
        self.visit_list_item(node)
        # LOG.debug('Not implemented field')

    def depart_field(self, node):
        self.depart_list_item(node)
        LOG.debug('Not implemented field')

    def visit_field_body(self, node):
        self.top.put_body(": ")
        node.tail = ''
        # LOG.debug('Not implemented field_body')

    def depart_field_body(self, node):
        pass
        # LOG.debug('Not implemented field_body')

    def visit_field_name(self, node):
        self.top.put_body(self.cms.visit_strong())
        node.tail = ''

    def depart_field_name(self, node):
        self.top.put_body(self.cms.depart_strong())

    def visit_important(self, node):
        self.top.put_body(self.cms.visit_important())

    def depart_important(self, node):
        self.top.put_body(self.cms.depart_important())

    def visit_problematic(self, node):
        self.top.put_body(self.cms.visit_warning())

    def depart_problematic(self, node):
        self.top.put_body(self.cms.depart_warning())

    def visit_line_block(self, node):
        LOG.debug('Not implemented line_block')

    def depart_line_block(self, node):
        LOG.debug('Not implemented line_block')

    def visit_line(self, node):
        LOG.debug('Not implemented line')

    def depart_line(self, node):
        LOG.debug('Not implemented line')

    def visit_table(self, node):
        self.top.put_body(self.cms.visit_table())
        self.push_context(TableContext())

    def depart_table(self, node):
        self.top.put_body(self.cms.depart_table())
        self.pop_context()

    def visit_colspec(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        if not table_context:
            raise RuntimeError("Expected a TableContext on the stack")
        col_width = int(node.attrib.get('colwidth'), 0)
        assert col_width != 0, "No col width?"

        table_context.cols.append(col_width)
        self._reset_element(node)

    def depart_colspec(self, node):
        pass

    def visit_tgroup(self, node):
        self._reset_element(node)

    def depart_tgroup(self, node):
        pass

    def visit_row(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        table_context.current_col = 0
        self.top.put_body('|')
        self._reset_element(node)

    def depart_row(self, node):
        self.top.put_body('\n')

    def visit_thead(self, node):
        self._reset_element(node)

    def depart_thead(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        self.top.put_body('|')
        for col_width in table_context.cols:
            delim = col_width * '-'
            delim += '|'
            self.top.put_body(delim)
        self.top.put_body('\n')

    def visit_tbody(self, node):
        self._reset_element(node)

    def depart_tbody(self, node):
        LOG.debug('Not implemented tbody')

    def visit_entry(self, node):
        table_context = next((ctx for ctx in (reversed(self._context)) if isinstance(ctx, TableContext)), None)
        table_context.current_col += 1
        self._reset_element(node)

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

    def visit_tip(self, node):
        self.top.put_body(self.cms.visit_tip())

    def depart_tip(self, node):
        self.top.put_body(self.cms.depart_tip())

    def visit_b(self, node):
        self.top.put_body(self.cms.visit_strong())

    def depart_b(self, node):
        self.top.put_body(self.cms.depart_strong())

    def visit_center(self, node):
        LOG.debug('Not implemented center')

    def depart_center(self, node):
        LOG.debug('Not implemented center')

############################################################################
#  END OF CLASS

# NOT A CLASS MEMBER
def visit_unsupported(self, node):
    print(f"Unsupported {node.tag}")


def configure_translator(filename):
    s = set()

    try:
        tree = ET.parse(filename)
    except Exception as e:
        print(f"When processing: f{filename}")
        raise(e)

    for e in tree.iter():
        s.add(e.tag)

    failed = False
    for tag in s:
        if hasattr(Translator, f'visit_{tag}'):
            continue

        # Not supported.
        setattr(Translator, f'visit_{tag}', visit_unsupported)

        #  Output what the user needs to implement to support it
        print("PASTE THIS IN TO THE PYTHON\n\n\n")
        print(f"\tdef visit_{tag}(self, node):\n\t\tLOG.debug('Not implemented {tag}')")
        print("")
        print(f"\tdef depart_{tag}(self, node):\n\t\tLOG.debug('Not implemented {tag}')")

        failed = True

    if failed:
        LOG.error(f"Add missing directives to continue.  Found when processing {filename}")
        sys.exit(1)


def write_frontmatter(f, front_matter):
    if ARGS.toml:
        f.write('+++\n')
        f.write(toml.dumps(front_matter))
        f.write('+++\n')
    else:
        # YAML renders in github
        f.write('---\n'),
        f.write(yaml.dump(front_matter))
        f.write('---\n')


def convert_one_xml_file_to_cms_style_md(cms, filename):
    LOG.debug(f"Processing {filename}")

    try:
        configure_translator(filename)
        t = Translator(cms)
        t.walk(filename)

        md = str(filename).replace('.xml', '.md')
        with open(md, 'w') as f:
            write_frontmatter(f, t.front_matter)
            f.write(t.astext())
    except ParseError as e:
        line, col = e.position
        LOG.error(f"When processing: {filename}:{line}")
        raise


def convert_all_xml_to_md(cms):
    LOG.warning("Converting all xml => md")

    files = [x for x in Path(REPOS).rglob('xml/xml/**/*.xml')]
    for x in files:
        convert_one_xml_file_to_cms_style_md(cms, x)

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
        if not os.path.isfile(file):
            continue
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
            LOG.debug(f"Rewritten file {file}")
            open(file, 'w').writelines(lines)


def preprocess(d):
    LOG.debug(f"Pre-processing {d}")
    replacements = [('.. raw:: html', '.. raw:: xml'), ('.. only:: html', '.. only:: xml')]
    files = [x for x in Path(d).rglob('*.rst')]
    _search_and_replace(files, replacements)


def _postprocess_xml_files(d):
    LOG.debug(f"Post-processing {d}")
    # Also matches: webkitallowfullscreen and mozallowfullscreen
    replacements = [
        ('allowfullscreen', 'allowfullscreen="true"'),
        ('&nbsp;', ' '),
        ('<br>', '')
    ]
    files = [x for x in Path(d).rglob('*.xml')]
    _search_and_replace(files, replacements)

    #  Get rid of all the unnecessary leading whitespace in XML formatting except for code blocks
    for file in files:
        lines = open(file, 'r').readlines()
        new_lines = []
        save = False
        in_literal_block = False
        for line in lines:
            if not in_literal_block:
                line = line.lstrip()
                save = True
            if line.lstrip().startswith('<literal_block'):
                in_literal_block = True
            if '</literal_block>' in line:
                in_literal_block = False
                print(line)

            new_lines.append(line)

        if save:
            open(file, 'w').writelines(new_lines)


def convert_rst_to_xml():
    LOG.warning("Converting all rst => xml using sphinx")
    dirs = [x for x in Path(REPOS).rglob('docs/source')]
    for d in dirs:
        LOG.warning(f"Converting {d}")
        preprocess(d)
        run_sphinx(d)


def postprocess_xml():
    LOG.warning("Post-processing all XML")
    for d in [x for x in Path(REPOS).rglob('xml/xml')]:
        _postprocess_xml_files(d)
    LOG.warning("Post-processing all XML finished")


def _remove_junk_that_breaks_hugo():
    root = os.path.join(REPOS, "en/docs/corda-enterprise/4.2/docs/")
    for f in ["source/resources/nodefull.md", "xml/xml/resources/nodefull.md"]:
        pathname = os.path.join(root, f)
        if os.path.exists(pathname): os.unlink(pathname)


def copy_to_content(cms):
    LOG.warning("Copying all md to content/")

    _remove_junk_that_breaks_hugo()

    dirs = []
    files = [x for x in Path(REPOS).rglob('xml/xml/**/*.md')]
    for src in files:
        dest = str(src).replace('docs/xml/xml/', '').replace(REPOS, CONTENT)
        src_filename = os.path.basename(src)
        dirname_only = os.path.basename(os.path.dirname(dest))

        # We need to rename index pages to _index.md (page bundle = section)
        # for hugo when we're in MAJOR.MINOR folders
        # otherwise, we're a plain-old "leaf bundle"
        if ARGS.cms == "hugo" and re.findall(r"\d\.\d", dirname_only):

            index_md = os.path.join(os.path.dirname(dest), '_index.md')

            if src_filename == 'index.md':
                LOG.info(f"Copying {src} to {dest}")
                dest = index_md  # it was 'index.rst', copying to '_index.md'

        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest), exist_ok=True)

        if dest.endswith("_index.md"):
            LOG.info(f"Copying {src} {dest}")

        LOG.debug(f"Copying {src} {dest}")
        shutil.copyfile(src, dest)
        if os.path.dirname(dest) not in dirs:
            dirs.append(os.path.dirname(dest))

    LOG.warning(f"Copied {len(files)} files")


def copy_resources_to_content():
    LOG.warning("Copying all resources to content/")

    for d in ['_static', 'resources']:
        dirs = [x for x in Path(REPOS).rglob(f'docs/source/{d}')]
        for src in dirs:
            dest = str(src).replace(f'docs/source/{d}', d).replace(REPOS, CONTENT)
            LOG.debug(f"Copying {src} {dest}")
            copy_tree(src, dest)

    LOG.warning(f"Copied resources")

    _replace_duplicate_resources()


def _get_duplicate_resources_by_hash():
    d = {}
    exts = [".pdf", ".png", ".gif", ".jpg"]
    for pathname in [x for x in Path(os.path.join(CONTENT, 'en')).rglob(f'**/*')]:
        ext = os.path.splitext(pathname)[1]
        if ext not in exts:
            continue
        hash = _hash_file(pathname)
        paths = d.get(hash, [])
        paths.append(pathname)
        d[hash] = paths

    return [paths for __, paths in d.items() if len(paths) > 1]


def _replace_duplicate_resources():
    LOG.warning("Removing duplicate resources")
    list_of_paths = _get_duplicate_resources_by_hash()
    # All extensions (above) that are repeated in 2 or more projects
    for paths in list_of_paths:
        f = [os.path.basename(path) for path in paths]
        if len(f) != len(paths):
            LOG.error("different filenames!")

        _replace_duplicate_resources_in_files(paths)


def _replace_duplicate_resources_in_files(paths):
    #  Firstly copy the first resource path to the common folder.
    new_relative_resource_path = None
    image_exts = [".png", ".gif", ".jpg"]

    for pathname in paths:
        filename = os.path.basename(pathname)
        is_image = bool(os.path.splitext(pathname)[1] in image_exts)

        #  locate 'docs'
        dirs = str(pathname).split("/")
        while dirs[0] != "docs":
            dirs.pop(0) # now we have [docs, corda-os, 4.4, ..., ..., file]

        old_relative_resource_path = os.path.sep.join(dirs[3:])
        if not new_relative_resource_path:
            if is_image:
                new_relative_resource_path = os.path.join("en", "images", filename)
            else:
                new_relative_resource_path = os.path.join("en", "pdf", filename)
            LOG.warning(f"Consolidating into one file {new_relative_resource_path}")

        dest = os.path.join(ROOT, "static", new_relative_resource_path)
        shutil.copyfile(pathname, dest)

        # don't fully match trailing parenthesis as we can have:
        # [text](the/old/link/text.md "some alt text at the end")
        replacements = [( f"({old_relative_resource_path}", f"(/{new_relative_resource_path}")]
        this_version = os.path.join(CONTENT, "en", dirs[0], dirs[1], dirs[2])
        files_in_this_version = [x for x in Path(this_version).rglob(f'**/*') if str(x).endswith(".md")]
        _search_and_replace(files_in_this_version, replacements)
        os.unlink(pathname)


def _hash_file(pathname):
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    #sha1 = hashlib.sha1()

    with open(pathname, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def create_missing_pages():
    if ARGS.cms not in ["hugo", "markdown"]:
        LOG.warning("Don't know what to do for other CMSs")
        return

    parent_dir = os.path.join(CONTENT, "en", "docs")

    for dir in os.listdir(parent_dir):
        item = os.path.join(parent_dir, dir)
        if not os.path.isdir(item):
            continue
        index_md = os.path.join(item, "_index.md")
        if not os.path.exists(index_md):
            LOG.warning(f"Writing empty: {index_md}")
            open(index_md, 'w').close()



def main():
    global ARGS, MENU_FILES, INCLUDES

    desc = "Convert rst files to md using sphinx"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--toml", "-t", help="write front matter as toml, default is yaml as that renders in github", default=False, action='store_true')
    parser.add_argument("--toc", help="include table of contents in the page", default=False, action='store_true')
    parser.add_argument("--full-conversion", "-f", help="full conversion of rst, default skip rst conversion for speed", default=False, action='store_true')
    parser.add_argument("--cms", "-c", help="generate (commonmark) markdown for cms", default='hugo', choices=['gatsby', 'markdown', 'hugo'])
    parser.add_argument("--skip-resources", help="skip copying resources", default=False, action='store_true')

    ARGS = parser.parse_args()

    _setup_logging()

    LOG.warning(f"You need to clone the repositories you wish to convert to {REPOS}")
    LOG.warning(f"You also need to then git checkout the branch you want.")
    LOG.warning(f"There is a script that does this - get_repos.sh")

    if ARGS.full_conversion:
        convert_rst_to_xml()
        postprocess_xml()
    else:
        LOG.warning("Skipping rst-to-xml")

    if ARGS.cms == 'markdown':
        cms = Markdown()  #  Generates hugo-shortcode free markdown - uses divs instead
    elif ARGS.cms == "gatsby":
        cms = Gatsby()  # which simply adds react tags <Tab> <Tabs> etc.
    else:
        cms = Hugo()

    menus_to_be_written_to_config, MENU_FILES = parse_indexes()
    INCLUDES = parse_literal_includes()

    menus = os.path.join(ROOT, "config/_default/menus/menus.en.toml")
    open(menus, 'w').write(toml.dumps(menus_to_be_written_to_config))

    convert_all_xml_to_md(cms)

    # filename = os.path.join(ROOT, "repos/en/docs/corda-os/4.4/docs/xml/xml/api-flows.xml")
    # convert_one_xml_file_to_cms_style_md(cms, filename)

    copy_to_content(cms)

    if not ARGS.skip_resources:
         copy_resources_to_content()

    create_missing_pages()


if __name__ == '__main__':
    main()
