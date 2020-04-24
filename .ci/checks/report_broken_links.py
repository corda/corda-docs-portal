#!/usr/bin/env python3

import argparse
import csv
import logging
import os
import sys
from shutil import copyfile

DESC = """ Build site locally and run linkchecker over it and report  """

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(THIS_DIR))

CONTENT_EN = os.path.join(ROOT, "content", "en")
STATIC = os.path.join(ROOT, "static")
STATIC_EN = os.path.join(STATIC, "en")
REPOS = os.path.join(ROOT, "repos")

LOG = logging.getLogger(__name__)


def _setup_logging():
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def find_all(name, path, filter_string=None):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            pathname = os.path.join(root, name)
            if filter_string is None or filter_string in pathname:
                result.append(pathname)
    return result


def strip_comments(csv_pathname):
    out_pathname = os.path.join(os.path.dirname(csv_pathname), "stripped-" + os.path.basename(csv_pathname))
    open(out_pathname, 'w').writelines(line for line in open(csv_pathname) if not line.startswith('#'))
    return out_pathname


def baseref_to_github(base_url, baseref):
    """ Convert the url to github """
    if baseref is None:
        return None

    replacement_url = "https://github.com/corda/docs-site/tree/staging/content/en"
    return baseref.replace(base_url, replacement_url).replace(".html", ".md")


def baseref_to_localhost(base_url, baseref):
    """ Convert the url to localhost:1313 """
    if baseref is None:
        return None

    replacement_url = "http://localhost:1313"
    return baseref.replace(base_url, replacement_url)


def baseref_to_file(base_url, baseref):
    """ Convert the url to something in the local clone """
    if baseref is None:
        return None

    replacement_url = CONTENT_EN
    return baseref.replace(base_url, replacement_url).replace(".html", ".md")


def suggest(root, url_name):
    """ Look for the base name of the url in the specified folder and return a list if found """
    base_name = os.path.basename(url_name)
    arr = find_all(base_name, root)
    if arr is None:
        return []

    return [str(p).replace(root, "") for p in arr]


def suggestions(url_name):
    """  Look for url_name and suggest a fix if we can find it on disk """
    base_name = os.path.basename(url_name)
    static = suggest(STATIC, base_name)
    if static:
        return static

    resource_is_in_content = suggest(CONTENT_EN, base_name)
    if resource_is_in_content:
        replacement = copy_suggestion_to_static(CONTENT_EN, resource_is_in_content)
        return [replacement]

    resource_is_in_repos = suggest(REPOS, base_name)
    if resource_is_in_repos:
        replacement = copy_suggestion_to_static(REPOS, resource_is_in_repos)
        return [replacement]

    LOG.error(f"UNFIXABLE FILE - MISSING IMAGE {url_name}")
    return []


def copy_suggestion_to_static(src_root, suggested_paths):
    """ Copy the first suggestion to the static folder """
    src = os.path.join(src_root, suggested_paths[0][1:])
    dest = os.path.join(STATIC_EN, os.path.basename(src))
    LOG.debug(f"Copying {src} to {dest}")
    copyfile(src, dest)
    replacement = dest.replace(STATIC, "")
    return replacement


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


def _try_and_fix_image(src_url, md_pathname, url_name):
    replacements = [str(item) for item in suggestions(url_name)]

    if replacements:
        LOG.debug(f"Fixing missing image:  {url_name} in {src_url} with {replacements[0]}")
        src = f"({url_name}"
        dest = f"({replacements[0]}"
        _search_and_replace([md_pathname], [(src, dest)])
        return True
    else:
        LOG.error(f"Missing image:  {url_name} in {src_url} - not found on disk")
        return False


def software_and_version(path):
    """ return 'corda-os', '4.4' """
    dirs = str(path).split("/")
    #  locate 'docs'
    while dirs[0] != "docs":
        dirs.pop(0)

    return dirs[1], dirs[2]


def _fix_page_api_link(full_url_to_file, markdown_file, resource_url):
    """ Might not be needed because we have redirects in place in nginx """
    software, version = software_and_version(markdown_file)

    replacement = f"https://api.corda.net/api/{software}/{version}/html/" + resource_url
    src = "(" + resource_url
    dest = "(" + replacement
    _search_and_replace([markdown_file], [(src, dest)])

    LOG.debug(f"Fixed {full_url_to_file}")

    pass


def _try_and_fix_bad_markdown_links(full_url_to_file, markdown_file, resource_url):
    if resource_url == ".md":
        LOG.debug(f"Cannot fix {full_url_to_file}")
        return False

    # url = os.path.basename(resource_url)

    src = "(" + resource_url
    dest = '({{% ref "' + resource_url + '" %}}'
    _search_and_replace([markdown_file], [(src, dest)])
    LOG.debug(f"Fixed {full_url_to_file}")
    return True


def _try_and_fix_page(full_url_to_file, markdown_file, resource_url):
    LOG.debug(f"{full_url_to_file} / {markdown_file} / {resource_url}")

    if resource_url.startswith("api/"):
        _fix_page_api_link(full_url_to_file, markdown_file, resource_url)
        return True

    return False


def _row_to_string(base_url, row):
    github = baseref_to_github(base_url, row['baseref'])
    localhost = baseref_to_localhost(base_url, row['baseref'])
    url_name = row.get("urlname", "")
    result = row.get("result", "")

    return f"Page: {localhost:70s} has bad link:  {url_name:70s}  |  {result} see also {github}"


class Results:
    def __init__(self):
        self.messages_by_severity = {}

    def add(self, severity, localhost, message):
        messages_by_url = self.messages_by_severity.get(severity, {})
        messages = messages_by_url.get(localhost, [])
        messages.append(message)
        messages_by_url[localhost] = messages
        self.messages_by_severity[severity] = messages_by_url

    def report(self):
        for severity, messages_by_url in self.messages_by_severity.items():
            for url, messages in messages_by_url.items():
                for message in messages:
                    if severity == "warning":
                        LOG.warning(message)
                    if severity == "error":
                        LOG.error(message)


def process_link_checker_file(args, csv_file):
    stripped_pathname = strip_comments(csv_file)

    results = Results()

    with open(stripped_pathname, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        count = 0
        image_count = 0
        page_count = 0
        for row in reader:
            localhost = baseref_to_localhost(args.base_url, row['baseref'])

            if args.ignore_wiki and "atlassian" in row["urlname"]:
                LOG.debug("Skipping wiki url")
                continue

            if not args.check_localhost_links and any([item in row["urlname"] for item in  ["http://127.0.0.1", "http://localhost"]]):
                LOG.debug("Skipping localhost urls")
                continue

            bad_site_url = args.base_url and row["url"] and args.base_url in row["url"] and row["url"].endswith(".md")
            valid = (row["valid"] is None or row["valid"] == 'True') and not bad_site_url

            if valid:
                continue

            bad_tls = any([item in row.get("result", "") for item in ["SSLError", "HTTPSConnectionPool"]])
            if bad_tls:
                results.add("warning", localhost, _row_to_string(args.base_url, row))
                continue

            count += 1

            url = baseref_to_localhost(args.base_url, row["baseref"])
            markdown_file = baseref_to_file(args.base_url, row["baseref"])

            url_name = row.get("urlname", "")

            bad_missing_images = any([url_name.endswith(suffix) for suffix in [".png", ".gif", ".jpg", ".jpeg", ".svg"]])
            if bad_missing_images:
                if args.ignore_images:
                    continue
                if args.fix:
                    _try_and_fix_image(url, markdown_file, url_name)
                image_count += 1

            bad_missing_regular_link = url_name.endswith(".html")
            if bad_missing_regular_link:
                if args.ignore_pages:
                    continue
                if args.fix:
                    _try_and_fix_page(url, markdown_file, url_name)
                page_count += 1

            if bad_site_url and args.fix:
                _try_and_fix_bad_markdown_links(url, markdown_file, url_name)

            results.add("error", localhost, _row_to_string(args.base_url, row))

    other_count = count - (page_count + image_count)

    results.report()

    if count != 0:
        LOG.error(f"Broken pages = {page_count}")
        LOG.error(f"Missing images = {image_count}")
        LOG.error(f"Others = {other_count}")
        LOG.error(f"Total broken links = {count}")

        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description=DESC)

    parser.add_argument("file", help="csv file to parse")
    parser.add_argument("--ignore-wiki", default=False, action="store_true")
    parser.add_argument("--ignore-pages", default=False, action="store_true")
    parser.add_argument("--ignore-images", default=False, action="store_true")
    parser.add_argument("--check-localhost-links", default=False, action="store_true")
    parser.add_argument("--fix", default=False, action="store_true", help="Try and fix in local repo")
    parser.add_argument("--base-url", default="http://docs.corda.net", help="URL that we ran linkchecker against")

    args = parser.parse_args()

    _setup_logging()

    csv_file = args.file
    if not os.path.exists(csv_file):
        LOG.error(f"CSV report file not generated?  Run linkchecker.  f{csv_file}")
        sys.exit(1)

    retval = process_link_checker_file(args, csv_file)
    sys.exit(retval)


if __name__ == '__main__':
    main()
