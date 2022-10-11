---
date: '2021-07-15'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-cordapps-flows
tags:
- api
- service
- hub
title: Accessing node services
weight: 2
---


# Access node services

You can access a node's `ServiceHub` within `FlowLogic.call`. This gives you access to all the node's services:


* `ServiceHub.networkMapCache` provides information on other nodes on the network (for example, notaries).
* `ServiceHub.identityService` lets you resolve anonymous identities into well-known identities if you have the required certificates.
* `ServiceHub.attachments` gives you access to the node’s attachments.
* `ServiceHub.validatedTransactions` gives you access to the transactions stored in the node.
* `ServiceHub.vaultService` stores the node’s current and historic states.
* `ServiceHub.keyManagementService` manages transaction signing and the generation of fresh public keys.
* `ServiceHub.myInfo` includes additional information about the node.
* `ServiceHub.clock` provides access to the node’s internal time and date.
* `ServiceHub.diagnosticsService` provides diagnostic information about the node, including the node version and currently running apps. This data should **only** be used for diagnostic purposes.
* `ServiceHub.contractUpgradeService` provides functionality for secure contract upgrades.


`ServiceHub` also exposes these properties:

* `ServiceHub.loadState` and `ServiceHub.toStateAndRef` to resolve a `StateRef` into a `TransactionState` or
a `StateAndRef`.
* `ServiceHub.signInitialTransaction` to sign a `TransactionBuilder` and convert it into a `SignedTransaction`.
* `ServiceHub.createSignature` and `ServiceHub.addSignature` to create and add signatures to a `SignedTransaction`.
