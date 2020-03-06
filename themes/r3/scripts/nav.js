export function activateListeners() {
    let navToggle = document.querySelector(".r3-o-sidebar__nav-toggle");
    let nav = document.querySelector(".r3-o-nav");

    navToggle.addEventListener(
        "click",
        () => {
            nav.classList.toggle("show-nav");
        },
        true
    );

    nav.querySelector("button").addEventListener(
        "click",
        () => {
            nav.classList.toggle("show-nav");
        },
        true
    );

    nav.addEventListener("click", () => {
        nav.classList.remove("show-nav");
    });
}
