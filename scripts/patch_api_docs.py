#!/usr/bin/env python3

DESC="""Converts (Jetbrains) dokka github-flavoured-markdown to hugo markdown"""

# Rewrites files:
# * Renames 'index.md' to 'index.md'
# * Adds simple front-matter
#
# Must run dokka as a gradle task, or the fat jar with the correct output type, e.g.:
#
#     java -jar dokka-fatjar.jar -output content/en/ -format gfm -pass -src corda-os/4.3
#
# etc.

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
LOG = logging.getLogger(__name__)
ARGS = None



def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


""" Rename any file that is 'index.md' to '_index.md' for Hugo """
def rename_docs(docs_dir):
    for src in Path(docs_dir).rglob('index.md'):
        os.rename(src, str(src).replace("index.md", "_index.md"))


""" Get the document name  """
def get_document_name(src):
    name = str(os.path.basename(src))
    if name != "_index.md":
        # use the file name without the file extension
        name = name.replace(".md", "")
    else:
        name = os.path.basename(os.path.dirname(src))
    return name


""" Replace the content of any file 'index.md' -> '_index.md' and
add front matter """
def patch_doc(src):
        lines = open(src, 'r').readlines()
        if "---" in lines[0]:
            continue

        new_lines = []
        for line in lines:
            new_line = line.replace('/index.md', '/_index.md')
            new_lines.append(new_line)

        name = get_document_name(src)        
        front_matter = ["---\n", f'title: "{name}"\n', "---\n\n"]
        open(src, 'w').writelines(front_matter + new_lines)


""" Patch up all api docs """
def patch_docs(docs_dir):
    rename_docs(docs_dir)
    for src in Path(docs_dir).rglob('*.md'):
        patch_doc(src)
        LOG.info(f"Processed {src}")


def main():
    global ARGS
    parser = argparse.ArgumentParser(description=DESC)
    ARGS = parser.parse_args()

    _setup_logging()

    patch_docs(CONTENT)


if __name__ == '__main__':
    main()
