---
aliases:
- /releases/4.4/node/operating/clientrpc.html
- /docs/corda-enterprise/head/node/operating/clientrpc.html
- /docs/corda-enterprise/node/operating/clientrpc.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    identifier: corda-enterprise-4-4-corda-nodes-operating-interacting
    name: "Interacting with a node"
    parent: corda-enterprise-4-4-corda-nodes-operating
tags:
- clientrpc
title: Interacting with a node
weight: 3
---

# Interacting with a node

To interact with your node, you need to write a client in a JVM-compatible language using the [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class.
This class allows you to connect to your node via a message queue protocol and provides a simple RPC interface for
interacting with the node. You make calls on a JVM object as normal, and the marshalling back-and-forth is handled for
you.


{{< warning >}}
The built-in Corda test webserver is deprecated and unsuitable for production use. If you want to interact with
your node via HTTP, you will need to stand up your own webserver that connects to your node using the
[CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class. You can find an example of how to do this using the popular Spring Boot server
[here](https://github.com/corda/spring-webserver).

{{< /warning >}}




## Connecting to a node via RPC

To use [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html), you must add `com.r3.corda:corda-rpc:$corda_release_version` as a `compile` dependency
in your client’s `build.gradle` file. As the RPC library has a transitive dependency on a patched version of Caffeine in Corda
Enterprise 4.0, you also need to add `corda-dependencies` to the list of repositories for your project in order to resolve
this dependency:

```kotlin
repositories {
    // ... other dependencies
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Caffeine version
}
```

[CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) has a `start` method that takes the node’s RPC address and returns a [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html).
[CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) has a `proxy` method that takes an RPC username and password and returns a [CordaRPCOps](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/core/messaging/CordaRPCOps.html)
object that you can use to interact with the node.

Here is an example of using [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) to connect to a node and log the current time on its internal clock:

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

[ClientRpcExample.kt](https://github.com/corda/enterprise/blob/release/ent/4.6/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/ClientRpcExample.kt) | [ClientRpcExample.java](https://github.com/corda/enterprise/blob/release/ent/4.6/docs/source/example-code/src/main/java/net/corda/docs/java/ClientRpcExample.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

{{< warning >}}
The returned [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) is somewhat expensive to create and consumes a small amount of
server side resources. When you’re done with it, call `close` on it. Alternatively you may use the `use`
method on [CordaRPCClient](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) which cleans up automatically after the passed in lambda finishes. Don’t create
a new proxy for every call you make - reuse an existing one.

{{< /warning >}}


For further information on using the RPC API, see [Using the client RPC API](../../../../corda-os/4.4/tutorial-clientrpc-api.md).


## RPC permissions

For a node’s owner to interact with their node via RPC, they must define one or more RPC users. Each user is
authenticated with a username and password, and is assigned a set of permissions that control which RPC operations they
can perform. Permissions are not required to interact with the node via the shell, unless the shell is being accessed via SSH.

RPC users are created by adding them to the `rpcUsers` list in the node’s `node.conf` file:

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

By default, RPC users are not permissioned to perform any RPC operations.


### Granting flow permissions

You provide an RPC user with the permission to start a specific flow using the syntax
`StartFlow.<fully qualified flow name>`:

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

You can also provide an RPC user with the permission to start any flow using the syntax
`InvokeRpc.startFlow`:

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


### Granting other RPC permissions

You provide an RPC user with the permission to perform a specific RPC operation using the syntax
`InvokeRpc.<rpc method name>`:

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


### Granting all permissions

You can provide an RPC user with the permission to perform any RPC operation (including starting any flow) using the
`ALL` permission:

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



## RPC security management

Setting `rpcUsers` provides a simple way of granting RPC permissions to a fixed set of users, but has some
obvious shortcomings. To support use cases aiming for higher security and flexibility, Corda offers additional security
features such as:



* Fetching users' credentials and permissions from an external data source (e.g.: a remote RDBMS), with optional in-memory
caching. In particular, this allows credentials and permissions to be updated externally without requiring nodes to be
restarted.
* Password stored in hash-encrypted form. This is regarded as must-have when security is a concern. Corda currently supports
a flexible password hash format conforming to the Modular Crypt Format provided by the [Apache Shiro framework](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html)


These features are controlled by a set of options nested in the `security` field of `node.conf`.
The following example shows how to configure retrieval of users' credentials and permissions from a remote database with
passwords in hash-encrypted format and enable in-memory caching of users' data:

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

```groovy
passwordEncryption = SHIRO_1_CRYPT
```

`SHIRO_1_CRYPT` identifies the [Apache Shiro fully reversible
Modular Crypt Format](https://shiro.apache.org/static/1.2.5/apidocs/org/apache/shiro/crypto/hash/format/Shiro1CryptFormat.html),
it is currently the only non-plain password hash-encryption format supported. Hash-encrypted passwords in this
format can be produced by using the [Apache Shiro Hasher command line tool](https://shiro.apache.org/command-line-hasher.html).


### Caching user accounts data

A cache layer on top of the external data source of users' credentials and permissions can significantly improve
performances in some cases, with the disadvantage of causing a (controllable) delay in picking up updates to the underlying data.
Caching is disabled by default, it can be enabled by defining the `options.cache` field in `security.authService`,
for example:

```groovy
options = {
     cache = {
        expireAfterSecs = 120
        maxEntries = 10000
     }
}
```

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
immediately to clear the client-side buffers and to stop the server from streaming. For Kotlin users, there is a
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

The client RPC protocol is versioned using the node’s platform version number (see [Versioning](../../cordapps/versioning.md)). When a proxy is created
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

If something goes wrong with the RPC infrastructure itself, an `RPCException` is thrown.  If something
goes wrong that needs a manual intervention to resolve (e.g. a configuration error), an
`UnrecoverableRPCException` is thrown. If you call a method that requires a higher version of the protocol
than the server supports, `UnsupportedOperationException` is thrown. Otherwise the behaviour depends
on the `devMode` node configuration option.

If the server implementation throws an exception, that exception is serialised and rethrown on the client
side as if it was thrown from inside the called RPC method. These exceptions can be caught as normal.


## Reconnecting RPC clients

In the current version of Corda, an RPC client connected to a node stops functioning when the node becomes unavailable or the associated TCP connection is interrupted.
Running RPC commands after this has happened will just throw exceptions. Any subscriptions to `Observable`s that have been created before the disconnection will stop receiving events after the connection is re-established.
RPC calls that have a side effect, such as starting flows, may or may not have executed on the node depending on when the client was disconnected.

It is the responsibility of application code to handle these errors and reconnect once the node is running again. The client will have to retrieve new `Observable`s and re-subscribe to them in order to keep receiving updates.
With regards to RPCs with side effects (e.g. flow invocations), the application code will have to inspect the state of the node to infer whether the call was executed on the server side (e.g. if the flow was executed or not) before retrying it.

You can make use of the options described below in order to take advantage of some automatic reconnection functionality that mitigates some of these issues.


### Enabling automatic reconnection

If you provide a list of addresses via the `haAddressPool` argument when instantiating a `CordaRPCClient`, then automatic reconnection will be performed when the existing connection is dropped.
However, the application code is responsible for waiting for the connection to be established again in order to perform any calls, retrieve new observables and re-subscribe to them.
This can be done by doing a simple, side-effect free RPC call (e.g. `nodeInfo`).

{{< note >}}
Any RPC calls that had not been acknowledged to the RPC client from the node at the point the disconnection happened, they will fail with a `ConnectionFailureException`.
It is important to note this does not mean the node did not execute the RPC calls, it only means the completion was not acknowledged. As described above, application code will have to check after the connection is re-established to determine whether these calls were actually executed.
Any observables that were returned before the disconnection will call the `onError` handlers.

{{< /note >}}

### Enabling graceful reconnection

A more graceful form of reconnection is also available. This will:


* reconnect any existing `Observable`s after a reconnection, so that they keep emitting events to the existing subscriptions.
* block any RPC calls that arrive during a reconnection or any RPC calls that were not acknowledged at the point of reconnection and will execute them after the connection is re-established.
* by default continue retrying indefinitely until the connection is re-established.  See `CordaRPCClientConfiguration.maxReconnectAttempts` for adjusting the number of retries.

More specifically, the behaviour in the second case is a bit more subtle:


* Any RPC calls that do not have any side-effects (e.g. `nodeInfo`) will be retried automatically across reconnections.
This will work transparently for application code that will not be able to determine whether there was a reconnection.
These RPC calls will remain blocked during a reconnection and will return successfully after the connection has been re-established.
* Any RPC calls that do have side-effects, such as the ones invoking flows (e.g. `startFlow`), will not be retried and they will fail with `CouldNotStartFlowException`.
This is done in order to avoid duplicate invocations of a flow, thus providing at-most-once guarantees. Application code is responsible for determining whether the flow needs to be retried and retrying it, if needed.


{{< warning >}}
In this approach, some events might be lost during a reconnection and not sent from the subscribed `Observable`s.

{{< /warning >}}


You can enable this graceful form of reconnection by using the `gracefulReconnect` parameter, which is an object containing 3 optional fields:


* `onDisconnect`: A callback handler that will be invoked every time the connection is disconnected.
* `onReconnect`: A callback handler that will be invoked every time the connection is established again after a disconnection.
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


### Retrying flow invocations

As implied above, when graceful reconnection is enabled, flow invocations will not be retried across reconnections to avoid duplicate invocations.
This retrying can be done from the application code after checking whether the flow was triggered previously by inspecting whether its side-effects have taken place.
A simplified, sample skeleton of such code could look like the following code:

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

The logic of the `wasFlowTriggered()` function is naturally dependent on the flow logic, so it can differ per use-case.


{{< warning >}}
This approach provides at-least-once guarantees. It cannot provide exactly-once guarantees, because of race conditions between the moment the check is performed and the moment the side-effects of the flow become visible.

{{< /warning >}}



## Wire security

If TLS communications to the RPC endpoint are required, the node must be configured with `rpcSettings.useSSL=true` (see [Node configuration options](../setup/corda-configuration-file)).
The node admin must then create a node-specific RPC certificate and key, by running the node once with the `generate-rpc-ssl-settings` command specified (see [Node command-line options](../node-commandline.md)).

The generated RPC TLS trust root certificate will be exported to a `certificates/export/rpcssltruststore.jks` file which should be distributed to the authorised RPC clients.

The connecting `CordaRPCClient` code must then use one of the constructors with a parameter of type `ClientRpcSslOptions` ([JavaDoc](https://api.corda.net/api/corda-enterprise/4.4/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html)) and set this constructor
argument with the appropriate path for the `rpcssltruststore.jks` file. The client connection will then use this to validate the RPC server handshake.

Note that RPC TLS does not use mutual authentication, and delegates fine grained user authentication and authorisation to the RPC security features detailed above.


## Whitelisting classes with the Corda node

CorDapps must whitelist any classes used over RPC with Corda’s serialization framework, unless they are whitelisted by
default in `DefaultWhitelist`. The whitelisting is done either via the plugin architecture or by using the
`@CordaSerializable` annotation (see [Object serialization](../../serialization.md)). An example is shown in [Using the client RPC API](../../../../corda-os/4.4/tutorial-clientrpc-api.md).
