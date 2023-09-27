---
date: '2023-08-10'
version: 'Corda 5.1'
title: "ledger.common"
menu:
  corda51:
    identifier: corda51-api-ledger-common
    parent: corda51-api-ledger
    weight: 1000
section_menu: corda51
---
# net.corda.v5.ledger.common

The `ledger-common` package contains interfaces and types that can be used for different ledger implementations, such as:
* Exception types
* A basic {{< tooltip >}}transaction{{< /tooltip >}} interface that gets implemented by different ledger models
* A transaction signature format
* A container for transaction metadata

{{< note >}}
Any ledger model implementation can use any of these types, but it is not mandatory.
{{< /note >}}
