---
date: '2020-07-15T12:00:00Z'
title: "Flows"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-flows
    weight: 5000
section_menu: corda-5-dev-preview
---

Describe the flows available in Corda 5..
sub-flows - Creating a new scope for initiating sessions and closing them once you leave the scope is one primary benefit

Corda networks use point-to-point messaging instead of a global broadcast. Coordinating an update requires network participants to specify exactly what information needs to be sent, to which counterparties, and in what order. Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a node how to achieve a specific task, such as issuing an asset or settling a trade. Once a given business process has been encapsulated in a flow and installed on a node as part of a CorDapp, a member of the network can instruct the node to kick off this business process at any time via their node. You can read more about flows

**
## Understand flows:
As a CorDApp developer,
I want to understand what a flow is and how they meet my business requirements.
I want to understand pre-requisite concepts such as Application Networks, Corda Identity, Virtual Nodes,
I want to understand core Flow concepts:
•	Flow “signatures”,
•	writing blocking code,
•	service injections,
•	http-rpc/ json data,
•	annotations
•	base flows types,
•	sub-flows,
•	initiator-responder pairs,
•	versioning and upgrades.
So I have a solid conceptual understanding of Flows and can apply them to my business problem.
The Corda 5 Documentation should explain:
•	Pre-req concepts (app networks, Corda identity, Virtual Nodes)
•	Key concepts for Flows
•	How to construct flows.
•	Flow API and how to use the methods
•	Examples of each API method/ Concepts


**
