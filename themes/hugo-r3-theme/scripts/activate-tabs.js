//  We want scripts to load last, including jquery.
//  Once jquery is loaded we can then 'activate' all the tabs.

import $ from 'jquery';
import 'jquery-ui';
import 'jquery-ui/ui/widgets/tabs';
import 'bootstrap';

const default_tab = "java";

export function activateTabs() {
    var elements = document.getElementsByClassName('r3-o-tabs');
    for (var i = 0; i < elements.length; i++) {
        var e = elements[i];
        var s = "#" + e.id;
        var default_tab_name = s + '-' + default_tab;

        // https://getbootstrap.com/docs/4.4/components/navs/#tabshow

        // Always make the first tab the visible one
        $(s + ' a').first().tab('show');

        // Unless it's the default tab i.e. 'java', in which case, show that instead
        var selector = s + ' a[href="' + default_tab_name + '"]';
        $(selector).tab('show');
    }
}
