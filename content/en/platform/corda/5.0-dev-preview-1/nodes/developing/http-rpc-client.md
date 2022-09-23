---
title: "Using the Java/Kotlin HTTP-RPC client"
date: '2021-09-14'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing
    identifier: corda-5-dev-preview-1-nodes-developing-http-rpc-client
    weight: 2600
section_menu: corda-5-dev-preview
description: >
  How to use the Java/Kotlin native HTTP-RPC client.
---

In the Corda 5 Developer Preview, you can send requests and retrieve their responses via the
HTTP API in two ways:
* [Generate client code from the OpenAPI Specification](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/generate-code/generate-code.md)
* Use the native HTTP-RPC client, `HttpRpcClient`, in your Java/Kotlin code.

`HttpRpcClient` simplifies Java/Kotlin calls to the HTTP-RPC service.

{{< note >}}

`HttpRpcClient` uses the same OpenAPI as a generated client. It is not privileged and does not
have any special provisions.

{{< /note >}}

## Implement `HttpRpcClient`

`HttpRpcClient` translates a standard interface call on the HTTP-RPC client side JVM into an HTTP remote communication.
It then waits for the server to respond. The interface call is completed when the server responds with a result.

Here is an example of an `RPCOps` interface from the HTTP client side:

```kotlin
@HttpRpcResource(
        name = "HealthCheckAPI",
        description = "Health Check",
        path = "health/"
)
interface HealthCheckAPI : RPCOps {
    @HttpRpcPOST(
            path = "plusone/{number}",
            title = "AddOne",
            description = "Add One"
    )
    fun plus(
            @HttpRpcPathParameter number: Long
    ): Long
}
```

The corresponding remote interface `HttpRpcClient` in Java:
1. Creates the `HttpRpcClient` and binds it to `HealthCheckAPI`.
2. When the client starts, produces `HttpRpcConnection` and uses this to obtain the `proxy`. (`proxy` is an instance of a [dynamic proxy](https://docs.oracle.com/javase/8/docs/technotes/guides/reflection/proxy.html) which translates
   interface calls into remote calls to the HTTP-RPC server side.)
3. Makes the remote HTTP-RPC call.

```
HttpRpcClient<HealthCheckAPI> client = new HttpRpcClient<>(...);

try (client) {
    HttpRpcConnection<HealthCheckAPI> connection = client.start();
    HealthCheckAPI proxy = connection.getProxy();
    assertEquals(3, proxy.plus(2L));
}
```

{{< note >}}

You need to make sure that when using `HttpRpcClient`, these are available on the class path
on the HTTP-RPC client side:
* Annotated interface class (in this example, `HealthCheckAPI`).
* Classes for parameters.
* Return results for the methods.
These classes must match those used on the server side implementation of the `RPCOps` interface.

{{< /note >}}

The code snippet in the example uses [try-with-resource](https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html)
Java construct. This means `HttpRpcClient` is closed at the end of the `try` scope. Because `HttpRpcClient` is
`AutoCloseable`, all the necessary tidy-up (including the release of all previously acquired resources) is completed.

## Implement `HttpRpcConnectionListener`

`HttpRpcClient` contains a facility which allows listeners to be added so that they are notified when the connection goes
up or down. It is perfectly legitimate to add a listener even before `HttpRpcClient` is started. Then when the `start` method
is called and the HTTP connection is successfully established, the attached listener is notified about such an event.

Connection listeners need to implement the `HttpRpcConnectionListener` interface.

For more information, refer to `HttpRpcClient` and `HttpRpcConnectionListener` in the
[KDocs](https://www.kdocs.co.uk/home).
