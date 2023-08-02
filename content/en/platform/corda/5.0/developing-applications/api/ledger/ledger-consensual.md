---
date: '2023-06-20'
version: 'Corda 5.0'
title: "net.corda.v5.ledger.consensual"
menu:
  corda5:
    identifier: corda5-api-ledger-consensual
    parent: corda5-api-ledger
    weight: 2000
section_menu: corda5
---
# net.corda.v5.ledger.consensual

This package provides a very rudimentary consensual ledger. This ledger enables one or more parties to create {{< tooltip >}}states{{< /tooltip >}} and agree on their content.
A CorDapp using the consensual ledger must define state classes that implement the `ConsensualState` interface and contain the information that
agreement should be reached on.
Every consensual state has a list of participants, and if all participants have signed the state, it is considered agreed. 

There is no inherent mechanism to evolve or consume states. For example, any mechanism to form a linked chain of states is defined by the CorDapp; the platform cannot enforce such a chain in a consensual model.