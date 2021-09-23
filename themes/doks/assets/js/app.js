import {DocsiteCookies} from "./cookie-banner";

document.addEventListener('DOMContentLoaded', () => {
  new DocsiteCookies();

  // Update for internal link with .md
  var external = RegExp('^((f|ht)tps?:)?//(?!' + location.host + ')');
  document.querySelectorAll('main a[href]').forEach((link) => {
    let url = link.getAttribute('href');
    if (false === external.test(url) && url.endsWith('.md')){
      url = url.substr(0, url.length - 3) + '.html';
      link.setAttribute('href', url);
    }
  });

  // Track all sections that have an `id` applied
  document.querySelectorAll('main h2, main h3, main h4, main h5').forEach((header) => {
    if (header.hasAttribute('id')) {
      const id = header.getAttribute('id');
      const menu = document.querySelector(`#TableOfContents li a[href="#${id}"]`);
      if (menu){
        menu.setAttribute('data-offsettop', header.offsetTop);
      }
    }
  });

  // Update active item for content
  document.addEventListener('scroll', function(e) {
    const pos = window.scrollY + window.innerHeight - 100;
    let max = 0;
    document.querySelectorAll(`#TableOfContents li a`).forEach((item) => {
      let top = parseInt(item.dataset.offsettop);
      if (top > max && top < pos){
        max = item.dataset.offsettop;
      }
      item.classList.remove('active');
    });

    const menu = document.querySelector(`#TableOfContents li a[data-offsettop="${max}"]`);
    if (menu){
      menu.classList.add('active');
    }
  });


  var sidebar = document.getElementsByClassName('docs-sidebar');
  if (sidebar.length > 0){
    sidebar = sidebar[0];

    var menuBtn = document.getElementById("menu-btn");
    menuBtn.addEventListener('change', e => {
      if(menuBtn.checked) {
        sidebar.classList.add('show');
      }
      else{
        sidebar.classList.remove('show');
      }
    });

    // hide sidebar when user click outside of menu on mobile
    sidebar.addEventListener('click', e => {
      if(e.target === e.currentTarget) {
        sidebar.classList.remove('show');
        menuBtn.checked = false;
      }
    });
  }
});
