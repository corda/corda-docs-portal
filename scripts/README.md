# Scripts

This folder will be removed.

It's only purpose is to contain some scripts to convert the old `rst` files into `md`.

Don't try and use it for your own purposes.

## Regenerating the pages

Note:  you should install python 3, and ensure you have created a virtual env and activated it.

```shell
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


It's all self contained.

To run the conversion script:

```
    cd <project root>
    python3 -m venv .venv
    source .venv/bin/activate
    cd scripts
    pip3 install -r requirements.txt
    ./regenerate.sh
``` 
