import "bootstrap";
import mermaid from "mermaid";
import docsearch from "docsearch.js";
import docsearchParams from "../../params.json";

mermaid.initialize({ startOnLoad: true });

docsearch({
    appId: docsearchParams.algolia_appId,
    apiKey: docsearchParams.algolia_apiKey,
    indexName: docsearchParams.aloglia_indexName,
    inputSelector: "#search-input",
    algoliaOptions: { hitsPerPage: 5 }
});
