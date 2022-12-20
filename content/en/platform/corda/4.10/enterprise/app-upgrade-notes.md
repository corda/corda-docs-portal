---
date: '2022-12-07'
menu:
  corda-enterprise-4-10:
    identifier: "corda-enterprise-4-10-cordapp-upgrade"
    parent: corda-enterprise-4-10-upgrading-menu
tags:
- app
- upgrade
- notes
title: Upgrading a CorDapp to a newer platform version
weight: 30
---

# Upgrading a CorDapp to a newer platform version

{{< warning >}}
Corda Enterprise Edition 4.10 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.10, read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md).
{{< /warning >}}

This guide shows you how to upgrade your CorDapp from previous platform versions to benefit
from the new features in the latest release.

Most of Corda's public, non-experimental APIs are backwards compatible. See the [full list of stable APIs](../../../../api-ref/api-ref-corda-4.md). If you are working with a stable API, you don't need to update your CorDapps. However, there are usually new features and other opt-in changes that may improve the security, performance, or usability of your
CorDapp that are worth considering for any actively maintained software.

{{< warning >}}
Sample CorDapps found in the Corda and Corda samples repositories should not be used in production.
If you do use them, re-namespace them to a package namespace you control and sign/version them.

{{< /warning >}}

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.10| 12 |
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

## Upgrade CorDapps to platform version 12

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 11

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 10

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 9

You don't need to perform a manual upgrade for this platform version.

## Upgrade CorDapps to platform version 8

To upgrade your CorDapps to platform version 8, you need to:
1. [Upgrade existing nodes to version 4.6](#upgrade-existing-nodes-to-version-46).
2. [Check that you are using Corda Gradle plugins version 5.0.12](#check-that-you-are-using-corda-gradle-plugins-version-5012).


### Upgrade existing nodes to version 4.6

When upgrading to Corda 4.6 from a previous version, you need to upgrade your nodes because of the operational improvements for [database schema harmonization](../../../../../en/platform/corda/4.6/enterprise/release-notes-enterprise.html#database-schema-harmonisation) that were introduced as part of this release.

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

## Upgrade CorDapps to platform versions 7

You don't need to perform a manual upgrade for this platform version.


## Upgrade CorDapps to platform versions 6

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
For more information on `Destination`, see the [Changelog](../../../../../en/platform/corda/4.4/open-source/changelog.html) for platform version 5, or the [KDocs](../../../../api-ref/api-ref-corda-4.html#corda-enterprise-4x-api-reference) for the interface.


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


## Upgrade CorDapps to platform version 4

To upgrade your CorDapps to platform version 4, you need to:
1. [Update RPC clients to use the new RPC library](#1-update-rpc-clients-to-use-the-new-rpc-library).
2. [Change the version numbers in your Gradle build file](#2-change-the-version-numbers-in-your-gradle-build-file).
3. [Update your Gradle build file](#3-update-your-gradle-build-file).
4. <a href="#4-remove-custom-configuration-from-your-nodeconf-file">Remove custom configuration from your `node.conf` file</a>.
5. <a href="#5-improve-the-security-of-your-cordapp-by-upgrading-how-you-use-finalityflow">Improve the security of your CorDapp by upgrading how you use `FinalityFlow`</a>.
6. <a href="#6-improve-the-security-of-your-cordapp-by-upgrading-your-use-of-swapidentitiesflow">Improve the security of your CorDapp by upgrading your use of `SwapIdentitiesFlow`</a>.
7. [Adjust your test code](#7-adjust-your-test-code).
8. <a href="#8-improve-the-security-of-your-cordapp-by-adding-belongstocontract-annotations">Improve the security of your CorDapp by adding `BelongsToContract` annotations</a>.
9. <a href="#9-learn-about-signature-constraints-and-signing-jar-files">Learn about signature constraints and signing `.jar` files</a>.
10. [Improve the security of your CorDapp: Package namespace handling](#10-improve-the-security-of-your-cordapp-package-namespace-handling).
11. [Consider adding extension points to your flows](#11-consider-adding-extension-points-to-your-flows).
12. [Update vault state queries](#12-update-vault-state-queries).
13. <a href="#13-update-your-quasarjar-file">Update your `quasar.jar` file</a>.
14. [Other features that you may find useful](#14-other-features-that-you-may-find-useful).


### 1. Update RPC clients to use the new RPC library

Unlike the RPC API, the RPC wire protocol isn't backwards compatible with Corda 3. Therefore, to use the new version of the RPC library, you need to update RPC clients (such as web servers) in lockstep with the node. As Corda 4 delivers RPC wire stability, you
will be able to update the node and CorDapps without the need to update RPC clients for future upgrades.

### 2. Change the version numbers in your Gradle build file

Change the versions in your Gradle build file as follows.

```groovy
ext.corda_release_version = '4.4'
ext.corda_gradle_plugins_version = '5.0.6'
ext.kotlin_version = '1.2.71'
ext.quasar_version = '0.7.14_r3'
```

You also need to add `corda-dependencies` to your list of repositories to make the custom-built version of Quasar available.

```groovy
repositories {
    mavenCentral()
    jcenter()
    // ... Repository access for Corda Enterprise and any other dependencies
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Quasar version
}
```

{{< note >}}
To benefit from new features, you may want to update your `kotlinOptions` to use language level 1.2. CorDapps targeting Corda 4
may not (at this time) use Kotlin 1.3.

{{< /note >}}

You also need to check you’re using Gradle 4.10—not 5. If you use the Gradle wrapper, run:

```shell
./gradlew wrapper --gradle-version 4.10.3
```

Otherwise, upgrade your installed copy in the usual way.

{{< note >}}
Platform version 5 requires a newer version of Gradle. If you intend to upgrade past platform version 4 at this time, you may want
to skip directly to the [version required by platform version 5](#update-gradle-version-and-associated-dependencies). You’ll still need to change the version
numbers in your Gradle build file as shown in this section.

{{< /note >}}

### 3. Update your Gradle build file

You can make several beneficial changes to your Gradle build file beyond simply incrementing the versions
as described in the step above.

#### Add CorDapp metadata
The Corda Gradle build plugin uses CorDapp metadata to populate your CorDapp's `.jar` file with useful information.
It should look like this:

```groovy
cordapp {
    targetPlatformVersion 4
    minimumPlatformVersion 4
    contract {
        name "MegaApp Contracts"
        vendor "MegaCorp"
        licence "A liberal, open source licence"
        versionId 1
    }
    workflow {
        name "MegaApp flows"
        vendor "MegaCorp"
        licence "A really expensive proprietary licence"
        versionId 1
    }
}
```


{{< important >}}
Watch out for the UK spelling of the word licence (with a c).


{{< /important >}}

You can set `name`, `vendor`, and `licence` to any string, they don’t have to be Corda identities.

Target versioning is a new concept introduced in Corda 4. Before you set values for `targetPlatformVersion` and `minimumPlatformVersion`, read our guide on [versioning](cordapps/versioning.md).

CorDapps running Corda 3 or older don't support CorDapp metadata. This means that your CorDapp may exhibit undefined behaviour at runtime when loaded in nodes that use a newer version.
Even so, it's best practice to complete this metadata ready for upgrades to future versions.


{{< note >}}
Corda versions and platform versions don't align, especially in later versions. For example Corda version 4.9 is platform version 10. See the [platform version matrix](#platform-version-matrix) for further information.
{{< /note >}}

`versionId` is a version code for *your* CorDapp, and is unrelated to Corda’s own versions.
It is used for informative purposes only.


#### Split your CorDapp into contract and workflow `.jar` files
The duplication between `contract` and `workflow` blocks exists because your CorDapp should be split into
two separate `.jar` files/modules. One should contain on-ledger validation code, like states and contracts. The other should contain workflows and anything else, such as services.

Historically one `.jar` file has been used for both, but this can result in sending your flow logic code over the network to
third-party peers even though they don’t need it.

For later versions, the `versionId` parameter attached to the workflow `.jar` file will also help with smoother upgrades
and migration features. You may directly reference the Gradle version number of your CorDapp when setting the
CorDapp specific `versionId` identifiers if this follows the convention of always being a whole number
starting from 1.

If you use the finance demo CorDapp, adjust your dependencies to the `finance-contracts`
and `finance-workflows` artifacts from your own contract and workflow `.jar` file respectively.


### 4. Remove custom configuration from your `node.conf` file

CorDapps can no longer access custom configuration items in the `node.conf` file, as the node’s configuration is not accessible. You can create a CorDapp configuration file for any custom CorDapp configuration. Save your CorDapp configuration file in the
*config* subdirectory of the node’s *cordapps* folder. The name of the file must match the name of the `.jar` file of the CorDapp. For example, if your
CorDapp is called `hello-0.1.jar`, you'll need a configuration file called `cordapps/config/hello-0.1.conf`.

If you are using the `extraConfig` of a `node` in the `deployNodes` Gradle task to populate custom configuration for testing, you will need
to change:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    node {
        name "O=Bank A,L=London,C=GB"c
        ...
        extraConfig = [ 'some.extra.config' : '12345' ]
    }
}
```

To:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    node {
        name "O=Bank A,L=London,C=GB"c
        ...
        projectCordapp {
            config "some.extra.config=12345"
        }
    }
}
```

See [CorDapp configuration files](cordapps/cordapp-build-systems.html#cordapp-configuration-files) for more information.



### 5. Improve the security of your CorDapp by upgrading how you use `FinalityFlow`

The previous `FinalityFlow` API is insecure. It doesn't have a receive flow, so requires counterparty nodes to accept any and
all signed transactions that are sent to it without performing any checks. Therefore, we *highly* recommend that existing CorDapps migrate to the new API to reliably enforce business network membership checks (for example).

The flows that make use of `FinalityFlow` in a CorDapp fall into two basic categories:


* **Non-initiating flows** finalise a transaction without the involvement of a counterpart flow.
* **Initiating flows** initiate a counterpart (responder) flow.

The main difference between these two types of flow is how the CorDapp can be upgraded.

Non-initiating flows can't be upgraded to the new `FinalityFlow` in a backwards compatible way. Changes to these flows need to be deployed simultaneously to all the nodes, using a *lockstep deployment*.

Initiating flows can be upgraded to use the new `FinalityFlow` in a backwards compatible way. This means you can deploy the upgraded CorDapp to the nodes using a *rolling deployment*.


{{< note >}}
A *lockstep deployment* involves stopping all nodes, upgrading to the new version of the CorDapp, and then re-starting them.
Nodes can't run different versions of the CorDapp at the same time.
A *rolling deployment* is where every node can be stopped, upgraded to the new version of the CorDapp, and re-started independently—at different times if needed.
Nodes can be running different versions of the CorDapp and still transact with each other successfully.

{{< /note >}}

To upgrade your `FinalityFlow`, you need to:


1. Change the flow that calls `FinalityFlow`.
2. Change or create the flow that will receive the finalised transaction.
3. Make sure your CorDapp’s `targetPlatformVersion` and `minimumPlatformVersion` are set to 4, see [2. Change the version numbers in your Gradle build file](#2-change-the-version-numbers-in-your-gradle-build-file).


#### Upgrading a non-initiating flow

This example takes a simple flow that finalizes a transaction without the involvement of a counterpart flow:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
class SimpleFlowUsingOldApi(private val counterparty: Party) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        val stx = dummyTransactionWithParticipant(counterparty)
        return subFlow(FinalityFlow(stx))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
public static class SimpleFlowUsingOldApi extends FlowLogic<SignedTransaction> {
    private final Party counterparty;

    @Suspendable
    @Override
    @SuppressWarnings("deprecation")    // deprecated usage of Finality flow API.
    public SignedTransaction call() throws FlowException {
        SignedTransaction stx = dummyTransactionWithParticipant(counterparty);
        return subFlow(new FinalityFlow(stx));
    }

```
{{% /tab %}}


{{< /tabs >}}

To use the new API, the flow needs to be annotated with `InitiatingFlow` and a `FlowSession` to the participant(s) of the transaction must be
passed to `FinalityFlow`:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
// Notice how the flow *must* now be an initiating flow.
@InitiatingFlow
class SimpleFlowUsingNewApi(private val counterparty: Party) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        val stx = dummyTransactionWithParticipant(counterparty)
        // We must initiate a flow session with each non-local participant in the transaction.
        val session = initiateFlow(counterparty)
        return subFlow(FinalityFlow(stx, session))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Notice how the flow *must* now be an initiating flow.
@InitiatingFlow
public static class SimpleFlowUsingNewApi extends FlowLogic<SignedTransaction> {
    private final Party counterparty;

    @Suspendable
    @Override
    public SignedTransaction call() throws FlowException {
        SignedTransaction stx = dummyTransactionWithParticipant(counterparty);
        // We must initiate a flow session with each non-local participant in the transaction.
        FlowSession session = initiateFlow(counterparty);
        return subFlow(new FinalityFlow(stx, session));
    }

```
{{% /tab %}}


{{< /tabs >}}

If there is more than one transaction participant, then a session must be initiated with each one, excluding the local party
and the notary.

A responder flow automatically runs on the other participants’ nodes, which calls `ReceiveFinalityFlow`
to record the finalized transaction:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
// All participants will run this flow to receive and record the finalized transaction into their vault.
@InitiatedBy(SimpleFlowUsingNewApi::class)
class SimpleNewResponderFlow(private val otherSide: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        subFlow(ReceiveFinalityFlow(otherSide))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// All participants will run this flow to receive and record the finalized transaction into their vault.
@InitiatedBy(SimpleFlowUsingNewApi.class)
public static class SimpleNewResponderFlow extends FlowLogic<Void> {
    private final FlowSession otherSide;

    @Suspendable
    @Override
    public Void call() throws FlowException {
        subFlow(new ReceiveFinalityFlow(otherSide));
        return null;
    }

```
{{% /tab %}}


{{< /tabs >}}

{{< note >}}
All the nodes in your business network will need the new CorDapp, otherwise they won’t know how to receive the transaction. *This
includes those nodes that didn’t have the CorDapp originally.* If a node receives a transaction but doesn’t have the new CorDapp, install the CorDapp and restart the node. The transaction will then be recorded.

{{< /note >}}

#### Upgrading an initiating flow

Use the existing flow session for flows that already initiate counterpart flows.
The new `FinalityFlow` is inlined and so the sequence of sends and receives between the two flows will
change and will be incompatible with your current flows. You can use the flow version API to write your flows in a
backwards compatible manner.

Here’s what an upgraded initiating flow may look like.

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
// Assuming the previous version of the flow was 1 (the default if none is specified), we increment the version number to 2
// To allow for backwards compatibility with nodes running the old CorDapp.
@InitiatingFlow(version = 2)
class ExistingInitiatingFlow(private val counterparty: Party) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        val partiallySignedTx = dummyTransactionWithParticipant(counterparty)
        val session = initiateFlow(counterparty)
        val fullySignedTx = subFlow(CollectSignaturesFlow(partiallySignedTx, listOf(session)))
        // Determine which version of the flow the counterparty is using.
        return if (session.getCounterpartyFlowInfo().flowVersion == 1) {
            // Use the old API if the counterparty is using the previous version of the flow.
            subFlow(FinalityFlow(fullySignedTx))
        } else {
            // Otherwise they're on at least version 2 and so we can send the finalized transaction on the existing session.
            subFlow(FinalityFlow(fullySignedTx, session))
        }
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Assuming the previous version of the flow was 1 (the default if none is specified), we increment the version number to 2
// To allow for backwards compatibility with nodes running the old CorDapp.
@InitiatingFlow(version = 2)
public static class ExistingInitiatingFlow extends FlowLogic<SignedTransaction> {
    private final Party counterparty;

    @Suspendable
    @Override
    @SuppressWarnings("deprecation")    // Deprecated usage of Finality flow API without session parameter.
    public SignedTransaction call() throws FlowException {
        SignedTransaction partiallySignedTx = dummyTransactionWithParticipant(counterparty);
        FlowSession session = initiateFlow(counterparty);
        SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(partiallySignedTx, singletonList(session)));
        // Determine which version of the flow the counterparty is using.
        if (session.getCounterpartyFlowInfo().getFlowVersion() == 1) {
            // Use the old API if the counterparty is using the previous version of the flow.
            return subFlow(new FinalityFlow(fullySignedTx));
        } else {
            // Otherwise they're on at least version 2 and so we can send the finalized transaction on the existing session.
            return subFlow(new FinalityFlow(fullySignedTx, session));
        }
    }

```
{{% /tab %}}


{{< /tabs >}}

For the responder flow, insert a call to `ReceiveFinalityFlow` at the location where it’s expecting to receive the
finalized transaction. If the initiator has been written in a backwards compatible way, then the responder must be as well.

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
// First you have to run the SignTransactionFlow, which will return a SignedTransaction.
val txWeJustSigned = subFlow(object : SignTransactionFlow(otherSide) {
    @Suspendable
    override fun checkTransaction(stx: SignedTransaction) {
        // Implement responder flow transaction checks here.
    }
})

if (otherSide.getCounterpartyFlowInfo().flowVersion >= 2) {
    // The counterparty is not using the old CorDapp, so call ReceiveFinalityFlow to record the finalized transaction.
    // If SignTransactionFlow is used, then you can verify the transaction received for recording is the same one
    // that was just signed.
    subFlow(ReceiveFinalityFlow(otherSide, expectedTxId = txWeJustSigned.id))
} else {
    // Otherwise the counterparty is running the old CorDapp and so you don't need to do anything further. The node
    // will automatically record the finalized transaction using the old insecure mechanism.
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// First you have to run the SignTransactionFlow, which will return a SignedTransaction.
SignedTransaction txWeJustSigned = subFlow(new SignTransactionFlow(otherSide) {
    @Suspendable
    @Override
    protected void checkTransaction(@NotNull SignedTransaction stx) throws FlowException {
        // Implement responder flow transaction checks here.
    }
});

if (otherSide.getCounterpartyFlowInfo().getFlowVersion() >= 2) {
    // The counterparty is not using the old CorDapp, so call ReceiveFinalityFlow to record the finalized transaction.
    // If SignTransactionFlow is used, then you can verify the transaction received for recording is the same one
    // that was just signed by passing the transaction id to ReceiveFinalityFlow.
    subFlow(new ReceiveFinalityFlow(otherSide, txWeJustSigned.getId()));
} else {
    // Otherwise the counterparty is running the old CorDapp, and so you don't need to do anything further. The node
    // will automatically record the finalized transaction using the old insecure mechanism.
}

```
{{% /tab %}}


{{< /tabs >}}

You no longer need to use `waitForLedgerCommit` in your responder flow. `ReceiveFinalityFlow` effectively does the same thing as it checks the finalized transaction has appeared in the local node's vault.


### 6. Improve the security of your CorDapp by upgrading your use of `SwapIdentitiesFlow`

The [confidential identities](cordapps/api-confidential-identity.md) API is experimental in Corda 3 and remains so in Corda 4. In this release, the `SwapIdentitiesFlow`
has been adjusted in the same way as the `FinalityFlow` (above). This is to resolve problems with confidential identities being injectable into a node
outside of other flow context. Old code will still work, but it is recommended to adjust your call sites so a session is passed into
the `SwapIdentitiesFlow`.


### 7. Adjust your test code

`MockNodeParameters` and the functions that create it no longer use a lambda expecting a `NodeConfiguration` object.
Use a `MockNetworkConfigOverrides` object instead.

If you are constructing a `MockServices` for testing contracts, and your contract uses the `Cash` contract from the finance CorDapp, you
now need to explicitly add `net.corda.finance.contracts` to the list of `cordappPackages`.

Example:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
val ledgerServices = MockServices(
    listOf("net.corda.examples.obligation", "net.corda.testing.contracts"),
    initialIdentity = TestIdentity(CordaX500Name("TestIdentity", "", "GB")),
    identityService = makeTestIdentityService()
)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MockServices ledgerServices = new MockServices(
    Arrays.asList("net.corda.examples.obligation", "net.corda.testing.contracts"),
    new TestIdentity(new CordaX500Name("TestIdentity", "", "GB")),
    makeTestIdentityService()
);
```
{{% /tab %}}

{{< /tabs >}}

becomes:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
val ledgerServices = MockServices(
    listOf("net.corda.examples.obligation", "net.corda.testing.contracts", "net.corda.finance.contracts"),
    initialIdentity = TestIdentity(CordaX500Name("TestIdentity", "", "GB")),
    identityService = makeTestIdentityService()
)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MockServices ledgerServices = new MockServices(
    Arrays.asList("net.corda.examples.obligation", "net.corda.testing.contracts", "net.corda.finance.contracts"),
    new TestIdentity(new CordaX500Name("TestIdentity", "", "GB")),
    makeTestIdentityService()
);
```
{{% /tab %}}

{{< /tabs >}}

You may need to use the new `TestCordapp` API when testing with the node driver or mock network, especially if you decide to keep using the
pre-Corda 4 `FinalityFlow` API. The previous method of pulling CorDapps into your tests using the `cordappPackages` parameter, does not honour CorDapp versioning.
The new API `TestCordapp.findCordapp()` discovers the CorDapps that contain the provided packages by scanning the classpath. Therefore, you have to ensure that the classpath the tests are running under contains either the CorDapp `.jar` or (if using Gradle) the relevant Gradle sub-project.
In the first case, the versioning information in the CorDapp `.jar` file will be maintained. In the second case, the versioning information will be retrieved from the Gradle `cordapp` task.
For example, if you are using `MockNetwork` for your tests, change the following code:

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
val mockNetwork = MockNetwork(
    cordappPackages = listOf("net.corda.examples.obligation", "net.corda.finance.contracts"),
    notarySpecs = listOf(MockNetworkNotarySpec(notary))
)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MockNetwork mockNetwork = new MockNetwork(
    Arrays.asList("net.corda.examples.obligation", "net.corda.finance.contracts"),
    new MockNetworkParameters().withNotarySpecs(Arrays.asList(new MockNetworkNotarySpec(notary)))
);
```
{{% /tab %}}

{{< /tabs >}}

To:

{{< tabs name="tabs-11" >}}
{{% tab name="kotlin" %}}
```kotlin
val mockNetwork = MockNetwork(
    MockNetworkParameters(
        cordappsForAllNodes = listOf(
            TestCordapp.findCordapp("net.corda.examples.obligation.contracts"),
            TestCordapp.findCordapp("net.corda.examples.obligation.flows")
        ),
        notarySpecs = listOf(MockNetworkNotarySpec(notary))
    )
)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MockNetwork mockNetwork = new MockNetwork(
    new MockNetworkParameters(
        Arrays.asList(
            TestCordapp.findCordapp("net.corda.examples.obligation.contracts"),
            TestCordapp.findCordapp("net.corda.examples.obligation.flows")
        )
    ).withNotarySpecs(Arrays.asList(new MockNetworkNotarySpec(notary)))
);
```
{{% /tab %}}

{{< /tabs >}}

Every package should exist in only one CorDapp. If this is not the case, the discovery process is unable to determine which CorDapp to use and you are likely to see the exception `There is more than one CorDapp containing the package`.
For instance, if you have two CorDapps containing the packages `net.corda.examples.obligation.contracts` and `net.corda.examples.obligation.flows`, you will get this error if you specify the package `net.corda.examples.obligation`.

{{< note >}}
If you have any CorDapp code (such as flows, contracts, or states) that is only used by the tests and located in the same test module, it now won’t be discovered.
You need to move them to the main module of one of your CorDapps or create a new separate CorDapp (if you don't want a production CorDapp to contain this code).

{{< /note >}}

### 8. Improve the security of your CorDapp by adding BelongsToContract annotations

Before platform version 4, the contract and flow logic ensured that the `TransactionState` objects
contained the correct class name of the expected contract class. If these checks are omitted, it's possible for a malicious counterparty
to construct a transaction, for example, a cash state governed by a commercial paper contract. The contract would see that there were no
commercial paper states in a transaction and do nothing (in other words, it will accept the transaction).

In Corda 4, if the CorDapp has a target platform version of 4 or higher, the platform is responsible for checking the `TransactionState` objects
contain the correct class name of the expected contract class.
 A state is expected
to be governed by a contract that is either:


* The outer class of the state class, if the state is an inner class of a contract. This is a common design pattern.
* Annotated with `@BelongsToContract` which specifies the contract class explicitly.

You can learn more by reading [contract/state agreement](cordapps/api-contract-constraints.html#contractstate-agreement).

If a CorDapp targets Corda 3 or lower (does not specify a target version),
states that point to contracts outside their package will trigger a log warning but validation will proceed.


### 9. Learn about signature constraints and signing `.jar` files

[Signature constraints](cordapps/api-contract-constraints.html#signature-constraints) are a new data model feature introduced in Corda 4. They make it much easier to smoothly
deploy application upgrades in a decentralised manner. Signature constraints are the new default mode for CorDapps. Upgrading your CorDapp to use version 4 Gradle plugins will mean your CorDapp is automatically signed, and new states will use new signature constraints selected automatically based on these signing keys.


{{< important >}}
You can use this feature if you plan to deploy to a compatibility zone that has raised its minimum platform version to check the correctness of the transaction. Please take this into account for your own schedule planning.

You can find out more about signature constraints and what they do by reading [CorDapp constraints migration](cordapps/cordapp-constraint-migration.md). The `TransactionBuilder` class will automatically use them if your CorDapp `.jar` file is signed. *We recommend all `.jar` files are signed*. Read [Sign the CorDapp](cordapps/cordapp-build-systems.html#sign-the-cordapp) to learn how to sign your `.jar` files. In dev mode, all `.jar` files are signed by developer certificates. If a `.jar` file has been signed with developer certificates and is deployed to a production node, the node will refuse to start. Therefore, to deploy CorDapps built for Corda 4 to production, you will need to generate signing keys and integrate them with the build process.


{{< /important >}}


{{< note >}}
You can find out how to upgrade CorDapps to use Corda 4 signature constraints and consume
existing states on ledger issued with older constraint types (such as Corda 3.x states issued with **hash** or **CZ whitelisted** constraints) by reading the [CorDapp constraints migration](cordapps/cordapp-constraint-migration.md) guide.

{{< /note >}}

### 10. Improve the security of your CorDapp: Package namespace handling

{{< note >}}
These changes are unlikely to affect many CorDapps, but you should still be aware of them.

{{< /note >}}

We have made two improvements to how Java package protection is handled in Corda 4:

* Package sealing.
* Package namespace ownership.

#### Package sealing
Version 4 of the finance CorDapp (`corda-finance-contracts.jar`, `corda-finance-workflows.jar`) is now built as a set of sealed and
signed `.jar` files. This means classes in your own CorDapps can't be placed under the package namespace `net.corda.finance`.

In the unlikely event that you were injecting code into `net.corda.finance.*` package namespaces from your own CorDapps, you will need to move them
into a new package. For example, `net/corda/finance/flows/MyClass.java` can be moved to `com/company/corda/finance/flows/MyClass.java`.
As a consequence your classes are no longer able to access non-public members of finance CorDapp classes.

When signing your `.jar` files for Corda 4, your own apps will also become sealed, meaning other `.jar` files cannot place classes into your packages.
This is a security upgrade that ensures package-private visibility in Java code works correctly. If other CorDapps could define classes in your
packages, they could call package-private methods, which may not be expected by the developers.

#### Package namespace ownership
This change is only relevant if you are joining a production compatibility zone. You may wish to contact your zone operator
and request ownership of your root package namespaces (for example `com.megacorp.*`), with the signing keys you will be using to sign your CorDapp `.jar` files.
The zone operator can then add your signing key to the network parameters, and prevent attackers defining types in your package namespaces.
Whilst this feature is optional and not strictly required, it may be helpful to block attacks at the boundaries of a Corda-based application
where type names may be taken ”as read”. You can learn more about this feature by reading
[package namespace ownership](node/deploy/env-dev.html#package-namespace-ownership).


### 11. Consider adding extension points to your flows

In Corda 4 it's possible for flows in one CorDapp to subclass and take over flows from another. This allows you to create generic, shared
flow logic that individual users can customise at pre-agreed points (protected methods). For example, a site-specific CorDapp could be developed
that converts transaction details into a PDF, which is then sent to a particular printer. This would be an inappropriate feature to put
into shared business logic, but not for a user-specific CorDapp that they've developed themselves.

If your flows could benefit from being extended in this way, see [overriding a flow via node configuration](cordapps/flow-overriding.html#overriding-a-flow-via-node-configuration).

### 12. Update vault state queries

In Corda 4, queries made on a node's vault can be filtered by the relevancy of those states to the node. As this functionality doesn't exist in
Corda 3, CorDapps will continue to receive all states relating to any vault queries. You may want to migrate queries that expect states that are only relevant
to the node in question, so you can filter them by relevant states. See [writing vault queries](cordapps/api-vault-query.md) for more details on how to do this. If you decide not to do this, queries may return more states than expected if the node is using observer functionality. See [Posting transactions to observer nodes](../../../../tutorials/corda/4.10/community/supplementary-tutorials/tutorial-observer-nodes.md) for more information.

### 13. Update your `quasar.jar` file

If your project is based on one of the official CorDapp templates, you'll likely have a `lib/quasar.jar` file checked in. You'll only use this if you use the JUnit runner in IntelliJ. In the latest release of the CorDapp templates, this directory has
been removed.

You can do either of the following.

* Upgrade your `quasar.jar` file to `0.7.14_r3`.
* Delete your `lib` directory and switch to using the Gradle test runner.

You can find instructions for both options in [Running tests in IntelliJ](../community/testing.html#running-tests-in-intellij).

### 14. Other features that you may find useful
There are several new APIs in the Corda 4 release that can help you build your application.

* The new `withEntityManager` API allows you to use JPA inside your flows and services.
* **Reference states** let you use an input state without consuming it.
* **State pointers** make it easier to ‘point’ to one state from another, and follow the latest version of a linear state.

Please also read the [CorDapp upgradeability guarantees](cordapps/cordapp-upgradeability.md).
