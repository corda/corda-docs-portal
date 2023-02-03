---
aliases:
- /head/key-concepts-node.html
- /HEAD/key-concepts-node.html
- /key-concepts-node.html
date: '2023-02-01'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-key-concepts-node
    parent: corda-enterprise-4-9-key-concepts
    weight: 1120
tags:
- concepts
- node
title: Nodes
---


# Nodes


* Nodes represent individuals and businesses on a Corda network.
* A node runs within a [Java Virtual Machine (JVM)](https://www.infoworld.com/article/3272244/what-is-the-jvm-introducing-the-java-virtual-machine.html) and has a unique network identity.
* The node interfaces with the outside world through:
  * The [network](key-concepts-ecosystem.md), which lets it interact with other nodes.
  * Remote procedure Call (RPC), which lets the node's owner interact with it.
* You can add extra functions to your node by installing [CorDapps](cordapps/cordapp-overview.md) in the plugin registry. CorDapps are distributed applications that let you accomplish different objectives with Corda.

## Video

{{% vimeo 214168860 %}}

## Node architecture

A Corda node runs within a Java Virtual Machine (JVM) runtime environment with a [unique network identity](key-concepts-ecosystem.html#node-identities). JVM runtime environments provide a consistent platform on which you can run and deploy Java applications, such as Corda services and
CorDapps. Here is a visualization of the node’s internal architecture:

{{< figure alt="node architecture" width=80% zoom="/en/images/node-architecture.png" >}}

The core elements of the architecture are:

* A persistence layer for storing data.
* A network interface for communication between nodes.
* An RPC interface for interacting with the node’s owner.
* The service hub, which lets the node’s flows call services in the node.
* A CorDapp interface and provider for extending the node by installing CorDapps.

## Persistence layer

The persistence layer has two parts:

* The **vault**, where the node stores any relevant current and historic states.
* The **storage service**, where it stores transactions, attachments, and flow checkpoints.

The node’s owner can query the node’s storage using the [RPC interface](#rpc-interface).

## Network interface

All communication with other nodes on the network is handled by the node itself, as part of running a flow. The
node’s owner does not interact with other network nodes directly.

## RPC interface

The node’s owner interacts with the node via remote procedure calls (RPC). The key RPC operations the node exposes
are documented in [API: RPC operations](api-rpc.md).

## The service hub

Internally, the node has access to a rich set of services that are used during flow execution to coordinate ledger
updates. The key services are:

* Information about other nodes on the network and the services they offer.
* Access to the contents of the [vault](key-concepts-vault.md) and the storage service.
* Access to the node’s public-private key pairs.
* Generation of new public-private key pairs.
* Information about the node itself.
* The current time, as tracked by the node.

## The CorDapp provider

Use the CorDapp provider to install new CorDapps which extend the behavior of the node.

Your node comes with several default CorDapps installed, which handle common tasks such as:

* Retrieving transactions and attachments from counterparties.
* Upgrading contracts.
* Broadcasting agreed ledger updates for recording by counterparties.

## Draining mode

You may want to decommission or shut down a node for various activities, such as planned maintenance and upgrades, or investigating
performance or latency issues. To shut down a node cleanly, you must drain it so that no node processes (or [flows](key-concepts-flows.md)) are active.

Checkpoints ensure durability against crashes and restarts, by freezing a flow and capturing its current status which is automatically saved to the database. When the node is restarted, it replays the flow from the last checkpoint.

Draining mode ensures that before shutting down:

* Commands requiring any new, RPC-initiated flows are rejected.
* Initial P2P session messages are not processed, meaning peers are not able to initiate new flows involving the node.
* All other activities proceed as usual, ensuring that the number of in-progress flows only goes down, not up.

Once the number of active flows reaches zero, it is safe to shut the node down.
The draining mode property is durable, meaning that restarting the node does not reset it to its default value and that an RPC command is required.

The node can be safely shut down via a drain using the [shell](node/operating/shell.md), Corda's embedded command line.
