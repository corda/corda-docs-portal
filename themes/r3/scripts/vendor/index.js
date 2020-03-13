import "./bootstrap-init";
import docsearch from "docsearch.js";
import docsearchParams from "../../params.json";

if (document.querySelector('#search-input')) {
    // Todo:  move this to per-section as Hugo has to insert the app-id.
    docsearch({
        appId: docsearchParams.algolia_appId,
        apiKey: docsearchParams.algolia_apiKey,
        indexName: docsearchParams.aloglia_indexName,
        inputSelector: "#search-input",
        algoliaOptions: { hitsPerPage: 5 }
    });
}
