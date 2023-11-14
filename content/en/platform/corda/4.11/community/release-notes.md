---
title: Corda Community Edition 4.11 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-05-08'
menu:
  corda-community-4-11:
    identifier: corda-community-4-11-release-notes
    parent: about-corda-landing-4-11-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Community Edition 4.11 release notes

Corda Community Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features and enhancements

### Two Phase Finality

Two Phase Finality protocol (`FinalityFlow` and `ReceiveFinalityFlow` sub-flows) has been added to improve resiliency and recoverability of CorDapps using finality. Existing CorDapps do not require any changes to take advantage of this new improved protocol.

See [Two Phase Finality]({{< relref "two-phase-finality.md" >}}).

### Upgraded dependencies

The following dependencies have been upgraded to address critical and high-severity security vulnerabilities:
* H2 has been upgraded from 1.4.197 to 2.1.214.
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final.
* Liquibase has been upgraded from 3.6.3 to 4.20.0.

### Consuming transaction IDs added to `vault_state` table

When a state is consumed by a transaction, Corda now adds the ID of the consuming transaction in the `consuming_tx_id`
column of the `vault_state` table. Corda only updates this database column for new transactions; for existing consumed
states already in the ledger, the value of `consuming_tx_id` is null.

### Deserializing AMQP data performance improvement

This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

### Extended SendTransactionFlow

`SendTransactionFlow` has been extended to allow for sending to multiple sessions.
The caller of `SendTransactionFlow` can indicate the type of sessions to send to, using the following new constructor arguments:

```
participantSessions: Set<FlowSessions>
observerSessions: Set<FlowSession>
```
These parameters are also used to infer and construct the type of recovery metadata to store on the sender side.

* Participant sessions default to using a `StatesToRecord` value of ONLY_RELEVANT
* Participant sessions default to using a `StatesToRecord` value of ALL_VISIBLE

### New Encryption Service

An AES-key implementation is used to encrypt and decrypt distribution record recovery metadata for sharing and persistence amongst peers.

### DJVM removal

The DJVM component required that all updates to Corda core were compatible with
the `core-deterministic` module. The following changes mitigate this issue:
* The experimental component DJVM has been removed from this and all future releases.
* Because of the DJVM removal, the `DriverParameters` class has changed. The two constructor parameters `djvmBootstrapSource`
and `djvmCordaSource` have been removed from `DriverParameters`. Any client code using `DriverParameters` now needs at least recompiling.

## Fixed issues

This release includes the following fixes:

* An issue has been resolved where, previously, an incorrect value for `Page.totalStatesAvailable` was returned for queries on `externalIds`, when there were external IDs mapped to multiple keys.

* Vault queries have been optimised to avoid the extra SQL query for the total state count where possible.

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.
* Debug logging of the Artemis server has been added.
* A new property, `previousPageAnchor`, has been added to `Vault.Page`. It is used to detect if the vault has changed while pages of a vault query have been loaded. If such a scenario is important to detect, then the property can be used to restart querying.

  An example of how to use this property can be found in [Vault Queries]({{< relref "api-vault-query.md#query-for-all-states-using-a-pagination-specification-and-iterate-using-the-totalstatesavailable-field-until-no-further-pages-available-1" >}}).

* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault. This issue has been resolved.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

* Added improvements to node thread names to make logging and debugging clearer.

* Previously, the order of the states in vault query results would sometimes be incorrect if they belonged to the same transaction. This issue has been resolved.

* Delays when performing a SSL handshake with new nodes no longer impacts existing connections with other nodes.

* PostgreSQL 9.6 and 10.10 have been removed from our support matrix as they are no longer supported by PostgreSQL themselves.

* Corda now supports JDK Azul 8u382 and Oracle JDK 8u381.

* log4j2.xml is now deleting the correct file for diagnostic and checkpoint logs in the rollover strategy configuration.

* Some log messages at the warning level, related to failed SSL handshakes, were inadvertently introduced during the improvements
  to SSL certificate handling in the previous patch release. These messages would frequently appear in the logs as part of
  connectivity tests for traffic load balancers and system monitoring. To reduce unnecessary noise in the logs, these specific log messages have been silenced.

## Database schema changes

The following database changes have been applied:

* The `vault_state` table now includes a `consuming_tx_id` column. The new column was added in the following migration script: `vault-schema.changelog-v14.xml`.

* Two Phase Finality introduces an additional data field within the main `DbTransaction` table:

  ```kotlin
  @Column(name = "signatures")
  val signatures: ByteArray?
  ```

* Two Phase Finality introduces two new database tables for storage of recovery metadata distribution records:

  ```bash
  @Entity
  @Table(name = "${NODE_DATABASE_PREFIX}sender_distribution_records")
  data class DBSenderDistributionRecord(
          @EmbeddedId
          var compositeKey: PersistentKey,

          /** states to record: NONE, ALL_VISIBLE, ONLY_RELEVANT */
          @Column(name = "sender_states_to_record", nullable = false)
          var senderStatesToRecord: StatesToRecord,

          /** states to record: NONE, ALL_VISIBLE, ONLY_RELEVANT */
          @Column(name = "receiver_states_to_record", nullable = false)
          var receiverStatesToRecord: StatesToRecord
  )

  @Entity
  @Table(name = "${NODE_DATABASE_PREFIX}receiver_distribution_records")
  data class DBReceiverDistributionRecord(
          @EmbeddedId
          var compositeKey: PersistentKey,

          /** Encrypted recovery information for sole use by Sender **/
          @Lob
          @Column(name = "distribution_list", nullable = false)
          val distributionList: ByteArray,

          /** states to record: NONE, ALL_VISIBLE, ONLY_RELEVANT */
          @Column(name = "receiver_states_to_record", nullable = false)
          val receiverStatesToRecord: StatesToRecord
  )
  ```
  The above tables use the same persistent composite key type:

  ```bash
  @Embeddable
  @Immutable
  data class PersistentKey(
          @Column(name = "transaction_id", length = 144, nullable = false)
          var txId: String,

          @Column(name = "peer_party_id", nullable = false)
          var peerPartyId: Long,

          @Column(name = "timestamp", nullable = false)
          var timestamp: Instant,

          @Column(name = "timestamp_discriminator", nullable = false)
          var timestampDiscriminator: Int
  )
  ```

  There are two further tables to hold distribution list privacy information (including encryption keys):

  ```bash
  @Entity
  @Table(name = "${NODE_DATABASE_PREFIX}recovery_party_info")
  data class DBRecoveryPartyInfo(
          @Id
          /** CordaX500Name hashCode() **/
          @Column(name = "party_id", nullable = false)
          var partyId: Long,

          /** CordaX500Name of party **/
          @Column(name = "party_name", nullable = false)
          val partyName: String
  )

  @Entity
  @Table(name = "${NODE_DATABASE_PREFIX}aes_encryption_keys")
  class EncryptionKeyRecord(
          @Id
          @Type(type = "uuid-char")
          @Column(name = "key_id", nullable = false)
          val keyId: UUID,

          @Column(name = "key_material", nullable = false)
          val keyMaterial: ByteArray
  )
  ```

See node migration scripts:
* `node-core.changelog-v23.xml`: Adds an additional data field within the main `DbTransaction` table.
* `node-core.changelog-v25.xml`: Adds Sender and Receiver recovery distribution record tables, plus the `PartyInfo` table.
* `node-core.changelog-v26.xml`: Adds AES encryption keys table.

## Third party component upgrades

The following table lists the dependency version changes between 4.9.5 and 4.10 Community Editions:

| Dependency           | Name           | Version 4.9.5 Community | Version 4.10 Community |
|----------------------|----------------|-------------------------|------------------------|
| com.squareup.okhttp3 | OKHttp         | 3.14.2                  | 3.14.9                 |
| org.bouncycastle	   | Bouncy Castle  | 1.68                    | 1.70                   |
| io.opentelemetry	   | Open Telemetry | -                       | 1.20.1                 |
| co.paralleluniverse:quasar-core    | Quasar       | 0.7.15_r3   | 0.7.16_r3              |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
