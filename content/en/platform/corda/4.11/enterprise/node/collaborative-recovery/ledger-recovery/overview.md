---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-ledger-recovery
    parent: corda-enterprise-4-11-corda-nodes-collaborative-recovery
tags:
- ledger recovery
title: Ledger Recovery
weight: 5
---

# Ledger Recovery

Ledger Recovery builds on the foundations established in [Two Phase Finality](two-phase-finality.md),
where recovery metadata is stored for transactions at both the sender's and receiver's side of a transaction flow.

For any given transaction, the sender's side stores one or more `SenderDistribution` records in its local
`sender_distribution_records` database table. There is one `SenderDistribution` record for each receiver peer of a transaction.
Receiver peers include any participants and/or observers to the transaction.

A `SenderDistribution` record contains the following transaction metadata:
* Transaction ID
* Receiver peer ID (the secure hashed value of `CordaX500Name` using SHA256)
* Receiver `StatesToRecord` value

{{< note >}}
The `SendTransactionFlow` has been enhanced to infer the value for receiver `StatesToRecord` based on the type of sessions passed into its constructor:
* `val participantSessions: Set<FlowSession>` defaults to `ONLY_RELEVANT`
* `val observerSessions: Set<FlowSession>` defaults to `ALL_VISIBLE`
  {{< /note >}}

Upon storing the `SenderDistribution` records for a transaction, the sender node also generates a single `ReceiverDistribution` record.

A `ReceiverDistribution` record contains the following transaction metadata:
* Transaction ID
* Sender peer ID (the hashed value of `CordaX500Name`)
* A distribution list comprising two sections:
  * An AES-encrypted map of all peers and their associated `StatesToRecord` value.
  * A tamper-proof cleartext `senderRecordedTimestamp`, indicating when the sender records were generated. The same
    timestamp will be used upon storing the `ReceiverDistribution` record at each of the receiving node peers. This is
    required to enable synchronized record comparisons across peers when performing transaction recovery.

The generated `ReceiverDistribution` record is then shared with all other peer sessions (both participants and observers)
to the transaction, which stores it in their local `receiver_distribution_records` database table.

{{< note >}}
A receiver cannot decrypt the actual contents of the distribution list within that record but shares it back to a transaction initiating node upon recovery.
The Corda X.500 name of all peers stored in a Ledger Recovery record use an undecipherable collision-free representation.
{{< /note >}}

Both sender's and receiver's distribution records use the same composite key type for uniquely storing records. The `PersistentKey` contains the following fields:
* Incremental sequence Number (Long)
* PartyId of flow peer (a secure hash stored as a String)
* Timestamp (Instant)
* Timestamp discriminator (Int)

The timestamp discriminator allows for storing of records generated at the same time but within different transactions.

The sender's and receiver's distribution records are subsequently used to enable Ledger Recovery.
