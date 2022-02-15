---
aliases:
- /head/key-concepts-node.html
- /HEAD/key-concepts-node.html
- /key-concepts-node.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-node
    parent: corda-os-4-8-key-concepts
    weight: 1120
tags:
- concepts
- node
title: Nodes
---


# Nodes

## Summary

* Nodes represent individuals and businesses on a Corda network.
* A node is [JVM](https://www.infoworld.com/article/3272244/what-is-the-jvm-introducing-the-java-virtual-machine.html) runtime with a unique network identity running the Corda software.
* The node has two interfaces with the outside world:
  * A network layer, for interacting with other nodes
  * RPC, for interacting with the node’s owner
* The node’s functionality is extended by installing CorDapps in the plugin registry.

## Video

{{% vimeo 214168860 %}}

## Node architecture

A Corda node is a JVM runtime environment with a [unique network identity](../../../../../en/platform/corda/4.8/open-source/key-concepts-ecosystem.html#node-identities). A node hosts Corda services and
CorDapps. Here is a visualization of the node’s internal architecture:

{{< figure alt="node architecture" width=80% zoom="/en/images/node-architecture.png" >}}

The core elements of the architecture are:

* A persistence layer for storing data.
* A network interface for communication between nodes.
* An RPC interface for interacting with the node’s owner.
* The service hub allows the node’s flows to call upon the node’s other services.
* A CorDapp interface and provider for extending the node by installing CorDapps.

## Persistence layer

The persistence layer has two parts:

* The **vault**, where the node stores any relevant current and historic states
* The **storage service**, where it stores transactions, attachments and flow checkpoints

The node’s owner can query the node’s storage using the RPC interface (see below).

## Network interface

All communication with other nodes on the network is handled by the node itself, as part of running a flow. The
node’s owner does not interact with other network nodes directly.

## RPC interface

The node’s owner interacts with the node via remote procedure calls (RPC). The key RPC operations the node exposes
are documented in [API: RPC operations](api-rpc.md).

## The service hub

Internally, the node has access to a rich set of services that are used during flow execution to coordinate ledger
updates. The key services provided are:

* Information on other nodes on the network and the services they offer.
* Access to the contents of the [vault](../../../../../en/platform/corda/4.8/open-source/key-concepts-vault.html) and the storage service.
* Access to the node’s public-private key pairs.
* Generation of new public-private key pairs.
* Information about the node itself.
* The current time, as tracked by the node.

## The CorDapp provider

New CorDapps are installed using the CorDapp provider and are used to extend the behavior of the node.

Several CorDapps are installed on the node by default to handle common tasks such as:

* Retrieving transactions and attachments from counterparties.
* Upgrading contracts.
* Broadcasting agreed ledger updates for recording by counterparties.

## Draining mode

Nodes can be decommissioned from the network, but in order to shut down a node cleanly, it is important that no node processes (or ['flows'](../../../../../en/platform/corda/4.8/open-source/key-concepts-flows.html)) are active,
meaning no [checkpoints](../../../../../en/platform/corda/4.8/open-source/contributing-flow-internals.html#checkpoints) are persisted. Checkpoints freeze a flow and capture its current
status, and they are automatically saved to the database when a flow suspends or resumes. A flow can be replayed from the last checkpoint if the node restarts, with this automatic checkpointing
ensuring durability against crashes and restarts. It is important that all of this in-progress data is cleared in anticipation of shutting down a node. The draining mode ensures that before shutting down:

* Commands requiring any new, RPC-initiated flows are rejected.
* Initial P2P session messages are not processed, meaning peers are not able to initiate new flows involving the node.
* All other activities proceed as usual, ensuring that the number of in-progress flows only goes down, not up.

Once the number of activities reaches zero, it is safe to shut the node down.
The draining mode property is durable, meaning that restarting the node does not reset it to its default value and that an RPC command is required.

The node can be safely shut down via a drain using the [shell](../../../../../en/platform/corda/4.8/open-source/shell.md), Corda's embedded command line.
