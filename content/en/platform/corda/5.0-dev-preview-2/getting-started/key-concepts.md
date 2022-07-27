---
date: '2020-07-15T12:00:00Z'
title: "Key concepts"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-gettingstarted
    weight: 3000
section_menu: corda-5-dev-preview
---

 ["Key concepts" should give a brief overview - a paragraph or two should generally suffice. If you find yourself writing more, consider if the content needs it's own concept section.]: #

## Packaging

CorDapps are built as a layered package. At the lowest level, a [Corda Package (CPK)](#cordapp-packages-cpks) represents a single code-entity authored by a CorDapp developer. For example, a library of flows to perform some task. A [Corda Package Bundle (CPB)](#cordapp-package-bundles-cpbs) is built using a collection of these packages, which represents a full application. Finally, information about the network can be added to a CPB to create a [Corda Package Installer (CPI)](#cordapp-package-installer-cpi) file. When this is installed into the system, the cluster knows that any entity using this file must join the specified network, and so can handle network onboarding accordingly.

### CorDapp Packages (CPKs)
The building blocks of CorDapps are a new file format called CorDapp Packages (.`cpk`s). This includes workflow and contract packages, additional metadata, a dependency tree, and version information. You can independently version `.cpk`s. Each .`cpk` runs in its own [sandbox](#sandboxes), isolated from other CPKs. This prevents dependency clashes and facilitates faster CorDapp development.

### CorDapp Package Bundles (CPBs)
The application publisher brings individual `.cpk` files together to make a single CorDapp Package Bundle (`.cpb`). The application publisher is a single entity that coordinates multiple parties to create a single application bundle for a network. When multiple firms compose CorDapps together, it creates a strong technical dependency that facilitates development, distribution, and upgrades.

### CorDapp Package Installer (CPI)
CorDapps are packaged in a single `.jar` file called a CorDapp Package Installer (CPI) containing all the pieces required to join and participate in an application network:
* The location of the network operator.
* A list of membership requirements.
* Third party dependencies.
* CorDapp logic.

The only difference between a development and a production CPI is the network information, so you can use the same software for testing environments.

## Identities

A Corda identity is any person or business that wants to interact with other people or businesses using Corda.

##	Application networks

Networks in Corda 5 are application networks, where all participants are running the same CorDapp. Network registration and member distribution is handled by the [Membership Group Manager (MGM)](../mgm/overview.html).

##	Clusters

 Clusters support members on multiple networks thanks to multi-tenancy support. Corda 5 supports multiple [Corda identities](#corda-identities) operating in the same cluster via [virtual nodes](#virtual-nodes). A virtual node is linked to a CPI and acts as a single member in a network once registration has been completed. A cluster allocates resources on a per-virtual node basis and ensures that code executing in the context of a particular virtual node is sandboxed away from other virtual nodes and platform code.

 *Note about what's available in DP 2 and what's coming soon*

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

You can think of a worker as something you call and assign a task. The worker takes the task away to work on it, then calls you back when the task is complete. Some workers might pass parts of a task you give them to other specialized workers. You can call multiple workers to complete different tasks based on your needs at a given moment. Workers increase their capacity when they have a lot to do and scale back when they don't. This property makes your Corda deployment resilient and scalable — you can add more workers if you need them, and add replicas of specific workers in case one fails. You can read more about workers [here](../getting-started/architecture/workers.html).

##	Flows

Corda networks use point-to-point messaging instead of a global broadcast. Coordinating an update requires network participants to specify exactly what information needs to be sent, to which counterparties, and in what order. Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a node how to achieve a specific task, such as issuing an asset or settling a trade. Once a given business process has been encapsulated in a flow and installed on a node as part of a CorDapp, a member of the network can instruct the node to kick off this business process at any time via their node. You can read more about flows [here](../flows/overview.html).

##	Distributed ledgers

...(consensual states/ UTXO)*..
*Note about what's available in DP 2 and what's coming soon*

##	P2P (peer-to-peer) framework

The P2P layer enables [identities](corda-identities) to exchange messages with each other regardless of whether they reside in the same or different clusters.
*Note about what's available in DP 2 and what's coming soon*
