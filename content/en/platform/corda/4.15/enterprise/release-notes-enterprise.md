---
title: Corda Enterprise Edition 4.15 release notes
date: '2026-11-24'

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

The Corda Enterprise Edition 4.15 release introduces cross-provider key rotation and new node metrics, upgrades the node's object-relational mapper to Hibernate ORM 7, and upgrades third-party components.

### Upgrade recommendation

{{< important >}}
**The Corda platform version has changed to 170 in this release (from 161 in Corda 4.14.4, and from 160 in earlier 4.14 releases). You must drain the node of all flows before you upgrade to Corda Enterprise Edition 4.15.**

Checkpoints created by an earlier version of Corda are not compatible with 4.15, and the node rejects them on startup. Before you upgrade, make sure there are no running, paused, or hospitalized flows on the node. Allow any remaining flows to complete, or safely kill them. For more information, see [Drain the node]({{< relref "minor-version-node-upgrade.md#step-1-drain-the-node" >}}) and [Troubleshooting stuck flows]({{< relref "node/operating/monitoring-and-logging/diagnosing-stuck-flows.md" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Enterprise release notes are on this page, and for the latest upgrade guide, refer to [Upgrading a CorDapp or node]({{< relref "upgrading-index.md" >}}).

Before you upgrade:

* Read [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}), and start a 4.15 test node with your CorDapps to check that they load and their flows run.
* Run the database update for 4.15. The Hibernate upgrade itself changes no tables, but 4.15 adds the `node_cross_provider_key_rotation_proof` table for key rotation.
* If you use the Archive Service, upgrade it to version 2.0.1 or later first. Archive Service 2.0 and earlier refer to Hibernate 5 classes, and a 4.15 node refuses to load them. See the [Archive Service release notes]({{< relref "../../../../tools/archiving-service/archiving-release-notes.md" >}}).

### Platform version change

Corda 4.15 uses platform version 170.

For more information about platform versions, see [Versioning]({{< relref "cordapps/versioning.md" >}}).

### New features, enhancements and restrictions

#### Cross-provider key rotation

Corda Enterprise Edition 4.15 introduces cross-provider key rotation, which moves a node's or notary's legal identity key to a different key provider without losing access to the states and transactions it already holds. The supported moves are from a file-based keystore to an HSM, from an HSM to a file-based keystore, and from one HSM to another.

The [HA Utilities]({{< relref "ha-utilities.md" >}}) tool generates the new key in the new provider and creates a *key rotation proof*: a signature by the old key over the new public key. After the rotation, the node no longer signs with the old key. It signs for its existing states with the new key, and transactions that consume states signed with the old key carry the proof chain, which every verifier checks together with the transaction signatures. The proofs add a small, fixed overhead to such transactions; once every state signed with the old key has been consumed, new transactions no longer need them.

Corda Enterprise Edition 4.15 supports three key rotation operations:

* **Same-provider key rotation**, available since Corda Enterprise 4.7, reissues a node's or notary's legal identity key within the same key provider.
* **Cross-provider key rotation** (new) moves a node's or notary's legal identity key to a different key provider. It supports standalone notaries and the workers of an HA notary cluster. Raft, BFT-SMaRt and Solana notaries cannot be rotated across key providers.
* **Confidential identity cross-provider key rotation** (new) moves a node's wrapped confidential identity keys to a different key provider, using the same proof mechanism.

Before you rotate a key:

* Every node on the network must run Corda 4.15 or later, and the network minimum platform version must be 170. If it is lower, the rotation tool fails, a 4.15 node with a key rotation file refuses to start, and a transaction builder rejects commands with key rotation proofs.
* Key rotation must be enabled in the CENM Identity Manager service (`allowKeyRotation = true` in the `identity-manager-alias` workflow) for the duration of the rotation, and disabled again afterwards.
* Every CorDapp on every node of the network must support key rotation, not only the CorDapps on the rotated node. A party is identified by its public key, so a CorDapp that compares parties, keys or certificates directly, or looks up states by party, may stop working for the rotated node's states until it is updated. The new `PartyIdentityResolver` API resolves a party recorded before a rotation to its current identity.
* A rotation cannot be reversed. Rehearse it in a test environment and take verified backups of the node database, the node directory and its keystores first.

Corda Open Source Edition 4.15 nodes can verify transactions that contain key rotation proofs, so they keep transacting with Corda Enterprise nodes that have rotated their keys, but they cannot rotate their own keys across providers.

The platform flows support rotated keys: `CollectSignaturesFlow` takes the keys in a key rotation proof into account, and `CashExitFlow` and the `OnLedgerAsset` helpers in the finance CorDapp work with rotated identity and notary keys. To test a CorDapp against a rotated key, create a `MockNetwork` with the new `MockNetworkParameters.enterpriseNodes` option and a network minimum platform version of 170, and call the new `MockNetwork.rotateKey` function.

For more information, see [Key rotation]({{< relref "node/key-rotation.md" >}}), [Cross-provider key rotation]({{< relref "node/cross-provider-key-rotation/cross-provider-key-rotation.md" >}}) and [Confidential identity cross-provider key rotation]({{< relref "node/cross-provider-key-rotation/confidential-identity-cross-provider-key-rotation.md" >}}).

#### Hibernate 7 and Jakarta Persistence

Corda Enterprise Edition 4.15 upgrades Hibernate ORM from version 5.6, which is end of life, to version 7.4.12. Hibernate 7 implements Jakarta Persistence 3.2, so the persistence annotations that CorDapps use for their vault schemas, and the `EntityManager` that `ServiceHub.withEntityManager` provides, move from the `javax.persistence` package to the `jakarta.persistence` package. The Hibernate upgrade itself needs no database migration, because Corda configures Hibernate 7 to read and write the formats that existing databases already use, including the single `hibernate_sequence`, UTC `TIMESTAMP` columns for `Instant`, binary `UUID` columns, `NUMBER(1)` booleans on Oracle and non-nationalised `VARCHAR` columns where Corda 4.14 used them on Oracle and SQL Server. The 4.15 database migrations for other features still apply, as for any release.

* **CorDapps built for Corda 4.14 or earlier run without a rebuild.** The node's CorDapp class loader converts their `javax.persistence` classes to `jakarta.persistence` as it loads them, and substitutes the Hibernate 5 `@Type` names (`uuid-char`, `corda-wrapper-binary`, `corda-blob`, `yes_no`, `true_false` and others) with the Hibernate 7 mappings that store the same format. New `YesNoBooleanConverter`, `TrueFalseBooleanConverter` and `SingleCharacterConverter` converters keep the `CHAR` columns a 4.14 node used readable on every database. The jar, its hash and its signature are unchanged, so contract constraints are not affected. The node logs one line per converted CorDapp.
* **Contract attachments are converted too.** The classes of contract attachments built for Corda 4.14 or earlier are converted in the same way when a transaction is verified, in the node and in the external verifier, so their contracts, and the transactions already on the ledger that use them, keep verifying.
* **The node refuses CorDapps that Hibernate 7 cannot run.** If a CorDapp uses a Hibernate 5 annotation, class or member that Hibernate 7 no longer has, such as `@TypeDef`, a custom `@Type`, or `Session.save`, `update` and `delete`, the node refuses to start and lists every affected class and member at once. Start a 4.15 test node with your CorDapps before upgrading production to find them. If a CorDapp cannot be rebuilt and you accept that such code fails only when it runs, the JVM option `-Dnet.corda.cordapp.missingHibernateReferences=warn` turns the class and member check into warnings; the annotation check cannot be turned off.
* **Hibernate 7 behaviour changes apply to converted and rebuilt CorDapps alike.** HQL and JPQL are validated strictly, and a query that refers to a column name instead of an attribute name is rejected with `SemanticException`. `persist` of a duplicate entity marks the transaction for rollback. Native queries return `Long` where they returned `BigInteger`. `LIKE` patterns no longer treat a backslash as an escape character on H2 and PostgreSQL. `NOT IN` an empty list now matches every row. On SQL Server, an `IN` list of more than 2,100 numeric values now fails, because each value is bound as a parameter. A query without `ORDER BY` can return rows in a different order. Run the flows of every CorDapp on a 4.15 test node before relying on them in production.
* **Rebuilt CorDapps use `jakarta.persistence`.** `ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`, `@Type(type = "...")` is replaced by `@JdbcTypeCode`, and Hibernate's `Session.save`, `update` and `delete` are replaced by `persist`, `merge` and `remove`. The `tools/scripts/migrate-cordapp-to-hibernate7.sh` script in the Corda repository applies the package, dependency and common `@Type` changes, and lists the rest for review. A Gradle build that has Hibernate 5 in the same configuration as Corda 4.15 fails with a capability conflict on `hibernate-core`. On Oracle and SQL Server, map `uuid-char` and `string` columns with `@JdbcTypeCode(Types.VARCHAR)` rather than a JPA `AttributeConverter`, which would nationalise the column.
* **CorDapps that must run on 4.14 and 4.15.** A CorDapp can be built once for both lines by carrying both sets of annotations, as Tokens SDK 1.3.5 does. Earlier Tokens SDK versions bind `withEntityManager` to `javax.persistence`, which fails in a 4.15 `MockNetwork`, `MockServices` or in-process driver node with `NoClassDefFoundError: javax/persistence/EntityManager`, although they run on a real 4.15 node.
* **`database.hibernateDialect`.** Hibernate 7 removed the version-specific dialects, such as `SQLServer2012Dialect`, `Oracle12cDialect` and `PostgreSQL95Dialect`. A node configured with one maps it to the replacement dialect and logs a warning. Remove the setting when convenient: Hibernate detects the database and its version itself.
* **Oracle.** Booleans stay `NUMBER(1)` on Oracle 23ai and later, and the node sets `oracle.jdbc.useFetchSizeWithLongColumn=true` so that vault queries can read `LONG RAW` columns.
* **Standalone JPA notary.** The notary uses the same compatibility settings as the node. On CockroachDB it now uses Hibernate's CockroachDB dialect unless `hibernateDialect` is set, so a serialisation conflict in the middle of a transaction is retried instead of failing the whole batch.
* **Databases.** Hibernate 7.4 raised the minimum database versions it supports, and the minimum supported CockroachDB version for the standalone JPA notary is now 24.3. Hibernate logs a warning (`HHH000511`) at start-up for an older database and carries on, so upgrade the database before the node. See the [platform support matrix]({{< relref "platform-support-matrix.md" >}}).

For what node operators and CorDapp developers need to do, see [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}).

#### New node metrics

Corda Enterprise Edition 4.15 adds node metrics that make common operational problems visible:

* **Node status:** `Node.Mode` (`NORMAL`, `DRAINING` or `READ_ONLY`), `Node.PlatformVersion`, `Node.ReleaseVersion`, `Node.Revision`, `Node.StartTime`, `Node.UptimeSeconds` and `Node.StartupDurationSeconds`.
* **Certificate expiry:** the alias, serial number and days to expiry of the node's legal identity, node CA and TLS certificates, for example `Certificates.TLS.DaysToExpiry`.
* **Flows:** `Flows.Paused`, and `Flows.WaitingOnNotary.Count` and `Flows.WaitingOnNotary.MaxAgeSeconds`, which show a slow or unreachable notary.
* **Notarisation rejections:** `Transaction.NotarisationRejected.Conflict`, `TimeWindowInvalid`, `TransactionInvalid`, `General` and `Other`.
* **Scheduler health:** `NodeSchedulerService.ConsecutiveDatabaseFailures`, `DatabaseFailures` and `MillisStalled`, which show when the node's scheduler can no longer run scheduled flows, for example during a database outage.

For more information, see [Node metrics]({{< relref "node/operating/monitoring-and-logging/node-metrics.md" >}}).

#### Warning when RPC runs without TLS

The node now prints a warning at start-up when its RPC port accepts connections without TLS, because RPC usernames and passwords are then sent over the network in clear text. The warning also calls out an `rpcSettings.ssl` block that is ignored because `rpcSettings.useSsl` is not `true`. No warning is printed for a node that uses a standalone RPC broker, where TLS is configured on the broker. The node's TLS transports were hardened at the same time: a TLS transport that is missing its key store or trust store now fails instead of falling back to plain text, and P2P connections always use mutual TLS. To enable TLS for RPC, see [Configuring wire security]({{< relref "node/operating/clientrpc.md#configuring-wire-security" >}}).

#### Docker image hardening

The Corda Enterprise Docker images have been hardened following a penetration test. Their default behaviour is unchanged, so existing deployments and scripts keep working.

* The base images are pinned by digest and use JDK 17.0.21.1 (Azul Zulu on Ubuntu and Alpine, Amazon Corretto on Amazon Linux), which fixes CVE-2026-114938. The OS packages are upgraded at build time, and setuid and setgid bits are removed.
* The node runs as the non-root `corda` user with the fixed UID and GID `1000:1000` in every variant, so Kubernetes `runAsNonRoot: true` works without `runAsUser`. The images support `--cap-drop ALL` and `--security-opt no-new-privileges`.
* The Corda binaries and the licence files are owned by `root` and are read-only. The `persistence`, `artemis` and `certificates` folders have mode `750`, and Corda is unpacked from `corda.jar` on every start, so changes to the unpacked copy do not survive a restart.
* The images declare their data folders as volumes, and the `cordapps`, `drivers` and configuration folders can be mounted read-only.
* A new health check reports the container as healthy once the node listens on its RPC port. If `rpcSettings.address` does not use the default port `10201`, set `CORDA_HEALTHCHECK_PORT`; otherwise the container is reported as unhealthy, which Docker Swarm acts on.

A read-only root file system is not supported yet. For more information, see [Corda Enterprise Docker image]({{< relref "docker-image.md" >}}).

### Platform and dependency changes

* **Java and Kotlin are unchanged.** Corda 4.15 runs on Java 17 and is built with Kotlin 1.9.20, as Corda 4.14 is. The Gradle version used to build CorDapps is unchanged.
* **Hibernate ORM 7.4.12 and Jakarta Persistence API 3.2.0** replace Hibernate ORM 5.6.15 and `javax.persistence-api` 2.2. Hibernate 7 is published as `org.hibernate.orm:hibernate-core`, where Hibernate 5 was `org.hibernate:hibernate-core`. Declare it as `cordaProvided` or compile-only if your CorDapp refers to Hibernate classes directly. See [Hibernate 7 and Jakarta Persistence](#hibernate-7-and-jakarta-persistence) above.
* **HikariCP 7.1.0** replaces HikariCP 5.1.0 for the node's database connection pool.
* **Liquibase 4.33.0** replaces Liquibase 4.20.0. It records the checksums of the changesets it applies in a new format and leaves the checksums of the changesets the database already has as they are, so the changelog table holds both formats after the upgrade. Liquibase's analytics are disabled.
* **H2 2.4.240** replaces H2 2.2.224 for development nodes. Existing H2 database files open without conversion. H2 2.5.x is deliberately not used, because it can lose committed data when the JVM exits without closing the database.
* **JDBC drivers.** The platform support matrix lists newer JDBC driver versions for SQL Server, Oracle and PostgreSQL.
* **Jetty 12.1.14** replaces Jetty 12.0.38, and **Jackson 2.22.4** replaces Jackson 2.21.7.
* **Artemis 2.57.0, Netty 4.1.139.Final and Quasar 0.9.3_r3** are used, as in Corda 4.14.4 apart from a Netty patch release.
* **Metrics collector and log tracer.** The metrics collector moves to Drools 7.74.1, and the log tracer moves to Jaeger 1.8.1.

For the full list, see [Third-party components upgrade](#third-party-components-upgrade).

### API changes

* **`ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`.** A CorDapp rebuilt for 4.15 must bind the block to the `jakarta.persistence` type. A CorDapp built for 4.14 or earlier is converted by the node and keeps working unchanged. The API checker does not report this change, because the recorded signature has no type parameters.
* **`Command`, `CommandWithParties` and `SignatureMetadata` have a new nullable property** for key rotation proofs. Their existing constructors are kept, but their `copy` methods now take the new property, so a CorDapp built for 4.14 or earlier that calls `copy` on one of these classes must be rebuilt against 4.15.
* **New key rotation APIs:** the `net.corda.core.crypto.keyrotation.crossprovider` package (`KeyRotationProof`, `KeyRotationProofChain`, `PartyIdentityResolver` and `PartyIdentityResolved`), `IdentityService.isKeyRotated`, `getProofChain` and `containsProofChain`, `KeyManagementService.isKeyRotated`, `hasRotatedKeys` and `rotatedKeys`, and, for testing, `MockNetworkParameters.enterpriseNodes` and `MockNetwork.rotateKey`.

### Fixed issues

* Fixed an issue where node registration with a Utimaco HSM failed with `CryptoServer Error B90C0103` when newer Utimaco JCE drivers were used. The bundled Utimaco JCE provider is upgraded to version 6.3.0. The new optional `additionalHosts` setting in the Utimaco configuration takes further addresses of the HSM, so that the driver reconnects on its own after an HSM restart or a network break.
* Fixed an issue where the Transaction Validator Utility failed to verify transactions created before Corda 4, which have no network parameters hash, and transactions that spend their outputs, with `UninitializedPropertyAccessException`. The utility now handles them as the node does. It also no longer fails to write its error zip with `ZipException: duplicate entry`, no longer prints each stack trace three times, and no longer leaves a partial zip behind.
* Fixed an issue where the Transaction Validator Utility did not stop when the node's network parameters file was missing or unreadable, and went on to fail the remaining transactions. It now stops at the first such error.
* Artemis's built-in message duplicate detection, which had been turned off since Corda Enterprise 4.13, is turned back on, as in Corda Enterprise 4.12 and Corda Open Source. The node's own de-duplication of messages was not affected.
* Fixed an issue where a flow restored from a checkpoint could fail when telemetry was enabled: with a `NullPointerException` if a telemetry component had been enabled after the checkpoint was written, or with an `IndexOutOfBoundsException` when span start and end events were enabled (`spanStartEndEventsEnabled`).
* The following vulnerabilities in dependencies have been addressed:

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-112046 | ASM |
| CVE-2026-116486 | Objenesis |
| CVE-2026-114938 | JDK in the Corda Enterprise Docker images |

### Known issues

#### Solana notary

The Solana notary program only supports a maximum `StateRef` index of 127. However, this is currently not
checked and enforced in the platform when output states are created. CorDapps must ensure they do not create more
than 128 output states in a transaction.

#### CVE-2026-92877 in jaxb-core

Corda 4.15 includes `org.glassfish.jaxb:jaxb-core` 4.0.7, which Hibernate ORM 7.4.12 depends on and which is affected by CVE-2026-92877 (XML external entity processing). R3 has assessed that the vulnerability cannot be exploited in Corda: Corda does not use JAXB, Hibernate reads its mapping and configuration XML through a path that is not affected, and the only affected component is used for XML-typed columns, which Corda does not have. The Corda Enterprise firewall does not include JAXB. No fixed version of `jaxb-core` has been released yet. R3 will upgrade it in a future release.

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Enterprise Edition 4.15 since Corda Enterprise Edition 4.14.4. Dependencies with unchanged versions, build and test tools, and JDBC drivers, which you supply yourself, are omitted.

| Dependency | Name | 4.14.4 Enterprise | 4.15 Enterprise |
| ---------- | ---- | ----------------- | --------------- |
| org.hibernate.orm:hibernate-core | Hibernate ORM | 5.6.15.Final (org.hibernate:hibernate-core) | 7.4.12.Final |
| jakarta.persistence:jakarta.persistence-api | Jakarta Persistence API | 2.2 (javax.persistence:javax.persistence-api) | 3.2.0 |
| com.zaxxer:HikariCP | HikariCP | 5.1.0 | 7.1.0 |
| org.liquibase:liquibase-core | Liquibase | 4.20.0 | 4.33.0 |
| com.h2database:h2 | H2 | 2.2.224 | 2.4.240 |
| net.bytebuddy:byte-buddy | Byte Buddy | 1.12.18 (transitive) | 1.18.8 |
| org.ow2.asm:asm\* | ASM | 9.5 | 9.11.1 |
| org.objenesis:objenesis | Objenesis | 3.3 (transitive) | 3.6 |
| com.rabbitmq:amqp-client | RabbitMQ AMQP client | 5.16.1 (transitive) | 5.37.0 |
| com.azure:azure-identity | Azure Identity | 1.18.3 | 1.18.7 |
| com.azure.resourcemanager:azure-resourcemanager | Azure Resource Manager | 2.62.0 | 2.65.0 |
| com.azure:azure-security-keyvault-keys | Azure Key Vault Keys | 4.10.6 | 4.11.3 |
| com.github.ben-manes.caffeine:caffeine | Caffeine | 3.2.3 | 3.3.0 |
| io.github.classgraph:classgraph | ClassGraph | 4.8.135 | 4.8.143 |
| org.apache.commons:commons-collections4 | Commons Collections | 4.3 | 4.6.0 |
| org.apache.commons:commons-configuration2 | Commons Configuration | 2.15.0 | 2.15.1 |
| org.apache.commons:commons-dbcp2 | Commons DBCP | 2.12.0 (transitive) | 2.14.0 |
| commons-io:commons-io | Commons IO | 2.21.0 | 2.22.0 |
| org.apache.commons:commons-lang3 | Commons Lang | 3.19.0 | 3.21.0 |
| org.apache.commons:commons-text | Commons Text | 1.10.0 (transitive) | 1.15.0 |
| com.lmax:disruptor | Disruptor | 3.4.2 | 4.0.0 |
| org.drools:drools-\*, org.kie:kie-api | Drools (metrics collector) | 6.0.1.Final | 7.74.1.Final |
| com.google.code.gson:gson | Gson | 2.8.9 | 2.14.0 |
| com.google.guava:guava | Guava | 33.1.0-jre | 33.7.2-jre |
| org.apache.httpcomponents.core5:httpcore5-h2 | Apache HttpCore 5 H2 | 5.3.6 (transitive) | 5.4.4 |
| com.fasterxml.jackson.\* | Jackson | 2.21.7 | 2.22.4 |
| io.jaegertracing:jaeger-\* | Jaeger (log tracer) | 0.30.3 | 1.8.1 |
| org.apache.thrift:libthrift | libthrift (log tracer) | 0.11 (shaded in Jaeger) | 0.25.0 |
| org.fusesource.jansi:jansi | Jansi | 1.18 | 2.4.3 |
| org.javassist:javassist | Javassist | 3.29.2-GA | 3.33.0-GA |
| com.jcabi:jcabi-manifests | jcabi-manifests | 1.1 | 2.2.0 |
| org.glassfish.jersey.\* | Jersey | 3.1.11 | 3.1.12 |
| org.eclipse.jetty.ee10:jetty-ee10-\* | Jetty | 12.0.38 | 12.1.14 |
| org.jolokia:jolokia-jvm | Jolokia | 1.6.1 | 1.6.2 |
| net.sf.jopt-simple:jopt-simple | JOpt Simple | 5.0.2 | 5.0.4 |
| com.jayway.jsonpath:json-path | JsonPath | 2.9.0 (transitive) | 2.10.0 |
| net.minidev:json-smart | json-smart | 2.5.2 | 2.6.0 |
| com.esotericsoftware:kryo | Kryo | 5.5.0 | 5.7.1 |
| de.javakaffee:kryo-serializers | Kryo serializers | 0.43 | 0.45 |
| org.jetbrains.lets-plot:lets-plot-batik | Lets-Plot Batik | 4.7.0 (transitive) | 4.11.0 |
| org.apache.logging.log4j:\* | Log4j | 2.25.5 | 2.26.1 |
| io.netty:netty-\* | Netty | 4.1.138.Final | 4.1.139.Final |
| io.netty:netty-tcnative-boringssl-static | Netty TCNative | 2.0.74.Final | 2.0.84.Final |
| com.nimbusds:nimbus-jose-jwt | Nimbus JOSE + JWT | 10.0.2 | 10.10 |
| io.opentelemetry:opentelemetry-\* | OpenTelemetry | 1.63.0 | 1.67.0 |
| io.opentelemetry.semconv:opentelemetry-semconv | OpenTelemetry semantic conventions | 1.41.1 | 1.44.0 |
| io.opentracing:opentracing-\* | OpenTracing | 0.31.0 | 0.33.0 |
| org.apache.shiro:shiro-core | Shiro | 3.0.0 | 3.0.1 |
| org.slf4j:\* | SLF4J | 2.0.12 | 2.0.20 |
| org.yaml:snakeyaml | SnakeYAML | 2.2 | 2.7 |
| org.springframework:spring-jdbc | Spring JDBC | 6.2.11 | 6.2.19 |
| org.apache.sshd:sshd-\* | Apache SSHD | 2.13.2 | 2.20.0 |
| org.apache.tika:tika-core | Apache Tika | 3.2.3 (transitive) | 3.3.2 |
| com.typesafe:config | Typesafe Config | 1.3.4 | 1.4.9 |
| Utimaco CryptoServer JCE provider | Utimaco JCE | Bundled earlier version | 6.3.0 |
