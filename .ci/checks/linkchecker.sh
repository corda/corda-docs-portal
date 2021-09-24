#!/usr/bin/env bash
set -eu

CADDYCFG="$(mktemp /tmp/Caddyfile.XXXXXX)"
CADDULOG="$(mktemp /tmp/caddy-log.XXXXXX)"

cat << "EOT" | caddy fmt - >"${CADDYCFG}"
http://localhost:1313 {
  root * /src/public
  file_server
}
EOT

caddy start --config "${CADDYCFG}" &> "${CADDULOG}"

sleep 1

muffet http://localhost:1313 -e 'https?:[^l][^o]'
