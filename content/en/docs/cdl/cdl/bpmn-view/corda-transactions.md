---
title: Corda transactions
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-bpmn-view"
    identifier: "cdl-bpmn-view-corda-transactions"
    weight: 30

tags:
- cdl
- cordapp design language
- business process modelling notation
- bpmn
- cordapp diagram
---

# Corda Transactions

After the Buyer has decided what they would like to buy, they need to initiate a Propose Corda Transaction. The Corda transactions are shown as a set of duplicated actions in the swim lane of each participant involved in the Corda transaction, with the Corda logo in the corner.

The actions are joined with a two way dashed line. In BPMN dashed lines denote messages and are normally unidirectional. However, in the CorDapp BPMN a two way arrow is used to reflect that there is a series of back and forth messages which result in a finalised transaction on the ledger.

The party that initiated the transaction is marked, and the message line is annotated on the Initiator end with a blue box giving more details about how the transaction was formed. This is typically what Flow is invoked and what the Command in the transaction should be.


{{< figure zoom="../resources/cdl-bpmn-agreement-process-corda-transactions.png" width="1000" title="Click to zoom image in new tab/window" >}}


In this example you can see that the Buyer will initiate the ProposeFlow to create a Propose transaction.
