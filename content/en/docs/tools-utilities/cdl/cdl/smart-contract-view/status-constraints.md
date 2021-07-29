---
title: Status constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-status-constraints"
    weight: 130

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- status constraints
---

# Status Constraints

Status Constraints are constraints over the Primary state when it is a particular status.

They are shown as a rounded box under the status state box to which the constraints apply:

{{< figure zoom="../resources/cdl-agreement-smart-contract-status-constraints.png" width="1000" title="Click to zoom image in new tab/window" >}}


In the Agreement example use case, status constraints are used to show which state properties must be populated for a particular status. In particular, the aim is to:

* Mandate that rejectionReason and rejectedBy are set to null when in the PROPOSED status.
* Mandate that rejectionReason and rejectedBy are filled in when in the REJECTED status.

Whether the fields should be null or populated in the AGREED status has not been specified.

{{< note >}}
When using Kotlin types, fields cannot be null unless they are marked as nullable with a '?' after the type, eg rejectionReason: String?. So there is no need to specify that a non-nullable field, eg buyer: Party must be populated, it is implied in the class type. Although in the example, we have stated it explicitly anyway.
{{< /note >}}
