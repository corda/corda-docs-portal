#!/usr/bin/env bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ROOT_DIR="$( cd "$( dirname $( dirname "$THIS_DIR" ))" >/dev/null 2>&1 && pwd )"

IMAGE_NAME=$1

echo Using docker image $IMAGE_NAME

HOST="docs.corda.net"

# Uses the built image outside of this script
id=$(docker run --rm -d -v $THIS_DIR/rebase_url.sh:/entry.sh --entrypoint=/entry.sh corda-docs-nginx "http://${HOST}/")
echo $id

trap 'docker kill $id' EXIT

ATTEMPTS=0
while [ $ATTEMPTS -lt 10 ]
do
  ATTEMPTS=$((ATTEMPTS + 1))
  echo "Try: ${ATTEMPTS}"
  docker exec -it $id pidof nginx &>/dev/null && break
  sleep 10
done

docker run -it --rm --link $id:${HOST} -u $(id -u):$(id -g) -v $THIS_DIR:/mnt linkchecker/linkchecker --verbose http://${HOST} --check-extern --quiet -F csv/utf-8/links.csv --ignore-url=".*\.md"
STATUS=$?

docker kill $id
docker rm $id

# Early exits
# All OK
if [[ $STATUS -eq 0 ]]; then
    exit 0
fi

# Could be a problem with docker, but likely linkchecker threw an exception
if [[ $STATUS -eq 2 ]]; then
    echo ERROR:  docker or linkchecker failed somehow
    exit $STATUS
fi

# '1' is broken links according to linkchecker docs
# https://linkchecker.github.io/linkchecker/man1/linkchecker.1.html
if [[ $STATUS -ne 1 ]]; then
    echo ERROR:  unknown exit code $status
    exit $STATUS
fi

docker run -it --rm -v $THIS_DIR:/mnt -w /mnt python:3 python report_broken_links.py links.csv
