---
title: States
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-states"
    weight: 70

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- states
---

# States

The first element of the diagram to consider is the Primary state type, in this case there is only one state type in the Smart Contract and it has been named the AgreementState. States are represented as rounded boxes with the following three sections:

* **Header**: Contains the class name (type) of the state, which must implement the ContractState interface, and the status that the state is in.
* **Properties**: Contains the properties in the state class together with their classes.
* **Participants**: Contains the participants - the Parties that will get a copy of any transaction in which this state is included as an input or output (but not reference state).

{{< figure zoom="../resources/cdl-agreement-smart-contract-state.png" width="350" title="Click to zoom image in new tab/window" >}}

In the Agreement example use case, the following properties are required:

* `buyer` - the buyer of the goods.
* `seller` - the seller of the goods.
* `goods` - a description of the goods being sold.
* `price` - the price of the goods being sold.
* `proposer` - the Party who is proposing the agreement.
* `consenter` - the party who is consenting to the proposed agreement.
* `rejectionReason` - a text field for supplying an explanation of why a proposed agreement was rejected.
* `rejectedBy` - the party who rejected the proposed agreement.

Note that rejectionReason and rejectedBy are nullable as they will not be required in all statuses.

As this needs to be a private transaction, the participants must be limited to the buyer and seller. So, both the buyer and seller will receive copies of the transactions but nobody else. Later, you must consider who gets copies of transaction through the transaction resolution process.
