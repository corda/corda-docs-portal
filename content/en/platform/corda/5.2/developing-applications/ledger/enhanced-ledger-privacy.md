---
description: Learn about the R3 contract-verifying notary protocol.
date: '2024-02-27'
title: "Enhanced Ledger Privacy"
menu:
  corda52:
    identifier: corda52-develop-notary-contract-verifying
    parent: corda52-fundamentals-ledger
    weight: 5050
---

# Enhanced Ledger Privacy

The notary is already a known party that must be trusted and so Corda can use it to not only check that the inputs are unconsumed, but also check and vouch for the validity of a transaction.
This is particularly suitable in use cases where the notary operator exists as an already trusted entity within the network, for example, a central bank.

Corda implements this with a notary that knows about the contracts governing the transactions in an application network, just like the other virtual nodes, and verifying that all transactions adhere to these contracts before signing them.
In this case, outputs from a transaction signed by the notary can be trusted to be valid by any virtual node without further verification of their provenance.
However, this means that the notary itself must check that any inputs to a transaction it verifies come from a transaction that has been signed by the same notary service.
Similarly, participants verifying a new proposed transaction now only need to check that all inputs come from transactions signed by the verifying notary service for the network.
Following this reasoning, the backchain resolution in the [non-validating notary protocol]({{< relref "./notaries/non-validating-notary/_index.md" >}}) of the {{< tooltip >}}UTXO{{< /tooltip >}} ledger model is replaced by a payload consisting of the proposed transaction plus any immediate predecessors that provide the inputs being consumed by the proposed transaction.

For improved efficiency and privacy, the inputs to a proposed transaction can be sent as **filtered transactions**. Filtered transactions use Merkle proofs to only reveal the relevant parts of a transaction. In this case, only the output states used in the proposed transaction and the notary metadata, along with the relevant notary signature, are sent

## Implementation

Writing a general purpose flow that proposes, negotiates, and finalizes does not differ whether a backchain or the enhanced privacy mode is used. Under the hood, the `UtxoLedgerService` methods such as `finalize`, `sendTransactionBuilder`, and `sendTransaction` behave differently to do one of the following:

* Include a backchain resolution
* Send a payload including the required filtered dependencies and check for the correct notary signatures on the dependencies on the receiving side

{{< note >}}
Disabling backchain resolution results in the loss of any side effects from distributing the backchain. Dependencies of a transaction are not fully resolved and added to the vault. Therefore, receiving a transaction with reference states does not make the reference states available in the receiver’s vault.
{{< /note >}}

### Reference States

Reference states are states that are referenced by a transaction without being consumed, but which must not be already consumed.

As dependencies to received transactions are not available in the vault, reference states must be distributed explicitly, using the `sendTransactionWithBackchain` or `receiveTransaction` flows available from the `UtxoLedgerService` interface. This forces a full backchain resolution for the output states of those transaction and records them in the vault, even if that is disabled for the application network. This ensures that old reference states are consumed correctly and not used erroneously in new transactions.

The following example illustrates why the backchain is required:

* The virtual node Alice has a reference state R1(0), the first output from a transaction R issuing reference states.
* For some reason, Alice misses the first update of reference states in transaction R2 that consumed R1(0) and issued R2(0).
* Another update transaction R3 consumes R2(0) and issues R3(0).

If Alice receives this with enhanced privacy (without backchain), she only receives a filtered version of R2, that wdoesill not have any inputs, and therefore not mark R1(0) as consumed.
By forcing a full backchain resolution, we ensure that Alice receives the full signed transaction R2 and thus R1(0) is consumed.

{{< note >}}
Because reference state distribution still requires a full backchain resolution, it is very important that transactions creating and consuming reference states are completely separate from transactions dealing with normal states, otherwise updating reference states might leak unwanted information.
This separation is good practice anyway, but becomes even more important when using the enhanced transaction privacy feature.
{{< /note >}}
