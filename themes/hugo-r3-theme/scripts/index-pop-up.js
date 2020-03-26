import $ from 'jquery';
import "bootstrap";

export function indexPopUp(id) {
    var key = id;
    var value = 'seen';
    if (localStorage.getItem(key) != value) {
        localStorage.setItem(key, value);
        $(id).modal({
            focus: true,
            show: true
        });
    }
}
