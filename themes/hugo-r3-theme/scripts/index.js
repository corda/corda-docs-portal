import { applyAnchors } from "./anchorify";
import { activateListeners } from "./nav";
import { scrollOffset, clickLinkOnNavExpandDropDown, uncheckDropDownOnClick } from "./sitemap";
import { activateTabs } from "./activate-tabs";
import { searchShortcut } from "./search-shortcut";
import { indexPopUp } from "./index-pop-up";

document.addEventListener("DOMContentLoaded", function() {
    applyAnchors();
    scrollOffset();
    activateListeners();
    activateTabs();
    searchShortcut();
    clickLinkOnNavExpandDropDown();
    uncheckDropDownOnClick();
});

// so that we can access it from the page that needs it.
window.oneTimePopUp = indexPopUp;
