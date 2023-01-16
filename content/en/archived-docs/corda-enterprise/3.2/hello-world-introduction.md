---
aliases:
- /releases/3.2/hello-world-introduction.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-hello-world-introduction
    parent: corda-enterprise-3-2-tutorials-index
    weight: 1010
tags:
- introduction
title: Hello, World!
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Hello, World!



* [The CorDapp Template](hello-world-template.md)
* [Writing the state](hello-world-state.md)
* [Writing the flow](hello-world-flow.md)
* [Running our CorDapp](hello-world-running.md)



By this point, [your dev environment should be set up](getting-set-up.md), you’ve run
[your first CorDapp](tutorial-cordapp.md), and you’re familiar with Corda’s [key concepts](key-concepts.md). What
comes next?

If you’re a developer, the next step is to write your own CorDapp. CorDapps are plugins that are installed on one or
more Corda nodes, and give the nodes’ owners the ability to make their node conduct some new process - anything from
issuing a debt instrument to making a restaurant booking.


## Our use-case

Our CorDapp will model IOUs on-ledger. An IOU – short for “I O(we) (yo)U” – records the fact that one person owes
another person a given amount of money. Clearly this is sensitive information that we’d only want to communicate on
a need-to-know basis between the lender and the borrower. Fortunately, this is one of the areas where Corda excels.
Corda makes it easy to allow a small set of parties to agree on a shared fact without needing to share this fact with
everyone else on the network, as is the norm in blockchain platforms.

To serve any useful function, our CorDapp will need at least two things:


* **States**, the shared facts that Corda nodes reach consensus over and are then stored on the ledger
* **Flows**, which encapsulate the procedure for carrying out a specific ledger update

Our IOU CorDapp is no exception. It will define both a state and a flow:


### The IOUState

Our state will be the `IOUState`. It will store the value of the IOU, as well as the identities of the lender and the
borrower. We can visualize `IOUState` as follows:


![tutorial state](/en/images/tutorial-state.png "tutorial state")


### The IOUFlow

Our flow will be the `IOUFlow`. This flow will completely automate the process of issuing a new IOU onto a ledger. It
is composed of the following steps:


![simple tutorial flow](/en/images/simple-tutorial-flow.png "simple tutorial flow")

In traditional distributed ledger systems, where all data is broadcast to every network participant, you don’t need to
think about data flows – you simply package up your ledger update and send it to everyone else on the network. But in
Corda, where privacy is a core focus, flows allow us to carefully control who sees what during the process of
agreeing a ledger update.


## Progress so far

We’ve sketched out a simple CorDapp that will allow nodes to confidentially issue new IOUs onto a ledger.

Next, we’ll be taking a look at the template project we’ll be using as the basis for our CorDapp.

