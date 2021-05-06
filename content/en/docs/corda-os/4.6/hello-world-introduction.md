---
aliases:
- /head/hello-world-introduction.html
- /HEAD/hello-world-introduction.html
- /hello-world-introduction.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-hello-world-introduction
    parent: corda-os-4-6-tutorials-index
    weight: 1010
tags:
- introduction
title: Hello, World!
---


# Hello, World!

Ready to write your first CorDapp? You've come to the right place!

## Introduction

CorDapps are applications that are installed on one or more Corda nodes, and that allow the node’s operator to instruct their node to perform some new process - anything from
issuing a debt instrument to making a restaurant booking.

Writing a CorDapp involves the following steps:

1. [Obtaining the CorDapp Template](hello-world-template.md)
2. [Writing the state](hello-world-state.md)
3. [Writing the flow](hello-world-flow.md)
4. [Running your CorDapp](hello-world-running.md)

## Pre-requisites

Before you begin, [your dev environment should be set up](getting-set-up.md), you should have run
[your first CorDapp](tutorial-cordapp.md), and should be familiar with Corda’s [key concepts](key-concepts.md).

## Use-case

You will write a CorDapp to model IOUs on the blockchain. Each IOU – short for “I O(we) (yo)U” – will record the fact that one node owes
another node a certain amount. This simple CorDapp will showcase several key benefits of Corda as a blockchain platform:


* **Privacy** - Since IOUs represent sensitive information, we will be taking advantage of Corda’s ability to only share
ledger updates with other nodes on a need-to-know basis, instead of using a gossip protocol to share this information with every node on
the network as you would with a traditional blockchain platform.
* **Well-known identities** - Each Corda node has a well-known identity on the network. This allows us to write code in terms of real
identities, rather than anonymous public keys.
* **Re-use of existing, proven technologies** - We will be writing our CorDapp using standard Java. It will run on a Corda node, which is
simply a Java process and runs on a regular Java machine (e.g. on your local machine or in the cloud). The nodes will store their data in
a standard SQL database.

CorDapps usually define at least three things:


* **States** - the (possibly shared) facts that are written to the ledger.
* **Flows** - the procedures for carrying out specific ledger updates.
* **Contracts** - the constraints governing how states of a given type can evolve over time.

Your IOU CorDapp is no exception. It will define the following components:


### IOUState

For a state, you will use the `IOUState`, representing an IOU. It will contain the IOU’s value, its lender, and its borrower. We can visualize
`IOUState` as follows:


{{< figure alt="tutorial state" zoom="/en/images/tutorial-state.png" >}}


### IOUFlow

For a flow, you will use the `IOUFlow`. This flow will completely automate the process of issuing a new IOU onto a ledger. It has the following
steps:


{{< figure alt="simple tutorial flow" zoom="/en/images/simple-tutorial-flow.png" >}}


### IOUContract

For this tutorial, you will use the default `TemplateContract`. You will update it to create a full-fledged `IOUContract` in [Applying contract constraints](tut-two-party-introduction.md).


## Progress so far

So far, you've decided on a design for a simple CorDapp that will allow nodes to agree new IOUs on the blockchain.

Next, you’ll take a look at the template project you’ll be using as the basis for our CorDapp.
