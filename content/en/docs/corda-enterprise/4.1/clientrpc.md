---
aliases:
- /releases/4.1/clientrpc.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-clientrpc
    parent: corda-enterprise-4-1-corda-nodes-index
    weight: 1100
tags:
- clientrpc
title: Interacting with a node
---




# Interacting with a node



## Overview

To interact with your node, you need to write a client in a JVM-compatible language using the [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class.
This class allows you to connect to your node via a message queue protocol and provides a simple RPC interface for
interacting with the node. You make calls on a JVM object as normal, and the marshalling back-and-forth is handled for
you.


{{< warning >}}
The built-in Corda webserver is deprecated and unsuitable for production use. If you want to interact with
your node via HTTP, you will need to stand up your own webserver that connects to your node using the
[CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class. You can find an example of how to do this using the popular Spring Boot server
[here](https://github.com/corda/spring-webserver).

{{< /warning >}}




## Connecting to a node via RPC

To use [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html), you must add `net.corda:corda-rpc:$corda_release_version` as a `cordaCompile` dependency
in your client’s `build.gradle` file.

[CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) has a `start` method that takes the node’s RPC address and returns a [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html).
[CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) has a `proxy` method that takes an RPC username and password and returns a [CordaRPCOps](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/core/messaging/CordaRPCOps.html)
object that you can use to interact with the node.

Here is an example of using [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) to connect to a node and log the current time on its internal clock:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
import net.corda.client.rpc.CordaRPCClient
import net.corda.core.utilities.NetworkHostAndPort.Companion.parse
import net.corda.core.utilities.loggerFor
import org.slf4j.Logger

class ClientRpcExample {
    companion object {
        val logger: Logger = loggerFor<ClientRpcExample>()
    }

    fun main(args: Array<String>) {
        require(args.size == 3) { "Usage: TemplateClient <node address> <username> <password>" }
        val nodeAddress = parse(args[0])
        val username = args[1]
        val password = args[2]

        val client = CordaRPCClient(nodeAddress)
        val connection = client.start(username, password)
        val cordaRPCOperations = connection.proxy

        logger.info(cordaRPCOperations.currentNodeTime().toString())

        connection.notifyServerAndClose()
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
import net.corda.client.rpc.CordaRPCClient;
import net.corda.client.rpc.CordaRPCConnection;
import net.corda.core.messaging.CordaRPCOps;
import net.corda.core.utilities.NetworkHostAndPort;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class ClientRpcExample {
    private static final Logger logger = LoggerFactory.getLogger(ClientRpcExample.class);

    public static void main(String[] args) {
        if (args.length != 3) {
            throw new IllegalArgumentException("Usage: TemplateClient <node address> <username> <password>");
        }
        final NetworkHostAndPort nodeAddress = NetworkHostAndPort.parse(args[0]);
        String username = args[1];
        String password = args[2];

        final CordaRPCClient client = new CordaRPCClient(nodeAddress);
        final CordaRPCConnection connection = client.start(username, password);
        final CordaRPCOps cordaRPCOperations = connection.getProxy();

        logger.info(cordaRPCOperations.currentNodeTime().toString());

        connection.notifyServerAndClose();
    }
}

```
{{% /tab %}}




[ClientRpcExample.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcExample.kt) | [ClientRpcExample.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/ClientRpcExample.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}


{{< warning >}}
The returned [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) is somewhat expensive to create and consumes a small amount of
server side resources. When you’re done with it, call `close` on it. Alternatively you may use the `use`
method on [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) which cleans up automatically after the passed in lambda finishes. Don’t create
a new proxy for every call you make - reuse an existing one.

{{< /warning >}}


For further information on using the RPC API, see [Using the client RPC API](tutorial-clientrpc-api.md).


## RPC permissions

For a node’s owner to interact with their node via RPC, they must define one or more RPC users. Each user is
authenticated with a username and password, and is assigned a set of permissions that control which RPC operations they
can perform. Permissions are not required to interact with the node via the shell, unless the shell is being accessed via SSH.

RPC users are created by adding them to the `rpcUsers` list in the node’s `node.conf` file:

{{< tabs name="tabs-2" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[]
    },
    ...
]
```
{{% /tab %}}

{{< /tabs >}}

By default, RPC users are not permissioned to perform any RPC operations.


### Granting flow permissions

You provide an RPC user with the permission to start a specific flow using the syntax
`StartFlow.<fully qualified flow name>`:

{{< tabs name="tabs-3" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "StartFlow.net.corda.flows.ExampleFlow1",
            "StartFlow.net.corda.flows.ExampleFlow2"
        ]
    },
    ...
]
```
{{% /tab %}}

{{< /tabs >}}

You can also provide an RPC user with the permission to start any flow using the syntax
`InvokeRpc.startFlow`:

{{< tabs name="tabs-4" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc.startFlow"
        ]
    },
    ...
]
```
{{% /tab %}}

{{< /tabs >}}


### Granting other RPC permissions

You provide an RPC user with the permission to perform a specific RPC operation using the syntax
`InvokeRpc.<rpc method name>`:

{{< tabs name="tabs-5" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc.nodeInfo",
            "InvokeRpc.networkMapSnapshot"
        ]
    },
    ...
]
```
{{% /tab %}}

{{< /tabs >}}


### Granting all permissions

You can provide an RPC user with the permission to perform any RPC operation (including starting any flow) using the
`ALL` permission:

{{< tabs name="tabs-6" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "ALL"
        ]
    },
    ...
]
```
{{% /tab %}}

{{< /tabs >}}



## RPC security management

Setting `rpcUsers` provides a simple way of granting RPC permissions to a fixed set of users, but has some
obvious shortcomings. To support use cases aiming for higher security and flexibility, Corda offers additional security
features such as:



* Fetching users credentials and permissions from an external data source (e.g.: a remote RDBMS), with optional in-memory
caching. In particular, this allows credentials and permissions to be updated externally without requiring nodes to be
restarted.
* Password stored in hash-encrypted form. This is regarded as must-have when security is a concern. Corda currently supports
a flexible password hash format conforming to the Modular Crypt Format provided by the [Apache Shiro framework](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html)


These features are controlled by a set of options nested in the `security` field of `node.conf`.
The following example shows how to configure retrieval of users credentials and permissions from a remote database with
passwords in hash-encrypted format and enable in-memory caching of users data:

{{< tabs name="tabs-7" >}}
{{% tab name="groovy" %}}
```groovy
security = {
    authService = {
        dataSource = {
            type = "DB"
            passwordEncryption = "SHIRO_1_CRYPT"
            connection = {
               jdbcUrl = "<jdbc connection string>"
               username = "<db username>"
               password = "<db user password>"
               driverClassName = "<JDBC driver>"
            }
        }
        options = {
             cache = {
                expireAfterSecs = 120
                maxEntries = 10000
             }
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}

It is also possible to have a static list of users embedded in the `security` structure by specifying a `dataSource`
of `INMEMORY` type:

{{< tabs name="tabs-8" >}}
{{% tab name="groovy" %}}
```groovy
security = {
    authService = {
        dataSource = {
            type = "INMEMORY"
            users = [
                {
                    username = "<username>"
                    password = "<password>"
                    permissions = ["<permission 1>", "<permission 2>", ...]
                },
                ...
            ]
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}


{{< warning >}}
A valid configuration cannot specify both the `rpcUsers` and `security` fields. Doing so will trigger
an exception at node startup.

{{< /warning >}}



### Authentication/authorisation data

The `dataSource` structure defines the data provider supplying credentials and permissions for users. There exist two
supported types of such data source, identified by the `dataSource.type` field:



* **INMEMORY**:
A static list of user credentials and permissions specified by the `users` field.


* **DB**:
An external RDBMS accessed via the JDBC connection described by `connection`. Note that, unlike the `INMEMORY`
case, in a user database permissions are assigned to *roles* rather than individual users. The current implementation
expects the database to store data according to the following schema:



* Table `users` containing columns `username` and `password`. The `username` column *must have unique values*.
* Table `user_roles` containing columns `username` and `role_name` associating a user to a set of *roles*.
* Table `roles_permissions` containing columns `role_name` and `permission` associating a role to a set of
permission strings.


{{< note >}}
There is no prescription on the SQL type of each column (although our tests were conducted on `username` and
`role_name` declared of SQL type `VARCHAR` and `password` of `TEXT` type). It is also possible to have extra columns
in each table alongside the expected ones.

{{< /note >}}




### Password encryption

Storing passwords in plain text is discouraged in applications where security is critical. Passwords are assumed
to be in plain format by default, unless a different format is specified by the `passwordEncryption` field, like:

{{< tabs name="tabs-9" >}}
{{% tab name="groovy" %}}
```groovy
passwordEncryption = SHIRO_1_CRYPT
```
{{% /tab %}}

{{< /tabs >}}

`SHIRO_1_CRYPT` identifies the [Apache Shiro fully reversible
Modular Crypt Format](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html),
it is currently the only non-plain password hash-encryption format supported. Hash-encrypted passwords in this
format can be produced by using the [Apache Shiro Hasher command line tool](https://shiro.apache.org/command-line-hasher.html).


### Caching user accounts data

A cache layer on top of the external data source of users credentials and permissions can significantly improve
performances in some cases, with the disadvantage of causing a (controllable) delay in picking up updates to the underlying data.
Caching is disabled by default, it can be enabled by defining the `options.cache` field in `security.authService`,
for example:

{{< tabs name="tabs-10" >}}
{{% tab name="groovy" %}}
```groovy
options = {
     cache = {
        expireAfterSecs = 120
        maxEntries = 10000
     }
}
```
{{% /tab %}}

{{< /tabs >}}

This will enable a non-persistent cache contained in the node’s memory with maximum number of entries set to `maxEntries`
where entries are expired and refreshed after `expireAfterSecs` seconds.


## Observables

The RPC system handles observables in a special way. When a method returns an observable, whether directly or
as a sub-object of the response object graph, an observable is created on the client to match the one on the
server. Objects emitted by the server-side observable are pushed onto a queue which is then drained by the client.
The returned observable may even emit object graphs with even more observables in them, and it all works as you
would expect.

This feature comes with a cost: the server must queue up objects emitted by the server-side observable until you
download them. Note that the server side observation buffer is bounded, once it fills up the client is considered
slow and will be disconnected. You are expected to subscribe to all the observables returned, otherwise client-side
memory starts filling up as observations come in. If you don’t want an observable then subscribe then unsubscribe
immediately to clear the client-side buffers and to stop the server from streaming. For Kotlin users there is a
convenience extension method called `notUsed()` which can be called on an observable to automate this step.

If your app quits then server side resources will be freed automatically.


{{< warning >}}
If you leak an observable on the client side and it gets garbage collected, you will get a warning
printed to the logs and the observable will be unsubscribed for you. But don’t rely on this, as garbage collection
is non-deterministic. If you set `-Dnet.corda.client.rpc.trackRpcCallSites=true` on the JVM command line then
this warning comes with a stack trace showing where the RPC that returned the forgotten observable was called from.
This feature is off by default because tracking RPC call sites is moderately slow.

{{< /warning >}}


{{< note >}}
Observables can only be used as return arguments of an RPC call. It is not currently possible to pass
Observables as parameters to the RPC methods. In other words the streaming is always server to client and not
the other way around.

{{< /note >}}

## Futures

A method can also return a `CordaFuture` in its object graph and it will be treated in a similar manner to
observables. Calling the `cancel` method on the future will unsubscribe it from any future value and release
any resources.


## Versioning

The client RPC protocol is versioned using the node’s platform version number (see [Versioning](versioning.md)). When a proxy is created
the server is queried for its version, and you can specify your minimum requirement. Methods added in later versions
are tagged with the `@RPCSinceVersion` annotation. If you try to use a method that the server isn’t advertising support
of, an `UnsupportedOperationException` is thrown. If you want to know the version of the server, just use the
`protocolVersion` property (i.e. `getProtocolVersion` in Java).

The RPC client library defaults to requiring the platform version it was built with. That means if you use the client
library released as part of Corda N, then the node it connects to must be of version N or above. This is checked when
the client first connects. If you want to override this behaviour, you can alter the `minimumServerProtocolVersion`
field in the `CordaRPCClientConfiguration` object passed to the client. Alternatively, just link your app against
an older version of the library.


## Thread safety

A proxy is thread safe, blocking, and allows multiple RPCs to be in flight at once. Any observables that are returned and
you subscribe to will have objects emitted in order on a background thread pool. Each Observable stream is tied to a single
thread, however note that two separate Observables may invoke their respective callbacks on different threads.


## Error handling

If something goes wrong with the RPC infrastructure itself, an `RPCException` is thrown. If you call a method that
requires a higher version of the protocol than the server supports, `UnsupportedOperationException` is thrown.
Otherwise the behaviour depends on the `devMode` node configuration option.

In `devMode`, if the server implementation throws an exception, that exception is serialised and rethrown on the client
side as if it was thrown from inside the called RPC method. These exceptions can be caught as normal.

When not in `devMode`, the server will mask exceptions not meant for clients and return an `InternalNodeException` instead.
This does not expose internal information to clients, strengthening privacy and security. CorDapps can have exceptions implement
`ClientRelevantError` to allow them to reach RPC clients.


## Reconnecting RPC clients

In the current version of Corda the RPC connection and all the observervables that are created by a client will just throw exceptions and die
when the node or TCP connection become unavailable.

It is the client’s responsibility to handle these errors and reconnect once the node is running again. Running RPC commands against a stopped
node will just throw exceptions. Previously created Observables will not emit any events after the node restarts. The client must explicitly re-run the command and
re-subscribe to receive more events.

RPCs which have a side effect, such as starting flows, may have executed on the node even if the return value is not received by the client.
The only way to confirm is to perform a business-level query and retry accordingly. The sample *runFlowWithLogicalRetry* helps with this.

In case users require such a functionality to write a resilient RPC client we have a sample that showcases how this can be implemented and also
a thorough test that demonstrates it works as expected.

The code that performs the reconnecting logic is: [ReconnectingCordaRPCOps.kt](https://github.com/corda/samples/blob/release-V4/net/corda/client/rpc/internal/ReconnectingCordaRPCOps.kt).

{{< note >}}
This sample code is not exposed as an official Corda API, and must be included directly in the client codebase and adjusted.

{{< /note >}}
The usage is showcased in the: [RpcReconnectTests.kt](https://github.com/corda/samples/blob/release-V4/node/src/integration-test/kotlin/net/corda/node/services/rpc/RpcReconnectTests.kt).
In case resiliency is a requirement, then it is recommended that users will write a similar test.

How to initialize the *ReconnectingCordaRPCOps*:

```kotlin
            val bankAReconnectingRpc = ReconnectingCordaRPCOps(bankAAddress, demoUser.username, demoUser.password)

```

[RpcReconnectTests.kt](https://github.com/corda/corda/blob/release/os/4.1/node/src/integration-test/kotlin/net/corda/node/services/rpc/RpcReconnectTests.kt)

How to track the vault :

```kotlin
            val vaultFeed = bankAReconnectingRpc.vaultTrackByWithPagingSpec(
                    Cash.State::class.java,
                    QueryCriteria.VaultQueryCriteria(),
                    PageSpecification(1, 1))
            val vaultObserverHandle = vaultFeed.updates.asReconnecting().subscribe { update: Vault.Update<Cash.State> ->
                log.info("vault update produced ${update.produced.map { it.state.data.amount }} consumed ${update.consumed.map { it.ref }}")
                vaultEvents.add(update)
            }

```

[RpcReconnectTests.kt](https://github.com/corda/corda/blob/release/os/4.1/node/src/integration-test/kotlin/net/corda/node/services/rpc/RpcReconnectTests.kt)

How to start a flow with a logical retry function that checks for the side effects of the flow:

```kotlin
                bankAReconnectingRpc.runFlowWithLogicalRetry(
                        runFlow = { rpc ->
                            log.info("Starting CashIssueAndPaymentFlow for $amount")
                            val flowHandle = rpc.startTrackedFlowDynamic(
                                    CashIssueAndPaymentFlow::class.java,
                                    baseAmount.plus(Amount.parseCurrency("$amount USD")),
                                    issuerRef,
                                    bankB.nodeInfo.legalIdentities.first(),
                                    false,
                                    notary
                            )
                            val flowId = flowHandle.id
                            log.info("Started flow $amount with flowId: $flowId")
                            flowProgressEvents.addEvent(flowId, null)

                            // No reconnecting possible.
                            flowHandle.progress.subscribe(
                                    { prog ->
                                        flowProgressEvents.addEvent(flowId, prog)
                                        log.info("Progress $flowId : $prog")
                                    },
                                    { error ->
                                        log.error("Error thrown in the flow progress observer", error)
                                    })
                            flowHandle.id
                        },
                        hasFlowStarted = { rpc ->
                            // Query for a state that is the result of this flow.
                            val criteria = QueryCriteria.VaultCustomQueryCriteria(builder { CashSchemaV1.PersistentCashState::pennies.equal(amount.toLong() * 100) }, status = Vault.StateStatus.ALL)
                            val results = rpc.vaultQueryByCriteria(criteria, Cash.State::class.java)
                            log.info("$amount - Found states ${results.states}")
                            // The flow has completed if a state is found
                            results.states.isNotEmpty()
                        },
                        onFlowConfirmed = {
                            flowsCountdownLatch.countDown()
                            log.info("Flow started for $amount. Remaining flows: ${flowsCountdownLatch.count}")
                        }
                )

```

[RpcReconnectTests.kt](https://github.com/corda/corda/blob/release/os/4.1/node/src/integration-test/kotlin/net/corda/node/services/rpc/RpcReconnectTests.kt)

Note that, as shown by the test, during reconnecting some events might be lost.

```kotlin
            // Check that enough vault events were received.
            // This check is fuzzy because events can go missing during node restarts.
            // Ideally there should be nrOfFlowsToRun events receive but some might get lost for each restart.
            assertTrue(vaultEvents!!.size + nrFailures * 2 >= nrOfFlowsToRun, "Not all vault events were received")

```

[RpcReconnectTests.kt](https://github.com/corda/corda/blob/release/os/4.1/node/src/integration-test/kotlin/net/corda/node/services/rpc/RpcReconnectTests.kt)


## Wire security

If TLS communications to the RPC endpoint are required the node should be configured with `rpcSettings.useSSL=true` see [Node configuration](corda-configuration-file.md).
The node admin should then create a node specific RPC certificate and key, by running the node once with `generate-rpc-ssl-settings` command specified (see [Node command-line options](node-commandline.md)).
The generated RPC TLS trust root certificate will be exported to a `certificates/export/rpcssltruststore.jks` file which should be distributed to the authorised RPC clients.

The connecting `CordaRPCClient` code must then use one of the constructors with a parameter of type `ClientRpcSslOptions` ([JavaDoc](https://api.corda.net/api/corda-enterprise/4.1/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html)) and set this constructor
argument with the appropriate path for the `rpcssltruststore.jks` file. The client connection will then use this to validate the RPC server handshake.

Note that RPC TLS does not use mutual authentication, and delegates fine grained user authentication and authorisation to the RPC security features detailed above.


## Whitelisting classes with the Corda node

CorDapps must whitelist any classes used over RPC with Corda’s serialization framework, unless they are whitelisted by
default in `DefaultWhitelist`. The whitelisting is done either via the plugin architecture or by using the
`@CordaSerializable` annotation.  See [Object serialization](serialization.md). An example is shown in [Using the client RPC API](tutorial-clientrpc-api.md).
