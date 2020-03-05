export function activateListeners() {
    let tocToggle = document.querySelector(".r3-o-sidebar__toc-toggle");
    let toc = document.querySelector(".r3-o-toc");

    tocToggle.addEventListener(
        "click",
        () => {
            toc.classList.toggle("show-toc");
        },
        true
    );

    toc.querySelector("button").addEventListener(
        "click",
        () => {
            toc.classList.toggle("show-toc");
        },
        true
    );

    toc.addEventListener("click", () => {
        toc.classList.remove("show-toc");
    });
}
