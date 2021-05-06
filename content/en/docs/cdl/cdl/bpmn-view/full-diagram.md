---
title: Full diagram
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-bpmn-view"
    identifier: "cdl-bpmn-view-full-diagram"
    weight: 50

tags:
- cdl
- cordapp design language
- business process modelling notation
- bpmn
- cordapp diagram
---


# Full diagram

Now that almost all the components needed to complete the full BPMN diagram are in place. You need to add an end event, this is represented as a thick circle and usually labled as 'End'.

The full diagram looks as follows:

{{< figure zoom="../resources/cdl-bpmn-agreement-process-full.png" width="1000" title="Click to zoom image in new tab/window" >}}

You can trace a number of different scenarios depending on the decisions that each of the participants takes.

{{< note >}}
To aid understanding of the BPMN View, this diagram is slightly simplified as it does not show the option for the proposer to reject their own proposal if they change their mind, which is something they can do in the smart contract.
{{< /note >}}
