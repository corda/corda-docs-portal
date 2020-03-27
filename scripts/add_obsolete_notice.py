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


def add_obsolete_notice_to_file(file):
    LOG.info(f"Processing {file}")
    old_lines = open(file, 'r').readlines()

    lines = []
    in_yaml = False
    for line in old_lines:
        should_write = False
        if line.strip() == "---":
            in_yaml = not in_yaml

            if not in_yaml:
                should_write = True

        lines.append(line)

        if should_write:
            lines.append("{{% important %}}\n")
            lines.append("This documentation is unsupported.\n")
            lines.append("Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead\n")
            lines.append("{{% /important %}}\n")

    open(file, 'w').writelines(lines)
    LOG.info(f"Processing {file} finished")


def process():
    LOG.warning("Adding unsupported notices to files")

    files = [x for x in Path(DOCS).rglob('**/*.md')]

    for file in files:
        # blunt weapon...
        unsupported = ["corda-enterprise/3.0", "corda-enterprise/3.1","corda-enterprise/3.2"]
        if any([part in str(file) for part in unsupported]):
            add_obsolete_notice_to_file(file)

    LOG.warning("Adding unsupported notices to files")


def main():
    desc = "Remove lines from markdown"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    process()


if __name__ == '__main__':
    main()
