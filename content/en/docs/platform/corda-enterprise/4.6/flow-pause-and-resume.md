---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps-flows
tags:
- flow
- pause
- resume
title: Pause and resume flows
weight: 20
---

# Pause and resume flows

This state machine feature enables you to pause `RUNNING` flows and flows `UNDER OBSERVATION` (by the [Flow Hospital](node/node-flow-hospital.md)) without needing to restart the node.

It also allows you to resume (retry) a `PAUSED` flow or a flow `UNDER OBSERVATION`.

This gives you more control of the flows running on a node - you can:

* `RETRY` a `HOSPITALIZED` flow.
* `PAUSE` an individual problematic flow, causing the flow to stop until you retry that flow.
* Stops any other running flows causing downtime.

{{< note >}}
`PAUSED` flows are automatically retried on node startup.
{{< /note >}}

## How to pause and resume flows

You can pause and retry a flow via both the nodes shell and an extensions RPC API.

### Pausing and retrying flows from the shell

The following examples show the different ways to use the `flow pause` and `flow retry` commands.

To pause a flow with a universally unique identifier `F420002B-BA1A-46D1-8C9F-A71AC659924E`:

```bash
flow pause F420002B-BA1A-46D1-8C9F-A71AC659924E
```

To pause all flows which are `RUNNING` or `HOSPITALIZED`:

```bash
flow pauseAll
```

To pause all `HOSPITALIZED` flows:

```bash
flow pauseAllHospitalized
```

To retry a flow with a universally unique identifier `F420002B-BA1A-46D1-8C9F-A71AC659924E`:

```bash
flow retry F420002B-BA1A-46D1-8C9F-A71AC659924E
```

To retry all paused flows:

```bash
flow retryAllPaused
```

To retry all hospitalized flows that are paused:

```bash
flow retryAllPausedHospitalized
```

In all cases, the shell prints a message stating if the operation succeeded or not.

### Pausing and retrying flows from RPC

To pause and retry flows from an RPC Client using the extensions RPC Interface (`FlowRPC`), use the Multi RPC Client - `MultiRPCClient`.

{{< note >}}
For more information about `MultiRPCClient`, see [Interacting with a node](node/operating/clientrpc.md#building-the-multi-rpc-client).
{{< /note >}}

First instantiate a `MultiRPCClient` for `FlowRPC` (this differs from the standard non-extensions RPC interface):

```kotlin
val username = "testuser"
val password = "password"
val rpcHostAndPort = NetworkHostAndPort("localhost", 10006)
val flowClient = MultiRPCClient(rpcHostAndPort, FlowRPCOps::class.java, username, password).start().getOrThrow()
```

To pause a flow, call `pauseFlow`:

```kotlin
val status = flowClient.proxy.pauseFlow(flowHandle.id)
```

To pause all flows, call `pauseAllFlows`:

```kotlin
val status = flowClient.proxy.pauseAllFlows()
```

To pause all hospitalised flows, call `pauseAllHospitalizedFlows`:

```kotlin
val status = flowClient.proxy.pauseAllHospitalizedFlows()
```

To retry a flow, call `retryFlow`:

```kotlin
val status = flowClient.proxy.retryFlow(flowHandle.id)
```

To retry all paused flows call `retryAllPausedFlows`:

```kotlin
val status = flowClient.proxy.retryAllPausedFlows()
```

To retry all hospitalized flows that are paused call `retryAllPausedHospitalized`:

```kotlin
val status = flowClient.proxy.retryAllPausedHospitalized()
```

All these methods will return `true` if the operation was successful, or `false` otherwise.

To prevent server-side resource leakage, use `flowClient.close()` to close `flowClient` when finished.

### Starting the node and pausing all flows

All flows can be paused when the node starts up - you can enable this in one of the following ways:

* Use the command-line option `--pause-all-flows`.
* Add the `smmStartMode="Safe"` option to the [node configuration file](node/setup/corda-configuration-file.md).

These flows can then be individually retried via RPC or the node shell.

This option also enables flow draining mode, which stops flows from being started via RPC, the shell, and counterparties.

You can turn flow draining mode off via RPC using the `setFlowsDrainingModeEnabled` RPC method.

How to disable flow draining via the shell:

```shell script
run setFlowsDrainingModeEnabled enabled: false
```

This feature can be useful if the node causes the machine to run out of memory (for example by trying to run too many flows). If this happens then users can restart the node and manually retry a few flows at a time.

Once the problem is resolved, flow draining mode can be disabled, allowing the node to continue running as normal.

Starting a node with the `--pause-all-flows` command-line option automatically enables flow draining mode but does not modify the node's configuration file.

{{< note >}}
Removing the `--pause-all-flows` command-line option or `smmStartMode="Safe"` from the node's configuration file will not disable flow draining. Flow draining can only be disabled manually via RPC or the shell.
{{< /note >}}

## How it works

Pausing a flow causes the flow to stop running (this might be after the next suspension). The flow can then be retried - this reloads the flow from the last checkpoint (in the same way as at node startup).

When a flow is `PAUSED`, a `PAUSE` event is added to the end of the flows event queue.

* If the flow is currently suspended, then once the flow processes all the events up to and including the `PAUSE` event, the fiber running the flow will abort.
* If the flow is not suspended, the flow will run until the next suspension point before the fiber running the flow aborts.

In both cases the shell and `RPC` commands return once the `PAUSE` event has been added to the flows event queue (this might be before the fiber aborts).

{{< note >}}
From an architectual perspective, the flows event queue interacts in the correct way with `killFlow` in that killing a flow takes priority over `PAUSING` a flow. This comes at the expense that it might take some time for `RUNNING` flows to actually pause.
{{< /note >}}

Retrying a `UNDER OBSERVATION` or `PAUSED` flow causes the state machine to restore the last checkpoint and run from that point on a new fiber. If a session has been initiated between a `PAUSED` flow and a counterparty flow, then messages sent to the `PAUSED` flow will be stored and processed if the flow is retried.

{{< note >}}
The `FlowState` of `PAUSED` flows' is not held in memory in order to reduce memory usage. Instead, it is reloaded from the database if the flow is retried.
{{< /note >}}

### Touch points with other Corda Enterprise features

If a flow that is currently `PAUSED` is killed, then that flow will still be killed in the normal way (including propagating exceptions to counterparties).

`PAUSED` flows cannot have a status of `HOSPITALIZED` as they share the same database column. You can make the distinction between flows with these statuses by checking if there is an exception in `node_flow_exceptions`. If there is one, in the normal bounds of a flow's lifecycle, then that flow must have previously been `HOSPITALIZED` before being `PAUSED`. This information is used to set an in-memory flag so that this information is available when attempting to un-pause a flow.
