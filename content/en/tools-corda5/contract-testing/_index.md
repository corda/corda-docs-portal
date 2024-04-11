---
date: '2023-08-12'
title: "Contract Testing Framework"
cascade: 
    project: corda5-tools
    section_menu: corda5-tools
    version: tools
menu:
  corda5-tools:
    weight: 1000
    identifier: contract-testing
---

The Contract Testing framework enables {{< tooltip >}}CorDapp{{< /tooltip >}} developers to test smart contracts locally at an early stage of the development cycle, without having to deploy a Corda network. With this framework, you can check that your CorDapp contracts behave as expected before, or after, you write the flows.

{{< note >}}
This version of the Contract Testing framework only supports UTXO contracts.
{{< /note >}}
