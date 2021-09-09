---
title: "Operating a node"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-rpc-node-interaction
    identifier: corda-5-dev-preview-1-rpc-node-interaction-operate-node
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
---

As part of the Corda 5 Developer Preview, developers have the opportunity to expose Remote Procedure Call (RPC)
functionality via a secure HTTP API. This allows you to operate your node without the need to use the internal RPC
interface.

Before you can operate your node using HTTP-RPC, you must:
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
