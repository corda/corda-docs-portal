# Hugo based Corda docs

There are detailed instructions in the  [usage docs](usage-docs/readme.md).

Please read them!

## Quick Start

* Download [hugo](https://github.com/gohugoio/hugo/releases)
* clone this repo
* edit the markdown in `content`

## Installing and running hugo

### Docker

If you are on linux or MacOS:

```
$ make help

local-serve          Build and serve hugo locally from memory or just use 'hugo' directly
local-build          Build the site (once only into public/) or just use 'hugo' directly
hugo-docker-image    Build hugo docker image
hugo-build           Run hugo build in docker (once only, into public/)
hugo-serve           Serve site from docker
prod-hugo-build      Prod build, minimal size
prod-docker-image    Create the prod docker image
prod-docker-serve    Run the nginx container locally on port 8888
publish              Build site, and publish docker image to registry - MAIN TARGET
```

Run `make local-build` to create a Hugo image, and then

```
make local-serve
```

to self-host the site with live reload.

The `publish` target is covered in the CI section below.

#### Windows

Install hugo locally and ensure it's on your path (see tbe Native section below).

In principle `docker` should work in a WSL session but I haven't tested it yet.  Same instructions as above.

Files in WSL are trivially editable if you open Explorer and navigate to `\\wsl$\ubunutu` (IIRC) or use Visual Studio Code as your primary editor.


### Native

Go to here https://github.com/gohugoio/hugo/releases

Install one of the `extended` versions.

Ensure you are at the root of this repository.

Run:

```
hugo serve
```

to run and serve the site on http://localhost:1313


### CI/Jenkins

The `publish` target does everything and is intended to be run in the CI system (Jenkins), but can be run locally.  It:

* builds a Docker image with `hugo`
* runs the `hugo` docker image to produce the site in `/public`
* builds a Docker image of `nginx` containing the content of `/public`
* attempts to `docker push` to whatever Docker regisitry *you are currenty logged in to

In principle, `docker push` should fail on your desktop at the final stage.

As a developer your probably just want to run:

```
make prod-docker-image
make prod-docker-serve
```

to run and test the `nginx` image on your desktop.

##  Gotchas

* Index pages should be `_index.md` otherwise subpages don't get rendered.
    * https://discourse.gohugo.io/t/not-generating-any-pages-other-than-index/10565


## Regenerating the pages

This section will be removed.

Note:  you should install python 3, and ensure you have created a virtual env and activated it.

```
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
```

Run the `regenerate.sh` script:

* Deletes all content except `_index.md`
* Deletes all repositories in the (temp) `repos` folder
* Runs `get_repos.sh` to clone all repositories and branches
    * Edit this file to change what is cloned and checked out.
* Runs `run_sphinx.py` to convert each repo/branch from `rst` to `md` and copies the files to `content`

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
