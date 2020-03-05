import { applyAnchors } from "./anchorify";
import { applySiteMapCollapse } from "./sitemap";
import { activateListeners }  from "./toc";
//import { applySiteMapCollapse } from "./sitemap";
import { activateListeners } from "./toc";
import { activateTabs } from "./activate-tabs";

document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    //  applySiteMapCollapse();
    activateListeners();
    activateTabs();
});
