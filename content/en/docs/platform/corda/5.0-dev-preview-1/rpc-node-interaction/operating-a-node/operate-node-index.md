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
functionality via a secure HTTP API, allowing you to operate your node without the need to use the internal RPC
interface. In addition, you also have access to a dynamic [OpenAPI specification](https://swagger.io/docs/specification/about/)
(formerly known as the Swagger specification).

Before you can operate your node using HTTP-RPC:
1. [Configure your node's node.conf file](configure-nodeconf.md).
2. [Setup SSL encryption](setup-ssl-encryption.md).
3. [Configure authentication and authorization](authentication/authentication.md). Nodes support both basic authentication and Azure Active Directory (AD) single sign-on (SSO).
4. [Manage user permissions](set-permissions.md).

You can operate your node [using the Corda Node CLI and `curl` commands](cli-curl/cli-curl.md).

