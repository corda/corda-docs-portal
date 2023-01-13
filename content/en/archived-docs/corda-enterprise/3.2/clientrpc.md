---
aliases:
- /releases/3.2/clientrpc.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-clientrpc
    parent: corda-enterprise-3-2-corda-nodes-index
    weight: 1060
tags:
- clientrpc
title: Client RPC
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Client RPC



## Overview

Corda provides a client library that allows you to easily write clients in a JVM-compatible language to interact
with a running node. The library connects to the node using a message queue protocol and then provides a simple RPC
interface to interact with the node. You make calls on a Java object as normal, and the marshalling back and forth is
handled for you.

The starting point for the client library is the [CordaRPCClient](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) class. [CordaRPCClient](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) provides a `start` method
that returns a [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html). A [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) allows you to access an implementation of the
[CordaRPCOps](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/core/messaging/CordaRPCOps.html) interface with `proxy` in Kotlin or `getProxy()` in Java. The observables that are returned by RPC
operations can be subscribed to in order to receive an ongoing stream of updates from the node. More detail on this
functionality is provided in the docs for the `proxy` method.


{{< warning >}}
The returned [CordaRPCConnection](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCConnection.html) is somewhat expensive to create and consumes a small amount of
server side resources. When you’re done with it, call `close` on it. Alternatively you may use the `use`
method on [CordaRPCClient](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/rpc/CordaRPCClient.html) which cleans up automatically after the passed in lambda finishes. Don’t create
a new proxy for every call you make - reuse an existing one.

{{< /warning >}}


For a brief tutorial on using the RPC API, see [Using the client RPC API](tutorial-clientrpc-api.md).


## RPC permissions

For a node’s owner to interact with their node via RPC, they must define one or more RPC users. Each user is
authenticated with a username and password, and is assigned a set of permissions that control which RPC operations they
can perform. Permissions are not required to interact with the node via the shell, unless the shell is being accessed via SSH.

RPC users are created by adding them to the `rpcUsers` list in the node’s `node.conf` file:

{{< tabs name="tabs-1" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[]
    }
    ...
]
```
{{% /tab %}}

{{< /tabs >}}

By default, RPC users are not permissioned to perform any RPC operations.


### Granting flow permissions

You provide an RPC user with the permission to start a specific flow using the syntax
`StartFlow.<fully qualified flow name>`:

{{< tabs name="tabs-2" >}}
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
    }
    ...
]
```
{{% /tab %}}

{{< /tabs >}}

You can also provide an RPC user with the permission to start any flow using the syntax
`InvokeRpc.startFlow`:

{{< tabs name="tabs-3" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "InvokeRpc.startFlow"
        ]
    }
    ...
]
```
{{% /tab %}}

{{< /tabs >}}


### Granting other RPC permissions

You provide an RPC user with the permission to perform a specific RPC operation using the syntax
`InvokeRpc.<rpc method name>`:

{{< tabs name="tabs-4" >}}
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
    }
    ...
]
```
{{% /tab %}}

{{< /tabs >}}


### Granting all permissions

You can provide an RPC user with the permission to perform any RPC operation (including starting any flow) using the
`ALL` permission:

{{< tabs name="tabs-5" >}}
{{% tab name="groovy" %}}
```groovy
rpcUsers=[
    {
        username=exampleUser
        password=examplePass
        permissions=[
            "ALL"
        ]
    }
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

{{< tabs name="tabs-6" >}}
{{% tab name="groovy" %}}
```groovy
security = {
    authService = {
        dataSource = {
            type = "DB",
            passwordEncryption = "SHIRO_1_CRYPT",
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

{{< tabs name="tabs-7" >}}
{{% tab name="groovy" %}}
```groovy
security = {
    authService = {
        dataSource = {
            type = "INMEMORY",
            users = [
                {
                    username = "<username>",
                    password = "<password>",
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

{{< tabs name="tabs-8" >}}
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

{{< tabs name="tabs-9" >}}
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
slow and kicked. You are expected to subscribe to all the observables returned, otherwise client-side memory starts
filling up as observations come in. If you don’t want an observable then subscribe then unsubscribe immediately to
clear the client-side buffers and to stop the server from streaming. If your app quits then server side resources
will be freed automatically.


{{< warning >}}
If you leak an observable on the client side and it gets garbage collected, you will get a warning
printed to the logs and the observable will be unsubscribed for you. But don’t rely on this, as garbage collection
is non-deterministic.

{{< /warning >}}



## Futures

A method can also return a `ListenableFuture` in its object graph and it will be treated in a similar manner to
observables. Calling the `cancel` method on the future will unsubscribe it from any future value and release any resources.


## Versioning

The client RPC protocol is versioned using the node’s Platform Version (see [Versioning](versioning.md)). When a proxy is created
the server is queried for its version, and you can specify your minimum requirement. Methods added in later versions
are tagged with the `@RPCSinceVersion` annotation. If you try to use a method that the server isn’t advertising support
of, an `UnsupportedOperationException` is thrown. If you want to know the version of the server, just use the
`protocolVersion` property (i.e. `getProtocolVersion` in Java).


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
This does not expose internal information to clients, strengthening privacy and security. CorDapps can have exceptions implement `ClientRelevantError` to allow them to reach RPC clients.


## Connection management

It is possible to not be able to connect to the server on the first attempt. In that case, the `CordaRPCCLient.start()`
method will throw an exception. The following code snippet is an example of how to write a simple retry mechanism for
such situations:

```Kotlin
fun establishConnectionWithRetry(nodeHostAndPort: NetworkHostAndPort, username: String, password: String): CordaRPCConnection {

    val retryInterval = 5.seconds

    do {
        val connection = try {
            logger.info("Connecting to: $nodeHostAndPort")
            val client = CordaRPCClient(
                    nodeHostAndPort,
                    object : CordaRPCClientConfiguration {
                        override val connectionMaxRetryInterval = retryInterval
                    }
            )
            val _connection = client.start(username, password)
            // Check connection is truly operational before returning it.
            val nodeInfo = _connection.proxy.nodeInfo()
            require(nodeInfo.legalIdentitiesAndCerts.isNotEmpty())
            _connection
        } catch(secEx: ActiveMQSecurityException) {
            // Happens when incorrect credentials provided - no point to retry connecting.
            throw secEx
        }
        catch(ex: RPCException) {
            // Deliberately not logging full stack trace as it will be full of internal stacktraces.
            logger.info("Exception upon establishing connection: " + ex.message)
            null
        }

        if(connection != null) {
            logger.info("Connection successfully established with: $nodeHostAndPort")
            return connection
        }
        // Could not connect this time round - pause before giving another try.
        Thread.sleep(retryInterval.toMillis())
    } while (connection == null)
}
```

After a successful connection, it is possible for the server to become unavailable. In this case, all RPC calls will throw
an exception and created observables will no longer receive observations. Below is an example of how to reconnect and
back-fill any data that might have been missed while the connection was down. This is done by using the `onError` handler
on the `Observable` returned by `CordaRPCOps`.

```Kotlin
fun performRpcReconnect(nodeHostAndPort: NetworkHostAndPort, username: String, password: String) {

    val connection = establishConnectionWithRetry(nodeHostAndPort, username, password)
    val proxy = connection.proxy

    val (stateMachineInfos, stateMachineUpdatesRaw) = proxy.stateMachinesFeed()

    val retryableStateMachineUpdatesSubscription: AtomicReference<Subscription?> = AtomicReference(null)
    val subscription: Subscription = stateMachineUpdatesRaw
            .startWith(stateMachineInfos.map { StateMachineUpdate.Added(it) })
            .subscribe({ clientCode(it) /* Client code here */ }, {
                // Terminate subscription such that nothing gets past this point to downstream Observables.
                retryableStateMachineUpdatesSubscription.get()?.unsubscribe()
                // It is good idea to close connection to properly mark the end of it. During re-connect we will create a new
                // client and a new connection, so no going back to this one. Also the server might be down, so we are
                // force closing the connection to avoid propagation of notification to the server side.
                connection.forceClose()
                // Perform re-connect.
                performRpcReconnect(nodeHostAndPort, username, password)
            })

    retryableStateMachineUpdatesSubscription.set(subscription)
}
```

In this code snippet it is possible to see that function `performRpcReconnect` creates an RPC connection and implements
the error handler upon subscription to an `Observable`. The call to this `onError` handler will be made when failover
happens then the code will terminate existing subscription, closes RPC connection and recursively calls `performRpcReconnect`
which will re-subscribe once RPC connection comes back online.

Client code if fed with instances of `StateMachineInfo` using call `clientCode(it)`. Upon re-connecting, this code receives
all the items. Some of these items might have already been delivered to client code prior to failover occurred.
It is down to client code in this case handle those duplicate items as appropriate.


## Wire protocol

The client RPC wire protocol is defined and documented in `net/corda/client/rpc/RPCApi.kt`.


## Wire security

`CordaRPCClient` has an optional constructor parameter of type `ClientRpcSslOptions`, defaulted to `null`, which allows
communication with the node using SSL. Default `null` value means no SSL used in the context of RPC.

To use this feature, the `CordaRPCClient` object provides a static factory method `createWithSsl`.

In order for this to work, the client needs to provide a truststore containing a certificate received from the node admin.
(The Node does not expect the RPC client to present a certificate, as the client already authenticates using the mechanism described above.)

For the communication to be secure, we recommend using the standard SSL best practices for key management.


## Whitelisting classes with the Corda node

CorDapps must whitelist any classes used over RPC with Corda’s serialization framework, unless they are whitelisted by
default in `DefaultWhitelist`. The whitelisting is done either via the plugin architecture or by using the
`@CordaSerializable` annotation.  See [Object serialization](serialization.md). An example is shown in [Using the client RPC API](tutorial-clientrpc-api.md).




