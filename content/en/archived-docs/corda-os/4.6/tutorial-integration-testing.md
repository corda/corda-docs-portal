---
aliases:
- /head/tutorial-integration-testing.html
- /HEAD/tutorial-integration-testing.html
- /tutorial-integration-testing.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-tutorial-integration-testing
    parent: corda-os-4-6-core-tutorials-index
    weight: 1150
tags:
- tutorial
- integration
- testing
title: Integration testing
---




# Conducting integration testing

This tutorial will take you through the steps involved in conducting integration testing on your CorDapp.

## Introduction

Integration testing involves bringing up nodes locally and testing invariants about them by starting flows and inspecting
their state.

In this tutorial, you will bring up three nodes - Alice, Bob, and a notary. Alice will issue cash to Bob, then Bob will send
this cash back to Alice. You will see how to test some simple deterministic and nondeterministic invariants in the meantime.

{{< note >}}
This example where Alice is self-issuing cash is purely for demonstration purposes; in reality, cash would be
issued by a bank and subsequently passed around.
{{< /note >}}

##  Starting the nodes

In order to spawn nodes, you will use the Driver DSL. This DSL allows you to start up node processes from code. It creates
a local network where all the nodes see each other and enables the safe shutting down of nodes in the background.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
driver(DriverParameters(startNodesInProcess = true, cordappsForAllNodes = FINANCE_CORDAPPS)) {
    val aliceUser = User("aliceUser", "testPassword1", permissions = setOf(
            startFlow<CashIssueAndPaymentFlow>(),
            invokeRpc("vaultTrackBy")
    ))

    val bobUser = User("bobUser", "testPassword2", permissions = setOf(
            startFlow<CashPaymentFlow>(),
            invokeRpc("vaultTrackBy")
    ))

    val (alice, bob) = listOf(
            startNode(providedName = ALICE_NAME, rpcUsers = listOf(aliceUser)),
            startNode(providedName = BOB_NAME, rpcUsers = listOf(bobUser))
    ).map { it.getOrThrow() }

```
{{% /tab %}}



{{% tab name="java" %}}
```java
driver(new DriverParameters()
        .withStartNodesInProcess(true)
        .withCordappsForAllNodes(FINANCE_CORDAPPS), dsl -> {

    User aliceUser = new User("aliceUser", "testPassword1", new HashSet<>(asList(
            startFlow(CashIssueAndPaymentFlow.class),
            invokeRpc("vaultTrack")
    )));

    User bobUser = new User("bobUser", "testPassword2", new HashSet<>(asList(
            startFlow(CashPaymentFlow.class),
            invokeRpc("vaultTrack")
    )));

    try {
        List<CordaFuture<NodeHandle>> nodeHandleFutures = asList(
                dsl.startNode(new NodeParameters().withProvidedName(ALICE_NAME).withRpcUsers(singletonList(aliceUser))),
                dsl.startNode(new NodeParameters().withProvidedName(BOB_NAME).withRpcUsers(singletonList(bobUser)))
        );

        NodeHandle alice = nodeHandleFutures.get(0).get();
        NodeHandle bob = nodeHandleFutures.get(1).get();

```
{{% /tab %}}
{{< /tabs >}}

The above code starts two nodes:

* A node for Alice, configured with an RPC user who has permissions to start the `CashIssueAndPaymentFlow` flow on it and query
Alice’s vault.
* A node for Bob, configured with an RPC user who only has permissions to start the `CashPaymentFlow` and query Bob’s vault.

{{< note >}}
You will notice that the code samples provided did not include how to start a notary. This is done automatically for you by the driver - it creates
a notary node with the name `DUMMY_NOTARY_NAME` which is visible to both nodes. If you wish to customise this, for
example, to create more notaries, then specify the `DriverParameters.notarySpecs` parameter.
{{< /note >}}

The `startNode` function returns a `CordaFuture` object that completes once the node is fully started and visible on
the local network. Returning a future allows starting of the nodes to be parallel. You must wait for the `CordaFuture` objects to complete, as to proceed, you will need the  `NodeHandles` for each object.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val aliceClient = CordaRPCClient(alice.rpcAddress)
val aliceProxy: CordaRPCOps = aliceClient.start("aliceUser", "testPassword1").proxy

val bobClient = CordaRPCClient(bob.rpcAddress)
val bobProxy: CordaRPCOps = bobClient.start("bobUser", "testPassword2").proxy

```
{{% /tab %}}



{{% tab name="java" %}}
```java
CordaRPCClient aliceClient = new CordaRPCClient(alice.getRpcAddress());
CordaRPCOps aliceProxy = aliceClient.start("aliceUser", "testPassword1").getProxy();

CordaRPCClient bobClient = new CordaRPCClient(bob.getRpcAddress());
CordaRPCOps bobProxy = bobClient.start("bobUser", "testPassword2").getProxy();

```
{{% /tab %}}
{{< /tabs >}}

## Connecting to each node via RPC

Next, you must connect to Alice and Bob from the test process using the test users created earlier. To be able to start flows and query states, you must establish an RPC connection to each node.

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
val bobVaultUpdates: Observable<Vault.Update<Cash.State>> = bobProxy.vaultTrackBy<Cash.State>().updates
val aliceVaultUpdates: Observable<Vault.Update<Cash.State>> = aliceProxy.vaultTrackBy<Cash.State>().updates

```
{{% /tab %}}



{{% tab name="java" %}}
```java
Observable<Vault.Update<Cash.State>> bobVaultUpdates = bobProxy.vaultTrack(Cash.State.class).getUpdates();
Observable<Vault.Update<Cash.State>> aliceVaultUpdates = aliceProxy.vaultTrack(Cash.State.class).getUpdates();

```
{{% /tab %}}

{{< /tabs >}}

## Monitoring changes to the vaults

You will be interested in changes to Alice’s and Bob’s vault, so you need to set up queries to return a stream of vault updates from each.

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
val issueRef = OpaqueBytes.of(0)
aliceProxy.startFlow(::CashIssueAndPaymentFlow,
        1000.DOLLARS,
        issueRef,
        bob.nodeInfo.singleIdentity(),
        true,
        defaultNotaryIdentity
).returnValue.getOrThrow()

bobVaultUpdates.expectEvents {
    expect { update ->
        println("Bob got vault update of $update")
        val amount: Amount<Issued<Currency>> = update.produced.first().state.data.amount
        assertEquals(1000.DOLLARS, amount.withoutIssuer())
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
OpaqueBytes issueRef = OpaqueBytes.of((byte)0);
aliceProxy.startFlowDynamic(
        CashIssueAndPaymentFlow.class,
        DOLLARS(1000),
        issueRef,
        bob.getNodeInfo().getLegalIdentities().get(0),
        true,
        dsl.getDefaultNotaryIdentity()
).getReturnValue().get();

@SuppressWarnings("unchecked")
Class<Vault.Update<Cash.State>> cashVaultUpdateClass = (Class<Vault.Update<Cash.State>>)(Class<?>)Vault.Update.class;

expectEvents(bobVaultUpdates, true, () ->
        expect(cashVaultUpdateClass, update -> true, update -> {
            System.out.println("Bob got vault update of " + update);
            Amount<Issued<Currency>> amount = update.getProduced().iterator().next().getState().getData().getAmount();
            assertEquals(DOLLARS(1000), Structures.withoutIssuer(amount));
            return null;
        })
);

```
{{% /tab %}}

{{< /tabs >}}

## Starting a flow

Now that you’re all set up, you can finally get some cash action going!

The code in the example below will start a `CashIssueAndPaymentFlow` flow on the Alice node. It specifies that you want Alice to self-issue $1000 which is
to be paid to Bob. It also specifies that the default notary identity created by the driver is the notary responsible for notarising
the created states. Note that no notarisation will occur yet, as you're not spending any states - you're only creating new ones on
the ledger.

We expect a single update to Bob’s vault when it receives the $1000 from Alice. This is what the `expectEvents` call
is asserting.

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
bobProxy.startFlow(::CashPaymentFlow, 1000.DOLLARS, alice.nodeInfo.singleIdentity()).returnValue.getOrThrow()

aliceVaultUpdates.expectEvents {
    expect { update ->
        println("Alice got vault update of $update")
        val amount: Amount<Issued<Currency>> = update.produced.first().state.data.amount
        assertEquals(1000.DOLLARS, amount.withoutIssuer())
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
bobProxy.startFlowDynamic(
        CashPaymentFlow.class,
        DOLLARS(1000),
        alice.getNodeInfo().getLegalIdentities().get(0)
).getReturnValue().get();

expectEvents(aliceVaultUpdates, true, () ->
        expect(cashVaultUpdateClass, update -> true, update -> {
            System.out.println("Alice got vault update of " + update);
            Amount<Issued<Currency>> amount = update.getProduced().iterator().next().getState().getData().getAmount();
            assertEquals(DOLLARS(1000), Structures.withoutIssuer(amount));
            return null;
        })
);

```
{{% /tab %}}
{{< /tabs >}}

As a next step, you might like to try setting up a test where Bob sends this cash back to Alice.

## Summary

That’s it! You saw how to start up several corda nodes locally, how to connect to them, and how to test some simple invariants
about `CashIssueAndPaymentFlow` and `CashPaymentFlow`.

You can find the complete test at `example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java`
(Java) and `example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt` (Kotlin) in the
[Corda repo](https://github.com/corda/corda).

{{< note >}}
To make sure the driver classes are included in your project, you will need to include the following in the `build.gradle` file in the module in
which you want to test:

```groovy
testCompile "$corda_release_group:corda-node-driver:$corda_release_version"
```
{{< /note >}}
