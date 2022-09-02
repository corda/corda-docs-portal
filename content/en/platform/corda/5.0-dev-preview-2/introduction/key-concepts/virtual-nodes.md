---
date: '2020-07-15T12:00:00Z'
title: "Virtual nodes"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 6000
section_menu: corda-5-dev-preview
---

## Overview

Corda 5 introduces the concept of virtual nodes to allow multi-tenancy. A virtual node, or group member, is a [Corda identity](../key-concepts.html#corda-identities) granted admission to a membership group. A virtual node contains everything needed to communicate and transact on Corda: keys, certificates, and storage. This enables the identity to join application networks, where they can interact with other group members according to the terms set by the [Membership Group Manager (MGM)](../../mgm/overview.html). Identities can join multiple application networks from one physical node infrastructure using virtual nodes.

Virtual nodes can be:
* **Multi-tenant.** You can host multiple virtual nodes on one deployment of Corda, at no additional cost.
* **Portable.** You can move a virtual node from one host to another.
* **Highly-available.** If you configure your node to be highly available, if it goes down, an identical one takes its place instantly.

To get a node ready to interact with others on application networks, it must be onboarded. The virtual node creates a [sandbox](../key-concepts.html#sandboxes). This is an area where the [CPI](../key-concepts.html#package-installer-cpi) can exist in isolation. The CPI can not see any other tenants on the host deployment and the other tenants can not see it. It associates that sandbox with a Corda identity and gets its keys, certificates, and storage.

Virtual nodes are built on several processes, which run independently and scale up and down based on need. These are called [workers](../key-concepts.html#workers), and can include the crypto worker, database worker, flow worker, and persistence worker, depending on the topology of a specific deployment.

## Communication

The processes communicate with each other using a message bus, Kafka. This ensures the information ends up in the right place at the right time. The message bus:
* Captures blobs of data, called events, that the processes generate.
* Interprets the data and stores it until the moment it becomes relevant.
* Delivers the message to the recipient process when the recipient process requires the information, preventing bottlenecks of information.

Virtual nodes communicate using flows. The message bus that links the processes supporting the virtual node also communicates with the Corda gateway. The gateway sends flows between virtual nodes through a secure HTTPS link.

You can use remote procedure calls (RPC) to interact with a virtual node. This functionality is exposed by the HTTPS REST API. You can use RPC to interact with the virtual node using:
* A command line interface (CLI).
* curl commands.

Virtual nodes generate a dynamic OpenAPI specification. You can locate this specification to get details of your virtual node's RPC functionality, including the endpoints, operations, operation parameters, and authentication methods.
