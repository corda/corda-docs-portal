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

{{< note >}}
If you are using the Archive Service with Corda Enterprise Edition 4.11, you must use the 1.1.x stream of the Archive Service release. For more details, see [Archive Service]({{< relref "../../../../tools/archiving-service/archiving-release-notes.md" >}}).
{{< /note >}}

## Corda Enterprise Edition 4.11.6 release notes

Corda Enterprise Edition 4.11.6 is a patch release of Corda Enterprise Edition focused on resolving issues and updating third-party dependencies. 

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

- The Corda Network Builder Tool now correctly deploys a Corda network both via CLI in Docker and Azure environments. <!-- ENT-12147 --> 
- The flow `recoverAllFinalityFlows` previously treated inactive flows as active. This behavior has been corrected. <!-- ENT-13814 ENT Only -->

### Third-party components upgrade

The following table lists the dependency upgrades for 4.11.6 Enterprise Edition. Dependencies with unchanged versions are omitted. <!-- ENT-13978 -->

| Dependency                                            | New Version        |
|-------------------------------------------------------|--------------------|
| com.github.docker-java:docker-java                    | 3.5.2              |
| com.github.docker-java:docker-java-transport-httpclient5 | 3.5.2           |
| io.netty:tcnative*                                    | 2.0.74.Final       |
| com.fasterxml.jackson.core:jackson-annotations        | 2.17.3             |
| io.netty:*                                            | 4.1.128.Final      |
| commons-beanutils:commons-beanutils                   | 1.11.0             |
| org.apache.commons:commons-lang3                      | 3.19.0             |
| org.controlsfx:controlsfx                             | 11.2.2             |
| com.azure.resourcemanager:azure-resourcemanager       | 2.52.0             |
| com.azure:azure-identity                              | 1.18.1             |
<!-- ENT-14529 -->

## Corda Enterprise Edition 4.11.5 release notes

Corda Enterprise Edition 4.11.5 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* When deploying a test node using DriverDSL, the node now starts successfully without encountering a `NoSuchMethodError` exception.
* You can now create two nodes with identical `O` field values but different `OU` values in their X.500 names when using the DriverDSL for testing.
* There is no longer a memory leak when creating a series of mock networks for testing purposes.
* Transactions with the in-flight transaction state, introduced in Corda version 4.11 to support transaction recovery, are no longer included when the Ledger Graph CorDapp builds a transaction graph. Instead, the CorDapp now ignores any transactions with an in-flight status.

### New features, enhancements and restrictions

* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.
* Docker images are now based on Java 8 build 432.

### Third-party components upgrade

The following table lists the dependency version changes between 4.11.4 and 4.11.5 Enterprise Editions:

| Dependency                   | Name                | Version 4.11.4 Enterprise   | Version 4.11.5 Enterprise      |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*          | Jetty               | 9.4.53.v20231009            | 9.4.56.v20240826               |
| commons-io:commons-io        | commons IO          | 2.6                         | 2.17.0                         |
| com.zaxxer:HikariCP          | Hikari              | 3.3.1                       | 4.0.3                          |
| org.apache.sshd:sshd-common  | sshd                | 2.9.2                       | 2.13.2                         |
| org.apache.commons:commons-configuration2   | commonsConfiguration2       | 2.10.0          | 2.11.0              |

## Corda Enterprise Edition 4.11.4 release notes

Corda Enterprise Edition 4.11.4 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* `ReceiveFinalityFlow` was returning a transaction that was missing the notary signature. This has now been fixed. The returned transaction now includes the notary signature.
* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Enterprise Edition 4.11.3 release notes

Corda Enterprise Edition 4.11.3 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Database upgrades failed when upgrading from a pre-4.11 node, if the database contained new-style confidential identities, that is, those without a certificate.

## Corda Enterprise Edition 4.11.2 release notes

Corda Enterprise Edition 4.11.2 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* In the default log4j2.xml file, the Delete action in the DefaultRolloverStrategy policy for log files beginning with `diagnostic-*` or `checkpoints_agent-*` was incorrect. It erroneously compared against the wrong file names. This issue has been rectified, ensuring that files are now deleted in accordance with the policy.
* Resolved a TLS connection issue regression when using a HSM to store TLS private keys.
* Fixed a regression in the RPC `getFlowsMatchingV2` extension operation that rendered it incompatible with previous Corda releases. This issue manifested in the Corda flow management GUI, preventing it from displaying the flow status of previous Corda releases. Due to this fix, if you have created an RPC client using 4.11.1 or 4.11, you need to rebuild the client using 4.11.2.
* Previously, a rare error scenario could occur where a node would erroneously perceive a valid connection to a peer when, in fact, it was not connected. This issue typically arose when the peer node was disconnecting/connecting. This issue has now been resolved.

### Third party component upgrades

* Jetty version was upgraded from 9.4.51.v20230217 to 9.4.53.v20231009.
* Apache Tomcat was upgraded from 9.0.82 to 9.0.83 in the node management plugin, which is now at version 1.0.6.


## Corda Enterprise Edition 4.11.1 release notes

Corda Enterprise Edition 4.11.1 is a patch release of Corda Enterprise Edition focused on resolving issues.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "../enterprise/_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Interoperability fix between 4.11 and pre-4.11 nodes when sending/fetching transactions for new data type: `TRANSACTION_RECOVERY`.

## Corda Enterprise Edition 4.11 release notes

Corda Enterprise Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features, enhancements and restrictions

### Archive Service and Corda Enterprise compatibility

The [Archive Service]({{< relref "../../../../tools/archiving-service/archiving-release-notes.md" >}}) is a standalone service that operates on a different release cadence to the Corda platform. If you intend to use it with Corda Enterprise 4.11 and above, you must use the 1.1.x version of the Archive Service. Version 1.0.x of the Archive Service is compatible with Corda 4.10 and below. The latest 1.1.x version of the Archive Service was introduced to handle the extra signatures column added to the node transactions table.

### JDK Azul and Oracle JDK upgrade

Corda now supports JDK Azul 8u382 and Oracle JDK 8u381.

### Collaborative Recovery deprecated

The Collaborative Recovery solution, along with the associated CorDapps (LedgerSync and LedgerRecover), is deprecated in Corda 4.11 and will be removed in Corda 4.12. You are now advised to use the new recovery tools introduced in version 4.11, as detailed in the following 4.11 release notes.

### Ledger Recovery

Ledger Recovery was introduced as part of the Corda 4.11 release. It complements a standardised Corda network operational backup and recovery process.

For more information, see [Ledger Recovery]({{< relref "node/collaborative-recovery/ledger-recovery/overview.md" >}}).

### Two Phase Finality

Two Phase Finality protocol (`FinalityFlow` and `ReceiveFinalityFlow` sub-flows) has been added to improve resiliency and
recoverability of CorDapps using finality. Existing CorDapps do not require any changes to take advantage of this
new improved protocol.

For more information, see [Two Phase Finality]({{< relref "two-phase-finality.md" >}}).

### Finality Recovery Tooling

RPC extension operations (additions to the FlowRPCOps interface) that allow for Finality Flow recovery by both the initiator and the receiver(s) have been added.
Also, Node Shell commands now allow operations teams to perform Finality Flow recovery.

For more information, see [Finality Flow Recovery]({{< relref "finality-flow-recovery.md" >}})

### Ledger Recovery flow

A new ledger recovery flow (`LedgerRecoveryFlow`) enables a node to identify and recover transactions from
peer recovery nodes to which it was a party (either initiator or receiver) and which are missing from its own ledger.

For more information, see [Ledger Recovery flow parameters]({{< relref "node/collaborative-recovery/ledger-recovery/ledger-recovery-flow.md" >}}).

### Confidential Identity key-pair generator

A new service has been added that pregenerates Confidential Identity keys to be used when using CIs in transactions.
These pre-generated CIs are subsequently used for backup recovery purposes.

### Additional Network Parameters

The following network parameters, and associated node configuration parameters, have been added:

* `confidentialIdentityMinimumBackupInterval`
* `recoveryMaximumBackupInterval`

These network parameters require CENM 1.6 or later.

For more information, see [Available Network Parameters]({{< relref "network/available-network-parameters.md" >}}).

### Distribution record cleanup

A new maintenance job `DistributionRecordCleanupTask` has been added. This removes ledger recovery distribution records that are older than the `recoveryMaximumBackupInterval` network parameter, and which are no longer needed.

If the network parameter `recoveryMaximumBackupInterval` is not defined, then the node parameter `enterpriseConfiguration.ledgerRecoveryConfiguration.recoveryMaximumBackupInterval`, if defined, is used instead.

If neither parameter is defined, then the distribution record maintenance job is disabled.

For more information, see [Ledger Recovery distribution record cleanup]({{< relref "node/operating/maintenance-mode.md#ledger-recovery-distribution-record-cleanup" >}}).

### Improved double-spend exception handling

Two Phase Finality automatically deletes an unnotarized transaction from the `DBTransaction` table if a double spend
is detected upon attempting notarization by the the initiator of `FinalityFlow`.

Additionally, if the new optional `ReceiveFinalityFlow` `handlePropagatedNotaryError` constructor parameter is set to `true` (default: `false`),
then the double spend error (`NotaryError.Conflict`) propagates back to the 2PF initiator. This enables the initiator to automatically remove the associated unnotarized transaction from its `DBTransaction` table.

If a CorDapp is compiled against Corda 4.11 (that is, its target platform version = 13) then double spend handling is enabled by default. For more information, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### Deserializing AMQP data performance improvement

This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

### Detect vault changes while vault query pages loaded

A new property, `previousPageAnchor`, has been added to `Vault.Page`. It is used to detect if the vault has changed while pages of a vault query have been loaded. If such a scenario is important to detect, then the property can be used to restart querying.

An example of how to use this property can be found in [Vault Queries]({{< relref "cordapps/api-vault-query.md#query-for-all-states-using-a-pagination-specification-and-iterate-using-the-totalstatesavailable-field-until-no-further-pages-available-1" >}}).

### Upgraded dependencies

The following dependencies have been upgraded to address critical and high-severity security vulnerabilities:

#### Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final
#### H2 upgraded from 1.4.197 to 2.2.214
H2 database has been upgraded to version 2.2.224 primarily to address vulnerabilities reported in earlier versions of H2.
H2 is not a supported production database and should only be used for development and test purposes. For detailed information
regarding the differences between H2 version 1.4.197 used in previous versions of Corda, and the new H2 version 2.2.224 implemented in 4.11,
see the [H2 documentation](https://www.h2database.com/html/main.html). The most important differences are the following:

* Entity naming

  H2 version 2.2.224 implements stricter rules regarding the naming of tables and columns within the database.
  The use of SQL keywords is no longer permitted. If a CorDapp schema uses a reserved name for a table or column,
  the CorDapp's flows will fail when attempting to interact with the table, resulting in an SQL-related exception.

  The solution for this issue involves renaming the problematic table or column to a non-reserved name. This renaming
  process should be implemented in the CorDapp's migration scripts and in the JPA entity definition within the CorDapp code.

* Backwards compatibility

  H2 version 2.x is not backwards-compatible with older versions. Limited backwards compatibility can be achieved by adding
  `MODE=LEGACY` to the H2 database URL. For more information, go to the LEGACY Compatibility Mode section
  of the [H2 Features](https://www.h2database.com/html/features.html) page.

  H2 2.x is unable to read database files created by older H2 versions. The recommended approach for upgrading an older database
  involves exporting the data and subsequently re-importing it into a new version 2.x database. Further details on this
  process are outlined on the [H2 Migration to 2.0](https://www.h2database.com/html/migration-to-v2.html) page.

#### Liquibase upgraded from 3.6.3 to 4.20.0

* API

  This version of Liquibase features a slightly different API compared to the previous version. CorDapps that have implemented
  their own database migration code that uses Liquibase need to be updated to align with the new API.

* Logging

  In this version of Liquibase, all INFO-level logging is directed to STDERR, while STDOUT is used for logging SQL queries.
  Utilities that have implemented their own database migration code that uses Liquibase can establish their custom logger
  to capture Liquibase's informational logging. The Liquibase API provides classes that can be used to integrate custom loggers.

### Consuming transaction IDs added to `vault_state` table

When a state is consumed by a transaction, Corda now adds the ID of the consuming transaction in the `consuming_tx_id` column of the `vault_state` table. Corda only updates this database column for new transactions; for existing consumed states already in the ledger, the value of `consuming_tx_id` is null.

### Node configuration change for better performance

To reduce flow latency and improve throughput, the following default values in the node configuration have changed:
* `enterpriseConfiguration.tuning.brokerConnectionTtlCheckIntervalMs` changed from 20 to 1 millisecond.
* `enterpriseConfiguration.tuning.journalBufferTimeout` changed from 3333333 nanoseconds to 1000000 nanoseconds.
* `notary.extraConfig.batchTimeoutMs` changed from 200 to 1.

### DJVM removal

Beta feature of the DJVM has been removed. As a result of the DJVM removal, the two constructor parameters `djvmBootstrapSource` and `djvmCordaSource` have been removed from the `DriverParameters` class. Any client code that utilizes `DriverParameters` now requires recompiling.

### Additional signature verification

The `recordTransactions()` function now performs stricter signature verification when using public `ServiceHub` API.
For more information, see [DBTransactionStorage]({{< relref "node-services.md#dbtransactionstorage" >}}).

### CENM compatibility

Except for exceptions stated in CENM release notes, this version of Corda is compatible with all currently released versions of CENM.

## Fixed issues

This release includes the following fixes since 4.10.3:

* PostgreSQL 9.6 and 10.10 have been removed from our support matrix as they are no longer supported by PostgreSQL themselves.

* log4j2.xml now deletes the correct file for diagnostic and checkpoint logs in the rollover strategy configuration.

* In the previous patch release, while enhancing SSL certificate handling, certain log messages associated
with failed SSL handshakes were unintentionally added. These messages often appeared in the logs during connectivity tests
for traffic load balancers and system monitoring. To reduce log noise, we have now silenced these specific log messages.

## Database schema changes

For a complete description of all database tables, see [Database tables]({{< relref "node/operating/node-database-tables.md" >}}).

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
  @Table(name = "${NODE_DATABASE_PREFIX}sender_distr_recs")
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
  @Table(name = "${NODE_DATABASE_PREFIX}receiver_distr_recs")
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

  Pre-generation of confidential identities for Ledger Recovery introduces four new fields within the `node_our_key_pairs` table:

  ```bash
  @Entity
  @Table(name = "${NODE_DATABASE_PREFIX}our_key_pairs")
  class PersistentKey(

        <.... existing fields not shown .... >

        @Enumerated(EnumType.ORDINAL)
        @Column(name = "key_type", nullable = false)
        var keyType: KeyType = CI,

        @Column(name = "crypto_config_hash", length = MAX_HASH_HEX_SIZE, nullable = true)
        var cryptoConfigHash: String? = null,

        @Enumerated(EnumType.ORDINAL)
        @Column(name = "status", nullable = false)
        var status: Status = CREATED,

        @Column(name = "generate_tm", nullable = false)
        var insertionDate: Instant = Instant.now()
  )
  ```

## Third party component upgrades

The following table lists the dependency version changes between 4.10.3 and 4.11 Enterprise Editions:

| Dependency                         | Name                | Version 4.10.3 Enterprise | Version 4.11 Enterprise|
|------------------------------------|---------------------|--------------------------|------------------------|
| org.bouncycastle                   | Bouncy Castle       | bcprov-jdk15on:1.70      | bcprov-jdk18on:1.75    |
| co.paralleluniverse:quasar-core    | Quasar              | 0.7.15_r3                | 0.7.16_r3              |
| org.hibernate                      | Hibernate           | 5.4.32.Final             | 5.6.14.Final           |
| com.h2database                     | H2                  | 1.4.197                  | 2.2.2241               |
| org.liquibase                      | Liquibase           | 3.6.3                    | 4.20.0                 |

## Log4j patches

Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
