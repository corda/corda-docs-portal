---
title: Output states
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-ledger-evolution-view"
    identifier: "cdl-ledger-evolution-view-output-states"
    weight: 30

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# Output States

Transaction output states take a similar form to the Smart Contract view and are shown at the end of an arrow coming out of the transaction:

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx1.png" width="500" title="Click to zoom image in new tab/window" >}}

You can see that whereas in the Smart Contract view the state boxes show the property types, in the Ledger Evolution view the state boxes show actual values for the properties.

You can also see that the participants no longer reference state properties, but have been replaced by actual Parties.

In our example we can see that Alice creates and signs a transaction which outputs a **PROPOSED** state that: proposes to Bob that Bob sells her *One bunch of bananas* for £10.
