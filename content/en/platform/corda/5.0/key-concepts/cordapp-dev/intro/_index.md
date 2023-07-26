---
title: "Introducing CorDapps"
date: 2023-07-25
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cordapp-dev-intro
    parent: corda5-key-concepts-cordapp-dev
    weight: 1000
section_menu: corda5
---

# Introducing CorDapps

## Overview

A CorDapp, or Corda distributed application, is distributed because parts of the application can be, or may need to be, executed on a Corda instance that is operated by another party that is a member of the same Corda application network.
This is not the same as an application that has multiple instance, hosted on different environments.

Consider the centralized application below. This is a single application that always executes within a single execution environment, regardless of the fact we have multiple deployments.

{{< 
  figure
	 src="centralized-application.png"
   width="50%"
	 figcaption="Centralized Application"
>}}

Similarly, centralized applications often use a services architecture that means different parts of the applications interact with each other. This could be inside an entity’s network or different parts may be operated by different parties. 

{{< 
  figure
	 src="services-architecture.png"
   width="50%"
	 figcaption="Services Architecture"
>}}

However, distributed applications in Corda, while being deployed by different parties in the network, are unique in that parts of the application execute in the different environments as part of the same execution context.

{{< 
  figure
	 src="distributed-application.png"
   width="50%"
	 figcaption="Distributed Application"
>}}

## Workflows, Contracts, and States

CorDapps are usually composed of workflows, contracts, and states. This section* will illustrate that contracts and states are optional, but a CorDapp must always define at least one workflow, often referred to simply as a flow.

Flows support the [orchestration layer]({{< relref "../../fundamentals/CorDapps/_index.md#orchestration-layer--flows" >}}), and are written in a JVM compatible language and are hosted by Corda. Typically, flows create or transfer states on behalf of a member of the application network (a virtual node) who seeks to form [consensus]({{< relref "../../fundamentals/CorDapps/_index.md#consensus-layer" >}}) with their peer nodes with the help of the notary.

Taking our [IOU Sample App](https://github.com/corda/corda5-samples/blob/main/kotlin-samples/corda5-obligation-cordapp/) as an example of a distributed app, all members of this fictional network can be lenders or borrowers issuing, transferring, or settling loans directly to each other. There is no central ledger of loans, and consensus is achieved between the participating parties, not a central entity.

The sample app contains three flows:

* Issue
* Transfer
* Settle

Each flow handles an `IOUState` that represents the loan amount, lender, and borrower. `IOUContract` is a contract that verifies transactions that are part of the given flows, using the given state.
In this example, transactions are between borrower and lender, which means each party, members of the application network (virtual nodes), interact with each other to reach consensus. 

{{< 
  figure
	 src="iou-app.png"
   width="75%"
	 figcaption="IOU Application"
>}}

## Participants and a Distributed Ledger

Corda flows usually involve multiple parties or participants, where each participant must be a member of the application network, or a virtual node, and is generally identified by an X.500 name.

In flow terms, we refer to the initiating flow as the code that is executed on the initiating participant, and the responder flow as the code that is executed as a response on the counter party (or parties). The initiating flow is generally initiated using the REST API, as described in the [Introducing the Corda APIs]({{< relref "../api/_index.md" >}}) section.

In the IOU example, the borrower and lender are both participants in the IOU issue flow, with the borrower on the initiating side and the lender on the responder side.

{{< 
  figure
	 src="iou-app-flows.png"
   width="75%"
	 figcaption="IOU Application Flows"
>}}

When the flow shown in the diagram completes successfully, both participants have stored the state (`IOUState`) in their respective vault databases.
In an example with multiple borrowers in the network, this could result in the following state:

{{< 
  figure
	 src="iou-app-states.png"
   width="75%"
	 figcaption="IOU Application State"
>}}

As shown, the lender’s vault contains all loans, but borrowers Alice and Bob can only see the loans related to them. 
This is referred to as a Distributed Ledger.

It is worth noting that while flows usually involve multiple parties, they do not have to. Sometimes flows that only involve the initiating party are required. Examples of this are minting tokens or providing a read API for states already in the vault.

The IOU example records transactions in the vault. However, it is possible to create flows that do not use the vault, but only use the orchestration (flow) layer.

## Conclusion
* A CorDapp can consist of only a flow, but usually flows are combined with states and contracts.
* Corda defines the concept of application networks. Each member of the network, or virtual node, is supported by a CorDapp.
* A flow can involve a single participant, but usually there are at least two.
* A flow is initiated by a single participant, who executes the initiating flow, and is responded to by the other party/parties as part of the responder flow.
* Each participant has their own vault where they can store states.
* Participants only store the states they have been party to. 