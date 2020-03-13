import { applyAnchors } from "./anchorify";
import { activateListeners } from "./nav";
import { accordionNav } from "./sitemap";
import { activateTabs } from "./activate-tabs";
import { searchShortcut } from "./search-shortcut";
document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    new accordionNav();
    activateListeners();
    activateTabs();
    searchShortcut();
});
