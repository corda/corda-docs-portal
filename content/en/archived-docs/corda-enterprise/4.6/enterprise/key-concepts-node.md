---
aliases:
- /head/key-concepts-node.html
- /HEAD/key-concepts-node.html
- /key-concepts-node.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-key-concepts-node
    parent: corda-enterprise-4-6-key-concepts
    weight: 1120
tags:
- concepts
- node
title: Nodes
---


# Nodes

## Summary

* *A node is JVM run-time with a unique network identity running the Corda software*
* *The node has two interfaces with the outside world:*
  * *A network layer, for interacting with other nodes*
  * *RPC, for interacting with the node’s owner*
* *The node’s functionality is extended by installing CorDapps in the plugin registry*

## Video

{{% vimeo 214168860 %}}

## Node architecture

A Corda node is a JVM run-time environment with a unique identity on the network that hosts Corda services and
CorDapps.

We can visualize the node’s internal architecture as follows:

{{< figure alt="node architecture" width=80% zoom="/en/images/node-architecture.png" >}}
The core elements of the architecture are:

* A persistence layer for storing data
* A network interface for interacting with other nodes
* An RPC interface for interacting with the node’s owner
* A service hub for allowing the node’s flows to call upon the node’s other services
* A cordapp interface and provider for extending the node by installing CorDapps

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

* Information on other nodes on the network and the services they offer
* Access to the contents of the vault and the storage service
* Access to, and generation of, the node’s public-private keypairs
* Information about the node itself
* The current time, as tracked by the node

## The CorDapp provider

The CorDapp provider is where new CorDapps are installed to extend the behavior of the node.

The node also has several CorDapps installed by default to handle common tasks such as:

* Retrieving transactions and attachments from counterparties
* Upgrading contracts
* Broadcasting agreed ledger updates for recording by counterparties

## Draining mode

In order to operate a clean shutdown of a node, it is important than no flows are in-flight, meaning no checkpoints should
be persisted. The node is able to be put in draining mode, during which:

* Commands requiring to start new flows through RPC will be rejected.
* Scheduled flows due will be ignored.
* Initial P2P session messages will not be processed, meaning peers will not be able to initiate new flows involving the node.
* All other activities will proceed as usual, ensuring that the number of in-flight flows will strictly diminish.

As their number reaches zero, it is safe to shut the node down.
This property is durable, meaning that restarting the node will not reset it to its default value and that a RPC command is required.

The node can be safely shut down via a drain using the shell.
