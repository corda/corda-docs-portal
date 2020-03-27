---
aliases:
- /releases/3.2/tut-two-party-introduction.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-tut-two-party-introduction
    parent: corda-enterprise-3-2-tutorials-index
    weight: 1020
tags:
- tut
- party
- introduction
title: Hello, World! Pt.2 - Contract constraints
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Hello, World! Pt.2 - Contract constraints

{{< note >}}
This tutorial extends the CorDapp built during the [Hello, World tutorial](hello-world-introduction.md).

{{< /note >}}
In the Hello, World tutorial, we built a CorDapp allowing us to model IOUs on ledger. Our CorDapp was made up of two
elements:


* An `IOUState`, representing IOUs on the ledger
* An `IOUFlow`, orchestrating the process of agreeing the creation of an IOU on-ledger

However, our CorDapp did not impose any constraints on the evolution of IOUs on the ledger over time. Anyone was free
to create IOUs of any value, between any party.

In this tutorial, we’ll write a contract to imposes rules on how an `IOUState` can change over time. In turn, this
will require some small changes to the flow we defined in the previous tutorial.

We’ll start by writing the contract.



* [Writing the contract](tut-two-party-contract.md)
* [Updating the flow](tut-two-party-flow.md)



