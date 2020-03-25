import { applyAnchors } from "./anchorify";
import { activateListeners } from "./nav";
import { scrollOffset, clickLinkOnNavExpandDropDown, uncheckDropDownOnClick } from "./sitemap";
import { activateTabs } from "./activate-tabs";
import { searchShortcut } from "./search-shortcut";
document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    scrollOffset();
    activateListeners();
    activateTabs();
    searchShortcut();
    clickLinkOnNavExpandDropDown();
    uncheckDropDownOnClick();
});
