#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys

from algoliasearch.search_client import SearchClient

DESC = """ Set the searchable facets on an index after with crawled and sent it to algolia  """

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)

LOG = logging.getLogger(__name__)


def _setup_logging():
    LOG.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:  %(message)s')
    ch.setFormatter(formatter)
    LOG.addHandler(ch)


def process(app_id, write_key, index_name, facets):
    LOG.info(f"Setting facets for searching on index {index_name} - {facets}")
    client = SearchClient.create(app_id, write_key)
    index = client.init_index(index_name)

    # https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/how-to/declaring-attributes-for-faceting/
    index.set_settings({
        'attributesForFaceting': facets
    })
    LOG.info(f"Setting facets for searching on index {index_name} finished")

    settings = index.get_settings()
    index_facets = settings.get('attributesForFaceting', [])
    LOG.info(f"Facets on index = {index_facets}")

    if not set(facets).issubset(index_facets):
        LOG.error("Facets are not set on the index.  Searching will be broken on the site.")
        return 1

    return 0


def main():
    parser = argparse.ArgumentParser(description=DESC)

    parser.add_argument("config", help="trivial config file")
    parser.add_argument("appId", help="application id")
    parser.add_argument("writeKey", help="Algolia secret write key")

    args = parser.parse_args()

    _setup_logging()

    if not os.path.exists(args.config):
        LOG.error(f"Config file does not exist: {args.config}")
        sys.exit(1)

    cfg = json.loads("\n".join(open(args.config, 'r').readlines()))
    return process(args.appId, args.writeKey, cfg["index"], cfg["facets"])


if __name__ == '__main__':
    sys.exit(main())
