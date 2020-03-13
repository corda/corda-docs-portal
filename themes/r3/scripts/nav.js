export function activateListeners() {
    let navToggle = document.querySelector(".r3-o-sidebar__nav-toggle");
    let nav = document.querySelector(".r3-o-nav");
    let navTransparent = document.querySelector(".r3-o-wrapper-nav");

    if (navToggle) {
        navToggle.addEventListener(
            "click",
            () => {
                nav.classList.toggle("show-nav");
                navTransparent.classList.add("show-nav");
            },
            true
        );
    }

    navTransparent.addEventListener("click", e => {
        if(e.target === navTransparent) {
            nav.classList.toggle("show-nav");
            navTransparent.classList.remove("show-nav");
        }
    });
}
