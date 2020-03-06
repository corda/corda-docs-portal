import { applyAnchors } from "./anchorify";
import { activateListeners }  from "./toc";
//import { applySiteMapCollapse } from "./sitemap";
import { activateTabs } from "./activate-tabs";

document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    //  applySiteMapCollapse();
    activateListeners();
    activateTabs();
});
