---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: corda-enterprise-4-7-corda-nodes-operating-interacting
    name: "Interacting with a node"
    parent: corda-enterprise-4-7-corda-nodes-operating
tags:
- clientrpc
title: Interacting with a node
weight: 3
---

# Interacting with a node

To interact with your node, you need to build an RPC client. This RPC client enables you to connect to a specified server and to make calls to the server that perform various useful tasks. The RPC client must be written in a JVM-compatible language.

Corda Enterprise supports two types of RPC client:
* **Corda RPC Client**, which is used if you want to interact with your node via the `CordaRPCOps` remote interface only.
* **Multi RPC Client**, which is used if you want to interact with your node via any of the other remote interfaces that the Corda node provides.

{{< warning >}}
The built-in Corda test webserver is deprecated and unsuitable for production use. If you want to interact with
your node via HTTP, you will need to stand up your own webserver that connects to your node using the
[CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class. You can find an example of how to do this using the popular Spring Boot server
[here](https://github.com/corda/spring-webserver).
{{< /warning >}}

## Building the Corda RPC Client

To interact with your node via the `CordaRPCOps` remote interface, you need to build a client that uses the [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class. The `CordaRPCClient` class enables you to connect to your node via a message queue protocol and provides a simple RPC interface (the `CordaRPCOps` remote interface) for interacting with the node. You make calls on a JVM object as normal, and the marshalling back-and-forth is handled for you.

### Pre-requisites

To be able to use the [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class, you must add `com.r3.corda:corda-rpc:$corda_release_version` as a `compile` dependency in your client’s `build.gradle` file. As the RPC library has a transitive dependency on a patched version of Caffeine in Corda
Enterprise 4.0, you must add `corda-dependencies` to the list of repositories for your project, as shown in the following example, to resolve
this dependency:

```kotlin
repositories {
    // ... other dependencies
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Caffeine version
}
```

### Connecting to a node with `CordaRPCClient`

The [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class has a `start` method that takes the node’s RPC address and returns a [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html).
[CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) has a `proxy` method that takes an RPC username and password and returns a [CordaRPCOps](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/core/messaging/CordaRPCOps.html)
object that you can use to interact with the node.

Here is an example of using [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) to connect to a node and log the current time on its internal clock:

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

{{< /tabs >}}

{{< warning >}}
The returned [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) is somewhat expensive to create and consumes a small amount of
server-side resources. When you’re done with it, call `close` on it. Alternatively, you would typically employ the `use`
method on [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) which cleans up automatically after the passed-in lambda finishes. Don’t create
a new proxy for every call you make - reuse an existing one.
{{< /warning >}}

For further information on using the RPC API, see [Working with the CordaRPCClient API](../../../../corda-os/4.7/tutorial-clientrpc-api.md).

### Defining RPC users and permissions

To interact with the Corda node via the RPC interface, a node operator must define one or more RPC users. Each user is authenticated with a username and password, and is assigned a set of permissions that control which RPC operations they can perform. To interact with the node via the local shell, permissions are not required. Permissions do, however, have effect if the shell is started via SSH.

#### Defining the RPC users

To define the users for the Corda RPC Client, add each user to the `rpcUsers` list in the node’s `node.conf` file, as shown in the following example:

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

By default, RPC users are not allowed to perform any RPC operations.

#### Granting flow permissions

To grant an RPC user permission to start a specific flow, use the syntax `StartFlow.<fully qualified flow name>`, and the listed `InvokeRpc` permissions, as shown in the following example:

```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc.nodeInfo",
            "InvokeRpc.registeredFlows",
            "InvokeRpc.partiesFromName",
            "InvokeRpc.wellKnownPartyFromX500Name",
            "StartFlow.net.corda.flows.ExampleFlow1",
            "StartFlow.net.corda.flows.ExampleFlow2"
        ]
    },
    ...
]
```

To grant an RPC user permission to start any flow, use the syntax `InvokeRpc.startFlow`, `InvokeRpc.startTrackedFlowDynamic`, and the listed `InvokeRpc` permissions, as shown in the following example:

```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc.nodeInfo",
            "InvokeRpc.registeredFlows",
            "InvokeRpc.partiesFromName",
            "InvokeRpc.wellKnownPartyFromX500Name",
            "InvokeRpc.startFlow",
            "InvokeRpc.startTrackedFlowDynamic"
        ]
    },
    ...
]
```

#### Fixing permissions

If an RPC user tries to perform an RPC operation that they do not have permission for, they will see an error like this:

```
User not authorized to perform RPC call public abstract net.corda.core.node.services.Vault$Page net.corda.core.messaging.CordaRPCOps.vaultQueryByWithPagingSpec(java.lang.Class,net.corda.core.node.services.vault.QueryCriteria,net.corda.core.node.services.vault.PageSpecification) with target []
```

To fix this, you must grant them permissions based on the method name: `InvokeRpc.<method name>`, where `<method name>` is the method name of the `CordaRPCOps` interface.

In this example, the method name is `vaultQueryByWithPagingSpec`, so `InvokeRpc.vaultQueryByWithPagingSpec` must be added to the RPC user's `permissions`.

#### Granting all permissions

To provide an RPC user with the permission to perform any RPC operation (including starting any flow), use the `ALL` permission, as shown in the following example:

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


### Reconnecting the Corda RPC Client

An RPC client connected to a node stops functioning when the node becomes unavailable or the associated TCP connection is interrupted.
Running RPC commands after this has happened will just throw exceptions. Any subscriptions to observables that have been created before the disconnection will stop receiving events after the connection is re-established.
RPC calls that have a side effect, such as starting flows, may or may not have executed on the node, depending on when the client was disconnected.

It is the responsibility of application code to handle these errors and reconnect once the node is running again. The client will have to retrieve new observables and re-subscribe to them in order to keep receiving updates.
With regards to RPCs with side effects (for example, flow invocations), the application code will have to inspect the state of the node to infer whether or not the call was executed on the server side (for example, if the flow was executed or not) before retrying it.

You can make use of the options described below in order to take advantage of some automatic reconnection functionality that mitigates some of these issues.

#### Enabling automatic reconnection

If you provide a list of addresses via the `haAddressPool` argument when instantiating a `CordaRPCClient`, then automatic reconnection will be performed when the existing connection is dropped.
However, the application code is responsible for waiting for the connection to be established again in order to perform any calls, retrieve new observables, and re-subscribe to them.
This can be done by doing any simple RPC call that is free from side effects (for example, `nodeInfo`).

{{< note >}}
Any RPC calls that had not been acknowledged to the RPC client from the node at the point the disconnection happened will fail with a `ConnectionFailureException`.
It is important to note that this does not mean that the node did not execute the RPC calls; it only means that the completion was not acknowledged. As described above, your application code will have to check after the connection is re-established to determine whether these calls were actually executed.
Any observables that were returned before the disconnection will call the `onError` handlers.
{{< /note >}}

#### Enabling graceful reconnection

A more graceful form of reconnection is also available. This will:

* Reconnect any existing observables after a reconnection, so that they keep emitting events to the existing subscriptions.
* Block any RPC calls that arrive during a reconnection or any RPC calls that were not acknowledged at the point of reconnection and will execute them after the connection is re-established.
* By default, continue retrying indefinitely until the connection is re-established. See `CordaRPCClientConfiguration.maxReconnectAttempts` for details of how to adjust the number of retries.

More specifically, the behaviour in the second case is a bit more subtle:

* Any RPC calls that do not have any side effects (for example, `nodeInfo`) will be retried automatically across reconnections.
This will work transparently for application code that will not be able to determine whether there was a reconnection.
These RPC calls will remain blocked during a reconnection and will return successfully after the connection has been re-established.
* Any RPC calls that do have side effects, such as the ones invoking flows (for example, `startFlow`), will not be retried and they will fail with `CouldNotStartFlowException`.
This is done in order to avoid duplicate invocations of a flow, thus providing at-most-once guarantees. Application code is responsible for determining whether the flow needs to be retried and retrying it, if needed.

{{< warning >}}
In this approach, some events might be lost during a reconnection and not sent from the subscribed observables.
{{< /warning >}}

You can enable this graceful form of reconnection by using the `gracefulReconnect` parameter, which is an object containing 3 optional fields:

* `onDisconnect`: A callback handler that is invoked every time the connection is disconnected.
* `onReconnect`: A callback handler that is invoked every time the connection is established again after a disconnection.
* `maxAttempts`: The maximum number of attempts that will be performed per *RPC operation*. A negative value implies infinite retries. The default value is 5.

This can be used in the following way:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}

```kotlin
val gracefulReconnect = GracefulReconnect(onDisconnect={/*insert disconnect handling*/}, onReconnect{/*insert reconnect handling*/}, maxAttempts = 3)
val cordaClient = CordaRPCClient(nodeRpcAddress)
val cordaRpcOps = cordaClient.start(rpcUserName, rpcUserPassword, gracefulReconnect = gracefulReconnect).proxy
```

{{% /tab %}}

{{% tab name="java" %}}

```java
private void onDisconnect() {
    // Insert implementation
}

private void onReconnect() {
    // Insert implementation
}

void method() {
    GracefulReconnect gracefulReconnect = new GracefulReconnect(this::onDisconnect, this::onReconnect, 3);
    CordaRPCClient cordaClient = new CordaRPCClient(nodeRpcAddress);
    CordaRPCConnection cordaRpcOps = cordaClient.start(rpcUserName, rpcUserPassword, gracefulReconnect);
}
```

{{% /tab %}}

{{< /tabs >}}

#### Retrying flow invocations

As implied above, when graceful reconnection is enabled, flow invocations will not be retried across reconnections to avoid duplicate invocations.
This retrying can be done from the application code after checking whether the flow was triggered previously by inspecting whether its side-effects have taken place.
The following is a simplified example of what your code might look like:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}

```kotlin
fun runFlowWithRetries(client: CordaRPCOps) {
    try {
        client.startFlowDynamic(...)
    } catch (exception: CouldNotStartFlowException) {
        if (!wasFlowTriggered()) {
            runFlowWithRetries(client)
        }
    }
}
```

{{% /tab %}}

{{% tab name="java" %}}

```java
void runFlowWithRetries(CordaRPCOps client) {
    try {
        client.startFlowDynamic(...);
    } catch (CouldNotStartFlowException exception) {
        if (!wasFlowTriggered()) {
            runFlowWithRetries(client);
        }
    }
}
```

{{% /tab %}}

{{< /tabs >}}

The logic of the `wasFlowTriggered()` function is naturally dependent on the flow logic, so it can differ per use case.

{{< warning >}}
This approach provides at-least-once guarantees. It cannot provide exactly-once guarantees, because of race conditions between the moment the check is performed and the moment the side effects of the flow become visible.
{{< /warning >}}

## Building the Multi RPC Client

Corda Enterprise exposes a number of custom, remote RPC interfaces.

To interact with your node via any of the following interfaces, you need to build a client that uses the [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) class:

* `net.corda.client.rpc.proxy.AuditDataRPCOps` - This interface enables you to audit the log of RPC activity.
* `net.corda.client.rpc.proxy.FlowRPCOps` - This interface enables you to retry a previously hospitalised flow.
* `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps` - This interface enables external applications to query and view the status of the flows which are currently under monitoring by the Flow Hospital.
* `net.corda.client.rpc.proxy.NodeHealthCheckRpcOps` - This interface enables you to get a report about the health of the Corda Enterprise node.
* `net.corda.client.rpc.proxy.notary.NotaryQueryRpcOps` - This interface enables you to perform a spend audit for a particular state reference.

All of these interfaces are located in the `:client:extensions-rpc` module.

{{< note >}}
`COMPLETED`, `FAILED`, and `KILLED` flows can only be queried when started by the `startFlowWithClientId` or `startFlowDynamicWithClientId` APIs using a unique, client-provided ID. For more information, see [Starting a flow with a client-provided unique ID](../../flow-start-with-client-id.md).
{{< /note >}}

{{< note >}}
`CordaRPCClient` enables you to interact with the `CordaRPCOps` remote interface. However, if you intend to interact with any of the other remote interfaces that the Corda Enterprise provides, you need to build a client that uses the [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) class.
{{< /note >}}

### Pre-requisites

To use the functionality of the [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) class from a custom JVM application, you must include the following
dependencies:

```groovy
dependencies {
    compile "net.corda:corda-rpc:$corda_release_version"
    compile "net.corda:corda-rpc-ext:$corda_release_version"
    ...
}
```
### Defining RPC users and permissions

On the Corda Enterprise node side, you must define one or more RPC users and grant permissions to those users to invoke remote methods. To do this, you must edit the `node.conf` file.

#### Granting all permissions

To provide an RPC user with the permission to all the methods of an interface, use the syntax `InvokeRpc.<interface name>#ALL` in the `node.conf` file.

For example, to grant permissions to all the methods of the `net.corda.client.rpc.proxy.NodeHealthCheckRpcOps` interface, you must include the syntax `InvokeRpc:net.corda.client.rpc.proxy.NodeHealthCheckRpcOps#ALL` in the `node.conf` file, as shown in the following code snippet:

```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc:net.corda.client.rpc.proxy.NodeHealthCheckRpcOps#ALL"
        ]
    },
    ...
]
```

#### Granting permissions for RPC operations

To grant permissions in situations where multiple RPC interfaces are running within a single node, you can use the `InvokeRpc` syntax in the `node.conf` file to specify permissions for a particular interface.

The `InvokeRpc` syntax can take any of the following forms:

* `InvokeRpc:com.fully.qualified.package.CustomClientRpcOps#firstMethod`

  Here, we are assuming that that there is a fully qualified interface `com.fully.qualified.package.CustomClientRpcOps` which has a method `firstMethod` permission to which we are specifying explicitly.

* `InvokeRpc:com.fully.qualified.package.CustomClientRpcOps#ALL`

  Here, we are granting permissions to all the methods of the `com.fully.qualified.package.CustomClientRpcOps` interface.

* `InvokeRpc:com.fully.qualified.package.CustomClientRpcOps#READ_ONLY`

  Here, we are granting permissions to a group of methods or properties that have been marked with `@RpcPermissionGroup(READ_ONLY)`. You can define as many groups as necessary and mark `RPCOps` interface methods as necessary. Each method may belong to multiple groups.

{{% note %}}
It is not uncommon for `RPCOps` interfaces to inherit from each other. Permissions to specific methods or methods groups should always be expressed using the declaring interface name. When granting RPC permissions, a node operator should disregard the `RPCOps` interfaces hierarchy.
{{% /note %}}

Consider the following interface definition in `com.fully.qualified.package` package:

```kotlin
interface Alpha : RPCOps {
    @RpcPermissionGroup(READ_ONLY)
    fun readAlpha() : String
}

interface Beta : Alpha {
    @RpcPermissionGroup(READ_ONLY, SENSITIVE)
    val betaValue : Int

    @RpcPermissionGroup(SENSITIVE)
    fun writeBeta(foo: Int)

    fun nothingSpecial() : Int
}
```

To grant permission to the `nothingSpecial()` method, you would use the syntax `InvokeRpc:com.fully.qualified.package.Beta#nothingSpecial`.

To grant permission to the `readAlpha()` method, you would use the syntax `InvokeRpc:com.fully.qualified.package.Alpha#readAlpha`, even though by inheritance, the `readAlpha()` method is also present in the `Beta` interface.

To grant permission to the `betaValue` property only, but not to the `readAlpha()` method, you would use the syntax `InvokeRpc:com.fully.qualified.package.Beta#READ_ONLY`.

To grant permission to the `readAlpha()` method only, but not to the `betaValue` property, you would use the syntax `InvokeRpc:com.fully.qualified.package.Alpha#READ_ONLY`.

{{% note %}}
Permission strings are case-insensitive.
{{% /note %}}

### Connecting to a node with `MultiRPCClient`

The code snippet below demonstrates how to use the [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) class  to build a Multi RPC Client and define the following:

* Endpoint address
* Interface class to be used for communication (in this example, `NodeHealthCheckRpcOps::class.java`, which is used to communicate with the `net.corda.client.rpc.proxy.NodeHealthCheckRpcOps` interface)
* User name
* Password

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}

```kotlin
val client = MultiRPCClient(rpcAddress, NodeHealthCheckRpcOps::class.java, "exampleUser", "examplePass")

client.use {
    val connFuture: CompletableFuture<RPCConnection<NodeHealthCheckRpcOps>> = client.start()
    val conn: RPCConnection<NodeHealthCheckRpcOps> = connFuture.get()
    conn.use {
        assertThat(it.proxy.runtimeInfo(), containsString("usedMemory"))
    }
}
```

{{% /tab %}}

{{% tab name="java" %}}

```java
try(MultiRPCClient client = new MultiRPCClient(rpcAddress, NodeHealthCheckRpcOps.class, "exampleUser", "examplePass")) {
    CompletableFuture<RPCConnection<NodeHealthCheckRpcOps>> connFuture = client.start();
    try(RPCConnection<NodeHealthCheckRpcOps> conn = connFuture.get()) {
        assertThat(conn.getProxy().runtimeInfo(), containsString("usedMemory"));
    }
}
```

{{% /tab %}}

{{< /tabs >}}

`MultiRPCClient` is not started upon its creation, thus enabling you to perform any additional configuration steps that may be required and attach
`RPCConnectionListener`s if necessary before starting.

When the `start` method is called on `MultiRPCClient`, it performs a remote call to establish an RPC connection with the specified endpoint.
The connection is not created instantly. For this reason, the `start()` method returns `Future` over `RPCConnection` for the specified remote interface type.

Once the connection has been created, it is possible to obtain a `proxy` and perform a remote call. In the example above, this is demonstrated by a
 call to the `runtimeInfo()` method of `NodeHealthCheckRpcOps` interface.

As some internal resources are allocated to `MultiRPCClient`, it is recommended that you call the `close()` method when the `MultiRPCClient` is no longer needed. In Kotlin, you would typically employ the `use` construct for this purpose. In Java, you can use `try-with-resource`.

`RPCConnection` is also a `Closeable` construct, so it is a good idea to call `close()` on it after use.


### Specifying multiple endpoint addresses

You can pass in multiple endpoint addresses when constructing `MultiRPCClient`.
If you do so, `MultiRPCClient` will operate in fail-over mode and if one of the endpoints becomes unreachable, it will automatically re-try the connection using a round-robin policy.

For more information, see the API documentation for [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html).

### Adding RPC connection listeners

If the reconnection cycle has started, the previously supplied `RPCConnection` may become interrupted and `proxy` will throw an
`RPCException` every time the remote method is called.

To be notified when the connection has been re-established or, indeed, to receive notifications throughout the lifecycle of every connection, you can add one or more [RPCConnectionListeners](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/RPCConnectionListener.html) to `MultiRPCClient`.
For more information, see [RPCConnectionListener](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/RPCConnectionListener.html) in the API documentation.

### Specifying RPC connection parameters
Many constructors are available for `MultiRPCClient`. This enables you to specify a variety of other configuration parameters relating to the RPC connection. The parameters for `MultiRPCClient` are largely similar to the parameters for [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html). For more information, see [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) in the API documentation.

## Managing RPC security

Setting `rpcUsers` provides a simple way of granting RPC permissions to a fixed set of users, but has some
obvious shortcomings. To support use cases aiming for higher security and flexibility, Corda offers additional security
features such as:

* Fetching users' credentials and permissions from an external data source (for example, from a remote RDBMS), with optional in-memory
caching. This allows credentials and permissions to be updated externally without requiring nodes to be
restarted.
* Passwords are stored in hash-encrypted form. This is regarded as a must-have when security is a concern. Corda currently supports
a flexible password hash format that conforms to the Modular Crypt Format provided by the [Apache Shiro framework](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html).

These features are controlled by a set of options nested in the `security` field of `node.conf`.
The following example shows how to configure retrieval of users' credentials and permissions from a remote database where
passwords are stored in hash-encrypted format and how to enable in-memory caching of users' data:

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

It is also possible to have a static list of users embedded in the `security` structure by specifying a `dataSource`
of `INMEMORY` type:

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

{{< warning >}}
For a valid configuration, you cannot specify both the `rpcUsers` and `security` fields. Doing so will trigger
an exception at node startup.
{{< /warning >}}

### Specifying authentication/authorisation data

The `dataSource` structure defines the data provider supplying credentials and permissions for users. There exist two
supported types of such data source, identified by the `dataSource.type` field:

* `INMEMORY`:
A static list of user credentials and permissions specified by the `users` field.

* `DB`:
An external RDBMS accessed via the JDBC connection described by `connection`. Note that, unlike the `INMEMORY`
case, in a user database, permissions are assigned to _roles_ rather than individual users. The current implementation
expects the database to store data according to the following schema:

  * Table `users` containing columns `username` and `password`. The `username` column *must have unique values*.
  * Table `user_roles` containing columns `username` and `role_name` associating a user to a set of *roles*.
  * Table `roles_permissions` containing columns `role_name` and `permission` associating a role with a set of
permission strings.

{{< note >}}
The SQL type of each column is not prescribed (although our tests were conducted on `username` and
`role_name` declared as the SQL type `VARCHAR` and `password`, declared as the type `TEXT`). In addition to the expected columns, you can include extra columns
in each table as needed.
{{< /note >}}

### Encrypting passwords

Storing passwords in plain text is discouraged in applications where security is critical. Passwords are assumed
to be in plain format by default, unless a different format is specified by the `passwordEncryption` field, as shown in the following example:

```groovy
passwordEncryption = SHIRO_1_CRYPT
```

`SHIRO_1_CRYPT` identifies the [Apache Shiro fully reversible
Modular Crypt Format](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html). This is currently the only non-plain password hash-encryption format supported. Hash-encrypted passwords in this
format can be produced by using the [Apache Shiro Hasher command line tool](https://shiro.apache.org/command-line-hasher.html).

### Caching user account data

A cache layer on top of the external data source of users' credentials and permissions can significantly improve
performance in some cases, with the disadvantage of causing a (controllable) delay in picking up updates to the underlying data.
Caching is disabled by default. It can be enabled by defining the `options.cache` field in `security.authService`,
as shown in the following example:

```groovy
options = {
     cache = {
        expireAfterSecs = 120
        maxEntries = 10000
     }
}
```

This enables a non-persistent cache to be created in the node’s memory with a maximum number of entries set to `maxEntries` and
where entries are expired and refreshed after `expireAfterSecs` seconds.

## Working with observables

The RPC system handles observables in a special way. When a method returns an observable, whether directly or
as a sub-object of the response object graph, an observable is created on the client to match the one on the
server. Objects emitted by the server-side observable are pushed onto a queue which is then drained by the client.
The returned observable may even emit object graphs with even more observables in them, and it all works as you
would expect.

This feature comes with a cost: the server must queue up objects emitted by the server-side observable until you
download them. Note that the server-side observation buffer is bounded, once it fills up, the client is considered
slow and will be disconnected. You are expected to subscribe to all the observables returned, otherwise client-side
memory starts filling up as observations come in. If you don’t want an observable, then subscribe then unsubscribe
immediately to clear the client-side buffers and to stop the server from streaming. For Kotlin users, there is a
convenience extension method called `notUsed()` which can be called on an observable to automate this step.

If your app quits, then server-side resources will be freed automatically.

{{< warning >}}
If you leak an observable on the client side and it gets garbage collected, a warning is
printed to the logs and the observable will be unsubscribed for you. But don’t rely on this, as garbage collection
is non-deterministic. If you set `-Dnet.corda.client.rpc.trackRpcCallSites=true` on the JVM command line, then
this warning includes a stack trace showing where the RPC that returned the forgotten observable was called from.
This feature is off by default because tracking RPC call sites is moderately slow.

{{< /warning >}}

{{< note >}}
Observables can only be used as return arguments of an RPC call. It is not currently possible to pass
observables as parameters to the RPC methods. In other words, the streaming is always server to client and not
the other way around.
{{< /note >}}

## Working with futures

A method can also return a `CordaFuture` in its object graph and it will be treated in a similar manner to
observables. Calling the `cancel` method on the future will unsubscribe it from any future value and release
any resources.

## Versioning

The client RPC protocol is versioned using the node’s platform version number (see [Versioning](../../cordapps/versioning.md)). When a proxy is created,
the server is queried for its version, and you can specify your minimum requirement. Methods added in later versions
are tagged with the `@RPCSinceVersion` annotation. If you try to use a method that the server isn’t advertising support
for, an `UnsupportedOperationException` is thrown. If you want to know the version of the server, just use the
`protocolVersion` property in Kotlin or `getProtocolVersion` in Java.

The RPC client library defaults to requiring the platform version it was built with. That means if you use the client
library released as part of Corda N, then the node it connects to must be of version N or above. This is checked when
the client first connects. If you want to override this behaviour, you can alter the `minimumServerProtocolVersion`
field in the `CordaRPCClientConfiguration` object passed to the client. Alternatively, just link your app against
an older version of the library.

## Managing thread safety

A proxy is thread safe, blocking, and allows multiple RPCs to be in flight at once. Any observables that are returned and
you subscribe to will have objects emitted in order on a background thread pool. Each observable stream is tied to a single
thread. However, note that two separate observables may invoke their respective callbacks on different threads.

## Handling errors

If something goes wrong with the RPC infrastructure itself, an `RPCException` is thrown. If something
goes wrong that needs a manual intervention to resolve (for example, a configuration error), an
`UnrecoverableRPCException` is thrown. If you call a method that requires a higher version of the protocol
than the server supports, `UnsupportedOperationException` is thrown. Otherwise, the behaviour depends
on the `devMode` node configuration option.

If the server implementation throws an exception, that exception is serialised and re-thrown on the client
side as if it were thrown from inside the called RPC method. These exceptions can be caught as normal.

## Configuring wire security

If TLS communications to the RPC endpoint are required, the node must be configured with `rpcSettings.useSSL=true` (see [Node configuration options](../setup/corda-configuration-file)).
The node admin must then create a node-specific RPC certificate and key, by running the node once with the `generate-rpc-ssl-settings` command specified (see [Node command-line options](../node-commandline.md)).
The generated RPC TLS trust root certificate is exported to a `certificates/export/rpcssltruststore.jks` file, which should be distributed to the authorised RPC clients.

The connecting `CordaRPCClient` code must then use one of the constructors with a parameter of type `ClientRpcSslOptions` ([JavaDoc](https://api.corda.net/api/corda-enterprise/4.7/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html)) and set this constructor
argument with the appropriate path for the `rpcssltruststore.jks` file. The client connection will then use this to validate the RPC server handshake.

Note that RPC TLS does not use mutual authentication, and delegates fine-grained user authentication and authorisation to the RPC security features detailed under [Managing RPC security](#managing-rpc-security).

## Whitelisting classes with the Corda node

CorDapps must whitelist any classes used over RPC with Corda’s serialization framework, unless they are whitelisted by
default in `DefaultWhitelist`. The whitelisting is done either via the plugin architecture or by using the
`@CordaSerializable` annotation (see [Serialization](../../serialization-index.md)). An example is shown in [Working with the CordaRPCClient API](../../../../corda-os/4.7/tutorial-clientrpc-api.md).
