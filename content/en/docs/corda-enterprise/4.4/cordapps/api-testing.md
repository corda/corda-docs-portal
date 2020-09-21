---
aliases:
- /releases/4.4/cordapps/api-testing.html
- /docs/corda-enterprise/head/cordapps/api-testing.html
- /docs/corda-enterprise/cordapps/api-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-cordapps-debugging
tags:
- api
- testing
title: "Testing a CorDapp"
weight: 1
---

# Testing CorDapps

## Flow testing

### MockNetwork

Flow testing can be fully automated using a `MockNetwork` composed of `StartedMockNode` nodes. Each
`StartedMockNode` behaves like a regular Corda node, but its services are either in-memory or mocked out.

A `MockNetwork` is created as follows:

{{< tabs name="tabs-1" >}}
{{< /tabs >}}

The `MockNetwork` requires at a minimum a list of CorDapps to be installed on each `StartedMockNode`. The CorDapps are looked up on the
classpath by package name, using `TestCordapp.findCordapp`. `TestCordapp.findCordapp` scans the current classpath to find the CorDapp that contains the given package.
This includes all the associated CorDapp metadata present in its MANIFEST.

`MockNetworkParameters` provides other properties for the network which can be tweaked. They default to sensible values if not specified.


### Adding nodes to the network

Nodes are created on the `MockNetwork` using:

{{< tabs name="tabs-2" >}}
{{< /tabs >}}

Nodes added using `createNode` are provided a default set of node parameters. However, it is also possible to
provide different parameters to each node using `MockNodeParameters`. Of particular interest are `configOverrides` which allow you to
override some of the default node configuration options. Please refer to the `MockNodeConfigOverrides` class for details what can currently
be overridden. Also, the `additionalCordapps` parameter allows you to add extra CorDapps to a specific node. This is useful when you wish
for all nodes to load a common CorDapp but for a subset of nodes to load CorDapps specific to their role in the network.


### Running the network

When using a `MockNetwork`, you must be careful to ensure that all the nodes have processed all the relevant messages
before making assertions about the result of performing some action. For example, if you start a flow to update the ledger
but don’t wait until all the nodes involved have processed all the resulting messages, your nodes’ vaults may not be in
the state you expect.

When `networkSendManuallyPumped` is set to `false`, you must manually initiate the processing of received messages.
You manually process received messages as follows:


* `StartedMockNode.pumpReceive()` processes a single message from the node’s queue
* `MockNetwork.runNetwork()` processes all the messages in every node’s queue until there are no further messages to
process

When `networkSendManuallyPumped` is set to `true`, nodes will automatically process the messages they receive. You
can block until all messages have been processed using `MockNetwork.waitQuiescent()`.


{{< warning >}}
If `threadPerNode` is set to `true`, `networkSendManuallyPumped` must also be set to `true`.

{{< /warning >}}



### Running flows

A `StartedMockNode` starts a flow using the `StartedNodeServices.startFlow` method. This method returns a future
representing the output of running the flow.

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
val signedTransactionFuture = nodeA.services.startFlow(IOUFlow(iouValue = 99, otherParty = nodeBParty))
```
{{% /tab %}}

{{% tab name="java" %}}
```java
CordaFuture<SignedTransaction> future = startFlow(a.getServices(), new ExampleFlow.Initiator(1, nodeBParty));
```
{{% /tab %}}

{{< /tabs >}}

The network must then be manually run before retrieving the future’s value:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
val signedTransactionFuture = nodeA.services.startFlow(IOUFlow(iouValue = 99, otherParty = nodeBParty))
// Assuming network.networkSendManuallyPumped == false.
network.runNetwork()
val signedTransaction = future.get();
```
{{% /tab %}}

{{% tab name="java" %}}
```java
CordaFuture<SignedTransaction> future = startFlow(a.getServices(), new ExampleFlow.Initiator(1, nodeBParty));
// Assuming network.networkSendManuallyPumped == false.
network.runNetwork();
SignedTransaction signedTransaction = future.get();
```
{{% /tab %}}

{{< /tabs >}}


### Accessing `StartedMockNode` internals


#### Querying a node’s vault

Recorded states can be retrieved from the vault of a `StartedMockNode` using:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
val myStates = nodeA.services.vaultService.queryBy<MyStateType>().states
```
{{% /tab %}}

{{% tab name="java" %}}
```java
List<MyStateType> myStates = node.getServices().getVaultService().queryBy(MyStateType.class).getStates();
```
{{% /tab %}}

{{< /tabs >}}

This allows you to check whether a given state has (or has not) been stored, and whether it has the correct attributes.


#### Examining a node’s transaction storage

Recorded transactions can be retrieved from the transaction storage of a `StartedMockNode` using:

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
val transaction = nodeA.services.validatedTransactions.getTransaction(transaction.id)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
SignedTransaction transaction = nodeA.getServices().getValidatedTransactions().getTransaction(transaction.getId())
```
{{% /tab %}}

{{< /tabs >}}

This allows you to check whether a given transaction has (or has not) been stored, and whether it has the correct
attributes.

### Further examples


* See the flow testing tutorial here
* See the oracle tutorial here for information on testing `@CordaService` classes
* Further examples are available in the Example CorDapp in
[Java](https://github.com/corda/samples/blob/release-V4/cordapp-example/workflows-java/src/test/java/com/example/test/flow/IOUFlowTests.java) and
[Kotlin](https://github.com/corda/samples/blob/release-V4/cordapp-example/workflows-kotlin/src/test/kotlin/com/example/test/flow/IOUFlowTests.kt)


## Contract testing

The Corda test framework includes the ability to create a test ledger by calling the `ledger` function
on an implementation of the `ServiceHub` interface.


### Test identities

You can create dummy identities to use in test transactions using the `TestIdentity` class:

{{< tabs name="tabs-7" >}}
{{< /tabs >}}

`TestIdentity` exposes the following fields and methods:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
val identityParty: Party = bigCorp.party
val identityName: CordaX500Name = bigCorp.name
val identityPubKey: PublicKey = bigCorp.publicKey
val identityKeyPair: KeyPair = bigCorp.keyPair
val identityPartyAndCertificate: PartyAndCertificate = bigCorp.identity
```
{{% /tab %}}

{{% tab name="java" %}}
```java
Party identityParty = bigCorp.getParty();
CordaX500Name identityName = bigCorp.getName();
PublicKey identityPubKey = bigCorp.getPublicKey();
KeyPair identityKeyPair = bigCorp.getKeyPair();
PartyAndCertificate identityPartyAndCertificate = bigCorp.getIdentity();
```
{{% /tab %}}

{{< /tabs >}}

You can also create a unique `TestIdentity` using the `fresh` method:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
val uniqueTestIdentity: TestIdentity = TestIdentity.fresh("orgName")
```
{{% /tab %}}

{{% tab name="java" %}}
```java
TestIdentity uniqueTestIdentity = TestIdentity.Companion.fresh("orgName");
```
{{% /tab %}}

{{< /tabs >}}


### MockServices

A mock implementation of `ServiceHub` is provided in `MockServices`. This is a minimal `ServiceHub` that
suffices to test contract logic. It has the ability to insert states into the vault, query the vault, and
construct and check transactions.

{{< tabs name="tabs-10" >}}
{{< /tabs >}}

Alternatively, there is a helper constructor which just accepts a list of `TestIdentity`. The first identity provided is
the identity of the node whose `ServiceHub` is being mocked, and any subsequent identities are identities that the node
knows about. Only the calling package is scanned for cordapps and a test `IdentityService` is created
for you, using all the given identities.

{{< tabs name="tabs-11" >}}
{{< /tabs >}}


### Writing tests using a test ledger

The `ServiceHub.ledger` extension function allows you to create a test ledger. Within the ledger wrapper you can create
transactions using the `transaction` function. Within a transaction you can define the `input` and
`output` states for the transaction, alongside any commands that are being executed, the `timeWindow` in which the
transaction has been executed, and any `attachments`, as shown in this example test:

{{< tabs name="tabs-12" >}}
{{< /tabs >}}

Once all the transaction components have been specified, you can run `verifies()` to check that the given transaction is valid.


#### Checking for failure states

In order to test for failures, you can use the `failsWith` method, or in Kotlin the `fails with` helper method, which
assert that the transaction fails with a specific error. If you just want to assert that the transaction has failed without
verifying the message, there is also a `fails` method.

{{< tabs name="tabs-13" >}}
{{< /tabs >}}

{{< note >}}
The transaction DSL forces the last line of the test to be either a `verifies` or `fails with` statement.

{{< /note >}}

#### Testing multiple scenarios at once

Within a single transaction block, you can assert several times that the transaction constructed so far either passes or
fails verification. For example, you could test that a contract fails to verify because it has no output states, and then
add the relevant output state and check that the contract verifies successfully, as in the following example:

{{< tabs name="tabs-14" >}}
{{< /tabs >}}

You can also use the `tweak` function to create a locally scoped transaction that you can make changes to
and then return to the original, unmodified transaction. As in the following example:

{{< tabs name="tabs-15" >}}
{{< /tabs >}}


#### Chaining transactions

The following example shows that within a `ledger`, you can create more than one `transaction` in order to test chains
of transactions. In addition to `transaction`, `unverifiedTransaction` can be used, as in the example below, to create
transactions on the ledger without verifying them, for pre-populating the ledger with existing data. When chaining transactions,
it is important to note that even though a `transaction` `verifies` successfully, the overall ledger may not be valid. This can
be verified separately by placing a `verifies` or `fails` statement  within the `ledger` block.

{{< tabs name="tabs-16" >}}
{{< /tabs >}}


### Further examples


* See the flow testing tutorial here
* Further examples are available in the Example CorDapp in
[Java](https://github.com/corda/samples/blob/release-V4/cordapp-example/workflows-java/src/test/java/com/example/test/flow/IOUFlowTests.java) and
[Kotlin](https://github.com/corda/samples/blob/release-V4/cordapp-example/workflows-kotlin/src/test/kotlin/com/example/test/flow/IOUFlowTests.kt)
