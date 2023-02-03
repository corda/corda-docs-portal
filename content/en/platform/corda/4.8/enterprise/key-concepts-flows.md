---
aliases:
- /head/key-concepts-flows.html
- /HEAD/key-concepts-flows.html
- /key-concepts-flows.html
date: '2023-02-01'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-key-concepts-flows
    parent: corda-enterprise-4-8-key-concepts
    weight: 1060
tags:
- concepts
- flows
title: Flows
---


# Flows

## Summary

* Communication between nodes is point-to-point using flows.
* Flows automate the process of agreeing ledger updates between two or more nodes.
* Built-in flows are provided to automate common tasks.

## Video

{{% vimeo 214046145 %}}

## Point-to-point messaging

Corda networks use point-to-point messaging, instead of a global broadcast model. To update the ledger, network participants
must specify what information needs to be sent, to which counterparties, and in what order.

Here is a visualisation of Alice and Bob agreeing a ledger update using this process:

{{< figure alt="flow" width=80% zoom="/en/images/flow.gif" >}}

## The flow framework

Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence
of steps that tells a node how to achieve a specific ledger update, such as issuing an asset or settling a trade.

Here is a diagram showing the flow's steps used between Alice and Bob to perform the ledger update:

{{< figure alt="flow sequence" width=80% zoom="/en/images/flow-sequence.png" >}}

## Running flows

Node operators use RPC calls to instruct their node to start a specific flow. The flow abstracts all
the networking, I/O, and concurrency issues away from the node operator.

All activity on the node occurs in the context of these flows. Unlike contracts, flows do not execute in a sandbox,
meaning that nodes can perform actions such as networking, I/O, and use sources of randomness within the execution of a
flow.

### Inter-node communication

Messages are passed from an active flow on one node to an active flow on another node. You can specify which flow classes
a node can respond to and with what flow it responds with.

For example, Alice is a node on the network and wishes to agree a ledger update with Bob, another network node. To
communicate with Bob:

1. Alice starts a flow that Bob is registered to respond to.
2. Alice sends Bob a message within the context of that flow.
3. Bob starts its registered counterparty flow.

Now that a connection is established, Alice and Bob can communicate to agree a ledger update by passing a series of
messages back and forth, as prescribed by the flow steps.

### Subflows

Flows can be composed by starting a flow as a subprocess in the context of another flow. The flow that is started as
a subprocess is known as a **subflow**. The parent flow will wait until the subflow returns.

#### The flow library

Corda provides a library of flows to handle common tasks, meaning that developers do not have to redefine the
logic behind common processes such as:

* Notarising and recording a transaction.
* Gathering signatures from counterparty nodes.
* Verifying a chain of transactions.

For further information on the available built-in flows, go to [API: Flows](api-flows.md).

## Concurrency

Nodes can have multiple active flows running at once.

Flows are serialized to disk whenever they enter a blocking state. For example, when they're waiting on I/O or a
networking call. This allows flows to be active for long periods of time, even during interruptions such as node restarts
and upgrades. Instead of waiting for the flow to become unblocked, the node immediately starts work on any
other scheduled flows, returning to the original flow at a later date.
