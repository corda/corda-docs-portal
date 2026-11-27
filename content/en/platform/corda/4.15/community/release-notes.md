---
title: Corda Open Source Edition 4.15 release notes
date: '2026-11-24'
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
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

Corda Open Source Edition 4.15 upgrades Hibernate ORM from version 5.6, which is end of life, to version 7.4.12, which implements Jakarta Persistence 3.2. The persistence annotations that CorDapps use for their vault schemas, and the `EntityManager` that `ServiceHub.withEntityManager` provides, move from the `javax.persistence` package to the `jakarta.persistence` package. The upgrade needs no database migration, and CorDapps and contract attachments built for Corda 4.14 or earlier run without a rebuild, because the node converts their classes as it loads them. The node refuses to start with a CorDapp that uses a Hibernate 5 feature that Hibernate 7 no longer has, and some query behaviour has changed, so start a 4.15 test node with your CorDapps and run their flows before you upgrade production.

For what node operators and CorDapp developers need to do, see [Hibernate 7 and Jakarta Persistence in Corda Open Source Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}).

**R3's CorDapp libraries.** The Token SDK and the Corda Accounts Library each have a release for Corda 4.15:

* **Token SDK 1.3.5** and **Corda Accounts Library 1.1.2** run on Corda 4.12 to 4.14 and on 4.15 with one jar: their schema classes carry both the `javax.persistence` and the `jakarta.persistence` annotations, their flows call the node's entity manager without binding to either API, and neither library declares a Hibernate dependency any more. Both are built against Corda 4.12.13 and need no configuration on a 4.15 node.
* **Earlier versions** of the two libraries only work as jars already deployed in a node's `cordapps` directory, which a 4.15 node converts as it loads them. They cannot be used to build or test a CorDapp for 4.15: `tokens-workflows` 1.3.4 and earlier declare Hibernate 5 as a runtime dependency, which Gradle refuses next to Corda 4.15, and a CorDapp that depends on an earlier version of either library fails its `MockNetwork`, `MockServices` and in-process driver tests on 4.15, where nothing is converted. Move to Token SDK 1.3.5 and Corda Accounts Library 1.1.2.
* **Building and testing a CorDapp for 4.15:** declare the two libraries as `cordapp` dependencies as before and test them in a 4.15 `MockNetwork` without further settings. If you build either library from source, build it against Corda 4.12, the default: a build against 4.15 runs on 4.15 only, because its `withEntityManager` code binds to the Jakarta `EntityManager`.

For the details, see the release notes of the [Tokens SDK]({{< relref "../../../../tools/tokens-sdk/tokens-sdk-index.md#changes-in-tokens-sdk-135" >}}) and the [Corda Accounts Library]({{< relref "../../../../tools/accounts/accounts-index.md#changes-in-corda-accounts-library-112" >}}).

#### Verifying transactions signed with a rotated key

Corda Enterprise Edition 4.15 introduces cross-provider key rotation, which moves a node's or notary's legal identity key to a different key provider, such as from a file-based keystore to an HSM. A Corda Open Source Edition node cannot rotate its own key across providers, but a 4.15 node verifies transactions that carry key rotation proofs, so it can keep transacting with Corda Enterprise nodes that have rotated their keys. New public APIs, such as `PartyIdentityResolver`, let CorDapps recognise a party across a rotation. A CorDapp that compares parties or keys directly may need changes before any node on the network rotates its key.

For more information, see [Parties whose key has been rotated]({{< relref "api-identity.md#parties-whose-key-has-been-rotated" >}}).

#### Node scheduler metrics

New metrics under `net.corda.NodeSchedulerService` (`ConsecutiveDatabaseFailures`, `DatabaseFailures` and `MillisStalled`) show when the node's scheduler can no longer run scheduled flows, for example during a database outage.

For more information, see [Node administration]({{< relref "node-administration.md" >}}).

#### Warning when RPC runs without TLS

The node now prints a warning at start-up when its RPC port accepts connections without TLS, because RPC usernames and passwords are then sent over the network in clear text. The node's TLS transports were hardened at the same time: a TLS transport that is missing its key store or trust store now fails instead of falling back to plain text, and P2P connections always use mutual TLS.

For more information, see [Configuring wire security]({{< relref "clientrpc.md#configuring-wire-security" >}}).

#### Docker image hardening

The Corda Open Source Docker images have been hardened. They use digest-pinned base images with a JDK that fixes CVE-2026-114938, run as the non-root `corda` user with the UID and GID `1000:1000`, keep the Corda binaries read-only, declare their data folders as volumes, and have a health check. Their default behaviour is unchanged, so existing deployments and scripts keep working. If `rpcSettings.address` does not use the default port `10201`, set `CORDA_HEALTHCHECK_PORT`, or the container is reported as unhealthy.

For more information, see [Image security]({{< relref "docker-image.md#image-security" >}}).

### Platform and dependency changes

* **Java and Kotlin are unchanged.** Corda 4.15 runs on Java 17 and is built with Kotlin 1.9.20, as Corda 4.14 is. The Corda Gradle plugins and the Gradle version used to build CorDapps are unchanged.
* **Hibernate ORM 7.4.12 and Jakarta Persistence API 3.2.0** replace Hibernate ORM 5.6.15 and `javax.persistence-api` 2.2. Hibernate 7 is published as `org.hibernate.orm:hibernate-core`, where Hibernate 5 was `org.hibernate:hibernate-core`. Declare it as `cordaProvided` or compile-only if your CorDapp refers to Hibernate classes directly. See [Hibernate 7 and Jakarta Persistence](#hibernate-7-and-jakarta-persistence) above.
* **HikariCP 7.1.0** replaces HikariCP 5.1.0 for the node's database connection pool.
* **Liquibase 4.33.0** replaces Liquibase 4.20.0. On a database that is already at 4.14, the database migration runs no changesets, but Liquibase stores changeset checksums in a new format, so it logs `Upgrading checksum for Changeset ...` once per existing changeset. Liquibase's analytics are disabled.
* **H2 2.4.240** replaces H2 2.2.224 for development nodes. Existing H2 database files open without conversion. H2 2.5.x is deliberately not used, because it can lose committed data when the JVM exits without closing the database.
* **Databases and JDBC drivers.** PostgreSQL 14 is no longer in the platform support matrix, which lists PostgreSQL JDBC Driver 42.7.14. See the [platform support matrix]({{< relref "release-platform-support-matrix.md" >}}).
* **Jetty 12.1.14** replaces Jetty 12.0.38, and **Jackson 2.22.4** replaces Jackson 2.21.7.
* **Artemis 2.57.0, Netty 4.1.139.Final and Quasar 0.9.3_r3** are used, as in Corda 4.14.4 apart from a Netty patch release.

For the full list, see [Third-party components upgrade](#third-party-components-upgrade).

### API changes

* **`ServiceHub.withEntityManager` now provides a `jakarta.persistence.EntityManager`.** A CorDapp rebuilt for 4.15 must bind the block to the `jakarta.persistence` type. A CorDapp built for 4.14 or earlier is converted by the node and keeps working unchanged.
* **New key rotation APIs.** See [Parties whose key has been rotated]({{< relref "api-identity.md#parties-whose-key-has-been-rotated" >}}).

### Fixed issues

* Fixed an issue where a flow restored from a checkpoint could fail when telemetry was enabled: with a `NullPointerException` if a telemetry component had been enabled after the checkpoint was written, or with an `IndexOutOfBoundsException` when span start and end events were enabled (`spanStartEndEventsEnabled`).
* The following vulnerabilities in dependencies have been addressed:

| Vulnerability   | Severity | Component           | Fixed in  |
|-----------------|----------|---------------------|-----------|
| CVE-2026-114938 | High     | JDK (Docker images) | 17.0.21.1 |
| CVE-2026-112046 | Medium   | ASM                 | 9.11.1    |
| CVE-2026-116486 | Low      | Objenesis           | 3.6       |

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
