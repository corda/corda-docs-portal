---
date: '2023-02-23'
title: "Network Operator Tooling"
menu:
  corda-5-beta:
    identifier: corda-5-beta-app-networks-tooling
    parent: corda-5-beta-app-networks
    weight: 2000
section_menu: corda-5-beta
---
This page lists the tools required by Corda Network Operators.

## curl

Examples in this documentation use the curl CLI to interact with HTTP endpoints on Linux and macOS. For information about installing curl, see the [curl documentation](https://curl.se/). Alternatives may be used if desired.
On Windows, PowerShell contains native support for HTTP calls.
## Corda CLI

Network operators require the Corda CLI to build CPIs.
For information about installation, see [Installing the Corda CLI]({{< relref "./installing-corda-cli.md" >}}).

## OpenSSL

Examples in this documentation use OpenSSL to display the content of certificates in a readable form. This is an optional tool. For information, see the [OpenSSL documentation](https://www.openssl.org/docs/). 