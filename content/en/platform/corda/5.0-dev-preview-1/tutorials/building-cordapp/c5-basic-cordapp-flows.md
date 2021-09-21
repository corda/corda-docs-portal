---
date: '2021-09-16'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-flows
    parent: corda-5-dev-preview-1-tutorials-buildingcordapp
    weight: 1040
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties, and in what order.

Built-in flows are provided in Corda to automate common tasks, such as gathering signatures from counterparty nodes or notarising and recording a transaction. You can also write your own flows to handle unique use cases.

Flow implementation in the Corda 5 Developer Preview has changed significantly from Corda 4. `FlowLogic` has been split into smaller interfaces. The `Flow` interface is now used to implement a flow. When you use this interface, it defines the `call` method where the business logic goes. Flows access the Corda 5 API through injectable services using the `@CordaInject` tag. All methods previously included in `FlowLogic` are now injectable services.

This new implementation lets you add the services you need, and leave out those that you don't. This makes your CorDapp much more lightweight, allowing your nodes to run faster.

This tutorial walks you through writing the flows you need in your CorDapp:
