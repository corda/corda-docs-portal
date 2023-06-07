---
title: "CorDapps"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-fundamentals-cordapps
    parent: corda5-fundamentals
    weight: 1000
section_menu: corda5
---

# CorDapps

A CorDapp is a Java (or any JVM targeting language) application built using the Corda build toolchain and APIs to solve a problem best solved using a decentralized approach. CorDapps are assembled as one or more JAR files bundled into the CorDapp packaging format. That file is then uploaded to Corda where it is executed, Corda acting as the application host for the CorDapp. Corda itself is running on a JVM usually hosted within a container framework.

{{< 
  figure
	 src="cordapp.png"
   width="50%"
	 figcaption="CorDapp Architecture"
>}}

CorDapps are composed of two layers:
* Orchestration layer
* Consensus layer

{{< 
  figure
	 src="cordapp-layers.png"
   width="50%"
	 figcaption="CorDapp Layers"
>}}

The first view, A, shows our CorDapp as a single entity. It interacts with Corda through the API at a programmatic level and with the hosting infrastructure when executing. Secondly, it interoperates with itself when other instances of it communicate and also with external systems where it is integrated into existing business processes and software.

Our second view, B, drills into this picture to highlight the two layers and how they interoperate with other aspects of a Corda deployment.

## Orchestration Layer — Flows

One of Corda’s distinguishing features is enabling permissioned identities within a context to communicate with one another without the need to modify the global state. The Orchestration layer of a CorDapp is essentially where this logic is written in the form of Corda flows. 

Flows in Corda are discrete pieces of business logic grouped together. Due to Corda’s distributed nature, it is not enough to simply “write a function” to encapsulate functionality, as that functionality almost certainly requires bringing together multiple parties. This means code will potentially be executed in as many locations as there are parties involved.

At the highest level, you can think of a flow as a linear set of instructions executed to some endpoint:

{{< 
  figure
	 src="flow.png"
   width="50%"
	 figcaption="A Flow"
>}}

A flow is generally created as two companion functions — an initiator and a responder. These model the two halves of a multi-party function call where the flow of logic is handed off for someone else to work on before returning some information and the flow continues:

{{< 
  figure
	 src="flow-parties.png"
   width="50%"
	 figcaption="A flow — an initiator and a responder"
>}}

In Corda, several parties can be involved in the execution of a flow:

{{< 
  figure
	 src="flow-multiple-parties.png"
   width="50%"
	 figcaption="Multiple parties to a flow"
>}}

The power of the Corda programming model is that it enables CorDapp Developers to write flows as seemingly synchronous singleton functions, whilst the hosting compute infrastructure actually breaks that user code up into many different chunks of work that can be distributed around the system as needed, much like a standard operating system grants access to physical compute resources.

{{< 
  figure
	 src="flow-chunks.png"
   width="50%"
	 figcaption="Chunks of work in a flow"
>}}

Whilst the general case for flows within a CorDapp is the orchestration of a global state change, they are also the primary mechanism by which behaviors can be invoked by users through external interaction via a REST service.

{{< 
  figure
	 src="flows-rest.png"
   width="50%"
	 figcaption="Flows invoked via the REST service"
>}}

Flows that only exist within a single identity’s context and do not need to communicate with another identity are equally permissible. 

## Consensus Layer

The defining aspect of a decentralized application is the ability for untrusting parties to reach an agreement about a modification to the global record of truth and, once that modification is applied, forever agree that it did indeed happen.

The orchestration layer has full, queryable access to the information contained within the consensus layer through the Corda CorDapp API. 

The mechanism for achieving consensus in Corda is pluggable. For example, Corda 5 allows for a UTXO model with notary double-spend protection. However, common across all models is once the orchestration layer has negotiated a potential change amongst peers, and that change is determined to be valid, it is applied to the global state.

### Decentralized Control

In a decentralized system, there is no single point of access to the global state. When untrusting parties reach a consensus, that is done in parallel by disparate parties with no implied ordering.

{{< 
  figure
	 src="centralized-decentralized.png"
   width="50%"
	 figcaption="Centralized versus Decentralized Agreement"
>}}

In a centralized system, how can an entity trust the global state when it has no direct say in all of the mutations applied?

{{< 
  figure
	 src="trust.png"
   width="50%"
	 figcaption="Issue of trust in Centralized Agreements"
>}}

Ultimately, each member of the network must be able to attest to the validity of all historic modifications so as to trust the current global state is, by inference, also valid.

### Validity and Smart Contracts

The validity of a proposal is evaluated within a decentralized system through a set of rules that each proposal must meet in order to be considered valid. Generally, this collection of rules is referred to as a smart contract and each proposed update will be governed by it.

Smart contracts can have different levels of granularity (network-wide or individual data representations) but the same general principles hold true that a proposal is only valid when the smart contract says it is. Rules in Corda can be arbitrary; however, there is a strong requirement that validity controls are deterministic as once evaluated as valid, checks on a change in the future must always return that it is valid. This means smart contracts can only reason about data present within the system of record: anything outside that generally leads to non-deterministic results as their presence cannot be guaranteed. 

{{< 
  figure
	 src="proposal-rules.png"
   width="50%"
	 figcaption="Validity of Proposals"
>}}

It is the responsibility of every party to a proposal to check that it is valid. This is a trustless environment where it is possible for a counterparty to submit a proposal that is not valid by the rules. Accepting an invalid update could have a number of consequences, including financial and reputational.

Execution and enforcement of these rules are determined by the underlying model chosen for the system of record. Public blockchains and cryptocurrency networks use different validation and consensus mechanisms than the Corda UTXO ledger, yet the underlying principle of allowing untrusting entities to propose updates and have them accepted into the global record as long as they conform to the rules and are agreed to the parties is true across all decentralized systems.

### Affirmative Consent

In parallel to the concept of validity, Corda also addresses the concept of affirmation. That is, the ability for an entity to signify, irrefutably to all, that it consents to a proposal in some capacity (for example, as a benefactor or observer). 

This is acheived through a cryptographic signature on a hash of the proposal. A set of signatures by all involved parties is sufficient to indicate that all agree that the update should take place. In conjunction with the execution of the validity rules, Corda can ensure the global state is only changed in ways that are valid and trustable by all.

For example, a simple IOU is issued from Alice to Bob, indicating that Alice owes Bob $100. The application network validates such a proposal with a set or rules, such as the IOU must have a borrower and a lender. This is the concept of validity, not morality or sensibility. In other words, although the rules might stop you from issuing an IOU without a lender, it will not prevent you issuing an IOU with an exceedingly large interest rate. This is where affirmative consent comes into play. Affirmative consent is represented by Bob signing the IOU proposal created and signed by Alice, to indicate that he agrees to the terms of the individual IOU proposal itself, such as interest rates, punishment for late payments, and so on. These two concepts in tandem are used to assure that the application network rules are not broken and that the involved parties agree to the proposal in a trustless environment.

## Identity Integration

This documentation references multiple parties several times in explaining the fundamental tenets of Corda and other decentralized platforms. This means Corda must internalize the concept that CorDapps are only ever operated as an aspect of an entity referred to as an identity.  

{{< 
  figure
	 src="identity-integration.png"
   width="50%"
	 figcaption="Identity Integration"
>}}

An instance of a CorDapp must always have an associated identity in Corda. A flow runs on behalf of an identity and communicates with another identity selected from the pool of possible candidates which responds in kind.

{{< 
  figure
	 src="identities.png"
   width="50%"
	 figcaption="Communicating Identities"
>}}

As identities communicate with one another, the global state is changed through the acceptance of proposals made via flows. These changes are stored on behalf of each identity where relevant.

{{< note >}}
To begin developing CorDapps, see the [Developingg Appations]({{< relref "../../../developing-applications/_index.md">}}) section.
{{< /note >}}