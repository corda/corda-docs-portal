#!/usr/bin/env bash
set -eu

INDEX="/usr/share/nginx/html/index.xml"

if [ -f "${INDEX}" ]
then
  NEWURL="$1"; shift

  BASEURL=$(sed -n 's;.*<link>\([^<]*/\)</link>.*;\1; p' "${INDEX}")

  if [ "x${BASEURL}" != x ] && [ "x${BASEURL}" != "x${NEWURL}" ]
  then
    echo "Updating base URL from '${BASEURL}' to '${NEWURL}'"
    while read -r file
    do
      sed -i -e 's!'"${BASEURL}"'!'"${NEWURL}"'!g' "${file}"
    done < <(grep --files-with-matches --ignore-case --recursive --fixed-strings "${BASEURL}" "$(dirname "${INDEX}")")
    echo "Updating base URL has been done"
  fi
fi

exec nginx -g 'daemon off;'
