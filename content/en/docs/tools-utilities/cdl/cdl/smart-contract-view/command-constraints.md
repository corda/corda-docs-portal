---
title: Command constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-command-constraints"
    weight: 160

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- command constraint
---

# Command Constraints

The final type of constraint to add to the Smart Contract view is the Command constraint. Command constraints are constraints which apply when a particular Command is used in the transaction. They can place constraints on any part of the transaction, including on states which are not part of this Smart Contract.


{{< figure zoom="../resources/cdl-agreement-smart-contract-command-constraints.png" width="1000" title="Click to zoom image in new tab/window" >}}

You can use Command constraints to indicate, amongst other things:

* The changes allowed between an input primary state and a corresponding output primary state.
* The required presence of a state from another smart contract, and the properties it must have.
* A required change in a state from another smart contract, eg in our example the incrementing of a BillingState.
* That properties across different states must match, eg the reference in state A must match the reference in state B.
