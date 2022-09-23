---
date: '2021-09-16'
title: Nodes
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-nodes
    weight: 800
section_menu: corda-5-dev-preview
---

As part of the Corda 5 Developer Preview, you can generate and host a secure HTTP API for your RPC interfaces using a
flexible module (HTTP-RPC). Clients no longer need to use the internal RPC interface to interact with their CorDapps.

HTTP-RPC generates web service endpoints from the properly annotated `RPCOps` interfaces and methods, and an
[OpenAPI 3](https://swagger.io/specification/)
standard JSON (also known as Swagger JSON) as a complete web service description. It also generates Swagger UI with
available authentication features that you can use to test the web service methods.

To interact with your node, the Corda Node CLI and `curl` commands allow you to start and kill flows, query the node's
vault, and perform operations on HTTP-RPC endpoints.

For more information, read about [developing nodes](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/developing-nodes-homepage.md) and [operating nodes](../../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/operating-nodes-homepage.md).
