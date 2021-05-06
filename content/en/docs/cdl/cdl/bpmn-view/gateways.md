---
title: Gateways
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-bpmn-view"
    identifier: "cdl-bpmn-view-gateways"
    weight: 40

tags:
- cdl
- cordapp design language
- business process modelling notation
- bpmn
- cordapp diagram
---

# Gateways

Business process have decision points in them, decisions are represented in BPMN as gateways. Normally this is the `exclusive-or` gateway which is represented by a diamond with a cross in the middle. This means, based on some criteria take one and only one of the possible sequence paths out of the gateway. The sequence arrows coming out of the gateway are labelled with the evaluated conditional value.

Using the gateway we can extend the diagram to show the next sequences of events:

 {{< figure zoom="../resources/cdl-bpmn-agreement-process-decision1.png" width="1000" title="Click to zoom image in new tab/window" >}}

You can see how the sequence flow (solid lines) picks up from Propose Deal action on the Seller's swimlane, even though the Buyer initiated the transaction. This is an example of how the Corda transaction guaranteed duplication in a counterparties vault can initiate that counterparty to take the next step in the overall business process.
