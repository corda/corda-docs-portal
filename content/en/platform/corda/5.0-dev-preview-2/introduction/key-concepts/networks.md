---
date: '2020-07-15T12:00:00Z'
title: "Application networks"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 4000
section_menu: corda-5-dev-preview
---

Networks in Corda 5 are application networks, where all participants are running the same CorDapp. Network registration and member distribution is handled by the [Membership Group Manager (MGM)](../mgm/overview.html). Application networks embrace the reality that regulated markets have strong privacy and governance requirements, reducing the scope of each network to a single bundle of applications all governed by the same rules.

##	Clusters

 Clusters allow members on multiple networks thanks to multi-tenancy support. Corda 5 supports multiple [Corda identities](#corda-identities) operating in the same cluster via [virtual nodes](#virtual-nodes). A virtual node is linked to a CPI and acts as a single member in a network once registration has been completed. A cluster allocates resources on a per-virtual node basis and ensures that code executing in the context of a particular virtual node is sandboxed away from other virtual nodes and platform code.

 *Note about what's available in DP 2 (no cloud deployments, no multi-cluster) and what's coming soon*

## Virtual nodes

A virtual node represents a [Corda identity](#corda-identities) and contains everything needed to communicate and transact on Corda: keys, certificates, and storage. This enables the identity to join application networks, where they can interact with other group members according to the terms set by the [Membership Group Manager (MGM)](../mgm/overview.html). Identities can join multiple application networks from one physical node infrastructure using virtual nodes.

Virtual nodes can be:
* **Multi-tenant.** You can host multiple virtual nodes on one deployment of Corda, at no additional cost.
* **Portable.** You can move a virtual node from one host to another.
* **Highly-available.** If you configure your node to be highly available, if it goes down, an identical one takes its place instantly.

 You can think of a virtual node as an environment that enables the processor to locate a specific [CPI](#cordapp-package-installer-cpi) file. The flows associated with the CPI let the virtual node communicate with others. You can read more about virtual nodes [here](../getting-started/architecture/virtualnodes.html).

## Sandboxes

Sandboxes are security mechanisms for separating running programs. They are the foundation that [virtual nodes](#virtual-nodes) run on, keeping contracts, workflows, and libraries separate from other code. The contents of these sandboxes are packaged up and shared for deployment by creating a [CPI file](#cordapp-package-installer-CPI). You can read more about sandboxes [here](../getting-started/architecture/workers.html).

## Workers

You can think of a worker as something you call and assign a task. The worker takes the task away to work on it, then calls you back when the task is complete. Some workers might pass parts of a task you give them to other specialized workers. You can call multiple workers to complete different tasks based on your needs at a given moment. Workers increase their capacity when they have a lot to do and scale back when they can. This property makes your Corda deployment resilient and scalable — you can add more workers if you need them, and add replicas of specific workers in case one fails. You can read more about workers [here](../getting-started/architecture/workers.html).

##	Flows

Corda networks use point-to-point messaging instead of a global broadcast. Coordinating an update requires network participants to specify exactly what information needs to be sent, to which counterparties, and in what order. Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a node how to achieve a specific task, such as issuing an asset or settling a trade. Once a given business process has been encapsulated in a flow and installed on a node as part of a CorDapp, a member of the network can instruct the node to kick off this business process at any time via their node. You can read more about flows [here](../flows/overview.html).

##	Distributed ledgers

...(consensual states/ UTXO)*..

*Note about what's available in DP 2 (nothing?) and what's coming soon - need to be clear what consensual ledge is not! (Sean working on blog post)*

##	Notary

...

*Note about what's available in DP 2 (nothing?) and what's coming soon*

##	P2P (peer-to-peer) framework

The P2P layer enables [identities](corda-identities) to exchange messages with each other regardless of whether they reside in the same or different clusters.

*Note about what's available in DP 2 (nothing?) and what's coming soon - layer cake architecture means p2p layer could be used independently - no flow network*
