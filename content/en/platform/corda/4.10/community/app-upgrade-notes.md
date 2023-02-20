---
aliases:
- /head/app-upgrade-notes.html
- /HEAD/app-upgrade-notes.html
- /app-upgrade-notes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-app-upgrade-notes
    parent: corda-community-4-10-upgrading
    weight: 20
tags:
- app
- upgrade
- notes
title: Upgrading CorDapps to newer platform versions
---

# Upgrading CorDapps to newer platform versions

These notes provide information on upgrading your CorDapps from previous versions. Corda provides backwards compatibility for public,
non-experimental APIs that have been committed to. A list can be found in the [API stability guarantees](api-stability-guarantees.md) page.

This means that you can upgrade your node across versions *without recompiling or adjusting your CorDapps*. You just have to upgrade
your node and restart.

However, there are usually new features and other opt-in changes that may improve the security, performance or usability of your
application that are worth considering for any actively maintained software.

{{< warning >}}
The sample apps found in the Corda repository and the Corda samples repository are not intended to be used in production.
If you are using them you should re-namespace them to a package namespace you control, and sign/version them yourself.
{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.10 | 12 |
| 4.9 | 11 |
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

## Upgrading CorDapps to platform version 9, 10, 11, and 12

No manual upgrade steps are required.

## Upgrading CorDapps to platform version 8 or lower

### Required actions relating to database optimisation in Corda 4.6

The operational improvements around database schema harmonisation that we have made in Corda 4.6 require a number of manual steps when upgrading to Corda 4.6 from a previous version. For more information, see the Corda Open Source 4.6 release notes available in the [archived-docs](https://github.com/corda/corda-docs-portal/tree/main/content/en/archived-docs) directory of the [corda/corda-docs-portal](https://github.com/corda/corda-docs-portal) repo.
The required steps for each upgrade path are described below.

#### Upgrading an existing node from Corda 4.5 (or earlier 4.x version) to version 4.6

1. Remove any entries of `transactionIsolationLevel`, `initialiseSchema`, or `initialiseAppSchema` from the database section of your node configuration file.
2. Update any missing core schema changes by running the node in `run-migration-scripts` mode: `java -jar corda.jar run-migration-scripts --core-schemas`.
3. Add Liquibase resources to CorDapps. In Corda 4.6, CorDapps that introduce custom schema need Liquibase migration scripts allowing them to create the schema upfront. For existing CorDapps that do not have migration scripts in their resources, they can be added as an external migration `.jar` file, as documented in the Corda Enterprise 4.6 database management scripts documentation (available in the [archived-docs](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-enterprise/4.6/enterprise/cordapps/database-management.md) directory of the [corda/corda-docs-portal](https://github.com/corda/corda-docs-portal) repo).
4. Update the changelog for existing schemas. After upgrading the Corda `.jar` file and adding Liquibase scripts to the CorDapp(s), any custom schemas from the apps are present
in the database, but the changelog entries in the Liquibase changelog table are missing (as they have been created by Liquibase). This will cause issues when starting the node, and also when running `run-migration-scripts` as tables that already exist cannot be recreated. By running the new sub-command `sync-app-schemas`, changelog entries are created for all existing mapped schemas from CorDapps: `java -jar corda.jar sync-app-schemas`.

{{< warning >}}
**IMPORTANT!**
1. Do **not** install any new CorDapp, or a version adding schema entities, before running the `sync-app-schemas` sub-command. Any mapped schema found in the CorDapps will be added to the changelog **without** trying to create the matching database entities.
2. If you are upgrading a node to Corda 4.6 while any CorDapp with mapped schemas is being installed, you **must synchronise the schemas** (and thus run `sync-app-schemas`) **before** the node can start again and/or before any app schema updates can be run. Therefore, you must **not** install or update a CorDapp with new or modified schemas while upgrading
the node, or after upgrading but before synchronising the app schemas.
{{< /warning >}}

#### Upgrading from Corda 3.x or Corda Enterprise 3.x

Corda 4.6 drops the support for retro-fitting the database changelog when migrating from Corda versions older than 4.0. Thus it is required to migrate to a previous 4.x version before
migrating to Corda 4.6 - for example, 3.3 to 4.5, and then 4.5 to 4.6.

### Corda Gradle Plugins version `5.0.12`

To successfully build a CorDapp against Platform Version 8 and Corda 4.6, you need to use version `5.0.12` of the Corda Gradle Plugins:

```
ext.corda_gradle_plugins_version = '5.0.12'
```

## Upgrading CorDapps to Platform Versions 6 and 7

No manual upgrade steps are required.

## Upgrading CorDapps to Platform Version 5

This section provides instructions for upgrading your CorDapps from previous versions to take advantage of features and enhancements introduced
in platform version 5.

{{< note >}}
If you are upgrading from a platform version older than 4, then the upgrade notes for upgrading to Corda 4 (below) also apply.

{{< /note >}}

### Step 1. Handle any source compatibility breaks (if using Kotlin)

The following code, which compiled in Platform Version 4, will not compile in Platform Version 5:

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

Compiling this code against Platform Version 5 will result in the following error:

`Type mismatch: inferred type is Any but AbstractParty was expected`

The issue here is that a new `Destination` interface introduced in Platform Version 5 can cause type inference failures when a variable is
used as an `AbstractParty` but has an actual value that is one of `Party` or `AnonymousParty`. These subclasses
implement `Destination`, while the superclass does not. Kotlin must pick a type for the variable, and so chooses the most specific
ancestor of both `AbstractParty` and `Destination`. This is `Any`, which is not a valid type for use as an `AbstractParty` later.
For more information on `Destination`, see the [Changelog](https://docs.corda.net/docs/corda-os/4.4/changelog.html) for Platform Version 5, or the KDocs for the interface
[here](../../../../api-ref/api-ref-corda-4.html#corda-community-edition-4x-api-reference).

Note that this is a Kotlin-specific issue. Java can instead choose `? extends AbstractParty & Destination` here, which can later be used
as `AbstractParty`.

To fix this, an explicit type hint must be provided to the compiler:

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



### Step 2. Update Gradle version and associated dependencies

Platform Version 5 requires Gradle 5.4 to build. If you use the Gradle wrapper, you can upgrade by running:


```shell
./gradlew wrapper --gradle-version 5.4.1
```



Otherwise, upgrade your installed copy in the usual manner for your operating system.

Additionally, you’ll need to add [https://repo.gradle.org/gradle/libs-releases](https://repo.gradle.org/gradle/libs-releases) as a repository to your project, in order to pick up the
*gradle-api-tooling* dependency. You can do this by adding the following to the repositories in your Gradle file:

```groovy
maven { url 'https://repo.gradle.org/gradle/libs-releases' }
```