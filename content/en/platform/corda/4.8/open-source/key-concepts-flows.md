---
aliases:
- /head/key-concepts-flows.html
- /HEAD/key-concepts-flows.html
- /key-concepts-flows.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-flows
    parent: corda-os-4-8-key-concepts
    weight: 1060
tags:
- concepts
- flows
title: Flows
---


# Flows

## Summary

* Flows automate the process of agreeing ledger updates.
* Communication between nodes only occurs in the context of these flows, and is point-to-point.
* Built-in flows are provided to automate common tasks.

## Video

{{% vimeo 214046145 %}}

## Point-to-point messaging

Corda networks use point-to-point messaging, instead of a global broadcast. To update the ledger, network participants
must specify what information needs to be sent, to which counterparties, and in what order.

Here is a visualisation of Alice and Bob agreeing a ledger update using this process:

{{< figure alt="flow" width=80% zoom="/en/images/flow.gif" >}}

## The flow framework

Rather than having to specify these steps manually, Corda automates the process using *flows*. A flow is a sequence
of steps that tells a node how to achieve a specific ledger update, such as issuing an asset or settling a trade.

Here is the flow's sequence of steps to perform the ledger update between Alice and Bob:

{{< figure alt="flow sequence" width=80% zoom="/en/images/flow-sequence.png" >}}

## Running flows

Once a given business process has been encapsulated in a flow and installed on the node as part of a CorDapp, the node’s
owner can instruct the node to kick off this business process at any time using an RPC call. The flow abstracts all
the networking, I/O and concurrency issues away from the node owner.

All activity on the node occurs in the context of these flows. Unlike contracts, flows do not execute in a sandbox,
meaning that nodes can perform actions such as networking, I/O and use sources of randomness within the execution of a
flow.

### Inter-node communication

Nodes communicate by passing messages between flows. Each node has zero or more flow classes which it is registered to
respond to messages from.

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

Further information on the available built-in flows can be found in [API: Flows](api-flows.md).

## Concurrency

Nodes can have multiple active flows running at once.

Flows are serialized to disk whenever they enter a blocking state. For example, when they're waiting on I/O or a
networking call. This allows flows to be active for long periods of time, even during interruptions such as node restarts
and upgrades. Instead of waiting for the flow to become unblocked, the node immediately starts work on any
other scheduled flows, returning to the original flow at a later date.
