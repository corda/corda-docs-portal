---
date: '2023-07-27T12:00:00Z'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-cordapps-flows
tags:
- flow
- ledger
- recovery
title: Ledger Recovery
weight: 45
---

Ledger Recovery builds on the foundations established in [Two Phase Finality](two-phase-finality.md), 
where recovery metadata is stored for transactions at both the sender and receiver side of a transaction flow.

For any given transaction, the sender side stores one or more `SenderDistribution` records in its local
`sender_distribution_records` database table. There is one `SenderDistribution` record for each receiver peer of a transaction.
Receiver peers include any participants and/or observers to the transaction.

A `SenderDistribution` record contains the following transaction metadata:

* Transaction ID
* Receiver peer ID (the hashed value of `CordaX500Name`)
* Receiver `StatesToRecord` value

{{< note >}}
The `SendTransactionFlow` has been enhanced to infer the value for receiver `StatesToRecord` based on the type of sessions passed into its constructor:

* val participantSessions: Set<FlowSession> => default to ONLY_RELEVANT
* val observerSessions: Set<FlowSession> => default to ALL_VISIBLE
{{< /note >}}

Upon storing the `SenderDistribution` records for a transaction, the sender node also generates a single `ReceiverDistribution` record.

A `ReceiverDistribution` record contains the following transaction metadata:

* Transaction ID
* Sender peer ID (the hashed value of `CordaX500Name`)
* A distribution list comprising two sections:
  * An AES-encrypted map of all peers and their associated `StatesToRecord` value.
  * A tamper-proof cleartext `senderRecordedTimestamp`, indicating when the sender records were generated. The same timestamp will be used upon storing the `ReceiverDistribution` record at each of the receiving node peers. This is required to enable synchronized record comparisons across peers when performing transaction recovery.

The generated `ReceiverDistribution` record is then shared with all other peer sessions (both participants and observers) to the transaction, which stores it in their local `receiver_distribution_records` database table. 

{{< note >}}
A receiver cannot decrypt the actual contents of the distribution list within that record, but shares it back to a transaction initiating node upon recovery.
{{< /note >}}

Both sender and receiver distribution records use the same composite key type for uniquely storing records. The `PersistentKey` contains the following fields:

* Incremental sequence Number (Long)
* Timestamp (Instant)
* Timestamp discriminator (Int)

The timestamp discriminator allows for storing of records generated at the same time but within different transactions.

The sender and receiver distribution records are subsequently used to enable Ledger Recovery.

## Ledger Recovery flow

The Ledger Recovery flow takes the following parameters:

```
private val recoveryPeers: Collection<Party>,
private val timeWindow: RecoveryTimeWindow,
private val useAllNetworkNodes: Boolean = false,
private val transactionRole: TransactionRole = TransactionRole.ALL,
private val dryRun: Boolean = false,
private val optimisticInitiatorRecovery: Boolean = false,
```

These parameters are described in the following section.


### Ledger Recovery flow parameters

#### `recoveryPeers`

`recoveryPeers` refers to a list of peer nodes to use for recovery.  This parameter is mandatory.

#### `timeWindows`

`timeWindow` refers to the recovery time window and defines a `fromTime` and `untilTime`. This parameter is mandatory. 

It defaults to using the Corda Network or Node Configuration configured time window.

#### `useAllNetworkNodes`

`useAllNetworkNodes` specifies if all peer nodes in the network map are used for recovery. This parameter is optional. The default value is *false*. If set to true, this parameter overrides the `recoveryPeers` list.

#### `transactionRole`

`transactionRole` specifies which type(s) of transactions to recover from the viewpoint of the recovering node. This parameter is optional. It defaults to *ALL*.

`transactionRole` can take the following values:

* **ALL** - Recover all transactions.
* **INITIATOR** - Only recover transactions that I initiated.
* **PEER** - Only recover transactions where I am a participant in a transaction.
* **OBSERVER** - Only recover transactions where I am an observer (but not participant) to a transaction.
* **PEER_AND_OBSERVER** - Only recover transactions where I am either a participant or observer.

#### `dryRun`

`dryRun` can be used to identify missing transactions without performing actual recovery. This parameter is optional. It defaults to *false*.

#### `optimisticInitiatorRecovery`

`optimisticInitiatorRecovery` is a special mode of operation that not only recovers missing transactions from peers,
but will also attempt to forward an initiated transaction (for example, where the recovering node was the initial sender of a
transaction) to other peers specified in the original transaction peers distribution list.

This option is useful if there is more than one failed node (for the same or overlapping recovery time window), as
missing transactions are pushed to other failed nodes (without them having to call the recovery flow themselves).

Note this option only works for active recovery (for example, where `dryRun` = false).

This parameter is optional. The default value is *false*.

#### `LedgerRecoverFlow`

`LedgerRecoverFlow` returns a collection of `RecoveryResult` for each identified recoverable transaction from a given peer.
A `RecoveryResult` includes the following information:

* `transactionId`: SecureHash; the ID of the transaction.
* `recoveryPeer`: The CordaX500Name of the peer from which the transaction was recovered.
* `transactionRole`: The peer's role in the transaction.
* `synchronized`: A Boolean value indicating if the transaction was successfully synchronized. This value will always be *false* if the `dryRun` option is specified.
* `synchronisedInitiated`: A Boolean value; this if only attempted if the `optimisticInitiatorRecovery` option is set to *true*.
* `failureCause`: A String variable containing the reason why a transaction failed to synchronize.

A `LedgerRecoveryException` is thrown if a fatal error occurs upon attempting recovery; for example, the peer recovery node is unreachable.

{{< warning >}}
This flow only works with transactions that are persisted with recovery metadata, as of Corda 4.11, version 13.
{{< /warning >}}

###  Recoverable transaction types

All transactions types are recoverable with the exception of issuance transactions without observers (for example, where a node issues new states to itself only).

## Invoking ledger recovery

```kotlin
net.corda.node.internal.recovery.FinalityRecoveryFlow
```

### Privacy

The ledger recovery `DistributionList` is now encrypted using AES keys stored in the node's database.
The node on startup will create 10 random AES keys and store them in the `node_aes_encryption_keys` table, if there are no keys already present.
The keys themselves are obfuscated, by wrapping them with a deterministic AES key derived from the key's ID and the node's X.500 name.
This is done purely to reduce the impact of an accidental data dump of the keys, and is not meant to be secure.

The `senderRecordedTimestamp` has been moved to a separate header object, and is treated as the authenticated additional data in the AES-GCM encryption. This allows it to be public, which is necessary as the receiver node needs to be read it without having access to the encryption key, but also gives a guarantee to the original sender during recovery that it has not been tampered with.

### Backup Policy and Confidential Identities

Ledger Recovery is intended to be used in conjunction with a holistic Corda Network back-up policy. The `LedgerRecoveryFlow` will default to using the following ledger `transactionRecoveryPeriod` parameter value for its `TimeRecoveryWindow`. 

For more information on the `transactionRecoveryPeriod` network parameter, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).

Recovering transactions using Confidential Identities requires the successful backup of the previous window of auto-generated CIs. The `confidentialIdentityPreGenerationPeriod` network parameter must be configured to specify the cut-off time after which we assume keys have not been backed up.

For more information on the `confidentialIdentityPreGenerationPeriod` network parameter, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).
