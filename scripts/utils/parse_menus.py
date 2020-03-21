#!/usr/bin/env python3

import argparse
import logging
import os
import re
from collections import Set
from pathlib import Path

import toml
import yaml

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(THIS_DIR))
REPOS = os.path.join(ROOT, "repos")
CONTENT = os.path.join(ROOT, "content")
REPOS_ROOT = os.path.join(REPOS, "en/docs")  # don't rely on this.

LOG = logging.getLogger(__name__)
ARGS = None


class Directive:
    def __init__(self):
        self.args = {}
        self.name = None
        self.value = None
        self.inner = []

    def parse(self, line):
        # The opening directive
        if line.strip().startswith(".."):
            parts = line.split("::")
            self.name = parts[0].replace("..", "").strip()
            if len(parts) > 1:
                self.value = parts[1].strip()
            return

        # A parameter
        if line.strip().startswith(":"):
            matches = re.match(r":(.*):\s+(.*)", line.strip())
            if matches:
                self.args[matches.group(1)] = matches.group(2)
            else:
                matches = re.match(r":(.*):", line.strip())
                if matches:
                    self.args[matches.group(1)] = "true"

            return

        # Content
        self.inner.append(line.strip())


class MenuEntry:
    def __init__(self, menu_id, identifier, name, parent, weight):
        self.menu_id = menu_id
        self.identifier = identifier
        self.name = name
        self.parent = parent
        self.weight = weight
        self.md_relpath = None

    def to_dict(self):
        d = {}
        if self.identifier:
            d["identifier"] = self.identifier
        if self.parent:
            d["parent"] = self.parent
        if self.name:
            d["name"] = self.name
        if self.weight:
            d["weight"] = self.weight
        return d

    def to_front_matter_entry(self):
        # if not(self.identifier or self.name or self.parent or self.weight):
        #     return { "menu" : self.menu_id}

        return {"menu": {self.menu_id: self.to_dict()}}


class Menus:
    def __init__(self):
        self.menu_entries_by_identifier = {}
        self.identifier_by_relpath = {}

    def add(self, menu_entry):
        """ Adds, or overwrites """
        if menu_entry is None:
            return

        if menu_entry.identifier is None:
            assert menu_entry.identifier is not None

        if menu_entry.md_relpath:
            self.identifier_by_relpath[menu_entry.md_relpath] = menu_entry.identifier
        self.menu_entries_by_identifier[menu_entry.identifier] = menu_entry

    def get_by_identifier(self, identifier):
        return self.menu_entries_by_identifier.get(identifier, None)

    def get_by_identifier_or_new(self, menu_id, identifier):
        return self.menu_entries_by_identifier.get(identifier, MenuEntry(menu_id, identifier, None, None, None))

    def get_by_relpath(self, relpath):
        identifier = self.identifier_by_relpath.get(relpath, None)
        if not identifier:
            return None
        return self.menu_entries_by_identifier.get(identifier, None)

    def get_menu_entries_for_config(self):
        """ literally just call toml.dumps() on this."""
        menu_entries_by_menu_id = {}
        for k in sorted(self.menu_entries_by_identifier.keys()):
            # if we're a menu entry that isn't in a page/file, it must be written to config
            # i.e. it's a caption.
            if self.menu_entries_by_identifier[k].md_relpath is not None:
                continue

            menu_id = self.menu_entries_by_identifier[k].menu_id
            a = menu_entries_by_menu_id.get(menu_id, [])
            a.append(self.menu_entries_by_identifier[k].to_dict())
            menu_entries_by_menu_id[menu_id] = a

        return menu_entries_by_menu_id

    def get_front_matter_by_menu_id_by_file(self):
        menu_ids = set() # corda-os-4-4, cenm-1-0 etc.
        for __, menu_entry in self.menu_entries_by_identifier.items():
            menu_ids.add(menu_entry.menu_id)

        d = {}
        for menu_id in menu_ids:
            fd = {}
            for __, menu_entry in self.menu_entries_by_identifier.items():
                if not menu_entry.md_relpath or menu_entry.menu_id != menu_id:
                    continue  # it's a caption
                fd[menu_entry.md_relpath] = menu_entry.to_front_matter_entry()
            d[menu_id] = fd

        return d


def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def parse_rst_files_for_menus():
    """ Returns a 2-tuple of { version : menus } and { version: files{file: submenu} }
    """
    LOG.info("Globbing rst files")
    index_files = [x for x in Path(REPOS).rglob('docs/source/**/*.rst')]
    LOG.info("Globbing rst files finished")

    LOG.info("Building menus")

    menus_obj = Menus()
    for index_file in index_files:
        parse_file_for_doctree(menus_obj, index_file)

    LOG.info("Building menus finished")

    return menus_obj.get_menu_entries_for_config(), menus_obj.get_front_matter_by_menu_id_by_file()


def repo_and_version(filename):
    dirs = str(filename).split("/")
    while dirs[0] != "docs":
        dirs.pop(0)

    return dirs[1], dirs[2]


def md_relpath(filename):
    dirs = str(filename).split("/")
    while dirs and len(dirs) > 5 and dirs[0] != "docs":
        dirs.pop(0)
    return "/".join(dirs[5:]).replace(".rst", ".md")


def version(filename):
    dirs = str(filename).split("/")
    #  locate 'docs'
    while dirs[0] != "docs":
        dirs.pop(0)

    return dirs[1] + os.sep + dirs[2]


def version_for_config(filename):
    # TOML/YAML doesn't like '.' in the string, and this string will be used in TOML/YAML
    return version(filename).replace(os.sep, "-").replace(".", "-")


def _get_name(caption, file_relpath):
    if caption:
        return caption
    filename = os.path.splitext(os.path.basename(file_relpath))[0]
    return filename.replace("-", " ")


def _get_page_identifier(version_prefix, file):
    """ return a consistently (unique) page identifier """
    if _is_index_page(file):
        return None

    #  Take the file name and attempt to create a caption.
    filename = os.path.splitext(os.path.basename(file))[0]
    if filename == "toc-tree":
        # Use parent folder name instead
        filename = os.path.basename(os.path.dirname(file))
    if filename.endswith("-index"):
        filename = filename.replace("-index", "")
    ident = " ".join(filename.split("-")).title()
    return version_prefix + "-" + ident.lower().replace(" ", "-").replace("&", "and")


def parse_file_for_doctree(menus, file):
    """ Returns a 2-tuple of { version : menus } and { version: files } where files = {file: submenu} }
    Files have '.md' suffix
    """

    # Only doctree directives
    directives = filter_directives(parse_rst(file))

    if not directives:
        return

    software_version = version_for_config(file)
    weight = 1000 if not _is_index_page(file) else 10

    this_page_identifier = _get_page_identifier(software_version, file)
    page_menu_entry = menus.get_by_identifier_or_new(software_version, this_page_identifier)

    for directive in directives:
        caption = directive.args.get("caption", None)

        # Any pages of this directive will 'hang off' the page_menu_entry
        parent_menu_entry = page_menu_entry

        # Except:
        if caption is not None:
            # We're a child of a (fake) caption entry
            # There isn't a page associated for the this branch node (menu entry), it's defined only
            # in the rst, so we need to add it to the menus.en.toml entries.
            caption_identifier = software_version + "-" + caption.lower().replace(" ", "-").replace("&", "and")
            caption_parent = page_menu_entry.identifier if page_menu_entry else None
            caption_menu_entry = MenuEntry(software_version, caption_identifier, caption, caption_parent, weight)
            menus.add(caption_menu_entry)

            parent_menu_entry = caption_menu_entry

        weight += 10

        for line in directive.inner:
            file_in_menu = _get_file_as_md_if_exists(os.path.dirname(file), _get_file_from_doctree_line(line))

            if not file_in_menu:
                continue

            leaf_page_identifier = _get_page_identifier(software_version, file_in_menu)
            leaf_menu_entry = menus.get_by_identifier_or_new(software_version, leaf_page_identifier)

            leaf_menu_entry.md_relpath = file_in_menu
            leaf_menu_entry.weight = weight
            leaf_menu_entry.parent = parent_menu_entry.identifier if parent_menu_entry else None

            menus.add(leaf_menu_entry)
            weight += 10


def filter_directives(directives):
    doctree_directives = []
    for directive in directives:
        if directive.name not in ['toctree', 'conditional-toctree']:
            continue

        if directive.args.get("if_tag", "htmlmode") != "htmlmode":
            continue

        doctree_directives.append(directive)
    return doctree_directives


def _get_file_as_md_if_exists(this_dir, file_in_menu):
    """ Return the full path to the *markdown* file, if it exists
    """
    if not file_in_menu:
        return None

    full_path = str(os.path.join(this_dir, file_in_menu))
    if not full_path.endswith(".rst"):
        full_path += ".rst" # rst is relax about suffixes when being referenced.
    if not os.path.exists(full_path):
        LOG.warning(f"Missing file in menu, ignoring: {full_path}")
        return None

    return md_relpath(full_path)


def _get_file_from_doctree_line(line):
    """ Simply extract the file name from the line, it's either the second argument, or the only argument
    """
    m = re.match(r"\s*(.*)\s*<(.*)>", line)
    if m:
        file_in_menu = m.group(2)
    else:
        file_in_menu = line.strip()
    return file_in_menu


def _is_index_page(file):
    return os.path.basename(file) in ["index.rst", "index.md", "_index.md"]


def parse_rst(index_file):
    """  Really rough parsing - just want 'toctree'  """
    LOG.info(f"Parsing {index_file}")
    directives = []

    lines = open(index_file, 'r').readlines()

    directive = None
    for line in lines:
        if line.lstrip().startswith(".."):
            if directive:
                directives.append(directive)  # append previous one to list
            directive = Directive()  # create new
            directive.parse(line)
        elif directive and (line.lstrip() != line or line.strip() == ""):
            directive.parse(line)  # line is part of current directive
        else:
            # we've left a directive
            if directive:
                directives.append(directive)
                directive = None

    if directive:
        directives.append(directive)

    return directives


def main():
    global ARGS

    desc = "Rebuild menus.en.toml from all rst files"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    a, b = parse_rst_files_for_menus()

    print(toml.dumps(a))


if __name__ == "__main__":
    main()
