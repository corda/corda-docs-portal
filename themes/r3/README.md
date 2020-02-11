# R3 Docs Hugo Theme

* Based on https://getbootstrap.com/docs/4.4
* https://r3-cev.atlassian.net/wiki/spaces/RI/pages/103907810/Marketing

## Building locally

Install `yarn` (see https://classic.yarnpkg.com/en/docs/install)

Then, if `yarn` is installed locally

* `yarn install`
* `yarn run build`

with watcher:

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
