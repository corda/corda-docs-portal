#!/usr/bin/env bash

PATH=$PATH:/usr/bin

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT="$( cd "$( dirname "$DIR" )" >/dev/null 2>&1 && pwd )"

npm install --prefix $ROOT/search

cd $ROOT
# TODO:  location of output by language
node search/build-lunrjs-index.js > $ROOT/static/search-index.json
