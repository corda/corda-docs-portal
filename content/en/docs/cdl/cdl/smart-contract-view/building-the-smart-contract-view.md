---
title: Building the Smart Contract view
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-building-the-smart-contract-view"
    weight: 60

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
---

# Building up the Smart Contract view

Over the following sections you will discover the elements of the Smart Contract view.

You will follow a simple negotiation use case, where a buyer is negotiating to buy some goods from a seller for an agreed price. The requirements can be summarised as follows:

* There should be a buyer and a seller who are represented as Parties on a Corda Network.
* The negotiation should result in an agreement recorded on the Corda Ledger which has the conscious and informed consent of both parties.
* The agreement should record the buyer, seller, description of the goods and the price agreed.
* Either party should be able to propose an agreement, with the other party either consenting to or rejecting the proposal.
* The proposer should be able to change their mind and revoke the proposal prior to the other party consenting.
* When a agreement is agreed, then a billing tracker must increment which tracks Network usage for the purpose of billing.
* Privacy must be maintained such that Parties to an agreement can't see previous agreements performed on the network to which they were not a party
* The Business Network Operator who manages the Agreement Service should not see details of the agreements made on their network.

You can follow the steps in the build up to a full Smart Contract view diagram which, will look like this:

{{< figure zoom="../resources/cdl-agreement-smart-contract-full.png" width="1000" title="Click to zoom image in new tab/window" >}}
