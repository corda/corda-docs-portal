---
aliases:
- /releases/4.4/metering-collector.html
- /docs/corda-enterprise/head/metering-collector.html
- /docs/corda-enterprise/metering-collector.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-ent-4-4-tool-index
tags:
- metering
- collector
title: Metering Collection Tool
---




# Metering Collection Tool

The Metering Collection Tool is used to collect metering data from a Corda Enterprise node. This page describes how
the node records metering data, and how to run the collection tool in order to collect that data.

The tool is distributed as part of Corda Enterprise 4.4 with the name “corda-tools-metering-collector-4.4.jar”. This JAR must be placed in the node’s
`cordapps` folder.

Note that Corda Enterprise nodes record metering data regardless of whether this tool is installed.



## Metering Data

Metering within Corda Enterprise is based on the signing of transactions. The act of signing over a transaction is referred to as a
*signing event*. Whenever a signing event occurs, a small piece of data is recorded by the node. This describes which entity signed the
transaction, what CorDapps and commands were involved, and what time this occurred. Note that signing events are recorded on a per-node
basis, so transaction signatures applied by a remote node will only have metering data recorded for those signatures on that node. Note
also that the time at which a transaction is signed is not exposed outside of the node.

Notaries running Corda Enterprise are also metered. In this case, data is recorded indicating what notarisation requests have been made
and who made them.


## Overview of the Metering Collection Tool

The Metering Collection Tool provides a mechanism for collecting metering data from both normal nodes and notaries running Corda Enterprise.
The tool provides three flows:



* `MeteringCollectionFlow` is used to collect metering data from normal nodes. It takes in a time window over which to collect data, and
optionally a set of CorDapps to filter the data by. It outputs both the total count of metering events that match filter in the time
window, and a breakdown of these events by the commands involved and the signing entities.
* `NotaryCollectionFlow` is used to collect metering data from notaries. It takes in a time window over which to collect the data. It
outputs a total count of notarisation requests over that interval, along with a breakdown of requests against the parties that made them.
* `RetrieveCordappDataFlow` is a utility flow to extract CorDapp hashes and signing keys for a given CorDapp name, in the correct format
for use in the `MeteringCollectionFlow` filter. The flow provides information about the versions and vendors of the returned CorDapps so
that the correct CorDapp data can be selected.



{{< warning >}}
The `NotaryCollectionFlow` does not allow the collection of metering data for notaries configured in highly-available mode.

{{< /warning >}}



## Using the `MeteringCollectionFlow`

As a flow, the `MeteringCollectionFlow` can be invoked in three main ways:



* Via RPC, using `startFlow`
* As a subflow of some wrapping flow
* Via the shell


In order to run `MeteringCollectionFlow`, three things must be specified:



* A time window over which to run
* A filter to select which CorDapps to collect data for
* A paging specification to describe how the flow should access the database


To specify the time window, `MeteringCollectionFlow` takes either a start and end date (both of type `Instant`), or a start date and a duration.
Note that as metering data is only recorded with a time granularity of an hour, the flow will not be able to collect metering data over
durations shorter than an hour.

The filter is specified by providing a `MeteringFilter` object, which consists of a `filterBy` criteria and a list of strings that describe
the CorDapps to filter by. There are four possible options to filter by, which are described below:


{{< table >}}

|`FilterBy` criteria|Description|Data Collected|`Filter` requirement|
|-----------------------|-----------------------------------------------------------|------------------------------------------------|-------------------------------------------------------------|
|NONE|Returns data for all CorDapps|All data for a node|None|
|CORDAPP_NAMES|Returns data for CorDapps matching specified names|Data for all versions of a CorDapp|List of names, as specified in CorDapp build information|
|CORDAPP_HASHES|Returns data for any CorDapp with jar hash in list|Data for particular CorDapp versions|List of SHA256 hashes of CorDapp JAR files|
|SIGNING_KEYS|Returns data for all CorDapps signed with any key in list|Data for particular owner(s) of CorDapps|List of SHA256 hashes of public keys used to sign JAR files|

{{< /table >}}

An additional utility flow is provided to retrieve CorDapp metadata for a particular CorDapp name: `RetrieveCordappDataFlow`. This can be
used to obtain CorDapp hashes and signing keys in the correct format for `MeteringCollectionFlow`. It additionally returns the version
numbers and vendors of the CorDapps, allowing the right hashes and keys to be found for particular versions.

The paging specification is used to control database access by ensuring that only a subset of data is accessed at once. This is important to
prevent too much data being read into memory at once, resulting in out of memory errors. By default, 10000 metering entries are read into
memory at a time. (Note that under the covers some aggregation occurs, so the number of returned entries is likely to be less than this.) If
more than one page of data is required, the flow may need to be run multiple times to collect the full breakdown of metering events.
However, the total count provided is always the full number of signing events that match the supplied criteria.

{{% note %}}
The metering collection functionality Filtering by CorDapp name is case insensitive for MSSQL Server. For more information, see [Database configuration - SQL Server](node/operating/node-database-admin.md#sql-server-3)
{{% /note %}}

### Examples

Collecting metering data for all CorDapps over the last 7 days:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
fun collectData(rpc: CordaRPCOps): CollectedMeteringData {
    val duration = Duration.ofDays(7)
    val startTime = Instant.now() - duration
    val filter = MeteringFilter(FilterBy.NONE, listOf())
    val page = 1 // Collect data for the first page of recorded data
    return rpc.startFlow(::MeteringCollectionFlow, startTime, duration, filter, page).returnValue.getOrThrow()
}
```
{{% /tab %}}

{{< /tabs >}}

Collecting metering data for the Finance Demo CorDapp over the last 7 days:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
fun collectData(rpc: CordaRPCOps): CollectedMeteringData {
    val duration = Duration.ofDays(7)
    val startTime = Instant.now() - duration
    val filter = MeteringFilter(FilterBy.CORDAPP_NAMES, listOf("Corda Finance Demo"))
    val page = 1 // Collect data for the first page of recorded data
    return rpc.startFlow(::MeteringCollectionFlow, startTime, duration, filter, page).returnValue.getOrThrow()
}
```
{{% /tab %}}

{{< /tabs >}}

Note that the name specified here is the name provided in the CorDapp metadata defined as part of the CorDapp build, and not the name of the
JAR file.

Collecting metering data for a particular version of the Finance Demo, using `RetrieveCordappDataFlow` to get the correct hash:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
fun collectData(rpc: CordaRPCOps): CollectedMeteringData {
    val duration = Duration.ofDays(7)
    val startTime = Instant.now() - duration
    val appData = rpc.startFlow(::RetrieveCordappDataFlow, listOf("Corda Finance Demo")).returnValue.getOrThrow()
    val hashes = appData.filter { it.version == "1" }.map { it.hash.toString() }
    val filter = MeteringFilter(FilterBy.CORDAPP_HASHES, listOf(hashes))
    val page = 1 // Collect data for the first page of recorded data
    return rpc.startFlow(::MeteringCollectionFlow, startTime, duration, filter, page).returnValue.getOrThrow()
}
```
{{% /tab %}}

{{< /tabs >}}


## Output Format

`MeteringCollectionFlow` outputs a data class that contains a structured representation of the metering data. The outputted data contains
the following:



* The total number of signing events that match the query provided
* The current version of the output metering data
* An object describing the query that produced this set of data. This includes the time window over which the data was collected, the
filter applied to the data, and the paging criteria used.
* A list of entries giving a breakdown of the metering data. Each entry contains a signing entity, a set of commands, a transaction type,
and a count of events in this page that match this specification.


The output object can also be serialized into JSON form, by calling `serialize`.


## Using the `MeteringCollectionFlow` from the shell

`MeteringCollectionFlow` provides an additional interface to make working with the tool from the shell more straightforward. This interface
uses date strings instead of `Instant` objects to specify the time window and breaks the filter up into its constituent parts. It is also
possible to omit the filter entirely if all metering data is required. Note that the smallest time window that can be specified from the
shell is a day.

When date strings are required, they are always in YYYY-MM-DD format. If the date does not parse correctly, an exception is thrown.

When the metering collector is run from the shell, the data is output to the terminal in JSON format.


### Examples

Collecting all metering data over a particular week:

```bash
start MeteringCollectionFlow startDate: 2019-11-07, daysToCollect: 7, page: 1
```

Collecting metering data for a particular CorDapp:

```bash
start MeteringCollectionFlow startDate: 2019-11-07, endDate: 2019-11-14, filterBy: CORDAPP_NAMES, filter: ["Corda Finance Demo"], page: 1
```

An example of the output JSON on the shell is shown below:

```bash
{"totalCount":2,"version":1,"query":{"startDate":"2019-11-13T00:00:00Z","endDate":"2019-11-15T00:00:00Z","filter":{"filterBy":"NONE","values":[]},"pageNumber":1,"totalPages":1,"pageSize":10000},"entries":[{"signingId":{"type":"NODE_IDENTITY","accountId":null},"txType":"STANDARD","commands":["net.corda.finance.contracts.asset.Cash.Commands.Issue"],"count":1},{"signingId":{"type":"NODE_IDENTITY","accountId":null},"txType":"STANDARD","commands":["net.corda.finance.contracts.asset.Cash.Commands.Move"],"count":1}]}
```
