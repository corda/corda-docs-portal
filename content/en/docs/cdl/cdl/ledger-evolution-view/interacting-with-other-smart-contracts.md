---
title: Interacting with other Smart Contracts
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-ledger-evolution-view"
    identifier: "cdl-ledger-evolution-view-interacting-with-other-smart-contracts"
    weight: 50

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# Interaction with other Smart Contracts

Sometimes multiple smart contracts interact with each other in a single transaction. You can show this by having multiple commands, one from each smart contract in the transaction, then linking the relevant states for each smart contract to the smart contract's Command.

In the Agreement example, Alice now wants to accept Bob's proposal, however, the Agreement Smart Contract specifies that upon the Agree Command, there must also be a BillingChip owned by the seller in the transaction. Assume that a BillingChip is part of a separate Smart Contract which provides a mechanism for tracking cumulative usage on the network.

{{< figure zoom="../resources/cdl-agreement-ledger-evolution-tx4-b.png" width="1000" title="Click to zoom image in new tab/window" >}}

The BillingChip is greyed out to show it as different to the Agreement Primary state, although this is optional.
