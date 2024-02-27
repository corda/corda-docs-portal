---
description: Learn about the R3 contract-verifying notary protocol.
date: '2024-02-27'
title: "Contract-Verifying Notary Protocol"
menu:
  corda52:
    identifier: corda52-develop-notary-contract-verifying
    parent: corda52-develop-notaries
    weight: 2000
---
# Contract-Verifying Notary Protocol

The notary is already a well known party that must be trusted and so Corda can use it to not only check that the inputs are unconsumed, but also check and vouch for the validity of a transaction.
This is particularly suitable in use cases where the notary operator exists as an already trusted entity within the network, for example, a central bank.

Corda implements this with a notary that knows about the contracts governing the transactions in an application network, just like the other virtual nodes, and verifying that all transactions adhere to these contracts before signing them.
In this case, outputs from a transaction signed by the notary can be trusted to be valid by any virtual node without further verification of their provenance.
However, this means that the notary itself must check that any inputs to a transaction it verifies come from a transaction that has been signed by the same notary service.
Similarly, participants verifying a new proposed transaction now only need to check that all inputs come from transactions signed by the verifying notary service for the network.
Following this reasoning, the backchain resolution in the [non-validating notary protocol]({{< relref "../ledger/non-validating-notary/_index.md" >}}) of the [UTXO ledger model]({{< relref "../ledger/_index.md" >}}) is replaced by a payload consisting of the proposed transaction plus any immediate predecessors that provide the inputs being consumed by the proposed transaction.

For improved efficiency and privacy, the inputs to a proposed transaction can be sent as **filtered transactions**. Filtered transactions use Merkle proofs to only reveal the relevant parts of a transaction. In this case, only the output states used in the proposed transaction and the notary metadata, along with the relevant notary signature, are sent.


