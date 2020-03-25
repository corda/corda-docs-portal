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

from utils.parse_menus import parse_rst_files_for_menus, version, version_for_config
from utils.parse_literal_includes import parse_literal_includes, md_relpath, github_shortcode_for

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
CONTENT = os.path.join(ROOT, "content")
DOCS = os.path.join(CONTENT, "en/docs")

LOG = logging.getLogger(__name__)
ARGS = None


def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def remove_line_from_file(file):
    LOG.info(f"Processing {file}")
    old_lines = open(file, 'r').readlines()
    line_count = len(old_lines)
    start_token = "{{/* github"
    end_token = "*/}}"
    lines = []
    for line in old_lines:
        if line.startswith(start_token) and end_token in line:
            a = [i+ end_token + "\n"  for i in line.split(end_token)]
            a[-1] = a[-1].strip(end_token  + "\n")
            lines.append("\n")
            lines.extend(a)
            lines.append("\n\n")
        else:
            lines.append(line)

    for line in lines[:]:  # iterate over copy of lines
        if line.startswith(start_token):
            LOG.warn(f"Removing line {line}")
            lines.remove(line)
            if not (line.startswith(start_token) and line.strip().endswith(end_token)):
                print(line)
                assert line.startswith(start_token) and line.strip().endswith(end_token)

    if line_count != len(lines):
        open(file, 'w').writelines(lines)
        LOG.warn(f"Rewriting {file}")


def remove_lines():
    LOG.warning("Removing all lines from markdown")

    files = [x for x in Path(DOCS).rglob('**/*.md')]

    for file in files:
        remove_line_from_file(file)

    LOG.warning("Removing all lines from markdown finished")


def main():
    desc = "Remove lines from markdown"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    remove_lines()


if __name__ == '__main__':
    main()
