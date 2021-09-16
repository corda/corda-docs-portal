---
date: '2021-09-16'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-flows
    parent: corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-intro
    weight: 1040
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties, and in what order.

Built-in flows are provided in Corda to automate common tasks, such as gathering signatures from counterparty nodes or notarising and recording a transaction. You can also write your own flows to handle unique use cases.
