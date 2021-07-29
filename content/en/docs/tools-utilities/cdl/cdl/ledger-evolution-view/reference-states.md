---
title: Reference states
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-ledger-evolution-view"
    identifier: "cdl-ledger-evolution-view-reference-states"
    weight: 60

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# Reference states

Reference states need to be represented in the Ledger Evolution View. Reference states are like input states in that they are a reference to already existing, non consumed states on the ledger, but they do not get consumed by the transaction and do not execute their contract logic.

You can show reference states as input states but with a dashed line from the state to the transaction in which it is referenced.

In the Agreement example, the Smart Contract requires that the BillingChip value is the same as the value specified by a ratecard state. This rate card needs to be used in multiple transactions so it is included as a reference state:

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx4-c.png" width="1000" title="Click to zoom image in new tab/window" >}}
