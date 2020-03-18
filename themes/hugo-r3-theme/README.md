# R3 Docs Hugo Theme

* Based on https://getbootstrap.com/docs/4.4
* https://r3-cev.atlassian.net/wiki/spaces/RI/pages/103907810/Marketing

## Building locally

Install `yarn` (see https://classic.yarnpkg.com/en/docs/install)

Then, if `yarn` is installed locally

* `yarn install`
* `yarn run devenv`

which run:

```
webpack --config webpack.config.js --mode development --watch
```

and

```
hugo serve --source ../..
```

where `../..` is the site location relative to the theme.

### Alternative Ways Of Running

With watcher:

* `yarn run build --watch`

Dev build is:

* `yarn run build-dev`

## Building via Docker

There is a `docker`ized build:

Dev:

* `make docker-image`
* `make docker-build-watch`

Prod:

* `make docker-image`
* `make docker-build`


## TODO Snag List

- [ ] Get rid of footer.
- [ ] Heading sizes, and spaces 2x space above heading and previous paragraph, (suggested 2x space == 44px) as below heading and next paragraph.
- [ ] Contrast on the left menu is too weak. Make font a darker blue.
- [ ] "TUT TWO PARTY INTRODUCTION" looks like it's in the wrong place? Does the new sidebar support multiple levels of nesting? The sidebar organisation now lacks the grouping the current site has.
- [ ] There's some sort of invisible frame for the sidebar, so you can scroll to the bottom of the content and not realise you haven't scrolled to the bottom of the sidebar. You have to scroll over the sidebar itself to see that but there's no visual hint that this is required, e.g. no scrollbar. Can we make the sidebar be a part of the same frame as the content so there's only one scrollpane?
- [ ] We could use some padding in the source code snippet blocks. 22px padding on the side
- [ ] API links are broken.
- [ ] Search doesn't work for me. Typing a query and pressing enter does nothing.

- [x] Extract css from theme for landing page.
- [x] Maybe the animation for opening a sidebar section doesn't need to trigger when just navigating between parts of a section that's already open?
