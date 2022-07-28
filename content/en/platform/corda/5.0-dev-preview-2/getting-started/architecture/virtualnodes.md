---
date: '2020-07-15T12:00:00Z'
title: "Virtual nodes"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-virtual-nodes
    parent: corda-5-dev-preview-architecture
    weight: 2000
section_menu: corda-5-dev-preview
---
a virtual node is the virtual mapping between application processes, data and identity and keys to form the logical equivalent of a Corda 4 node (such as Alice in Network 1 with App A/B/C).

This is an exciting step forward for:

enabling true (virtual) node multi-tenancy on a shared cluster
> this is important for managed service providers or developers looking at progressive decentralisation.
enabling multi-network
> Alice can join several application networks using the same “client” at no margin cost.
reducing cost of ownership
> particularly for operating models where previously multiple nodes were deployed
improving development/test experience
> particularly for production-like tests, dynamic configuration of a cluster (with several virtual nodes) allows for a much faster and simpler test set up/ run time.
Finally — as virtual nodes are just a mapping between processes, data, and keys, they can be…. portable.
Virtual nodes makes it easy to join multiple networks. Rather than having multiple Corda deployments you can have multiple virtual nodes, allowing you to be easily represented in each network with separate identities.

Group member
A Corda identity that has been granted admission to a membership group. Synonym for a virtual node.

A virtual node represents a [Corda identity](#corda-identities), a person or business that wants to interact with other people or businesses using Corda. A virtual node contains everything needed to communicate and transact on Corda: keys, certificates, and storage. This enables the identity to join application networks, where they can interact with other group members according to the terms set by the [Membership Group Manager (MGM)](../mgm/overview.html). Identities can join multiple application networks from one physical node infrastructure using virtual nodes.

Virtual nodes can be:
* **Multi-tenant.** You can host multiple virtual nodes on one deployment of Corda, at no additional cost.
* **Portable.** You can move a virtual node from one host to another.
* **Highly-available.** If you configure your node to be highly available, if it goes down, an identical one takes its place instantly.

## What is it made of?
Nothing — it's virtual! You can think of a virtual node as an environment that enables the processor to locate a specific [CPI](#package-installer-cpi) file. The flows associated with the CPI let the virtual node communicate with others. The contracts define that virtual node's rules for verifying transactions.

## How does it work?
To get a node ready to interact with others on application networks, it must be onboarded. The virtual node creates a [sandbox](#sandboxes) — an area where the [CPI](#package-installer-cpi) can exist in isolation, meaning it can't see any other tenants on the host deployment, and the other tenants can not see it. It associates that sandbox with a Corda identity and gets its keys, certificates, and storage.

Virtual nodes are built on several processes, which run independently and scale up and down based on need. These are called [workers](#workers), and can include the crypto worker, database worker, flow worker, and persistence worker, depending on the topology of a specific deployment.

The processes communicate with each other using a message bus, Kafka. This ensures the information ends up in the right place at the right time. The message bus:
* Captures blobs of data, called events, that the processes generate.
* Interprets the data and stores it until the moment it becomes relevant.
* Delivers the message to the recipient process when the recipient process requires the information, preventing bottlenecks of information.

## How do virtual nodes communicate with each other?
Virtual nodes communicate using flows. The message bus that links the processes supporting the virtual node also communicates with the Corda gateway. The gateway sends flows between virtual nodes through a secure HTTPS link.

## How do I interact with my virtual node?
You can use remote procedure calls (RPC). This functionality is exposed by the HTTPS REST API.

You can use RPC to interact with the virtual node using:
* A command line interface (CLI).
* curl commands.

Virtual nodes generate a dynamic OpenAPI specification. You can locate this specification to get details of your virtual node's RPC functionality, including the endpoints, operations, operation parameters, and authentication methods.
