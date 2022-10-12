---
title: "Using HttpRpcClient in polling requests"
date: '2021-09-16'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing-durable-streams
    identifier: corda-5-dev-preview-1-nodes-developing-durable-streams-java
    weight: 3400
section_menu: corda-5-dev-preview
description: >
  How to use the native HTTP-RPC client, `HttpRpcClient`, in polling requests.
expiryDate: '2022-09-28'  
---

In the Corda 5 Developer Preview, you can use the [native HTTP-RPC client](../../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/http-rpc-client.md), `HttpRpcClient`, in your
Java/Kotlin code.

`HttpRpcClient` simplifies Java/Kotlin calls to the HTTP-RPC service.

{{< note >}}

`HttpRpcClient` uses the same OpenAPI as a generated client. It is not privileged and does not
have any special provisions.

OpenAPI and JSON payload still remain the *primary* protocol of HTTP-RPC exchange.

{{< /note >}}

Here is an `RPCOps` interface definition for a simple durable stream operation:

```kotlin
@CordaSerializable
enum class NumberTypeEnum {
    EVEN, ODD
}

@HttpRpcResource("...")
interface NumberSequencesRPCOps : RPCOps {
    @HttpRpcPOST
    fun retrieve(type: NumberTypeEnum): DurableCursorBuilder<String>
}
```

You can write the same definition using `HttpRpcClient` as if normal interface methods (such as `poll`) are invoked:

```kotlin
        val client = HttpRpcClient(
                baseAddress = "http://localhost:$port/api/v1/",
                NumberSequencesRPCOps::class.java,
                HttpRpcClientConfig()
                        .username(userAlice.username)
                        .password(requireNotNull(userAlice.password))
        )

        client.use {
            val connection = client.start()
            with(connection.proxy) {
                val cursor = this.retrieve(NumberTypeEnum.EVEN).build()
                with(cursor.poll(100, 100.seconds)) {
                    assertEquals(100, values.size)
                    assert(values.first() == "Two")
                    assert(values.last() == "Two hundreds")
                    assertFalse(this.isLastResult)
                    cursor.commit(this)
                }

                with(cursor.poll(200, 100.seconds)) {
                    assertEquals(200, values.size)
                    assert(values.first() == "Two hundreds and two")
                    assert(values.last() == "Six hundreds")
                    assertFalse(this.isLastResult)
                    // Committed not the last
                    cursor.commit(positionedValues[2].position) // 206
                }
            }
        }
```

`HttpRpcClient` uses [dynamic proxies](https://docs.oracle.com/javase/8/docs/technotes/guides/reflection/proxy.html)
to translate interface calls into remote calls to the HTTP-RPC server side.

## `PositionManager`

The HTTP-RPC client is responsible for [tracking positions/sequence](../../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/durable-streams-homepage.html#tracking-positions).

If you're using Java, you can track positions using the interface `PositionManager`:

```kotlin
interface PositionManager : Supplier<Long>, Consumer<Long>
```

`PositionManager` can `get` and `set` position value as a `Long` value.

You can have a custom implementation of the `PositionManager` interface. `DurableCursorBuilder` can use this custom
implementation which you can assign to a build before the first durable query is made using the `poll`
method. After the `poll` method has been called, changes can't be made to the `PositionManager`.

By default `PositionManager` is initialized with `InMemoryPositionManager` which retains position value inside `AtomicLong`.
