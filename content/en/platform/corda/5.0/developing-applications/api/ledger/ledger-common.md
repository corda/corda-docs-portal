---
date: '2023-06-20'
version: 'Corda 5.0'
title: "net.corda.v5.ledger.common"
menu:
  corda5:
    identifier: corda5-api-ledger-common
    parent: corda5-api-ledger
    weight: 1000
section_menu: corda5
---
# net.corda.v5.ledger.common

The `ledger-common` package contains interfaces and types that can be used for different ledger implementations, such as:
* Exception types
* A basic transaction interface that gets implemented by different ledger models
* A transaction signature format
* A container for transaction metadata

{{< note >}}
Any ledger model implementation can use any of these types, but it is not mandatory.
{{< /note >}}