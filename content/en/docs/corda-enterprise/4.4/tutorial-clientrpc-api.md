---
aliases:
- /releases/4.4/tutorial-clientrpc-api.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-tutorials
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
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L39-L56' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 1' end='END 1' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
Now we can connect to the node itself using a valid RPC user login and start generating transactions in a different
thread using `generateTransactions` (to be defined later):

```kotlin
val client = CordaRPCClient(node.rpcAddress)
val proxy = client.start("user", "password").proxy

thread {
    generateTransactions(proxy)
}

```
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L60-L65' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 2' end='END 2' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
`proxy` exposes the full RPC interface of the node:

The RPC operation we need in order to dump the transaction graph is `internalVerifiedTransactionsFeed`. The type
signature tells us that the RPC operation will return a list of transactions and an `Observable` stream. This is a
general pattern, we query some data and the node will return the current snapshot and future updates done to it.
Observables are described in further detail in [Interacting with a node](clientrpc.md)

```kotlin
val (transactions: List<SignedTransaction>, futureTransactions: Observable<SignedTransaction>) = proxy.internalVerifiedTransactionsFeed()

```
{{/* github src='core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' start='interface CordaRPCOps' end='}' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
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
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L69-L69' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 3' end='END 3' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
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
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L73-L81' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 4' end='END 4' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
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
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L109-L135' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 6' end='END 6' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
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
{{/* github src='docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt#L84-L102' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt' start='START 5' end='END 5' */}}[ClientRpcTutorial.kt](https://github.com/corda/enterprise/blob/release/ent/4.4/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcTutorial.kt)
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

Wildcard permissions can be set by using the *** character, e.g.:

```text
rpcUsers : [
    { username=user, password=password, permissions=[ StartFlow.net.corda.finance.flows.* ] }
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

