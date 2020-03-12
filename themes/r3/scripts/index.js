import { applyAnchors } from "./anchorify";
import { activateListeners } from "./nav";
//import { applySiteMapCollapse } from "./sitemap";
import { activateTabs } from "./activate-tabs";
import { searchShortcut } from "./search-shortcut";
document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    //  applySiteMapCollapse();
    activateListeners();
    activateTabs();
    searchShortcut();
});
