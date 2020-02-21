import { applySiteMapCollapse } from "./js/sitemap";
import { applyAnchors } from "./js/anchorify";
import { activateListeners } from "./js/toc";
import './sass/main.scss';

applyAnchors();
applySiteMapCollapse();

document.addEventListener('DOMContentLoaded', function () {
    activateListeners();
});


