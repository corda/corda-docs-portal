---
date: '2020-09-10'
title: "Confidential Identities SDK"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-confidential-identities
    weight: 8500
section_menu: corda-5-dev-preview
description: >
    Documentation for the Confidential Identities SDK.
---


Confidential identities are key pairs where the corresponding X.509 certificate (and path) are not made public, so that parties who are not involved in the transaction cannot identify the owner. They are owned by a well-known identity, which must sign the X.509 certificate. Before constructing a new transaction the initiating party must request that the counter-party generate and exchange a new confidential identity, a process which is managed using `RequestKeyFlow` (discussed below). The public key of this confidential identity is then used when generating output states and commands for the transaction.

Where using outputs from a previous transaction in a new transaction, counterparties may need to know who the involved parties are. If confidential identities are being used, the buyer will want to ensure that the asset being transferred is owned by the seller, and the seller will likewise want to ensure that the cash being transferred is owned by the buyer. Verifying this requires both nodes to have a copy of the confidential identities for the asset and cash input states. `SyncKeyMappingFlow` manages this process. It takes as inputs a transaction and a counter-party session, and for every confidential identity involved in that transaction for which the calling node holds the certificate path, it sends this certificate path to the counter-party. Alternatively, instead of taking a transaction as an input, a list of confidential identities to sync can be given as input.

For convenience, these two flows have initiating flows available in `com.r3.corda.lib.ci.workflows.InitiatingFlows` which can be called as subflows instead of initiating sessions in a custom flow.

## About this version

This version of Confidential Identities is for use only with the Corda 5 Developer preview. It cannot be used with any other version of Corda.
