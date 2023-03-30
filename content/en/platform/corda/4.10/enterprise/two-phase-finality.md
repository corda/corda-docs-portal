---
date: '2023-03-30T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-cordapps-flows
tags:
- flow
- finality
- recovery
title: Two Phase Finality
weight: 20
---

# Two Phase Finality

## Introduction

Finality refers to the act of notarising, recording and sharing a transaction with all of its participants. Finality enables ledger consistency.

An **initiator** will use the built-in flow called `FinalityFlow` to finalise a transaction:

- Send the transaction to the chosen notary and, if necessary, satisfy the notary that the transaction is valid.
- Record the transaction in the local vault, if it is relevant (i.e. involves the owner of the node).
- Send the fully signed transaction to the other participants for recording as well.

One or more **receivers** will use the built-in flow `ReceiveFinalityFlow` to receive and record the finalised transaction.

## Conventional implementation

Up until Corda 4.10, the finality flow protocol was implemented using a single pass transaction sharing mechanism as depicted below:

{{< figure alt="conventional finality protocol" width=80% zoom="./resources/C4 Finality - Conventional.png" >}}

Note the following:

- Peers only receive the finalised transaction after successful notarisation
- Recovery is only possible at the Initiator side as Peers have no record of a transaction until finality.
- Failure conditions may lead to ledger inconsistency requiring manual intervention for recovery.

## Two Phase Finality (2PF)

To address the shortcomings of the conventional protocol, Two Phase Finality introduces a multi-phased protocol whereby:

- All parties have a copy of the Un-notarised transaction (Phase 1).
- Additional metadata is stored with the un-notarised transaction to aid recovery.
- All parties eventually have a copy of the Notarised transaction (Phase 2)
- Recovery is possible at both Initiator and Peer sides.
- Failure conditions may lead to ledger inconsistency which is recoverable using a new suite of recovery tools and commands.

The following diagram illustrates the new protocol:

{{< figure alt="conventional finality protocol" width=80% zoom="./resources/C4 Finality - Optimised 2Phase Finality.png" >}}

The two primary optimisations used within the protocol are:

- usage of a *Deferred Acknowledgement* in Phase 1, whereby the Receiver sends back an explicit `FetchDataFlow.Request.End`
  Ack to the Initiator `SendTransaction` flow.

  Note: The `ReceiverTransactionFlow` is now passed an optional parameter (deferredAck = true) to tell it to not perform any final Ack’ing.

- implementation of an Optimistic Finalisation protocol in Phase 2, whereby a FinalityFlow Receiver of a follow-up
  transaction (with the same peer, and using a transaction derived from the same back chain as a previous un-notarised
  transaction) will automatically mark the un-notarised transaction as final (based on the guarantee that the follow-up
  receiver flow is receiving the initial transaction from the originating Initiator that already finalised it successfully).

### Performance

Internal R3 benchmarks indicate that 2PF incurs penalties of up to 15% increased latency, and a
degradation in throughput of up to 15% (for the classic Cash Issue and Pay CorDapp use case scenario).
This tradeoff in performance is outweighed by the resilience and recoverability benefits of the Two Phase Finality protocol.
