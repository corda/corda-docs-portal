---
title: Starting and sequencing
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-bpmn-view"
    identifier: "cdl-bpmn-view-starting-and-sequencing"
    weight: 20

tags:
- cdl
- cordapp design language
- business process modelling notation
- bpmn
- cordapp diagram
---

# Starting and sequencing

The start of a BPMN process is represented with a thin circle, normally annotated with 'Start', or sometimes the starting condition which triggers the process.

Activities or task are shown as Boxes within the swimlane of the participant who is performing the task. Sequential activities are shown by joining them with a solid line.

{{< figure zoom="../resources/cdl-bpmn-agreement-process-starting-and-sequencing.png" width="1000" title="Click to zoom image in new tab/window" >}}

So in this example, the process is started by the Buyer and the first thing they do is to *Decide what they would like to buy*.
