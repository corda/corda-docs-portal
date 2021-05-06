# Corda Developer Documentation

[![Build Status](https://ci01.dev.r3.com/buildStatus/icon?job=Docs-Builders%2FBuild%2Fcorda-docs%2Fmaster)](https://ci01.dev.r3.com/job/Docs-Builders/job/Build/job/corda-docs/job/master/)

There are detailed instructions in the  [usage docs](usage-docs/readme.md).

Please read them!

You will need:

* [hugo](https://github.com/gohugoio/hugo/releases)  (a single binary on all platforms)
    * Use the latest version, otherwise at least v0.65
* a text editor: we strongly recommend [Visual Studio Code](https://code.visualstudio.com/).

## Quick Start

* Download [hugo](https://github.com/gohugoio/hugo/releases)
* clone this repo
* `cd` into the root of the repo and run `hugo serve`
* edit the markdown in `content`

### Edit The Current Web Page

If you have installed VSCode, you can run `hugo` in a mode that allows you to open markdown content from the browser.

On Mac or Linux, start `hugo` using:

```makefile
make local-serve-and-edit
```

In Powershell (Windows ...and Linux!):

```powershell
serve_and_edit.ps1
```

and you will see:

![edit markdown](usage-docs/images/page-edit.png)

## Installing and Running Hugo

### Docker

If you are on Linux or MacOS you can also build using Docker images (WSL2 not supported yet), type `make help` to see the options

#### Windows

Install `hugo` locally and ensure it is on your path (see tbe Native section below).

It is also available via `choco`.

#### Mac and Linux

Hugo is available via `brew`, and most Linux package installers (`apt`, `pacman`, and so on).

### Binary Download

Go to here https://github.com/gohugoio/hugo/releases

Install one of the `extended` versions.

## CI/Jenkins

The `publish` target does everything and is intended to be run in the CI system (Jenkins), but can be run locally.  It:

* builds a Docker image with `hugo`
* runs the `hugo` docker image to produce the site in `/public`
* builds a Docker image of `nginx` containing the content of `/public`
* attempts to `docker push` to whatever Docker registry *you are currently logged in to.

In principle, `docker push` should fail on your desktop at the final stage.

As a developer your just want to run:

```
make prod-docker-serve
```

to run and test the `nginx` image on your desktop.


##  Docker build configuration

It is possible to override the `baseURL` of the project at build time.

One way to do this is to use the configuration files, e.g.

```shell script
make HUGO_ARGS="--config config.toml,config.dev.toml" prod-docker-serve
```

which makes the `nginx` image and starts it on port 8888

The alternative is to run:

```shell script
make DOCKER_BUILD_ARGS="-e HUGO_BASEURL=\"http://localhost:8888\"" prod-docker-serve
```

If you need to change many parameters in Hugo's configuration, then prefer
to use the configuration file override.
