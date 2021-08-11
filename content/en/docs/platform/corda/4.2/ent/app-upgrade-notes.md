---
aliases:
- /releases/4.2/app-upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- app
- upgrade
- notes
title: Upgrading apps to Corda 4
---




# Upgrading apps to Corda 4

These notes provide instructions for upgrading your CorDapps from previous versions. Corda provides backwards compatibility for public,
non-experimental APIs that have been committed to. A list can be found in the [Corda API](corda-api.md) page.

This means that you can upgrade your node across versions *without recompiling or adjusting your CorDapps*. You just have to upgrade
your node and restart.

However, there are usually new features and other opt-in changes that may improve the security, performance or usability of your
application that are worth considering for any actively maintained software. This guide shows you how to upgrade your app to benefit
from the new features in the latest release.


{{< warning >}}
The sample apps found in the Corda repository and the Corda samples repository are not intended to be used in production.
If you are using them you should re-namespace them to a package namespace you control, and sign/version them yourself.

{{< /warning >}}




## Step 1. Switch any RPC clients to use the new RPC library

Although the RPC API is backwards compatible with Corda 3, the RPC wire protocol isn’t. Therefore RPC clients like web servers need to be
updated in lockstep with the node to use the new version of the RPC library. Corda 4 delivers RPC wire stability and therefore in future you
will be able to update the node and apps without updating RPC clients.



## Step 2. Adjust the version numbers in your Gradle build files

Alter the versions you depend on in your Gradle file like so:

```groovy
ext.corda_release_version = '4.2'
ext.corda_gradle_plugins_version = '4.0.42'
ext.kotlin_version = '1.2.71'
ext.quasar_version = '0.7.11_r3'
```

You also need a add `corda-dependencies` to the list of repositories to make the custom built version of Quasar available:

```groovy
repositories {
    mavenCentral()
    jcenter()
    // ... Repository access for Corda Enterprise and any other dependencies
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Quasar version
}
```

{{< note >}}
You may wish to update your kotlinOptions to use language level 1.2, to benefit from the new features. Apps targeting Corda 4
may not at this time use Kotlin 1.3, as it was released too late in the development cycle
for us to risk an upgrade. Sorry! Future work on app isolation will make it easier for apps to use newer Kotlin versions than
the node itself uses.

{{< /note >}}
You should also ensure you’re using Gradle 4.10 (but not 5). If you use the Gradle wrapper, run:

```kotlin
./gradlew wrapper --gradle-version 4.10.3
```

Otherwise just upgrade your installed copy in the usual manner for your operating system.


## Step 3. Update your Gradle build file

There are several adjustments that are beneficial to make to your Gradle build file, beyond simply incrementing the versions
as described in step 1.

**Provide app metadata.** This is used by the Corda Gradle build plugin to populate your app JAR with useful information.
It should look like this:

```kotlin
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

Name, vendor and licence can be set to any string you like, they don’t have to be Corda identities.

Target versioning is a new concept introduced in Corda 4. Learn more by reading [Versioning](versioning.md).
Setting a target version of 4 opts in to changes that might not be 100% backwards compatible, such as
API semantics changes or disabling workarounds for bugs that may be in your apps, so by doing this you
are promising that you have thoroughly tested your app on the new version. Using a high target version is
a good idea because some features and improvements are only available to apps that opt in.

The minimum platform version is the platform version of the node that you require, so if you
start using new APIs and features in Corda 4, you should set this to 4. Unfortunately Corda 3 and below
do not know about this metadata and don’t check it, so your app will still be loaded in such nodes and
may exhibit undefined behaviour at runtime. However it’s good to get in the habit of setting this
properly for future releases.

{{< note >}}
Whilst it’s currently a convention that Corda releases have the platform version number as their
major version i.e. Corda 3.4 implements platform version 3, this is not actually required and may in
future not hold true. You should know the platform version of the node releases you want to target.

{{< /note >}}
The new `versionId` number is a version code for **your** app, and is unrelated to Corda’s own versions.
It is used to informative purposes only. See “[App versioning with Signature Constraints](api-contract-constraints.md#app-versioning-with-signature-constraints)” for more information.

**Split your app into contract and workflow JARs.** The duplication between `contract` and `workflow` blocks exists because you should split your app into
two separate JARs/modules, one that contains on-ledger validation code like states and contracts, and one
for the rest (called by convention the “workflows” module although it can contain a lot more than just flows:
services would also go here, for instance). For simplicity, here we use one JAR for both, but this is in
general an anti-pattern and can result in your flow logic code being sent over the network to arbitrary
third party peers, even though they don’t need it.

In future, the version ID attached to the workflow JAR will also be used to help implement smoother upgrade
and migration features. You may directly reference the gradle version number of your app when setting the
CorDapp specific versionId identifiers if this follows the convention of always being a whole number
starting from 1.

If you use the finance demo app, you should adjust your dependencies so you depend on the finance-contracts
and finance-workflows artifacts from your own contract and workflow JAR respectively.


## Step 4. Remove any custom configuration from the node.conf

CorDapps can no longer access custom configuration items in the `node.conf` file. Any custom CorDapp configuration should be added to a
CorDapp configuration file. The Node’s configuration will not be accessible. CorDapp configuration files should be placed in the
*config* subdirectory of the Node’s *cordapps* folder. The name of the file should match the name of the JAR of the CorDapp (eg; if your
CorDapp is called `hello-0.1.jar` the configuration file needed would be `cordapps/config/hello-0.1.conf`).

If you are using the `extraConfig` of a `node` in the `deployNodes` Gradle task to populate custom configuration for testing, you will need
to make the following change so that:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    node {
        name "O=Bank A,L=London,C=GB"c
        ...
        extraConfig = [ 'some.extra.config' : '12345' ]
    }
}
```

Would become:

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

See [CorDapp configuration files](cordapp-build-systems.md#cordapp-configuration-files-ref) for more information.



## Step 5. Security: Upgrade your use of FinalityFlow

The previous `FinalityFlow` API is insecure. It doesn’t have a receive flow, so requires counterparty nodes to accept any and
all signed transactions that are sent to it, without checks. It is **highly** recommended that existing CorDapps migrate
away to the new API, as otherwise things like business network membership checks won’t be reliably enforced.

The flows that make use of `FinalityFlow` in a CorDapp can be classified in the following 2 basic categories:


* **non-initiating flows**: these are flows that finalise a transaction without the involvement of a counterpart flow at all.
* **initiating flows**: these are flows that initiate a counterpart (responder) flow.

There is a main difference between these 2 different categories, which is relevant to how the CorDapp can be upgraded.
The second category of flows can be upgraded to use the new `FinalityFlow` in a backwards compatible way, which means the upgraded CorDapp can be deployed at the various nodes using a *rolling deployment*.
On the other hand, the first category of flows cannot be upgraded to the new `FinalityFlow` in a backwards compatible way, so the changes to these flows need to be deployed simultaneously at all the nodes, using a *lockstep deployment*.

{{< note >}}
A *lockstep deployment* is one, where all the involved nodes are stopped, upgraded to the new version of the CorDapp and then re-started.
As a result, there can’t be any nodes running different versions of the CorDapp at any time.
A *rolling deployment* is one, where every node can be stopped, upgraded to the new version of the CorDapp and re-started independently and on its own pace.
As a result, there can be nodes running different versions of the CorDapp and transact with each other successfully.

{{< /note >}}
The upgrade is a three step process:


* Change the flow that calls `FinalityFlow`.
* Change or create the flow that will receive the finalised transaction.
* Make sure your application’s minimum and target version numbers are both set to 4 (see [Step 2. Adjust the version numbers in your Gradle build files](#cordapp-upgrade-version-numbers-ref)).


### Upgrading a non-initiating flow

As an example, let’s take a very simple flow that finalises a transaction without the involvement of a counterpart flow:

{{< tabs name="tabs-1" >}}
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
    public SignedTransaction call() throws FlowException {
        SignedTransaction stx = dummyTransactionWithParticipant(counterparty);
        return subFlow(new FinalityFlow(stx));
    }

```
{{% /tab %}}




[FinalityFlowMigration.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FinalityFlowMigration.kt) | [FinalityFlowMigration.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/FinalityFlowMigration.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

To use the new API, this flow needs to be annotated with `InitiatingFlow` and a `FlowSession` to the participant(s) of the transaction must be
passed to `FinalityFlow` :

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Notice how the flow *must* now be an initiating flow even when it wasn't before.
@InitiatingFlow
class SimpleFlowUsingNewApi(private val counterparty: Party) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        val stx = dummyTransactionWithParticipant(counterparty)
        // For each non-local participant in the transaction we must initiate a flow session with them.
        val session = initiateFlow(counterparty)
        return subFlow(FinalityFlow(stx, session))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Notice how the flow *must* now be an initiating flow even when it wasn't before.
@InitiatingFlow
public static class SimpleFlowUsingNewApi extends FlowLogic<SignedTransaction> {
    private final Party counterparty;

    @Suspendable
    @Override
    public SignedTransaction call() throws FlowException {
        SignedTransaction stx = dummyTransactionWithParticipant(counterparty);
        // For each non-local participant in the transaction we must initiate a flow session with them.
        FlowSession session = initiateFlow(counterparty);
        return subFlow(new FinalityFlow(stx, session));
    }

```
{{% /tab %}}




[FinalityFlowMigration.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FinalityFlowMigration.kt) | [FinalityFlowMigration.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/FinalityFlowMigration.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

If there are more than one transaction participants then a session to each one must be initiated, excluding the local party
and the notary.

A responder flow has to be introduced, which will automatically run on the other participants’ nodes, which will call `ReceiveFinalityFlow`
to record the finalised transaction:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
// All participants will run this flow to receive and record the finalised transaction into their vault.
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
// All participants will run this flow to receive and record the finalised transaction into their vault.
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




[FinalityFlowMigration.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FinalityFlowMigration.kt) | [FinalityFlowMigration.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/FinalityFlowMigration.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

{{< note >}}
As described above, all the nodes in your business network will need the new CorDapp, otherwise they won’t know how to receive the transaction. **This
includes nodes which previously didn’t have the old CorDapp.** If a node is sent a transaction and it doesn’t have the new CorDapp loaded
then simply restart it with the CorDapp and the transaction will be recorded.

{{< /note >}}

### Upgrading an initiating flow

For flows which are already initiating counterpart flows then it’s a matter of using the existing flow session.
Note however, the new `FinalityFlow` is inlined and so the sequence of sends and receives between the two flows will
change and will be incompatible with your current flows. You can use the flow version API to write your flows in a
backwards compatible manner.

Here’s what an upgraded initiating flow may look like:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
// Assuming the previous version of the flow was 1 (the default if none is specified), we increment the version number to 2
// to allow for backwards compatibility with nodes running the old CorDapp.
@InitiatingFlow(version = 2)
class ExistingInitiatingFlow(private val counterparty: Party) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        val partiallySignedTx = dummyTransactionWithParticipant(counterparty)
        val session = initiateFlow(counterparty)
        val fullySignedTx = subFlow(CollectSignaturesFlow(partiallySignedTx, listOf(session)))
        // Determine which version of the flow that other side is using.
        return if (session.getCounterpartyFlowInfo().flowVersion == 1) {
            // Use the old API if the other side is using the previous version of the flow.
            subFlow(FinalityFlow(fullySignedTx))
        } else {
            // Otherwise they're at least on version 2 and so we can send the finalised transaction on the existing session.
            subFlow(FinalityFlow(fullySignedTx, session))
        }
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Assuming the previous version of the flow was 1 (the default if none is specified), we increment the version number to 2
// to allow for backwards compatibility with nodes running the old CorDapp.
@InitiatingFlow(version = 2)
public static class ExistingInitiatingFlow extends FlowLogic<SignedTransaction> {
    private final Party counterparty;

    @Suspendable
    @Override
    public SignedTransaction call() throws FlowException {
        SignedTransaction partiallySignedTx = dummyTransactionWithParticipant(counterparty);
        FlowSession session = initiateFlow(counterparty);
        SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(partiallySignedTx, singletonList(session)));
        // Determine which version of the flow that other side is using.
        if (session.getCounterpartyFlowInfo().getFlowVersion() == 1) {
            // Use the old API if the other side is using the previous version of the flow.
            return subFlow(new FinalityFlow(fullySignedTx));
        } else {
            // Otherwise they're at least on version 2 and so we can send the finalised transaction on the existing session.
            return subFlow(new FinalityFlow(fullySignedTx, session));
        }
    }

```
{{% /tab %}}




[FinalityFlowMigration.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FinalityFlowMigration.kt) | [FinalityFlowMigration.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/FinalityFlowMigration.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

For the responder flow, insert a call to `ReceiveFinalityFlow` at the location where it’s expecting to receive the
finalised transaction. If the initiator is written in a backwards compatible way then so must the responder.

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
// First we have to run the SignTransactionFlow, which will return a SignedTransaction.
val txWeJustSigned = subFlow(object : SignTransactionFlow(otherSide) {
    @Suspendable
    override fun checkTransaction(stx: SignedTransaction) {
        // Implement responder flow transaction checks here
    }
})

if (otherSide.getCounterpartyFlowInfo().flowVersion >= 2) {
    // The other side is not using the old CorDapp so call ReceiveFinalityFlow to record the finalised transaction.
    // If SignTransactionFlow is used then we can verify the tranaction we receive for recording is the same one
    // that was just signed.
    subFlow(ReceiveFinalityFlow(otherSide, expectedTxId = txWeJustSigned.id))
} else {
    // Otherwise the other side is running the old CorDapp and so we don't need to do anything further. The node
    // will automatically record the finalised transaction using the old insecure mechanism.
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// First we have to run the SignTransactionFlow, which will return a SignedTransaction.
SignedTransaction txWeJustSigned = subFlow(new SignTransactionFlow(otherSide) {
    @Suspendable
    @Override
    protected void checkTransaction(@NotNull SignedTransaction stx) throws FlowException {
        // Implement responder flow transaction checks here
    }
});

if (otherSide.getCounterpartyFlowInfo().getFlowVersion() >= 2) {
    // The other side is not using the old CorDapp so call ReceiveFinalityFlow to record the finalised transaction.
    // If SignTransactionFlow is used then we can verify the tranaction we receive for recording is the same one
    // that was just signed by passing the transaction id to ReceiveFinalityFlow.
    subFlow(new ReceiveFinalityFlow(otherSide, txWeJustSigned.getId()));
} else {
    // Otherwise the other side is running the old CorDapp and so we don't need to do anything further. The node
    // will automatically record the finalised transaction using the old insecure mechanism.
}

```
{{% /tab %}}




[FinalityFlowMigration.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FinalityFlowMigration.kt) | [FinalityFlowMigration.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/FinalityFlowMigration.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

You may already be using `waitForLedgerCommit` in your responder flow for the finalised transaction to appear in the local node’s vault.
Now that it’s calling `ReceiveFinalityFlow`, which effectively does the same thing, this is no longer necessary. The call to
`waitForLedgerCommit` should be removed.


## Step 6. Security: Upgrade your use of SwapIdentitiesFlow

The [Confidential identities](api-identity.md#confidential-identities-ref) API is experimental in Corda 3 and remains so in Corda 4. In this release, the `SwapIdentitiesFlow`
has been adjusted in the same way as `FinalityFlow` above, to close problems with confidential identities being injectable into a node
outside of other flow context. Old code will still work, but it is recommended to adjust your call sites so a session is passed into
the `SwapIdentitiesFlow`.


## Step 7. Possibly, adjust test code

`MockNodeParameters` and functions creating it no longer use a lambda expecting a `NodeConfiguration` object.
Use a `MockNetworkConfigOverrides` object instead. This is an API change we regret, but unfortunately in Corda 3 we accidentally exposed
large amounts of the node internal code through this one API entry point. We have now insulated the test API from node internals and
reduced the exposure.

If you are constructing a MockServices for testing contracts, and your contract uses the Cash contract from the finance app, you
now need to explicitly add `net.corda.finance.contracts` to the list of `cordappPackages`. This is a part of the work to disentangle
the finance app (which is really a demo app) from the Corda internals. Example:

```kotlin
val ledgerServices = MockServices(
    listOf("net.corda.examples.obligation", "net.corda.testing.contracts"),
    identityService = makeTestIdentityService(),
    initialIdentity = TestIdentity(CordaX500Name("TestIdentity", "", "GB"))
)
```

becomes:

```kotlin
val ledgerServices = MockServices(
    listOf("net.corda.examples.obligation", "net.corda.testing.contracts", "net.corda.finance.contracts"),
    identityService = makeTestIdentityService(),
    initialIdentity = TestIdentity(CordaX500Name("TestIdentity", "", "GB"))
)
```

You may need to use the new `TestCordapp` API when testing with the node driver or mock network, especially if you decide to stick with the
pre-Corda 4 `FinalityFlow` API. The previous way of pulling in CorDapps into your tests (i.e. via using the `cordappPackages` parameter) does not honour CorDapp versioning.
The new API `TestCordapp.findCordapp()` discovers the CorDapps that contain the provided packages scanning the classpath, so you have to ensure that the classpath the tests are running under contains either the CorDapp `.jar` or (if using Gradle) the relevant Gradle sub-project.
In the first case, the versioning information in the CorDapp `.jar` file will be maintained. In the second case, the versioning information will be retrieved from the Gradle `cordapp` task.
For example, if you are using `MockNetwork` for your tests, the following code:

```kotlin
val mockNetwork = MockNetwork(
    cordappPackages = listOf("net.corda.examples.obligation", "net.corda.finance.contracts"),
    notarySpecs = listOf(MockNetworkNotarySpec(notary))
)
```

would need to be transformed into:

```kotlin
val mockNetwork = MockNetwork(MockNetworkParameters(
    cordappsForAllNodes = listOf(TestCordapp.findCordapp("net.corda.businessnetworks.membership")),
    notarySpecs = listOf(MockNetworkNotarySpec(notary))
))
```

Note that every package should exist in only one CorDapp, otherwise the discovery process won’t be able to determine which one to use and you will most probably see an exception telling you `There is more than one CorDapp containing the package`.
For instance, if you have 2 CorDapps containing the packages `net.corda.examples.obligation.contracts` and `net.corda.examples.obligation.flows`, you will get this error if you specify the package `net.corda.examples.obligation`.

{{< note >}}
If you have any CorDapp code (e.g. flows/contracts/states) that is only used by the tests and located in the same test module, it won’t be discovered now.
You will need to move them in the main module of one of your CorDapps or create a new, separate CorDapp for them, in case you don’t want this code to live inside your production CorDapps.

{{< /note >}}

## Step 8. Security: Add BelongsToContract annotations

In versions of the platform prior to v4, it was the responsibility of contract and flow logic to ensure that `TransactionState` objects
contained the correct class name of the expected contract class. If these checks were omitted, it would be possible for a malicious counterparty
to construct a transaction containing e.g. a cash state governed by a commercial paper contract. The contract would see that there were no
commercial paper states in a transaction and do nothing, i.e. accept.

In Corda 4 the platform takes over this responsibility from the app, if the app has a target version of 4 or higher. A state is expected
to be governed by a contract that is either:


* The outer class of the state class, if the state is an inner class of a contract. This is a common design pattern.
* Annotated with `@BelongsToContract` which specifies the contract class explicitly.

Learn more by reading [Contract/State Agreement](api-contract-constraints.md#contract-state-agreement). If an app targets Corda 3 or lower (i.e. does not specify a target version),
states that point to contracts outside their package will trigger a log warning but validation will proceed.


## Step 9. Learn about signature constraints and JAR signing

[Signature Constraints](api-contract-constraints.md#signature-constraints) are a new data model feature introduced in Corda 4. They make it much easier to
deploy application upgrades smoothly and in a decentralised manner. Signature constraints are the new default mode for CorDapps, and
the act of upgrading your app to use the version 4 Gradle plugins will result in your app being automatically signed, and new states
automatically using new signature constraints selected automatically based on these signing keys.


{{< important >}}
You will be able to use this feature if the compatibility zone you plan to deploy on has raised its minimum platform version


{{< /important >}}

to check the correctness of the transaction. Please take this into account for your own schedule planning.You can read more about signature constraints and what they do in [API: Contract Constraints](api-contract-constraints.md). The `TransactionBuilder` class will
automatically use them if your application JAR is signed. **We recommend all JARs are signed**. To learn how to sign your JAR files, read
[Signing the CorDapp JAR](cordapp-build-systems.md#cordapp-build-system-signing-cordapp-jar-ref). In dev mode, all JARs are signed by developer certificates. If a JAR that was signed
with developer certificates is deployed to a production node, the node will refuse to start. Therefore to deploy apps built for Corda 4
to production you will need to generate signing keys and integrate them with the build process.

{{< note >}}
Please read the [CorDapp constraints migration](cordapp-constraint-migration.md) guide to understand how to upgrade CorDapps to use Corda 4 signature constraints and consume
existing states on ledger issued with older constraint types (e.g. Corda 3.x states issued with **hash** or **CZ whitelisted** constraints).

{{< /note >}}

## Step 10. Security: Package namespace handling

Almost no apps will be affected by these changes, but they’re important to know about.

There are two improvements to how Java package protection is handled in Corda 4:


* Package sealing
* Package namespace ownership

**Sealing.** App isolation has been improved. Version 4 of the finance CorDapps (*corda-finance-contracts.jar*, *corda-finance-workflows.jar*) is now built as a set of sealed and
signed JAR files. This means classes in your own CorDapps cannot be placed under the following package namespace:  `net.corda.finance`

In the unlikely event that you were injecting code into `net.corda.finance.*` package namespaces from your own apps, you will need to move them
into a new package, e.g. `net/corda/finance/flows/MyClass.java` can be moved to `com/company/corda/finance/flows/MyClass.java`.
As a consequence your classes are no longer able to access non-public members of finance CorDapp classes.

When signing your JARs for Corda 4, your own apps will also become sealed, meaning other JARs cannot place classes into your own packages.
This is a security upgrade that ensures package-private visibility in Java code works correctly. If other apps could define classes in your own
packages, they could call package-private methods, which may not be expected by the developers.

**Namespace ownership.** This part is only relevant if you are joining a production compatibility zone. You may wish to contact your zone operator
and request ownership of your root package namespaces (e.g. `com.megacorp.*`), with the signing keys you will be using to sign your app JARs.
The zone operator can then add your signing key to the network parameters, and prevent attackers defining types in your own package namespaces.
Whilst this feature is optional and not strictly required, it may be helpful to block attacks at the boundaries of a Corda based application
where type names may be taken “as read”. You can learn more about this feature and the motivation for it by reading
“[Package namespace ownership](network-bootstrapper.md#package-namespace-ownership)”.


## Step 11. Consider adding extension points to your flows

In Corda 4 it is possible for flows in one app to subclass and take over flows from another. This allows you to create generic, shared
flow logic that individual users can customise at pre-agreed points (protected methods). For example, a site-specific app could be developed
that causes transaction details to be converted to a PDF and sent to a particular printer. This would be an inappropriate feature to put
into shared business logic, but it makes perfect sense to put into a user-specific app they developed themselves.

If your flows could benefit from being extended in this way, read “[Configuring Responder Flows](flow-overriding.md)” to learn more.


## Step 12. Possibly update vault state queries

In Corda 4 queries made on a node’s vault can filter by the relevancy of those states to the node. As this functionality does not exist in
Corda 3, apps will continue to receive all states in any vault queries. However, it may make sense to migrate queries expecting just those states relevant
to the node in question to query for only relevant states. See [API: Vault Query](api-vault-query.md) for more details on how to do this. Not doing this
may result in queries returning more states than expected if the node is using observer functionality (see “[Observer nodes](tutorial-observer-nodes.md)”).


## Step 13. Explore other new features that may be useful

Corda 4 adds several new APIs that help you build applications. Why not explore:


* The [new withEntityManager API](https://api.corda.net/api/corda-os/4.2/html/api/javadoc/net/corda/core/node/ServiceHub.html#withEntityManager-block-) for using JPA inside your flows and services.
* [Reference States](api-states.md#reference-states), that let you use an input state without consuming it.
* [State Pointers](api-states.md#state-pointers), that make it easier to ‘point’ to one state from another and follow the latest version of a linear state.

Please also read the [CorDapp Upgradeability Guarantees](cordapp-upgradeability.md) associated with CorDapp upgrading.


## Step 14. Possibly update your checked in quasar.jar

If your project is based on one of the official cordapp templates, it is likely you have a `lib/quasar.jar` checked in.  It is worth noting
that you only use this if you use the JUnit runner in IntelliJ.  In the latest release of the cordapp templates, this directory has
been removed.

You have some choices here:


* Upgrade your `quasar.jar` to `0.7.11_r3`
* Delete your `lib` directory and switch to using the Gradle test runner

Instructions for both options can be found in [Running tests in Intellij](tutorial-cordapp.md#tutorial-cordapp-running-tests-intellij).
