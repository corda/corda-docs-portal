---
title: Input states
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-ledger-evolution-view"
    identifier: "cdl-ledger-evolution-view-input-states"
    weight: 40

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# Input States

Transaction input states are shown at the beginning of an arrow going into transaction boxes. You must ensure that an individual instance of a state is only ever shown once on the diagram, with input and output arrows linking it respectively to the transaction that created it, and the transaction that consumes it.

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx2.png" width="900" title="Click to zoom image in new tab/window" >}}

In this example, you can see that Bob has rejected Alice's proposal. He does this by creating and signing a transaction which consumes the **PROPOSED** state and creates a **REJECTED** state that: rejects the transaction because he has *Run out of bananas*.

Continuing with the example, you can see that Bob has come up with a counter-proposal for *One bag of grapes* for £8. You can see that now Bob is the proposer, whereas Alice is the consenter in the new **PROPOSED** state and that he got to the **PROPOSED** state from a repropose command rather than a propose command.

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx3.png" width="1000" title="Click to zoom image in new tab/window" >}}
