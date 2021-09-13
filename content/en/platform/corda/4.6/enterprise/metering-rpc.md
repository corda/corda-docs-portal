---
date: '2020-07-15T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- node
- administration
title: "Metering client"
weight: 135
---

# Metering client for the Metering Collection Tool

The [Metering Collection Tool](metering-collector.md) collects metering data from one or more Corda Enterprise Nodes. The purpose of the metering _client_ is to perform this remotely without having to access the environment where the collector node is running, or opening a [Shell](node/operating/shell.md) for it. To do this, the metering client uses RPC to connect to a designated collector node. The designated collector node then runs the Metering Collection Tool to collect the metering data from the specified set of nodes: these are known as the destination nodes. The data is then returned to the metering client. The metering client saves the results to a file.

{{< note >}}
Destination nodes must be configured to share their metering data with the designated collector node. For more information, see [How metering data is shared](metering-collector.md#how-metering-data-is-shared).
{{< /note >}}

{{< note >}}
Only the transactions that cause a ledger update are reported (i.e., NORMAL, CONTRACT_UPGRADE, and NOTARY_CHANGE). The transactions that do not cause a ledger update are not included in the metering report. For more information, see [available transaction types](metering-collector.md#filtering-by-transaction-type).
{{< /note >}}

Any Corda Enterprise Node can be used as a designated collector node as long as the destination nodes have been configured to share metering data with it. If one or more destination nodes have not been configured to share metering data with the designated collector node, then the collected data will not include metering data from those nodes, but the metering report will include information that the node has not been configured to share data the requested data.

## Configuration

The metering client requires the following configuration information:

* RPC username, password, and hostname; this information is used to connect to the designated collector node and launch the data collection flows (see [`nodeRpcLogin`](#noderpclogin))
* A list of nodes to retrieve data from (see [`destinations`](#destinations))
* A list of CorDapps to collect the data for (see [CorDapps](#cordapps))
* A collection period (see [Collection period](#collection-period))

The metering client is configured using a configuration file in the [Typesafe/Lightbend](https://github.com/lightbend/config) format. An example is shown below.

```
nodeRpcLogin {
    address  = "localhost:10009"
    username = "rpcUsername"
    password = "rpcPassword"
}
destinations = [ "O=PartyA,L=London,C=GB", "O=PartyB,L=London,C=GB", "O=PartyC,L=London,C=GB" ]
cordappsByName = [ "Corda Finance Demo" ]
cordappsByJarHash = [ "A11D1E66A084B36DAEB8B894B9F4CCE66FC4B57D7EBCAED98B729A4D35A58D36" ]
cordappsBySignatureHash = [ "AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B" ]
output = "output.json"
timeout = "PT30s"
start = "2020-01-01"
end = "2021-01-01"
```

In this example, the metering client connects to the designated collector node with address `localhost:10009` and credentials `rpcUsername` and `rpcPassword`. The designated collector node then queries nodes `O=PartyA,L=London,C=GB`, `O=PartyB,L=London,C=GB`, `O=PartyC,L=London,C=GB` for metering records relating to a CorDapp with name "Corda Finance Demo", a CorDapp with jar hash `A11D1E66A084B36DAEB8B894B9F4CCE66FC4B57D7EBCAED98B729A4D35A58D36` and a CorDapp with signature hash `AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B` between the dates `2020-01-01` and `2021-01-01`. The produced metering report will be saved to `output.json` in the base directory of the metering client.

Some properties in the configuration file can be overwritten using command-line arguments. For more information, see [Running the metering client](#running-the-metering-client).

## Configuration fields

The configuration fields used by the metering client are described below.

### `nodeRpcLogin`

This is **required**.

This is the RPC login information.

The designated collector node is the node which collects the data from the destination nodes. The metering client needs the following information to connect to the designated collector node:

1. The designated collector node address, specified in the `hostname:port` format.
2. The user credentials required to access the designated collector node, specified as `username` and `password`.

#### `nodeRpcLogin` configuration-file example

```
nodeRpcLogin {
    address = "<hostname>:<port>"   // e.g., address = "localhost:10009"
    username = "<username>"         // e.g., username = "rpcUsername"
    password = "<password>"         // e.g., password = "rpcPassword"
}
```

#### `nodeRpcLogin` command-line example

You can overwrite the RPC login elements using any of the following command-line options: `address`, `username`, and `password`.

```bash
--address="localhost:10009" --username="rpcUsername" --password="rpcPassword"
```

### `destinations`

This is **required**.

This is a list of the destination nodes (the nodes that metering data is collected from), specified using their X500 names. If you want metering data to be collected from the designated collector node as well, you must explicitly include it in this list: it is not automatically included.

#### `destinations` configuration-file example

```
destinations = [ "O=PartyA,L=London,C=GB", "O=PartyB,L=London,C=GB", "O=PartyC,L=London,C=GB" ]
```

#### `destinations` command-line example

```bash
--destinations="O=PartyA,L=London,C=GB;O=PartyB,L=London,C=GB;O=PartyC,L=London,C=GB"
```

### CorDapps

Metering data will be collected for each listed CorDapp. You can list the CorDapps in the following ways:

* By name (the `shortName` of the workflows part of the CorDapp).
* By `.jar` hash (SHA-256 hash of the `.jar` file representing the workflows part of the CorDapp).
* By signature hash (SHA-256 hash of the public key used to sign the workflows part of the CorDapp).

These lists are specified by `cordappsByName`, `cordappsByJarHash`, and `cordappsBySignatureHash`.

If none of these are specified, then the client will return a list of CorDapps that are visible to the designated collector node.

If a listed CorDapp does not exist on any of the destination nodes, the report will not show any metering records for that CorDapp. The `unresponsiveNodeList` will be updated with a `Node not configured to share data for filters:` message for each node that does not have CorDapps associated that filter.

#### CorDapps configuration-file example

```
cordappsByName = [ <cordapp name 1>, <cordapp name 2>, ..., <cordapp name N> ]
cordappsByJarHash = [ <cordapp jar hash 1>, <cordapp jar hash 2>, ..., <cordapp jar hash N> ]
cordappsBySignatureHash = [ <cordapp signature hash 1>, <cordapp signature hash 2>, ..., <cordapp signature hash N> ]

```

#### CorDapps command-line example

```bash
--cordappsByName=<cordapp name 1>;<cordapp name 2>; ...;<cordapp name N>  \
--cordappsByJarHash=<cordapp jar hash 1>;<cordapp jar hash 2>; ...;cordapp jar hash N>  \
--cordappsBySignatureHash=<cordapp signature hash 1>;<cordapp signature hash 2>; ...;<cordapp signature hash N>
```

A specific example looks like this:

```bash
--cordappsByName="Corda Finance Demo;Yo Flows; ...;Bikemarket"  \
--cordappsByJarHash="A11D1E66A084B36DAEB8B894B9F4CCE66FC4B57D7EBCAED98B729A4D35A58D36;3BD1DA447CFE79AA754F030DF97FA989106DDA4475D9E8F4EDE30F3A87F47EC5"  \
--cordappsBySignatureHash="AA59D829F2CA8FDDF5ABEA40D815F937E3E54E572B65B93B5C216AE6594E7D6B;AA59DE3E54E572B65B93B5C216AE6594E7D6B829F2CA8FDDF5ABEA40D815F937"
```

### `output`

The location of the output file.

{{< note >}}
If a file already exists in the specified location, a timestamp will be added to the output filename.
{{< /note >}}

_Default_: `output-[timestamp].json`, where `[timestamp]` is a timestamp representing when the collection finished, such as `output-2020-07-22_10-33-12.json`.

#### `output` configuration-file example

```
output = "path/to/output.json"
```

#### `output` command-line example

```bash
--output="path/to/output.json"
```

### `timeout`

The entire allocated collection time. This is _not_ the same as the running time of the client.

{{< note >}}
Use the [`Duration` format](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html) to specify values for `timeout`.
{{< /note >}}

_Default_: `30s` (30 seconds)

#### `timeout` configuration-file example

```
timeout = "PT30s"
```

#### `timeout` command-line example

```bash
--timeout="PT30s"
```

### Collection period

There are two ways to define a collection period:

* Using a `start` value and an `end` value
* Using a `start` value and a `period` value

If you do not specify any of these, then the default values for `start` and `end` will be used.

If you only specify `start`, then the default value of `end` will be used.

If you only specify `end`, then the default value of `start` will be used.

If you only specify `period`, then the default value of `start` will be used.

If you specify `start`, `end`, and `period`, the configuration will be treated as ambiguous and the metering client will return an exception.

#### `start`

This is the start of the collection period.

_Default_: start of the previous calendar quarter.

##### `start` configuration-file example

```
start = "yyyy-MM-dd"
```

##### `start` command-line example

```bash
--start="yyyy-MM-dd"
```

#### `end`

This is the end of the collection period.

_Default_: the end of the previous calendar quarter.

##### `end` command-line example

```bash
--end="yyyy-MM-dd"
```

##### `end` configuration-file example

```
end = "yyyy-MM-dd"
```

#### `period`

You can define the collection period using the `period` option with `start`. This option specifies the amount of time _after_ `start` that metering data should be collected for.  

This can be specified in nanoseconds, microseconds, milliseconds, seconds, minutes, hours, days, weeks, months, and years. If the metering client cannot interpret this parameter, it returns an exception.

For example, if the `period` is set to `P30D` (30 days) and `start` is set, the collection period will be from the `start` date until 30 days after the `start` date.

{{< note >}}
Use the [`Duration` format](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html) to specify values for `period`.
{{< /note >}}

##### `period` configuration-file example

```
period = "P30D"
```

##### `period` command-line example

```bash
--period="P30D"
```

## Running the metering client

The metering client is a `.jar` file which is run on the command line.

```bash
java -jar corda-tools-metering-rpc-client.jar --config "path/to/config.conf"
```

The metering client will report `Collection complete` when data has been collected from all the destination nodes. If some of the nodes were not responsive during the first collection, it will report `Warning: some nodes were not responsive. Please see the generated report.`

It is possible to override settings in the configuration file by using command-line options. In the following example, the RPC login information set in `config.conf` is overridden by the values set on the command line.

```bash
java -jar corda-tools-metering-rpc-client.jar.jar \
  --config "path/to/config.conf"  \
  --address="localhost:32055" \
  --username="user1" \
  --password="password"
```

In the following example, `start`, `period`, and the location of the output file are set on the command line.

```bash
java -jar corda-tools-metering-rpc-client.jar  \
  --config "path/to/config.conf" \
  --start="2020-09-25" \
  --period="P30D" \
  --output="path/to/output.json"
```

## Output format

The output of the metering client is a JSON file that includes the following elements.

{{< table >}}

| Element               | Description                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------|
| `results`             | Maps each CorDapp to the number of metering records of each CorDapp.                        |
| `collectionPeriod`    | Contains the start and end date of this collection period.                                  |
| `nodeCount`           | The total number of nodes included in this report. This does not include unresponsive nodes.|
| `unresponsiveNodeList`        | A list of unresponsive nodes (nodes that timed out during collection).                      |
| `version`             | The version of the format used when collecting data.                                        |
| `collectionTimestamp` | The end timestamp of the latest run. This timestamp is different from the end timestamp in `collectionPeriod` and it represents when the actual collection process finished.|

{{< /table >}}

An example output file is shown below.

```json
{
  "results": [
    {
      "cordappName": <cordappName>,
      "cordappHash": <cordapp Jar Hash>,
      "count": <number_of_signing_events>
    }
  ],
  "collectionPeriod": {
    "start": "yyyy-MM-dd",
    "end": "yyyy-MM-dd"
  },
  "nodeCount": 123,
  "unresponsiveNodeList": [
    {
      "name": "O=PartyC, L=London, C=GB",
      "reason": "Node timed-out during collection."
    },
    {
      "name": "O=PartyC, L=London, C=GB",
      "reason": "Node timed-out during collection."
    }
  ],
  "version": "1",
  "collectionTimestamp": "yyyy-MM-dd HH-mm-ss"
}
```

{{< note >}}
A signing event can be assigned to multiple CorDapps. The total count for each CorDapp will include every event assigned to it, even if that event is also assigned to another CorDapp.
{{< /note >}}

{{< note >}}
If a CorDapp has no metering events associated with it, the metering report will report 0 counts associated with that particular CorDapp.
{{< /note >}}

{{% note %}}
The metering collection functionality Filtering by CorDapp name is case insensitive for MSSQL Server. For more information, see [Database configuration - SQL Server](node/operating/node-database-admin.md#sql-server-3)
{{% /note %}}

## Fault tolerance

As mentioned in [Output format](#output-format), collection from some nodes may fail, meaning that not all of the required data is returned. You can manually re-run the collection to collect the remaining data, and you can re-run it multiple times until all the nodes have responded (meaning the `unresponsive` list will be empty).

To re-run a collection, use the `--previous-report` argument, as shown in the following example.

```bash
java -jar corda-tools-metering-rpc-client.jar  \
  --config "path/to/config.conf" \
  --previous-report="path/to/previous/output.json"  
```

This command will attempt to update the previous collection results by contacting _only_ the nodes in `unresponsiveNodeList`. The data retrieved during this new collection will be merged with the previous report to form a new report.

{{< note >}}
If a node has been reported as misconfigured for a particular filter, no data associated with this node will be added to the report.
{{< /note >}}

To avoid overwriting the previous report, the name of the new report will have the format `[previous-report]-[timestamp].json`, where `[previous-report]` is the file name of the previous report and `[timestamp]` is a timestamp indicating when the collection finished. For example:

* If the previous report was `output.json` and the repeat collection finished at 10:33 on 22 July 2020, the new report will be `output-2020-07-22_10-33-00.json`.
* If the previous report was `output-2020-07-22_10-20-00.json`, then the new report would be `output-2020-07-22_10-20-00-2020-07-22_10-33-00.json`.
