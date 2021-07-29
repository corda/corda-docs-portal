---
title: Billing example
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-privacy-overlay"
    identifier: "cdl-privacy-overlay-billing-example"
    weight: 20

tags:
- cdl
- cordapp design language
- ledger evolution
- privacy overlay
- cordapp diagram
---

# Billing Example

To illustrate the Privacy Overlay, and how it can be used effectively, two possible implementations of the Billing mechanism referred to in the Agreement Smart Contract are shown.

The requirements for the Billing mechanism are:

* The Business Network Operator 'Agree Corp', who has built and runs the Agreement CorDapp wants to bill the users of the Network based on usage.
* Whenever a deal is finalised on the network, as indicated by a transaction with an 'Agree' command, Agree Corp should receive notice of that activity.
* AgreeCorp must receive that notice before the (off ledger) invoicing date, not necessarily at the time of finalisation of the Agree transaction.
* Agree Corp should have the ability to vary the billing rate per Agree transaction at any time.
* AgreeCorp must not receive a copy of any agreements made on its Network.
* Parties who are not participants on an agreement must not receive copies of an Agreement, including in future transaction resolutions.

The intuitive approach to meeting these requirements is to create a BillingState which that must be included in each Agree transaction, with a cumulativeUse tracker that increments by a per transaction rate each time it is used. The Smart Contract for this BillingState might look like this:

{{< figure zoom="../resources/cdl-naive-billing-smart-contract.png" width="700" title="Click to zoom image in new tab/window" >}}

With a corresponding RateCard smart contract:

{{< figure zoom="../resources/cdl-ratecard-smart-contract.png" width="700" title="Click to zoom image in new tab/window" >}}

You can show the Billing and RateCard Smart Contracts interacting with the Agreement Smart Contract using the Ledger Evolution view:

{{< figure zoom="../resources/cdl-agreement-naive-billing-ledger-evolution-tx4-a.png" width="700" title="Click to zoom image in new tab/window" >}}

You can see that the cumulativeUse property has increased between the input.BillingState and output.BillingState by the amount indicated in the RateCardState.

You can then show what happens when the same billing token is used in another Agree transaction, this time with Charlie to buy 'One kg of sausages' for £20:

{{< figure zoom="../resources/cdl-agreement-naive-billing-ledger-evolution-tx4-b.png" width="1000" title="Click to zoom image in new tab/window" >}}

The next step is to add the privacy overlay.
