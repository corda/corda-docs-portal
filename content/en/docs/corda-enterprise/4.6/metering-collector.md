---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- metering
- collector
title: Metering Collection Tool
weight: 130
---


# Metering Collection Tool

The Metering Collection Tool is used to collect metering data from a Corda Enterprise node.

On this page you can learn how the node records metering data and how to run the collection tool in order to collect that data.

{{< note >}}
Corda Enterprise nodes record metering data regardless of whether the Metering Collection Tool is installed on the node.
{{< /note >}}

## Overview

The Metering Collection Tool provides a mechanism for collecting metering data from both normal nodes and notaries running Corda Enterprise.

The tool uses the following flows:

* `MeteringCollectionFlow` - use this flow to collect metering data from a node by using the node's shell. You must specify, as an argument, the time window over which the flow will be collecting metering data. You can also specify a set of CorDapps to filter the data by. The flow output represents both the total count of metering events that match the filter within the time window, and a breakdown of these events based on the commands involved and the signing entities. You can invoke this flow from the shell, however its usage via RPC has been deprecated - you can use the `NodeMeteringCollectionFlow` flow instead. This flow gathers data from the "current" node - the node where it was initiated.
* `NodeMeteringCollectionFlow` - use this flow to collect metering data from a node by connecting to it via RPC. You must specify, as an argument, the time window over which the flow will be collecting metering data. You can also specify a set of CorDapps to filter the data by. The flow output represents both the total count of metering events that match the filter within the time window, and a breakdown of these events based on the commands involved and the signing entities. This flow gathers data from the "current" node - the node where it was initiated.
* `FilteredMeteringCollectionFlow` - use this flow to collect metering data from another node on the network by connecting to it via RPC. The `FilteredMeteringCollectionFlow` flow is identical to the `NodeMeteringCollectionFlow` flow except that `FilteredMeteringCollectionFlow` collects data from another node on the network - a node that is different from the one where the flow was initiated. For that reason, it requires an additional argument where you must specify the party running the node where metering data is to be collected from.
* `AggregatedMeteringCollectionFlow` - use this flow to collect aggregated metering data from other nodes on the network - nodes that are different from the one where it was initiated. You must specify, as arguments, the time window over which the flow will be collecting metering data as well as the party running the node where metering data will be collected from. The flow output represents the total count of signing events that happened on the monitored nodes during the specified time window.
* `MultiFilteredCollectionFlow` - use this flow to collect metering data from multiple nodes on the network by connecting to them via RPC. The `MultiFilteredCollectionFlow` flow is identical to the `FilteredMeteringCollectionFlow` flow except that `MultiFilteredCollectionFlow` collects data from multiple nodes on the network sequentially in a single flow, and returns the result as a `JSON` string. You can use this flow from the node shell only. You can use the dedicated method `FilteredMeteringCollectionFlow#multiCollect` to collect metering data from multiple nodes in parallel by using an RPC client to connect to the initiating flow - the collection process then uses the flow framework to collect metering data from the other nodes on the network.
* `MultiAggregatedCollectionFlow` - use this flow to collect aggregated metering data from multiple nodes on the network sequentially in a single flow. The `MultiAggregatedCollectionFlow` flow is identical to the `AggregatedMeteringCollectionFlow` flow except that `MultiAggregatedCollectionFlow` collects data from multiple nodes on the network sequentially in a single flow, and returns the result as a `JSON` string. You can use this flow from the node shell only. If you want to use an RPC client to connect to the nodes, use the dedicated method `AggregatedMeteringCollectionFlow#multiCollect` to collect metering data from multiple nodes in parallel via RPC.
* `NotaryCollectionFlow` - use this flow to collect metering data from notaries. You must specify, as an argument, the time window over which the flow will be collecting metering data. The flow output represents the total count of notarisation requests during the specified time window, along with a breakdown of these requests filtered by the parties that made them.
* `RetrieveCordappDataFlow`- use this utility flow to extract CorDapp hashes and signing keys for a given CorDapp name, in the correct format, for use in the `NodeMeteringCollectionFlow` flow filter (see above). This flow provides information about the versions and vendors of the returned CorDapps so that the correct CorDapp data can be selected.

{{< warning >}}
The `NotaryCollectionFlow` flow does not allow the collection of metering data for notaries configured in high-availability mode.
{{< /warning >}}

{{< note >}}
The difference between `AggregatedMeteringCollectionFlow` and `FilteredMeteringCollectionFlow` is that the output of the `FilteredMeteringCollectionFlow` flow provides a detailed breakdown of the events by identity and command, and `AggregatedMeteringCollectionFlow` only reports the total number of signing events in the metering data collection.
{{< /note >}}

## Installation

The Metering Collection Tool is distributed as part of Corda Enterprise 4.6 under the name `corda-tools-metering-collector-4.6.jar`. You must place this `.jar` file in the `cordapps` directory of the node.

## Metering data

The Corda Enterprise metering process is based on the signing of transactions.

Once a transaction is signed, no-one will be able to modify the transaction
without invalidating this signature. This effectively makes the transaction immutable.

The act of signing a transaction is referred to as a **signing event**.
Whenever a signing event occurs, a small piece of data is recorded by the node. This data describes which entity signed the
transaction, what CorDapps and commands were involved, and the time when the signing event occurred.

{{< note >}}
Signing events are recorded on a "per node" basis, so transaction signatures applied by a remote node will only have metering data recorded for those signatures on that node.
The time when a transaction is signed is not exposed outside of the node.
{{< /note >}}

Notaries running on Corda Enterprise are also metered. The data recorded for notaries indicates what notarisation requests were made and who made them.

### How metering data is shared

The Metering Collection Tool also contains responder flows that can be used by other nodes on the network to collect metering data from the node where
the respective CorDapp is installed. This feature must be enabled by the node operator deploying a
[CorDapp configuration file](/docs/corda-os/4.6/cordapp-build-systems.html#cordapp-configuration-files) for the CorDapp.
If no configuration file is deployed, metering data will not be shared with any other network party.

An example configuration file that enables metering data sharing is shown below:

```json
"access_configuration" : {
    "network_collectors" : ["O=PartyA,L=New York,C=US", "O=PartyB,L=Zurich,C=CH"],
    "cordapp_collectors" : {
        "by_name" : {
            "Corda Finance Demo" : ["O=PartyB,L=Zurich,C=CH"]
        },
        "by_hash" : {
          "FC0150EFAB3BBD715BDAA7F67B4C4DB5E133D919B6860A3D3B4C6C7D3EFE25D5" :
            ["O=PartyC,L=London,C=GB"],
          "44489E8918D7D8F7A3227FE56EC34BFDDF15BD413FF92F23E72DD5D543BD6194" :
            ["O=PartyC,L=London,C=GB"]
        },
        "by_signature" : {
          "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" :
            ["O=PartyD,L=Dublin,C=IE"]
        }
    }
}
```

Based on the example configuration above:
* Nodes `PartyA` and `PartyB` collect [aggregated metering data](#using-AggregatedMeteringCollectionFlow) from the node. This means that only the total number of signing events, which have happened within the specified time period, are shared.
* Node `PartyB` node collects detailed metering data related to all installed CorDapps called *Corda Finance Demo* (the name must be an exact match).
* Node `PartyC` collects detailed metering data related to CorDapps with a `.jar` hash either `FC0150EFAB3BBD715BDAA7F67B4C4DB5E133D919B6860A3D3B4C6C7D3EFE25D5` or `44489E8918D7D8F7A3227FE56EC34BFDDF15BD413FF92F23E72DD5D543BD6194`.
* Node `PartyD` collects detailed metering data related to all CorDapps that have had their `.jar` files signed with the key `AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B`.

To create the configuration file correctly, use the [`RetrieveCordappDataFlow`](#using-RetrieveCordappDataFlow) flow to get detailed information about the CorDapps deployed on your node.

{{< warning >}}
It is very important that you create the configuration file correctly. To do so, you must follow the configuration process described below exactly, otherwise the collection of metering data will fail and the node could even fail to start.
{{< /warning >}}

* Use the [`RetrieveCordappDataFlow`](#using-RetrieveCordappDataFlow) flow to get detailed information about the CorDapps deployed on your node.
* Ensure you configure the correct values for the configuration file static keys (`access_configuration`, `network_collectors`, `by_hash`, and so on). Any errors, like a typo, will mean your configuration is ignored and the default applied. As a result, no metering data will be shared.
* Ensure that every `.jar` hash, `.jar` signature, and CorDapp name in the configuration matches at least one of the deployed CorDapps. This means that you must not whitelist a CorDapp that does not exist. This step is essential in order to pass the configuration validation step that runs at node start-up, which checks that the X.500 names used in the configuration file are valid. If the configuration validation step fails for any reason, the node will fail to start.

## Use procedures

This section provides instructions on how to use each of the Metering Collection Tool flows.

{{< note >}}
In the list of flows below:
* The `FilteredMeteringCollectionFlow` flow and the `AggregatedMeteringCollectionFlow` flow gather data from a node or nodes on the network different from the node where the respective flow was initiated.
* The `NodeMeteringCollectionFlow` flow and the `MeteringCollectionFlow` flow collect metering data from the "current" node - the node where each of the flows was initiated.
{{< /note >}}

### Using `MeteringCollectionFlow`

You invoke this flow from the [shell](node/operating/shell.md). The flow takes the following arguments:

1. A time window over which the flow runs. This is a mandatory argument. The accepted time window formats are either a start date and an end date (both of type `Instant`), or a start date and a duration (see the [Usage](#usage) section below). Note that the minimum time unit you can use is an hour, so the flow is unable to collect metering data over durations shorter than an hour.
2. A filter to select which CorDapps to collect data for. To specify a filter, provide a `MeteringFilter` object, which consists of `filterBy` criteria and a list of strings that describe
the CorDapps to filter by. There are four possible options to filter by, which are described in the [data filtering section](#data-filtering).
3. A paging specification to describe how the flow should access the database. The paging specification is used to control database access by ensuring that only a subset of data is accessed at once. This is important in order to prevent too much data being read into memory at once, which would result in out-of-memory errors. By default, up to 10 000 metering entries are read into memory at a time, although the number of returned entries is likely to be smaller because some aggregation takes place in the background. If more than one page of data is required, the flow may need to be run multiple times to collect the full breakdown of metering events. However, the total count provided is always the full number of signing events that match the supplied criteria.

Use the shell interface to invoke the flow by specifying the time window - either provide the `startDate` and `endDate` for the metering data collection in the format `YYYY-MM-DD`, or the `startDate` (in the same format) and the duration as an integer number of `daysToCollect`.

You can also specify a filter according to the rules described in the [data filtering section](#data-filtering). This is not needed if all the metering data is required. As mentioned above, the smallest time window you can specify is one day.

When date strings are required, they are always in the `YYYY-MM-DD` format. If the date does not parse correctly, an exception is thrown.

The example below shows a collection of all metering data over a particular week:

```bash
start MeteringCollectionFlow startDate: 2019-11-07, daysToCollect: 7, page: 1
```

The example below shows a collection of metering data for a particular CorDapp:

```bash
start MeteringCollectionFlow startDate: 2019-11-07, endDate: 2019-11-14, filterBy: CORDAPP_NAMES, filter: ["Corda Finance Demo"], page: 1
```

#### Output

The output of the `MeteringCollectionFlow` flow is a data class that contains a structured representation of the metering data, as follows:

* The total number of signing events that match the query provided.
* The current version of the output metering data.
* An object describing the query that produced this set of data. This includes the time window over which the data was collected, the
filter applied to the data, and the paging criteria used.
* A list of entries giving a breakdown of the metering data. Each entry contains a signing entity, a set of commands, a transaction type,
and a count of events in this page that match this specification.

The output object can also be serialised into `JSON` format by calling `serialize`.

When you run Metering Collection Tool from the shell, the collected metering data is shown as output on the shell terminal, in `JSON` format. The example below shows the output `JSON` on the shell terminal:

```bash
{"totalCount":2,"version":1,"query":{"startDate":"2019-11-13T00:00:00Z","endDate":"2019-11-15T00:00:00Z","filter":{"filterBy":"NONE","values":[]},"pageNumber":1,"totalPages":1,"pageSize":10000},"entries":[{"signingId":{"type":"NODE_IDENTITY","accountId":null},"txType":"NORMAL","commands":["net.corda.finance.contracts.asset.Cash.Commands.Issue"],"count":1},{"signingId":{"type":"NODE_IDENTITY","accountId":null},"txType":"NORMAL","commands":["net.corda.finance.contracts.asset.Cash.Commands.Move"],"count":1}]}
```

### Using `NodeMeteringCollectionFlow`

You can use this flow to retrieve detailed metering data from the node the RPC client connects to. The flow is similar to the `MeteringCollectionFlow` flow, however it provides
a simpler API that does not require data pagination.

{{< note >}}
The metering sharing configuration does not apply here as it is expected that only the node operator is allowed to connect to the node via RPC.
{{< /note >}}

The example below shows how to retrieve metering data from a node running on the local machine, for CorDapps named *myCorDapp1* and *myCorDapp2* (as well as any other CorDapp that contains those two strings in its name), for the duration of the past 7 days:

{{< tabs name="tabs-NodeMeteringCollectionFlow" >}}
{{% tab name="java" %}}
```java
NetworkHostAndPort hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000");
CordaRPCClient client = new CordaRPCClient(hostAndPort);
NodeMeteringData meteringData =
        client.use("rpcUsername", "rpcPassword", conn -> {
            CordaRPCOps rpcOps = conn.getProxy();
            Instant now = Instant.now();
            Instant sevenDaysAgo = now.minus(7, ChronoUnit.DAYS);
            FlowHandle<NodeMeteringData> handle = rpcOps.startFlowDynamic(
                    NodeMeteringCollectionFlow.class,
                    new Filter.And(
                            Filter.ByTimeStamp.between(sevenDaysAgo, now),
                            new Filter.Or(
                                    new Filter.ByCordapp.ByName("myCorDapp1"),
                                    new Filter.ByCordapp.ByName("myCorDapp2")
                            )
                    ));
            Future<NodeMeteringData> result = handle.getReturnValue();
            try {
                return result.get();
            } catch (InterruptedException | ExecutionException e) {
                throw new RuntimeException(e);
            }
        });
```

{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000")
val client = CordaRPCClient(hostAndPort)
val nodeMeteringData = client.use("rpcUsername", "rpcPassword") { conn: CordaRPCConnection ->
    val rpcOps = conn.proxy
    val now = Instant.now()
    val sevenDaysAgo = now.minus(7, ChronoUnit.DAYS)
    val handle = rpcOps.startFlow(
            ::NodeMeteringCollectionFlow, Filter.And(
            Filter.ByTimeStamp.between(sevenDaysAgo, now),
            Filter.Or(Filter.ByCordapp.ByName("myCorDapp1"), Filter.ByCordapp.ByName("myCorDapp2"))
    ))
    val result: Future<NodeMeteringData> = handle.returnValue
    try {
        result.get()
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Using `AggregatedMeteringCollectionFlow`
<a name="using-AggregatedMeteringCollectionFlow"></a>

You can use this flow to collect aggregated metering data from a remote node on the network. Aggregated metering data only contains the total number of signing events that happened within a given time period, without any additional information such as signing service public key, contract command, or transaction type.

{{< note >}}
The result of the metering data collection with this flow depends on what the node operator decided to share with you in their [CorDapp configuration](#sharing-of-metering-data). In particular, your X.500 name must be present in their list of `network_collectors`, otherwise the invocation of this flow will result in an `PermissionDeniedException` error.
{{< /note >}}

The example below shows how to retrieve aggregated metering data by connecting to a node running on the local machine, from the node ran by `O=PartyA,L=New York,C=US`, for the duration of the past 7 days:

{{< tabs name="tabs-AggregatedMeteringCollectionFlow" >}}
{{% tab name="java" %}}
```java
NetworkHostAndPort hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000");
CordaRPCClient client = new CordaRPCClient(hostAndPort);
AggregatedNodeMeteringData meteringData =
        client.use("rpcUsername", "rpcPassword", conn -> {
            CordaRPCOps rpcOps = conn.getProxy();
            Party destination = rpcOps.wellKnownPartyFromX500Name(
                    CordaX500Name.parse("O=PartyA,L=New York,C=US")
            );
            Instant now = Instant.now();
            Instant sevenDaysAgo = now.minus(7, ChronoUnit.DAYS);
            FlowHandle<AggregatedNodeMeteringData> handle =
                    rpcOps.startFlowDynamic(AggregatedMeteringCollectionFlow.class,
                            destination,
                            Filter.ByTimeStamp.between(sevenDaysAgo, now)
                    );
            Future<AggregatedNodeMeteringData> result = handle.getReturnValue();
            try {
                return result.get();
            } catch (InterruptedException | ExecutionException e) {
                throw new RuntimeException(e);
            }
        });
```

{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000")
val client = CordaRPCClient(hostAndPort)
val data = client.use("rpcUsername", "rpcPassword") { conn: CordaRPCConnection ->
    val rpcOps = conn.proxy
    val destination = rpcOps.wellKnownPartyFromX500Name(
            CordaX500Name.parse("O=PartyA,L=New York,C=US")
    )!!
    val now = Instant.now()
    val sevenDaysAgo = now.minus(7, ChronoUnit.DAYS)
    val handle = rpcOps.startFlow(
            ::AggregatedMeteringCollectionFlow,
            destination,
            Filter.ByTimeStamp.between(sevenDaysAgo, now)
    )
    try {
        handle.returnValue.get()
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Using `FilteredMeteringCollectionFlow`
<a name="using-FilteredMeteringCollectionFlow"></a>

You can use this flow to collect metering data from a remote node on the network. It is similar to the `NodeMeteringCollectionFlow` flow - the difference between the two is that `FilteredMeteringCollectionFlow` collects metering data from a remote node on the network and `NodeMeteringCollectionFlow` collects metering data from the node the RPC client connects to.

{{< note >}}
The result of the metering data collection with this flow depends on what the node operator decided to share with you in their [CorDapp configuration](#sharing-of-metering-data).

If nothing was shared, you will receive an object with an empty `entries` list. In order for the Metering Collection Tool to distinguish between the case where there was no metering data on the collected node and the case where the node operator did not whitelist it, the returned object contains the `collectedCorDapps` field, which is populated with the list of CorDapps the requester is allowed to collect metering data for.

If `collectedCorDapps` is returned as an empty list, this means that the requester was not authorised to collect metering data from any of the requested CorDapps. However, if `entries` is returned as an empty list but `collectedCorDapps` is not, this means that the CorDapps contained in `collectedCorDapps` have been collected but no metering data was present during the specified time window.
{{< /note >}}

The example below shows how to retrieve metering related to CorDapps with names *myCorDapp1* and *myCorDapp2* (as well as any other CorDapp with a name containing any of those two strings), connecting to a node running on the local machine, from the node ran by `O=PartyA,L=New York,C=US`, for the duration of the past 7 days:

{{< tabs name="tabs-FilteredMeteringCollectionFlow" >}}
{{% tab name="java" %}}
```java
NetworkHostAndPort hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000");
CordaRPCClient client = new CordaRPCClient(hostAndPort);
FilteredNodeMeteringData meteringData =
        client.use("rpcUsername", "rpcPassword", conn -> {
            CordaRPCOps rpcOps = conn.getProxy();
            Party destination = rpcOps.wellKnownPartyFromX500Name(
                    CordaX500Name.parse("O=PartyA,L=New York,C=US")
            );
            Instant now = Instant.now();
            Instant sevenDaysAgo = now.minus(7, ChronoUnit.DAYS);
            FlowHandle<FilteredNodeMeteringData> handle = rpcOps.startFlowDynamic(
                    FilteredMeteringCollectionFlow.class,
                    destination,
                    new Filter.And(
                            Filter.ByTimeStamp.between(sevenDaysAgo, now),
                            new Filter.Or(
                                    new Filter.ByCordapp.ByName("myCorDapp1"),
                                    new Filter.ByCordapp.ByName("myCorDapp2")
                            )
                    )
            );
            Future<FilteredNodeMeteringData> result = handle.getReturnValue();
            try {
                return result.get();
            } catch (InterruptedException | ExecutionException e) {
                throw new RuntimeException(e);
            }
        });
```

{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000")
val client = CordaRPCClient(hostAndPort)
val data = client.use("rpcUsername", "rpcPassword") { conn: CordaRPCConnection ->
    val rpcOps = conn.proxy
    val destination = rpcOps.wellKnownPartyFromX500Name(
            CordaX500Name.parse("O=PartyA,L=New York,C=US")
    )!!
    val now = Instant.now()
    val sevenDaysAgo = now.minus(7, ChronoUnit.DAYS)
    val handle = rpcOps.startFlow(
            ::FilteredMeteringCollectionFlow,
            destination,
            Filter.And(
                    Filter.ByTimeStamp.between(sevenDaysAgo, now),
                    Filter.Or(
                            Filter.ByCordapp.ByName("myCorDapp1"),
                            Filter.ByCordapp.ByName("myCorDapp2")
                    )
            )
    )
    try {
        handle.returnValue.get()
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
```
{{% /tab %}}

{{< /tabs >}}


### Using `RetrieveCordappDataFlow`
<a name="using-RetrieveCordappDataFlow"></a>

You can use this additional utility flow to retrieve CorDapp metadata for a particular CorDapp name, and to obtain CorDapp hashes and signing keys in the correct format in order to construct a valid `MeteringFilter` instance. The flow also returns the version numbers and vendors of the queried CorDapps, allowing you to extract the right hashes and keys for particular versions.

The example below shows how to invoke this flow from the node shell:

```bash
Tue May 05 16:23:08 IST 2020>>> flow start com.r3.corda.metering.RetrieveCordappDataFlow

 ✓ Starting
▶︎ Done
Flow completed with result: [{
  "name" : "Corda Finance Demo",
  "vendor" : "R3",
  "version" : "1",
  "hash" : "FD8C8A320794B7D928DB90EBACC27A06B6AB683111799380286F2F7A8AB819F2",
  "signingKeys" : [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
}, {
  "name" : "Corda Finance Demo",
  "vendor" : "R3",
  "version" : "1",
  "hash" : "44489E8918D7D8F7A3227FE56EC34BFDDF15BD413FF92F23E72DD5D543BD6194",
  "signingKeys" : [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
}, {
  "name" : "Corda Metering Collection Tool",
  "vendor" : "R3",
  "version" : "4.6-SNAPSHOT",
  "hash" : "FC0150EFAB3BBD715BDAA7F67B4C4DB5E133D919B6860A3D3B4C6C7D3EFE25D5",
  "signingKeys" : [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
}]
```

The example below shows how to invoke this flow using RPC:

{{< tabs name="tabs-RetrieveCordappDataFlow" >}}
{{% tab name="java" %}}

```java
NetworkHostAndPort hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000");
CordaRPCClient client = new CordaRPCClient(hostAndPort);
List<? extends CordappData> corDappData =
  client.use("rpcUsername", "rpcPassword", conn -> {
    CordaRPCOps rpcOps = conn.getProxy();
    FlowHandle<List<? extends CordappData>> handle =
      rpcOps.startFlowDynamic(RetrieveCordappDataFlow.class);
    Future<List<? extends CordappData>> result = handle.getReturnValue();
    try {
        return result.get();
    } catch (InterruptedException | ExecutionException e) {
        throw new RuntimeException(e);
    }
});
```

{{% /tab %}}

{{% tab name="kotlin" %}}

```kotlin
val hostAndPort = NetworkHostAndPort.parse("127.0.0.1:10000")
val client = CordaRPCClient(hostAndPort)
val corDappData =
  client.use("rpcUsername", "rpcPassword") { conn: CordaRPCConnection ->
    val rpcOps = conn.proxy
    val handle = rpcOps.startFlow(::RetrieveCordappDataFlow)
    val result: Future<List<CordappData>> = handle.returnValue
    try {
        result.get()
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
```

{{% /tab %}}

{{< /tabs >}}


### Collecting metering data from multiple nodes

There are two mechanisms you can use to collect metering data from multiple nodes on the network - by connecting to the node via:

* the [Corda RPC API](api-rpc.md)
* the [node shell](node/operating/shell.md)

#### Collecting metering data from multiple nodes using the Corda RPC API

You can use the following two methods:
- `FilteredMeteringCollectionFlow.multiCollect`
- `AggregatedMeteringCollectionFlow.multicollect`

Both methods start multiple parallel flows on the collector node, each of them collecting metering data from a different node on the network. You can specify a timeout period
so that any flows that do not terminate within the timeout are simply cancelled, and only the data from the flows that completed successfully is processed.

You can specify a callback as an argument. The callback is invoked once for each destination node as soon as the relative flow returns. The callback takes the following parameters:

* The destination party from which metering data has been collected.
* The `Filter` instance that was used for the metering data collection.
* A `Future` that is guaranteed to be done at the time of the callback invocation.

If the flow invocation resulted in an exception, the exception is thrown again inside the callback when calling `Future.get` and it is expected that the callback is able to handle it. In case this fails, the execution is interrupted, and all the created sub-flows are cancelled.

The example below shows filtered metering collection from two nodes:

{{< tabs name="tabs-FilteredMeteringCollectionFlow.multicollect" >}}
{{% tab name="java" %}}
```java
Instant now = Instant.now();
Instant sevenDaysAgo = now.minus(7, ChronoUnit.DAYS);
Filter filter = new Filter.And(
        Filter.ByTimeStamp.between(sevenDaysAgo, now),
        new Filter.Or(
                new Filter.ByCordapp.ByName("myCorDapp1"),
                new Filter.ByCordapp.ByName("myCorDapp2")
        )
);
CordaRPCOps rpcOps = conn.getProxy();
List<Pair<Party, Filter>> destinations =
        Stream.of("O=PartyA,L=New York,C=US", "O=PartyB,L=New York,C=US")
                .map(CordaX500Name::parse)
                .map(rpcOps::wellKnownPartyFromX500Name)
                .map(party -> new Pair<>(party, filter))
                .collect(Collectors.toList());

FilteredMeteringCollectionFlow.FilteredResultConsumer consumer = (
        Party destination,
        Filter f,
        Future<FilteredNodeMeteringData> result
) -> {
    try {
        FilteredNodeMeteringData data = result.get();
        //do something with the data
    } catch (ExecutionException | InterruptedException e) {
        throw new RuntimeException(e);
    }
};
FilteredMeteringCollectionFlow.multiCollect(
        rpcOps,
        destinations,
        consumer,
        Duration.of(30, ChronoUnit.SECONDS));
```

{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val now = Instant.now()
val sevenDaysAgo = now.minus(7, ChronoUnit.DAYS)
val filter = Filter.And(
        Filter.ByTimeStamp.between(sevenDaysAgo, now),
        Filter.Or(
                Filter.ByCordapp.ByName("myCorDapp1"),
                Filter.ByCordapp.ByName("myCorDapp2")
        )
)
val destinations = sequenceOf("O=PartyA,L=New York,C=US", "O=PartyB,L=New York,C=US")
        .map { CordaX500Name.parse(it) }
        .map { rpcOps.wellKnownPartyFromX500Name(it)!! }
        .map { it to filter }
        .toList()
val consumer = {
    destination: Party,
    filter : Filter,
    result: Future<FilteredNodeMeteringData> ->
    try {
        val data = result.get()
        //do something with the data
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
FilteredMeteringCollectionFlow.multiCollect(
        rpcOps,
        destinations,
        consumer,
        Duration.of(30, ChronoUnit.SECONDS))
```
{{% /tab %}}

{{< /tabs >}}

The example below shows aggregated metering collection from two nodes:

{{< tabs name="tabs-AggregatedMeteringCollectionFlow.multicollect" >}}
{{% tab name="java" %}}
```java
CordaRPCOps rpcOps = conn.getProxy();
Instant now = Instant.now();
Instant sevenDaysAgo = now.minus(7, ChronoUnit.DAYS);
List<Pair<Party, Filter>> destinations =
        Stream.of("O=PartyA,L=New York,C=US", "O=PartyB,L=New York,C=US")
                .map(CordaX500Name::parse)
                .map(rpcOps::wellKnownPartyFromX500Name)
                .map(party -> new Pair<>(party, Filter.ByTimeStamp.between(sevenDaysAgo, now)))
                .collect(Collectors.toList());

AggregatedMeteringCollectionFlow.AggregatedResultConsumer consumer = (
        Party destination,
        Filter f,
        Future<AggregatedNodeMeteringData> result
) -> {
    try {
        AggregatedNodeMeteringData data = result.get();
        //do something with the data
    } catch (ExecutionException | InterruptedException e) {
        throw new RuntimeException(e);
    }
};
AggregatedMeteringCollectionFlow.multiCollect(
        rpcOps,
        destinations,
        consumer,
        Duration.of(30, ChronoUnit.SECONDS));
```

{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val now = Instant.now()
val sevenDaysAgo = now.minus(7, ChronoUnit.DAYS)
val filter = Filter.ByTimeStamp.between(sevenDaysAgo, now)
val destinations = sequenceOf("O=PartyA,L=New York,C=US", "O=PartyB,L=New York,C=US")
        .map { CordaX500Name.parse(it) }
        .map { rpcOps.wellKnownPartyFromX500Name(it)!! }
        .map { it to filter }
        .toList()
val consumer = {
    _ : Party,
    _ : Filter,
    result: Future<AggregatedNodeMeteringData> ->
    try {
        val data = result.get()
        //do something with the data
    } catch (e: ExecutionException) {
        throw e.cause ?: e
    }
}
AggregatedMeteringCollectionFlow.multiCollect(
        rpcOps,
        destinations,
        consumer,
        Duration.of(30, ChronoUnit.SECONDS))
```
{{% /tab %}}

{{< /tabs >}}

#### Multiple nodes collection using the node shell

You can use the following two flows:
- `MultiAggregatedCollectionFlow`
- `MultiFilteredCollectionFlow`

As regards data filtering and permissions, both of them are identical to their single node counterparts - `AggregatedMeteringCollectionFlow` and `FilteredMeteringCollectionFlow`, respectively.

They proceed through all the destination nodes in sequential order. This can significantly slow down the collection process and can cause the execution to hang indefinitely if one of the destination nodes is down or is not running the Metering Collection Tool CorDapp.

Both flows take the following parameters when invoked from the shell:

- `dateFormat`: The date format to use for parsing the `start` and `end` parameter values. The accepted format is [SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html).
- `start`: A string representing the start date to collect metering data from. The accepted format is either [SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html) or the one returned by the `SimpleDateFormat.getInstance` method, which defaults to your locale settings.
- `end`: A string representing the end date to collect metering data by. The accepted format is either [SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html) or the one returned by the `SimpleDateFormat.getInstance` method, which defaults to your locale settings.
- `period`: The period of time after `start` or before `end` to be used for collecting metering data. You can use the following measuring units: `nanoseconds`, `microseconds`, `milliseconds`, `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`, and `years`. You can also use any unambiguous prefix for these units - for example, `1mo` will be interpreted as one month but `1m` will cause an error as it is unclear whether you mean one month or one minute. Any failure in the interpretation of this parameter will raise an exception `IllegalArgumentException`.
- `destinations`: A list of the X.500 names of the parties running the nodes from which metering data is to be collected. The names do not need to be the full qualified X.500 names since `IdentityService.partiesFromName` will be invoked on them and if more parties match input string,
 metering data will be collected from all their nodes. If this parameter is omitted, metering data will be collected from all nodes present in the network map.
 - `txTypes`: A list of transaction types to be included in the results. If this parameter is omitted, transactions of any type will be collected. See [the data filtering paragraph](#data-filtering-shell) for more information about transaction types.
- `filter`: This parameter is only available for `MultiFilteredCollectionFlow` and allows you to filter metering data by CorDapp. See also [the data filtering paragraph](#data-filtering-shell).

{{< note >}}
You only need to specify two out of the following three parameters: `start`, `end`, and `period`. If you only provide `period`, it is implicitly interpreted as an invocation with `period` and `end` values, where `end` is set to the current timestamp.
{{< /note >}}

{{< warning >}}
Due to some node shell limitations, you must wrap the `start`, `end`, `period`, and `dateFormat` parameters within an object when you create them in the shell. For example, use `start : {value: "2020-06-01 05:45"}` instead of simply `start : "2020-06-01 05:45"`.
{{< /warning >}}

#### Output format

For both methods, the result printed in the shell terminal is a formatted `JSON` object. Its keys are the X.500 names of the destination nodes, and its value is the `JSON` representation of the response object returned from the collection - an instance of `AggregatedNodeMeteringData` for `MultiAggregatedCollectionFlow`, and an instance of `FilteredNodeMeteringData` for `MultiFilteredCollectionFlow`. If any of the destination nodes throws an exception, it is shown in the response object `JSON`.

#### Examples

**Collecting aggregated metering data for last month from "O=PartyB,L=New York,C=US" and "O=PartyA,L=New York,C=US"**

```bash
Wed May 06 15:13:52 IST 2020>>> flow start com.r3.corda.metering.MultiAggregatedCollectionFlow period: {value: 1mon}, destinations: [PartyA, PartyB]

▶︎ Starting
    Done
 ✓ Starting
▶︎ Done
Flow completed with result: {
  "data" : {
    "O=PartyB, L=New York, C=US" : {
      "version" : 1,
      "count" : 51
    },
    "O=PartyA, L=New York, C=US" : {
      "exception" : "net.corda.core.flows.FlowException",
      "message" : "com.r3.corda.metering.PermissionDeniedException: You don't have permission to collect aggregated metering from this node",
      "cause" : {
        "exception" : "com.r3.corda.metering.PermissionDeniedException",
        "message" : "You don't have permission to collect aggregated metering from this node"
      }
    }
  },
  "window" : {
    "startInstant" : "2020-04-06T14:14:38.844Z",
    "endInstant" : "2020-05-06T14:14:38.844Z"
  }
}
```

{{< note >}}
In the example above, note that even though `PartyA` threw an `PermissionDeniedException` exception, the collection continued successfully to `PartyB`.
{{< /note >}}

Alternatively, you can achieve a similar result by running the following commands:

```
flow start com.r3.corda.metering.MultiAggregatedCollectionFlow dateFormat: {value: "yyyy-MM-dd"},  period: {value: 1mon}, end : {value: "2020-05-06"}, destinations: [PartyA, PartyB]
flow start com.r3.corda.metering.MultiAggregatedCollectionFlow dateFormat: {value: "yyyy-MM-dd"},  start: {value: "2020-04-06"}, end : {value: "2020-05-06"}, destinations: [PartyA, PartyB]
flow start com.r3.corda.metering.MultiAggregatedCollectionFlow dateFormat: {value: "yyyy-MM-dd"},  start: {value: "2020-04-06"}, end : {value: "2020-05-06"}, destinations: [PartyA, PartyB]
```

**Collecting filtered metering data for last month from `O=PartyB,L=New York,C=US` and `"O=PartyA,L=New York,C=US"`**

```bash
Wed May 06 15:37:45 IST 2020>>> flow start com.r3.corda.metering.MultiFilteredCollectionFlow period: {value: 1mon}, destinations: [PartyA, PartyB], filter: {filterBy: CORDAPP_NAMES, values: [Finance]}, txTypes: [NORMAL]

 ✓ Starting
▶︎ Done
Flow completed with result: {
  "data" : {
    "O=PartyB, L=New York, C=US" : {
      "version" : 1,
      "entries" : [ {
        "signingId" : {
          "type" : "NODE_IDENTITY",
          "accountId" : null
        },
        "txType" : "NORMAL",
        "commands" : [ "net.corda.finance.contracts.asset.Cash.Commands.Issue" ],
        "count" : 1
      } ],
      "collectedCorDapps" : [ {
        "name" : "Corda Finance Demo",
        "vendor" : "R3",
        "version" : "1",
        "hash" : "4DF7DAC0703459E97CB040CD6194ACC0D7B53931FAFC859158B16FDD85D525B5",
        "signingKeys" : [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
      } ]
    },
    "O=PartyA, L=New York, C=US" : {
      "version" : 1,
      "entries" : [ {
        "signingId" : {
          "type" : "NODE_IDENTITY",
          "accountId" : null
        },
        "txType" : "NORMAL",
        "commands" : [ "net.corda.finance.contracts.asset.Cash.Commands.Issue" ],
        "count" : 1
      } ],
      "collectedCorDapps" : [ {
        "name" : "Corda Finance Demo",
        "vendor" : "R3",
        "version" : "1",
        "hash" : "4DF7DAC0703459E97CB040CD6194ACC0D7B53931FAFC859158B16FDD85D525B5",
        "signingKeys" : [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
      } ]
    }
  },
  "params" : {
    "window" : {
      "startInstant" : "2020-04-06T14:38:11.428Z",
      "endInstant" : "2020-05-06T14:38:11.428Z"
    },
    "filter" : {
      "filterBy" : "CORDAPP_NAMES",
      "values" : [ "Finance" ]
    }
  }
}
```
Alternatively, you can achieve a similar result by running the following commands:

```
flow start com.r3.corda.metering.MultiFilteredCollectionFlow period: {value: 1mon}, filter: {filterBy: CORDAPP_HASHES, values: [4DF7DAC0703459E97CB040CD6194ACC0D7B53931FAFC859158B16FDD85D525B5]}
flow start com.r3.corda.metering.MultiFilteredCollectionFlow dateFormat: {value: "yyyy-MM-dd"},  start: {value: "2020-04-06"}, end : {value: "2020-05-06"}, destinations: [PartyA, PartyB], filter: {filterBy: CORDAPP_NAMES, values: [Finance]}, txTypes: [NORMAL]
flow start com.r3.corda.metering.MultiFilteredCollectionFlow dateFormat: {value: "yyyy-MM-dd"},  start: {value: "2020-04-06"}, end : {value: "2020-05-06"}, destinations: [PartyA, PartyB], filter: {filterBy: CORDAPP_NAMES, values: [Finance]}, txTypes: [NORMAL]
```

### Data filtering using the node shell
<a name="data-filtering-shell"></a>

When you use the node shell to filter metering data, you can only filter by:

* CorDapp
* transaction type
* timestamp

#### Filtering by CorDapp

To filter metering data by CorDapp, use the `filter` parameter in the `MeteringCollectionFlow`, `MultiAggregatedMeteringCollectionFlow`, and `MultiFilteredMeteringCollectionFlow` flows.

This parameter requires an object created by the `filterBy` parameter that specifies the type of filter and the filter `values` - an array of strings that represents the filter argument. The following example shows a list of filters available for `filterBy`:

{{< table >}}

|`filterBy` criteria|Description|Data Collected|`Filter` requirement|
|-----------------------|-----------------------------------------------------------|------------------------------------------------|-------------------------------------------------------------|
|NONE|Returns data for all CorDapps|All data for a node|None|
|CORDAPP_NAMES|Returns data for CorDapps matching the specified names|Data for all versions of a CorDapp|List of names, as specified in the CorDapp build information|
|CORDAPP_HASHES|Returns data for any CorDapp in the list with a `.jar` hash|Data for particular CorDapp versions|List of SHA256 hashes of CorDapp `.jar` files|
|SIGNING_KEYS|Returns data for all CorDapps in the list signed with any key|Data for particular Cordapp owner(s)|List of SHA256 hashes of public keys used to sign `.jar` files|

{{< /table >}}

#### Filtering by transaction type

To filter metering data by transaction type, use the `txTypes` parameter in the `MultiAggregatedMeteringCollectionFlow` and `MultiFilteredMeteringCollectionFlow` flows.

This parameter takes an array with all the types that will be included.

The available transaction types are as follows:

- `NORMAL`
- `CONTRACT_UPGRADE`
- `NOTARY_CHANGE`
- `UNKNOWN`

{{< note >}}
The transaction types `NORMAL`, `CONTRACT_UPGRADE`, and `NOTARY_CHANGE` correspond to transactions that cause a ledger update, while the `UNKNOWN` transaction type corresponds to transactions that do not cause a ledger update.
{{< /note >}}

### Data filtering using the RPC API
<a name="data-filtering-rpc"></a>

You can use data filtering via the RPC API for the `NodeMeteringCollectionFlow`, `AggregatedMeteringCollectionFlow`, and `FilteredMeteringCollectionFlow` flows.

{{< note >}}
Filtering by CorDapp is forbidden for the `AggregatedMeteringCollectionFlow` flow - if you provide such a filter, either directly or as part of a boolean filter, an exception `WrongParameterException` will be thrown.
{{< /note >}}

All classes listed below belong to the `com.r3.corda.metering.filter` package.

{{< table >}}

|Class name|Description|
|-|-|
| ```Filter.Or``` | Represents the logical `or` of the filters provided as constructor parameters |
| ```Filter.And``` | Represents the logical `and` of the filters provided as constructor parameters |
| ```Filter.ByTimeStamp.Since``` | Matches only the meterings with a later timestamp than the one provided |
| ```Filter.ByTimeStamp.Until``` | Matches only the meterings with an earlier timestamp than the one provided |
| ```Filter.ByCorDapp.ByName``` | Matches only the meterings related to signing events generated by a CorDapp with a name that contains the provided string |
| ```Filter.ByCorDapp.ByJarHash``` | Matches only the meterings related to signing events generated by a CorDapp with a `.jar` hash that matches the one provided |
| ```Filter.ByCorDapp.ByJarSignature``` | Matches only the meterings related to signing events generated by a CorDapp with a `.jar` file that was signed with the provided public key |
| ```Filter.ByCorDapp.ByTransactionType``` | Matches only the meterings related to transactions of the specified transaction type (helpers are available to specify ledger-updating transactions and non-ledger-updating transactions) |

{{< /table >}}


{{% note %}}
The metering collection functionality Filtering by CorDapp name is case insensitive for MSSQL Server. For more information, see [Database configuration - SQL Server](node/operating/node-database-admin.md#sql-server-3)
{{% /note %}}
