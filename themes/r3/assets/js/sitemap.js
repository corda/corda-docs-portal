
/** Find page in site map and open collapsed nodes */
function locatePageInSiteMap() {
    var thisPage = document.URL.split('#')[0];
    var sitemap = document.getElementById("r3-sitemap");
    var elements = sitemap.getElementsByTagName("a");
    for (var i = 0 ; i < elements.length; i++) {
        if (thisPage == elements[i].href) {
            var e = elements[i];
            while(e && e !== sitemap) {
                if (e.classList.contains("nested")) {
                    e.classList.toggle("active");
                }
                e = e.parentNode;
            }
            elements[i].id = "r3-o-selected-page";
            break;
        }
    }
}

/** Applies leaf node toggle for collapse/show for the site tree */
export function applySiteMapCollapse() {
    var toggler = document.getElementsByClassName("caret");
    var i;

    for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function () {
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
        });
    }

    locatePageInSiteMap();
}
