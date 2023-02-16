---
date: '2020-07-15T12:00:00Z'
title: "Key Concepts"
menu:
  corda-5-beta:
    parent: corda-5-beta-intro
    identifier: corda-5-beta-key-concepts
    weight: 2000
section_menu: corda-5-beta
---
## Layered Architecture

The Corda platform is a layered toolbox that you can approach from the bottom up, pulling in more advanced concepts only when needed. There are currently three distinct layers:
1.	[P2P layer](#p2p-layer)
2.	[Flow layer](#flow-layer)
3.	[Ledger layer](#ledger-layer)

{{< figure src="images/layered-architecture.png" figcaption="Corda 5 architecture" alt="Layered architecture of Corda 5" >}}

### P2P Layer

The P2P Layer allows an identity to establish a communication session with another identity on an [application network](#application-networks) at their published address, regardless of whether they reside in the same or different [clusters](#clusters).
It manages the lifecycle, link establishment, connection recovery, back pressure, caching, heart beating, transmission, message chunking, etc., for communications intended to flow between identities. It has two primary components; the Gateway and Link Manager.

### Flow Layer

The Flow Layer expands the capabilities of the P2P Layer with the introduction of the flow framework.
[Flows](#flows) allow Developers to encapsulate complex business logic that orchestrates actions by multiple parties into simple, linear code.
Corda takes that simple code and breaks it into asynchronous messages executed across the network with responses flowing to where they should.
This is transparent to Developers.

For example, if Alice needs to talk to Bob and have Bob seek Charlie's agreement, before sending the agreed proposal to Claire, the Flow Layer is required.
It is about the orchestration of events, passing information that requires agreeing, viewing, and actioning.
This layer integrates with the system of record and triggers events.
CorDapps can drive third-party systems here and respond to incoming events.

The Flow Layer is accessed through a series of APIs that allow for the creation of flows.
This is where the business problem is solved and the majority of code is written.
This is the code that is built, packaged, distributed, installed, and executed.

### Ledger Layer

The [Ledger](../developing/ledger/ledger.html) Layer addresses business problems that require some form of distributed ledger.
This layer solves problems where orchestrating parties must verify that something is true without trusting one another.
The layer is itself pluggable, enabling you to select different ledger models as needed.
When the lifecycle of data continues beyond the parties' first interaction with it, the Ledger Layer allows its evolution without the input of the creating party.
Ledger code adds the ability to cryptographically verify proposed changes to data such that no parties can repudiate what was agreed.
Corda 5 contains the following ledger models:
*	Consensual
*	UTXO (unspent transaction output)

## CorDapps
Similar to operating systems, Corda, and DLT in general, is valuable to Developers who they enable but require applications to be useful to users.
Distributed applications (Dapps) deployed on Corda are known as **CorDapps**.
CorDapps encapsulate the logic that brings parties into agreement through [flows](#flows).
The set of all possible entities granted permission by the [Membership Group Manager (MGM)](#membership-management) to use a CorDapp is known as an [application network](#application-networks).
CorDapps are built as a layered [package](#packaging).

## Application Networks

Corda is a permissioned digital ledger platform and to use a [CorDapp](#cordapps), entities must be approved and their identity verified against a set of rules.
Corda does not care what those rules are.
Rules can be as lax as allowing anyone to join who asks or as strict as requiring a full KYC process.
Corda facilitates these rules through the [Membership Group Manager (MGM)](#membership-management).

It is up to a network operator to determine their needs and requirements.
Participants joining a network are agreeing to the rules of the network and understand that all other participants were vetted to the same level.
The set of all possible entities onboarded according to the rules of the network is referred to as the **application network**.
It is the sum of all members and the states that they have created and transacted between them.
This is all of the possible users permitted to use an application.
For the operator of an application, it is their complete list of customers.
From the perspective of one of those customers, it is who they are allowed to interact with.

You can learn more about networks in [Network Types](../deploying/network-types.html).

## Membership Management

### Members

*Members* are identified by a holding ID, which is a combination of a network group ID (or the hash thereof) and an X.500 name. The X.500 name must be unique within a single network.
Corda creates the holding ID when a [virtual node](#virtual-nodes) for a member is created on a cluster that has the CPI for the desired network installed.

After creation of the virtual node, the member must be registered with the [Membership Group Manager (MGM)](#mgm). Only after registration with the MGM will the member:

* have a valid public/private ledger key pair to sign transactions and identify themselves as participants.
* be visible to other members for interactions.
* be able to use flow session to communicate to other members.

### MGM

The **MGM** enables network operators to set the rules for their [application network](#application-networks).
It approves or declines new members and distributes membership lists to members. Lists are signed and verifiable to prevent tampering, ensuring [virtual nodes](#virtual-nodes) can trust each other.
The MGM is a CorDapp which runs as a virtual node, allowing you to create and operate many application networks using the same Corda deployment.

Entities permitted to join an application network are represented by a public/private keypair, optionally attested by a certificate authority as belonging to an X.500 identity.
The application network operator sets the rules in the [CPI](#corda-package-installer-cpi) as to which certificate authority it trusts to attest that an identity matches.
The operator can run any additional checks they wish.
The keypair is used to sign things within the context of the application by the identity, attesting that it agrees to what is being proposed.

{{< note >}}
Currently, the MGM allows each network member to be aware of every other member.
However, based on feedback, we could introduce additional models. For example, a broker model where each client is only aware of the brokers, but the brokers are aware of every other node.
{{< /note >}}

You can learn more about configuring an MGM in [Onboarding the MGM](../operating/operating-tutorials/onboarding/mgm-onboarding.html).

## Virtual Nodes

Corda 5 virtualizes the execution of [flow](#flows) process steps, allowing flows for multiple identities and from multiple CorDapps to be executed within the same compute environment at the same time.

Virtual nodes reduce the overhead of each identity on an [application network](#application-networks).
At the time of onboarding, the overhead of an identity relates only to the load it brings to the system rather than incurring a cost for simply existing.
The overhead of keeping onboarded identities available to transact with other members is not fixed and identities are transient, only active when actually required.

A **virtual node** is the combination of the context of an identity and the temporary compute instances created to execute [flows](#flows) on behalf of that identity.
An instance of a virtual node is created for long enough to handle the required execution steps and then allowed to dematerialize. It is identified by the short hash of the member’s holding ID. It consists of all of the required configuration to create the various sandboxes that are required to run the virtual node’s code on the workers of the cluster, plus database tables, and cryptographic keys so that the virtual node can store data and sign and verify transactions.
{{< figure src="images/virtual-node.png" figcaption="Virtual node interaction" alt="Virtual node" >}}
At any point in time, many instances of a virtual node may be executing, limited only by the availability of [flow workers](#workers). An additional number of flows may be inflight with other virtual node instances suspended in a checkpoint store.

This is achieved by a state machine that enables each node to schedule various operations for each step of a flow.
{{< figure src="images/state-machines.png" figcaption="State machines executing flows for multiple identities" alt="State machine" >}}

This enables Corda to run multiple flows at once, scheduling tasks for different flows as required, very much like a traditional scheduler in an operating system.
{{< figure src="images/state-machine-checkpointed.png" width="75%" figcaption="State machine executing checkpointed flows" alt="Virtual node" >}}
As shown, the flow framework acts as a distributed state machine designed to schedule the different steps. Flows are checkpointed at any stage where they would suspend. That checkpoint is persisted for potential recovery of the flow and the next flow is scheduled for execution from the point it was previously suspended.

## Sandboxes

**Sandboxes** are an essential part of the high-availability (HA) and multi-tenant architecture of Corda 5, ensuring stability and security.
Sandboxes are the foundation that virtual nodes run on, keeping contracts, workflows, and libraries separate from other code. Each [virtual node](#virtual-nodes) runs on top of one or more sandboxes.

The code encapsulated within a [CorDapp](#cordapps) is executed by the [workers](#workers) in a [Corda Cluster](#clusters).
The majority of the time, this is the [flows](#flows) within the compiled [CPK](#corda-packages-cpks) on behalf of a specific user.
Since Corda itself is executing third-party code, CorDapp execution environments must be sandboxed from the host, Corda, to prevent the CorDapp from having access to system-level permissions and privileges.
Much like processes in a modern operating system, workers are run on behalf of an identity, with only the appropriate information accessible.

Sandboxes, whilst crucial to the execution of Corda, are a concept that the majority of CorDapp developers never need to concern themselves with. The guarantee made by the platform is that when executed, CorDapp code will not allow the user running it access to any part of the system it should not.

## Flows

As described in the [Flow Layer](#flow-layer) section of the [architecture overview](#layered-architecture), **flows** are the mechanism through which a [CorDapp](#cordapps) encapsulates the logic of its application that brings parties into agreement.
This logic is written in a sequential manner, allowing developers to focus on the logic itself rather than the integration of the logic into an asynchronous event-based system.

Flows utilize the Corda API to perform the required actions to solve a business problem, such as:
* Sending X to Alice and checking their response and doing something with it.
* Proposing an update to something and getting agreement from all parties.
* When event Y occurs, do Z.

For more information about the flows API, see [Corda API](../developing/api/application/application.html#flows).

## Workers

An instance of Corda is composed of a number of processes executing in parallel to perform all of the required operations.
This includes responding to RPC requests, running CorDapps, accessing cryptographic material, etc.
These processes are hosted by Corda **workers**. The exact division of processes to workers is determined by the requirements of the running instance. Simpler instances may co-locate many processes into a single worker sacrificing finer-grained control and scaling for simplicity of management.

Workers are optimally hosted in a Kubernetes environment.
This enables a Corda operator to leverage the innate capabilities of K8s for automatic scaling and failover of the workers deployed into it.
It is through this scaling that Corda achieves its HA guarantees.

## Packaging

Just like a regular application, your [CorDapp](#cordapps) must be packaged for distribution and installation. Corda takes a three-layered model to its packaging design to allow maximum reusability and portability:
1. [Corda Package (CPK)](#corda-packages-cpks) — represents a single code-entity authored by a CorDapp developer.
2. [Corda Package Bundle (CPB)](#corda-package-bundles-cpbs) — built using a collection of CPKs, which represents a full application.
3. [Corda Package Installer (CPI)](#corda-package-installer-cpi) — contains the CPB and information about the network.

{{< figure src="images/cordapp-packaging.png" figcaption="CorDapp Packaging" >}}

You can read how to package your CorDapp in the [Development Tutorials](../developing/development-tutorials/cordapp-packaging.html).

### Corda Packages (CPKs)
CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application.
Corda runs each CPK runs in its own [sandbox](#sandboxes), isolated from other CPKs.

### Corda Package Bundles (CPBs)
CPBs are complete applications minus the “run time information” needed to onboard entities into it.
CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an [application network](#application-networks).

### Corda Package Installer (CPI)
Corda is only useful when many entities are using a CorDapp to transact.
The set of entities that can use an application is called an [application network](#application-networks).
These have rules and other meta information beyond the simple code in the CPKs.
CPIs contain the CPB and all of the information required to join and participate in an application network.

For example, consider a currency CPB that cannot become a currency network until rules are put in place. Membership onboarding is decided on and the currency symbol set. CPIs add this meta information to the CPB to allow for easy distribution and onboarding of identities.

The only difference between a development CPI and a production CPI is the network information. Both environments deploy the same CPB but that CPB will be wrapped into a different CPI for installation and setup.

## Clusters

A **Corda cluster** is the term for the set of all workers deployed into a Kubernetes environment. A cluster is a distinct entity from the (partial) network(s) it hosts. It is the hardware, the databases, and HSMs. A cluster is operated and maintained to ensure that the software, Corda, executing within it is performant and responsive.

A single cluster can encapsulate the entirety of an application network or just a part. It can host identities for many networks or just a single one. It can even host applications of a single identity. The architecture depends on the use case executed. If the members of an application network are mature enough to host their own code, to truly be decentralised, then their identity, their [virtual node](#virtual-nodes), will be executed within their own cluster and other identities may be on a cluster managed by a third party. The [application network](#application-networks) emerges above all of this.
