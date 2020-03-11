#!/usr/bin/env python3

import logging
import os
import shutil
import sys
import re
import argparse
from pathlib import Path
import json
import toml
import yaml
import hashlib
from collections import namedtuple
from utils.parse_menus import version, version_for_config, parse_rst, repo_and_version

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(THIS_DIR))
REPOS = os.path.join(ROOT, "repos")
CONTENT = os.path.join(ROOT, "content")
REPOS_ROOT = os.path.join(REPOS, "en/docs")  # don't rely on this.

LOG = logging.getLogger(__name__)
ARGS = None


def _setup_logging():
    # LOG.setLevel(logging.WARN)
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def md_relpath(non_md_path):
    """ relative to docs/content root """
    dirs = str(non_md_path).split("/")
    #  locate 'docs'
    while dirs[0] != "docs":
        dirs.pop(0)

    # can do all this in one search and replace without collisions for .xml and .rst files to get .md
    return "/".join(dirs[3:])\
        .replace('docs/xml/xml/', '')\
        .replace('docs/source/', '')\
        .replace('.rst', '.md')\
        .replace(".xml", ".md")


def _repo_relpath(full_path):
    """ relative to repository root """
    dirs = str(full_path).replace(REPOS, '').split('/')
    return "/".join(dirs[5:])


def _github_repo(repo):
    if repo == "corda-os":
        return "corda"
    if repo == "corda-enterprise":
        return "enterprise"
    if repo == "cenm":
        return "network-services"
    return repo


def _github_version(repo, version):
    if repo == "corda-os":
        if version == "4.0":
            return "release/4.0"
        if version == "3.4":
            return "release-V3"
        if version.startswith("4."):
            return f"release/os/{version}"
        return version
    if repo == "corda-enterprise":
        if version == "4.1":
            return "release/4.1"
        if version == "4.0":
            return "release-4.0"
        if version == "3.3":
            return "release/release-V3"
        if version.startswith("4."):
            return f"release/ent/{version}"
        return version
    if repo == "cenm":
        return f"release/{version}"
    return version


def _github_raw_path(repo, version, literalinclude_relpath):
    return f"https://raw.githubusercontent.com/corda/{_github_repo(repo)}/{_github_version(repo, version)}/{literalinclude_relpath}"


def _find_line_number(lines, value):
    line_number = 1
    for line in lines:
        if line.strip().endswith(value):
            break
        line_number += 1

    return line_number


def _github_path(repo, version, literalinclude_relpath, args):
    pathname = os.path.join(REPOS_ROOT, repo, version, literalinclude_relpath)
    url = f"https://github.com/corda/{_github_repo(repo)}/blob/{_github_version(repo, version)}/{literalinclude_relpath}"

    if not os.path.exists(pathname):
        LOG.error(f"Path does not exist, return URL anyway: {pathname}")
        return url

    lines = open(pathname, 'r').readlines()

    url_suffix = ""
    if "start-after" in args:
        num = _find_line_number(lines, args['start-after']) + 1
        url_suffix += f"#L{num}"
        if "end-before" in args:
            num = _find_line_number(lines, args['end-before']) - 1
            url_suffix += f"-L{num}"

    return url + url_suffix


def parse_literal_includes_in_file(filename):
    """ Returns a namedtuple """
    relpath = md_relpath(filename)
    repo, version = repo_and_version(filename)

    version_key = version_for_config(filename)

    directives = parse_rst(filename)

    LiteralInclude = namedtuple("LiteralInclude", ['src', 'url', 'raw_url', 'start_after', 'end_before'])

    literal_includes = []
    for directive in directives:
        if directive.name != "literalinclude":
            continue
        full_path = os.path.abspath(os.path.join(os.path.dirname(filename), directive.value))

        src_relpath = _repo_relpath(full_path)
        url = _github_path(repo, version, src_relpath, directive.args)
        raw_url = _github_raw_path(repo, version, src_relpath)

        literal_includes.append(LiteralInclude(src_relpath, url, raw_url, directive.args.get("start-after", ""),
                                               directive.args.get("end-before", "")))

    return version_key, relpath, literal_includes


def github_shortcode(literal_include):
    src, url, raw_url, start_after, end_before = literal_include
    return "{{/* github " + f"src='{src}' url='{url}' raw='{raw_url}' start='{start_after}' end='{end_before}'" + " */}}"


def github_shortcode_for(index, literal_includes):
    return github_shortcode(literal_includes[index])


def parse_literal_includes():
    files = [x for x in Path(REPOS).rglob('docs/source/**/*.rst')]

    lookup = {}
    for file in files:
        version_key, md_relpath, literal_includes = parse_literal_includes_in_file(file)
        files_dict = lookup.get(version_key, {})
        files_dict[md_relpath] = literal_includes
        lookup[version_key] = files_dict

    return lookup


def main():
    global ARGS

    desc = "Rebuild menus.en.toml from index.rst files"
    parser = argparse.ArgumentParser(description=desc)

    ARGS = parser.parse_args()

    _setup_logging()

    parse_literal_includes_in_file("/home/barry/dev/r3/forks/docs-site/repos/en/docs/corda-os/4.4/docs/source/hello-world-state.rst")

    d = parse_literal_includes()
    for k, v in d.items():
        for k2, v2 in v.items():
            print(k, k2, v2)


if __name__ == '__main__':
    main()
