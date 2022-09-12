---
date: '2020-07-15T12:00:00Z'
title: "Key concepts"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-intro
    identifier: corda-5-dev-preview-key-concepts
    weight: 2000
section_menu: corda-5-dev-preview
---
## Layered architecture

The Corda platform is a layered toolbox that you can approach from the bottom up, pulling in more advanced concepts only when needed. There are currently three distinct layers:
1.	[P2P layer](#p2p-Layer)
2.	[Flow layer](#flow-Layer)
3.	[Ledger layer](#ledger-Layer)

*Diagram?*

### P2P layer

The P2P layer allows an identity to establish a session with another identity on an [application network](#application-networks)at their published address, regardless of whether they reside in the same or different clusters.
It manages the lifecycle, link establishment, connection recovery, back pressure, caching, heart beating, transmission, message chunking, etc for communications intended to flow between identities.

{{< note >}}
The P2P layer is not officially exposed to CorDapp Developers to access natively in this Developer Preview of Corda 5 and so its implementation in CorDapps is not currently supported.
Support will be available in a future release as there is great value in an end-to-end authenticated messaging system that can multiplex thousands of messages whilst remaining HA and secure and also embodying a strong identity model.
{{< /note >}}
<!--

*Note about what's available in DP 2 (nothing?) and what's coming soon - layer cake architecture means p2p layer could be used independently - no flow network*
-->

### Flow layer

The flow layer builds on top of the P2P layer. It expands the capabilities it expresses with [flows](#flows).
Flows allow Developers to encapsulate complex business logic that orchestrates actions by multiple parties into simple, linear code.
Under the hood, Corda takes that simple code and breaks it into asynchronous messages executed across the network with responses flowing to where they should.
This is transparent to Developers.

If Alice needs to talk to Bob and have Bob get Charlie to agree and send that to Claire, this is the layer to embrace.
It is about the orchestration of events, passing information that requires agreeing, viewing, and actioning.
CorDapps can drive third party systems here and respond to incoming events.

The flow layer is accessed through a series of APIs that allow for the creation of flows.
This is where the business problem is solved and the majority of code is written.
This is the code that is built, packaged, distributed, installed, and executed.

### Ledger layer

The ledger layer addresses business problems that require some form of distributed ledger.
This layer solves problems where orchestrating parties must verify something is true without trusting one another.
The layer is itself pluggable, enabling you to select different models of ledgers as needed.
When the lifecycle of data continues beyond the parties first interacting with it, the ledger layer allows its evolution without the input of the creating party.
Ledger code adds the ability to cryptographically verify proposed changes to data such that no parties can repudiate they agreed.
Future versions will contain the following ledger models:
*	[Consensual ](#consensual )
*	[UTXO](#UTXO)

#### Consensual
<<< Ask @Christian Sailer >>>
#### UTXO
<<< Ask @Christian Sailer >>>

{{< note >}}
The ledger layer is not available in this Developer Preview of Corda 5.
{{< /note >}}

## CorDapps
Similar to operating systems, Corda, and DLT in general, is valuable to Developers who they enable but require applications to be useful to users.
Distributed applications (Dapps) deployed on Corda are known as **CorDapps**.
CorDapps encapsulate the logic that brings parties into agreement through [flows](#flows).
The set of all possible entities granted permission by the [MGM](#mgm) to use a CorDapp is known as an [application network](#application-networks).
CorDapps are built as a layered [package](#packaging).

## Application networks

Corda is a permissioned blockchain and to use a [CorDapp](#cordapps) users must be approved and their identity tested to a set of rules. Corda does not care what those rules are.
Rules can be as lax as allowing anyone to join who asks or as strict as requiring a full KYC process.
Corda facilitates these rules through the [Membership Group Manager (MGM)](#mgm).

It is up to a network operator to determine their needs and requirements.
Participants joining a network are agreeing to the rules of the network and understand that all other participants were vetted to the same level.
The set of all possible entities onboarded according to the rules of the network is referred to as the **application network**.
This is all of the possible users permitted to use an application.
For the operator of an application, it is their complete list of customers.
From the perspective of one of those customers, it is who they are allowed to interact with.

*Diagram?*

## Membership management

The **Membership Group Manager (MGM)** enables network operators to set the rules for their [application network](#application-networks), approves or declines new members, and distributes membership lists to the other members.
The MGM is a CorDapp which runs as a virtual node, allowing you to create/operate many application networks using the same Corda deployment.

Entities permitted to join an application network are represented by a public/private keypair optionally attested by a certificate authority as belonging to an X500 identity.
The application network operator sets the rules in the CPI as to which certificate authority it trusts to attest that an identity matches. The operator can run any additional checks they wish.
The keypair is used to sign things within the context of the application by the identity, attesting that it agrees to what is being proposed.

{{< note >}}
Currently, the MGM allows each network member to be aware of every other member. However, this is a result of development time and interest from the community, not a “hard rule” for application networks.
{{< /note >}}

## Virtual nodes

Corda 5 virtualizes the execution of [flow](#flows) process steps, allowing flows for multiple identities and from multiple CorDapps to be executed within the same compute environment at the same time.

Virtual nodes reduce the overhead of each identity on an [application network](#networks).
At the time of onboarding, the overhead of an identity relates only to the load it brings to the system rather than incurring a cost for simply existing.
The overhead of keeping onboarded identities available to transact with other members is not fixed and identities are transient, only active when actually required.

A **virtual node** is the combination of the context of an identity and the temporary compute instances created to execute [flows](#flows) on behalf of that identity.
An instance of a virtual node is created for long enough to handle the execution steps needed and then allowed to dematerialize.
{{< figure src="images/virtual-node.png" figcaption="Virtual node interaction" alt="Virtual node" >}}
At any point in time, many instances of a virtual node may be executing. The number limited to the availability of [flow workers](#workers), with an additional number of flows inflight with other virtual node instances suspended in a checkpoint store.

This is achieved by a state machine that enables each node to schedule various operations for each step of a flow.
{{< figure src="images/state-machines.png" figcaption="State machines executing flows for multiple identities" alt="State machine" >}}

This enables Corda to run multiple flows at once, scheduling tasks for different flows as required, very much like a traditional scheduler in an operating system.
{{< figure src="images/state-machine-checkpointed.png" width="75%" figcaption="State machine executing checkpointed flows" alt="Virtual node" >}}
As shown, the flow framework acts as a distributed state machine designed to schedule the different steps. Flows are checkpointed at any stage where they would suspend. That checkpoint is persisted for potential recovery of the flow and the next flow is scheduled for execution from the point it was previously suspended.

## Sandboxes

**Sandboxes** are an essential part of the high-availability (HA) and multi-tenant architecture of Corda 5, ensuring stability and security.
Sandboxes are the foundation that virtual nodes run on, keeping contracts, workflows, and libraries separate from other code. Each [virtual node](#virtual-nodes) runs on top of one or more sandboxes.
Isolating CorDapp classes and dependencies in this way also isolates them from the Corda host process. Since Corda itself is executing third-party code, that execution environment needs sandboxing from the host, Corda, to prevent the CorDapp from having access to system-level permissions and privileges. CorDapps do not share libraries with Corda itself and therefore can use their own version of 3rd party dependencies, for example.
Sandboxes provide the ability to install and upgrade CorDapps without impacting other CorDapps operating in the same Corda instance. You can upgrade CorDapps without the need to stop existing flows or the host process and potentially load multiple versions of a particular CorDapp or library.

The code encapsulated within a [CorDapp](#cordapps) is executed by the [workers](#workers) in a [Corda Cluster](#corda-clusters). The majority of the time, this is the flows within the compiled [CPK](#cordapp-packages-cpks) on behalf of a specific user. Since Corda itself is executing third-party code, that execution environment needs sandboxing from the host, Corda, to prevent the CorDapp from having access to system-level permissions and privileges. Much like processes in a modern operating system, they are run on behalf of an identity, and they cannot access the information they shouldn’t.

Sandboxes, whilst crucial to the execution of Corda, are a concept that the majority of CorDapp developers never need to concern themselves with. The guarantee made by the platform is that when executed, CorDapp code will not allow the user running it access to any part of the system it should not.

## Flows

As described in the [flow layer](#flow-layer) section of the [architecture overview](#architecture), **flows** are the mechanism through which a [CorDapp](#cordapps) encapsulates the logic of its application that brings parties into agreement over something.
This logic is written in a sequential manner, allowing developers to focus on the logic itself rather than the integration of the logic into an asynchronous event-based system.

Flows utilize the Corda API to perform the required actions to solve a business problem, such as:
* Sending X to Alice and checking their response and doing something with it.
* Proposing an update to something and getting agreement from all parties.
* When event Y occurs, do Z.

*cross-ref to flow API section*

## Workers

An instance of Corda is composed of a number of processes executing in parallel to perform all of the required operations.
This includes responding to RPC requests, running CorDapps, accessing cryptographic material, etc.
These processes are hosted by Corda **workers**. The exact division of processes to workers is determined by the requirements of the running instance. Simpler instances may co-locate many processes into a single worker sacrificing finer-grained control and scaling for simplicity of management.

Workers are optimally hosted in a Kubernetes environment.
This enables a Corda operator to leverage the innate capabilities of K8s for automatic scaling and failover of the workers deployed into it.
It is through this scaling that Corda achieves its HA guarantees.

## Packaging

Just like a regular application, your [CorDapp](#cordapps) must be packaged for distribution and installation. Corda takes a three-layered model to its packaging design to allow maximum reusability and portability:
1. [Corda Package (CPK)](#cordapp-packages-cpks) — represents a single code-entity authored by a CorDapp developer.
2. [Corda Package Bundle (CPB)](#cordapp-package-bundles-cpbs) — built using a collection of CPKs, which represents a full application.
3. [Corda Package Installer (CPI)](#cordapp-package-installer-cpi) — contains the CPB and information about the network.

## CorDapp Packages (CPKs)
CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application.
Under the hood, each CPK runs in its own [sandbox](#sandboxes), isolated from other CPKs.

## CorDapp Package Bundles (CPBs)
CPBs are complete applications minus the “run time information” needed to onboard entities into it.
CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an [application network](#application-networks).

## CorDapp Package Installer (CPI)
Corda is only useful when many entities are using a CorDapp to transact.
The set of entities that can use an application is called an application network.
These have rules and other meta information beyond the simple code in the CPKs.
CPIs contain the CPB and all of the information required to join and participate in an application network.

For example, consider a currency CPB that cannot become a currency network until rules are put in place. Membership onboarding is decided on and the currency symbol set. CPIs add this meta information to the CPB to allow for easy distribution and onboarding of identities.

The only difference between a development CPI and a production CPI is the network information. Both environments deploy the same CPB but that CPB will be wrapped into a different CPI for installation and setup.

## Clusters

A **Corda cluster** is the term for the set of all workers deployed into a Kubernetes environment. A cluster is a distinct entity from the (partial) network(s) it hosts. It is the hardware, the databases, and HSMs. A cluster is operated and maintained to ensure that the software, Corda, executing within it is performant and responsive.

A single cluster can encapsulate the entirety of an application network or just a part. It can host identities for many networks or just a single one. It can even host applications of a single identity. The architecture depends on the use case executed. If the members of an application network are mature enough to host their own code, to truly be decentralised, then their identity, their [virtual node](#virtual-nodes), will be executed within their own cluster and other identities may be on a cluster managed by a third party. The [application network](#application-networks) emerges above all of this.

*Note about what's available in DP 2 (no cloud deployments, no multi-cluster) and what's coming soon*
*Cross-ref to local Kubernetes depolyment*
