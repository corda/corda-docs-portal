#  R3 Docs Site Usage

These pages are not rendered by Hugo.  Hugo only renders pages in the `/content` folder.

These pages explain how to add more documentation, and some of the site design.

Hugo has extensive [documentation](https://gohugo.io/getting-started/quick-start/).

The docs site runs with _continuous deployment_.  When your pull request is merged the changes will be deployed to 'production' once an automatic hugo build is complete.

## Quick Start

Download:

* [Visual Studio Code](https://code.visualstudio.com/) or an editor of your choice.
* [Hugo](https://github.com/gohugoio/hugo/releases)
    * Ensure the `hugo` binary is on your `PATH`
* [Fork this repository](https://guides.github.com/activities/forking/) (you can clone it, but you won't be able to push).

Then:

```
cd docs-site
hugo serve
```

* Open http://localhost:1313 (or whatever it says in the console)
* Finally, edit Markdown and watch the page update!

## I am...

### ...Authoring Content

* [Editing pages](editing-pages.md)
* [Pushing your changes](pushing-page-changes.md)

### ...Authoring New Versions and Modifying the Site

* [New documentation versions](new-versions.md)
* [How do the side menus work?](hugo-menus.md)
* [How does internationlization work?](i18n.md)

### ...Modifying the Theme

* Start with the [Hugo documentation](https://gohugo.io/documentation/).
* Clone the [Hugo R3 theme](https://github.com/corda/hugo-r3-theme)
* [Site design](site-design.md)

### ...Changing the Build Pipeline

* [Makefiles, docker, and nginx](technical-details.md)