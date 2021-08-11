---
aliases:
- /releases/4.2/flow-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-flow-testing
    parent: corda-enterprise-4-2-tutorials-index
    weight: 1110
tags:
- flow
- testing
title: Writing flow tests
---




# Writing flow tests

A flow can be a fairly complex thing that interacts with many services and other parties over the network. That
means unit testing one requires some infrastructure to provide lightweight mock implementations. The MockNetwork
provides this testing infrastructure layer; you can find this class in the test-utils module.

A good example to examine for learning how to unit test flows is the `ResolveTransactionsFlow` tests. This
flow takes care of downloading and verifying transaction graphs, with all the needed dependencies. We start
with this basic skeleton:

```kotlin
class ResolveTransactionsFlowTest {
    private lateinit var mockNet: MockNetwork
    private lateinit var notaryNode: StartedMockNode
    private lateinit var megaCorpNode: StartedMockNode
    private lateinit var miniCorpNode: StartedMockNode
    private lateinit var newNotaryNode: StartedMockNode
    private lateinit var megaCorp: Party
    private lateinit var miniCorp: Party
    private lateinit var notary: Party
    private lateinit var newNotary: Party

    @Before
    fun setup() {
        val mockNetworkParameters = MockNetworkParameters(
                cordappsForAllNodes = listOf(DUMMY_CONTRACTS_CORDAPP, enclosedCordapp()),
                notarySpecs = listOf(
                        MockNetworkNotarySpec(DUMMY_NOTARY_NAME),
                        MockNetworkNotarySpec(DUMMY_BANK_A_NAME)
                )
        )
        mockNet = MockNetwork(mockNetworkParameters)
        notaryNode = mockNet.notaryNodes.first()
        megaCorpNode = mockNet.createPartyNode(CordaX500Name("MegaCorp", "London", "GB"))
        miniCorpNode = mockNet.createPartyNode(CordaX500Name("MiniCorp", "London", "GB"))
        notary = notaryNode.info.singleIdentity()
        megaCorp = megaCorpNode.info.singleIdentity()
        miniCorp = miniCorpNode.info.singleIdentity()
        newNotaryNode = mockNet.notaryNodes[1]
        newNotary = mockNet.notaryNodes[1].info.singleIdentity()
    }

    @After
    fun tearDown() {
        mockNet.stopNodes()
        System.setProperty("net.corda.node.dbtransactionsresolver.InMemoryResolutionLimit", "0")
    }

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/4.2/core-tests/src/test/kotlin/net/corda/coretests/internal/ResolveTransactionsFlowTest.kt)

We create a mock network in our `@Before` setup method and create a couple of nodes. We also record the identity
of the notary in our test network, which will come in handy later. We also tidy up when we’re done.

Next, we write a test case:

```kotlin
@Test
fun `resolve from two hashes`() {
    val (stx1, stx2) = makeTransactions()
    val p = TestFlow(setOf(stx2.id), megaCorp)
    val future = miniCorpNode.startFlow(p)
    mockNet.runNetwork()
    future.getOrThrow()
    miniCorpNode.transaction {
        assertEquals(stx1, miniCorpNode.services.validatedTransactions.getTransaction(stx1.id))
        assertEquals(stx2, miniCorpNode.services.validatedTransactions.getTransaction(stx2.id))
    }
}

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/4.2/core-tests/src/test/kotlin/net/corda/coretests/internal/ResolveTransactionsFlowTest.kt)

We’ll take a look at the `makeTransactions` function in a moment. For now, it’s enough to know that it returns two
`SignedTransaction` objects, the second of which spends the first. Both transactions are known by MegaCorpNode but
not MiniCorpNode.

The test logic is simple enough: we create the flow, giving it MegaCorpNode’s identity as the target to talk to.
Then we start it on MiniCorpNode and use the `mockNet.runNetwork()` method to bounce messages around until things have
settled (i.e. there are no more messages waiting to be delivered). All this is done using an in memory message
routing implementation that is fast to initialise and use. Finally, we obtain the result of the flow and do
some tests on it. We also check the contents of MiniCorpNode’s database to see that the flow had the intended effect
on the node’s persistent state.

Here’s what `makeTransactions` looks like:

```kotlin
private fun makeTransactions(signFirstTX: Boolean = true, withAttachment: SecureHash? = null): Pair<SignedTransaction, SignedTransaction> {
    // Make a chain of custody of dummy states and insert into node A.
    val dummy1: SignedTransaction = DummyContract.generateInitial(0, notary, megaCorp.ref(1)).let {
        if (withAttachment != null)
            it.addAttachment(withAttachment)
        when (signFirstTX) {
            true -> {
                val ptx = megaCorpNode.services.signInitialTransaction(it)
                notaryNode.services.addSignature(ptx, notary.owningKey)
            }
            false -> {
                notaryNode.services.signInitialTransaction(it, notary.owningKey)
            }
        }
    }
    megaCorpNode.transaction {
        megaCorpNode.services.recordTransactions(dummy1)
    }
    val dummy2: SignedTransaction = DummyContract.move(dummy1.tx.outRef(0), miniCorp).let {
        val ptx = megaCorpNode.services.signInitialTransaction(it)
        notaryNode.services.addSignature(ptx, notary.owningKey)
    }
    megaCorpNode.transaction {
        megaCorpNode.services.recordTransactions(dummy2)
    }
    return Pair(dummy1, dummy2)
}

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/4.2/core-tests/src/test/kotlin/net/corda/coretests/internal/ResolveTransactionsFlowTest.kt)

We’re using the `DummyContract`, a simple test smart contract which stores a single number in its states, along
with ownership and issuer information. You can issue such states, exit them and re-assign ownership (move them).
It doesn’t do anything else. This code simply creates a transaction that issues a dummy state (the issuer is
`MEGA_CORP`, a pre-defined unit test identity), signs it with the test notary and MegaCorp keys and then
converts the builder to the final `SignedTransaction`. It then does so again, but this time instead of issuing
it re-assigns ownership instead. The chain of two transactions is finally committed to MegaCorpNode by sending them
directly to the `megaCorpNode.services.recordTransaction` method (note that this method doesn’t check the
transactions are valid) inside a `database.transaction`.  All node flows run within a database transaction in the
nodes themselves, but any time we need to use the database directly from a unit test, you need to provide a database
transaction as shown here.
