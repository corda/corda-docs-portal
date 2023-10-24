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
* Receiver peer ID (the secure hashed value of `CordaX500Name` using SHA256)
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
* PartyId of flow peer (a secure hash stored as a String).
* Timestamp (Instant)
* Timestamp discriminator (Int)

The timestamp discriminator allows for storing of records generated at the same time but within different transactions.

The sender and receiver distribution records are subsequently used to enable Ledger Recovery.

## Ledger Recovery flow

The Ledger Recovery flow takes the following parameters:

```
val recoveryPeers: Collection<Party>,
val timeWindow: RecoveryTimeWindow? = null,
val useAllNetworkNodes: Boolean = false,
val dryRun: Boolean = false,
val useTimeWindowNarrowing: Boolean = true,
val verboseLogging: Boolean = false,
val recoveryBatchSize: Int = 1000
```

These parameters are described in the following section.


### Ledger Recovery flow parameters

#### `recoveryPeers`

`recoveryPeers` refers to a list of peer nodes to use for recovery.  This parameter is mandatory unless using `useAllNetworkNodes`.

#### `timeWindows`

`timeWindow` refers to the recovery time window and defines a `fromTime` and `untilTime`. This parameter is mandatory if not explicitly defined in configuration.

If a value is not specified by the user, the flow will attempt to use the Corda Network or Node Configuration configured time window.
Note the precedence order for this parameter is user specified first, then Node Configuration, then Corda Network parameter.

#### `useAllNetworkNodes`

`useAllNetworkNodes` specifies if all peer nodes in the network map (excluding Notary nodes) are to be used for recovery.
This parameter is optional. The default value is *false*. If set to true, this parameter overrides the `recoveryPeers` list.

#### `dryRun`

`dryRun` can be used to identify missing transactions without performing actual recovery. This parameter is optional. It defaults to *false*.

#### `useTimeWindowNarrowing`

`useTimeWindowNarrowing` specifies whether to use a window narrowing algorithm to determine the optimal time window of transactions
that are recoverable from a peer. It defaults to *true*.
For example, if the original time window specifies 30 days and there are only 3 consecutive days of missing transactions
from day 10 to day 12, a narrowed time window will determine that reconciliation only needs to take place for that 3 day time period.

#### `verboseLogging`

`verboseLogging` specifies whether to log details of each recovered transaction. By default, the flow will only report
total counts of recovered records. It defaults to *false*.

#### `recoveryBatchSize`

`recoveryBatchSize` is a performance tuning parameter that specifies how many records should be recovered in each interaction with
a recovery peer. It has been fine-tuned to a value of 1000, and can be tweaked to take into account the amount of physical memory
available on a node host.

#### `LedgerRecoverFlow`

`LedgerRecoverFlow` returns a `LedgerRecoveryResult` which includes the following information:

* `totalRecoveredRecords`: Long; total number of recovered transaction Distribution Records. For the purpose of recovery counting
there is a one-to-one association with a single transaction on a node.
* `totalRecoveredTransactions`: Long; total number of recovered transactions. This may be less than the total number of Distribution Records
if there are any transactions that already exist in the recovering node's database.
* `totalErrors`: Long; total number of errors encountered upon attempting recovery. See the node logs for details of these errors.

A `LedgerRecoveryException` is thrown if a fatal error occurs upon attempting recovery; for example, if no time window is specified and no time window configuration is defined.

{{< warning >}}
This flow only works with transactions that are persisted with recovery metadata, as of Corda 4.11, version 13.
{{< /warning >}}

###  Recoverable transaction types

All transactions types are recoverable with the exception of issuance transactions without observers (for example, where a node issues new states to itself only).

## Invoking ledger recovery

```kotlin
net.corda.core.flows.LedgerRecoveryFlow
```

### Privacy

The ledger recovery `DistributionList` is now encrypted using AES keys stored in the node's database.
Upon startup a node will create 10 random AES keys and store them in the `node_aes_encryption_keys` table, if there are no keys already present.
The keys themselves are obfuscated, by wrapping them with a deterministic AES key derived from the key's ID and the node's X.500 name.
This is done purely to reduce the impact of an accidental data dump of the keys, and is not meant to be secure.

The `senderRecordedTimestamp` has been moved to a separate header object, and is treated as the authenticated additional data in the AES-GCM encryption. This allows it to be public, which is necessary as the receiver node needs to be read it without having access to the encryption key, but also gives a guarantee to the original sender during recovery that it has not been tampered with.

### Backup Policy and Confidential Identities

Ledger Recovery is intended to be used in conjunction with a holistic Corda Network back-up policy. The `LedgerRecoveryFlow` will default to using the following ledger `transactionRecoveryPeriod` parameter value for its `TimeRecoveryWindow`.

For more information on the `transactionRecoveryPeriod` network parameter, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).

Recovering transactions using Confidential Identities requires the successful backup of the previous window of auto-generated CIs. The `confidentialIdentityPreGenerationPeriod` network parameter must be configured to specify the cut-off time after which we assume keys have not been backed up.

For more information on the `confidentialIdentityPreGenerationPeriod` network parameter, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).

## Archiving

The [Archive Service](../../../../tools/archiving-service/archiving-service-index.md) archives Ledger Recovery distribution records associated with the archived transactions. (The tables `node_sender_distribution_records` and `node_receiver_distribution_records` are included in the archiving process.)

### Performance
The Ledger Recovery flow has been optimised to support large scale recovery of transactions (internal testing has been conducted
using ten's of thousands of transactions). This has been accomplished using a combination of parallelism (when recovering against
more than one peer) and batching at several layers (reconciliation window, across-the-wire transfer of records and transactions,
and database transactional updates). Window narrowing uses a cryptographic hashing algorithm to rapidly determine the optimal recovery
window for any given peer. Furthermore, internal state is kept to a minimum, thus enabling recovery to be resumed from the
point it left off should there be any interruption in service.
