---
aliases:
- /head/hello-world-introduction.html
- /HEAD/hello-world-introduction.html
- /hello-world-introduction.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-hello-world-introduction
    parent: corda-os-4-8-tutorials-index
    weight: 1010
tags:
- introduction
title: Writing a CorDapp using a template
---


# Writing a CorDapp using a template

Ready to write your first Corda Distributed Application (CorDapp)? You've come to the right place!

A CorDapp solves a specific problem using the Corda framework. CorDapps are stored on Corda nodes and executed on the Corda network. This *distributes* the app, allowing it to run on multiple systems simultaneously — unlike traditional apps, which utilize one dedicated system to achieve an assigned task. CorDapps let nodes communicate with each other to reach agreement on updates to the ledger by defining flows that Corda node owners can invoke over RPC.

Writing a CorDapp using a template involves the following steps:

1. [Get the CorDapp template](obtain-the-cordapp-template)
2. [Modify the state](modify-the-state.md)
3. [Modify the flow](modify-the-flow.md)
4. [Run your CorDapp](run-your-cordapp.md)


## Before you start

Before starting the tutorial steps, you should:

* [Familiarize yourself with Corda’s key concepts](key-concepts.md)
* [Get set up for CorDapp development](getting-set-up.md)
* [Run your first CorDapp](tutorial-cordapp.md)


## Use case

You will write a CorDapp to model IOUs on the blockchain. Each IOU – short for “I O(we) (yo)U” – will record the fact that one node owes
another node a certain amount.

In your CorDapp PartyA represents a company who have agreed to lend PartyB an amount of money. In order to maintain the obligations of the loan, you are going to use Corda to represent the loan agreement as an IOU on a network.

Once you have completed this process, you will see how CorDapps can be constructed according to any business logic you choose to apply. This could be an agreement to repay a loan, but it could be anything else that requires binding agreement between two or more parties.

This simple CorDapp will showcase several key benefits of Corda as a blockchain platform:

* **Privacy** - Since IOUs represent sensitive information, we will be taking advantage of Corda’s ability to only share
ledger updates with other nodes on a need-to-know basis, instead of using a gossip protocol to share this information with every node on
the network as you would with a traditional blockchain platform.
* **Well-known identities** - Each Corda node has a well-known identity on the network. This allows us to write code in terms of real
identities, rather than anonymous public keys.
* **Re-use of existing, proven technologies** - We will be writing our CorDapp using standard Java. It will run on a Corda node, which is
simply a Java process and runs on a regular Java machine, for example, on your local machine or in the cloud. The nodes will store their data in
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
