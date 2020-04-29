//  We want scripts to load last, including jquery.
//  Once jquery is loaded we can then 'activate' all the tabs.

import $ from 'jquery';
import 'jquery-ui';
import 'jquery-ui/ui/widgets/tabs';

export function activateTabs() {
    var elements = document.getElementsByClassName('r3-o-tabs');
    for (var i = 0; i < elements.length; i++) {
        var e = elements[i];
        var s = "#" + e.id;
        $(function () { $(s).tabs(); });
    }
}
