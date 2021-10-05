---
title: "Implementing durable streams on the server"
date: '2021-09-16'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing-durable-streams
    identifier: corda-5-dev-preview-1-nodes-developing-durable-streams-server
    weight: 3600
section_menu: corda-5-dev-preview
description: >
  How to implement durable streams on the server.
---

HTTP-RPC is a secure HTTP API for you RPC interfaces which allows requests and responses to pass between an HTTP client
and HTTP server.

When [defining durable stream methods](../../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/define-methods/methods.md), you must include the special construct `DurableStreamContext`.

`DurableStreamContext` captures *technical* (non-business logic) parameters for HTTP-RPC calls, such as:
* From which position elements should be served.
* How many elements the client should receive.
* How long the call may wait (block) on the server side for elements to become available.

You must use these parameters when creating the HTTP-RPC server side implementation.

For this client side interface:
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

The server side implementation would be:

```kotlin
class NumberSequencesRPCOpsImpl : NumberSequencesRPCOps {

    override fun retrieve(type: NumberTypeEnum): DurableCursorBuilder<String> {
        return DurableStreamHelper.withDurableStreamContext {
            val pad = when (type) {
                NumberTypeEnum.EVEN -> 2
                NumberTypeEnum.ODD -> 1
            }

            val longRange: LongRange = (currentPosition + 1)..(currentPosition + maxCount)
            val positionedValues = longRange.map { pos -> pos to (pad + pos * 2).toHumanReadableNumber() }
            DurableStreamHelper.outcome(Long.MAX_VALUE, false, positionedValues)
        }
    }
}
```

In the server side implementation:
* `DurableStreamHelper` implements a special DSL syntax to take care of `DurableStreamContext`, such that server side logic can be implemented assuming that `DurableStreamContext` is just available.
* `DurableStreamHelper.outcome()` returns a correctly typed streaming result from a list of pair values.

To learn more, refer to `DurableStreamContext` and `DurableStreamHelper` in the [KDocs](https://www.kdocs.co.uk/home).
