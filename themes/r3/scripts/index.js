import { applyAnchors } from "./anchorify";
import { activateListeners }  from "./nav";
//import { applySiteMapCollapse } from "./sitemap";
import { activateTabs } from "./activate-tabs";

document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    //  applySiteMapCollapse();
    activateListeners();
    activateTabs();
});
