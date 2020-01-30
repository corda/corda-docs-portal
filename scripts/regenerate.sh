#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT="$( cd "$( dirname "$DIR" )" >/dev/null 2>&1 && pwd )"
REPOS=$ROOT/repos

echo "removing existing content"
find $ROOT/content ! -name '_index.md' -type f -exec rm -f {} +

echo "removing existing repos"
rm -rf $REPOS

echo "getting repos"
source $DIR/get_repos.sh

echo "running sphinx to convert rst -> md and copy to content/"
python3 run_sphinx.py
