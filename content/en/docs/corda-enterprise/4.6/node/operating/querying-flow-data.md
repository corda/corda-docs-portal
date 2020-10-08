---
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- shell
- node
- query
- flow
title: Querying flow data
weight: 6
---

# Querying flow data

As a node operator, you can query a node to retrieve flow checkpoint data which can help you in managing your node.

A checkpoint is a record of flow data taken at key points during a flow's operation, typically whenever the flow is suspended and waiting for a response or message. Querying this checkpoint data enables you to inspect the status of any flows being executed on your node and can assist you in troubleshooting issues that may arise in relation to flows.

With Corda Enterprise, you can query flow data in the following ways:

* You can [query flow data via RPC](#querying-flow-data-via-RPC)
* You can [query flow data via the node shell](#querying-flow-data-via-the-node-shell)

## Querying flow data via RPC

Corda Enterprise exposes a number of custom, remote RPC interfaces, which enable you to interact with your node. For a list of all the remote interfaces that are available in Corda Enterprise, see [Building a Multi RPC Client](clientrpc.md).

The `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps` interface is an RPC extension which enables external applications to query and view the status of the flows which are currently being monitored by the Flow Hospital.

To use the `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps` interface to query flow status via RPC, you need to complete the following steps:

1. Build a Multi RPC client - see [Building a Multi RPC Client](#-building-a-multi-rpc-client).
2. Specify the search criteria for the query - see [Specifying the query criteria](#specifying-the-query-criteria).

### Building a Multi RPC Client

To be able to use the `net.corda.client.rpc.proxy.NodeFlowStatusRpcOps` interface to interact with your node and query flow status via RPC, you must build a Multi RPC Client that uses the `NodeFlowStatusRpcOps::class.java` interface class for communication. The following code snippet provides an example of how to do this:

```kotlin
val rpcAddress = NetworkHostAndPort("nodeAddress", 1000)
val client = MultiRPCClient(rpcAddress, NodeFlowStatusRpcOps::class.java, rpcUser.username, rpcUser.password)
val connFuture = client.start()
val conn = connFuture.get()
val flowStatusRPCOPs = conn.proxy
```
To view the full code sample, see [NodeFlowStatusRpcOps.kt](../../resources/extensions-rpc/NodeFlowStatusRpcOps.kt).

For details of how to build a Multi RPC Client, see [Building a Multi RPC Client](clientrpc.md). See also [MultiRPCClient](https://api.corda.net/api/corda-enterprise/4.6/html/api/javadoc/net/corda/client/rpc/ext/MultiRPCClient.html) in the API documentation.

### Specifying the query criteria

To return flow checkpoint data via RPC, you must specify your search criteria.

Including one or more search criteria will enable you to identify flows that did not complete and where:

* The flow is or is not compatible with the current Corda runtime environment.
* The flow relates to a particular CorDapp.
* The flow class name includes a particular string fragment.
* The flow was executed within a specific time window.
* The flow is in a particular state.
* The flow did not proceed beyond a specific progress step.
* The flow remained stuck at a checkpoint for a particular length of time.

The available search parameters and their required formats are outlined in the table below.


{{< table >}}

| Parameter name | Description | Format |
|---------|----------|---------|---------|
| `flowClass` | The name of the class that implements the flow. You do not need to enter the full name - providing a fragment of the class name is enough to identify the class. The * regex operator is applied to the start and end of the fragment. | String |  
| `flowState` | The state of the flow at its latest checkpoint. The state is one of the following values: `RUNNABLE`, `FAILED`, `COMPLETED`, `HOSPITALIZED`, `KILLED`, `PAUSED`. | Enum |
| `progressStep` | If the flow implements progress tracking, specifies the latest step that was encountered before checkpointing. A progressStep is a user-defined value which is defined by the CorDapp developer - you can specify the name of any progressStep defined in your CorDapp. The * regex operator is applied to the start and end of the fragment. | String |  
| `cordapp` | The name of the CorDapp that contains the flow. You do not need to enter the full name - providing a fragment of the name is enough to identify the CorDapp. The * regex operator is applied to the start and end of the fragment. | String |
| `compatibleWithCurrentCordaRuntime` | Indicates whether the suspended flow is compatible with and can be loaded on the current Corda runtime environment. | Boolean String |
| `suspensionDuration` | The minimum duration for which a flow must have remained suspended (that is, "stuck") at a checkpoint. | java.time.Duration |  
| `flowStart` | Uses the `net.corda.core.contracts.TimeWindow` class to define an open or closed time window for when the flow was first started.  The start time of the time-window in which the flow was started. A start-open window will return all flows started before the Unix 0 Instant (that is, the time 00:00 on January 1, 1970). An end-open window will return all flows started after a given time and before the current Instant. All times specified are inclusive. | net.corda.core.contracts.TimeWindow |  
{{< /table >}}

{{< warning >}}
`COMPLETED`, `FAILED` and `KILLED` flows can only be queried when started by the `startFlowWithClientId` or `startFlowDynamicWithClientId` APIs.
{{< /warning >}}

The code example below shows how you can define a query that will return all flows that have not completed as expected and which meet the following criteria:

* The flow belongs to the `IssueToken` flow class.
* The flow's state is `RUNNABLE`.
* The flow is at the progress step called `SIGNING`.
* The flow belongs to the `tokens-workflows` CorDapp.
* The flow is compatible with and can be loaded on the current Corda runtime environment.
* The flow has remained suspended for at least 10 minutes.
* The flow started in the last 30 minutes.

```kotlin
val rpcAddress = NetworkHostAndPort("nodeAddress", 1000)
val client = MultiRPCClient(rpcAddress, NodeFlowStatusRpcOps::class.java, rpcUser.username, rpcUser.password)
val connFuture = client.start()
val conn = connFuture.get()
val flowStatusRPCOPs = conn.proxy

val matchingFlows: List<String>  = flowStatusRPCOPs.getFlowsMatching(FlowStatusQuery(
    flowClass = "IssueToken",
    flowState = FlowState.RUNNABLE,
    progressStep = "SIGNING",
    cordapp = "tokens-workflows",
    compatibleWithCurrentCordaRuntime = true,
    suspensionDuration = Duration.ofMinutes(10),
    flowStart = TimeWindow.between(Instant.now().minus(30, ChronoUnit.MINUTES), Instant.now())
    )
)
matchingFlows.forEach { flowId ->
    println(flowStatusRPCOPs.getFlowStatus(flowId))
}

```
[NodeFlowStatusRpcOps.kt](../../resources/extensions-rpc/NodeFlowStatusRpcOps.kt)

When this query is executed, a list of the flow IDs for all flows that did not complete and which meet the search criteria is returned. For each flow ID, the status of the specified flow is also returned.


## Querying flow data via the node shell

To query the node for flow data via the [Node Shell](shell.md), you must use the `flowStatus` query command.

You can use the `flowStatus` query command, in combination with one or more parameters, to retrieve various types of flow data from the node's checkpoints.


### View all flows that have not completed

You can use the `flowStatus` command to return a list of all flows on a node that have not completed. To do this, run the following query:

```
flowStatus queryFlows
```

A list consisting of the flow IDs of all flows on the node that have not completed is returned.

The flow ID belonging to each flow is listed on a separate line, as shown in the example below:

```
5da55b82-332f-4ecd-a20c-3b02be040bb7
4dc21e46-142g-7rbt-b56i-2k41mr701lb2
```

### View flows that meet specific search criteria

You can view a subset of all flows that did not complete by including specific search criteria in your query. You do this by combining the `flowStatus queryFlows` query command with one of more of the parameters shown in the table below.

Including one or more search criteria will enable you to identify flows that did not complete and where:

* The flow is or is not compatible with the current Corda runtime environment.
* The flow relates to a particular CorDapp.
* The flow includes a particular flow class.
* The flow was executed within a specific time window.
* The flow is in a particular state.
* The flow did not proceed beyond a specific progress step.
* The flow remained stuck at a checkpoint for a particular length of time.

The available search parameters and their required formats are outlined in the table below.

{{< table >}}

| Parameter name | Description | Format |
|---------|----------|---------|---------|
| `compatibleWithCurrentCordaRuntime` | Indicates whether the suspended flow is compatible with and can be loaded on the current Corda runtime environment. | Boolean String |
| `cordapp` | The name of the CorDapp that contains the flow. You do not need to enter the full name - providing a fragment of the name is enough to identify the CorDapp. | String |  
| `flowClass` | The name of the class that implements the flow. You do not need to enter the full name - providing a fragment of the class name is enough to identify the class. | String |  
| `flowStartFrom` | The start time of the time-window in which the flow was started. If you do not specify a start time value, the start time is taken to be a UNIX 0 timestamp (that is, the time 00:00 on January 1, 1970). If you specify a value for `flowStartFrom` but do not specify a value for `flowStartUntil`, the query will return a list of all flows that did not complete up until the time that the query was run. | String in ISO8601 DateTime format*. |  
| `flowStartUntil` | The end time of the time-window in which the flow was started. If you specify a value for `flowStartUntil` but do not specify a value for `flowStartFrom`, the query will return a list of all flows that did not complete since the node started up. | String in ISO8601 DateTime format*. |  
| `flowState` | The state of the flow at its latest checkpoint. The state is one of the following values: `RUNNABLE`, `FAILED`, `COMPLETED`, `HOSPITALIZED`, `KILLED`, `PAUSED`. | String |  
| `progressStep` | If the flow implements progress tracking, specifies the latest step that was encountered before checkpointing. A progressStep is a user-defined value which is defined by the CorDapp developer - you can specify the name of any progressStep defined in your CorDapp. | String |  
| `suspensionDuration` | The minimum duration for which a flow must have remained suspended (that is, "stuck") at a checkpoint. This is entered in the format `"<value>, <unit>"` where `<value>` is a numerical value and `<unit>` is the unit of time, specified as `SECONDS`, `MINUTES`, `HOURS` or `DAYS`). | String |  
{{< /table >}}

{{< warning >}}
`COMPLETED`, `FAILED` and `KILLED` flows can only be queried when started by the `startFlowWithClientId` or `startFlowDynamicWithClientId` APIs.
{{< /warning >}}

\*  See [Sample query to view all suspended flows within a particular time-window](#sample-query-to-view-all-suspended-flows-within-a-particular-time-window).

#### Constructing your query

To return specific information about a flow, a query must contain the following elements:

* The query command: `flowStatus queryFlows`.
* One or more parameters from the above table. These parameters define the data that is returned from each checkpoint.

If you run the query without including any specific search criteria, a list consisting only of the flow IDs of all flows on the node that have not completed is returned, as outlined under [View all flows that have not completed](#view-all-flows-that-have-not-completed).

#### Sample query to view all suspended flows in a particular state

To return a list of all flows that have not completed and are in a particular state (in this example, the `HOSPITALIZED` state), run the following query:

```
flowStatus queryFlows flowState: HOSPITALIZED
```

#### Sample query to view all suspended flows in a particular class

To return a list of all flows that have not completed and which relate to a particular flow class (in this example, the `HospitalizerFlow` class), run the following query:

```
flowStatus queryFlows flowClass: HospitalizerFlow
```

#### Sample query to view all suspended flows within a particular time-window

When specifying time-windows, all dates and times must be specified in accordance with the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html/) as follows:

```
yyyy-MM-ddTHH:mm:ss
```

For example, to specify a `flowStartFrom` time of 08:45:56 on July 21, 2020, you must enter the time in the following format:

```
2020-07-21T08:45:56
```

You can create a query for an open or closed time-window.

To return a list of all flows that did not complete within a closed time-window, specify both a start time and end time for the time-window as follows:

 ```
 flowStatus queryFlows flowStartFrom: 2020-05-16T09:30:00 flowStartUntil: 2020-05-17T09:30:00
 ```

The following query is an example of an open time-window, where only the start-time of the time-window is specified:

```
flowStatus queryFlows flowStartFrom: 2020-05-16T09:30:00
```

If running a query for an open-ended time-window, note the following:

* If you specify a value for `flowStartFrom` but do not specify a value for `flowStartUntil`, the query will return a list of all flows that did not complete up until the time that the query was run.

* If you specify a value for `flowStartUntil` but do not specify a value for `flowStartFrom`, the query will return a list of all flows that did not complete since the node started up.

#### Sample query to view flows suspended for a particular duration

To return a list of all flows that have been suspended (that is, "stuck") for a certain minimum period of time, specify a value for `suspensionDuration`. Specifying a value for `suspensionDuration` filters out flows that have not been suspended for _at least_ this duration.

This option is particularly useful if, for example, you want to identify all flows that have been stuck for a certain period of time or if you want to exclude flows that have been executed recently from the results returned. For example, if you know that a flow takes a certain amount of time to execute, you may wish to check for flows that have not completed that have been stuck for a period of time that is longer than the normal execution period.

To specify the `suspensionDuration`, enter the value in the format `"<value>, <unit>"` where `<value>` is a numerical value and `<unit>` is the unit of time, specified as `SECONDS`, `MINUTES`, `HOURS` or `DAYS`.

To return a list of all flows that have not completed and which have been stuck a certain minimum period of time (in this example, at least 2 hours), run the following query:

```
flowStatus queryFlows suspensionDuration: "2, HOURS"
```

#### Sample compound queries

You can combine multiple search criteria in a single query. For example, you could combine the two sample queries described in [Sample query to view all suspended flows in a particular state](#sample-query-to-view-all-suspended-flows-in-a-particular-state) and [Sample query to view all suspended flows in a particular class](#sample-query-to-view-all-suspended-flows-in-a-particular-class) into a single query as follows:

`flowStatus queryFlows flowState: HOSPITALIZED flowClass: HospitalizerFlow`

You can also construct more complex queries, such as the following:

`flowStatus queryFlows compatibleWithCurrentCordaRuntime: true cordapp: custom-cordapp flowClass: Hospitalizer suspensionDuration: "5, MINUTES"`

In this example, flow data will be returned for flows that have not completed and which also meet all of the following conditions:
* The flow is compatible with the current Corda runtime environment.
* The flow exists in the CorDapp called `custom-cordapp`.
* The flow belongs to the `Hospitalizer` class.
* The flow has been suspended for five minutes or more.


### View summary information for a suspended flow

If you want to obtain a summary of checkpoint data relating to one or more suspended flows, you can use the `flowStatus` query command, in combination with the `queryById` field.

For example, to return summary data for the flow which has the flow ID `5da55b82-332f-4ecd-a20c-3b02be040bb7`, you would structure your query as follows:

 ```
 flowStatus queryById 5da55b82-332f-4ecd-a20c-3b02be040bb7
 ```

 Running this query returns the following checkpoint data for the flow:

```
flowStatus queryById 5da55b82-332f-4ecd-a20c-3b02be040bb7
---
- flowId: "5da55b82-332f-4ecd-a20c-3b02be040bb7"
  flowClass: "net.corda.failingflows.workflows.HospitalizerFlow"
  flowState: "HOSPITALIZED"
  cordappContext:
    cordappName: "custom-cordapp_1_7_6732caa5-99b8-4b95-a935-bde44bc65172"
    cordaVersion: 7
  compatibleWithCurrentCordaRuntime: true
  progressStep: null
  invocationContext:
    invocationSource: "RPC"
    userName: null
    initiatingParty: null
    userSuppliedInformation: null
  suspensionMetadata: null
  flowStart: 1595323327.416000000
  lastCheckpoint: 1595323327.481000000
```

You can return summary data for one or more flows in a single query.

To return data for more than one flow, specify the flow IDs of the relevant flows in the following format:

```
flowStatus queryById flowId1 flowId2
```

 For example, let's say you want to return summary data for following two flows:

 * Flow ID of the first flow: `5da55b82-332f-4ecd-a20c-3b02be040bb7`
 * Flow ID of the second flow: `4dc21e46-142g-7rbt-b56i-2k41mr701lb2`

 To do this, you would structure your query as follows, listing each flow ID, separated by a space:

```
flowStatus queryById 5da55b82-332f-4ecd-a20c-3b02be040bb7 4dc21e46-142g-7rbt-b56i-2k41mr701lb2
```

### Get help with the `flowStatus` command

You can view a list of all arguments relating to the `flowStatus` command by entering the following command:

```
flowStatus --help
```

A list of all possible options is returned.
