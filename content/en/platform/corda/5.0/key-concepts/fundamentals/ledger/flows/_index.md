---
title: "Flows"
date: 2023-06-08
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-ledger-flows
    parent: corda5-fundamentals-ledger
    weight: 4000
section_menu: corda5
---

# Flows


Communication between participants in an application network is point-to-point using flows. Flows automate the process of agreeing ledger updates between two or more participants. Built-in flows are provided to automate common tasks.

## Point-to-Point Messaging

Corda networks use point-to-point messaging, instead of a global broadcast model. To update the ledger, network participants must specify what information needs to be sent, to which counterparties, and in what order.

For example, the following shows Alice and Bob agreeing a ledger update using this process:

{{< 
  figure
	 width="50%"
	 src="flow.gif"
	 figcaption="Messaging Example"
>}}

## Flow Framework

Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a virtual node how to achieve a specific ledger update, such as issuing an asset or settling a trade.
For example, the following shows the flow’s steps used between Alice and Bob to perform the ledger update:

{{< 
  figure
	 width="50%"
	 src="flow-sequence.png"
	 figcaption="Flow Sequence Example"
>}}

## Running Flows

Node operators use [REST]({{< relref "../../../../reference/rest-api/_index.md">}}) calls to instruct their node to start a specific flow. The flow abstracts all the networking, I/O, and concurrency issues away from the node operator.
All activity on the node occurs in the context of these flows. Unlike contracts, flows execute in a flow sandbox, meaning that nodes can perform actions such as networking, I/O, and use sources of randomness within the execution of a flow.

### Inter-Node Communication
Messages are passed from an active flow on one virtual node to an active flow on another virtual node. You can specify which flow classes a node can respond to and with what flow it responds with.

For example, Alice is a participant on the network and wishes to agree a ledger update with Bob, another network participant. To communicate with Bob:

1. Alice starts a flow that Bob is registered to respond to.
2. Alice sends Bob a message within the context of that flow.
3. Bob starts its registered counterparty flow.

Now that a connection is established, Alice and Bob can communicate to agree a ledger update by passing a series of messages back and forth, as defined by the flow steps.

### Subflows
Flows can be composed by starting a flow as a subprocess in the context of another flow. The flow that is started as a subprocess is known as a subflow. The parent flow waits until the subflow returns.

## Flow Library
Corda provides a library of flows to handle common tasks. As a result, you do not have to redefine the logic behind common processes such as:
* Notarizing and recording a transaction.
* Gathering signatures from counterparty nodes.
* Verifying a chain of transactions.
Rather than exposing a library of subflows, this functionality is invoked via the `UtxoLedgerService` class. For example, calling the `finalize()` method invokes a subflow under the hood.

## Concurrency
Virtual nodes can have multiple active flows running at once. Flows are serialized to the message bus whenever they enter a blocking state. For example, when waiting on I/O or a networking call. This allows flows to be active for long periods of time, even during interruptions such as node restarts and upgrades. Instead of waiting for the flow to become unblocked, the node immediately starts work on any other scheduled flows, returning to the original flow at a later date. A flow will suspend whenever it needs to perform an operation using platform APIs. Flows can survive a failover event, allowing them to migrate to another flow worker process if required.