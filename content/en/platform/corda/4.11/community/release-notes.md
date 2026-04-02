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

## Corda Community Edition 4.11.7 release notes

Corda Community Edition 4.11.7 is a patch release of Corda Community Edition focused on resolving issues and updating third-party dependencies.

### Fixed issues

* The RPC listener of a Corda node can now be protected from brute-force login attempts and abusive authentication activity. For details of this and how
  to enable it see [rateLimit]({{< relref "corda-configuration-fields.md#ratelimit" >}}).
* Extra logging has been added if a node is unable to serialise an exception.

### Third party components upgrade

The following table lists the dependency version changes in the 4.11.7 Community Edition. Dependencies with unchanged versions are omitted.

|Dependency|Name|Version|
|-----|-----|-----|
|com.github.docker-java:*|Docker Java|3.5.3|
|org.bouncycastle:bcprov-jdk18on|Bouncy Castle|1.79|
|org.eclipse.jetty:*|Jetty|9.4.57.v20241219|
|org.glassfish.jersey.*|Jersey|2.47|
|org.assertj:assertj-core|AssertJ|3.27.7|
|io.netty:netty-*|Netty|4.1.130.Final|
|net.i2p.crypto:eddsa|Crypto EddSA|(removed)|
|com.bloxbean.cardano:net-i2p-crypto-eddsa|Bloxbean EddSA|0.3.1|
|commons-io:commons-io|Commons IO|2.21.0|
|org.controlsfx:controlsfx|Controls FX|11.2.3|

## Corda Community Edition 4.11.6 release notes

Corda Community Edition 4.11.6 is a patch release of Corda Community Edition focused on resolving issues and updating third-party dependencies.

### Fixed issues

-  The Corda Network Builder Tool now correctly deploys a Corda network both via CLI in Docker and Azure environments. <!-- ENT-12147 -->

### Third party components upgrade

The following table lists the dependency version changes in the 4.11.6 Community Edition. Dependencies with unchanged versions are omitted. <!-- ENT-13978 -->

| Dependency                                            | New Version        |
|-------------------------------------------------------|--------------------|
| com.github.docker-java:docker-java                    | 3.5.1              |
| com.github.docker-java:docker-java-transport-httpclient5 | 3.5.1           |
| io.netty:tcnative*                                    | 2.0.74.Final       |
| com.fasterxml.jackson.core:jackson-annotations        | 2.17.3             |
| io.netty:*                                            | 4.1.128.Final      |
| commons-beanutils:commons-beanutils                   | 1.11.0             |
| org.apache.commons:commons-lang3                      | 3.19.0             |
| com.azure.resourcemanager:azure-resourcemanager       | 2.52.0             |
| com.azure:azure-identity                              | 1.18.1             |
 <!-- ENT-14529 -->

## Corda Community Edition 4.11.5 release notes

Corda Community Edition 4.11.5 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* When deploying a test node using DriverDSL, the node now starts successfully without encountering a `NoSuchMethodError` exception.
* You can now create two nodes with identical `O` field values but different `OU` values in their X.500 names when using the DriverDSL for testing.

### New features, enhancements and restrictions

* Contract JAR signing key rotation of R3-provided CorDapps is included in this patch release.
* Docker images are now based on Java 8 build 432.

### Third party components upgrade

The following table lists the dependency version changes between 4.11.4 and 4.11.5 Community Editions:

| Dependency                   | Name                | Version 4.11.4 Community    | Version 4.11.5 Community       |
|------------------------------|---------------------|-----------------------------|--------------------------------|
| org.eclipse.jetty:*          | Jetty               | 9.4.53.v20231009            | 9.4.56.v20240826               |
| commons-io:commons-io        | commons IO          | 2.6                         | 2.17.0                         |
| com.zaxxer:HikariCP          | Hikari              | 3.3.1                       | 4.0.3                          |

## Corda Community Edition 4.11.4 release notes

Corda Community Edition 4.11.4 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* `ReceiveFinalityFlow` was returning a transaction that was missing the notary signature. This has now been fixed. The returned transaction now includes the notary signature.
* `ReceiveTransactionFlow` was checking that the network parameters on the transaction existed before `ResolveTransactionFlow` was executed.
  This could cause a problem in certain scenarios; for example, when sending a top-level transaction to a new node in a migrated network, as the old network parameters would not exist on this new node. This has now been fixed.
* When resolving a party, in some code paths, `wellKnownPartyFromAnonymous` did not consider notaries from network parameters when trying to resolve an X.500 name. This scenario could occur when introducing a new node to a newly-migrated network as the new node would not have the old notary in its network map. This has now been fixed. Notaries from network parameters are now considered in the check.

## Corda Community Edition 4.11.3 release notes

Corda Community Edition 4.11.3 is a patch release of Corda Community Edition to keep it synchronised with the release of Corda Enterprise Edition 4.11.3.

## Corda Community Edition 4.11.2 release notes

Corda Community Edition 4.11.2 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* In the default log4j2.xml file, the Delete action in the DefaultRolloverStrategy policy for log files beginning with `diagnostic-*` or `checkpoints_agent-*`  was incorrect. It erroneously compared against the wrong file names. This issue has been rectified, ensuring that files are now deleted in accordance with the policy.
* Previously, a rare error scenario could occur where a node would erroneously perceive a valid connection to a peer when, in fact, it was not connected. This issue typically arose when the peer node was disconnecting/connecting.

### Third party component upgrades

* Jetty version was upgraded from 9.4.51.v20230217 to 9.4.53.v20231009.


## Corda Community Edition 4.11.1 release notes

Corda Community Edition 4.11.1 is a patch release of Corda Community Edition focused on resolving issues.

### Fixed issues

* Interoperability fix between 4.11 and pre-4.11 nodes when sending/fetching transactions for new data type: `TRANSACTION_RECOVERY`.

## Corda Community Edition 4.11 release notes

Corda Community Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features and enhancements

### JDK Azul and Oracle JDK upgrade

Corda now supports JDK Azul 8u382 and Oracle JDK 8u381.

### Two Phase Finality

Two Phase Finality protocol (`FinalityFlow` and `ReceiveFinalityFlow` sub-flows) has been added to improve resiliency and recoverability of CorDapps using finality. Existing CorDapps do not require any changes to take advantage of this new improved protocol. The recovery flows that take advantage of this new protocol are present only in the Corda Enterprise edition.

### Upgraded dependencies

The following dependencies have been upgraded to address critical and high-severity security vulnerabilities:

#### Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final
#### H2 upgraded from 1.4.199 to 2.2.214
H2 database has been upgraded to version 2.2.224 primarily to address vulnerabilities reported in earlier versions of H2.
H2 is not a supported production database and should only be used for development and test purposes. For detailed information
regarding the differences between H2 version 1.4.199 used in previous versions of Corda, and the new H2 version 2.2.224 implemented in 4.11,
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

The DJVM component required that all updates to Corda core were compatible with the `core-deterministic` module.
To mitigate this issue, the experimental component DJVM has been removed from this and all future releases.
As a result of the DJVM removal, the two constructor parameters `djvmBootstrapSource` and `djvmCordaSource` have been
removed from the `DriverParameters` class. Any client code that utilizes `DriverParameters` now requires recompiling.

## Fixed issues

This release includes the following fixes since 4.10.3:

* PostgreSQL 9.6 and 10.10 have been removed from our support matrix as they are no longer supported by PostgreSQL themselves.

* log4j2.xml now deletes the correct file for diagnostic and checkpoint logs in the rollover strategy configuration.

* In the previous patch release, while enhancing SSL certificate handling, certain log messages associated
  with failed SSL handshakes were unintentionally added. These messages often appeared in the logs during connectivity tests
  for traffic load balancers and system monitoring. To reduce log noise, we have now silenced these specific log messages.

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

## Third party component upgrades

The following table lists the dependency version changes between 4.10.3 and 4.11 Community Editions:

| Dependency                         | Name                | Version 4.10.3 Community | Version 4.11 Community |
|------------------------------------|---------------------|--------------------------|------------------------|
| org.bouncycastle                   | Bouncy Castle       | bcprov-jdk15on:1.70      | bcprov-jdk18on:1.75    |
| co.paralleluniverse:quasar-core    | Quasar              | 0.7.15_r3                | 0.7.16_r3              |
| org.hibernate                      | Hibernate           | 5.4.32.Final             | 5.6.14.Final           |
| com.h2database                     | H2                  | 1.4.197                  | 2.2.2241               |
| org.liquibase                      | Liquibase           | 3.6.3                    | 4.20.0                 |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.
