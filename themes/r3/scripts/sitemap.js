/** Find page in site map and open collapsed nodes */
function locatePageInSiteMap() {
    var thisPage = document.URL.split("#")[0];
    var sitemap = document.getElementById("r3-sitemap");

    var elements = sitemap.getElementsByTagName("a");
    for (var i = 0; i < elements.length; i++) {
        if (thisPage == elements[i].href) {
            var e = elements[i];
            while (!e.classList.contains("nested")) {
                e = e.parentNode;
            }
            e.classList.remove("nested");

            while (e && e !== sitemap) {
                if (e.classList.contains("nested")) {
                    e.classList.toggle("active");
                    e.querySelector(".caret").classList.toggle("caret-down");
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
    locatePageInSiteMap();
    var toggler = document.getElementsByClassName("caret");
    var i;

    for (i = 0; i < toggler.length; i++) {
        toggler[i].addEventListener("click", function() {
            this.parentElement
                .querySelector(".nested")
                .classList.toggle("active");
            this.classList.toggle("caret-down");
        });
    }
}

// The function actually applying the offset
function offsetAnchor() {
    if (location.hash.length !== 0) {
      window.scrollTo(window.scrollX, window.scrollY - 60);
    }
}

export function scrollOffset() {
    document.addEventListener('click', e => {
        if(e.target.hash || (e.target.firstChild && e.target.firstChild.hash) ) {
            if (e.target.firstChild.hash) {
                window.location.hash = e.target.firstChild.hash;
            }
            window.setTimeout(function() {
                offsetAnchor();
              }, 0);
        }
    });
}
