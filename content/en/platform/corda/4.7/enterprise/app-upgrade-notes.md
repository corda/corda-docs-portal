---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: "corda-enterprise-4-7-cordapp-upgrade"
    parent: corda-enterprise-4-7-upgrading-menu
tags:
- app
- upgrade
- notes
title: Upgrading a CorDapp to a newer platform version
weight: 30
---

# Upgrading a CorDapp to a newer platform version

{{< warning >}}
Corda Enterprise Edition 4.7.1 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.7.1 please read the guidance on [upgrading your notary service]({{< relref "../../../../../en/platform/corda/4.7/enterprise/notary/upgrading-the-ha-notary-service.md" >}}).
{{< /warning >}}

These notes provide instructions for upgrading your CorDapps from previous versions. Corda provides backwards compatibility for public,
non-experimental APIs that have been committed to. A list can be found in the api-stability-guarantees page.

This means that you can upgrade your node across versions *without recompiling or adjusting your CorDapps*. You just have to upgrade
your node and restart.

However, there are usually new features and other opt-in changes that may improve the security, performance or usability of your
application that are worth considering for any actively maintained software. This guide shows you how to upgrade your app to benefit
from the new features in the latest release.


{{< warning >}}
The sample apps found in the Corda repository and the Corda samples repository are not intended to be used in production.
If you are using them you should re-namespace them to a package namespace you control, and sign/version them yourself.

{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.8 | 10 |
| 4.7 | 9 |
| 4.6 | 8 |
| 4.5 | 7 |
| 4.4 | 6 |
| 4.3 | 5 |
| 4.2 | 4 |
| 4.1 | 4 |
| 4.0 | 4 |
| 3.3 | 3 |
{{< /table >}}

## Upgrading CorDapps to platform version 9

No manual upgrade steps are required.

## Upgrading CorDapps to platform version 8

To upgrade your CorDapps to platform version 8, you need to:
1. [Upgrade existing nodes to version 4.6](#upgrade-existing-nodes-to-version-46).
2. [Check that you are using Corda Gradle plugins version 5.0.12](#check-that-you-are-using-corda-gradle-plugins-version-5012).

### Upgrade existing nodes to version 4.6

When upgrading to Corda 4.6 from a previous version, you need to upgrade your nodes because of the operational improvements for database schema harmonization that were introduced as part of this release.

Follow the steps below for each upgrade path.

#### Upgrade a node from Corda 4.5 (or earlier 4.x version)

1. Remove any entries of `transactionIsolationLevel`, `initialiseSchema`, `initialiseAppSchema`, and `runMigration` from the database section of your [node configuration file](node/setup/corda-configuration-file.md).
2. Update any missing core schema changes by either running the [Database Management Tool](database-management-tool.md) (recommended) or running the node in `run-migration-scripts` mode: `java -jar corda.jar run-migration-scripts --core-schemas`.

#### Upgrade a node from Corda 3.x or Corda Enterprise 3.x

Version 4.6 doesn't retro-fit the database changelog when upgrading from versions older than 4.0. Therefore, you need to upgrade to a previous 4.x version before upgrading to 4.6. For example, 3.3 to 4.5, and then 4.5 to 4.6.

### Check that you are using Corda Gradle plugins version 5.0.12

You need to use version 5.0.12 of the Corda Gradle plugins to successfully build a CorDapp against platform version 8 and Corda 4.6.

```
ext.corda_gradle_plugins_version = '5.0.12'
```

## Upgrade CorDapps to platform version 7

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 6

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 5

To upgrade your CorDapps to platform version 5, you need to:
1. [Handle any source compatibility breaks](#handle-any-source-compatibility-breaks-if-youre-using-kotlin).
2. [Update Gradle version and associated dependencies](#update-gradle-version-and-associated-dependencies).

### Handle any source compatibility breaks (if you're using Kotlin)

The following code (which compiled in platform version 4) will not compile in platform version 5:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
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
For more information on `Destination`, see the [Changelog](https://github.com/corda/corda-docs-portal/tree/main/content/en/archived-docs/corda-os/4.4/changelog.md) for platform version 5, or the [KDocs](../../../../api-ref/api-ref-corda-4.html#corda-enterprise-4x-api-reference) for the interface.


{{< note >}}
This is a Kotlin-specific issue. Java can choose `? extends AbstractParty & Destination`, which can subsequently be used
as `AbstractParty`.

{{< /note >}}


To fix the issue, you must provide an explicit type hint to the compiler.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
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

