---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- in memory
- transaction data
- install
- node operator
- DAG
- ledger graph

title: LedgerGraph
weight: 500
---

# LedgerGraph

**LedgerGraph** is a CorDapp you can use to get in-memory access to transaction data. Transaction information is kept in a graph structure on any node where **LedgerGraph** is installed. As not all transactions are related to all other transactions, there can actually be multiple components in the graph: each a **directed acyclic graph** (DAG).

**LedgerGraph** enables other CorDapps, such as the set of [Collaborative Recover CorDapps](../collaborative-recovery/introduction-cr), to have near real-time access to data concerning all of a node's transactions and their relationships. Without it, many operations would be unacceptably slow and impractical.

{{< warning >}}
LedgerGraph is a dependency for the set of Collaborative Recovery CorDapps V1.1 and above. If you are using an earlier version of Collaborative Recovery, you should not install the stand-alone LedgerGraph.
{{< /warning >}}

## Installation requirements

* **Corda Enterprise**

    Corda nodes _must_ be running Corda Enterprise NOT Corda Open Source.

* **Node Minimum Platform Version (MPV)** > 6

    LedgerGraph requires operative Corda nodes to have a Minimum Platform Version (MPV) of 6 or greater, which corresponds with Corda Enterprise 4.4 or newer.


### Database requirements

LedgerGraph CorDapps are tested against Corda Enterprise and will work according to the [support matrix.] (../../platform-support-matrix.html#platform-support-matrix).

## Install LedgerGraph


### File Check

The first step in installation of the LedgerGraph CorDapps is to obtain the Jar files (distributable binaries that the Corda node will run). These should be provided by your Corda representative. Once you have obtained the software in a distributable format, you are ready to install them into your operating Corda node.

You should have access to _two_ individual jar files - one for **LedgerGraph** itself, and, optionally, another for the **LedgerGraph Confidential Identities** CorDapp. You should be able to access these files readily on the machine from which you will be performing the installation.

{{< warning >}}
This process will require your node to be down for a small period of time. This means your node will be unable to receive or sign incoming transaction for the duration of the installation process. It is recommended that you perform this installation in a maintenance window or other pre-scheduled and communicated time slot.
{{< /warning >}}

### Flow Draining Mode

In order to safely install the LedgerGraph software, all pending Corda Flows must finish executing. This can be accomplished by enabling `flowDrainingMode` - which is a configuration setting that causes the node to no longer accept any incoming instructions to initiate new flows or accept newly initiated incoming flows. Instead, only currently checkpointed flows will continue to execute until the node is `drained` of any pending activity.

This can be done in one of the following two ways.

* **RPC**

    By RPC using the `setFlowsDrainingModeEnabled` method with the parameter `true`.

* **CRaSH Shell**

    Via the shell by issuing the following command:

    ```sh
    run setFlowsDrainingModeEnabled enabled: true
    ```

### Shut Down the Node

Once the node has been successfully drained of any pending activity you will be able to shut it down safely. Use the `checkpoints` command, as shown below, to output a JSON representation of remaining checkpoints.

```sh
checkpoints dump
```

If this list is empty, the node has been successfully drained. If the list contains representations of in-flight flows, and continues to do so for an unreasonable amount of time, the flows may have become stuck. At this point you may wish to kill the flows explicitly using the `killFlow` api. To learn more about this and the associated risks you can review the documentation found [here](https://docs.corda.net/docs/corda-enterprise/4.4/cordapps/upgrading-cordapps.html#flow-drains).

### Uninstall Old Versions

There are no earlier versions of this CorDapp. However, if you are upgrading from version 1.0 of **Collaborative Recovery**, then you should replace `ledger-sync-confidential-identities-1.0.jar` with `ledger-graph-1.1.jar`.

### Install the CorDapps

{{< warning >}}
Do not install LedgerGraph on nodes running **Collaborative Recovery** CorDapp versions earlier than **v1.1**.
{{< /warning>}}

Using the file transfer protocol of your choice, add the necessary JAR files for `ledger-graph` and, optionally, <nobr>`ledger-graph-confidential-identities`</nobr> to the `cordapps` sub-directory of your Corda node.

Before proceeding, check to ensure that your transfer completed successfully and that the files' sizes don't differ from the originals that you received.

If you're installing the <nobr>`ledger-graph-confidential-identities`</nobr> CorDapp, please refer to the Confidential Identities section of this document.

### Restart the Node

Restart the node in the same manner originally started by the [node operator](../deploy/deploying-a-node.md/).

Depending on the size of the  node's vault, it might take longer to start than it did previously.

{{< note >}}
You have installed LedgerGraph.
{{< /note >}}

### Verify

Now that you have successfully installed the LedgerGraph CorDapps, let's verify that they are available for use. To do so, we will attempt to list out the flows available for initiating via the CRaSH shell.

In the CRaSH shell, run the following command:

```sh
flow list
```

You should now see a list of flows printed to the console, including those listed below. The LedgerGraph CorDapp contains the following flows:

* `GetLedgerGraphMetricsFlow`.
* `GetLedgerGraphErrorsFlow`.

## Configuration Parameters

You can tune **LedgerGraph**'s behaviour through a small set of configuration parameters, shown in this table:

{{< table >}}
|Configuration Parameter|Default Value|Acceptable Value(s)|Description|
|-|:-:|:-:|-|
|`transactionReaderPageSize` &dagger; |`100`|`10` to `10,000,000`|The number of transactions to include in the result set when querying the database during graph initialization.|
|`transactionReaderPoolSize` &Dagger;|`10`|`1` to `1000`|The number of threads to use when deserializing transaction data during graph initialization.|
{{< /table >}}

**&dagger;** Because there can be an extremely large number of transactions in a node's vault, it is important to select an appropriate page size for your database to optimize retrieval performance. Some amount of experimentation may be required on your part to find/define the best value to be used here, so we don't recommend the default value for most production environments.

**&Dagger;** When Corda stores transactions, their data is serialized before being added to a database table. In order for **LedgerGraph** to make use of this data, it must first _deserialize_ it. This can be a relatively slow process, so allowing multiple threads to perform the deserialization in parallel can greatly reduce overall initialization time. You may need to experiment in your set up to find and define the best value to be used here.

## Configure LedgerGraph parameters

To use LedgerGraph's configuration parameters, create a configuration file named after the **LedgerGraph** JAR file. For example, if the JAR file is called `ledger-graph-1.1.jar`, the configuration file would be `<corda_node_dir>/cordapps/config/ledger-graph-1.1.conf`.

If the configuration parameter is not specified, or the configuration file is not present, the default value(s) will be used.

**Example configuration file contents:**

```ini
transactionReaderPageSize = 10000
transactionReaderPoolSize = 32
```


## Support for Confidential Identities

If you are using Corda [Confidential Identities](./../../cordapps/api-confidential-identity.md), you need to add further configuration to LedgerGraph  in order to properly support your environment. This is due to a limitation in the current implementation of the Confidential Identities CorDapp.

This additional configuration step helps to ensure that confidential identities on your node are properly mapped to known identities (where they have been shared with your node) when new transactions are processed and added to the graph.

In order for LedgerGraph to properly identify transactions belonging to specific confidential identities, the **confidential owning keys** for those identities must be shared between the involved Corda nodes before to being loaded by LedgerGraph to retrieve data concerning those transactions.

To configure LedgerGraph for use with Confidential Identities:

1. Deploy the <code>ledger-<b>graph</b>-confidential-identities</code> JAR file to `<corda_node_dir>/cordapps`.

2. Edit the node configuration file `<corda_node_dir>/node.conf`, adding the following flow override:

```js
flowOverrides {
    overrides=[
        {
            initiator="com.r3.corda.lib.ci.workflows.SyncKeyMappingInitiator"
            responder="com.r3.dr.ledgergraph.ci.flows.CustomSyncKeyMappingResponder"
        }
    ]
}
```

## Flows

Following is a list of the flows exposed by **LedgerGraph**:

### `GetLedgerGraphMetricsFlow`

#### Example Usage(s)

    ```
    flow start GetLedgerGraphMetricsFlow
    ```

#### Overview

This flow returns metrics related to **LedgerGraph** itself. Specifically, the following information is returned:

* A list of IDs for transactions that could not be resolved (`unresolvedTransactions`).
* A list of IDs for attachments that could not be resolved (`unresolvedAttachments`).
* A list of IDs for network parameters that could not be resolved (`unresolvedNetworkParameters`).
* Metrics for each DAG (`dagMetrics`).
    * The number of transactions in the DAG (`transactionCount`).
    * The combined size (in bytes) of all transactions in the DAG (`totalSizeOfTransactions`).
    * The number of attachments referenced by transactions in the DAG (`attachmentCount`).
    * The combined size (in bytes) of all attachments referenced by transactions in the DAG (`totalSizeOfAttachments`).
    * The length of the longest "chain" of transactions in the DAG (`lengthOfLongestTransactionChain`).
    * Whether all output states of all transactions in this DAG have been spent (consumed) (`isFullySpent`<sup>*</sup>).

{{< note >}}
The DAG itself is considered to be spent, or "fully spent" when all of the DAG's transactions' output states have been spent (or consumed).
{{< /note >}}

#### Parameters

None.

#### Return Type

A `LedgerGraphMetrics` object.


### `GetLedgerGraphErrorsFlow`

#### Example Usage(s)

```
flow start GetLedgerGraphErrorsFlow
```

#### Overview

If any errors were encountered by **LedgerGraph**, this flow can be used to retrieve information regarding those errors.

#### Parameters

None.

#### Return Type

A list of `GraphError` objects.


## JMX Metrics

A Corda node running the **LedgerGraph** CorDapp will expose the following metrics via JMX.

### `LedgerGraphIsInitialized`

#### Overview

Indicates whether **LedgerGraph** has finished initialization.

#### Parameters

None.

#### Return Type

* `true` if **LedgerGraph** has been initialized, `false` otherwise.

### `LedgerGraphIsSelfConsistent`

#### Overview

Indicates whether **LedgerGraph** is in a consistent state. **LedgerGraph** can be in an inconsistent state for a number of reasons, like missing transaction data, or failure to initialize at node startup. See the log files for more information regarding any consistency issues.

#### Parameters

None.

#### Return Type

`true` if the **LedgerGraph** is in a consistent state. `false` otherwise.

### `LedgerGraphHasUnresolvedTransactions`

#### Overview

Indicates whether **LedgerGraph** has found reference to transactions that it cannot find in the database. When a transaction is inspected and found that it consumes one or more output states of another transaction, but that other transaction can't be found, that _other_ transaction said to be _unresolved_.

#### Parameters

None.

#### Return Type

`true` if any transactions cannot be found, `false` otherwise.

### `LedgerGraphUnresolvedTransactionsCount`

#### Overview

Provides the number of transactions that **LedgerGraph** was unable to resolve.

#### Parameters

None.

#### Return Type

The number of transactions.

### `LedgerGraphHasUnresolvedAttachments`

#### Overview

Indicates whether **LedgerGraph** has found reference to attachments that it cannot find in the database.

#### Parameters

None.

#### Return Type

`true` if any attachments cannot be found, `false` otherwise.

### `LedgerGraphUnresolvedAttachmentsCount`

#### Overview

Provides the number of attachments that **LedgerGraph** was unable to resolve.

#### Parameters

None.

#### Return Type

The number of attachments.

### `LedgerGraphHasUnresolvedNetworkParameters`

#### Overview

Indicates whether **LedgerGraph** has found reference to network parameters that it cannot find in the database.

#### Parameters

None.

#### Return Type

`true` if any network parameters cannot be found, `false` otherwise.

### `LedgerGraphUnresolvedNetworkParametersCount`

#### Overview

Provides the number of network parameters that **LedgerGraph** was unable to resolve.

#### Parameters

None.

#### Return Type

The number of network parameters.

### `getNumberOfLedgerGraphDagsThatExceedLengthThreshold`

#### Overview

Provides the number of DAGs that exceed the specified length. The length of the DAG is taken from the length of the longest path through the DAG from a transaction that has only issuance states to another that has only exit states _or_ one or more unconsumed states.

{{< note >}}
Observe that endpoint's name starts with `get`.
{{< /note >}}

#### Parameters

`maxLength`: Integer. DAGs whose lengths exceed this value will be counted in the number of DAGs that exceed the length threshold.

#### Return Type

The number of DAGs that exceed the specified length.

### `LedgerGraphSpentDagsCount`

#### Overview

Provides the number of DAGs where all of their transactions' output states have been spent/consumed.

#### Parameters

None.

#### Return Type

The number of DAGs whose transactions' states are all spent.

### `LedgerGraphDiskSizeOfSpentDags`

#### Overview

Provides the combined size (in bytes) of all transaction data for all spent DAGs.

#### Parameters

None.

#### Return Type

The number of bytes used by all transactions of all spent DAGs.

### `LedgerGraphErrors`

#### Overview

Provides details on any errors **LedgerGraph** may have encountered during or since initialization.

#### Parameters

None.

#### Return Type

A list of strings that provide a description of the errors that were encountered.

## System Requirements

### Software Requirements

The **LedgerGraph** CorDapp requires participating Corda nodes to be:
- Using Corda Enterprise, not Corda Open Source (OS).
- Corda Minimum Platform Version (MPV) > 6.
- Running on top of a supported [database technology](https://docs.corda.r3.com/platform-support-matrix.html).

### Memory Requirements

Memory requirements for **LedgerGraph** are mainly dependent on the the size of a node's vault. Since **LedgerGraph** is an in-memory graph of all transactions in the vault, its size is directly related to the number of transactions that exist.

Overall memory usage will be dependent on the number of transactions, number of participants (parties) involved in each transaction, and then number of output states for each transaction.

The following table provides a rough estimation of how much RAM _may_ be required for the number of transactions shown. This is a guideline only. There are many variables in any given Corda network that can affect the amount of heap space used, but this should give you an idea.

{{< table >}}
| Number of Transactions | Estimated RAM Usage (MB<sup>&dagger;</sup>) |
|:------------:|:-------------------------------:|
| 10 thousand  | 10                              |
| 100 thousand | 70                              |
| 1 million    | 690                             |
| 10 million   | 6,900                           |
| 100 million  | 71,680  &Dagger; |
{{< /table >}}

**&dagger;** 1MB = 1,024<sup>2</sup> bytes.

**&Dagger;** Extrapolated. Not tested.


## Log Messages

**LedgerGraph** emits its logs from the `com.r3.dr.ledgergraph` package, and following is an example of a Log4j2 _logger_ that enables `DEBUG`-level logging of **LedgerGraph** logs.

```xml
<Loggers>
    <Logger name="com.r3.dr.ledgergraph" level="DEBUG" />
</Loggers>
```

To specify your own Log4j2 configuration, you can set the following property when starting your Corda node. See the [Log4j 2.x docs](https://logging.apache.org/log4j/2.x/manual/configuration.html) for more information on configuring Log4j2.

```
-Dlog4j.configurationFile=path/to/log4j2.xml
```

## Workflow

### Getting Metrics Data

To get some metrics from **LedgerGraph**, you can use the `GetLedgerGraphMetricsFlow`:

```sh
flow start GetLedgerGraphMetricsFlow
```

This flow will return immediately, and will provide output similar to the following (formatted for readability).

```
Flow completed with result: LedgerGraphMetrics(
    unresolvedTransactions=[],
    unresolvedAttachments=[
        4C2325D02D1A17078C0CB5B863DFD031E7845FDBF15103BDB119DFE0B6ADD73F
    ],
    unresolvedNetworkParameters=[],
    dagMetrics=[
        DagMetrics(
            transactionCount=1,
            totalSizeOfTransactions=4206,
            attachmentCount=2,
            totalSizeOfAttachments=181504,
            lengthOfLongestTransactionChain=2,
            isFullySpent=false
        )
    ]
)
```

### Checking for Errors

To check if **LedgerGraph** ran into any errors you can use the `GetLedgerGraphErrorsFlow` flow to get any available information regarding those errors:

```sh
flow start GetLedgerGraphErrorsFlow
```
This flow will return immediately, and will provide output similar to the following.

```
Flow completed with result:
[Attachment with ID '4C2325D02D1A17078C0CB5B863DFD031E7845FDBF15103BDB119DFE0B6ADD73F' could not be found.]
```
