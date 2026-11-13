---
date: '2023-01-09'
menu:
  corda-enterprise-4-15:
    identifier: "corda-enterprise-4-15-cordapp-upgrade"
    parent: corda-enterprise-4-15-upgrading-menu
tags:
- app
- upgrade
- notes
title: Upgrading a CorDapp to a newer platform version
weight: 30
---

# Upgrading a CorDapp to a newer platform version

This guide shows you how to upgrade your CorDapp from previous platform versions to benefit
from the new features in the latest release.

Most of Corda's public, non-experimental APIs are backwards compatible. See the [full list of stable APIs]({{< relref "../../../../api-ref/api-ref-corda-4.md" >}}). If you are working with a stable API, you do not need to update your CorDapps. However, there are usually new features and other opt-in changes that may improve the security, performance, or usability of your
CorDapp that are worth considering for any actively maintained software.

{{< warning >}}
Sample CorDapps found in the Corda and Corda samples repositories should not be used in production.
If you do use them, re-namespace them to a package namespace you control and sign/version them.
{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release | Platform version |
|:--------------|:----------------|
| 4.15          | 170             |
| 4.14          | 160             |
| 4.13          | 150             |
| 4.12          | 140             |
| 4.11          | 13              |
| 4.10          | 12              |
| 4.9           | 11              |
| 4.8           | 10              |
| 4.7           | 9               |
| 4.6           | 8               |
| 4.5           | 7               |
| 4.4           | 6               |
| 4.3           | 5               |
| 4.2           | 4               |
| 4.1           | 4               |
| 4.0           | 4               |
| 3.3           | 3               |
{{< /table >}}

## Upgrading CorDapps to platform version 170

Platform version 170 represents Corda 4.15, which upgrades the node's object-relational mapper from Hibernate ORM 5.6 to Hibernate ORM 7.4.12. Hibernate 7 implements Jakarta Persistence, so the persistence annotations and the `EntityManager` that CorDapps use move from the `javax.persistence` package to the `jakarta.persistence` package. The Hibernate upgrade itself needs no database migration; the 4.15 node upgrade still runs the usual migrations for the new tables that other 4.15 features add.

A CorDapp built for Corda 4.14 or earlier does not have to be rebuilt to run on a 4.15 node: the node converts its `javax.persistence` classes to `jakarta.persistence` as it loads them, and substitutes the Hibernate 5 `@Type` names that Corda registered (`uuid-char`, `corda-wrapper-binary`, `corda-blob`) and Hibernate 5's own. The node refuses to start if a CorDapp uses a Hibernate 5 annotation, class or member that Hibernate 7 no longer has, such as a custom `@Type` or `Session.save`, so test every CorDapp on a 4.15 node before you upgrade production.

To rebuild a CorDapp for Corda 4.15:

1. Replace `javax.persistence` with `jakarta.persistence`, and `javax.persistence:javax.persistence-api` with `jakarta.persistence:jakarta.persistence-api:3.2.0`.
2. Replace `org.hibernate:hibernate-core` with `org.hibernate.orm:hibernate-core:7.4.12.Final`, and keep it a `cordaProvided` (compile-only) dependency.
3. Replace `@Type(type = "uuid-char")` with `@JdbcTypeCode(SqlTypes.VARCHAR)`, `@Type(type = "corda-wrapper-binary")` with `@JdbcTypeCode(SqlTypes.VARBINARY)`, and `@Type(type = "corda-blob")` with `@JdbcTypeCode(CordaSqlTypes.CORDA_BLOB)`.
4. Replace `Session.save`, `update`/`saveOrUpdate` and `delete` with `persist`, `merge` and `remove`. Use attribute names, not column names, in HQL and JPQL.
5. Increase the CorDapp version, rebuild, test against every database you support, and sign with the same key as before.

The script `tools/scripts/migrate-cordapp-to-hibernate7.sh` in the [Corda repository](https://github.com/corda/corda/blob/release/os/4.15/tools/scripts/migrate-cordapp-to-hibernate7.sh) applies steps 1 and 2, and the `uuid-char` and `corda-wrapper-binary` replacements of step 3, to a source tree, and lists the other `@Type` names, the `Session` calls and the queries for you to change by hand. For the full list of changes, the Hibernate 7 behaviour changes that affect rebuilt and converted CorDapps alike, and what makes the node refuse a CorDapp, see [Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15]({{< relref "hibernate-7-upgrade.md" >}}).

## Upgrading CorDapps to platform version 160

No manual upgrade steps are required.

## Upgrading CorDapps to platform version 150

No manual upgrade steps are required.

## Upgrading CorDapps to platform version 140

Platform version 140 which represents Corda 4.12 is a major platform upgrade. In this version, Corda has been upgraded to run on Java 17 and to use Kotlin 1.9.20. This also means that you must recompile Corda 4.12 CorDapps with Java 17 and Kotlin 1.9.20. Once recompiled and fully tested, you must sign CorDapps with the same key used to sign the 4.11 CorDapps.

Additionally, if a CorDapp has been updated to platform version 140, you must upgrade Corda nodes to Corda 4.12. For instructions on how to upgrade Corda nodes, see [Corda Enterprise Edition 4.11 to 4.12 upgrade guide]({{< relref "upgrade-guide.md" >}}).

## Upgrading CorDapps to platform version 9, 10, 11, 12, and 13

No manual upgrade steps are required.

## Upgrading CorDapps to platform version 8

To upgrade your CorDapps to platform version 8, you need to:
1. [Upgrade existing nodes to version 4.6]({{< relref "#upgrade-existing-nodes-to-version-46" >}}).
2. [Check that you are using Corda Gradle plugins version 5.0.12]({{< relref "#check-that-you-are-using-corda-gradle-plugins-version-5012" >}}).

### Upgrade existing nodes to version 4.6

When upgrading to Corda 4.6 from a previous version, you need to upgrade your nodes because of the operational improvements for database schema harmonization that were introduced as part of this release.

Follow the steps below for each upgrade path.

#### Upgrade a node from Corda 4.5 (or earlier 4.x version)

1. Remove any entries of `transactionIsolationLevel`, `initialiseSchema`, `initialiseAppSchema`, and `runMigration` from the database section of your [node configuration file]({{< relref "node/setup/corda-configuration-file.md" >}}).
2. Update any missing core schema changes by either running the [database management tool]({{< relref "database-management-tool.md" >}}) (recommended) or running the node in `run-migration-scripts` mode: `java -jar corda.jar run-migration-scripts --core-schemas`.

#### Upgrade a node from Corda 3.x or Corda Enterprise 3.x

Version 4.6 does not retro-fit the database changelog when upgrading from versions older than 4.0. Therefore, you need to upgrade to a previous 4.x version before upgrading to 4.6. For example, 3.3 to 4.5, and then 4.5 to 4.6.

### Check that you are using Corda Gradle plugins version 5.0.12

You need to use version 5.0.12 of the Corda Gradle plugins to successfully build a CorDapp against platform version 8 and Corda 4.6.

```
ext.corda_gradle_plugins_version = '5.0.12'
```

## Upgrade CorDapps to platform version 7

You do not need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 6

You do not need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 5

To upgrade your CorDapps to platform version 5, you need to:
1. [Handle any source compatibility breaks]({{< relref "#handle-any-source-compatibility-breaks-if-youre-using-kotlin" >}}).
2. [Update Gradle version and associated dependencies]({{< relref "#update-gradle-version-and-associated-dependencies" >}}).

### Handle any source compatibility breaks (if you're using Kotlin)

The following code (which compiled in platform version 4) will not compile in platform version 5:

{{< tabs name="tabs-1" >}}
{{% tab name="Kotlin" %}}
```kotlin
data class Obligation(val amount: Amount<Currency>, val lender: AbstractParty, val borrower: AbstractParty)

val (lenderId, borrowerId) = if (anonymous) {
    val anonymousIdentitiesResult = subFlow(SwapIdentitiesFlow(lenderSession))
    Pair(anonymousIdentitiesResult[lenderSession.counterparty]!!, anonymousIdentitiesResult[ourIdentity]!!)
} else {
    Pair(lender, ourIdentity)
}

val obligation = Obligation(100.dollars, lenderId, borrowerId)
```
{{% /tab %}}

{{< /tabs >}}

If you try to compile this code in platform version 5, you'll get the following error.

`Type mismatch: inferred type is Any but AbstractParty was expected`

This is because a new `Destination` interface (introduced in platform version 5) can cause type inference failures when using a variable as an `AbstractParty` which has an actual value that is one of `Party` or `AnonymousParty`. These subclasses
implement `Destination`, while the superclass does not. Kotlin must pick a type for the variable, and so chooses the most specific
ancestor of both `AbstractParty` and `Destination`. This is `Any`, which is not subsequently a valid type for `AbstractParty`.

For more information on `Destination`, see the [Changelog](https://github.com/corda/corda-docs-portal/tree/main/content/en/archived-docs/corda-os/4.4/changelog.md) for platform version 5, or the [KDocs]({{< relref "../../../../api-ref/api-ref-corda-4.md#corda-enterprise-4x" >}}) for the interface.

{{< note >}}
This is a Kotlin-specific issue. Java can choose `? extends AbstractParty & Destination`, which can subsequently be used
as `AbstractParty`.

{{< /note >}}


To fix the issue, you must provide an explicit type hint to the compiler.

{{< tabs name="tabs-2" >}}
{{% tab name="Kotlin" %}}
```kotlin
data class Obligation(val amount: Amount<Currency>, val lender: AbstractParty, val borrower: AbstractParty)

val (lenderId, borrowerId) = if (anonymous) {
    val anonymousIdentitiesResult = subFlow(SwapIdentitiesFlow(lenderSession))
    Pair(anonymousIdentitiesResult[lenderSession.counterparty]!!, anonymousIdentitiesResult[ourIdentity]!!)
} else {
    // This Pair now provides a type hint to the compiler
    Pair<AbstractParty, AbstractParty>(lender, ourIdentity)
}

val obligation = Obligation(100.dollars, lenderId, borrowerId)
```
{{% /tab %}}

{{< /tabs >}}

This stops type inference from occurring and forces the variable to be of type `AbstractParty`.



### Update Gradle version and associated dependencies

Platform version 5 requires Gradle 5.4. If you use the Gradle wrapper, you can upgrade by running:


```shell
./gradlew wrapper --gradle-version 5.4.1
```



Otherwise, upgrade your installed copy in the usual way.

Additionally, you’ll need to add [https://repo.gradle.org/gradle/libs-releases](https://repo.gradle.org/gradle/libs-releases) as a repository to your project, to pick up the
**gradle-api-tooling** dependency. To do this, add the following to the repositories in your Gradle file:

```groovy
maven { url 'https://repo.gradle.org/gradle/libs-releases' }
```

