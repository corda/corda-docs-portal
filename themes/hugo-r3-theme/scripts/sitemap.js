// The function actually applying the offset
function offsetAnchor() {
    if (location.hash.length !== 0) {
        window.scrollTo(window.scrollX, window.scrollY - 80);
    }
}

export function scrollOffset() {
    document.addEventListener('click', e => {
        // Are we a url that ends with '#some-anchor'?
        // ...and we're an anchor in the current page.
        // Otherwise we break every link with an anchor...
        if (e.target.hash && e.target.pathname === window.location.pathname) {
            e.preventDefault();
            if (window.location.hash !== e.target.hash) {
                window.location.hash = e.target.hash;
                offsetAnchor();
            }
        }

        if (e.target.firstChild && e.target.firstChild.hash) {
            window.location.hash = e.target.firstChild.hash;
            window.setTimeout(
                () => offsetAnchor(),
                0
            );
        }
    });
}

export function clickLinkOnNavExpandDropDown() {
    let docsNav = document.querySelector('.r3-o-docs-nav');
    if (docsNav) {
        docsNav.addEventListener('click', e => {
            if (e.target.type === "checkbox") {
                let nodes = e.target.parentElement.children;
                for (let node of nodes) {
                    if (node.href && node.href !== window.location.href) {
                        window.location.href = node.href;
                    }
                }
            }
        });
    }
}

export function uncheckDropDownOnClick() {
    let docsNav = document.querySelector('.r3-o-docs-nav');
    if (docsNav) {

        let checkboxes = docsNav.querySelectorAll('input[type=checkbox]');

        for (let box of checkboxes) {
            if (window.location.pathname === box.dataset.url) {
                box.checked = false;
            }
        }
        docsNav.style.display = "block";
    }
}
