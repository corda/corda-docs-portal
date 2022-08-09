---
date: '2020-07-15T12:00:00Z'
title: "Flows"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 9000
section_menu: corda-5-dev-preview
---

Corda networks use point-to-point messaging instead of a global broadcast. Coordinating an update requires network participants to specify exactly what information needs to be sent, to which counterparties, and in what order. Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a node how to achieve a specific task, such as issuing an asset or settling a trade. Once a given business process has been encapsulated in a flow and installed on a node as part of a CorDapp, a member of the network can instruct the node to kick off this business process at any time via their node. You can read more about flows [here](../flows/overview.html).
