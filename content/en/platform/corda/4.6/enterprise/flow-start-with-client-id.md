---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps-flows
tags:
- flow
- start
- client
- id
title: Starting a flow with a client-provided unique ID
weight: 30
---


# Starting a flow with a client-provided unique ID

This feature enables you to make flow starts more reliable by relating a flow to an external client id. It addresses a common problem for developers where, once a flow has started, there are no built-in mechanisms to check whether that flow has indeed started. In addition, when an RPC client disconnects from a node, any flow futures currently used by the client would become invalidated and unable to complete.

You can use this feature to enable an RPC client to reconnect to an existing flow after a disconnect between the client and the node. This eliminates the need to write custom logic that allows you to check if a flow has already been invoked. Corda can then reliably handle this logic without custom code, so that node restarts or flow retries can be handled in a reliable manner.

You can also enable an RPC client to signal to Corda to retain the flow's result or exception, so that it could be reclaimed at any time in the future.

{{< note >}}
`COMPLETED`, `FAILED`, and `KILLED` flows can only be queried via the Multi RPC client when started by the `startFlowWithClientId` or `startFlowDynamicWithClientId` APIs described further below. For more information, see the [Interacting with a node](node/operating/clientrpc.md).
{{< /note >}}


## Steps and examples

To handle the re-hooking to an existing flow, two new APIs have been added that take a `clientId` as an argument. `clientId` informs a node to potentially re-hook to an existing flow.

When a flow is started using one of the new APIs, the following scenarios are possible:

* There is no flow started with the passed-in `clientId`: start a new flow and record the `clientId` mapping for future use.
* There is a running flow mapped to the `clientId`: re-hook to the existing flow by returning the flow's future (completes when the flow finishes).
* There is a completed flow or a failed flow, mapped to the `clientId`: return a completed future containing the flow's result, or the exception that caused it to fail.

The two APIs are available from `CordaRPCOps` (see [Using the client RPC API](../../corda-os/4.6/tutorial-clientrpc-api.md)). They both return a `FlowHandleWithClientId`, which extends `FlowHandle` but also contains the `clientId` that the flow started with.

### `startFlowDynamicWithClientId` API

If a flow with the provided `clientId` exists, then the API return its future. Otherwise, the API starts a new flow (in the same way as `startFlow`).

{{< note >}}
**Notes:**

* If the `clientId` matches a flow, then the rest of the arguments passed to `startFlowDynamicWithClientId` are ignored - these do not need to match any arguments that the existing flow had started with.
* The `startFlowDynamicWithClientId` API behaviour described above does not apply for the pre-existing start flow APIs (`startFlow` and `startTrackedFlow`) - in those cases a new start flow request always equals a new spawned flow.
* Overloaded methods named `startFlowWithClientId` have been added in `CordaRPCOps` (only available for Kotlin).
{{< /note >}}

To start a flow with a `clientId`:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
val clientId = UUID.randomUUID().toString()
val flowHandleWithClientIdA = cordaRpcOps.startFlowDynamicWithClientId(clientId, ResultFlow::class.java, flowArgA, flowArgB, flowArgC)
val flowHandleWithClientIdB = cordaRpcOps.startFlowWithClientId(clientId, ::ResultFlow, flowArgA, flowArgB, flowArgC)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
String clientId = UUID.randomUUID().toString();
FlowHandleWithClientId flowHandleWithClientId = cordaRpcOps.startFlowDynamicWithClientId(clientId, ResultFlow.class, flowArgA, flowArgB, flowArgC);
```
{{% /tab %}}

{{< /tabs >}}

### `reattachFlowWithClientId` API

This API only uses the `clientId` to re-hook to an existing flow. This enables a client to forget the arguments of a flow it previously started because only the `clientId` is needed here. If a flow is not found for a `clientId`, then it returns `null`.

To re-hook to a flow previously started with a `clientId`:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val clientId = UUID.randomUUID().toString()
cordaRpcOps.startFlowWithClientId(clientId, ::ResultFlow, flowArgA, flowArgB, flowArgC)
val flowHandleWithClientId = cordaRpcOps.reattachFlowWithClientId<Int>(clientId)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
String clientId = UUID.randomUUID().toString();
cordaRpcOps.startFlowDynamicWithClientId(clientId, ResultFlow.class, flowArgA, flowArgB, flowArgC);
FlowHandleWithClientId flowHandleWithClientId = cordaRpcOps.reattachFlowWithClientId(clientId);
```
{{% /tab %}}

{{< /tabs >}}

### `removeClientId` API

The two APIs described above allocate resources on the node's side in order to retain the returned results (or the exceptions thrown if the flow failed) for flows that started with a `clientId`, so that these flows can be re-hooked. For these resources to be freed, a clean `removeClientId` API has been added, as described below.

The `removeClientId` API frees resources held on the node's side for a flow previously started with a `clientId`. This API should be used when a client is confident that the result of a flow are no longed needed. After the API cleans up the results, the `clientId` is no longer recognised by the node. As a result, if the same `clientId` is used again, it would start a new flow instead of re-hooking to an existing one.

**Note:** Any attempt to remove the resources of a running flow will fail. Only resources of finished flows can be freed.

To free up the resources held for a `clientId` in the node and the database:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
val clientId = UUID.randomUUID().toString()
cordaRpcOps.startFlowWithClientId(clientId, ::ResultFlow, flowArgA, flowArgB, flowArgC)
val removed = cordaRpcOps.removeClientId(clientId)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
String clientId = UUID.randomUUID().toString();
cordaRpcOps.startFlowDynamicWithClientId(clientId, ResultFlow.class, flowArgA, flowArgB, flowArgC);
Boolean removed = cordaRpcOps.removeClientId(clientId);
```
{{% /tab %}}

{{< /tabs >}}


### `finishedFlowsWithClientIds` API

Sometimes the client code may lose track of flows that have started with `clientId` via `startFlowDynamicWithClientId` API described above. However, the client may still need a way to retrieve flows started with `clientId`, in order to re-attach to them (`reattachFlowWithClientId`) or remove them (`removeClientId`).

The `finishedFlowsWithClientIds` API returns back to the client a `clientId`-to-flow status mapping for all flows that were started with a `clientId` and have finished at the time of the request. The mapping pairs `clientId` to `Boolean` values for each flow - `true` if the flow `COMPLETED` or `false` if the flow `FAILED`.

To get all flows that have started with a `clientId` and have finished:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
val finishedFlowsWithClientIds = cordaRpcOps.finishedFlowsWithClientIds()
```
{{% /tab %}}

{{% tab name="java" %}}
```java
Map<String, Boolean> finishedFlowsWithClientIds = cordaRpcOps.finishedFlowsWithClientIds();
```
{{% /tab %}}

{{< /tabs >}}

The example below demonstrates how to use this feature to make client code, interacting with a Corda node, safer if the client's JVM shuts down unexpectedly. The client process can safely recover its previous state and resume from where it left off.

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
class FlowExecutor(private val proxy: CordaRPCOps, private val dbClientStorage: DBClientStorage) {

    /**
     * Stores in persistent store the [clientId] and starts the flow with their arguments.
     * This service method could be called from multiple threads concurrently, adding a [clientId] record in the database, start the flow on Corda node,
     * and wait on the flows result future.
     */
    fun startFlowWithClientId(clientId: String, flowArgA: String, flowArgB: Int, flowArgC: Boolean) {
        dbClientStorage.addClientId(clientId)
        val flowHandle = proxy.startFlowWithClientId(clientId, ::ResultFlow, flowArgA, flowArgB, flowArgC)
        flowHandle.returnValue.toCompletableFuture().thenApply {
            doOnResult(it, clientId)
        }
    }

    /**
     * On client start up, checks if there are started flows bound with clientIds and reattaches to them.
     * This could happen if flows were started on node side, from client threads and client's jvm was shut down unexpectedly,
     * before processing their result, and remove the client id from the client's persistent store.
     */
    fun onStart() {
        val pendingClientIds = dbClientStorage.getClientIds()
        if (pendingClientIds.isNotEmpty()) {
            reattachToFlows(pendingClientIds)
        }
    }

    /**
     * Re-attach to flows using the same [clientIds] previously used to start at [startFlowsWithClientId]. Please note that the flow arguments
     * are not needed for [CordaRPCOps.reattachFlowWithClientId] to re-attach to the flow and return its flow handle.
     * On using the flow's result, free the flow's resources on the node's side, using the [clientId].
     * Please note that we should be aware of the return types of the flows we are attaching to be matching [CordaRPCOps.reattachFlowWithClientId] parameterized type.
     */
    private fun reattachToFlows(clientIds: Set<String>) {
        for (clientId in clientIds) {
            val flowHandle = proxy.reattachFlowWithClientId<Int>(clientId)
            flowHandle!!.returnValue.toCompletableFuture().thenApply {
                doOnResult(it, clientId)
            }
        }
    }

    private fun doOnResult(flowResult: Int, clientId: String) {
        useFlowResult(flowResult)
        // We should first update the client id on the client's persistent storage as completed, and then remove it from the Corda node,
        // because if done the other way around, we could risk having the flow removed from the Corda node, and then if the client JVM goes down,
        // we could end up with the client id removed from the node but not marked as completed in the persistent storage.
        // Therefore on client restart it would then start a new flow within Corda since that client id would be no longer known to the Corda node.
        dbClientStorage.removeClientId(clientId)
        proxy.removeClientId(clientId)
    }
}
```
{{% /tab %}}

{{< /tabs >}}
