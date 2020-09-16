const algolia_appId = "UX2KMUWFAL";
const algolia_apiKey = "1fe3367db02689b4aeebc59efad5abaf";
const algolia_index = "docs.corda.net";
const facetFilters = window.facetFilters;

export function docSearchInit(){
    if (document.querySelector('#search-input')) {
        //https://www.algolia.com/doc/api-reference/api-parameters/facetFilters/?language=javascript
        let algoliaOptions = {
            hitsPerPage: 30,
            facetFilters: facetFilters
        };

        if(/404.html/.test(window.location.pathname)){
           delete algoliaOptions.facetFilters;
        }

        window.docsearch({
            appId: algolia_appId,
            apiKey: algolia_apiKey,
            indexName: algolia_index,
            inputSelector: "#search-input",
            algoliaOptions: algoliaOptions
        });
    }
}
