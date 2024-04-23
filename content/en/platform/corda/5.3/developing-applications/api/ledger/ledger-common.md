---
date: '2023-06-20'
title: "ledger.common"
menu:
  corda53:
    identifier: corda53-api-ledger-common
    parent: corda53-api-ledger
    weight: 1000
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

For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/ledger/common/package-summary.html" target=" blank">Java API documentation</a>.
