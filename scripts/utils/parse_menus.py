#!/usr/bin/env python3

import argparse
import logging
import os
import re
from pathlib import Path

import toml

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


def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def parse_indexes():
    """ Returns a 2-tuple of { version : menus } and { version: files{file: submenu} }
    """
    LOG.info("Globbing rst files")
    index_files = [x for x in Path(REPOS).rglob('docs/source/**/*.rst')]
    LOG.info("Globbing rst files finished")

    LOG.info("Building menus")

    all_menus = {}
    all_files = {}

    for index_file in index_files:
        menus, files = parse_index(index_file)

        # Update entries that go into menus.en.toml
        for top_most_menu_identifier, new_menu_entries in menus.items():
            menu_entries = all_menus.get(top_most_menu_identifier, [])
            for new_menu_entry in new_menu_entries:
                if new_menu_entry["identifier"] not in [m["identifier"] for m in menu_entries]:
                    menu_entries.append(new_menu_entry)

            all_menus[top_most_menu_identifier] = menu_entries

        # Update look up for files to see what menu they belong under, if any
        for top_most_menu_identifier, new_menu_entries in files.items():
            menu_by_file = all_files.get(top_most_menu_identifier, {})
            for file, menu in new_menu_entries.items():
                menu_by_file[file] = menu
            all_files[top_most_menu_identifier] = menu_by_file

    LOG.info("Building menus finished")

    print(toml.dumps(all_menus))

    return all_menus, all_files


def repo_and_version(filename):
    dirs = str(filename).split("/")
    while dirs[0] != "docs":
        dirs.pop(0)

    return dirs[1], dirs[2]


def version(filename):
    dirs = str(filename).split("/")
    #  locate 'docs'
    while dirs[0] != "docs":
        dirs.pop(0)

    return dirs[1] + os.sep + dirs[2]


def version_for_config(filename):
    # TOML/YAML doesn't like '.' in the string, and this string will be used in TOML/YAML
    return version(filename).replace(os.sep, "-").replace(".", "-")


def parse_index(file):
    """ Returns a 2-tuple of { version : menus } and { version: files } where files = {file: submenu} }
    Files have '.md' suffix
    """
    directives = parse_rst(file)
    ver = version_for_config(file)
    menus = []
    files = {}

    weight = 10
    for directive in directives:
        if directive.name not in ['toctree', 'conditional-toctree']:
            continue

        if directive.args.get("if_tag", "htmlmode") != "htmlmode":
            continue

        caption = _get_menu_title(directive, file)

        # Create the submenu entries (for hugo)
        identifier = ver + "-" + caption.lower().replace(" ", "-").replace("&", "and")
        d = {"identifier": identifier, "name": caption, "weight": weight}
        weight += 10
        menus.append(d)

        #  identify pages in sub menus
        for line in directive.inner:
            m = re.match(r"\s*(.*)\s*<(.*)>", line)
            if m:
                file_in_menu = m.group(2)
            else:
                file_in_menu = line.strip()

            if file_in_menu:
                full_path = str(os.path.join(os.path.dirname(file), file_in_menu))
                if not full_path.endswith(".rst"):
                    full_path += ".rst"
                if not os.path.exists(full_path):
                    LOG.error(f"Missing file in menu, ignoring: {full_path}")
                    continue
                if file_in_menu.endswith(".rst"):
                    file_in_menu = file_in_menu.replace(".rst", ".md")
                else:
                    file_in_menu += ".md" # rst is relax about suffixes when being referenced.
                x = files.get(ver, {})
                x[file_in_menu] = identifier
                files[ver] = x

    return {ver: menus}, files


def _get_menu_title(directive, file):
    """ Return the title of the menu from the directive, or use the filename or even
    the parent folder """
    caption = directive.args.get("caption", None)
    if not caption:
        #  Take the file name and attempt to create a caption.
        filename = os.path.splitext(os.path.basename(file))[0]
        if filename == "toc-tree":
            # Use parent folder name instead
            filename = os.path.basename(os.path.dirname(file))
        if filename.endswith("-index"):
            filename = filename.replace("-index", "")
        caption = " ".join(filename.split("-")).title()
    return caption


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
            continue  # not a directive

    if directive:
        directives.append(directive)

    return directives


def main():
    global ARGS

    desc = "Rebuild menus.en.toml from index.rst files"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    parse_indexes()


if __name__ == "__main__":
    main()
