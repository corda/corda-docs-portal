---
aliases:
- /head/tut-two-party-introduction.html
- /HEAD/tut-two-party-introduction.html
- /tut-two-party-introduction.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-tut-two-party-introduction
    parent: corda-os-4-6-hello-world-introduction
    weight: 1050
tags:
- tut
- party
- introduction
title: Applying contract constraints
---


# Applying contract constraints

In the previous steps of the Hello, World tutorial, you built a CorDapp which enabled you to model IOUs on ledger.

Your CorDapp was made up of two elements:

* An `IOUState`, representing IOUs on the blockchain
* An `IOUFlow` and `IOUFlowResponder` flow pair, orchestrating the process of agreeing the creation of an IOU on-ledger

However, the CorDapp as it stands so far does not impose any constraints on the evolution of IOUs on the blockchain over time. Anyone would be free
to create IOUs of any value, between any party.

To rectify this, you must next write a contract to imposes rules on how an `IOUState` can change over time. In turn, this
will require some small changes to the flow you defined earlier in [Writing the flow](hello-world-flow.md).

Start by writing the contract - see [Writing the contract](tut-two-party-contract.md).

Once that's done, you'll need to make the necessary updates to the flow - see [Updating the flow](tut-two-party-flow.md).
