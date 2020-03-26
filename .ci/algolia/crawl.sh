#!/usr/bin/env bash
# pass these in:  

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

ALGOLIA_APPLICATION_ID=$1
ALGOLIA_API_ADMIN_KEY=$2

ALGOLIA_CONFIG=$(jq -r tostring $THIS_DIR/algolia.search.json)

echo $ALGOLIA_CONFIG

docker run -e "APPLICATION_ID=$ALGOLIA_APPLICATION_ID" -e "API_KEY=$ALGOLIA_API_ADMIN_KEY" -e 'CONFIG='"$ALGOLIA_CONFIG"'' algolia/docsearch-scraper
