---
aliases:
- /releases/3.3/tutorial-integration-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-tutorial-integration-testing
    parent: corda-enterprise-3-3-tutorials-index
    weight: 1070
tags:
- tutorial
- integration
- testing
title: Integration testing
---


# Integration testing

Integration testing involves bringing up nodes locally and testing
invariants about them by starting flows and inspecting their state.

In this tutorial we will bring up three nodes - Alice, Bob and a
notary. Alice will issue cash to Bob, then Bob will send this cash
back to Alice. We will see how to test some simple deterministic and
nondeterministic invariants in the meantime.

{{< note >}}
This example where Alice is self-issuing cash is purely for
demonstration purposes, in reality, cash would be issued by a bank
and subsequently passed around.

{{< /note >}}
In order to spawn nodes we will use the Driver DSL. This DSL allows
one to start up node processes from code. It manages a network map
service and safe shutting down of nodes in the background.

```kotlin
driver(DriverParameters(
        startNodesInProcess = true,
        extraCordappPackagesToScan = listOf("net.corda.finance.contracts.asset","net.corda.finance.schemas")
)) {
    val aliceUser = User("aliceUser", "testPassword1", permissions = setOf(
            startFlow<CashIssueFlow>(),
            startFlow<CashPaymentFlow>(),
            invokeRpc("vaultTrackBy"),
            invokeRpc(CordaRPCOps::notaryIdentities),
            invokeRpc(CordaRPCOps::networkMapFeed)
    ))
    val bobUser = User("bobUser", "testPassword2", permissions = setOf(
            startFlow<CashPaymentFlow>(),
            invokeRpc("vaultTrackBy"),
            invokeRpc(CordaRPCOps::networkMapFeed)
    ))
    val (alice, bob) = listOf(
            startNode(providedName = ALICE_NAME, rpcUsers = listOf(aliceUser)),
            startNode(providedName = BOB_NAME, rpcUsers = listOf(bobUser))
    ).transpose().getOrThrow()


```
{{/* github src='docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' url='https://github.com/corda/enterprise/blob/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt#L50-L70' raw='https://raw.githubusercontent.com/corda/enterprise/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' start='START 1' end='END 1' */}}[IntegrationTestingTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/3.3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt)
The above code starts three nodes:


* Alice, who has user permissions to start the `CashIssueFlow` and
`CashPaymentFlow` flows
* Bob, who only has user permissions to start the `CashPaymentFlow`
* A notary that offers a `ValidatingNotaryService`. We won’t connect
to the notary directly, so there’s no need to provide a `User`

The `startNode` function returns a future that completes once the
node is fully started. This allows starting of the nodes to be
parallel. We wait on these futures as we need the information
returned; their respective `NodeHandles` s.

```kotlin
val aliceClient = CordaRPCClient(alice.rpcAddress)
val aliceProxy = aliceClient.start("aliceUser", "testPassword1").proxy

val bobClient = CordaRPCClient(bob.rpcAddress)
val bobProxy = bobClient.start("bobUser", "testPassword2").proxy

```
{{/* github src='docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' url='https://github.com/corda/enterprise/blob/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt#L74-L78' raw='https://raw.githubusercontent.com/corda/enterprise/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' start='START 2' end='END 2' */}}[IntegrationTestingTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/3.3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt)
After getting the handles we wait for both parties to register with
the network map to ensure we don’t have race conditions with network
map registration. Next we connect to Alice and Bob respectively from
the test process using the test user we created. Then we establish RPC
links that allow us to start flows and query state.

```kotlin
val bobVaultUpdates = bobProxy.vaultTrackBy<Cash.State>(criteria = QueryCriteria.VaultQueryCriteria(status = Vault.StateStatus.ALL)).updates
val aliceVaultUpdates = aliceProxy.vaultTrackBy<Cash.State>(criteria = QueryCriteria.VaultQueryCriteria(status = Vault.StateStatus.ALL)).updates

```
{{/* github src='docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' url='https://github.com/corda/enterprise/blob/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt#L82-L83' raw='https://raw.githubusercontent.com/corda/enterprise/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' start='START 3' end='END 3' */}}[IntegrationTestingTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/3.3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt)
We will be interested in changes to Alice’s and Bob’s vault, so we
query a stream of vault updates from each.

Now that we’re all set up we can finally get some cash action going!

```kotlin
val numberOfStates = 10
val issueRef = OpaqueBytes.of(0)
val notaryParty = aliceProxy.notaryIdentities().first()
(1..numberOfStates).map { i ->
    aliceProxy.startFlow(::CashIssueFlow,
            i.DOLLARS,
            issueRef,
            notaryParty
    ).returnValue
}.transpose().getOrThrow()
// We wait for all of the issuances to run before we start making payments
(1..numberOfStates).map { i ->
    aliceProxy.startFlow(::CashPaymentFlow,
            i.DOLLARS,
            bob.nodeInfo.singleIdentity(),
            true
    ).returnValue
}.transpose().getOrThrow()

bobVaultUpdates.expectEvents {
    parallel(
            (1..numberOfStates).map { i ->
                expect(
                        match = { update: Vault.Update<Cash.State> ->
                            update.produced.first().state.data.amount.quantity == i * 100L
                        }
                ) { update ->
                    println("Bob vault update of $update")
                }
            }
    )
}

```
{{/* github src='docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' url='https://github.com/corda/enterprise/blob/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt#L87-L118' raw='https://raw.githubusercontent.com/corda/enterprise/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' start='START 4' end='END 4' */}}[IntegrationTestingTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/3.3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt)
The first loop creates 10 threads, each starting a `CashFlow` flow
on the Alice node. We specify that we want to issue `i` dollars to
Bob, setting our notary as the notary responsible for notarising the
created states. Note that no notarisation will occur yet as we’re not
spending any states, only creating new ones on the ledger.

We started the flows from different threads for the sake of the
tutorial, to demonstrate how to test non-determinism, which is what
the `expectEvents` block does.

The Expect DSL allows ordering constraints to be checked on a stream
of events. The above code specifies that we are expecting 10 updates
to be emitted on the `bobVaultUpdates` stream in unspecified order
(this is what the `parallel` construct does). We specify an
(otherwise optional) `match` predicate to identify specific updates
we are interested in, which we then print.

If we run the code written so far we should see 4 nodes starting up
(Alice, Bob, the notary and an implicit Network Map service), then
10 logs of Bob receiving 1,2,…10 dollars from Alice in some unspecified
order.

Next we want Bob to send this cash back to Alice.

```kotlin
for (i in 1..numberOfStates) {
    bobProxy.startFlow(::CashPaymentFlow, i.DOLLARS, alice.nodeInfo.singleIdentity()).returnValue.getOrThrow()
}

aliceVaultUpdates.expectEvents {
    sequence(
            // issuance
            parallel(
                    (1..numberOfStates).map { i ->
                        expect(match = { it.moved() == -i * 100 }) { update: Vault.Update<Cash.State> ->
                            assertEquals(0, update.consumed.size)
                        }
                    }
            ),
            // move to Bob
            parallel(
                    (1..numberOfStates).map { i ->
                        expect(match = { it.moved() == i * 100 }) { update: Vault.Update<Cash.State> ->
                        }
                    }
            ),
            // move back to Alice
            sequence(
                    (1..numberOfStates).map { i ->
                        expect(match = { it.moved() == -i * 100 }) { update: Vault.Update<Cash.State> ->
                            assertEquals(update.consumed.size, 0)
                        }
                    }
            )
    )
}

```
{{/* github src='docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' url='https://github.com/corda/enterprise/blob/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt#L122-L152' raw='https://raw.githubusercontent.com/corda/enterprise/release/release-V3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt' start='START 5' end='END 5' */}}[IntegrationTestingTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/3.3/docs/source/example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt)
This time we’ll do it sequentially. We make Bob pay 1,2,..10 dollars
to Alice in order. We make sure that a the `CashFlow` has finished
by waiting on `startFlow` ‘s `returnValue`.

Then we use the Expect DSL again, this time using `sequence` to test
for the updates arriving in the order we expect them to.

Note that `parallel` and `sequence` may be nested into each other
arbitrarily to test more complex scenarios.

That’s it! We saw how to start up several corda nodes locally, how to
connect to them, and how to test some simple invariants about
`CashFlow`.

To run the complete test you can open
`example-code/src/integration-test/kotlin/net/corda/docs/IntegrationTestingTutorial.kt`
from IntelliJ and run the test, or alternatively use gradle:

```bash
# Run example-code integration tests
./gradlew docs/source/example-code:integrationTest -i
```

