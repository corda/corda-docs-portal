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
- LedgerRecover
- ledger recovery

title: LedgerRecover (Automatic)
weight: 500
---

# LedgerRecover (Automatic)

**Who this documentation is for:**
* Node operators
* Business Network Operators (BNOs)
* Corda developers

In a disaster recovery scenario, you can use LedgerRecover to either automatically or manually recover lost data. You should consider the automatic process your preferred option, before trying to recover data manually.

## Configuration parameters

LedgerRecover can be configured, [like other CorDapps](../../cordapps/cordapp-build-systems), by creating a configuration file named after the LedgerRecover configuration `.jar` file. For example, if the LedgerRecover `.jar` file is called `ledger-recover-1.0.jar`, the configuration file would be `<corda_node_dir>/cordapps/config/ledger-recover-1.0.conf`.

You can adjust LedgerRecover behaviour using the configuration parameters set out in the table below. If a configuration parameter is not specified, or the configuration file is not present, the default value is used.

**Example configuration file contents**

```ini
maxAllowedTransactions = 30
maxAllowedSizeInBytes = 3000000
timeWindowForMaxAllowedSize = 1h
maxAllowedRequests = 30
timeWindowForMaxAllowedRequests = 1h
```

**Details of configuration parameters**

{{< table >}}

|Configuration Parameter|Default Value|Acceptable Value(s)|Description|
|-|:-:|:-:|-|
|`maxAllowedTransactions`|`30`|`1` to `1000`| Maximum number of allowed transactions per recovery request.*|
|<a id="max-allowed-size">`maxAllowedSizeInBytes`</a>|`3000000`|`1` to `10000000`|Use this configuration parameter in conjunction with `timeWindowForMaxAllowedSize` to control the total size of transactions the node will send as a response to a recovery request from another party/node within a given amount of time (sliding time window). For example: 1000000 bytes per minute. **&Dagger;**|
|`timeWindowForMaxAllowedSize` **&dagger;**|`1h`|`1m` to `24h`|Use this configuration parameter in conjunction with `maxAllowedSizeInBytes` to control the total size of transactions the node will send as a response to a recovery request from another party/node within a given amount of time (sliding time window). For example: 1000000 bytes per minute. **&Dagger;**|
|`maxAllowedRequests`|`30`|`1` to `100`|Use this configuration parameter in conjunction with `timeWindowForMaxAllowedRequests` to control how often a node will initiate or respond to recovery requests from another party/node within a given amount of time (sliding time window). For example: 10 requests per minute.|
|`timeWindowForMaxAllowedRequests` **&dagger;**|`1h`|`1m` to `24h`|Use this configuration parameter in conjunction with `maxAllowedRequests` to control how often a node will initiate or respond to recovery requests from another party/node within a given amount of time (sliding time window). For example: 10 requests per minute.|
|`manualExportTransactionsBatchSize`|`100`|`100` to `100000`|Defines the number of transactions that will be read as a batch during manual export. Consider changing this to improve manual export performance. This property has a conservative default value to not exceed the `WHERE value IN(...)` limit, which is different for different databases. Check your database vendor's documentation before changing.|
|`manualImportNumberOfTransactionsToCommitAfter`|`1000`|`1000` to `10000`|Defines the number of transactions to import after which a database commit will be performed during manual import.|

{{< /table >}}

{{< note >}}
\*Number of transactions is used as an estimate for the total size of transaction data on the requester node, as actual size of data is not known by the requester before recovery.
{{< /note >}}

**&dagger;** Duration value. Supported values are the same as the _time portion_ of a duration represented by ISO_8601. For example: `1H`, `3S`, `5H3M2S`, etc... Spaces between or around time elements are tolerated, e.g. `1H 30M`, but other characters are not. The units can be represented in uppercase, or lowercase (that is, `H` or `h`, `M` or `m`, `S` or `s`).

**&Dagger;** In case the size limit is exceeded, no part of the transaction that breaches the limit (together with referenced attachments, network parameters and the transaction backchain) are sent. This prevents the ledger from becoming inconsistent.

## Flows

You need to use flows to initiate and monitor the automatic ledger recovery process. Each flow you can use is detailed in this section, along with its parameters, return type, commmand line interface and examples.

Available flows:

* `AutomaticLedgerRecoverFlow`: Initiates an automatic recovery process with a counterparty.
* `FailAutomaticRecoveryFlow`: Marks an automatic recovery process as failed.
* `ShowInitiatedAutomaticRecoveryProgressFlow`: Returns the number of transactions received against number of total transactions requested on the latest automatic recovery request.
* `GetRecoveryRequestsFlow`: Retrieves recovery requests optionally filtered by the provided parameters.
* `GetCurrentRecoveryRequestWithPartyFlow`: Retrieves the current `RecoveryRequest` with a counterparty.
* `GetRecoveryLogsFlow`: Fetches all `RecoveryLog`s associated with a specific `RecoveryRequest`.


### AutomaticLedgerRecoverFlow

This flow initiates an automatic recovery process with a counterparty.

The requesting node first fetches the latest results of the corresponding `ReconciliationStatus` and verifies that it indicates differences between the ledgers of the requesting and responding nodes.

The requesting node then filters out any transactions that already exist in its vault. This is done to prevent re-requesting a transaction to be recovered that already exists on the ledger, for example, as a result of a concurrent automatic recovery.

Successful execution will persist a record of this `RecoveryRequest` in a custom CorDapp table on both the requesting and responding nodes.

Before a record of the `RecoveryRequest` is persisted by the requester, the following will be checked:

* The list of requested transactions is not empty.
* The number of transactions requested does not exceed the configured limit.
* The number of recovery requests within a timeframe does not exceed the configured limit (for example, 3 requests per 1 hour).
* The total number of transactions requested for recovery within a timeframe does not exceed the configured limit (for example, 30 transactions per hour).
* There is no current `RecoveryRequest` where the requesting node has the same role (for example, listed as the requester of the recovery).

After persisting a record of the `RecoveryRequest`, the requester will send the list of transactions that need to be recovered to the responding party. The responder will conduct the same verifications, as well as assuring that the requesting party is entitled to that transaction data. This is required to prevent privacy leaks and it means that *both* parties must be either a participant to the transactions requested *or* the transactions requested are part of those transactions' respective back-chains.

The verifications above are implemented to ensure that private ledger data is not erroneously or maliciously transmitted in the context of LedgerRecover.

Each transaction is then sent back to and received by the requester using an extended version of the standard `SendTransaction`/`ReceiveTransaction` Corda platform flows. Sending and receipt of the transactions and associated artifacts (backchain transactions, attachments, network parameters) are logged in the `CR_RECOVERY_LOG` table. As the exact size of data to be sent becomes measurable at this stage, this is also when limits to the amount of data sent are applied and the requests get throttled, if applicable.

{{< attention >}}

Importing transaction data triggers the same events as receipt of *new* transactions. This means the recorded time stamp of any *new* transactions will be the *new* time at which they were recorded, not the original time. This is expected behaviour. Nodes do not rely on subjective local time. The only source of truth with respect to time is a notary signature over a time window.

{{< /attention >}}

If the `RecoveryRequest` is successful, it is then marked as `COMPLETED` on both the requester and responder nodes; otherwise, it is marked as `FAILED` and the reason for any failure will also be persisted.

In case of failure, the usage of standard Corda flows for transmission of artifacts prevents the ledger from becoming inconsistent. This holds true even if the transmission has been stopped half way through.

Upon successful completion of the automatic LedgerRecover, all `ReconciliationStatus`es initiated by the requester node (of the recovery) are refreshed. This is done so that newly acquired transactions will not show up as difference in the reconciliation results.

{{< note >}}
When recovered transactions are persisted, these will trigger the same events as were triggered when the transaction was originally persisted (before the disaster). If users are subscribing to vault-observable feeds (see [documentation on updates](https://docs.corda.net/api/kotlin/corda/net.corda.core.node.services/-vault-service/updates.html)), they will receive duplicate updates.
{{< /note >}}

#### Parameters

* `party` - The legal identity of the node from which the transactions will be recovered. This parameter is not nullable.

#### Return type
* None

#### Command Line Interface

```
flow start AutomaticLedgerRecoverFlow party: "<X500 Name of Counterparty>"
```

Example:

```
flow start AutomaticLedgerRecoverFlow party: "O=PartyB, L=London, C=GB"
```

#### Exceptions

* `AutomaticRecoveryException` - Thrown if the corresponding `ReconciliationStatus` shows no differences, if there are no transactions to recover, or if the received transaction was not included in the list of requested transactions.
* `TransactionLimitExceededException` - Thrown if the number of requested transactions per request exceeds the configured limit.
* `RequestLimitExceededException` - Thrown if the number of requests within a timeframe exceeds the configured limit.
* `SizeLimitExceededException` - Thrown by the responder node if the size of artifacts (including not only transactions but referenced artifacts such as attachments and network parameters) to send within a timeframe exceeds the configured limit. In this case, the recovery is only _partially_ completed; the transaction exceeding the limit (including its components) is not sent, but the preceding transactions are sent and saved successfully. See [maxAllowedSizeInBytes](#max-allowed-size) for more details.
* `RecoveryAlreadyInprogressException` - Thrown by either the requesting or responding nodes if an existing `RecoveryRequest` is already in progress.
* `RecoveryRequestVerificationException` - Thrown by the responder node if the `RecoveryRequest` received from the requesting node includes transactions which they are not permitted to request.

### FailAutomaticRecoveryFlow

This flow is used by a party to mark an automatic recovery process as failed. The initiating party marks their recovery request as `FAILED`. A failed `RecoveryRequest` remains as a record in the `CR_RECOVERY_REQUEST` table for record-keeping and querying.

{{< note >}}
This flow should be run after running `killFlow`. See [Killing Automatic Recovery Flows](#Killing-Automatic-Recovery-Flows) for details.
{{< /note >}}

#### Parameters

* `requestId` - The `UUID` representing the automatic `RecoveryRequest` that is to be marked as failed.
* `failReason` - A message indicating the reason why this `RecoveryRequest` is being marked as `FAILED`.

#### Return type

* None

#### Command Line Interface

```
flow start FailAutomaticRecoveryFlow requestId: <UUID of RecoveryRequest>, failReason: "<Cited reason for request failure>"
```

Example:

```
flow start FailAutomaticRecoveryFlow requestId: a5b3d634-9d34-47e8-9733-64db75115392, failReason: "Operator intervention."
```

#### Exceptions

* `RecoveryNotFoundException` - Thrown if the `RecoveryRequest` is not found.
* `AutomaticRecoveryException` - Thrown if the `RecoveryRequest` is not automatic or if it's not `IN_PROGRESS`.

### ShowInitiatedAutomaticRecoveryProgressFlow

Returns the progress (number of transactions received against number of total transactions requested) on the latest automatic recovery request initiated by the node.

#### Parameters

* `party` - The legal identity of the node from which the transactions will be recovered.

#### Return type

* `RecoveryProgress` - A simple data class representing the number of transactions received (`done`) of the total number of transactions requested (`total`).

###### Example output:

```sh
RecoveryProgress(done=13, total=20)
```

#### Command Line Interface

```
flow start ShowInitiatedAutomaticRecoveryProgressFlow party: "<X500 Name of Counterparty>"
```

Example:

```
flow start ShowInitiatedAutomaticRecoveryProgressFlow party: "O=PartyB, L=London, C=GB"
```

#### Exceptions

* `RecoveryNotFoundException` - Thrown if no automatic `RecoveryRequest` initiated by this node is found.

### GetRecoveryRequestsFlow

Retrieves `RecoveryRequest`s optionally filtered by the provided parameters.

#### Parameters

* `party` - The legal identity of the node from which the transactions will be recovered. This parameter is nullable.
* `isRequester` - The values `true` or `false` indicate if the node running the flow wants to query the current recovery that is initiated (`true`) or received (`false`) by it. This parameter is nullable.
* `statuses` - List of recovery statuses that can be queried. This parameter is nullable and represented as type `Set<RecoveryStatusFlag>`.

    >  Note: All parameters are nullable. When used with zero arguments, this flow returns all `RecoveryRequest` records.

#### Return type

* A _list_ of `RecoveryRequest` objects.

##### Example output:

This sample output has been formatted for readability:

```
    Flow completed with result: [
        RecoveryRequest(
            recoveryID=80edc8fc-088c-4367-acb4-cc4d6f0d44c7,
            party=O=PartyB, L=London, C=GB,
            isRequester=true,
            timeStarted=1582813640139,
            timeFinished=null,
            requestedTransactionIDs=[
                BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
                FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273
            ],
            recoveryStatusFlag=IN_PROGRESS,
            failureReason='',
            isManual=false,
            stateMachineRunId=[b2510d34-dc58-45a9-b754-3b90268ff5c7]
        )
    ]
```

#### Command Line Interface

```shell script
flow start GetRecoveryRequestsFlow
```

```shell script
flow start GetRecoveryRequestsFlow party: "O=PartyB, L=London, C=GB", isRequester: null, statuses: null
```

```shell script
flow start GetRecoveryRequestsFlow party: null, isRequester: true, statuses: null
```

```shell script
flow start GetRecoveryRequestsFlow party: "O=PartyB, L=London, C=GB", isRequester: true, statuses: null
```

```shell script
flow start GetRecoveryRequestsFlow party: null, isRequester: null, statuses: ["IN_PROGRESS", "COMPLETED"]
```

```shell script
flow start GetRecoveryRequestsFlow party: "O=PartyB, L=London, C=GB", isRequester: true, statuses: ["IN_PROGRESS", "COMPLETED"]
```


### GetCurrentRecoveryRequestWithPartyFlow

Retrieves the current `RecoveryRequest` with a counterparty.

#### Parameters

* `party` - The legal identity of the node from which the transactions will be recovered.
* `isRequester` - The values `true` or `false` indicate if the node running the flow wants to query the current recovery that is initiated (`true`) or received (`false`) by it.

#### Return type

* `RecoveryRequest` - The `RecoveryRequest` object that has been successfully persisted by the initiating node.

    > Note: This flow returns the current recovery which can be both automatic or manual.

###### Example output:

This sample output has been formatted for readability:
```
    RecoveryRequest(
        recoveryID=80edc8fc-088c-4367-acb4-cc4d6f0d44c7,
        party=O=PartyB, L=London, C=GB,
        isRequester=true,
        timeStarted=1582813640139,
        timeFinished=null,
        requestedTransactionIDs=[
            BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
            FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273
        ],
        recoveryStatusFlag=IN_PROGRESS,
        failureReason='',
        isManual=false,
        stateMachineRunId=[b2510d34-dc58-45a9-b754-3b90268ff5c7]
    )
```


#### Command Line Interface

```
flow start GetCurrentRecoveryRequestWithPartyFlow party: "<X500 Name of Counterparty>", isRequester: <true or false>
```

Example:

```
flow start GetCurrentRecoveryRequestWithPartyFlow party: "PartyA, L=London, C=GB", isRequester: true
```

#### Exceptions
* `MultipleRecoveryRecordsException` - Thrown if there is more than one current recovery in the node's database.

### GetRecoveryLogsFlow

This flow fetches all `RecoveryLog`s associated with a specific `RecoveryRequest`.

#### Parameters

* `recoveryRequestId` - The `UUID` of the `RecoveryRequest` for which the logs will be retrieved.

#### Return type

* A _list_ of `RecoveryLog` objects.

###### Example output:

This sample output has been formatted for readability:
```
    Flow completed with result: [
        RecoveryLog(
            id=38ef35a9-a437-412f-9057-4d087057153f,
            recoveryRequest=RecoveryRequest(
                recoveryID=80edc8fc-088c-4367-acb4-cc4d6f0d44c7,
                party=O=PartyB, L=London, C=GB,
                isRequester=true,
                timeStarted=1582813640139,
                timeFinished=null,
                requestedTransactionIDs=[
                    BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
                    FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273
                ],
                recoveryStatusFlag=IN_PROGRESS,
                failureReason='',
                isManual=false,
                stateMachineRunId=[b2510d34-dc58-45a9-b754-3b90268ff5c7]
            ),
            artifactID=BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
            artifactType=TRANSACTION,
            sizeInBytes=13,
            time=1583102330225
        ),
        RecoveryLog(
            id=c8cb323b-cb42-4e65-a9ba-61d3c27b4c39,
            recoveryRequest=RecoveryRequest(
                recoveryID=80edc8fc-088c-4367-acb4-cc4d6f0d44c7,
                party=O=PartyB, L=London, C=GB,
                isRequester=true,
                timeStarted=1582813640139,
                timeFinished=null,
                requestedTransactionIDs=[
                    BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
                    FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273
                ],
                recoveryStatusFlag=IN_PROGRESS,
                failureReason='',
                isManual=false,
                stateMachineRunId=[b2510d34-dc58-45a9-b754-3b90268ff5c7]
            ),
        artifactID=FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273,
        artifactType=TRANSACTION,
        sizeInBytes=13,
        time=1583102333001
        )
    ]
```


#### Command Line Interface

```shell script
flow start GetRecoveryLogsFlow recoveryRequestId: <UUID of the recovery request>
```

Example:

```shell script
flow start GetRecoveryLogsFlow recoveryRequestId: 38ef35a9-a437-412f-9057-4d087057153f
```

## Related database tables

**Do _NOT_ edit or change the contents of the LedgerSync database table(s).**

### Recovery Request table

Some information regarding the state of recovery can be found in a node's `CR_RECOVERY_REQUEST` table (only present if the LedgerRecover CorDapp is installed). The Recovery Request table logs all recoveries that have taken place and provides all state information.

|Column|Description|
|-|-|
|`recovery_id`|The unique ID of the recovery request.|
|`party_name`|The name of the counterparty that the recovery is related to.|
|`is_requester`|Whether this status represents a recovery that was requested/initiated from this node (`true` or `1`), or from another node _to_ this one (`false` or `0`).|
|`time_started` **&dagger;**|The time the recovery started.|
|`time_finished` **&dagger;**|The time the recovery finished, if applicable.|
|`requested_transaction_ids`|The list of transaction IDs to recover. Stored as a serialized set of transaction IDs.
|`recovery_status`|The status of the recovery: `IN_PROGRESS`, `COMPLETED` or `FAILED`.|
|`failure_reason`|If the recovery encountered an error, such as an exception, a description is stored in this field. Associated with the `FAILED` status.|
|`is_manual`|Whether this recovery is manual (`true` or `1`) or automatic (`false` or `0`).|
|`state_machine_id`|The ID of the state machine that executed the related recovery flow (`null` if the recovery is manual). Recorded in the event the flow needs to be killed via the `killFlow` RPC command.|

**&dagger;** Recorded as the number of milliseconds.

### Recovery Log table

Some information regarding the progress of recovery can be found in a node's `CR_RECOVERY_LOG` table (only present if the LedgerRecover CorDapp is installed). The Recovery Log table logs all artifacts received or sent during recovery and provides all state information.

|Column|Description|
|-|-|
|`recovery_id`|The unique ID of the recovery request.|
|`id`|The unique ID of the recovery log.|
|`artifact_id`|The ID of the artifact received/sent for recovery.|
|`artifact_type`|The type of artifact recovered: `TRANSACTION`, `ATTACHMENT` or `NETWORK_PARAMETERS`.|
|`size_in_bytes`|Size of the artifact in bytes.|
|`time` **&dagger;**|The time the artifact was received/sent for recovery.|

**&dagger;** Recorded as the number of milliseconds.

## JMX metrics

The JMX metrics for LedgerRecover (Automatic) are identical to those of [LedgerRecover (Manual)](ledger-recovery-manual.md#JMX-Metrics).

{{< note >}}
The metrics do not distinguish between automatic and manual recoveries - the results returned are aggregated over both types.
{{< /note >}}

## System requirements

System requirements for LedgerRecover (Automatic) are identical to those of [LedgerRecover (Manual)](ledger-recovery-manual.md#System-Requirements).

## Log messages

LedgerRecover (Automatic) recovery processes emit logging statements from the package `com.r3.dr.ledgerrecover.app.automatic.flows`. Logging statements generally provide information as to the progress of the flow in which they were made.

## Example workflow

### Scenario

In this scenario, we'll make the following assumptions:

* Our actors, parties A (us) and B (the other party) are on a two-party Corda network comprised of their nodes and a notary).

* Both party nodes are running Corda Enterprise and have LedgerSync and LedgerRecover installed.

* We (party A) have experienced a disaster in which
    * our vault became corrupt,
    * we subsequently restored from our most recent backup,
    * our most recent backup was made 12 hours ago, but there were new transactions that occurred since then (we are missing transactions).

* All of our transactions, aside from self-issuances (if any), involved party B.

* We either have not been anonymizing our identity, or we have exchanged identity information with party B such that party B can identify transactions that involve us, party A.

* [Reconciliation](./ledger-sync.md#Workflow) has been successfully completed and shows differences between our (party A) vault and party B's.

### Process

This process, or a similar process, should be the default workflow after recovering your vault from backup. It should involve every other party you've previously transacted with. In our example, we're only recovering transactions from one other party, but it's likely you've transacted with more than one party in the past.

The automatic LedgerRecover process facilitates the entire recovery process - including the retrieval, verification, formatting and sending of data to be recovered.

#### Step 1. Initiate the automatic recovery request

Once the Reconciliation results with party B show there are missing transactions to be recovered, we (party A) can launch automatic LedgerRecover by running the following flow:

```sh
flow start AutomaticLedgerRecoverFlow party: "O=PartyB, L=London, C=GB"
```

When run successfully, this flow will persist a `RecoveryRequest` in the `CR_RECOVERY_REQUEST` table of the both requesting and responding nodes based on the previously conducted reconciliation. Further operations described will update this record with the current progress.

> Note: Operators can monitor the recovery progress while it is running using [ShowInitiatedAutomaticRecoveryProgressFlow](#ShowInitiatedAutomaticRecoveryProgressFlow).

The requesting node should now have successfully recovered their vault and should be able to transact with the counterparty with whom they were recovering. `RecoveryRequest` will be marked as `COMPLETED` on both nodes and `ReconciliationStatus` will be refreshed automatically on the requester node.

##### Unhappy path - Exception is thrown by the initiating node

If the initiating node (node A) throws an exception, it is very likely for one of the following reasons:

- The reconciliation process is either still in progress or has failed. In the former situation, wait for the reconciliation process to be scheduled or complete. In the latter situation, review the node logs to determine the cause of the reconciliation failure (see the logging section of the [LedgerSync documentation](./ledger-sync.md#Log-Messages)) and then reschedule the reconciliation so that it may be completed successfully.

- The recovery request breached one of the following constraints:
    - The list of transactions to be recovered is empty. This may be a result of a concurrent recovery processes with another counterparty. In this case, the reconciliation result contained only false positives and there is nothing to recover. Consider [refreshing the reconciliation results](./ledger-sync.md#RefreshReconciliationStatusesFlow).
    - There are too many transactions to recover. Consider running a [LedgerRecover (Manual)](./ledger-recovery-manual.md#Workflow) process instead.
    - The automatic recovery requests initiated against the counterparty are too frequent.

##### Unhappy path - Exception is thrown by the responding node

If the responder node (node B) throws an exception, it is very likely for one of the following reasons:

- The recovery request breached one of the following constraints:
    - The list of transactions to be recovered is empty.
    - The total size of transactions requested to be sent has exceeded the configured limits. Consider running a [LedgerRecover (Manual)](./ledger-recovery-manual.md#Workflow) process instead from the initiating node.
    - The automatic recovery requests received from the initiating party are too frequent.
    - The requested transaction data should not be known about by the initiating party.

#### Killing Automatic Recovery Flows

As indicated in steps above, it may be necessary to kill an automatic LedgerRecover flow. This is a *two-step process*.

##### Step 1

The first step is to use the Corda RPC command `killFlow`.  For this, you'll need the **state machine run ID** of the flow to kill. This can be obtained from the output using [GetCurrentRecoveryRequestWithPartyFlow](#GetCurrentRecoveryRequestWithPartyFlow).

```sh
run killFlow id: <state-machine-run-id>
```

Example:

```sh
run killFlow id: 80edc8fc-088c-4367-acb4-cc4d6f0d44c7
```

##### Step 2

The next step is to run the [FailAutomaticRecoveryFlow](#FailAutomaticRecoveryFlow) flow to update the status of the recovery from `IN_PROGRESS` to `FAILED`. This is a necessary step in order to be able to run recoveries with the involved other party in the future. Not completing this step will cause any future recovery request with the involved other party to be rejected, as concurrent automatic recoveries are not permitted.

```
flow start FailAutomaticRecoveryFlow requestId: <UUID of RecoveryRequest>, failReason: "<Cited reason for request failure>"
```

Example:

```
flow start FailAutomaticRecoveryFlow requestId: 80edc8fc-088c-4367-acb4-cc4d6f0d44c7, failReason: "Operator intervention."
```

And if you run the [GetRecoveryRequestsFlow](#GetRecoveryRequestsFlow) flow again as follows,

```sh
flow start GetRecoveryRequestsFlow party: "O=PartyB, L=London, C=GB", isRequester: true
```

you should see the `RecoveryStatusFlag` status set to `FAILED`.

Sample output, formatted for readability:
```
    Flow completed with result: [
        RecoveryRequest(
            recoveryID=80edc8fc-088c-4367-acb4-cc4d6f0d44c7,
            party=O=PartyB, L=London, C=GB,
            isRequester=true,
            timeStarted=1582813640139,
            timeFinished=null,
            requestedTransactionIDs=[
                BA5C1583C3A13A035EB0CDDC7B53B707FFFB6B0BBFB867B7E8E90A9CC4BE3E16,
                FA90DAFC1E0F106FB2F99B96FD41FE7B16EA9E586F683EEA5AF8DA1B14CDF273
            ],
            recoveryStatusFlag=FAILED,
            failureReason='Operator intervention.',
            isManual=false,
            stateMachineRunId=[b2510d34-dc58-45a9-b754-3b90268ff5c7]
        )
    ]
```
