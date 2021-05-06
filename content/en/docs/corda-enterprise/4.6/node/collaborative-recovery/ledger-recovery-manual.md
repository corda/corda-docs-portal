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

title: LedgerRecover (Manual)
weight: 600
---

# LedgerRecover (Manual) guide

**Who this documentation is for:**
* Node operators
* Business Network Operators (BNOs)
* Corda developers

In a disaster recovery scenario, if you have been unable to use the automatic LedgerRecover process to recover lost data, you can attempt the recovery with the manual LedgerRecover approach. In this situation, you and the other node operators involved in the process initiate and execute the LedgerRecover (Manual) [workflows](#workflowsection) manually.

As these processes are managed on a discretionary basis, restrictions on the size, duration or other criteria used with an automatic recovery process are not applied. However, you should be extremely careful when accepting and executing manually initiated `RecoveryRequests`, even more so when the requested
set of transactions IDs is extremely large.

## System requirements

Manual Recovery processes executed via the LedgerRecover CorDapp require participating Corda nodes to be:

- Using Corda Enterprise, not Corda Open Source (OS)
- Corda Minimum Platform Version (MPV) > 6
- Running on top of a supported [database technology](/docs/corda-enterprise/4.6/platform-support-matrix.html)

Corda nodes are also expected to have backups from which they are able to partially restore the contents of their vault to a state that is self-consistent, meaning that all available transactions and dependencies are correctly recorded in the vault and all appropriate tables. These tables may not be current, and may be missing records of some transactions due to a disaster scenario.

## Configuration parameters

{{< table >}}

| Configuration parameter   | Header Two     | Acceptable values |
| :------------- | :------------- | :---------------- |
| `manualExportTransactionsBatchSize` | 100      | 100 to 100000 |
| `manualImportNumberOfTransactionsToCommitAfter` | 1000 | 1000 to 10000 |

{{< /table >}}

## Flows

In this section, you will find the flows that facilitate manual recovery as defined in the LedgerRecover CorDapp.

Descriptions of flows include:
* the name of the initiating flow
* the data required for invocation
* the type of data that is returned
* a description of its intended use.

As a node operator, you will need to interact with LedgerRecover via the exposed flows in addition to the JMX metrics defined in later sections
of this documentation.

### `InitiateManualRecoveryFlow`

This flow initiates a manual recovery process between two nodes on the basis of a previous reconciliation. First, the node will fetch the relevant
`ReconciliationStatus` with the counterparty specified. The `ReconciliationStatus` is the record containing all of the transaction IDs and associated
artifacts that need to be recovered.

The initiating node then persists a `RecoveryRequest` - this is a record containing the details of the recovery. The initial record is persisted in a `REQUESTED` status indicating it has not been acted on by the counterparty. The initiating node will then request that the counterparty also persists a `RecoveryRequest`.

On receipt of this request, the counterparty persists their own record as a `RecoveryRequest` with an identical ID, also in a 'requested' status. The shared ID (represented as a `UUID`) links the corresponding `RecoveryRequest`s across the nodes.

It is important to note that before a record of the `RecoveryRequest` is persisted by the initiator, they will check the following:
* That there is *not* a current `RecoveryRequest` where the initiating node has the same role (for example, listed as the initiator).
* The referenced `ReconciliationStatus` explicitly indicates that there are differences found between the initiating node and the responding node. If any of the above checks fail (by throwing an exception), the initiator will persist the `RecoveryRequest` in a failed `STATUS`.

After persisting a record of the `RecoveryRequest`, the initiator will send the UUID of said request to the responder who will conduct the verifications
listed above in addition to the following:
* The requesting party should either be a participant in the transactions requested or the requested transactions should be part of the backchain.
* If the above checks fail (by throwing an exception), the responder will not persist a record and will propagate an error message back to the initiator.
* The initiator will then persist a `RecoveryRequest` in a failed status with the returned error message.

The verifications above are implemented to ensure that private ledger data is not erroneously or maliciously transmitted via the `LedgerRecover` CorDapp.

#### Parameters

* `party` - The legal identity of the node from whom you will be recovering transactions. This parameter is not nullable and represented as type `Party`.
* `transactionIds` - This is a set of transaction IDs that will be requested from the counterparty as part of the recovery process. This parameter is nullable and represented as type `Set<String>`.

#### Return type

* `RecoveryRequest` - This flow returns the entire `RecoveryRequest` object that has been successfully persisted by the initiating node. This will be displayed in the console as follows:

```
RecoveryRequest(recoveryID=e769be7d-deb1-46dd-98fc-fe09e6e172b3, party=O=PartyB, L=London, C=GB, isRequester=true, timeStarted=1582643485140, timeFinished=null,
requestedTransactionIDs=[4F2F2AFB66670C6F7A4BF0BA201609A70DE49C87C29C8C2ABB19CE55DF251F01, E6156EBA7EEB23802CF2B5D0FE53601B849F0EC0F0326B440957636D3B08E462,
87391C19593CFEEC9F804921790388C869C38496B400522E7D23BD8BD3138494, 4A1C94374E8C27A3ED8760DF32F13ECA6FED464B9EF0C19CCB6C203B76101E06], recoveryStatusFlag=REQUESTED,
failureReason='', isManual=true, stateMachineRunId=null)
```

#### Command Line Interface

* `flow start InitiateManualRecoveryFlow party: <X500 Name of Counterparty>`
* Example: `flow start InitiateManualRecoveryFlow party: "O=PartyB, L=London, C=GB"`

#### Exceptions
* `ManualRecoveryException` - This exception will be thrown by the initiating node if an existing `RecoveryRequest` is currently in progress.
* `DatabaseServiceException` - This will be thrown by either the initiating or responding node if an existing `RecoveryRequest` is in progress and wasn't detected by the initial flow checks.
* `RecoveryRequestVerificationException` - This will be thrown by the responding node if the `RecoveryRequest` received from the initiating node includes transactions which they are not permitted to request.

### `CompleteManualRecoveryFlow`

This flow is used by a node operator to mark an existing `RecoveryRequest` as complete.

This should only be done when:
* the counterparty has exported and delivered a file containing the transactions to be recovered
* you have successfully imported those transactions into the vault.

This is done automatically by the responding party after running `ExportTransactionsFlow` and automatically by the initiating party after running `ImportTransactionsFlow`.

In this process, the initiating party marks their `RecoveryRequest` as complete. This flow does not update the `counterParty`.

#### Parameters

* `requestId` - A `String` representing the `UUID` of the `RecoveryRequest` you wish to mark as completed. This parameter is not nullable.

#### Return type

* `Unit / Void` - None.

#### Command Line Interface

* `flow start CompleteManualRecoveryFlow requestId: <UUID of RecoveryRequest>`
* Example: `flow start CompleteManualRecoveryFlow requestId: "24e3d306-01cd-437d-a6a7-106c299e8245"`

#### Exceptions

* `ManualRecoveryException` - This exception is thrown by the initiating node if there is no `RecoveryRequest` with the ID specified or if a `RecoveryRequest` is found but is not in a 'requested' status.
* `DatabaseServiceException` - This exception is thrown by the either the initiating nodes if the above flow checks fail for the same reasons - if there is no `RecoveryRequest` with the counterparty specified or if a `RecoveryRequest` is found but is not in progress.


### `FailManualRecoveryFlow`

This flow is used by a party to fail a manual recovery process with a counterparty. The initiating party marks their recovery request as having failed.
They then ask the counterparty to do the same, sending them the `requestId` and the `failReason`. Failed `RecoveryRequests` remain as records in the `CR_RECOVERY_REQUEST` table for record-keeping and querying.

#### Parameters

* `requestId` - A `String` representing the `UUID` of the manual `RecoveryRequest` you wish to mark as failed.
* `failReason` - A message indicating the reason you are failing this `RecoveryRequest`.
  An example of an acceptable `failReason` would be:
  This RecoveryRequest was conducted outside of the normal recovery schedule specified in the Business Network Governance documentation.

* When a counterparty opts to fail a given RecoveryRequest that was made at an unexpected or invalid time, this reason would be provided as an argument to the command outlined below.

#### Return type

* `Unit / Void` - None.

#### Command Line Interface

* `flow start FailManualRecoveryFlow requestId: <UUID of RecoveryRequest>, failReason: <Cited reason for request failure>`
* Example: `flow start FailManualRecoveryFlow requestId: "a5b3d634-9d34-47e8-9733-64db75115392", failReason: "Didn't you get the memo?"`

#### Exceptions

* `ManualRecoveryException` - This exception will be thrown by the initiating node if there is no `RecoveryRequest` with the ID specified or if a `RecoveryRequest` is found but is not in a 'requested' status. This exception will also be thrown if the provided `failString` is too long or has unacceptable characters.

### `ExportTransactionsFlow`

This flow fetches a `RecoveryRequest` from the database, verifies that the requested transactions therein should be available to the initiating party and then exports the transaction data as a `VaultArchive`. The related `RecoveryRequest` is then marked as complete. The exported data will be available at: `path`/recoveryStatusID.

This flow only marks the `RecoveryRequest` as complete on behalf of the invoking node. The node that initiated the `RecoveryRequest` will not mark their record as complete until they have successfully imported the transaction data.

#### Parameters

* `requestId` - A `String` representing the `UUID` corresponding to the manual `RecoveryRequest` for which you will be exporting a file containing transaction data (a `VaultArchive`).
* `path` - A `String` representing the file path to which you will export the requested data to the filesystem.

#### Return type

* `Unit / Void` - None.

#### Command Line Interface

* `flow start ExportTransactionsFlow requestId: <UUID of RecoveryRequest>, path: <PATH_TO_DESIRED_VAULT_ARCHIVE_EXPORT>`
* Example: `flow start ExportTransactionsFlow requestId: "a5b3d634-9d34-47e8-9733-64db75115392", path: "/var/folders/vault_archives"`

#### Vault archive

A `VaultArchive` is a file/folder structure representing exported data from the nodes vault. It's structured in a specific format so that the initiating node (for whom you are exporting this `VaultArchive`) is able to interpret and import the transaction data back into their vault. The data in the `VaultArchive` is stored in [Corda Wire Format](https://docs.corda.net/wire-format.html) and may be deserialized and inspected using the [Corda Blob Inspector](https://docs.corda.net/blob-inspector.html).

An example of the file folder structure of a `VaultArchive` is defined below:

{{< table >}}

|Recovery Folder Title|Artifact Folder Title|Artifact Description|
|-|-|-|
|`RecoveryId`|`attachments`|This folder contains all attachments referenced in the attached transactions with file names corresponding to the file hash.|
|-|`network-parameters`|This folder contains all serialized network parameters used in the attached transactions with file names corresponding to the hashed data.|
|-|`recovery-description`|This is a summary file containing information required by the `LedgerRecover` CorDapp for verification and import by the initiating counterparty.|
|-|`transactions`|This folder will contain all transactions represented as individual files, identified by the transaction ID.|

{{< /table >}}

An example of how to deserialize a given transaction is defined here as well:

Generic: `java -jar corda-tools-blob-inspector.jar <PATH_TO_ARCHIVE_DIRECTORY>`

Example command: `java -jar corda-tools-blob-inspector-4.3.jar /private/var/folders/208d202e-40fe-4427-9f8d-b38b5b54a7e6/transactions/0B996DCD52265D866DC9424779556229CB30AB489C2AF6B60454F84B122A6E1B`

Example output:

        net.corda.core.transactions.SignedTransaction
        ---
        wire:
          id: "0B996DCD52265D866DC9424779556229CB30AB489C2AF6B60454F84B122A6E1B"
          notary: "O=Notary, L=London, C=GB"
          inputs:
          - txhash: "E60F725BA973D2B2AE28009BBF389578653ECBA7C11452B088DDC3BA822C6C82"
            index: 0
          outputs:
          - data: !<net.corda.finance.contracts.asset.Cash$State>
              amount: "100.00 GBP issued by O=NodeA, L=New York, C=US[00]"
              exitKeys:
              - "GfHq2tTVk9z4eXgyNrHSfCfsKgKtNBHQLwBEj5GauybzPn8xXQjYJC61hgfL"
              - "GfHq2tTVk9z4eXgyU5aRQzVRG9E1YuJpuiT6L48nChgLMjyJLBCXGhwnXKYJ"
              owner: "O=NodeB, L=New York, C=US"
            contract: "net.corda.finance.contracts.asset.Cash"
            notary: "O=Notary, L=London, C=GB"
            encumbrance: null
            constraint: !<net.corda.core.contracts.HashAttachmentConstraint>
              attachmentId: "6D3710B6908D0DD7F62CCD40A61DB8DC2203C68B6A2FB67884E1E92990FDE642"
          commands:
          - value: !<net.corda.finance.contracts.asset.Cash$Commands$Move>
              contract: null
            signers:
            - "GfHq2tTVk9z4eXgyU5aRQzVRG9E1YuJpuiT6L48nChgLMjyJLBCXGhwnXKYJ"
          timeWindow: null
          attachments:
          - "6D3710B6908D0DD7F62CCD40A61DB8DC2203C68B6A2FB67884E1E92990FDE642"
          references: []
          privacySalt: "2E3D8C3691E8DA4236FFF733E1C8F354E78FD30D20CDC176E363FBA53769C21C"
          networkParametersHash: "8E5B1401F0CE19E4FC54797A9AF35F229F26826A8AD4825890D7EA26B66B91D5"
        signatures:
        - bytes: !!binary |-
            Pd6YzKVz/p+VJZJAIhAx+1MTs6K4aZJiYJdzucgJjhDI6A+1FUXvsD3t3r9Uxgvs2x9BIcPmLoR6\nsfhGXHnTAA==
          by: "GfHq2tTVk9z4eXgyU5aRQzVRG9E1YuJpuiT6L48nChgLMjyJLBCXGhwnXKYJ"
          signatureMetadata:
            platformVersion: 5
            scheme: "EDDSA_ED25519_SHA512"
          partialMerkleTree: null
        - bytes: !!binary |-
            FO6BgtpIRD1ZdULm5Ec6u2An7vcQ34W3iC+EWRB0W8k14lmBWWs/JaXeendf5g1GjzeuXxnFLfk9\n6n4d0vlUDA==
          by: "GfHq2tTVk9z4eXgyRMW1yxrrbqC7nYgTD4gjgpePqcbN2B5zaTgm5UkstzB2"
          signatureMetadata:
            platformVersion: 5
            scheme: "EDDSA_ED25519_SHA512"
          partialMerkleTree: null

#### Exceptions

  * `ManualRecoveryException` - This exception will be thrown by the node initiating this flow for any of the following reasons:
* the `RecoveryRequest` does not exist,
* they are not the designated responder,
* the `RecoveryRequest` is not designated as being manual,
* or the `RecoveryRequest` is not in the state `Requested` (which it should be by default after running `InitiateManualRecoveryFlow`).
  * `VaultExporterException` - This will be thrown if there isn't a sufficient amount of disk space available to persist the `VaultArchive`. This exception   will also be thrown if any of the requested artifacts (transaction IDs, attachments or network parameters) do not exist in the vault.
  * `RecoveryRequestVerificationException` - This will be thrown by the responding node if the `RecoveryRequest` received from the initiating node includes transactions which they are not permitted to view.


### `ImportTransactionsFlow`

This flow fetches a `RecoveryRequest` with a specified ID from the database. The flow then conducts a series of verifications including checking the request is manual, is in progress, that you are requester and that contents of the vault archive match the related `RecoveryRequest`. It then attempts to import the data into the vault.

If the import fails, the flow will fail the recovery request. Otherwise, the request is marked as complete and recovery has been successfully facilitated with the counterparty.

This flow uses existing Corda mechanisms to import transaction data back into the vault. This means that recovered transactions will trigger the same events as "new" transactions. Applications subscribing to vault observable fields will receive duplicate updates. External systems relying on LedgerData are expected to be able to handle receipt of duplicated updates resulting from recovery processes.

{{< attention >}}

Importing transaction data triggers the same events as receipt of *new* transactions. This means the recorded time stamp of any *new* transactions will be the *new* time at which they were recorded, not the original time. This is expected behaviour. Nodes do not rely on subjective local time. The only source of truth with respect to time is a notary signature over a time window.

{{< /attention >}}

Applications subscribing to vault observable fields will receive duplicate updates. External systems relying on LedgerData are expected to be able to handle receipt of duplicated updates resulting from recovery processes.

This flow will also trigger a refresh of reconciliation statuses with all counterparties.

#### Parameters

* `requestId` - A `String` representing the `UUID` corresponding to the manual `RecoveryRequest` for which you will be importing a file containing transaction data (a `VaultArchive`).
* `path` - A `String` representing the file path of the `VaultArchive` from which you will import the requested data to node's vault.

#### Return type

* `Unit / Void` - None.

#### Command Line Interface

* `flow start ImportTransactionsFlow requestId: <UUID of RecoveryRequest>, path: <PATH_TO_DESIRED_VAULT_ARCHIVE_EXPORT>`
* Example: `flow start ImportTransactionsFlow requestId: "a5b3d634-9d34-47e8-9733-64db75115392", path: "/var/folders/vault_archives"`

#### Exceptions

  * `ManualRecoveryException` - This exception will be thrown by the node initiating this flow for any of the following reasons:
* the `RecoveryRequest` does not exist,
* they are not the designated requester,
* the `RecoveryRequest` is not designated as being manual,
* the `RecoveryRequest` is not in the state `Requested` (which it should be by default after running `InitiateManualRecoveryFlow`),
* or if the transaction IDs specified in the `RecoveryRequest` do not match the transaction ids specified in the `VaultArchive`.
  * `CorruptedArchiveException` - This will be thrown if the ID of a deserialized transaction doesn't match the name of the file in which it is provided.
  * `MissingArtifactsException` - This will be thrown if an artifact that was specified for recovery does not exist and is not included in the `VaultArchive`.

## Related database tables

The current state of a manual recovery request is stored in the `CR_RECOVERY_REQUEST` table, which is only present if the *LedgerRecover* CorDapp
has been installed. This table will capture all previously executed `RecoveryRequest`s and their outcomes as either `Failed` or `Completed`.

{{< note >}}
`RecoveryRequest`s and associated data are outside the scope of `LedgerRecover` as they are not vault data or vault related data. These tables should be backed up via synchronous or asynchronous replication if they are critical for regulators or other audit activities.
{{< /note >}}

## JMX metrics

A Corda node running the LedgerRecover CorDapp will expose the following metrics via JMX:

### `CurrentRecoveryRequestWithParty`

This is an endpoint exposed via JMX that returns the current `RecoveryRequest` related to a specific party.

#### Parameters

* `party` - A `String` representing the `X500Name` of the counterparty that is the subject of the query.
* `isRequester` - A boolean flag indicating whether or not the specified party was the initiator of the `RecoveryRequest`.

#### Return type

* `RecoveryRequest` - This endpoint returns a `RecoveryRequest`, which is an object containing all information pertaining to a given recovery.

### `RecoveryRequestsInTimeWindow`

This is an endpoint exposed via JMX that returns all current `RecoveryRequests` within a specified time window.

#### Parameters

* `isRequester` - A boolean flag indicating whether or not the specified party was the initiator of the `RecoveryRequest`.
* `timeStart` - A time stamp, represented as a `Long` data type indicated when the time window should begin for the purposes of querying.
* `timeEnd` - A time stamp, represented as a `Long` data type indicated when the time window should end for the purposes of querying.

#### Return type

* `Array<RecoveryRequest>` - This endpoint returns an array of `RecoveryRequest`s that took place during the specified time window.

### `FailedPartiesAsInitiator`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network with whom you have initiated a `RecoveryRequest` which has subsequently failed.

### `FailedPartiesAsRecipient`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network who have initiated or attempted to initiate a `RecoveryRequest` with us, which has subsequently failed.

### `InProgressPartiesAsInitiator`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network with whom you have initiated a `RecoveryRequest` that is currently in progress.

### `InProgressPartiesAsRecipient`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network who have initiated or a `RecoveryRequest` with us which is still in progress.

### `RequestedPartiesAsInitiator`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network with whom you have initiated a `RecoveryRequest` which has been persisted in an initial state with the status - `requested`.

### `RequestedPartiesAsRecipient`

This endpoint returns a list of `CordaX500Name`s as `String`s representing the identity of the nodes on the network who have attempted to initiate a `RecoveryRequest` with us which has been persisted in an initial state with the status - `requested`.

### `NumberOfFailedRecoveriesAsInitiator`

This endpoint returns the number of nodes on the network with whom you have initiated a `RecoveryRequest` which has subsequently failed.

### `NumberOfFailedRecoveriesAsRecipient`

This endpoint returns the number of nodes on the network who have initiated or attempted to initiate a `RecoveryRequest` with us, which has subsequently failed.

### `NumberOfInProgressRecoveriesAsInitiator`

This endpoint returns the number of nodes on the network with whom you have initiated a `RecoveryRequest` that is currently in progress.

### `NumberOfInProgressRecoveriesAsRecipient`

This endpoint returns the number of nodes on the network who have initiated or a `RecoveryRequest` with us which is still in progress.

### `NumberOfCompletedRecoveriesAsInitiator`

This endpoint returns the number of nodes on the network with whom you have initiated a `RecoveryRequest` that has been completed.

### `NumberOfCompletedRecoveriesAsRecipient`

This endpoint returns the number of nodes on the network who have initiated or a `RecoveryRequest` with us that has been completed.

### `NumberOfRequestedRecoveriesAsInitiator`

This endpoint returns the number of nodes on the network with whom you have initiated a `RecoveryRequest` which has been persisted in an
    initial state with the status - `requested`.

### `NumberOfRequestedRecoveriesAsRecipient`

This endpoint returns the number of nodes on the network who have attempted to initiate a `RecoveryRequest` with us which has been persisted
    in an initial state with the status - `requested`.

## Log messages

LedgerRecover manual recovery processes emit logging statements from the package `com.r3.dr.ledgerrecover.app.manual.flows`. Logging statements
generally provide information as to the progress of the flow in which they were made.

## Example workflow

In this section, you will walk through the complete execution of a manual recovery process. This workflow represents the **happy path** or the ideal steps and outcomes that will take place during recovery.

You can also see excerpts explicitly titled **unhappy path** that describe the scenarios in which a given step might fail, and what actions to take to get back onto the happy path.

### Scenario
In this scenario, we'll make the following assumptions:

* The actors, Parties A and B are on a two-party Corda network, comprised of their nodes and a notary.

* Both nodes are running Corda Enterprise and have both LedgerSync and LedgerRecovery installed.
*  Both nodes have backups of their vaults.
*  PartyA has experienced a disaster in which their vault became corrupt.
*  PartyA subsequently restored from the backup.
*  PartyA successfully completed reconciliation with PartyB which indicated that there were differences found between their vaults.
*  PartyA determined that the number of differences found was too large for regular operations and is now attempting a manual recovery process.

### Step 1. Initiate the manual recovery request

To kick off a manual recovery process, the initiating node should execute the `InitiateManualRecoveryFlow` using the following command.

`flow start InitiateManualRecoveryFlow party: "O=PartyB, L=London, C=GB"`

When run successfully, this flow will persist a `RecoveryRequest` in the `CR_RECOVERY_REQUEST` table of the both initiating and counterparty nodes based on the previously conducted reconciliation. Further operations described will update this record with the current progress. The following will be logged to the CRaSh shell. The node operator should take note of the `recoveryID` for future operations.

```
    RecoveryRequest(recoveryID=e769be7d-deb1-46dd-98fc-fe09e6e172b3, party=O=PartyB, L=London, C=GB, isRequester=true, timeStarted=1582643485140, timeFinished=null,
    requestedTransactionIDs=[4F2F2AFB66670C6F7A4BF0BA201609A70DE49C87C29C8C2ABB19CE55DF251F01, E6156EBA7EEB23802CF2B5D0FE53601B849F0EC0F0326B440957636D3B08E462,
    87391C19593CFEEC9F804921790388C869C38496B400522E7D23BD8BD3138494, 4A1C94374E8C27A3ED8760DF32F13ECA6FED464B9EF0C19CCB6C203B76101E06], recoveryStatusFlag=REQUESTED,
    failureReason='', isManual=true, stateMachineRunId=null)
```

#### Unhappy path - Exception is thrown by the initiating node

If the initiating node throws an exception, it is very likely for one of the following reasons:
- The reconciliation process is either still in progress or has failed. In the former situation, wait for the reconciliation process to be scheduled or complete. In the
latter situation, review the node logs to determine the cause of the reconciliation failure (see the logging section of [LedgerSync documentation](./ledger-sync.md)) and
then reschedule the reconciliation so that it may be completed successfully.

#### Unhappy path - Exception is thrown by the responding node

If the responding node throws an exception, a `RecoveryRequest` will have been created, persisted by the initiator and subsequently failed. The reason for the failure will be propagated back to the initiating node and recorded in the node logs. Review the node logs - the explanation for the failure should be prefaced by: `Manual Recovery Initialization has failed for the counterparty with the message:`.

The common reasons for this **unhappy path** are that the `RecoveryRequest` contained transactions that were invalid for recovery or that there was a `RecoveryRequest` already registered as being in progress by the counterparty with the identity of the initiator. In the first case, the node operator should restart the disaster recovery process by rescheduling reconciliation
with the counterparty. In the latter situation, the node operator of the initiating party should first check their node logs and then check the `CR_RECOVERY_REQUEST` table in their database to
determine if there is, in fact, another valid and current `RecoveryRequest`. If so, they should wait for the counterparty to continue with the process described herein. If not, they should
request that the counterparty use `FailManualRecoveryRequest` to invalidate the record so that the initiating party may create another valid `RecoveryRequest` and continue with the recovery process.

### Step 2. Export the transaction data

Based on the governing rules of the Corda network in which nodes are deployed, the node operator of the counterparty may be expected to be monitoring the exposed JMX endpoints so that they may understand when a valid `RecoveryRequest` has been initiated with them. Once a record of the `RecoveryRequest` has been successfully persisted on both the initiating and responding nodes (reflected via the monitored JMX attributes), the node operator of the responding party needs to create a `VaultArchive` containing all of the requested ledger data. They can do so using the following command:

`flow start ExportTransactionsFlow requestId: "e769be7d-deb1-46dd-98fc-fe09e6e172b3", path: "/var/folders/vault_archives"`

Once completed successfully, the `RecoveryRequest` record will be marked as complete on the responding node (the node on which the `ExportTransactionsFlow` flow was run).

Note that the `requestId` argument passed in the command above is the same as the one that was returned in step 1. The node operator can either be explicitly informed of this ID for convenience or they can query their `CR_RECOVERY_REQUEST` table for `RecoveryRequest` records with the initiator and retrieve the request ID. Querying can be done using `GetRecoveryRequestsFlow` which returns a `List` of `RecoveryRequest` objects based on the counterparty and a target list of `RecoveryStatusFlags`.

#### Unhappy path - Exception is thrown by the node executing this flow

Exceptions thrown in this stage are related to one of two things. Either the `RecoveryRequest` was invalid, in which case it should be:
1. Immediately rejected and failed or,
2. The node did not have sufficient disk space to persist the generated `VaultArchive`.

In the first case, there is no further action required by the node operator. They may optionally inform the requesting counterparty that their `RecoveryRequest`
referenced transaction data that was invalid and they may have to restart the disaster recovery process. In the second case, the node operator will need to make more disk space available before reattempting the export.

### Step 3. Transmit the vault archive

{{< warning >}}
This step is entirely off ledger. It's important to recognize that the exported `VaultArchive` contains highly sensitive transaction data representing the *private* ledger data shared between two counterparties.
{{< /warning >}}

Corda does not attempt to solve the problem of securely and privately transmitting large file payloads - operating business entities should follow their internal best practices as well as any guidelines defined by the network or business network in determining the appropriate vehicle for delivery of the `VaultArchive` with the counterparty.

### Step 4. Import the transaction data

This is the final step in the **happy path** for manual ledger recovery. In this step, it is assumed that the initiating node has received a copy of the `VaultArchive` which is now stored in a known location
accessible via the Corda node. The initiating party should run `ImportTransactionsFlow` to read the `VaultArchive` data and load it into the vault using the following command:

`flow start ImportTransactionsFlow requestId: "e769be7d-deb1-46dd-98fc-fe09e6e172b3", path: "/var/folders/vault_archives`

{{< note >}}
The path must be adjusted to reflect where the `VaultArchive` is saved on the responding node's filesystem.
{{< /note >}}

When run successfully the initiating node should have successfully recovered their vault and be able to transact with the counterparty with whom they were recovering. `ReconciliationStatus` will be refreshed
automatically after a successful import.

##### Unhappy path - Exception is thrown by the node executing this flow

Exceptions in this step stem from the `VaultArchive` being invalid or not corresponding to the `RecoveryRequest` with the counterparty. In this case, it is likely that the counterparty delivered the wrong `VaultArchive`
file for import. The action here would be to inform the counterparty of the invalid `VaultArchive` and request that they export and deliver the file once more. In order for an import to be successful, the `RecoveryRequest`
must also be in progress - if this is not the case (that is, the `RecoveryRequest` was erroneously failed prior to import), then the manual recovery process will have to be restarted on the basis of the last successful
reconciliation. It is expected that after importing the `VaultArchive`, the node operator will verify that the refreshed `ReconciliationStatus` record now indicates there are no differences found with the counterparty.
