#!/usr/bin/env python3

import argparse
import logging
import os
from pathlib import Path

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
CONTENT = os.path.join(ROOT, "content")
DOCS = os.path.join(CONTENT, "en/docs")

LOG = logging.getLogger(__name__)
ARGS = None


def _setup_logging():
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def add_alias_to_file(file):
    LOG.info(f"Processing {file}")
    old_lines = open(file, 'r').readlines()
    line_count = len(old_lines)
    lines = []
    in_yaml = False
    for line in old_lines:
        if line.strip() == "---":
            in_yaml = not in_yaml

        lines.append(line)

        if in_yaml and line.strip() == "aliases:":
            html = str(os.path.basename(file)).replace(".md", ".html")
            lines.append(f"- /{html}\n")

    open(file, 'w').writelines(lines)
    LOG.info(f"Processing {file} finished")


def add_aliases():
    LOG.warning("Adding versionless aliases to file")

    files = [x for x in Path(DOCS).rglob('**/*.md')]

    for file in files:
        # blunt weapon...
        if "corda-os/4.4" in str(file) or "cenm/1.2" in str(file):
            filename = os.path.basename(file)
            if filename not in ["_index.md", "index.md"]:
                add_alias_to_file(file)

    LOG.warning("Adding versionless aliases to file")


def main():
    desc = "Remove lines from markdown"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    add_aliases()


if __name__ == '__main__':
    main()
