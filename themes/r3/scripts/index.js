import { applyAnchors } from "./anchorify";
import { applySiteMapCollapse } from "./sitemap";
import { activateListeners }  from "./toc";

document.addEventListener('DOMContentLoaded', function () {
    applyAnchors();
    applySiteMapCollapse();
    activateListeners();
});
