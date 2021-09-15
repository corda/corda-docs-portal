---
title: "Operating nodes"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes
    identifier: corda-5-dev-preview-1-nodes-operating
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
---

In the Corda 5 Developer Preview, developers can expose Remote Procedure Call (RPC)
functionality via a secure HTTP API.

Before you can operate your node using the HTTP API for RPC (HTTP-RPC), you must:
1. [Configure your node's `node.conf` file](configure-nodeconf.md).
2. [Setup SSL encryption](setup-ssl-encryption.md).
3. [Configure authentication and authorization](authentication/authentication.md). Nodes support both basic authentication and Azure Active Directory (AD) single sign-on (SSO).
4. [Manage user permissions](set-permissions.md).

You can operate your node using:
* [The Corda Node CLI](cli-curl/cli-curl.md#use-corda-node-cli-to-interact-with-nodes-via-http-rpc).
* [`curl` commands](cli-curl/cli-curl.md#invoke-http-rpc-using-curl).

You also have access to a dynamic [OpenAPI specification](https://swagger.io/docs/specification/about/)
(formerly known as the Swagger specification). For more information, see
[locating your node's OpenAPI specification](openapi.md).
