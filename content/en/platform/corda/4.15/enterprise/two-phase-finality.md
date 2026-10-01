---
date: '2023-03-30T12:00:00Z'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-cordapps-flows
tags:
- two
- phase
- finality
title: Two phase finality
weight: 40
---

## Introduction

Finality refers to the act of notarizing, recording, and sharing a transaction with all of its participants. Finality enables ledger consistency.

An **initiator** uses the built-in flow called `FinalityFlow` to finalize a transaction:

1. Send the transaction to the chosen notary and, if necessary, satisfy the notary that the transaction is valid.
2. Record the transaction in the local vault, if it is relevant (that is, it involves the owner of the node).
3. Send the fully signed transaction to the other participants for recording also.

One or more **receivers** use the built-in flow `ReceiveFinalityFlow` to receive and record the finalized transaction.

## Conventional implementation

Up until Corda 4.10, the finality flow protocol was implemented using a single pass transaction sharing mechanism as depicted below:

{{< figure alt="Conventional Single Phase Finality Protocol" width=100% zoom="./resources/C4-finality-conventional.png" >}}

{{< note >}}
* Peers only received the finalized transaction after successful notarization.
* Recovery was only possible at the initiator side, as peers had no record of a transaction until finality.
* Failure conditions may have led to ledger inconsistency, requiring manual intervention for recovery.
{{< /note >}}

## Two phase finality (2PF)

To address the shortcomings of the conventional protocol, Two phase finality introduces a multi-phased protocol whereby:

* All parties have a copy of the unnotarized transaction. (Phase 1)
* Additional metadata is stored with the unnotarized transaction to aid recovery.
* All parties eventually have a copy of the notarized transaction. (Phase 2)
* Recovery is possible at both the initiator and the receiver sides.
* Failure conditions may lead to ledger inconsistency, which is recoverable using a new suite of
  [finality flow recovery tools and commands]({{< relref "finality-flow-recovery.md" >}}).

The following diagram illustrates the Two Phase Finality protocol:

{{< figure alt="Two Phase Finality Protocol" width=100% zoom="./resources/C4-finality-optimized-two-phase-finality.png" >}}

The two primary optimizations used within the protocol are:

* Usage of a *Deferred Acknowledgment* in Phase 1, where the Receiver sends back an explicit `FetchDataFlow.Request.End`
  acknowledgment to the initiator `SendTransaction` flow.

  Note that the `ReceiverTransactionFlow` is now passed an optional parameter (`deferredAck` = true) to instruct it to not perform any final acknowledging.

* Implementation of an Optimistic Finalization protocol in Phase 2, where a FinalityFlow receiver of a follow-up
  transaction (with the same peer, and using a transaction derived from the same back chain as a previous unnotarized
  transaction) automatically marks the unnotarized transaction as final. This is based on the guarantee that the follow-up
  receiver flow is receiving the initial transaction from the originating initiator that already finalized it successfully.

### Performance

Internal R3 benchmarks indicate that 2PF incurs penalties of up to 15% increased latency, and a
degradation in throughput of up to 15% (for the classic Cash Issue and Pay CorDapp use case scenario).
This trade-off in performance is outweighed by the resilience and recoverability benefits of the Two Phase Finality protocol.
