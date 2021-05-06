---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-collaborative-recovery
tags:
- disaster recovery
- collaborative recovery
- install
- node operator

title: The Ledger Sync CorDapp
weight: 400
---

# LedgerSync

**Who this documentation is for:**
* Node operators
* Business Network Operators (BNOs)
* Corda developers

Part of [Collaborative Recovery](introduction-cr.md), LedgerSync is a CorDapp used to discover any differences between the common ledger data held by two nodes that exist on the same Business Network. This is called the **Reconciliation** stage of collaborative recovery.

It uses an efficient set reconciliation algorithm to minimise the amount of network communication required. Reconciliations can be configured to run both on-demand, and at a given time (through the use of scheduled states).

All reconciliations are added to a bounded execution pool, which is configurable, for eventual execution by the internal job scheduler. Results of reconciliations are stored in the database of the node that requested the reconciliation, and work only in one direction.

This means the node that requested the reconciliation will be notified if the responding node has transactions that the requesting node does not. The responding node will not be notified if the requesting node has transactions that the responding node does not.

{{< figure alt="Ledger Sync Flow" zoom="../../resources/collaborative-recovery/ledger-sync-flow.png" >}}

## System requirements

The **LedgerSync** CorDapp requires participating Corda nodes to
 - be using Corda Enterprise, not Corda Open Source (OS); and
 - be using Corda Minimum Platform Version (MPV) >= 6; and
 - have the matching version of the LedgerGraph CorDapp installed; and
 - running on top of a supported [database technology](../../platform-support-matrix).

## Configuration parameters

You can adjust LedgerSync behaviour using the configuration parameters listed below. If the configuration parameter is not specified, or the configuration file is not present, the default values are used.

You can configure LedgerSync, like other CorDapps, by creating a configuration file named after the LedgerSync configuration `.jar` file. For example, if the LedgerSync `.jar` file is called `ledger-sync-1.0.jar`, the configuration file would be `<corda_node_dir>/cordapps/config/ledger-sync-1.0.conf`.


### Example configuration file contents

```ini
maxNumberOfIbfFilterFlows = 5
maxNumberOfParallelReconciliationRequests = 3
maxReconciliationRetryAttemptTimeout = 1h
timeWindowForReconciliationRequestLimit = 1h
maxAllowedReconciliationRequestsPerTimeWindow = 1000
```

### Details of configuration parameters

{{< table >}}


|Configuration Parameter|Default Value|Acceptable Value(s)|Description|
|-|:-:|:-:|-|
|`maxNumberOfIbfFilterFlows`|`5`|`1` to `15`|When LedgerSync attempts to reconcile with another party, it exchanges a number of "Invertible Bloom Filters" in order to accurately estimate the number of ledger differences. This configuration parameter is used to limit the number of these exchanges in order to prevent intentional/accidental abuse of the responding node's flow.|
|`maxNumberOfParallelReconciliationRequests`|`3`|`1` to `10`|Limits the configured node to the specified maximum number of active concurrent (parallel) reconciliations. |
|`maxReconciliationRetryAttemptTimeout` **&dagger;**|`1h`|`0s` or more|When the configured node's execution pool for reconciliations is full, it will reject any _incoming_ reconciliation requests by throwing an exception to the requester, indicating that it is too busy to handle the request. This configuration parameter is used to control how long the requesting node will keep retrying the reconciliation. Back-pressure is applied to keep the node from retrying excessively over short periods. |
|`timeWindowForReconciliationRequestLimit` **&dagger;**|`1h`|`0s` or more|Use this configuration parameter in conjunction with `maxAllowedReconciliationRequestsPerTimeWindow` to control how often a node will respond to reconciliation requests from another party/node within a given amount of time (sliding time window). For example: 10 responses per minute. Note that this limit is not preserved over node restarts.|
|`maxAllowedReconciliationRequestsPerTimeWindow`|`1000`|`0` to `2147483647`|Use this configuration parameter in conjunction with `timeWindowForReconciliationRequestLimit` to control how often a node will respond to reconciliation requests from another party/node within a given amount of time (sliding time window). For example: 10 responses per minute. Note that this limit is not preserved over node restarts.|
|`transactionReaderPageSize`|`100`|`10` to `10000000`|During initialization, the vault is read in batches (or pages) of rows to optimize database read performance. This controls the batch/page size used during that operation.|
|`transactionReaderPoolSize`|`10`|`5` to `1000`|The number of threads to use when deserializing transaction data during initialization.|


{{< /table >}}

**&dagger;** Duration value. Supported values are the same as the *time portion* of a duration represented by ISO_8601. For example: `1H`, `3S`, `5H3M2S`, and so on. Spaces between or around time elements are tolerated, e.g. `1H 30M`, but other characters are not. The units can be represented in uppercase, or lowercase (that is, `H` or `h`, `M` or `m`, `S` or `s`).


## Flows

All reconciliation tasks are carried out using flows. You can see the list flows exposed by LedgerSync, and their parameters, below:

### `ScheduleReconciliationFlow`

This flow starts an outgoing reconciliation from the current node with each of the specified parties. The reconciliation is added as a job to an internal queue for eventual execution. When the reconciliation starts depends on whether there are other ongoing reconciliations and whether the configured maximum for concurrent reconciliations has been exceeded.

The flow will first check that the node is self-consistent - a check facilitated by the Collaborative Recovery CorDapps. An in-memory representation of vault data is built to ensure all transactions and dependencies are correctly recorded in vault tables. The in-memory representation is built using only the necessary transaction metadata - not the underlying transaction data. This allows the constructed graph to contain an arbitrarily large of transactions without impacting node performance.

If the other party being reconciled with is too busy, the scheduler will make numerous attempts to perform the reconciliation with an appropriate fallback so as not to overwhelm the other party's node with repeated attempts. The number of attempts depends on the node's LedgerSync configuration - see the `maxReconciliationRetryAttemptTimeout` configuration parameter in the table above.

Reconciliation is bound by the `maxMessageSize` [network parameter](../../network/network-map.html#network-parameters). This means that if there is a very large number of differences between two nodes, it may not be possible to perform the reconciliation. In that event, the reconciliation would fail with `MaxMessageSizeExceededException`. You can see this in the logs, or by calling `GetReconciliationStatusForPartyFlow`.

{{< attention >}}
When you request a reconciliation to be performed with a party, if the execution pool is full, the reconciliation will be delayed until an open spot in the pool becomes available. If the node is restarted, and the reconciliation job has not entered the execution pool prior to the restart, the job will be lost and will need to be re-requested by calling this flow again.
{{< /attention >}}

It is not possible to perform reconciliations under the following conditions:

* The party being reconciled against has the same identity as the node where you're starting the reconciliation (a party can't reconcile with itself).
* There is already an *outgoing* reconciliation scheduled/ongoing with the other party.

This flow returns immediately after the reconciliation jobs are added to the scheduler's queue. To get the status of a given reconciliation, see the related flows below.

If `ScheduleReconciliationFlow` returns without successfully scheduling reconciliation activity, you, the node operator, should review the logs. In this case, the node is either still performing self-consistency checks (which may be the case if the node was started recently) or the node may have experienced a disaster resulting in inconsistent vault data. If this is the case, the node must be restored from backup to a consistent state before proceeding. To confirm if inconsistencies have been detected in vault data, check the following exposed [JMX metrics](#jmx-metrics) - getLedgerGraphIsInitialized, getLedgerGraphIsSelfConsistent, getLedgerGraphErrors.

#### Example usage

`flow start ScheduleReconciliationFlow parties: ["O=PartyA, L=London, C=GB", "O=PartyB, L=Ottawa, C=CA"]`

#### Parameters

* `parties` - A list of legal identies of the nodes to reconcile against.

#### Return type

* None

### `GetReconciliationStatusesFlow`

Gets a list of all reconciliation statuses that match the given criteria. For example, you can use this method to get all of the statuses that are `IN_PROGRESS` and were initiated by the current node.

#### Example usages

*   ```
    flow start GetReconciliationStatusesFlow isRequester: true
    ```
*   ```
    flow start GetReconciliationStatusesFlow party: "O=PartyA, L=London, C=GB", isRequester: true
    ```
*   ```
    flow start GetReconciliationStatusesFlow party: "O=PartyA, L=London, C=GB", lastReconciliationStatus: IN_PROGRESS, isRequester: true
    ```
*   ```
    flow start GetReconciliationStatusesFlow lastReconciliationStatus: DIFFERENCES_FOUND, isRequester: true
    ```

#### Parameters

* `party` - The legal identity of the node for which you want to get the status (optional).
* `lastReconciliationStatus` - The status that you want to look up (optional).
* `isRequester` - Whether you want to look up statuses where the current node initiated the reconciliation (`true`), or whether it was another party that initiated it with the current node (`false`).

#### Return type

* A _list_ of `ReconciliationStatus` objects.

### `GetReconciliationStatusForPartyFlow`

Gets the status of the reconciliation for the given party.

#### Example usage(s)

`flow start GetReconciliationStatusForPartyFlow party: "O=PartyA, L=London, C=GB", isRequester: true`


#### Parameters

* `party` - The legal identity of the node for which you want to get the status.
* `isRequester` - Whether you want to look up the status where the current node initiated the reconciliation (`true`), or whether it was another party that initiated it with the current node (`false`).

#### Return type

A `ReconciliationStatus` object, or `null` if there was no reconciliation found for the given parameters.

### `RefreshReconciliationStatusesFlow`

This flow "refreshes" the results of a previous reconciliation where transactions were found to be missing from the current node's ledger. It scans the node's ledger looking for transactions whose IDs match those in the list of missing transactions. If transactions are found, the reconciliation's status is updated to reflect that the transactions are no longer missing.

You need to refresh a reconciliation's status in the case where some, or all, of the missing transactions have been recovered.

#### Example usage(s)

`flow start RefreshReconciliationStatusesFlow`

#### Parameters

None

#### Return type

None

### `StopReconciliationForPartyFlow`

Sets the status of an outgoing or incoming reconciliation request to `STOPPED`, and attempts to kill any threads attached to the reconciliation. This should only be used in conjunction with (after) the Corda `killFlow` RPC command. This is a necessary step in some circumstances since, otherwise, the scheduler would not be able to start a new reconciliation with the involved party.

#### Example usage(s)

`flow start StopReconciliationForPartyFlow`

#### Parameters

`party` - The legal identity of the node for whom you want to stop the reconciliation.

#### Return type

None

### `IsReconciliationScheduledForPartyFlow`

This testing flow is used to determine whether the given `Party` has an on-going, _outgoing_, reconciliation in the scheduler. It is not useful for getting the status of a reconciliation. It is only useful for checking if the scheduler is aware of it, not whether it is currently executing.

{{< note >}}
This, and all flows in `com.r3.dr.ledgersync.app.flows.internal`, are used for debugging and testing purposes, and should not be used directly by your CorDapps. Its behaviour is implementation-specific, and is subject to change without notice.
{{< /note >}}

#### Example usage(s)

```
flow start IsReconciliationScheduledForPartyFlow party: "O=PartyA, L=London, C=GB"
```

#### Parameters

`party` - The legal identity of the node for which you want to get the scheduling status.

#### Return type

Returns `true` if there is an _outgoing_ reconciliation for the `Party` in the scheduler. Returns `false` otherwise.


### `IsRespondingToReconciliationForPartyFlow`

This testing flow is used to determine whether the given `Party` has an on-going, _incoming_, reconciliation in the scheduler. It is not useful for getting the status of a reconciliation. It is only useful for checking if the scheduler is aware of it, not whether it is currently executing.

{{< note >}}
This, and all flows in `com.r3.dr.ledgersync.app.flows.internal`, are used for debugging and testing purposes, and should not be used directly by your CorDapps. Its behaviour is implementation-specific, and is subject to change without notice.
{{< /note >}}

#### Example usage(s)

```
flow start IsRespondingToReconciliationForPartyFlow party: "O=PartyA, L=London, C=GB"
```
#### Parameters

`party` - The legal identity of the node for which you want to get the scheduling status.

#### Return type

Returns `true` if there is an _incoming_ reconciliation for the `Party` in the scheduler. Returns `false` otherwise.

## Related database tables

Do not edit or change the contents of the LedgerSync database table(s).

The information provided in this section is meant only to provide insight into the purpose of the database tables' existence. It is implementation-specific, and is subject to change without notice.

### Reconciliation Status table

Some information regarding the state of reconciliations can be found in a node's `CR_RECONCILIATION_STATUS` table. This table is present when the LedgerSync CorDapp is installed. You should not rely on this as a log of reconciliations, nor is it reliable for providing all state information.

The status of a reconciliation is only stored/updated in this table when a reconciliation is actually executed by the scheduler (becomes `IN_PROGRESS`), or stops/fails thereafter. Reconciliations that are yet to enter the execution pool will not appear in this table, and so the data in this table should not be used for real-time status monitoring. Please use the provided API (see [Flows](#Flows) or [JMX](#JMX%20Metrics)) to get reliable status information on reconciliations.

### Table Structure

{{< table >}}

|Column|Description|
|-|-|
|`party_name`|The unique name of another party that the reconciliation is related to.|
|`is_requester`|Whether this status represents a reconciliation that was requested/initiated from this node (`true` or `1`), or from another node _to_ this one (`false` or `0`).|
|`state_machine_id`|The ID of the state machine that executed the related reconciliation flow. Recorded in the event the flow needs to be killed via the `killFlow` RPC command.|
|`last_successful_reconciliation_time_started` **&dagger;**|The time the most recent _successful_ reconciliation started (may be different from `last_reconciliation_time_started`). Recorded as the number of milliseconds.|
|`last_successful_reconciliation_time_finished` **&dagger;**|The time the most recent _successful_ reconciliation, if applicable, finished (may be different from `last_reconciliation_time_finished`). Recorded as the number of milliseconds.|
|`last_successful_reconciliation_status` **&dagger;** **&Dagger;**|The status of the most recent _successful_ reconciliation, if applicable. Possible values are `DIFFERENCES_FOUND` or `DIFFERENCES_NOT_FOUND`.|
|`last_successful_reconciliation_result` **&dagger;**|The results of the most recent _successful_ reconciliation (regardless of success), if applicable. Stored as a serialized set of the IDs of all of the transactions that involve the requesting/responding parties as well as all of the transactions that make up their back-chains. If there are no transaction IDs, or there was no successful reconciliation, then an empty set is stored.
|`last_reconciliation_time_started`|The time the most recent reconciliation (regardless of success) started. Recorded as the number of milliseconds.|
|`last_reconciliation_time_finished`|The time the most recent reconciliation (regardless of success) finished. Recorded as the number of milliseconds.|
|`last_reconciliation_status` **&Dagger;**|The status of the most recent reconciliation (regardless of success). Possible values are `IN_PROGRESS`, `DIFFERENCES_FOUND`, `DIFFERENCES_NOT_FOUND`, `FAILED`, or `STOPPED`.|
|`last_reconciliation_error`|If the reconciliation encountered an error, such as an exception, a description is stored in this field. Associated with the `FAILED` status.|

{{< /table >}}

**&dagger;** `last_successful_XXX` columns are only updated when a reconciliation involving the given party completed *successfully*, and so do *not* necessarily represent the most recently run reconciliation. This means that it is possible for these columns to indicate success, when the most recently run reconciliation actually failed.

**&Dagger;** Possible values for `status` columns are:

* `DIFFERENCES_FOUND`

    Applies to: `last_reconciliation_status`, and `last_successful_reconciliation_status`.

    This status indicates that the reconciliation with another party found differences between this node's and their node's ledgers. If the `last_successful_reconciliation_status` field is set to this status, then the contents of the `last_successful_reconciliation_result` field can be considered valid.

* `DIFFERENCES_NOT_FOUND`

    Applies to: `last_reconciliation_status`, and `last_successful_reconciliation_status`.

    This status indicates that the reconciliation with another party did not find any differences between this node's and their node's ledgers.

* `IN_PROGRESS`

    Applies to: `last_reconciliation_status` only.

    This status indicates that the reconciliation with another party is *in progress*, meaning that the process has actually started and is pending completion.

* `FAILED`

    Applies to: `last_reconciliation_status` only.

    This status indicates that the reconciliation with another party has failed due to an error in communication between the nodes, or another unexpected runtime exception. If this status is set, `last_reconciliation_error` will have also been updated with information regarding the reason for the failure.

* `STOPPED`

    Applies to: `last_reconciliation_status` only.

    This status indicates that the reconciliation with another party was manually stopped via the `StopReconciliationForPartyFlow`.


## JMX metrics

A Corda node running the LedgerSync CorDapp exposes the following metrics via JMX.

### `ReconciliationStatus`

Gets the `ReconciliationStatus` for the specified party. If there is no such reconciliation for that party, `null` is returned.

#### Parameters

`party` - The legal identity of the node for which you want the status.

#### Return type

A `ReconciliationStatus` object, or `null` if there is no reconciliation ongoing with the specified party.

### `FailedParties`

Gets a list of party names where their reconciliations have failed.

#### Parameters

None.

#### Return type

A list of party names.

### `PartiesWithDifference`

Gets a list of party names where their reconciliations have reported differences.

#### Parameters

None.

#### Return type

A list of party names.

### `NumberOfScheduledReconciliations`

Gets the number of reconciliations that are currently scheduled for execution.

#### Parameters

None.

#### Return type

The number of reconciliations.

### `NumberOfReconciliationsInProgress`

Gets the number of reconciliations that are currently executing.

#### Parameters

None.

#### Return type

The number of reconciliations.

### `NumberOfFailedReconciliations`

Gets the number of reconciliations that have failed.

#### Parameters

None.

#### Return type

The number of reconciliations.

### `NumberOfReconciliationsWithDifferences`

Gets the number of reconciliations where differences were found.

#### Parameters

None.

#### Return type

The number of reconciliations.

### `NumberOfReconciliationsWithoutDifferences`

#### Overview

Gets the number of reconciliations where differences were *not* found.

#### Parameters

None.

#### Return type

The number of reconciliations.


## Log messages

LedgerSync emits the majority of its logs from the `com.r3.dr.ledgersync` package. Due to limitations in Corda's logger implementation, log messages emitted from flows all come from the package `net.corda.flow`. To facilitate the filtering of LedgerSync-specific flow log messages, those logs are configured with the following Log4j _markers_:

* `ReconcileWithPartyFlow`
* `RefreshReconciliationStatusesFlow`
* `StopReconciliationForPartyFlow`
* `ScheduleReconciliationFlow`

Following are examples of Log4j2 _loggers_ that enable `DEBUG`-level logging of LedgerSync logs from the `com.r3.dr.ledgersync` package, as well as any logs with the `ReconcileWithPartyFlow` marker.

```xml
<Loggers>
    <Logger name="com.r3.dr.ledgersync" level="DEBUG" />

    <Logger name="net.corda.flow" level="DEBUG">
        <MarkerFilter marker="ReconcileWithPartyFlow" onMatch="ACCEPT" onMismatch="DENY" />
    </Logger>
</Loggers>
```

To specify your own Log4j2 configuration, you can set the following property when starting your Corda node. See the [Log4j 2.x docs](https://logging.apache.org/log4j/2.x/manual/configuration.html) for more information on configuring Log4j2.

```
-Dlog4j.configurationFile=path/to/log4j2.xml
```

## Example workflow

In this section, we'll walk through the process of using LedgerSync to perform a reconciliation with another party, where we are missing transactions after a disaster scenario and we'll recover those transactions from the other party.

### Scenario

In this scenario, we'll make the following assumptions:

* Our actors, parties A (us) and B (the other party) are on a two-party Corda network comprised of their nodes and a notary.

* Both party nodes are running Corda Enterprise and have LedgerSync installed.

* Both parties, A and B, perform regular backups of their own vaults.

* We (party A) have experienced a disaster in which
    * our vault became corrupt,
    * we subsequently restored from our most recent backup,
    * our most recent backup was made 12 hours ago, but there were new transactions that occurred since then (we are missing transactions).

* All of our transactions, aside from self-issuances (if any), involved party B.

* We either have not been anonymizing our identity, or we have exchanged identity information with party B such that party B can identify transactions that involve us, party A.

### Process

This process, or a similar process, should be followed every time after recovering your vault from backup. It should involve every other party you've previously transacted with. In our example, we're only reconciling with one other party, but it's likely you've transacted with more than one party in the past.

### Step 1. Reconciliation

The first step we need to perform after recovering our vault from the most recent backup is to initiate a reconciliation request with the other party (party B). This must be done from _our_ (party A's) node.

This can be done using the `ScheduleReconciliationFlow` flow from the Corda CLI:

```sh
flow start ScheduleReconciliationFlow parties: ["O=PartyB, L=London, C=GB"]
```

This flow expects a list, hence the use of brackets `[` `]`.

This flow will return immediately, and should indicate success.

#### When the unexpected happens

It is possible to get an exception when executing this flow.

**`ReconciliationAlreadyScheduledException`** &mdash; As the name suggests, this exception will be thrown if there is already an ongoing reconciliation with the party you've tried to reconcile with. This exception can also occur if the other party (party B) has already initiated a reconciliation with you in the other direction; B -&gt; A instead of A -&gt; B.

**`MaxIncomingSessionsExceededException`** &mdash; This exception can be thrown if the other party (party B) is already overloaded processing reconciliations from other parties. In this event, it is recommended that you try again at a later time.

### Step 2. Checking the Status of the Reconciliation

Since the call to `ScheduleReconciliationFlow` returns immediately, it won't tell you whether the reconciliation was successful, stopped for some reason, or is still in progress.

To view the status of a reconciliation, you can use the `GetReconciliationStatusForPartyFlow` flow from the Corda CLI.

```sh
flow start GetReconciliationStatusForPartyFlow party: "O=PartyB, L=London, C=GB", isRequester: true
```

This flow will look up the status of the given reconciliation (if it exists), and will return a `ReconciliationStatus` object which you can inspect.

If the reconciliation is still in progress, the result of the previous call will look similar to the following (note that the output here has been re-formatted for ease of readability).

```
Flow completed with result: ReconciliationStatus(
    partyName="O=PartyB, L=London, C=GB",
    isRequester=true,
    stateMachineRunId="c243222b-1940-45df-8828-a8496196d274"
    lastSuccessfulReconciliationTimeStarted=null,
    lastSuccessfulReconciliationTimeFinished=null,
    lastSuccessfulReconciliationStatus=null,
    lastSuccessfulReconciliationResult=[

    ],
    lastReconciliationTimeStarted=1582894011489,
    lastReconciliationTimeFinished=null,
    lastReconciliationStatus=IN_PROGRESS,
    lastReconciliationError=""
)
```

If the reconciliation finished, and found differences, the result will look similar to the following (note, again, that the output here has been re-formatted for ease of readability). The `lastSuccessfulReconciliationStatus` field being set to `DIFFERENCES_FOUND` will indicate that there were differences discovered, while the `lastSuccessfulReconciliationResult` field will contain a list of the transaction IDs that were found to exist on party B's node, and missing on ours.

```
Flow completed with result: ReconciliationStatus(
    partyName="O=PartyB, L=London, C=GB",
    isRequester=true,
    stateMachineRunId="c243222b-1940-45df-8828-a8496196d274"
    lastSuccessfulReconciliationTimeStarted=1582893847919,
    lastSuccessfulReconciliationTimeFinished=1582893848879,
    lastSuccessfulReconciliationStatus=DIFFERENCES_FOUND,
    lastSuccessfulReconciliationResult=[
        0B81D5CB3FC8B88669C57281B028D8656F030C6D105FDE4BD34D9051DDB6629B,
        0F4BB8AB994F5860933F402276ED288518592413F56550DB3F79056C8364498D,
        42453FF02CD23715595ED07A3A2C4E84C6DF8C93B6C07C21AA0AE11DFCDFFBB5,
        3D9DDF59F8CD75A4C87A28FB7DB0CAFB758B8D40F3675CBA331AD4A6C27CB132,
        5CB4A8B86D9513D04FD25C067E562511812B9DF2C638168F5CDDB9BEF618FF94,
        DFC3FDF97B6ADBE514DF272BD2B90E2150ACD256E20E5D55275913BEBABCABC4,
        904E7BC465DC28B4717A7B8391916BE0F78568862941B17B2BF62EA789C1CE7D,
        A53D01DF6980EE285FAEB0F8C26E67222B0F91A87C468411DDDC87C0ACD19377,
        997F77E5D02B263F9832F0002C3B18A07298DEF4AAB0E16153B9A9DFC617F604,
        1E014176450C0198A2686A06A2885710F071466B5D537BEEF88510EF9AD48653
    ],
    lastReconciliationTimeStarted=1582893847919,
    lastReconciliationTimeFinished=1582893848879,
    lastReconciliationStatus=DIFFERENCES_FOUND,
    lastReconciliationError=""
)
```

#### When the unexpected happens

* **No differences were found, or not all expected differences were found** &mdash; It is possible that when reconciling with another party that no differences will be discovered between your ledger and theirs, or that you were expecting more to be found, but they weren't. This could be for a number of reasons, but the most likely are that either the transaction(s) did not actually involve the other party, like an issuance, or the other party is not able to tell that the transactions you were expecting involved your identity &ndash; maybe your identity had been anonymized.

* **The reconciliation is 'stuck' with a status of `IN_PROGRESS`** &mdash; This may occur for the following reasons.

1. The other party's node is down, or is not present on the network.
2.  The other party's node does not have the LedgerSync CorDapp installed.
3.  An unforeseen problem was encountered when your node tried to persist an updated status to its database for the reconciliation.

In all cases, it may be necessary to *kill* the flow. See below for the details of this process.

* **An error occurred** &mdash; It is possible that an unforeseen error occurred while processing either the initiating (on your node), or the responding (on the other party's node) flows. In such an event, you will need to inspect the node logs for the cause and may need to re-run the reconciliation.


### Step 3. Transaction recovery

If differences were found during the reconciliation, the next step will be to perform an [Automatic Recovery](ledger-recovery-automatic.md/) or a [Manual Recovery](ledger-recovery-manual.md/).

#### Killing Reconciliation Flows

As indicated in steps above, it may be necessary to kill a reconciliation flow. This is a _two-step process_. The first step is to use the Corda RPC command `killFlow`.  For this, you'll need the **state machine run id** of the flow to kill. This can be obtained from the output when you run `GetReconciliationStatusForPartyFlow`.

```
sh
run killFlow id: <state-machine-run-id>
```

For example:

```
sh
run killFlow id: c243222b-1940-45df-8828-a8496196d274
```

The result of running `killFlow` should look like this:

```
[ERROR] 14:14:32+0000 [flow-worker] corda.flow. - Flow interrupted while waiting for events, aborting immediately {fiber-id=10000004, flow-id=54010768-0e49-4c0b-a996-978cf80ab3d9, invocation_id=e957b4af-f479-4aa0-96ac-9177627bd9ab, invocation_timestamp=2020-02-28T14:02:00.488Z, origin=com.r3.dr.ledgersync.app.services.ReconciliationService, session_id=e957b4af-f479-4aa0-96ac-9177627bd9ab, session_timestamp=2020-02-28T14:02:00.488Z, thread-id=443}
```

The next step, which must be run *after* `killFlow`, is to run the `StopReconciliationForPartyFlow` flow to update the status of the reconciliation from `IN_PROGRESS` to `STOPPED`. Not completing this step will prevent the reconciliation scheduler from being able to do reconciliations with that other party and it will also result in a spot in the scheduler's execution pool being permanently occupied by a reconciliation that does not exist.

```
sh
flow start StopReconciliationForPartyFlow party: "O=PartyB, L=London, C=GB"
```

The result of running the previous flow should look as follows:

```
Flow completed with result: kotlin.Unit
```

And if you run the `GetReconciliationStatusForPartyFlow` flow again as follows:

```
sh
flow start GetReconciliationStatusForPartyFlow party: "O=PartyB, L=London, C=GB", isRequester: true
```

You should see the `lastReconciliationStatus` status set to `STOPPED`.

Sample output, formatted for readability:
```
Flow completed with result: ReconciliationStatus(
    partyName="O=PartyB, L=London, C=GB",
    isRequester=true,
    stateMachineRunId="c243222b-1940-45df-8828-a8496196d274"
    lastSuccessfulReconciliationTimeStarted=null,
    lastSuccessfulReconciliationTimeFinished=null,
    lastSuccessfulReconciliationStatus=null,
    lastSuccessfulReconciliationResult=[

    ],
    lastReconciliationTimeStarted=1582898520512,
    lastReconciliationTimeFinished=1582899423716,
    lastReconciliationStatus=STOPPED,
    lastReconciliationError=""
)
```
