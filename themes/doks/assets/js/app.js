function feedbackDocs(element){
  var opposite = (element.dataset.action === 'like') ? 'opinion-dislike' : 'opinion-like';
  document.getElementById(opposite).classList.remove('show');

  if (ga){
    ga('send', 'event', 'Feedback', element.dataset.action, element.dataset.doc);
  }
  else{
    console.error('Google Analytic not found');
  }
}

function toggleSideBar(){
  var items = document.getElementsByClassName('docs-sidebar');
  if (items.length > 0){
    var sidebar = items[0];

    if (sidebar.classList.contains('show')){
      sidebar.classList.remove('show');
    }
    else{
      sidebar.classList.add('show');
    }
  }

}

document.addEventListener('DOMContentLoaded', () => {
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

  // hide sidebar
  var sidebar = document.getElementsByClassName('docs-sidebar');
  if (sidebar.length > 0){
    sidebar = sidebar[0];

    sidebar.addEventListener('click', e => {
      if(e.target === e.currentTarget) {
        sidebar.classList.remove('show');
        document.getElementById("menu-btn").checked = false;
      }
    });
  }
});
