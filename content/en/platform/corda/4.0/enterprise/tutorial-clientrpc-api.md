---
aliases:
- /releases/4.0/tutorial-clientrpc-api.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-tutorial-clientrpc-api
    parent: corda-enterprise-4-0-tutorials-index
    weight: 1080
tags:
- tutorial
- clientrpc
- api
title: Using the client RPC API
---





# Using the client RPC API

In this tutorial we will build a simple command line utility that connects to a node, creates some cash transactions
and dumps the transaction graph to the standard output. We will then put some simple visualisation on top. For an
explanation on how RPC works in Corda see [Interacting with a node](clientrpc.md).

We start off by connecting to the node itself. For the purposes of the tutorial we will use the Driver to start up a notary
and a Alice node that can issue, move and exit cash.

Here’s how we configure the node to create a user that has the permissions to start the `CashIssueFlow`,
`CashPaymentFlow`, and `CashExitFlow`:

```kotlin
enum class PrintOrVisualise {
    Print,
    Visualise
}

@Suppress("DEPRECATION")
fun main(args: Array<String>) {
    require(args.isNotEmpty()) { "Usage: <binary> [Print|Visualise]" }
    val printOrVisualise = PrintOrVisualise.valueOf(args[0])

    val baseDirectory = Paths.get("build/rpc-api-tutorial")
    val user = User("user", "password", permissions = setOf(startFlow<CashIssueFlow>(),
            startFlow<CashPaymentFlow>(),
            startFlow<CashExitFlow>(),
            invokeRpc(CordaRPCOps::nodeInfo)
    ))
    driver(DriverParameters(driverDirectory = baseDirectory, cordappsForAllNodes = FINANCE_CORDAPPS, waitForAllNodesToFinish = true)) {
        val node = startNode(providedName = ALICE_NAME, rpcUsers = listOf(user)).get()

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

Now we can connect to the node itself using a valid RPC user login and start generating transactions in a different
thread using `generateTransactions` (to be defined later):

```kotlin
val client = CordaRPCClient(node.rpcAddress)
val proxy = client.start("user", "password").proxy

thread {
    generateTransactions(proxy)
}

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

`proxy` exposes the full RPC interface of the node:

```kotlin
    /** Returns a list of currently in-progress state machine infos. */
    fun stateMachinesSnapshot(): List<StateMachineInfo>

    /**
     * Returns a data feed of currently in-progress state machine infos and an observable of
     * future state machine adds/removes.
     */
    @RPCReturnsObservables
    fun stateMachinesFeed(): DataFeed<List<StateMachineInfo>, StateMachineUpdate>

    /**
     * Returns a snapshot of vault states for a given query criteria (and optional order and paging specification)
     *
     * Generic vault query function which takes a [QueryCriteria] object to define filters,
     * optional [PageSpecification] and optional [Sort] modification criteria (default unsorted),
     * and returns a [Vault.Page] object containing the following:
     *  1. states as a List of <StateAndRef> (page number and size defined by [PageSpecification])
     *  2. states metadata as a List of [Vault.StateMetadata] held in the Vault States table.
     *  3. total number of results available if [PageSpecification] supplied (otherwise returns -1)
     *  4. status types used in this query: UNCONSUMED, CONSUMED, ALL
     *  5. other results (aggregate functions with/without using value groups)
     *
     * @throws VaultQueryException if the query cannot be executed for any reason
     *        (missing criteria or parsing error, paging errors, unsupported query, underlying database error)
     *
     * Notes
     *   If no [PageSpecification] is provided, a maximum of [DEFAULT_PAGE_SIZE] results will be returned.
     *   API users must specify a [PageSpecification] if they are expecting more than [DEFAULT_PAGE_SIZE] results,
     *   otherwise a [VaultQueryException] will be thrown alerting to this condition.
     *   It is the responsibility of the API user to request further pages and/or specify a more suitable [PageSpecification].
     */
    // DOCSTART VaultQueryByAPI
    @RPCReturnsObservables
    fun <T : ContractState> vaultQueryBy(criteria: QueryCriteria,
                                         paging: PageSpecification,
                                         sorting: Sort,
                                         contractStateType: Class<out T>): Vault.Page<T>
    // DOCEND VaultQueryByAPI

    // Note: cannot apply @JvmOverloads to interfaces nor interface implementations
    // Java Helpers

    // DOCSTART VaultQueryAPIHelpers
    fun <T : ContractState> vaultQuery(contractStateType: Class<out T>): Vault.Page<T>

    fun <T : ContractState> vaultQueryByCriteria(criteria: QueryCriteria, contractStateType: Class<out T>): Vault.Page<T>

    fun <T : ContractState> vaultQueryByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): Vault.Page<T>

    fun <T : ContractState> vaultQueryByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): Vault.Page<T>
    // DOCEND VaultQueryAPIHelpers

    /**
     * Returns a snapshot (as per queryBy) and an observable of future updates to the vault for the given query criteria.
     *
     * Generic vault query function which takes a [QueryCriteria] object to define filters,
     * optional [PageSpecification] and optional [Sort] modification criteria (default unsorted),
     * and returns a [DataFeed] object containing
     * 1) a snapshot as a [Vault.Page] (described previously in [CordaRPCOps.vaultQueryBy])
     * 2) an [Observable] of [Vault.Update]
     *
     * Notes: the snapshot part of the query adheres to the same behaviour as the [CordaRPCOps.vaultQueryBy] function.
     *        the [QueryCriteria] applies to both snapshot and deltas (streaming updates).
     */
    // DOCSTART VaultTrackByAPI
    @RPCReturnsObservables
    fun <T : ContractState> vaultTrackBy(criteria: QueryCriteria,
                                         paging: PageSpecification,
                                         sorting: Sort,
                                         contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>
    // DOCEND VaultTrackByAPI

    // Note: cannot apply @JvmOverloads to interfaces nor interface implementations
    // Java Helpers

    // DOCSTART VaultTrackAPIHelpers
    fun <T : ContractState> vaultTrack(contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

    fun <T : ContractState> vaultTrackByCriteria(contractStateType: Class<out T>, criteria: QueryCriteria): DataFeed<Vault.Page<T>, Vault.Update<T>>

    fun <T : ContractState> vaultTrackByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): DataFeed<Vault.Page<T>, Vault.Update<T>>

    fun <T : ContractState> vaultTrackByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): DataFeed<Vault.Page<T>, Vault.Update<T>>
    // DOCEND VaultTrackAPIHelpers

    /**
     * @suppress Returns a list of all recorded transactions.
     *
     * TODO This method should be removed once SGX work is finalised and the design of the corresponding API using [FilteredTransaction] can be started
     */
    @Deprecated("This method is intended only for internal use and will be removed from the public API soon.")
    fun internalVerifiedTransactionsSnapshot(): List<SignedTransaction>

    /**
     * @suppress Returns the full transaction for the provided ID
     *
     * TODO This method should be removed once SGX work is finalised and the design of the corresponding API using [FilteredTransaction] can be started
     */
    @CordaInternal
    @Deprecated("This method is intended only for internal use and will be removed from the public API soon.")
    fun internalFindVerifiedTransaction(txnId: SecureHash): SignedTransaction?

    /**
     * @suppress Returns a data feed of all recorded transactions and an observable of future recorded ones.
     *
     * TODO This method should be removed once SGX work is finalised and the design of the corresponding API using [FilteredTransaction] can be started
     */
    @Deprecated("This method is intended only for internal use and will be removed from the public API soon.")
    @RPCReturnsObservables
    fun internalVerifiedTransactionsFeed(): DataFeed<List<SignedTransaction>, SignedTransaction>

    /** Returns a snapshot list of existing state machine id - recorded transaction hash mappings. */
    fun stateMachineRecordedTransactionMappingSnapshot(): List<StateMachineTransactionMapping>

    /**
     * Returns a snapshot list of existing state machine id - recorded transaction hash mappings, and a stream of future
     * such mappings as well.
     */
    @RPCReturnsObservables
    fun stateMachineRecordedTransactionMappingFeed(): DataFeed<List<StateMachineTransactionMapping>, StateMachineTransactionMapping>

    /** Returns all parties currently visible on the network with their advertised services. */
    fun networkMapSnapshot(): List<NodeInfo>

    /**
     * Returns all parties currently visible on the network with their advertised services and an observable of
     * future updates to the network.
     */
    @RPCReturnsObservables
    fun networkMapFeed(): DataFeed<List<NodeInfo>, NetworkMapCache.MapChange>

    /** Returns the network parameters the node is operating under. */
    val networkParameters: NetworkParameters

    /**
     * Returns [DataFeed] object containing information on currently scheduled parameters update (null if none are currently scheduled)
     * and observable with future update events. Any update that occurs before the deadline automatically cancels the current one.
     * Only the latest update can be accepted.
     * Note: This operation may be restricted only to node administrators.
     */
    // TODO This operation should be restricted to just node admins.
    @RPCReturnsObservables
    fun networkParametersFeed(): DataFeed<ParametersUpdateInfo?, ParametersUpdateInfo>

    /**
     * Accept network parameters with given hash, hash is obtained through [networkParametersFeed] method.
     * Information is sent back to the zone operator that the node accepted the parameters update - this process cannot be
     * undone.
     * Only parameters that are scheduled for update can be accepted, if different hash is provided this method will fail.
     * Note: This operation may be restricted only to node administrators.
     * @param parametersHash hash of network parameters to accept
     * @throws IllegalArgumentException if network map advertises update with different parameters hash then the one accepted by node's operator.
     * @throws IOException if failed to send the approval to network map
     */
    // TODO This operation should be restricted to just node admins.
    fun acceptNewNetworkParameters(parametersHash: SecureHash)

    /**
     * Start the given flow with the given arguments. [logicType] must be annotated
     * with [net.corda.core.flows.StartableByRPC].
     */
    @RPCReturnsObservables
    fun <T> startFlowDynamic(logicType: Class<out FlowLogic<T>>, vararg args: Any?): FlowHandle<T>

    /**
     * Start the given flow with the given arguments, returning an [Observable] with a single observation of the
     * result of running the flow. [logicType] must be annotated with [net.corda.core.flows.StartableByRPC].
     */
    @RPCReturnsObservables
    fun <T> startTrackedFlowDynamic(logicType: Class<out FlowLogic<T>>, vararg args: Any?): FlowProgressHandle<T>

    /**
     * Attempts to kill a flow. This is not a clean termination and should be reserved for exceptional cases such as stuck fibers.
     *
     * @return whether the flow existed and was killed.
     */
    fun killFlow(id: StateMachineRunId): Boolean

    /** Returns Node's NodeInfo, assuming this will not change while the node is running. */
    fun nodeInfo(): NodeInfo

    /**
     * Returns network's notary identities, assuming this will not change while the node is running.
     *
     * Note that the identities are sorted based on legal name, and the ordering might change once new notaries are introduced.
     */
    fun notaryIdentities(): List<Party>

    /** Add note(s) to an existing Vault transaction. */
    fun addVaultTransactionNote(txnId: SecureHash, txnNote: String)

    /** Retrieve existing note(s) for a given Vault transaction. */
    fun getVaultTransactionNotes(txnId: SecureHash): Iterable<String>

    /** Checks whether an attachment with the given hash is stored on the node. */
    fun attachmentExists(id: SecureHash): Boolean

    /** Download an attachment JAR by ID. */
    fun openAttachment(id: SecureHash): InputStream

    /** Uploads a jar to the node, returns it's hash. */
    @Throws(java.nio.file.FileAlreadyExistsException::class)
    fun uploadAttachment(jar: InputStream): SecureHash

    /** Uploads a jar including metadata to the node, returns it's hash. */
    @Throws(java.nio.file.FileAlreadyExistsException::class)
    fun uploadAttachmentWithMetadata(jar: InputStream, uploader: String, filename: String): SecureHash

    /** Queries attachments metadata */
    fun queryAttachments(query: AttachmentQueryCriteria, sorting: AttachmentSort?): List<AttachmentId>

    /** Returns the node's current time. */
    fun currentNodeTime(): Instant

    /**
     * Returns a [CordaFuture] which completes when the node has registered wih the network map service. It can also
     * complete with an exception if it is unable to.
     */
    @RPCReturnsObservables
    fun waitUntilNetworkReady(): CordaFuture<Void?>

    // TODO These need rethinking. Instead of these direct calls we should have a way of replicating a subset of
    // the node's state locally and query that directly.
    /**
     * Returns the well known identity from an abstract party. This is intended to resolve the well known identity
     * from a confidential identity, however it transparently handles returning the well known identity back if
     * a well known identity is passed in.
     *
     * @param party identity to determine well known identity for.
     * @return well known identity, if found.
     */
    fun wellKnownPartyFromAnonymous(party: AbstractParty): Party?

    /** Returns the [Party] corresponding to the given key, if found. */
    fun partyFromKey(key: PublicKey): Party?

    /** Returns the [Party] with the X.500 principal as it's [Party.name]. */
    fun wellKnownPartyFromX500Name(x500Name: CordaX500Name): Party?

    /**
     * Get a notary identity by name.
     *
     * @return the notary identity, or null if there is no notary by that name. Note that this will return null if there
     * is a peer with that name but they are not a recognised notary service.
     */
    fun notaryPartyFromX500Name(x500Name: CordaX500Name): Party?

    /**
     * Returns a list of candidate matches for a given string, with optional fuzzy(ish) matching. Fuzzy matching may
     * get smarter with time e.g. to correct spelling errors, so you should not hard-code indexes into the results
     * but rather show them via a user interface and let the user pick the one they wanted.
     *
     * @param query The string to check against the X.500 name components
     * @param exactMatch If true, a case sensitive match is done against each component of each X.500 name.
     */
    fun partiesFromName(query: String, exactMatch: Boolean): Set<Party>

    /** Enumerates the class names of the flows that this node knows about. */
    fun registeredFlows(): List<String>

    /**
     * Returns a node's info from the network map cache, where known.
     * Notice that when there are more than one node for a given name (in case of distributed services) first service node
     * found will be returned.
     *
     * @return the node info if available.
     */
    fun nodeInfoFromParty(party: AbstractParty): NodeInfo?

    /**
     * Clear all network map data from local node cache. Notice that after invoking this method your node will lose
     * network map data and effectively won't be able to start any flow with the peers until network map is downloaded
     * again on next poll - from `additional-node-infos` directory or from network map server. It depends on the
     * polling interval when it happens. You can also use [refreshNetworkMapCache] to force next fetch from network map server
     * (not from directory - it will happen automatically).
     * If you run local test deployment and want clear view of the network, you may want to clear also `additional-node-infos`
     * directory, because cache can be repopulated from there.
     */
    fun clearNetworkMapCache()

    /**
     * Poll network map server if available for the network map. Notice that you need to have `compatibilityZone`
     * or `networkServices` configured. This is normally done automatically on the regular time interval, but you may wish to
     * have the fresh view of network earlier.
     */
    fun refreshNetworkMapCache()

    /** Sets the value of the node's flows draining mode.
     * If this mode is [enabled], the node will reject new flows through RPC, ignore scheduled flows, and do not process
     * initial session messages, meaning that P2P counterparties will not be able to initiate new flows involving the node.
     *
     * @param enabled whether the flows draining mode will be enabled.
     * */
    fun setFlowsDrainingModeEnabled(enabled: Boolean)

    /**
     * Returns whether the flows draining mode is enabled.
     *
     * @see setFlowsDrainingModeEnabled
     */
    fun isFlowsDrainingModeEnabled(): Boolean

    /**
     * Shuts the node down. Returns immediately.
     * This does not wait for flows to be completed.
     */
    fun shutdown()

    /**
     * Shuts the node down. Returns immediately.
     * @param drainPendingFlows whether the node will wait for pending flows to be completed before exiting. While draining, new flows from RPC will be rejected.
     */
    fun terminate(drainPendingFlows: Boolean = false)

    /**
     * Returns whether the node is waiting for pending flows to complete before shutting down.
     * Disabling draining mode cancels this state.
     *
     * @return whether the node will shutdown when the pending flows count reaches zero.
     */
    fun isWaitingForShutdown(): Boolean

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)

The RPC operation we need in order to dump the transaction graph is `internalVerifiedTransactionsFeed`. The type
signature tells us that the RPC operation will return a list of transactions and an `Observable` stream. This is a
general pattern, we query some data and the node will return the current snapshot and future updates done to it.
Observables are described in further detail in [Interacting with a node](clientrpc.md)

```kotlin
val (transactions: List<SignedTransaction>, futureTransactions: Observable<SignedTransaction>) = proxy.internalVerifiedTransactionsFeed()

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

The graph will be defined as follows:


* Each transaction is a vertex, represented by printing `NODE <txhash>`
* Each input-output relationship is an edge, represented by printing `EDGE <txhash> <txhash>`

```kotlin
when (printOrVisualise) {
    PrintOrVisualise.Print -> {
        futureTransactions.startWith(transactions).subscribe { transaction ->
            println("NODE ${transaction.id}")
            transaction.tx.inputs.forEach { (txhash) ->
                println("EDGE $txhash ${transaction.id}")
            }
        }
    }

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

Now we just need to create the transactions themselves!

```kotlin
fun generateTransactions(proxy: CordaRPCOps) {
    val vault = proxy.vaultQueryBy<Cash.State>().states

    var ownedQuantity = vault.fold(0L) { sum, state ->
        sum + state.state.data.amount.quantity
    }
    val issueRef = OpaqueBytes.of(0)
    val notary = proxy.notaryIdentities().first()
    val me = proxy.nodeInfo().legalIdentities.first()
    while (true) {
        Thread.sleep(1000)
        val random = SplittableRandom()
        val n = random.nextDouble()
        if (ownedQuantity > 10000 && n > 0.8) {
            val quantity = Math.abs(random.nextLong()) % 2000
            proxy.startFlow(::CashExitFlow, Amount(quantity, USD), issueRef)
            ownedQuantity -= quantity
        } else if (ownedQuantity > 1000 && n < 0.7) {
            val quantity = Math.abs(random.nextLong() % Math.min(ownedQuantity, 2000))
            proxy.startFlow(::CashPaymentFlow, Amount(quantity, USD), me)
        } else {
            val quantity = Math.abs(random.nextLong() % 1000)
            proxy.startFlow(::CashIssueFlow, Amount(quantity, USD), issueRef, notary)
            ownedQuantity += quantity
        }
    }
}

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

We utilise several RPC functions here to query things like the notaries in the node cluster or our own vault. These RPC
functions also return `Observable` objects so that the node can send us updated values. However, we don’t need updates
here and so we mark these observables as `notUsed` (as a rule, you should always either subscribe to an `Observable`
or mark it as not used. Failing to do so will leak resources in the node).

Then in a loop we generate randomly either an Issue, a Pay or an Exit transaction.

The RPC we need to initiate a cash transaction is `startFlow` which starts an arbitrary flow given sufficient
permissions to do so.

Finally we have everything in place: we start a couple of nodes, connect to them, and start creating transactions while
listening on successfully created ones, which are dumped to the console. We just need to run it!

```text
# Build the example
./gradlew docs/source/example-code:installDist
# Start it
./docs/source/example-code/build/install/docs/source/example-code/bin/client-rpc-tutorial Print
```

Now let’s try to visualise the transaction graph. We will use a graph drawing library called [graphstream](http://graphstream-project.org/).

```kotlin
    PrintOrVisualise.Visualise -> {
        val graph = MultiGraph("transactions")
        transactions.forEach { transaction ->
            graph.addNode<Node>("${transaction.id}")
        }
        transactions.forEach { transaction ->
            transaction.tx.inputs.forEach { ref ->
                graph.addEdge<Edge>("$ref", "${ref.txhash}", "${transaction.id}")
            }
        }
        futureTransactions.subscribe { transaction ->
            graph.addNode<Node>("${transaction.id}")
            transaction.tx.inputs.forEach { ref ->
                graph.addEdge<Edge>("$ref", "${ref.txhash}", "${transaction.id}")
            }
        }
        graph.display()
    }
}

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

If we run the client with `Visualise` we should see a simple random graph being drawn as new transactions are being created.


## Whitelisting classes from your CorDapp with the Corda node

As described in [Interacting with a node](clientrpc.md), you have to whitelist any additional classes you add that are needed in RPC
requests or responses with the Corda node.  Here’s an example of both ways you can do this for a couple of example classes.

```kotlin
// Not annotated, so need to whitelist manually.
data class ExampleRPCValue(val foo: String)

// Annotated, so no need to whitelist manually.
@CordaSerializable
data class ExampleRPCValue2(val bar: Int)

class ExampleRPCSerializationWhitelist : SerializationWhitelist {
    // Add classes like this.
    override val whitelist = listOf(ExampleRPCValue::class.java)
}

```

[ClientRpcTutorial.kt](https://github.com/corda/corda/blob/release/os/4.0/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)

See more on plugins in [Running nodes locally](running-a-node.md).


## Security

RPC credentials associated with a Client must match the permission set configured on the server node.
This refers to both authentication (username and password) and authorisation (a permissioned set of RPC operations an
authenticated user is entitled to run).

In the instructions below the server node permissions are configured programmatically in the driver code:

```text
driver(driverDirectory = baseDirectory) {
    val user = User("user", "password", permissions = setOf(startFlow<CashFlow>()))
    val node = startNode("CN=Alice Corp,O=Alice Corp,L=London,C=GB", rpcUsers = listOf(user)).get()
```

When starting a standalone node using a configuration file we must supply the RPC credentials in the node configuration,
like illustrated in the sample configuration below, or indicate an external database storing user accounts (see
[Interacting with a node](clientrpc.md) for more details):

```text
rpcUsers : [
    { username=user, password=password, permissions=[ StartFlow.net.corda.finance.flows.CashFlow ] }
]
```

When using the gradle Cordformation plugin to configure and deploy a node you must supply the RPC credentials in a similar
manner:

```text
rpcUsers = [
        ['username' : "user",
         'password' : "password",
         'permissions' : ["StartFlow.net.corda.finance.flows.CashFlow"]]
]
```

You can then deploy and launch the nodes (Notary and Alice) as follows:

```text
# to create a set of configs and installs under ``docs/source/example-code/build/nodes`` run
./gradlew docs/source/example-code:deployNodes
# to open up two new terminals with the two nodes run
./docs/source/example-code/build/nodes/runnodes
# followed by the same commands as before:
./docs/source/example-code/build/install/docs/source/example-code/bin/client-rpc-tutorial Print
./docs/source/example-code/build/install/docs/source/example-code/bin/client-rpc-tutorial Visualise
```

With regards to the start flow RPCs, there is an extra layer of security whereby the flow to be executed has to be
annotated with `@StartableByRPC`. Flows without this annotation cannot execute using RPC.

See more on security in [Secure coding guidelines](secure-coding-guidelines.md), node configuration in [Node configuration](corda-configuration-file.md) and
Cordformation in [Running nodes locally](running-a-node.md).
