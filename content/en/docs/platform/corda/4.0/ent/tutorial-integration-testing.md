---
aliases:
- /releases/4.0/tutorial-integration-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-tutorial-integration-testing
    parent: corda-enterprise-4-0-tutorials-index
    weight: 1070
tags:
- tutorial
- integration
- testing
title: Integration testing
---




# Integration testing

Integration testing involves bringing up nodes locally and testing invariants about them by starting flows and inspecting
their state.

In this tutorial we will bring up three nodes - Alice, Bob and a notary. Alice will issue cash to Bob, then Bob will send
this cash back to Alice. We will see how to test some simple deterministic and nondeterministic invariants in the meantime.

{{< note >}}
This example where Alice is self-issuing cash is purely for demonstration purposes, in reality, cash would be
issued by a bank and subsequently passed around.

{{< /note >}}
In order to spawn nodes we will use the Driver DSL. This DSL allows one to start up node processes from code. It creates
a local network where all the nodes see each other and provides safe shutting down of nodes in the background.

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




[KotlinIntegrationTestingTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt) | [JavaIntegrationTestingTutorial.java](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

The above code starts two nodes:


* Alice, configured with an RPC user who has permissions to start the `CashIssueAndPaymentFlow` flow on it and query
Alice’s vault.
* Bob, configured with an RPC user who only has permissions to start the `CashPaymentFlow` and query Bob’s vault.

{{< note >}}
You will notice that we did not start a notary. This is done automatically for us by the driver - it creates
a notary node with the name `DUMMY_NOTARY_NAME` which is visible to both nodes. If you wish to customise this, for
example create more notaries, then specify the `DriverParameters.notarySpecs` parameter.

{{< /note >}}
The `startNode` function returns a `CordaFuture` object that completes once the node is fully started and visible on
the local network. Returning a future allows starting of the nodes to be parallel. We wait on these futures as we need
the information returned; their respective `NodeHandles` s.

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




[KotlinIntegrationTestingTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt) | [JavaIntegrationTestingTutorial.java](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Next we connect to Alice and Bob from the test process using the test users we created. We establish RPC links that allow
us to start flows and query state.

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




[KotlinIntegrationTestingTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt) | [JavaIntegrationTestingTutorial.java](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We will be interested in changes to Alice’s and Bob’s vault, so we query a stream of vault updates from each.

Now that we’re all set up we can finally get some cash action going!

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




[KotlinIntegrationTestingTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt) | [JavaIntegrationTestingTutorial.java](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

We start a `CashIssueAndPaymentFlow` flow on the Alice node. We specify that we want Alice to self-issue $1000 which is
to be payed to Bob. We specify the default notary identity created by the driver as the notary responsible for notarising
the created states. Note that no notarisation will occur yet as we’re not spending any states, only creating new ones on
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




[KotlinIntegrationTestingTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt) | [JavaIntegrationTestingTutorial.java](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Next we want Bob to send this cash back to Alice.

That’s it! We saw how to start up several corda nodes locally, how to connect to them, and how to test some simple invariants
about `CashIssueAndPaymentFlow` and `CashPaymentFlow`.

You can find the complete test at `example-code/src/integration-test/java/net/corda/docs/java/tutorial/test/JavaIntegrationTestingTutorial.java`
(Java) and `example-code/src/integration-test/kotlin/net/corda/docs/kotlin/tutorial/test/KotlinIntegrationTestingTutorial.kt` (Kotlin) in the
[Corda repo](https://github.com/corda/corda).

{{< note >}}
To make sure the driver classes are included in your project you will need the following in your `build.gradle` file in the module in
which you want to test:

```groovy
testCompile "$corda_release_group:corda-node-driver:$corda_release_version"
```

{{< /note >}}
