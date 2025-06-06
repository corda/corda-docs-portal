---
date: '2023-06-20'
title: "ledger.consensual"
menu:
  corda52:
    identifier: corda52-api-ledger-consensual
    parent: corda52-api-ledger
    weight: 2000
---
# net.corda.v5.ledger.consensual

This package provides a very rudimentary consensual ledger. This ledger enables one or more parties to create {{< tooltip >}}states{{< /tooltip >}} and agree on their content.
A {{< tooltip >}}CorDapp{{< /tooltip >}} using the consensual ledger must define state classes that implement the `ConsensualState` interface and contain the information that
agreement should be reached on.
Every consensual state has a list of participants, and if all participants have signed the state, it is considered agreed.

There is no inherent mechanism to evolve or consume states. For example, any mechanism to form a linked chain of states is defined by the CorDapp; the platform cannot enforce such a chain in a consensual model.

For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/ledger/consensual/package-summary.html" target=" blank">Java API documentation</a>.
