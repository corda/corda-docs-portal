---
title: Universal constraints
date: 2020-10-15T00:00:00+01:00
menu:
  tools:
    parent: cdl-smart-contract-view
    identifier: cdl-smart-contract-view-universal-constraints
    name: Universal constraints
    weight: 120
title: Universal constraints
---

# Universal constraints

Universal constraints are constraints over the Primary state which must be satisfied irrespective of the status of the Primary state.

They are shown as a rounded box in the top left corner of the diagram:

{{< figure zoom="../resources/cdl-agreement-smart-contract-universal.png" width="1000" title="Click to zoom image in new tab/window" >}}

In our use case we want to make sure that the buyer and seller are different parties, and that it is only the buyer and seller that are proposing and consenting to agreements.
