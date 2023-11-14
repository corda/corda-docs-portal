---
title: Corda Enterprise Edition 4.11 release notes
date: '2023-05-08'

menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-release-notes
    parent: about-corda-landing-4-11-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.11 release notes

Corda Enterprise Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features and enhancements

### Ledger Recovery

A new ledger recovery flow (`LedgerRecoveryFlow`) enables a node to identify and recover transactions from
peer recovery nodes to which it was a party (either initiator or receiver) and which are missing from its own ledger.

For more information, see [Ledger Recovery Flow]({{< relref "ledger-recovery-flow.md" >}}).

### Confidential Identity key-pair generator

A new service has been added that pregenerates Confidential Identity keys to be used when using CIs in transactions.
These pre-generated CIs are subsequently used for backup recovery purposes.

### Additional Network Parameters

The following network parameters, and associated node configuration parameters, have been added:

* `confidentialIdentityMinimumBackupInterval`
* `confidentialIdentityPreGenerationPeriod`
* `recoveryMaximumBackupInterval`
* `transactionRecoveryPeriod`

For more information, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).

### Distribution record cleanup

A new maintenance job `DistributionRecordCleanupTask` has been added. This removes ledger recovery distribution records that are older than the `recoveryMaximumBackupInterval` network parameter, and which are no longer needed.

If the network parameter `recoveryMaximumBackupInterval` is not defined, then the node parameter `enterpriseConfiguration.ledgerRecoveryConfiguration.recoveryMaximumBackupInterval`, if defined, is used instead.

If neither parameter is defined, then the distribution record maintenance job is disabled.

For more information, see [Ledger Recovery distribution record cleanup]({{< relref "node/operating/maintenance-mode.md#ledger-recovery-distribution-record-cleanup" >}}).

### Two Phase Finality

Two Phase Finality protocol (`FinalityFlow` and `ReceiveFinalityFlow` sub-flows) has been added to improve resiliency and
recoverability of CorDapps using finality. Existing CorDapps do not require any changes to take advantage of this
new improved protocol.

For more information, see [Two Phase Finality]({{< relref "two-phase-finality.md" >}}).

### Improved double-spend exception handling

Two Phase Finality automatically deletes an unnotarized transaction from the `DBTransaction` table if a double spend
is detected upon attempting notarization by the the initiator of `FinalityFlow`.

Additionally, if the new optional `ReceiveFinalityFlow` `handlePropagatedNotaryError` constructor parameter is set to `true` (default: `false`),
then the double spend error (`NotaryError.Conflict`) propagates back to the 2PF initiator. This enables the initiator to automatically remove the associated unnotarized transaction from its `DBTransaction` table.

If a CorDapp is compiled against Corda 4.11 (that is, its target platform version = 13) then double spend handling is enabled by default. For more information, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### Finality Recovery Tooling

RPC extension operations (additions to the FlowRPCOps interface) which allow for Finality Flow recovery by both the initiator and the receiver(s).
Also, Node Shell commands now allow operations teams to perform Finality Flow recovery.

For more information, see [Finality Flow Recovery]({{< relref "finality-flow-recovery.md" >}})

### Deserializing AMQP data performance improvement

This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

### Detect vault changes while vault query pages loaded

A new property, `previousPageAnchor`, has been added to `Vault.Page`. It is used to detect if the vault has changed while pages of a vault query have been loaded. If such a scenario is important to detect, then the property can be used to restart querying.

An example of how to use this property can be found in [Vault Queries]({{< relref "cordapps/api-vault-query.md#query-for-all-states-using-a-pagination-specification-and-iterate-using-the-totalstatesavailable-field-until-no-further-pages-available-1" >}}).

### Upgraded dependencies

The following dependencies have been upgraded to address critical and high-severity security vulnerabilities:
* H2 has been upgraded from 1.4.197 to 2.1.214.
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final.
* Liquibase has been upgraded from 3.6.3 to 4.20.0.

### Consuming transaction IDs added to `vault_state` table

When a state is consumed by a transaction, Corda now adds the ID of the consuming transaction in the `consuming_tx_id` column of the `vault_state` table. Corda only updates this database column for new transactions; for existing consumed states already in the ledger, the value of `consuming_tx_id` is null.

### Node configuration change for better performance

To reduce flow latency and improve throughput, the following default values in the node configuration have changed:
* `enterpriseConfiguration.tuning.brokerConnectionTtlCheckIntervalMs` changed from 20 to 1 millisecond.
* `enterpriseConfiguration.tuning.journalBufferTimeout` changed from 3333333 nanoseconds to 1000000 nanoseconds.
* `notary.extraConfig.batchTimeoutMs` changed from 200 to 1.

### DJVM removal

The DJVM component required that all updates to Corda core were compatible with
the `core-deterministic` module.
To mitigate this issue, the experimental component DJVM has been removed from this and all future releases.
As a result of the DJVM removal, the `DriverParameters` class has changed. The two constructor parameters `djvmBootstrapSource`
and `djvmCordaSource` have been removed from `DriverParameters`. Any client code using `DriverParameters` now needs at least recompiling.

### Additional signature verification

The `recordTransactions()` function now performs stricter signature verification when using public `ServiceHub` API.
For more information, see [DBTransactionStorage]({{< relref "node-services.html#dbtransactionstorage" >}}).

## Fixed issues

This release includes the following fixes:

* An issue has been resolved where, previously, an incorrect value for `Page.totalStatesAvailable` was returned for queries on `externalIds`, when there were external IDs mapped to multiple keys.

* Vault queries have been optimised to avoid the extra SQL query for the total state count where possible.

* Updated documentation for both `.startNodes()` and `.stopNodes()` of `MockNetwork` to indicate that restarting nodes is not supported.

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resource in the HSM. This issue occurred when:

  * The Securosys HSM was configured in a master-clone cluster
  * The master HSM had failed and Corda had failed-over to use the clone HSM
  * There was an attempt to create a transaction using confidential identities

  The issue is now resolved. When generating a wrapped key-pair the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update the PrimusX JCE should be upgraded to version 2.3.4 or later.

  There is no need to upgrade the HSM firmware version for this update but it is recommended to keep the firmware up to date as a matter of course. Currently, the latest firmware version if 2.8.50.

* Previously, where nodes had invoked a very large number of flows, the cache of client IDs that had not been removed were taking up significant heap space. A solution has been implemented where the space taken up has been reduced by 170 bytes per entry. For example, 1 million unremoved client IDs now take up 170,000,000 bytes less heap space than before.

* A new or restarted peer node coming online and connecting to a node for the first time can significantly slow message processing from other peers on the node to which it connects.  With this improvement, new peers coming online get a dedicated thread on the node they connect to and do not delay message processing for existing peer-to-peer connections on the receiving node.

* Improved compatibility when using the performance test suite from Apple silicon Macs.

* Previously, when loading checkpoints, the only log messages recorded were at the end of the process, recording the total number of checkpoints loaded.

  Now, the following additional logging has been added:

  * Checkpoints: Logging has been added for the two types of checkpoints - runnable and paused flows - being loaded; log messages show the number of checkpoints loaded every 30 seconds until all checkpoints have been loaded.

  * Finished flows: Log messages now show the number of finished flows.

  For example:

  ```
  [INFO ] 2023-02-03T17:00:12,767Z [main] statemachine.MultiThreadedStateMachineManager. - Loading checkPoints flows {}
  [INFO ] 2023-02-03T17:00:12,903Z [main] statemachine.MultiThreadedStateMachineManager. - Number of runnable flows: 0. Number of paused flows: 0 {}
  [INFO ] 2023-02-03T17:00:12,911Z [main] statemachine.MultiThreadedStateMachineManager. - Started loading finished flows {}
  [INFO ] 2023-02-03T17:00:28,437Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 9001 finished flows {}
  [INFO ] 2023-02-03T17:00:43,606Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 24001 finished flows {}
  [INFO ] 2023-02-03T17:00:46,650Z [main] statemachine.MultiThreadedStateMachineManager. - Number of finished flows : 27485 {}
  ```

* Previously, if a node was configured to use two different slots on the Luna HSM (for example using one slot for node identities and a separate slot for the confidential identities), this failed. This issue has now been resolved.

  {{< warning >}}
  However, as a result of this fix, you need to make sure the Luna client your are using is version 10.4.0 or later.
  {{</ warning >}}

* The default value for the node configuration value `cryptoServiceTimeout` has been increased from 1 second to 10 seconds.

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.

* Debug logging of the Artemis server has been added.

* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault. This issue has been resolved.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

* Added improvements to node thread names to make logging and debugging clearer.

* Previously, the order of the states in vault query results would sometimes be incorrect if they belonged to the same transaction. This issue has been resolved.

* Delays when performing a SSL handshake with new nodes no longer impacts existing connections with other nodes.

* PostgreSQL 9.6 and 10.10 have been removed from our support matrix as they are no longer supported by PostgreSQL themselves.

* Corda now supports JDK Azul 8u382 and Oracle JDK 8u381.

* log4j2.xml now deletes the correct file for diagnostic and checkpoint logs in the rollover strategy configuration.

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

The following table lists the dependency version changes between 4.10.2 and 4.11 Enterprise Editions:

| Dependency                         | Name                | Version 4.1.2 Enterprise | Version 4.11 Enterprise|
|------------------------------------|---------------------|--------------------------|------------------------|
| com.squareup.okhttp3               | OKHttp              | 3.14.2                   | 3.14.9                 |
| org.bouncycastle                   | Bouncy Castle       | 1.68                     | 1.70                   |
| io.opentelemetry                   | Open Telemetry      | -                        | 1.20.1                 |
| org.apache.commons:commons-text    | Apache Commons-Text | 1.9                      | 1.10.0                 |
| org.apache.shiro                   | Apache Shiro        | 1.9.1                    | 1.10.0                 |
| co.paralleluniverse:quasar-core    | Quasar              | 0.7.15_r3                | 0.7.16_r3              |

## Log4j patches

Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
