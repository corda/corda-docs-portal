---
aliases:
- /releases/release-V3.1/api-testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-1:
    identifier: corda-os-3-1-api-testing
    parent: corda-os-3-1-corda-api
    weight: 1120
tags:
- api
- testing
title: 'API: Testing'
---




# API: Testing



## Flow testing


### MockNetwork

Flow testing can be fully automated using a `MockNetwork` composed of `StartedMockNode` nodes. Each
`StartedMockNode` behaves like a regular Corda node, but its services are either in-memory or mocked out.

A `MockNetwork` is created as follows:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
class FlowTests {
    private lateinit var mockNet: MockNetwork

    @Before
    fun setup() {
        network = MockNetwork(listOf("my.cordapp.package", "my.other.cordapp.package"))
    }
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public class IOUFlowTests {
    private MockNetwork network;

    @Before
    public void setup() {
        network = new MockNetwork(ImmutableList.of("my.cordapp.package", "my.other.cordapp.package"));
    }
}
```
{{% /tab %}}

{{< /tabs >}}

The `MockNetwork` requires at a minimum a list of packages. Each package is packaged into a CorDapp JAR and installed
as a CorDapp on each `StartedMockNode`.


#### Configuring the `MockNetwork`

The `MockNetwork` is configured automatically. You can tweak its configuration using a `MockNetworkParameters`
object, or by using named paramters in Kotlin:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val network = MockNetwork(
        // A list of packages to scan. Any contracts, flows and Corda services within these
        // packages will be automatically available to any nodes within the mock network
        cordappPackages = listOf("my.cordapp.package", "my.other.cordapp.package"),
        // If true then each node will be run in its own thread. This can result in race conditions in your
        // code if not carefully written, but is more realistic and may help if you have flows in your app that
        // do long blocking operations.
        threadPerNode = false,
        // The notaries to use on the mock network. By default you get one mock notary and that is usually
        // sufficient.
        notarySpecs = listOf(MockNetworkNotarySpec(DUMMY_NOTARY_NAME)),
        // If true then messages will not be routed from sender to receiver until you use the
        // [MockNetwork.runNetwork] method. This is useful for writing single-threaded unit test code that can
        // examine the state of the mock network before and after a message is sent, without races and without
        // the receiving node immediately sending a response.
        networkSendManuallyPumped = false,
        // How traffic is allocated in the case where multiple nodes share a single identity, which happens for
        // notaries in a cluster. You don't normally ever need to change this: it is mostly useful for testing
        // notary implementations.
        servicePeerAllocationStrategy = InMemoryMessagingNetwork.ServicePeerAllocationStrategy.Random())

val network2 = MockNetwork(
        // A list of packages to scan. Any contracts, flows and Corda services within these
        // packages will be automatically available to any nodes within the mock network
        listOf("my.cordapp.package", "my.other.cordapp.package"), MockNetworkParameters(
        // If true then each node will be run in its own thread. This can result in race conditions in your
        // code if not carefully written, but is more realistic and may help if you have flows in your app that
        // do long blocking operations.
        threadPerNode = false,
        // The notaries to use on the mock network. By default you get one mock notary and that is usually
        // sufficient.
        notarySpecs = listOf(MockNetworkNotarySpec(DUMMY_NOTARY_NAME)),
        // If true then messages will not be routed from sender to receiver until you use the
        // [MockNetwork.runNetwork] method. This is useful for writing single-threaded unit test code that can
        // examine the state of the mock network before and after a message is sent, without races and without
        // the receiving node immediately sending a response.
        networkSendManuallyPumped = false,
        // How traffic is allocated in the case where multiple nodes share a single identity, which happens for
        // notaries in a cluster. You don't normally ever need to change this: it is mostly useful for testing
        // notary implementations.
        servicePeerAllocationStrategy = InMemoryMessagingNetwork.ServicePeerAllocationStrategy.Random())
)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MockNetwork network = MockNetwork(
        // A list of packages to scan. Any contracts, flows and Corda services within these
        // packages will be automatically available to any nodes within the mock network
        ImmutableList.of("my.cordapp.package", "my.other.cordapp.package"),
        new MockNetworkParameters()
                // If true then each node will be run in its own thread. This can result in race conditions in
                // your code if not carefully written, but is more realistic and may help if you have flows in
                // your app that do long blocking operations.
                .setThreadPerNode(false)
                // The notaries to use on the mock network. By default you get one mock notary and that is
                // usually sufficient.
                .setNotarySpecs(ImmutableList.of(new MockNetworkNotarySpec(DUMMY_NOTARY_NAME)))
                // If true then messages will not be routed from sender to receiver until you use the
                // [MockNetwork.runNetwork] method. This is useful for writing single-threaded unit test code
                // that can examine the state of the mock network before and after a message is sent, without
                // races and without the receiving node immediately sending a response.
                .setNetworkSendManuallyPumped(false)
                // How traffic is allocated in the case where multiple nodes share a single identity, which
                // happens for notaries in a cluster. You don't normally ever need to change this: it is mostly
                // useful for testing notary implementations.
                .setServicePeerAllocationStrategy(new InMemoryMessagingNetwork.ServicePeerAllocationStrategy.Random()));
```
{{% /tab %}}

{{< /tabs >}}


### Adding nodes to the network

Nodes are created on the `MockNetwork` using:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
class FlowTests {
    private lateinit var mockNet: MockNetwork
    lateinit var nodeA: StartedMockNode
    lateinit var nodeB: StartedMockNode

    @Before
    fun setup() {
        network = MockNetwork(listOf("my.cordapp.package", "my.other.cordapp.package"))
        nodeA = network.createPartyNode()
        // We can optionally give the node a name.
        nodeB = network.createPartyNode(CordaX500Name("Bank B", "London", "GB"))
    }
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public class IOUFlowTests {
    private MockNetwork network;
    private StartedMockNode a;
    private StartedMockNode b;

    @Before
    public void setup() {
        network = new MockNetwork(ImmutableList.of("my.cordapp.package", "my.other.cordapp.package"));
        nodeA = network.createPartyNode(null);
        // We can optionally give the node a name.
        nodeB = network.createPartyNode(new CordaX500Name("Bank B", "London", "GB"));
    }
}
```
{{% /tab %}}

{{< /tabs >}}


#### Registering a node’s initiated flows

Regular Corda nodes automatically register any response flows defined in their installed CorDapps. When using a
`MockNetwork`, each `StartedMockNode` must manually register any responder flows it wishes to use.

Responder flows are registered as follows:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
nodeA.registerInitiatedFlow(ExampleFlow.Acceptor::class.java)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
nodeA.registerInitiatedFlow(ExampleFlow.Acceptor.class);
```
{{% /tab %}}

{{< /tabs >}}


### Running the network

Regular Corda nodes automatically process received messages. When using a `MockNetwork` with
`networkSendManuallyPumped` set to `false`, you must manually initiate the processing of received messages.

You manually process received messages as follows:


* `StartedMockNode.pumpReceive` to process a single message from the node’s queue
* `MockNetwork.runNetwork` to process all the messages in every node’s queue. This may generate additional messages
that must in turn be processed>

    * `network.runNetwork(-1)` (the default in Kotlin) will exchange messages until there are no further messages to
process





### Running flows

A `StartedMockNode` starts a flow using the `StartedNodeServices.startFlow` method. This method returns a future
representing the output of running the flow.

{{< tabs name="tabs-5" >}}
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

{{< tabs name="tabs-6" >}}
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


#### Creating a node database transaction

Whenever you query a node’s database (e.g. to extract information from the node’s vault), you must wrap the query in
a database transaction, as follows:

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
nodeA.database.transaction {
    // Perform query here.
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
node.getDatabase().transaction(tx -> {
    // Perform query here.
}
```
{{% /tab %}}

{{< /tabs >}}


#### Querying a node’s vault

Recorded states can be retrieved from the vault of a `StartedMockNode` using:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
nodeA.database.transaction {
    val myStates = nodeA.services.vaultService.queryBy<MyStateType>().states
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
node.getDatabase().transaction(tx -> {
    List<MyStateType> myStates = node.getServices().getVaultService().queryBy(MyStateType.class).getStates();
}
```
{{% /tab %}}

{{< /tabs >}}

This allows you to check whether a given state has (or has not) been stored, and whether it has the correct attributes.


#### Examining a node’s transaction storage

Recorded transactions can be retrieved from the transaction storage of a `StartedMockNode` using:

{{< tabs name="tabs-9" >}}
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


* See the flow testing tutorial [here](flow-testing.md)
* See the oracle tutorial [here](oracles.md) for information on testing `@CordaService` classes
* Further examples are available in the Example CorDapp in
[Java](https://github.com/corda/cordapp-example/blob/release-V3/java-source/src/test/java/com/example/flow/IOUFlowTests.java) and
[Kotlin](https://github.com/corda/cordapp-example/blob/release-V3/kotlin-source/src/test/kotlin/com/example/flow/IOUFlowTests.kt)


## Contract testing

The Corda test framework includes the ability to create a test ledger by calling the `ledger` function
on an implementation of the `ServiceHub` interface.


### MockServices

A mock implementation of `ServiceHub` is provided in `MockServices`. This is a minimal `ServiceHub` that
suffices to test contract logic. It has the ability to insert states into the vault, query the vault, and
construct and check transactions.

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
private val ledgerServices = MockServices(
        // A list of packages to scan for cordapps
        cordappPackages = listOf("net.corda.finance.contracts"),
        // The identity represented by this set of mock services. Defaults to a test identity.
        // You can also use the alternative parameter initialIdentityName which accepts a
        // [CordaX500Name]
        initialIdentity = megaCorp,
        // An implementation of IdentityService, which contains a list of all identities known
        // to the node. Use [makeTestIdentityService] which returns an implementation of
        // [InMemoryIdentityService] with the given identities
        identityService = makeTestIdentityService(megaCorp.identity)
)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
    ledgerServices = new MockServices(
            // A list of packages to scan for cordapps
            singletonList("net.corda.finance.contracts"),
            // The identity represented by this set of mock services. Defaults to a test identity.
            // You can also use the alternative parameter initialIdentityName which accepts a
            // [CordaX500Name]
            megaCorp,
            // An implementation of [IdentityService], which contains a list of all identities known
            // to the node. Use [makeTestIdentityService] which returns an implementation of
            // [InMemoryIdentityService] with the given identities
            makeTestIdentityService(megaCorp.getIdentity())
    );

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Alternatively, there is a helper constructor which just accepts a list of `TestIdentity`. The first identity provided is
the identity of the node whose `ServiceHub` is being mocked, and any subsequent identities are identities that the node
knows about. Only the calling package is scanned for cordapps and a test `IdentityService` is created
for you, using all the given identities.

{{< tabs name="tabs-11" >}}
{{% tab name="kotlin" %}}
```kotlin
private val simpleLedgerServices = MockServices(
        // This is the identity of the node
        megaCorp,
        // Other identities the test node knows about
        bigCorp,
        alice
)

```
{{% /tab %}}



{{% tab name="java" %}}
```java
private final MockServices simpleLedgerServices = new MockServices(
        // This is the identity of the node
        megaCorp,
        // Other identities the test node knows about
        bigCorp,
        alice
);

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### Writing tests using a test ledger

The `ServiceHub.ledger` extension function allows you to create a test ledger. Within the ledger wrapper you can create
transactions using the `transaction` function. Within a transaction you can define the `input` and
`output` states for the transaction, alongside any commands that are being executed, the `timeWindow` in which the
transaction has been executed, and any `attachments`, as shown in this example test:

{{< tabs name="tabs-12" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
fun simpleCPMoveSuccess() {
    val inState = getPaper()
    ledgerServices.ledger(dummyNotary.party) {
        transaction {
            input(CP_PROGRAM_ID, inState)
            command(megaCorp.publicKey, CommercialPaper.Commands.Move())
            attachments(CP_PROGRAM_ID)
            timeWindow(TEST_TX_TIME)
            output(CP_PROGRAM_ID, "alice's paper", inState.withOwner(alice.party))
            verifies()
        }
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Test
public void simpleCPMoveSuccess() {
    ICommercialPaperState inState = getPaper();
    ledger(ledgerServices, l -> {
        l.transaction(tx -> {
            tx.input(JCP_PROGRAM_ID, inState);
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Move());
            tx.attachments(JCP_PROGRAM_ID);
            tx.timeWindow(TEST_TX_TIME);
            tx.output(JCP_PROGRAM_ID, "alice's paper", inState.withOwner(alice.getParty()));
            return tx.verifies();
        });
        return Unit.INSTANCE;
    });
}

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Once all the transaction components have been specified, you can run `verifies()` to check that the given transaction is valid.


#### Checking for failure states

In order to test for failures, you can use the `failsWith` method, or in Kotlin the `fails with` helper method, which
assert that the transaction fails with a specific error. If you just want to assert that the transaction has failed without
verifying the message, there is also a `fails` method.

{{< tabs name="tabs-13" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
fun simpleCPMoveFails() {
    val inState = getPaper()
    ledgerServices.ledger(dummyNotary.party) {
        transaction {
            input(CP_PROGRAM_ID, inState)
            command(megaCorp.publicKey, CommercialPaper.Commands.Move())
            attachments(CP_PROGRAM_ID)
            `fails with`("the state is propagated")
        }
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Test
public void simpleCPMoveFails() {
    ICommercialPaperState inState = getPaper();
    ledger(ledgerServices, l -> {
        l.transaction(tx -> {
            tx.input(JCP_PROGRAM_ID, inState);
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Move());
            tx.attachments(JCP_PROGRAM_ID);
            return tx.failsWith("the state is propagated");
        });
        return Unit.INSTANCE;
    });
}

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

{{< note >}}
The transaction DSL forces the last line of the test to be either a `verifies` or `fails with` statement.

{{< /note >}}

#### Testing multiple scenarios at once

Within a single transaction block, you can assert several times that the transaction constructed so far either passes or
fails verification. For example, you could test that a contract fails to verify because it has no output states, and then
add the relevant output state and check that the contract verifies successfully, as in the following example:

{{< tabs name="tabs-14" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
fun simpleCPMoveFailureAndSuccess() {
    val inState = getPaper()
    ledgerServices.ledger(dummyNotary.party) {
        transaction {
            input(CP_PROGRAM_ID, inState)
            command(megaCorp.publicKey, CommercialPaper.Commands.Move())
            attachments(CP_PROGRAM_ID)
            `fails with`("the state is propagated")
            output(CP_PROGRAM_ID, "alice's paper", inState.withOwner(alice.party))
            verifies()
        }
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Test
public void simpleCPMoveSuccessAndFailure() {
    ICommercialPaperState inState = getPaper();
    ledger(ledgerServices, l -> {
        l.transaction(tx -> {
            tx.input(JCP_PROGRAM_ID, inState);
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Move());
            tx.attachments(JCP_PROGRAM_ID);
            tx.failsWith("the state is propagated");
            tx.output(JCP_PROGRAM_ID, "alice's paper", inState.withOwner(alice.getParty()));
            return tx.verifies();
        });
        return Unit.INSTANCE;
    });
}

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

You can also use the `tweak` function to create a locally scoped transaction that you can make changes to
and then return to the original, unmodified transaction. As in the following example:

{{< tabs name="tabs-15" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
fun `simple issuance with tweak and top level transaction`() {
    ledgerServices.transaction(dummyNotary.party) {
        output(CP_PROGRAM_ID, "paper", getPaper()) // Some CP is issued onto the ledger by MegaCorp.
        attachments(CP_PROGRAM_ID)
        tweak {
            // The wrong pubkey.
            command(bigCorp.publicKey, CommercialPaper.Commands.Issue())
            timeWindow(TEST_TX_TIME)
            `fails with`("output states are issued by a command signer")
        }
        command(megaCorp.publicKey, CommercialPaper.Commands.Issue())
        timeWindow(TEST_TX_TIME)
        verifies()
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Test
public void simpleIssuanceWithTweakTopLevelTx() {
    transaction(ledgerServices, tx -> {
        tx.output(JCP_PROGRAM_ID, "paper", getPaper()); // Some CP is issued onto the ledger by MegaCorp.
        tx.attachments(JCP_PROGRAM_ID);
        tx.tweak(tw -> {
            tw.command(bigCorp.getPublicKey(), new JavaCommercialPaper.Commands.Issue());
            tw.timeWindow(TEST_TX_TIME);
            return tw.failsWith("output states are issued by a command signer");
        });
        tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Issue());
        tx.timeWindow(TEST_TX_TIME);
        return tx.verifies();
    });
}

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


#### Chaining transactions

The following example shows that within a `ledger`, you can create more than one `transaction` in order to test chains
of transactions. In addition to `transaction`, `unverifiedTransaction` can be used, as in the example below, to create
transactions on the ledger without verifying them, for pre-populating the ledger with existing data. When chaining transactions,
it is important to note that even though a `transaction` `verifies` successfully, the overall ledger may not be valid. This can
be verified separately by placing a `verifies` or `fails` statement  within the `ledger` block.

{{< tabs name="tabs-16" >}}
{{% tab name="kotlin" %}}
```kotlin
@Test
fun `chain commercial paper double spend`() {
    val issuer = megaCorp.party.ref(123)
    ledgerServices.ledger(dummyNotary.party) {
        unverifiedTransaction {
            attachments(Cash.PROGRAM_ID)
            output(Cash.PROGRAM_ID, "alice's $900", 900.DOLLARS.CASH issuedBy issuer ownedBy alice.party)
        }

        // Some CP is issued onto the ledger by MegaCorp.
        transaction("Issuance") {
            output(CP_PROGRAM_ID, "paper", getPaper())
            command(megaCorp.publicKey, CommercialPaper.Commands.Issue())
            attachments(CP_PROGRAM_ID)
            timeWindow(TEST_TX_TIME)
            verifies()
        }

        transaction("Trade") {
            input("paper")
            input("alice's $900")
            output(Cash.PROGRAM_ID, "borrowed $900", 900.DOLLARS.CASH issuedBy issuer ownedBy megaCorp.party)
            output(CP_PROGRAM_ID, "alice's paper", "paper".output<ICommercialPaperState>().withOwner(alice.party))
            command(alice.publicKey, Cash.Commands.Move())
            command(megaCorp.publicKey, CommercialPaper.Commands.Move())
            verifies()
        }

        transaction {
            input("paper")
            // We moved a paper to another pubkey.
            output(CP_PROGRAM_ID, "bob's paper", "paper".output<ICommercialPaperState>().withOwner(bob.party))
            command(megaCorp.publicKey, CommercialPaper.Commands.Move())
            verifies()
        }

        fails()
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Test
public void chainCommercialPaperDoubleSpend() {
    PartyAndReference issuer = megaCorp.ref(defaultRef);
    ledger(ledgerServices, l -> {
        l.unverifiedTransaction(tx -> {
            tx.output(Cash.PROGRAM_ID, "alice's $900",
                    new Cash.State(issuedBy(DOLLARS(900), issuer), alice.getParty()));
            tx.attachments(Cash.PROGRAM_ID);
            return Unit.INSTANCE;
        });

        // Some CP is issued onto the ledger by MegaCorp.
        l.transaction("Issuance", tx -> {
            tx.output(Cash.PROGRAM_ID, "paper", getPaper());
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Issue());
            tx.attachments(JCP_PROGRAM_ID);
            tx.timeWindow(TEST_TX_TIME);
            return tx.verifies();
        });

        l.transaction("Trade", tx -> {
            tx.input("paper");
            tx.input("alice's $900");
            tx.output(Cash.PROGRAM_ID, "borrowed $900", new Cash.State(issuedBy(DOLLARS(900), issuer), megaCorp.getParty()));
            JavaCommercialPaper.State inputPaper = l.retrieveOutput(JavaCommercialPaper.State.class, "paper");
            tx.output(JCP_PROGRAM_ID, "alice's paper", inputPaper.withOwner(alice.getParty()));
            tx.command(alice.getPublicKey(), new Cash.Commands.Move());
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Move());
            return tx.verifies();
        });

        l.transaction(tx -> {
            tx.input("paper");
            JavaCommercialPaper.State inputPaper = l.retrieveOutput(JavaCommercialPaper.State.class, "paper");
            // We moved a paper to other pubkey.
            tx.output(JCP_PROGRAM_ID, "bob's paper", inputPaper.withOwner(bob.getParty()));
            tx.command(megaCorp.getPublicKey(), new JavaCommercialPaper.Commands.Move());
            return tx.verifies();
        });
        l.fails();
        return Unit.INSTANCE;
    });
}

```
{{% /tab %}}




[TutorialTestDSL.kt](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/kotlin/net/corda/docs/tutorial/testdsl/TutorialTestDSL.kt) | [CommercialPaperTest.java](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/test/java/net/corda/docs/java/tutorial/testdsl/CommercialPaperTest.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


### Further examples


* See the flow testing tutorial [here](tutorial-test-dsl.md)
* Further examples are available in the Example CorDapp in
[Java](https://github.com/corda/cordapp-example/blob/release-V3/java-source/src/test/java/com/example/flow/IOUFlowTests.java) and
[Kotlin](https://github.com/corda/cordapp-example/blob/release-V3/kotlin-source/src/test/kotlin/com/example/flow/IOUFlowTests.kt)
