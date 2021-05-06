# Searching

The search functionality is powered by [Algolia docsearch](https://docsearch.algolia.com).

## Configuration

Configuration is [explained here](https://docsearch.algolia.com/docs/config-file/)

In the `_index.md` of a `software version`, we define:

* a `project` parameter, e.g. `corda-os`
* a `version` parameter, e.g. `4.4`

The site implicitly gives us a the language for the current set of pages.

We then need to do the following steps:

* These 3 parameters are set in every page inside a software version in their `meta` tags, and are indexed by Algolia, e.g.

```html
<meta name="docsearch:language" content="en">
<meta name="docsearch:version" content="4.3">
<meta name="docsearch:project" content="corda-enterprise">
```

* We then [configure our search](https://www.algolia.com/doc/api-reference/api-parameters/facetFilters/) page to filter results on these values only when we are within a particular software version to get context aware results.

```javascript
if (document.querySelector('#search-input')) {
    docsearch({
        appId: "UX2KMUWFAL",
        apiKey: "1fe3367db02689b4aeebc59efad5abaf",
        indexName: "docs.corda.net",
        inputSelector: "#search-input",
        algoliaOptions: {
            hitsPerPage: 5,
            facetFilters: [
                'project:corda-enterprise',
                'version:4.3',
                'language:en'
            ]
        }
    });
}
```

## Building the Search Index

This should be done periodically by our CI system, but a manual rebuild can be triggered by:

```make
make crawl ALGOLIA_APPLICATION_ID=UX2KMUWFAL ALGOLIA_API_ADMIN_KEY=<THE SECRET WRITE API KEY>
```

The `SECRET WRITE API KEY` can be found by logging into the [Algolia Console](https://www.algolia.com/apps/UX2KMUWFAL/api-keys/all).

## Adding a New Index

If you need to add a new index in Algolia, typically for a new website and not this one, find someone with admin access, and add a new index.

* Upload your new index (`make crawl` does this for us here).
* Configure the index with the [attributes for faceting](https://www.algolia.com/doc/guides/managing-results/refine-results/faceting/#declaring-attributes-for-faceting), in our case `project`, `version`, and `language`.
