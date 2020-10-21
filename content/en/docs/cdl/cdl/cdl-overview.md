---
title: "CDL Overview"
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    identifier: "cdl-overview"
    name: "CorDapp Design Language (CDL) overview"
    weight: 100
tags:
- Designing CorDapps
- CDL
- Corda design language
---

# CorDapp Design Language (CDL) overview


CorDapp Design Language (CDL) is a set of diagrammatic views you can use to concisely and accurately guide the design of your CorDapp. Using CDL in the design phase of your CorDapp allows you to:

* Represent and reason about core aspects of the Corda design including: Ledger data, shared logic, permissioning, and privacy.
* Reason about more complex CorDapp designs through abstraction from the code and standardisation.
* Produce complete, well thought-out CorDapp designs.
* Document standardised design patterns.
* Degrade gracefully. You don't always have to put in all the detail, but it should be self-consistent at the level of detail you choose.

## Who should use the CDL

CorDapp Design Language is for anyone who wants to articulate and understand non-trivial CorDapp designs. This may include:

* CorDapp Architects.
* CorDapp Developers.
* Business Analysts.
* Application Testers.
* Quality Assurance Analysts.
* Security Analysts.
* Technical Auditors.

It can also be used to communicate to non-technical audiences, for example in marketing materials, though most likely in a simplified form.

## Introducing the main CDL views

There are three main CDL views, each of which serves a different purpose in communicating a CorDapp design:

* The Smart Contract view - the primary view of CDL, which represents the design of your Corda smart contract.
* The Ledger Evolution view - a view of the smart contract in action, with representations of transactions and states on the Ledger.
* The Business Process Modelling Notation (BPMN) views - showing the process flows of your CorDapp.

In the sections below, you will find an overview of each CDL view. For a more in depth guide, take a look at the [CDL views documentation](cdl-views).

### The Smart Contract view

This is the primary view of CDL - it represents the design of your Corda smart contracts. In Corda, smart contracts consist of one or more Corda states, which represent the data going onto the Ledger, together with a Corda contract which constrains what can be done with the data in those states.

{{< note >}}
In earlier versions of CDL, the Smart Contract view was known as the State Machine view.
{{< /note >}}

#### An example Smart Contract view:

{{< figure zoom="./resources/cdl-agreement-smart-contract-full.png" width="800" title="Click to zoom image in new tab/window" >}}

This diagram shows the three statuses an agreement can have, together with the possible transitions from one status to another, and the constraints governing both statuses and transitions.

The black filled circle on the left represents the initial, uncreated, state of an agreement, which is brought into existence by being proposed, while the circle on the right represents the terminal, completed state in which the agreement has been fulfilled.

The base assumption behind the view is that Corda States can be in a number of *statuses* which might represent, for example, different stages on a multiparty workflow. We define rules for how the smart contract can move between statuses and the constraints which must be satisfied with each transition.

This view is conceptually modelled on a Finite State Machine. The classic example of which is a washing machine that has two states: **Full of water** and **Empty**. The washing machine's Finite State Machine should have the constraint that the user can only execute the **Open door** Command when the washing machine is in the **Empty** State. If it doesn't, someone is going to end up with a very wet floor.

For simple CorDapp smart contracts, there may only be one, implicit status. The Smart Contract view can still be used to communicate the design, it just devolves down to a diagram with only one state box.

A detailed explanation of the elements which make up the Smart Contract view can be found [here](smart-contract-view/cdl-smart-contract-view.md)

A Lucidchart template with the CDL Smart Contract view standard shapes [can be found here](https://app.lucidchart.com/invitations/accept/6adacd29-482f-45ca-9bdd-57252d64c8fc).

{{< note >}}
You need an active Lucidchart accound to access this folder.
{{< /note >}}

In addition, the section [CDL to Code](cdl-to-code/cdl-to-code.md) section shows a standardised way to transform the CDL Smart Contract view into code.


### The Ledger Evolution view (with Privacy overlay)

If the Smart Contract view defines a smart contract's design, the Ledger Evolution view shows that smart contract in action.

The Corda Ledger can be considered as a Directed Acyclic Graph (DAG) of states and transactions connected by input/output relationships. States are generated as outputs to a transaction, and go on to be consumed as the inputs of other transactions. The transactions have associated properties, such as the commands and who signed them.

You can't show the whole Corda Ledger in a single view (and wouldn't be useful to try). However, it is useful to show a sub-graph of the wider Ledger which concerns a particular set of transitions for the smart contract in question, and that's what the Ledger view does.

An example Ledger Evolution view:

{{< figure zoom="./resources/cdl-agreement-naive-billing-ledger-evolution-charlie.png" width="800" title="Click to zoom image in new tab/window" >}}

Here both states and transactions are represented as "nodes" in the graph. There is a connecting arrow from a transaction to a state when the state is an output of the transaction, and from a state to a transaction when the state is consumed by that transaction.

The Ledger Evolution view also has an additional Privacy overlay represented as the purple and orange lines in the above diagram. Each overlay is from the perspective of a Party on the ledger. It starts with a state which the Party is a participant on and then traces back through the DAG to show all the previous transactions the Party's node will receive a copy of through the transaction resolution mechanism. The green circles indicate that privacy has been preserved, where as the red circles indicate a privacy leak.

With this view, you have insight on privacy from the design phase. An unintended privacy leak can be a show stopper for a CorDapp. It's best to consider this early on, not at the point where your customer's information security team won't sign off the deployment.

A detailed explanation of the elements which make up the Ledger Evolution view can be found [here](ledger-evolution-view/cdl-ledger-evolution-view.md).

A Lucidchart template with the CDL Ledger Evolution view standard shapes [can be found here](https://app.lucidchart.com/invitations/accept/6adacd29-482f-45ca-9bdd-57252d64c8fc).


### The Business Process Modelling Notation (BPMN) view

The Business Process Modelling Notation view is, as the name suggests, a BPMN diagram showing the process flows of your CorDapp. It can be used to describe the macro Business Process flows, or alternatively the back and forth communication within a Corda Flow.

An example BPMN view:

{{< figure zoom="./resources/cdl-bpmn-simultaneous-action.png" width="750" title="Click to zoom image in new tab/window" >}}

The notation follows BPMN v2 standards, with a few small additions:

* Where a Corda transaction is written to the Ledger, this is represented as a simultaneous task/action on the swim lane of every participant to the transaction. Each state is marked with a small Corda logo.
* The initiator of the transaction should be indicated on the version of the action that appears in the initiator's swim lane.
* An optional Blue box can be added to show further salient details about the transaction, such as the name of the Flow which triggered it or the command used in the transaction.

Lucidchart has a standard Shapes library for BPMN 2.0 diagrams, in addition a Lucidchart template with the CDL Ledger Evolution view standard shapes can be found [here](https://app.lucidchart.com/invitations/accept/6adacd29-482f-45ca-9bdd-57252d64c8fc).

A detailed explanation of the elements which make up the BPM view can be found [here](bpmn-view/cdl-bpmn-view.md).
