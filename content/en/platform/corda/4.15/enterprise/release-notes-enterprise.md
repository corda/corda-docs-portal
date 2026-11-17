---
title: Corda Enterprise Edition 4.15 release notes
date: '2025-03-19'

menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-release-notes
    parent: about-corda-landing-4-15-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.15 release notes

## Corda Enterprise Edition 4.15 release notes

The Corda Enterprise Edition 4.15 release upgrades the node's object-relational mapper to Hibernate ORM 7 and upgrades third-party components.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Platform version change

Corda 4.15 uses platform version 170.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### New features, enhancements and restrictions

#### Hibernate 7 and Jakarta Persistence

Corda Enterprise Edition 4.15 upgrades Hibernate ORM from version 5.6, which is end of life, to version 7.4.12. Hibernate 7 implements Jakarta Persistence 3.2, so the persistence annotations that CorDapps use for their vault schemas, and the `EntityManager` that `ServiceHub.withEntityManager` provides, move from the `javax.persistence` package to the `jakarta.persistence` package. The Hibernate upgrade itself needs no database migration, because Corda configures Hibernate 7 to read and write the formats that existing databases already use, including the single `hibernate_sequence`, UTC `TIMESTAMP` columns for `Instant`, binary `UUID` columns and `NUMBER(1)` booleans on Oracle. The 4.15 database migrations for other features still apply, as for any release.

* **CorDapps built for Corda 4.14 or earlier run without a rebuild.** The node's CorDapp class loader converts their `javax.persistence` classes to `jakarta.persistence` as it loads them, and substitutes the Hibernate 5 `@Type` names (`uuid-char`, `corda-wrapper-binary`, `corda-blob`, `yes_no`, `true_false` and others) with the Hibernate 7 mappings that store the same format. New `YesNoBooleanConverter`, `TrueFalseBooleanConverter` and `SingleCharacterConverter` converters keep the `CHAR` columns a 4.14 node used readable on every database. The jar, its hash and its signature are unchanged. The node refuses to start, naming every affected class, if a CorDapp uses a Hibernate 5 annotation, class or member that Hibernate 7 no longer has, such as `@TypeDef`, a custom `@Type` or `Session.save`. Hibernate 7's behaviour changes, such as strict HQL validation and `persist` marking the transaction for rollback on a duplicate, apply to converted CorDapps as to rebuilt ones.
* **Rebuilt CorDapps use `jakarta.persistence`.** `ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`, `@Type(type = "...")` is replaced by `@JdbcTypeCode`, and Hibernate's `Session.save`, `update` and `delete` are replaced by `persist`, `merge` and `remove`. A Gradle build that has Hibernate 5 in the same configuration as Corda 4.15 fails with a capability conflict on `hibernate-core`. A script in the Corda repository applies the package, dependency and common `@Type` changes, and lists the rest for review.
* **`database.hibernateDialect`.** Hibernate 7 removed the version-specific dialects, such as `SQLServer2012Dialect` and `Oracle12cDialect`. A node configured with one maps it to the replacement dialect and logs a warning.
* **Oracle.** Booleans stay `NUMBER(1)` on Oracle 23ai and later, and the node sets `oracle.jdbc.useFetchSizeWithLongColumn=true` so that vault queries can read `LONG RAW` columns.
* **Standalone JPA notary.** The notary uses the same compatibility settings as the node. On CockroachDB it now uses Hibernate's CockroachDB dialect unless `hibernateDialect` is set.

For what node operators and CorDapp developers need to do, see [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}).

### Third-party component upgrades

The following table lists the dependency version changes for 4.15 Enterprise Edition:

| Dependency                                   | Name                     | New Version     |
| -------------------------------------------- | ------------------------ | --------------- |
| org.hibernate.orm:hibernate-core             | Hibernate ORM            | 7.4.12.Final    |
| jakarta.persistence:jakarta.persistence-api  | Jakarta Persistence API  | 3.2.0           |
| com.zaxxer:HikariCP                          | HikariCP                 | 7.1.0           |
| org.liquibase:liquibase-core                 | Liquibase                | 4.33.0          |

## Corda Enterprise Edition 4.14.2 release notes

Corda Enterprise Edition 4.14.2 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Revert the fix to handle stuck messages in Artemis. Previously on extremely rare occasions messages could become stuck in Artemis. This has now been resolved in Artemis.
* The following table shows the vulnerabilities addressed in this patch release.

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-33870 | Netty     |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.14.2. Dependencies with unchanged versions are omitted.

| Dependency                          | Name    | Version |
|-------------------------------------|---------|--------|
| io.netty:netty-*                    | Netty   | 4.1.132.Final       |

## Corda Enterprise Edition 4.14.1 release notes

Corda Enterprise Edition 4.14.1 is a patch release of Corda Enterprise Edition focused on resolving issues and upgrading dependencies to address security updates.

### Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

### Fixed issues

* Improved error reporting in RPCClientProxyHandler, for example when the user does not have sufficient permissions to perform an operation.
* The following table shows the vulnerabilities addressed in this patch release.

|Vulnerability| Component |
|-------------|-----------|
|CVE-2026-27446| Artemis   |
|CVE-2026-1605| Jetty     |
|CVE-2025-11143| Jetty     |
| CVE-2026-24400 | AssertJ   |

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.12.10. Dependencies with unchanged versions are omitted.

| Dependency                          | Name           | Version       |
|-------------------------------------|----------------|---------------|
| com.fasterxml.jackson..*            | Jackson        | 2.18.6        |
| org.apache.activemq:artemis-*       | Artemis        | 2.52.0        |
| org.eclipse.jetty.ee10:jetty-ee10-* | Jetty          | 2.25.3        |

## Corda Enterprise Edition 4.14 release notes

The Corda Enterprise Edition 4.14 release introduces new functionality and third-party component upgrades.

## Upgrade recommendation

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

## Platform version change

Corda 4.14 uses platform version 160.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

## New features, enhancements and restrictions

### Solana notary

Corda Enterprise 4.14 introduces the Solana notary, a new notary type that records notarisation results on the
[Solana](https://solana.com/) blockchain. The Solana notary enables CorDapps to perform atomic cross-chain operations — a Corda
transaction is only notarised if a corresponding Solana program instruction (such as an SPL token transfer) also
succeeds, and vice versa. This makes it possible to build use cases such as atomic delivery-versus-payment where a
Corda asset is exchanged for a Solana-based stablecoin in a single, indivisible operation.

For more information, see [Solana notary]({{< relref "notary/solana-notary.md" >}}).

### Notary instructions

Corda 4.14 introduces `NotaryInstruction`, an extensible mechanism for attaching additional directives to a
transaction that a specialised notary can act on during notarisation. Notary instructions are stored in a new
transaction component group (`NOTARY_INSTRUCTIONS_GROUP`), are covered by the transaction's Merkle tree, and are
available to contracts for verification.

New `TransactionBuilder` and `LedgerTransaction` APIs support notary instructions:

* `TransactionBuilder.addNotaryInstruction(instruction)` — attaches a notary instruction to the transaction being
  built.
* `LedgerTransaction.notaryInstructionsOfType<T>()` — retrieves all notary instructions of a given type, allowing
  contracts to verify them.

For backwards compatibility, standard notaries reject any transaction that contains notary instructions. Only
specialised notaries — such as the Solana notary — accept and process them.

## Known issues

### Solana notary

The Solana notary program only supports a maximum `StateRef` index of 127. However, this is currently not
checked and enforced in the platform when output states are created. CorDapps must ensure they do not create more
than 128 output states in a transaction.

## Third-party component upgrades

The following table lists the dependency version changes for 4.14 Enterprise Editions:

| Dependency                               | Name         | New Version             |
| ---------------------------------------- | ------------ | ----------------------- |
| org.apache.activemq:*                    | Artemis      | 2.44.0                  |
| org.apache.commons:commons-lang3         | Commons Lang | 3.19.0                  |
| org.glassfish.jersey.*                   | Jersey       | 3.1.11                  |
| org.apache.logging.log4j:*               | Log4J        | 2.25.1                  |
| io.netty:*                               | netty        | 4.1.128.Final           |
| io.netty:netty-tcnative-boringssl-static | tcnative     | 2.0.74.Final            |
