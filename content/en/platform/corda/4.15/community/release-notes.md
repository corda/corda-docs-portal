---
title: Corda Open Source Edition 4.15 release notes
date: '2026-11-24'
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.ht3
menu:
  corda-community-4-15:
    identifier: corda-community-4-15-release-notes
    parent: about-corda-landing-4-15-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Open Source Edition 4.15 release notes

## Corda Open Source Edition 4.15 release notes

The Corda Open Source Edition 4.15 release upgrades the node's object-relational mapper to Hibernate ORM 7, adds support for verifying transactions signed with a rotated key, and upgrades third-party components.

### Upgrade recommendation

{{< important >}}
**The Corda platform version has changed to 170 in this release (from 161 in Corda 4.14.4, and from 160 in earlier 4.14 releases). You must drain the node of all flows before you upgrade to Corda Open Source Edition 4.15.**

Checkpoints created by an earlier version of Corda are not compatible with 4.15, and the node rejects them on startup. Before you upgrade, make sure there are no running, paused, or hospitalized flows on the node. Allow any remaining flows to complete, or safely kill them. For more information, see [Draining mode]({{< relref "key-concepts-node.md#draining-mode" >}}).
{{< /important >}}

As a developer or node operator, you should upgrade to the [latest released version of Corda]({{< relref "_index.md" >}}) as soon as possible. The latest Corda Open Source release notes are on this page, and for the latest upgrade guide, refer to [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) and [Upgrading your node]({{< relref "node-upgrade-notes.md" >}}).

Corda 4.15 moves from Hibernate 5 to Hibernate 7. Before you upgrade, read [Hibernate 7 and Jakarta Persistence in Corda Open Source Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}), and start a 4.15 test node with your CorDapps to check that they load and their flows run.

### Platform version change

Corda 4.15 uses platform version 170.

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

### New features, enhancements and restrictions

#### Hibernate 7 and Jakarta Persistence

Corda Open Source Edition 4.15 upgrades Hibernate ORM from version 5.6, which is end of life, to version 7.4.12. Hibernate 7 implements Jakarta Persistence 3.2, so the persistence annotations that CorDapps use for their vault schemas, and the `EntityManager` that `ServiceHub.withEntityManager` provides, move from the `javax.persistence` package to the `jakarta.persistence` package. The Hibernate upgrade itself needs no database migration, because Corda configures Hibernate 7 to read and write the formats that existing databases already use, including the single `hibernate_sequence`, UTC `TIMESTAMP` columns for `Instant` and binary `UUID` columns. Corda Open Source Edition 4.15 adds no other changesets either.

* **CorDapps built for Corda 4.14 or earlier run without a rebuild.** The node's CorDapp class loader converts their `javax.persistence` classes to `jakarta.persistence` as it loads them, and substitutes the Hibernate 5 `@Type` names (`uuid-char`, `corda-wrapper-binary`, `corda-blob`, `yes_no`, `true_false` and others) with the Hibernate 7 mappings that store the same format. New `YesNoBooleanConverter`, `TrueFalseBooleanConverter` and `SingleCharacterConverter` converters keep the `CHAR` columns a 4.14 node used readable. The jar, its hash and its signature are unchanged, so contract constraints are not affected. The node logs one line per converted CorDapp.
* **Contract attachments are converted too.** The classes of contract attachments built for Corda 4.14 or earlier are converted in the same way when a transaction is verified, in the node and in the external verifier, so their contracts, and the transactions already on the ledger that use them, keep verifying.
* **The node refuses CorDapps that Hibernate 7 cannot run.** If a CorDapp uses a Hibernate 5 annotation, class or member that Hibernate 7 no longer has, such as `@TypeDef`, a custom `@Type`, or `Session.save`, `update` and `delete`, the node refuses to start and lists every affected class and member at once. Start a 4.15 test node with your CorDapps before upgrading production to find them. If a CorDapp cannot be rebuilt and you accept that such code fails only when it runs, the JVM option `-Dnet.corda.cordapp.missingHibernateReferences=warn` turns the class and member check into warnings; the annotation check cannot be turned off.
* **Hibernate 7 behaviour changes apply to converted and rebuilt CorDapps alike.** HQL and JPQL are validated strictly, and a query that refers to a column name instead of an attribute name is rejected with `SemanticException`. `persist` of a duplicate entity marks the transaction for rollback. Native queries return `Long` where they returned `BigInteger`. `LIKE` patterns no longer treat a backslash as an escape character on H2 and PostgreSQL. `NOT IN` an empty list now matches every row. An entity attribute of an array type such as `IntArray` is mapped to the database's array type, so a column created before 4.15 fails validation, and a `Byte[]` or `Character[]` attribute is refused at start-up. A query without `ORDER BY` can return rows in a different order. Run the flows of every CorDapp on a 4.15 test node before relying on them in production.
* **Rebuilt CorDapps use `jakarta.persistence`.** `ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`, `@Type(type = "...")` is replaced by `@JdbcTypeCode`, and Hibernate's `Session.save`, `update` and `delete` are replaced by `persist`, `merge` and `remove`. The `tools/scripts/migrate-cordapp-to-hibernate7.sh` script in the Corda repository applies the package, dependency and common `@Type` changes, and lists the rest for review. A Gradle build that has Hibernate 5 in the same configuration as Corda 4.15, for example through a dependency on an older `corda-core`, fails with a capability conflict on `hibernate-core`.
* **Testing.** `MockNetwork`, `MockServices` and in-process driver nodes do not convert CorDapps, because the CorDapp's classes are on the test classpath. A CorDapp built for 4.14 that binds `withEntityManager` to `javax.persistence.EntityManager` fails there with `NoClassDefFoundError: javax/persistence/EntityManager`. Port your own CorDapp, and test unported third-party CorDapp jars on out-of-process driver nodes, which convert them as a real node does.
* **Databases.** Hibernate 7.4 raised the minimum database versions it supports. Hibernate logs a warning (`HHH000511`) at start-up for an older database and carries on, so upgrade the database before the node. See the [platform support matrix]({{< relref "release-platform-support-matrix.md" >}}).

For what node operators and CorDapp developers need to do, see [Hibernate 7 and Jakarta Persistence in Corda Open Source Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}).

#### Verifying transactions signed with a rotated key

Corda Enterprise Edition 4.15 introduces cross-provider key rotation, which moves a node's or notary's legal identity key to a different key provider, such as from a file-based keystore to an HSM. After a rotation, the node signs for its existing states with the new key and a *key rotation proof*: a signature by the old key over the new one. Transactions that consume states signed with the old key carry the proof chain.

A Corda Open Source Edition node cannot rotate its own key across providers, but a 4.15 node verifies transactions that contain key rotation proofs, so it can transact with Corda Enterprise nodes that have rotated their keys. Key rotation requires every node on the network to run Corda 4.15 or later and a network minimum platform version of 170. For more information, see [Cross-provider key rotation]({{< relref "../enterprise/node/cross-provider-key-rotation/cross-provider-key-rotation.md" >}}).

New public APIs support key rotation:

* The `net.corda.core.crypto.keyrotation.crossprovider` package: `KeyRotationProof`, `KeyRotationProofChain`, and `PartyIdentityResolver` and `PartyIdentityResolved`, which resolve a `Party` recorded before a rotation to the party's current identity, so that CorDapps can compare parties across a rotation.
* `IdentityService.isKeyRotated`, `getProofChain` and `containsProofChain`, and `KeyManagementService.isKeyRotated`, `hasRotatedKeys` and `rotatedKeys`.
* A nullable `keyRotationProofChainMap` property on `Command` and `CommandWithParties`, and a nullable `proofChain` property on `SignatureMetadata`.

`CollectSignaturesFlow` takes the keys in a key rotation proof into account when it checks that all required signatures are present, and the `OnLedgerAsset` helpers in the finance CorDapp support notaries that have rotated their keys.

A CorDapp that compares parties, keys or certificates directly, or looks up states by party, may stop working for a rotated node's states until it is updated. Before any node on a network rotates its key, check that every CorDapp on every node supports key rotation.

#### Node scheduler metrics

New metrics under `net.corda.NodeSchedulerService` show when the node's scheduler can no longer run scheduled flows, for example during a database outage: `ConsecutiveDatabaseFailures`, `DatabaseFailures` and `MillisStalled`. For more information, see [Node administration]({{< relref "node-administration.md" >}}).

#### Warning when RPC runs without TLS

The node now prints a warning at start-up when its RPC port accepts connections without TLS, because RPC usernames and passwords are then sent over the network in clear text. The warning also calls out an `rpcSettings.ssl` block that is ignored because `rpcSettings.useSsl` is not `true`. The node's TLS transports were hardened at the same time: a TLS transport that is missing its key store or trust store now fails instead of falling back to plain text, and P2P connections always use mutual TLS. To enable TLS for RPC, see [Configuring wire security]({{< relref "clientrpc.md#configuring-wire-security" >}}).

#### Docker image hardening

The Corda Open Source Docker images have been hardened following a penetration test. Their default behaviour is unchanged, so existing deployments and scripts keep working.

* The base images are pinned by digest and use Azul Zulu 17.0.21.1, which fixes CVE-2026-114938. The OS packages are upgraded at build time, and setuid and setgid bits are removed.
* The node runs as the non-root `corda` user with the fixed UID and GID `1000:1000`, so Kubernetes `runAsNonRoot: true` works without `runAsUser`. The image supports `--cap-drop ALL` and `--security-opt no-new-privileges`.
* The Corda binaries are owned by `root` and are read-only. The `persistence`, `artemis` and `certificates` folders have mode `750`, and Corda is unpacked from `corda.jar` on every start, so changes to the unpacked copy do not survive a restart.
* The image declares its data folders as volumes, and the `cordapps`, `drivers` and configuration folders can be mounted read-only.
* A new health check reports the container as healthy once the node listens on its RPC port. If `rpcSettings.address` does not use the default port `10201`, set `CORDA_HEALTHCHECK_PORT`; otherwise the container is reported as unhealthy, which Docker Swarm acts on.

A read-only root file system is not supported yet. For more information, see [Official Corda Docker image]({{< relref "docker-image.md" >}}).

### Platform and dependency changes

* **Java and Kotlin are unchanged.** Corda 4.15 runs on Java 17 and is built with Kotlin 1.9.20, as Corda 4.14 is. The Corda Gradle plugins and the Gradle version used to build CorDapps are unchanged.
* **Hibernate ORM 7.4.12 and Jakarta Persistence API 3.2.0** replace Hibernate ORM 5.6.15 and `javax.persistence-api` 2.2. Hibernate 7 is published as `org.hibernate.orm:hibernate-core`, where Hibernate 5 was `org.hibernate:hibernate-core`. Declare it as `cordaProvided` or compile-only if your CorDapp refers to Hibernate classes directly. See [Hibernate 7 and Jakarta Persistence](#hibernate-7-and-jakarta-persistence) above.
* **HikariCP 7.1.0** replaces HikariCP 5.1.0 for the node's database connection pool.
* **Liquibase 4.33.0** replaces Liquibase 4.20.0. On a database that is already at 4.14, the database migration runs no changesets, but Liquibase stores changeset checksums in a new format, so it logs `Upgrading checksum for Changeset ...` once per existing changeset. Liquibase's analytics are disabled.
* **H2 2.4.240** replaces H2 2.2.224 for development nodes. Existing H2 database files open without conversion. H2 2.5.x is deliberately not used, because it can lose committed data when the JVM exits without closing the database.
* **Jetty 12.1.14** replaces Jetty 12.0.38, and **Jackson 2.22.4** replaces Jackson 2.21.7.
* **Artemis 2.57.0, Netty 4.1.139.Final and Quasar 0.9.3_r3** are used, as in Corda 4.14.4 apart from a Netty patch release.

For the full list, see [Third-party components upgrade](#third-party-components-upgrade).

### API changes

* **`ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`.** A CorDapp rebuilt for 4.15 must bind the block to the `jakarta.persistence` type. A CorDapp built for 4.14 or earlier is converted by the node and keeps working unchanged. The API checker does not report this change, because the recorded signature has no type parameters.
* **`Command`, `CommandWithParties` and `SignatureMetadata` have a new nullable property** for key rotation proofs. Their existing constructors are kept, but their `copy` methods now take the new property, so a CorDapp built for 4.14 or earlier that calls `copy` on one of these classes must be rebuilt against 4.15.
* **New key rotation APIs.** See [Verifying transactions signed with a rotated key](#verifying-transactions-signed-with-a-rotated-key).

### Fixed issues

* Fixed an issue where a flow restored from a checkpoint could fail when telemetry was enabled: with a `NullPointerException` if a telemetry component had been enabled after the checkpoint was written, or with an `IndexOutOfBoundsException` when span start and end events were enabled (`spanStartEndEventsEnabled`).
* The following vulnerabilities in dependencies have been addressed:

| Vulnerability  | Component |
|----------------|-----------|
| CVE-2026-112046 | ASM |
| CVE-2026-116486 | Objenesis |
| CVE-2026-114938 | JDK in the Corda Docker images |

### Known issues

#### CVE-2026-92877 in jaxb-core

Corda 4.15 includes `org.glassfish.jaxb:jaxb-core` 4.0.7, which Hibernate ORM 7.4.12 depends on and which is affected by CVE-2026-92877 (XML external entity processing). R3 has assessed that the vulnerability cannot be exploited in Corda: Corda does not use JAXB, Hibernate reads its mapping and configuration XML through a path that is not affected, and the only affected component is used for XML-typed columns, which Corda does not have. No fixed version of `jaxb-core` has been released yet. R3 will upgrade it in a future release.

### Third-party components upgrade

This table shows the updates in dependency versions for Corda Open Source 4.15 since Corda Open Source 4.14.4. Dependencies with unchanged versions, and build and test tools, are omitted.

| Dependency | Name | 4.14.4 Open Source | 4.15 Open Source |
| ---------- | ---- | ------------------ | ---------------- |
| org.hibernate.orm:hibernate-core | Hibernate ORM | 5.6.15.Final (org.hibernate:hibernate-core) | 7.4.12.Final |
| jakarta.persistence:jakarta.persistence-api | Jakarta Persistence API | 2.2 (javax.persistence:javax.persistence-api) | 3.2.0 |
| com.zaxxer:HikariCP | HikariCP | 5.1.0 | 7.1.0 |
| org.liquibase:liquibase-core | Liquibase | 4.20.0 | 4.33.0 |
| com.h2database:h2 | H2 | 2.2.224 | 2.4.240 |
| net.bytebuddy:byte-buddy | Byte Buddy | 1.12.18 (transitive) | 1.18.8 |
| org.ow2.asm:asm\* | ASM | 9.5 | 9.11.1 |
| org.objenesis:objenesis | Objenesis | 3.3 (transitive) | 3.6 |
| com.azure:azure-identity | Azure Identity | 1.18.3 | 1.18.7 |
| com.azure.resourcemanager:azure-resourcemanager | Azure Resource Manager | 2.62.0 | 2.65.0 |
| com.github.ben-manes.caffeine:caffeine | Caffeine | 3.2.3 | 3.3.0 |
| io.github.classgraph:classgraph | ClassGraph | 4.8.135 | 4.8.143 |
| org.apache.commons:commons-collections4 | Commons Collections | 4.3 | 4.6.0 |
| org.apache.commons:commons-configuration2 | Commons Configuration | 2.15.0 | 2.15.1 |
| commons-io:commons-io | Commons IO | 2.21.0 | 2.22.0 |
| org.apache.commons:commons-lang3 | Commons Lang | 3.19.0 | 3.21.0 |
| com.lmax:disruptor | Disruptor | 3.4.2 | 4.0.0 |
| com.google.guava:guava | Guava | 33.1.0-jre | 33.7.2-jre |
| com.fasterxml.jackson.\* | Jackson | 2.21.7 | 2.22.4 |
| org.fusesource.jansi:jansi | Jansi | 1.18 | 2.4.3 |
| org.javassist:javassist | Javassist | 3.29.2-GA | 3.33.0-GA |
| com.jcabi:jcabi-manifests | jcabi-manifests | 1.1 | 2.2.0 |
| org.glassfish.jersey.\* | Jersey | 3.1.11 | 3.1.12 |
| org.eclipse.jetty.ee10:jetty-ee10-\* | Jetty | 12.0.38 | 12.1.14 |
| org.jolokia:jolokia-jvm | Jolokia | 1.6.1 | 1.6.2 |
| net.sf.jopt-simple:jopt-simple | JOpt Simple | 5.0.2 | 5.0.4 |
| net.minidev:json-smart | json-smart | 2.5.2 | 2.6.0 |
| com.esotericsoftware:kryo | Kryo | 5.5.0 | 5.7.1 |
| de.javakaffee:kryo-serializers | Kryo serializers | 0.43 | 0.45 |
| org.apache.logging.log4j:\* | Log4j | 2.25.5 | 2.26.1 |
| io.netty:netty-\* | Netty | 4.1.138.Final | 4.1.139.Final |
| io.netty:netty-tcnative-boringssl-static | Netty TCNative | 2.0.74.Final | 2.0.84.Final |
| com.nimbusds:nimbus-jose-jwt | Nimbus JOSE + JWT | 10.0.2 | 10.10 |
| io.opentelemetry:opentelemetry-\* | OpenTelemetry | 1.63.0 | 1.67.0 |
| io.opentelemetry.semconv:opentelemetry-semconv | OpenTelemetry semantic conventions | 1.41.1 | 1.44.0 |
| org.apache.shiro:shiro-core | Shiro | 3.0.0 | 3.0.1 |
| org.slf4j:\* | SLF4J | 2.0.12 | 2.0.20 |
| org.yaml:snakeyaml | SnakeYAML | 2.2 | 2.7 |
| com.typesafe:config | Typesafe Config | 1.3.4 | 1.4.9 |
