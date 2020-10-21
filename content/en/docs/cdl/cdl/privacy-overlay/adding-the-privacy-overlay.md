---
title: Adding the Privacy Overlay
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-privacy-overlay"
    identifier: "cdl-privacy-overlay-adding-the-privacy-overlay"
    weight: 30

tags:
- cdl
- cordapp design language
- ledger evolution
- privacy overlay
- cordapp diagram
---

# Adding the Privacy Overlay

The Privacy Overlay is always from the perspective of a single Party on the ledger. It shows what the Party's node ends up with in their vault via the transaction resolution mechanism. You can add multiple Privacy Overlays on the same Ledger Evolution view using different colours to denote the different parties.

As the Privacy overlay traces back through the DAG you will normally start at the end of the Ledger Evolution by identifying a state that has the Party we are analysing as a participant. You then simply trace back the DAG from that state.

If a transaction contains information the Party is allowed to see, you mark the transaction block with a 'Visibility allowed' green circle. If the transaction contains information the Party is not allowed to see, you mark the transaction with a red 'Privacy leak' circle.

In this diagram, these visibility permissions are illustrated by AgreeCorp who, per the requirements, is not allowed to see any Agreements on its network:

{{< figure zoom="../resources/cdl-agreement-naive-billing-ledger-evolution-agreecorp.png" width="1000" title="Click to zoom image in new tab/window" >}}

This is extended to Charlie, who is permitted to see his own Agreement, but not prior Agreements in the backchain:

{{< figure zoom="../resources/cdl-agreement-naive-billing-ledger-evolution-charlie.png" width="1000" title="Click to zoom image in new tab/window" >}}

You can see from this view that the initial mechanism for implementing Billing creates privacy leaks in transaction tx 4b and in the backchain. It is clear that this design requires a better mechanism.
