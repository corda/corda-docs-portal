---
title: "Operating nodes"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes
    identifier: corda-5-dev-preview-1-nodes-operating
    weight: 3800
section_menu: corda-5-dev-preview
expiryDate: '2022-09-28'
---

In the Corda 5 Developer Preview, developers can expose Remote Procedure Call (RPC)
functionality via a secure HTTP API.

Before you can operate your node using the HTTP API for RPC (HTTP-RPC), you must:
1. <a href="configure-nodeconf.md">Configure the `node.conf` file</a>.
2. [Setup SSL encryption](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/setup-ssl-encryption.md).
3. [Configure authentication and authorization](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/authentication/authentication.md). Nodes support both basic authentication and Azure Active Directory (AD) single sign-on (SSO).
4. [Manage user permissions](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/set-permissions.md).

HTTP-RPC will run on node startup if you have configured the `node.conf` file. You can interact with your node using:
* [The Corda Node CLI](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/cli-curl/cli-curl.html#use-the-corda-node-cli-to-interact-with-nodes-via-http-rpc).
* <a href="cli-curl/cli-curl.html#invoke-http-rpc-using-curl">`curl` commands</a>.

You also have access to a dynamic [OpenAPI specification](https://swagger.io/docs/specification/about/)
(formerly known as the Swagger specification). For more information, read <a href="openapi.md">how to
locate your node's OpenAPI specification</a>.

{{< note >}}
Nodes in the Corda 5 Developer Preview can only support a single sandbox, running a single CorDapp at any one time.
{{< /note >}}
