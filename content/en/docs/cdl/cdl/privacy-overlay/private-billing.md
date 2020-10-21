---
title: Private billing
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-privacy-overlay"
    identifier: "cdl-privacy-overlay-adding-the-private-billing"
    weight: 40

tags:
- cdl
- cordapp design language
- ledger evolution
- privacy overlay
- cordapp diagram
---

# Private Billing

In order to move to a billing mechanism which preserves privacy and meets the requirements, you can employ the 'Receipts' design pattern.

In the receipts pattern, there is a dependent state which has a rule that mandates that it cannot perform some action unless it sees proof that an `EnablerState` has undergone a specified action. If you put the dependent action and the enabling action in the same Corda transaction you will require the backchain of both state to be resolved for all future uses of those states. This is the what causes the privacy leaks in the naive Billing mechanism.

To avoid this we separate the enabler action out into its own transaction and generate a receipt proving that the action has taken place. It is this receipt which is used in the dependent transaction to proove that the enabling action took place.

In the private Billing mechanism in the Agreement example, the dependent state is the Agreement state and the enabling state will be a billing chip which proves that the main billing State has incremented it cumulativeUse property.

The Billing Smart Contract now looks like this diagram. You can see that there is the additional BillingChip state as well as the Primary BillingState:

{{< figure zoom="../resources/cdl-private-billing-smart-contract.png" width="700" title="Click to zoom image in new tab/window" >}}

In the Ledger Evolution view, the generation of the BillingChip is shown as follows:

{{< figure zoom="../resources/cdl-agreement-private-billing-ledger-evolution-chip1.png" width="700" title="Click to zoom image in new tab/window" >}}

The BillingChip can then go on to be used as the enabler for the dependent Agree transaction:

{{< figure zoom="../resources/cdl-agreement-private-billing-ledger-evolution-tx4-a.png" width="1000" title="Click to zoom image in new tab/window" >}}

Then the same steps are repeated for Charlie's sausage transaction (Tx 4b):

{{< figure zoom="../resources/cdl-agreement-private-billing-ledger-evolution-tx4-b.png" width="1000" title="Click to zoom image in new tab/window" >}}

Now you can add the Privacy Overlays for AgreeCorp and Charlie we see that privacy has been preserved:

{{< figure zoom="../resources/cdl-agreement-private-billing-ledger-evolution-privacy-overlays.png" width="1000" title="Click to zoom image in new tab/window" >}}

Explicitly, AgreeCorp's node doesn't resolve either Tx 4a or Tx 4b and Charlies node doesn't resolve the previous agreement between Alice and Bob.
