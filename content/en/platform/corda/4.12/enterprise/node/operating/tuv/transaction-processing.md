---
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-transaction-processing
    parent: corda-enterprise-4-12-tuv
tags:
- transaction processing
- tuv
- transaction validator utility
title: Transaction processing
weight: 300
---

# Transaction processing

You can provide a class to process transactions at runtime using the `-c` or `--class-load` CLI option. If you do not provide the `-c` CLI option, then the utility defaults to load the process which performs transaction verification and deserialization.
You can also create and load a user-defined class. To learn how to create your own pluggable class, follow the steps in the [Testing Transaction Validator Utility](({{< relref "testing-tuv" >}})) section.
