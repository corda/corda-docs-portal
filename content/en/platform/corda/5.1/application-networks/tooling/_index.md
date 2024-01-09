---
description: "Review the tools required by Network Operators."
date: '2023-04-07'
title: "Network Operator Tooling"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-tooling
    parent: corda51-networks
    weight: 2000
section_menu: corda51
---
<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}

</style>

# Network Operator Tooling
Corda Network Operators require the following:

| Tool      | Description                                                                                                                                                                                                                                                                                    |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| curl      | Examples in this documentation use the curl CLI to interact with HTTP endpoints on Linux and macOS. For information about installing curl, see the [curl documentation](https://curl.se/). Alternatives may be used if desired. On Windows, PowerShell contains native support for HTTP calls. |
| Corda CLI | Network operators require the Corda CLI to build {{< tooltip >}}CPIs{{< /tooltip >}}. For information about installation, see [Installing the Corda CLI]({{< relref "./installing-corda-cli.md" >}}).                                                                                          |
| OpenSSL   | Examples in this documentation use OpenSSL to display the content of certificates in a readable form. This is an optional tool. For information, see the [OpenSSL documentation](https://www.openssl.org/docs/).                                                                               |
