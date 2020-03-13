import "bootstrap";
import $ from "jquery";

(function bootstrapListenerCollapseNav(){
    $('.r3-o-sidebar__nav-content #TableOfContents>ul>li>a').on('click', function(){
        $('#r3-toc-nav').collapse('hide');
        document.querySelector("#reverseAni").beginElement();
    });
})();
