---
title: Flow constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-flow-constraints"
    weight: 150

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- flow constraints
---

# Flow Constraints

Each of the transitions shown in a Smart Contract view diagram are enacted through a Corda transaction. These transactions are built, signed, and finalised using Corda flows. In order to aid understanding of the wider CorDapp design it can be useful to indicate what the Flows should be doing when they are building the transaction that implements a particular transition. You do this using a **flow constraint**.

Flow constraints are denoted by a blue box attached to the relevant Path:


{{< figure zoom="../resources/cdl-agreement-smart-contract-flow-constraints.png" width="1000" title="Click to zoom image in new tab/window" >}}

{{< attention >}}
Flow constraints are ***not*** implemented in the smart contract, they are really only a note about what a different part of the CorDapp *may* be doing when a Path is enacted. As they are not implemented in the smart contract they don't carry the same Corda guarantees that different counterparties are following the same set of rules. Or to put it another way, the counterparty could have re-written their Flows: don't place critical business controls that other parties will rely on in the Flows.
{{< /attention >}}

You can use flow constraints to illustrate:

* Which party is intended to initiate the flow which builds and initially signs the transaction. This is important because it is normally only the initiator who gets to make an informed and conscious decision to partake in the transaction, responders nodes will accept and possibly sign valid transactions but there is usually not a human 'do you want to do this?' decision step.
* Checks that a Party should do before they initiate a transaction - for example, has the initiator got enough funds or stock for this Agreement.
* Events which will trigger a Flow - for example, trigger this flow when the goods have been dispatched.
