---
date: '2023-03-30T12:00:00Z'
menu:
  corda-enterprise-4.14:
    parent: corda-enterprise-4.14-cordapps-flows
tags:
- flow
- two
- phase
- finality
- recovery
title: Finality flow recovery
weight: 45
---

# Finality flow recovery

[Two Phase Finality]({{< relref "two-phase-finality.md" >}}) introduces recovery metadata and a new transaction status of `IN_FLIGHT` to denote that a transaction has not yet been fully finalized. The protocol stores the additional flow transaction recovery metadata upon initially recording an unnotarized transaction. This metadata is used to enable **initiator** and **receiver** recovery should a flow fail at some point within the finality protocol.

Specifically, the `FinalityFlow` initiator stores:

* The Corda X.500 name of the **initiator** party.
* The list of Corda X.500 names of the **other parties** the initiator shares the transaction with. These include participants on the transaction contract, plus any additional sessions passed into `FinalityFlow`, such as **observer** nodes.
* The `StatesToRecord` status (the default value is `ONLY_RELEVANT`). This status determines if states are recorded in the vault for a node.

The `ReceiveFinalityFlow` receiver stores:

* The Corda X.500 name of the initiator party.
* The `StatesToRecord` status (described above).

The initiator of a `FinalityFlow` transaction stores all of the above recovery metadata locally. The list of participants
is not shared across the network, and is private only to the initiator.

The receiver of a shared `FinalityFlow` transaction only receives and records who the initiator is and the `StatesToRecord` status.

A finality flow transaction is recoverable when its transaction status is `IN_FLIGHT`. This could be at either or both of the initiator and receiver(s) sides, depending on how far the finality protocol progressed before failure at a given participant:

* If the initiator reached a point whereby the transaction was successfully notarized, then recovery can be executed at either, or both, the initiator and receiver sides:
  * If the initiator triggers recovery first, it is not necessary for the receiver to perform the same.
  * If the receiver triggers recovery first, then the initiator must also follow (only if it also failed after the notarization step).
* If notarization has not yet taken place, then recovery must be triggered from the initiator side only.
* If the initiator of a transaction successfully notarized and finalized, it is possible to trigger recovery of failed peers by triggering recovery on the initiator side and specifying the transaction ID to recover.

{{< warning >}}
Finality flow failure typically leads to temporal ledger inconsistency. The following scenarios are possible with Two Phase Finality:
* The initiator completes successfully and races ahead to use any output states from a previously finalized transaction before receivers of the original transaction have finalized (or failed prior to finalization).
* The receiver completes successfully before the initiator completes finalization. This may happen after the initiator successfully sends the notary signature to the receiver(s) but then fails prior to finalizing its own transaction.
{{< /warning >}}

The state machine enables you to recover finality flows that are in a `FAILED` checkpoint flow status. An optional `force-recover` flag also forces recovery of any finality flows that are in a `RUNNABLE`, `PAUSED`, or `HOSPITALIZED` checkpoint flow status.

{{< note >}}
`PAUSED` and `HOSPITALIZED` flows are automatically retried on node startup, and so may recover without the need for  {{< /note >}}

### Issuance transactions with observers

Transactions that do not require notarization (for example, issuance) also store recovery metadata such that any observers to
an issuance transaction may also be recovered. That is, should an issuance transaction fail to broadcast the transaction
to an observer peer, it is possible to invoke the recovery flow at the initiator to ensure the transaction is correctly
re-distributed to that observer peer.

{{< note >}}
For the purpose of performance optimization, issuance transactions are not intermediately stored with an `IN_FLIGHT` status.
All recovery metadata is directly stored as part of initiator finalization with a status of 'VERIFIED`.
{{< /note >}}

## Recovering finality flows

You can recover a finality flow by using any of the following methods:

* The extensions `FlowRPCOps` RPC API
* Node shell commands
* Directly invoking the recovery flow, either from the Node Shell or programmatically within a CorDapp

```kotlin
net.corda.node.internal.recovery.FinalityRecoveryFlow
```

All recovery operations return the following:

*  **true** if a transaction is successfully recovered.
*  **false** if a transaction does not require recovery.
*  **FlowRecoveryException** if there is an error whilst performing recovery.

### Recovering finality flows using the extensions `FlowRPCOps` RPC API

The `FlowRPCOps` API exposes the following recovery operations:

```kotlin
/**
 * Recover a failed finality flow by id.
 * [forceRecover] will attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 *
 * @return
 *   true if a transaction is successfully recovered
 *   false if a transaction does not require recovery
 *
 * @throws [FlowRecoveryException] if there is an error whilst performing recovery
 */
fun recoverFinalityFlow(id: StateMachineRunId, forceRecover: Boolean = false): Boolean

/**
 * Recover a specified set of failed finality flows by id.
 * [forceRecover] will attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 *
 * @return map of identified failed flows and whether they were successfully recovered.
 */
fun recoverFinalityFlows(ids: Set<StateMachineRunId>, forceRecover: Boolean = false): Map<StateMachineRunId, Boolean>

/**
 * Recover all failed finality flows as determined by associated status.
 * Specifically,
 *  FlowState.FAILED
 *  TransactionStatus.IN_FLIGHT
 * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 *
 * @return map of identified failed flows and whether they were successfully recovered.
 */
fun recoverAllFinalityFlows(forceRecover: Boolean = false): Map<StateMachineRunId, Boolean>

/**
 * Recover a failed finality flow by transaction id.
 * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 * This operation will attempt to recovery failed peers if the initiator-side of the transaction completed successfully.
 *
 * @return
 *   true if a transaction is successfully recovered
 *   false if a transaction does not require recovery
 *
 * @throws [FlowRecoveryException] if there is an error whilst performing recovery
 */
fun recoverFinalityFlowByTxnId(txnId: SecureHash, forceRecover: Boolean = false): Boolean

/**
 * Recover a specified set of failed finality flows by transaction id.
 * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 * This operation will attempt to recovery failed peers if the initiator-side of the transaction completed successfully.
 *
 * @return map of identified failed transactions and whether they were successfully recovered.
 */
fun recoverFinalityFlowByTxnIds(txnIds: Set<SecureHash>, forceRecover: Boolean = false): Map<SecureHash, Boolean>

/**
 * Recover flows matching the specified query criteria.
 * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
 *
 * @return map of identified failed flows and whether they were successfully recovered.
 */
fun recoverFinalityFlowsMatching(query: FlowRecoveryQuery, forceRecover: Boolean = false): Map<StateMachineRunId, Boolean>

```

For the latter operation, `FlowRecoveryQuery` criteria defines the following:

```kotlin
data class FlowRecoveryQuery(
    val timeframe: FlowTimeWindow? = null,
    val initiatedBy: CordaX500Name? = null,
    val counterParties: List<CordaX500Name>?  = null)

data class FlowTimeWindow(val fromTime: Instant? = null, val untilTime: Instant? = null)
```

In addition to the recovery operations, the following flow status operations (and associated Node Shell commands) have
been added to the `NodeFlowStatusRpcOps` extension RPC API:

```kotlin
/**
 * @param flowId the flowId to return information for
 * @return FlowTransaction object describing flow transaction details.
 */
@RpcPermissionGroup(READ_ONLY)
fun getFlowTransaction(flowId: String): FlowTransactionInfo?

/**
 * @param txnId the transaction to return information for
 * @return FlowTransaction object describing flow transaction details.
 */
@RpcPermissionGroup(READ_ONLY)
fun getFlowTransactionByTxnId(txnId: String): FlowTransactionInfo?
```

There operations are useful for identifying failed finality flows, and return flow transaction information including the
additional recovery metadata:

```kotlin
data class FlowTransactionInfo(
    val stateMachineRunId: StateMachineRunId,
    val txId: String,
    val status: TransactionStatus,
    val timestamp: Instant,
    val initiator: CordaX500Name? = null,
    val peers: Set<CordaX500Name>? = null
)
```

{{< warning >}}
Finality flow recovery requires that your Corda network has a minimum platform version of 4, as the `TransactionnotarizationCheckFlow`
used internally by `FinalityPeerRecoveryFlow` uses [reference states]({{< relref "key-concepts-transactions.md#reference-states" >}}).

{{< /warning >}}

### Recovering finality flows from the shell

The following examples show the different ways to use the finality flow query and recovery commands.

To check the status of a flow as a `FinalityFlow` initiator:

```bash
flowStatus queryFinalityById e0d781be-b4ab-43e0-b694-e97cc4eaa6ee

FlowTransactionInfo(stateMachineRunId=[e0d781be-b4ab-43e0-b694-e97cc4eaa6ee], txId=19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F, status=IN_FLIGHT, timestamp=2023-03-29T11:16:29.477Z, initiator=O=Alice Corp, L=Madrid, C=ES, peers=[O=Bob Plc, L=Rome, C=IT])
---
- stateMachineRunId:
    uuid: "e0d781be-b4ab-43e0-b694-e97cc4eaa6ee"
  txId: "19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F"
  status: "IN_FLIGHT"
  initiator:
    x500Principal:
      name: "O=Alice Corp,L=Madrid,C=ES"
  peers:
    x500Principal:
      name: "O=Bob Plc,L=Rome,C=IT"
```
{{< note >}}
* The `initiator` field is the initiator of the command.
* The `peers` field contains the other participants' distribution list.
{{< /note >}}

You can also perform the same check by specifying a transaction ID.  This is commonly the case when recovering from a receiver perspective (as an initiator flow ID is meaningless outside its own node).

```bash
flowStatus queryFinalityByTxnId 19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F
```

To check the status of a flow transaction as a `ReceiveFinalityFlow` receiver:

```bash
flowStatus queryFinalityByTxnId 7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4

FlowTransactionInfo(stateMachineRunId=[8cc13ed6-ea14-43e6-a7b0-85a61fb3bbb1], txId=7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4, status=IN_FLIGHT, timestamp=2023-03-29T12:40:23.628Z, initiator=O=Alice Corp, L=Madrid, C=ES, peers=null)
---
- stateMachineRunId:
    uuid: "8cc13ed6-ea14-43e6-a7b0-85a61fb3bbb1"
  txId: "7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4"
  status: "IN_FLIGHT"
  initiator:
    x500Principal:
      name: "O=Alice Corp,L=Madrid,C=ES"
  peers: null
```

{{< note >}}
* `initiator` refers to the party that initiated the `FinalityFlow`.
* `peers` field is **null**: this information is private to the initiator only.
{{< /note >}}

To recover a failed finality flow using the flow ID:

```bash
flow recoverFinality 821884be-8e9f-486d-8228-70d97e215218
Recovered finality flow [821884be-8e9f-486d-8228-70d97e215218]
```

Should recovery fail, you will see the following response:

```bash
Failed to recover finality flow 821884be-8e9f-486d-8228-70d97e215218
```

Further information explaining why a flow failed to recover can be found in the node logs.
A prime example is attempting to recover a flow that has already completed successfully.
The node logs show the following message:

```bash
Recovery not possible for transaction with status VERIFIED
```

To recover a failed finality flow by using the transaction ID:

```bash
flow recoverFinalityByTxnId 7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4
Recovered finality flow [821884be-8e9f-486d-8228-70d97e215218]
```
Should recovery fail, you see the following response:

```bash
Failed to recover finality flow 7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4
```

After successfully recovering a finality flow, the flow transaction status should move to `VERIFIED`.

To recover all failed finality flows in one operation:

```bash
flow recoverAllFinality
Recovered finality flow(s)
Results: [[4cbfa031-90de-4564-a375-30141a18bbba]=true]
```

{{< note >}}
This operation returns a list of flow identifier/Boolean (success/failure) pairs.
In all other cases, the shell prints a message stating if the operation succeeded or not.
{{< /note >}}

To recover all failed finality flows, including those in a `PAUSED` or `HOSPITALIZED` checkpoint state:

```bash
flow recoverAllFinality --force-recover
Recovered finality flow(s)
Results: [[358a7b4e-074a-4da8-b6d7-64f1d923f9a8]=true, [c3cf2d33-6a36-4266-a9cb-f488ac3194cc]=true]
```

To recover finality flows using a custom query:

```bash
flow recoverFinalityMatching \
    flowStartFromTime: "2023-12-04T10:15:30.00", \
    flowStartUntilTime: "2023-12-05T10:15:30.00Z", \
    initiatedBy: "O=PartyA,L=London,C=GB", \
    counterParties: ["O=PartyA,L=London,C=GB", "O=PartyB,L=London,C=GB"]
```
Note, at least one custom criteria option must be specified.

### Recovering finality flows from RPC

To pause and retry flows from an RPC Client using the extensions RPC Interface (`FlowRPC`), use the Multi RPC Client - `MultiRPCClient`.

{{< note >}}
For more information about `MultiRPCClient`, see [Interacting with a node: Building the Multi RPC Client ]({{< relref "node/operating/clientrpc.md#building-the-multi-rpc-client" >}}).
{{< /note >}}

First, instantiate a `MultiRPCClient` for `FlowRPC` (this differs from the standard non-extensions RPC interface):

```kotlin
val username = "testuser"
val password = "password"
val rpcHostAndPort = NetworkHostAndPort("localhost", 10006)
val flowClient = MultiRPCClient(rpcHostAndPort, FlowRPCOps::class.java, username, password).start().getOrThrow()
```

To recover a single finality flow by ID, call `recoverFinalityFlow`:

```kotlin
val status = flowClient.proxy.recoverFinalityFlow(flowHandle.id)
```

This method returns a **status** of `true` if the operation was successful, or `false` otherwise.

To recover multiple finality flows by ID, call `recoverFinalityFlows`:

```kotlin
val resultMap = flowClient.proxy.recoverFinalityFlows(setOf(flowHandle1.id, flowHandle2.id))
```

This method returns a **resultMap** (`Map<StateMachineRunId, Boolean>`), consisting of a collection of flow identifier/Boolean (success/failure) entries.

To recover a single finality flow which has been `HOSPITALIZED` or `PAUSED`, use the **force recovery flag**, as follows:

```kotlin
val status = flowClient.proxy.recoverFinalityFlow(flowHandle.id, forceRecover = true)
```

{{< note >}}
It is a common scenario for a `ReceiveFinalityFlow` receiver to be put into a hospitalized state should the
`FinalityFlow` initiator fail at certain specific points in the protocol.
{{< /note >}}

To recover a single finality flow by transaction ID, call `recoverFinalityFlowByTxnId`:

```kotlin
val status = flowClient.proxy.recoverFinalityFlowByTxnId(stx.id)
```

To recover multiple finality flows by transaction ID, call `recoverFinalityFlowByTxnIds`:

```kotlin
val resultMap = flowClient.proxy.recoverFinalityFlowByTxnIds(setOf(stx1.id, stx2,id))
```

To recover all finality flows, call `recoverAllFinalityFlows`:

```kotlin
val resultMap = flowClient.proxy.recoverAllFinalityFlows()
```

To recover all finality flows for a given timeframe using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
    FlowRecoveryQuery(timeframe = FlowTimeWindow(
        fromTime = startTime,
        untilTime = endTime
        )
    )
)
```

To recover all finality flows initiated by Charlie using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
    FlowRecoveryQuery(initiatedBy = CHARLIE_NAME))
```

To recover all finality flows with Charlie as peer using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
    FlowRecoveryQuery(counterParties = listOf(CHARLIE_NAME)))
```

To prevent server-side resource leakage, use `flowClient.close()` to close `flowClient` when finished.

### Querying finality flows from RPC

Instantiate a `MultiRPCClient` for `NodeFlowStatusRpcOps` as follows:

```kotlin
val username = "testuser"
val password = "password"
val rpcHostAndPort = NetworkHostAndPort("localhost", 10006)
val flowClient = MultiRPCClient(rpcHostAndPort, NodeFlowStatusRpcOps::class.java, username, password).start().getOrThrow()
```

To query a flow transaction by flow ID, call `getFlowTransaction`:

```kotlin
val flowInfo = flowClient.proxy.getFlowTransaction(flowHandle.id)
```

Similarly, to query a flow transaction by transaction ID, call `getFlowTransactionByTxnId`:

```kotlin
val flowInfo = flowClient.proxy.getFlowTransactionByTxnId(txnId)
```

Both these methods return a **FlowTransactionInfo** object if the flow transaction exists.

#### Implementation

`FinalityRecoveryFlow` is the primary flow that orchestrates recovery by identifying whether initiator or peer recovery
is required according to the flow transaction recovery metadata.

Where this flow is called from a node that is:
* An initiator to a transaction, then the subflow `FinalityInitiatorRecoveryFlow` is called.
* A peer to a transaction, then the subflow `FinalityPeerRecoveryFlow` is called.

Finality flow recovery uses a suite of internal flows which implement similar functionality to the actual `FinalityFlow`
and `ReceiveFinalityFlow`. These internal flows are:

```kotlin
net.corda.node.internal.recovery.FinalityInitiatorRecoveryFlow
net.corda.node.internal.recovery.FinalityPeerRecoveryFlow
net.corda.node.internal.recovery.TransactionnotarizationCheckFlow
```

`TransactionnotarizationCheckFlow` is a helper flow used by the `FinalityPeerRecoveryFlow` that determines whether
a `SignedTransaction` has been previously notarized.

It builds a new transaction that has:
* A single input from the original `SignedTransaction` as a reference state. Reference states cannot be spent and are thus never recorded by the notary upon a notarization check.
* A dummy `RecoveryContract`, to simulate creation of a new output and command.

Upon attempting to notarize this new dummy transaction, the flow can determine whether the inputs were previously spent
based on the information reported by a `NotaryError.Conflict` exception.

