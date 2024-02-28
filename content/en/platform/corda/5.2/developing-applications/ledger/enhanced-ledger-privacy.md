---
description: Learn about the R3 contract-verifying notary protocol.
date: '2024-02-27'
title: "Transaction Privacy Enhancements"
menu:
  corda52:
    identifier: corda52-develop-notary-contract-verifying
    parent: corda52-fundamentals-ledger
    weight: 5050
---

# Transaction Privacy Enhancements

Transaction privacy enhancements enable you to operate a network that increases the privacy of transactions by no longer requiring every virtual node in a network to see and verify all predecessors, linked by inputs, back to issuance of a transaction on the UTXO ledger. In exchange, visibility of transaction content must be given to the notary.

The notary is already a known party that must be trusted and so Corda can use it to not only check that the inputs are unconsumed, but also check and vouch for the validity of a transaction.
This is particularly suitable in use cases where the notary operator exists as an already trusted entity within the network, for example, a central bank.

Corda implements this with a notary that knows about the contracts governing the transactions in an application network, just like the other virtual nodes, and verifying that all transactions adhere to these contracts before signing them.
In this case, outputs from a transaction signed by the notary can be trusted to be valid by any virtual node without further verification of their provenance.
However, this means that the notary itself must check that any inputs to a transaction it verifies come from a transaction that has been signed by the same notary service.
Similarly, participants verifying a new proposed transaction now only need to check that all inputs come from transactions signed by the verifying notary service for the network.
Following this reasoning, the backchain resolution in the [non-validating notary protocol]({{< relref "./notaries/non-validating-notary/_index.md" >}}) of the {{< tooltip >}}UTXO{{< /tooltip >}} ledger model is replaced by a payload consisting of the proposed transaction plus any immediate predecessors that provide the inputs being consumed by the proposed transaction.

For improved efficiency and privacy, the inputs to a proposed transaction can be sent as **filtered transactions**. Filtered transactions use Merkle proofs to only reveal the relevant parts of a transaction. In this case, only the output states used in the proposed transaction and the notary metadata, along with the relevant notary signature, are sent.

## Considerations

This section outlines the [advantages](#backchain-skipping-advantages) and [drawbacks](#backchain-skipping-drawbacks) of backchain skipping (contract-verifying notary protocol) versus backchain resolution (non-validating notary protocol).

### Backchain Skipping Advantages

* **Enhanced privacy between participants**  - Participants only see the transactions that they are party to. While they need to see the inputs to a transaction to verify it before signing, they receive those as part of filtered transactions, so they only see exactly the required inputs.
* **Enhanced performance** - Instead of an ever growing backchain, Corda only requires a bundle with the direct inputs for each new transaction, so the throughput of the system will not start to degrade with long time use of tokens.
* **Reduced storage footprint** - Each member node only needs to store transactions it is involved in, and the direct inputs. Depending on the nature of the network application, this can lead to a drastic reduction in required database space.
* **Easier archiving** - Once all outputs from a transaction are spent, the transaction it will no longer be required, making it easier to deduce which parts of the ledger can be archived.
* **Eliminates denial of state attacks** - Running verification on the notary eliminates any risk of denial of state attacks by requesting notarizations of bogus transactions with known inputs. Every transaction has to conform to the contract rules of the network and is checked to carry the required signatures.

### Backchain Skipping Drawbacks

* **More trust in the notary operator** - Participants must all rely on the contract verifying notary working correctly, and the network traffic to the notary is increased. This must be taken into consideration when planning the network layout.
Furthermore, it will often be impossible to prove the validity of a transaction locally without relying on the verification run on the notary to endorse the validity of the inputs.
* **Increased notary operator responsibility** - Depending on the legal frameworks around the application network, the notary operator might become liable for the correctness of the contract verification.
* **Loss of privacy towards the notary operator** - In the classic UTXO model, only participants involved in transactions see the transaction and the backchain. The network operator and the notary never see any contents of the transactions, only the hashes and indices denoting the consumed and created states. In the contract-verifying model, the notary must process all transaction content, to enable a total view of all interactions on the global ledger. However, there is no requirement for the notary to store a copy of all the transaction data.
* **Loss of history** - No provenance or audit trail of a state is maintained without introducing special virtual nodes to observe all transactions in the network. If necessary, for example supply chain tracing this must be enforced by the smart contracts.

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

If Alice receives this with enhanced privacy (without backchain), she only receives a filtered version of R2, that does not have any inputs, and therefore not mark R1(0) as consumed.
By forcing a full backchain resolution, we ensure that Alice receives the full signed transaction R2 and thus R1(0) is consumed.

{{< note >}}
Because reference state distribution still requires a full backchain resolution, it is very important that transactions creating and consuming reference states are completely separate from transactions dealing with normal states, otherwise updating reference states might leak unwanted information.
This separation is good practice anyway, but becomes even more important when using the enhanced transaction privacy feature.
{{< /note >}}
