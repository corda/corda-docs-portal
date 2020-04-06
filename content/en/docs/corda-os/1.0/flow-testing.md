---
aliases:
- /releases/release-V1.0/flow-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-flow-testing
    parent: corda-os-1-0-tutorials-index
    weight: 1100
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
    lateinit var mockNet: MockNetwork
    lateinit var a: StartedNode<MockNetwork.MockNode>
    lateinit var b: StartedNode<MockNetwork.MockNode>
    lateinit var notary: Party
    lateinit var megaCorpServices: MockServices
    lateinit var notaryServices: MockServices

    @Before
    fun setup() {
        setCordappPackages("net.corda.testing.contracts")
        megaCorpServices = MockServices(MEGA_CORP_KEY)
        notaryServices = MockServices(DUMMY_NOTARY_KEY)
        mockNet = MockNetwork()
        val nodes = mockNet.createSomeNodes()
        a = nodes.partyNodes[0]
        b = nodes.partyNodes[1]
        a.internals.registerInitiatedFlow(TestResponseFlow::class.java)
        b.internals.registerInitiatedFlow(TestResponseFlow::class.java)
        mockNet.runNetwork()
        notary = a.services.getDefaultNotary()
    }

    @After
    fun tearDown() {
        mockNet.stopNodes()
        unsetCordappPackages()
    }

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/test/kotlin/net/corda/core/internal/ResolveTransactionsFlowTest.kt)

We create a mock network in our `@Before` setup method and create a couple of nodes. We also record the identity
of the notary in our test network, which will come in handy later. We also tidy up when we’re done.

Next, we write a test case:

```kotlin
@Test
fun `resolve from two hashes`() {
    val (stx1, stx2) = makeTransactions()
    val p = TestFlow(setOf(stx2.id), a.info.chooseIdentity())
    val future = b.services.startFlow(p).resultFuture
    mockNet.runNetwork()
    val results = future.getOrThrow()
    assertEquals(listOf(stx1.id, stx2.id), results.map { it.id })
    b.database.transaction {
        assertEquals(stx1, b.services.validatedTransactions.getTransaction(stx1.id))
        assertEquals(stx2, b.services.validatedTransactions.getTransaction(stx2.id))
    }
}

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/test/kotlin/net/corda/core/internal/ResolveTransactionsFlowTest.kt)

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
    val dummy1: SignedTransaction = DummyContract.generateInitial(0, notary, MEGA_CORP.ref(1)).let {
        if (withAttachment != null)
            it.addAttachment(withAttachment)
        when (signFirstTX) {
            true -> {
                val ptx = megaCorpServices.signInitialTransaction(it)
                notaryServices.addSignature(ptx)
            }
            false -> {
                notaryServices.signInitialTransaction(it)
            }
        }
    }
    val dummy2: SignedTransaction = DummyContract.move(dummy1.tx.outRef(0), MINI_CORP).let {
        val ptx = megaCorpServices.signInitialTransaction(it)
        notaryServices.addSignature(ptx)
    }
    a.database.transaction {
        a.services.recordTransactions(dummy1, dummy2)
    }
    return Pair(dummy1, dummy2)
}

```

[ResolveTransactionsFlowTest.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/test/kotlin/net/corda/core/internal/ResolveTransactionsFlowTest.kt)

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

With regards to initiated flows (see [Writing flows](flow-state-machines.md) for information on initiated and initiating flows), the
full node automatically registers them by scanning the CorDapp jars. In a unit test environment this is not possible so
`MockNode` has the `registerInitiatedFlow` method to manually register an initiated flow.
