import { debounce } from "lodash-es";
export function searchShortcut() {
    const body = document.querySelector("body");
    const searchBar = document.querySelector("#search-input");

    const pressForwardSlash = debounce(function(searchBar) {
        searchBar.focus();
    }, 400);

    body.addEventListener("keydown", e => {
        if (e.key === "/" && e.target !== searchBar) {
            e.preventDefault();
            pressForwardSlash(searchBar);
        }
    });
}
