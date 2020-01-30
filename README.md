# Hugo based Corda docs

* Ensure you install the 'extended' version of hugo:
    * https://gohugo.io/troubleshooting/faq/#i-get-this-feature-is-not-available-in-your-current-hugo-version

* Searching for help:  ensure you include the word `gohugo` in the search.

* Shortcodes allow to write richer markdown pages (e.g. tabbed code).

New page:

```
hugo new posts/my_new_post.md
```

## Installing and running hugo

### Docker

If you are on linux or MacOS:

```
$ make help

docker-image         Build hugo docker image
docker-build         Run hugo build in docker
docker-serve         Serve site from docker
```

Run `make docker-image` to create a Hugo image, and then

```
make docker-serve
```

to self-host the site with live reload.

#### Windows

Install hugo locally and ensure it's on your path.  

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


##  Gotchas

* Index pages should be `_index.md` otherwise subpages don't get rendered.
    * https://discourse.gohugo.io/t/not-generating-any-pages-other-than-index/10565


## Regenerating the pages

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
