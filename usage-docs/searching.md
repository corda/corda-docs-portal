# Searching

The search functionality is powered by [Algolia docsearch](https://docsearch.algolia.com).

## Configuration

Configuration is [explained here](https://docsearch.algolia.com/docs/config-file/)

In the `_index.md` of a `software version`, we define:

* a `project` parameter, e.g. `corda-os`
* a `version` parameter, e.g. `4.4`

The site implicitly give us a the language for the current set of pages.

These 3 parameters are set in every software version page in the `meta` tags, and are indexed by Algolia.

We then configure our search page to filter results on these values only when we are with a particular software version to get context aware results.

## Rebuilding the Search Index

This should be done periodically by our CI system, but a manual rebuild can be triggered by:

```make
make crawl ALGOLIA_APPLICATION_ID=UX2KMUWFAL ALGOLIA_API_ADMIN_KEY=<THE SECRET WRITE API KEY>
```

The `SECRET WRITE API KEY` can be found by logging into the [Algolia Console](https://www.algolia.com/apps/UX2KMUWFAL/api-keys/all).
