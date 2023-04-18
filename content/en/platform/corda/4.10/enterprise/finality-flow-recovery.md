---
date: '2023-03-30T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-cordapps-flows
tags:
- flow
- two
- phase
- finality
- recovery
title: Finality Flow Recovery
weight: 45
---

# Finality Flow Recovery

[Two Phase Finality](two-phase-finality.md) introduces recovery metadata and a new transaction status of `MISSING_NOTARY_SIG`
to denote that a transaction has not yet been fully finalised. The protocol stores the additional flow transaction recovery metadata
upon initially recording an un-notarised transaction. This metadata is used to enable **initiator** and **receiver** recovery
should a flow fail at some point within the finality protocol.

Specifically, the `FinalityFlow` initiator stores:

- Corda X500 name of **initiator** party
- list of Corda X500 names of **other parties** we share the transaction with (these include participants on the transaction contract
  plus any additional sessions passed into FinalityFlow, such as **observer** nodes)
- `StatesToRecord` status (defaulting to `ONLY_RELEVANT`). Recall, this determines whether states are recorded in the vault for a node.

The `ReceiveFinalityFlow` receiver stores:

- Corda X500 name of initiator party
- `StatesToRecord`

The initiator of a `FinalityFlow` transaction will store all the above recovery metadata locally. The list of participants
is not shared across the network and is private only to the initiator.
The receiver of a shared `FinalityFlow` transaction will only receive and record who the initiator is and the `StatesToRecord` status.

A Finality flow transaction is recoverable when its transaction status is `MISSING_NOTARY_SIG`.
This could be at either or both of the Initiator and Receiver(s) sides, depending on how far the finality protocol progressed
before failure at a given participant:

- if the initiator reached a point whereby the transaction was successfully notarised, then recovery can be executed at
  either or both initiator and receiver sides:
    - where the initiator triggers recovery first, it will not be necessary for the receiver to perform the same.
    - where the receiver triggers recovery first, then the initiator must also follow (only if it also failed after the
      notarisation step).
- if notarisation hasn't yet taken place then recovery must be triggered from the initiator side only.
- if the initiator of a transaction successfully notarised and finalised, it is possible to trigger recovery of failed peers
  by triggering recovery on the initiator side and specifying the transaction id to recover.

{{< warning >}}

Finality flow failure typically leads to temporal ledger inconsistency.
The following scenarios are possible with Two Phase Finality:
- Initiator completes successfully and races ahead to use any output states from a previously finalised transaction
  before receivers of the original transaction have finalised (or failed prior to finalisation).
- Receiver completes successfully before Initiator completes finalisation (i.e. this may happen after the initiator
  successfully sends notary signature to the receiver(s) but then fails prior to finalising its own transaction).

{{< /warning >}}

The state machine enables you to recover finality flows that are in a `FAILED` checkpoint flow status.
An optional `force-recover` flag also forces recovery of any finality flows that are in a `RUNNABLE`, `PAUSED` or `HOSPITALIZED`
checkpoint flow status.

{{< note >}}
`PAUSED` and `HOSPITALIZED` flows are automatically retried on node startup and may thus recover without the need for
manual intervention.
{{< /note >}}

## How to recover finality flows

You can recover a finality flow by using any of the following methods:
- the extensions `FlowRPCOps` RPC API.
- node shell commands
- directly invoking the recovery flows (either from the Node Shell or programmatically within a CorDapp):

```kotlin
net.corda.node.internal.recovery.FinalityRecoveryFlow
net.corda.node.internal.recovery.FinalityPeerRecoveryFlow
```

### Recovering finality flows using the extensions `FlowRPCOps` RPC API.

The `FlowRPCOps` API exposes the following recovery operations:

```kotlin
    /**
     * Recover a failed finality flow by id.
     * [forceRecover] will attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
     *
     * @return whether the flow was successfully recovered.
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
     *  TransactionStatus.MISSING_NOTARY_SIG
     * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
     *
     * @return map of identified failed flows and whether they were successfully recovered.
     */
    fun recoverAllFinalityFlows(forceRecover: Boolean = false): Map<StateMachineRunId, Boolean>

    /**
     * Recover a failed finality flow by transaction id.
     * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
     *
     * @return whether the flow was successfully recovered.
     */
    fun recoverFinalityFlowByTxnId(txnId: SecureHash, forceRecover: Boolean = false): Boolean

    /**
     * Recover a specified set of failed finality flows by transaction id.
     * [forceRecover] will also attempt to recover flows which are in a RUNNABLE, PAUSED or HOSPITALIZED state.
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

There operations are useful for identifying failed finality flows and return flow transaction information including the
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
Finality Flow recovery requires that your Corda Network has a Minimum Platform Version of 4 as the `TransactionNotarisationCheckFlow`
used internally by `FinalityPeerRecoveryFlow` uses [reference states](key-concepts-transactions.html#reference-states).

{{< /warning >}}

### Recovering finality flows from the shell

The following examples show the different ways to use the finality flow query and recovery commands.

To check the status of a flow as a `FinalityFlow` initiator:

```bash
flowStatus queryFinalityById e0d781be-b4ab-43e0-b694-e97cc4eaa6ee

FlowTransactionInfo(stateMachineRunId=[e0d781be-b4ab-43e0-b694-e97cc4eaa6ee], txId=19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F, status=MISSING_NOTARY_SIG, timestamp=2023-03-29T11:16:29.477Z, initiator=O=Alice Corp, L=Madrid, C=ES, peers=[O=Bob Plc, L=Rome, C=IT])
---
- stateMachineRunId:
    uuid: "e0d781be-b4ab-43e0-b694-e97cc4eaa6ee"
  txId: "19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F"
  status: "MISSING_NOTARY_SIG"
  initiator:
    x500Principal:
      name: "O=Alice Corp,L=Madrid,C=ES"
  peers:
    x500Principal:
      name: "O=Bob Plc,L=Rome,C=IT"
```
Note:
- `initiator` refers to myself as caller of the command.
- `peers` field contains the other participants' distribution list.


We could also have performed the same check by specifying a transaction id.
This is commonly the case when recovering from a receiver perspective (as an initiator flow id is meaningless outside its own node).

```bash
flowStatus queryFinalityByTxnId 19BE64484D3CBF532A8FB2ACA1AEACA38B1FBA3C38B0518B7F5316AC9E79432F
```

To check the status of a flow transaction as a `ReceiveFinalityFlow` receiver:

```bash
flowStatus queryFinalityByTxnId 7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4

FlowTransactionInfo(stateMachineRunId=[8cc13ed6-ea14-43e6-a7b0-85a61fb3bbb1], txId=7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4, status=MISSING_NOTARY_SIG, timestamp=2023-03-29T12:40:23.628Z, initiator=O=Alice Corp, L=Madrid, C=ES, peers=null)
---
- stateMachineRunId:
    uuid: "8cc13ed6-ea14-43e6-a7b0-85a61fb3bbb1"
  txId: "7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4"
  status: "MISSING_NOTARY_SIG"
  initiator:
    x500Principal:
      name: "O=Alice Corp,L=Madrid,C=ES"
  peers: null
```

Note:
- `initiator` refers to the party that initiated the `FinalityFlow`
- `peers` field is **null** (this information is private to the initiator only)

To recover a failed finality flow by flow id:

```bash
flow recoverFinality 821884be-8e9f-486d-8228-70d97e215218
Recovered finality flow [821884be-8e9f-486d-8228-70d97e215218]
```

Should recovery fail, you will see the following response:

```bash
Failed to recover finality flow 821884be-8e9f-486d-8228-70d97e215218
```

Further information explaining why a flow failed to recover can be found in the node logs.
A prime example is attempting to recover a flow that has already completed successsfuly.
The node logs will show the following message:

```bash
Recovery not possible for transaction with status VERIFIED
```

To recover a failed finality flow by transaction id:

```bash
flow recoverFinalityByTxnId 7E7EE31CA6371D73CDDB1A7992E239CE222606EA845F1ABC87995898017904A4
Recovered finality flow [821884be-8e9f-486d-8228-70d97e215218]
```
Should recovery fail, you will see the following response:

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

Note, this operation returns a list of flow identifier / Boolean (success / failure) pairs.
In all other cases, the shell prints a message stating if the operation succeeded or not.

To recover all failed finality flows including those in a PAUSED or HOSPITALIZED checkpoint state:

```bash
flow recoverAllFinality --force-recovery
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

### Recovering Finality flows from RPC

To pause and retry flows from an RPC Client using the extensions RPC Interface (`FlowRPC`), use the Multi RPC Client - `MultiRPCClient`.

{{< note >}}
For more information about `MultiRPCClient`, see [Interacting with a node](node/operating/clientrpc.html#building-the-multi-rpc-client).
{{< /note >}}

First instantiate a `MultiRPCClient` for `FlowRPC` (this differs from the standard non-extensions RPC interface):

```kotlin
val username = "testuser"
val password = "password"
val rpcHostAndPort = NetworkHostAndPort("localhost", 10006)
val flowClient = MultiRPCClient(rpcHostAndPort, FlowRPCOps::class.java, username, password).start().getOrThrow()
```

To recover a single finality flow by id, call `recoverFinalityFlow`:

```kotlin
val status = flowClient.proxy.recoverFinalityFlow(flowHandle.id)
```

This method will return a **status** of `true` if the operation was successful, or `false` otherwise.

To recover multiple finality flow(s) by id, call `recoverFinalityFlows`:

```kotlin
val resultMap = flowClient.proxy.recoverFinalityFlows(setOf(flowHandle1.id, flowHandle2.id))
```

This method will return a **resultMap** (`Map<StateMachineRunId, Boolean>`) consisting of a collection of flow identifier / Boolean (success / failure) entries.

To recover a single finality flow which has been HOSPITALIZED or PAUSED we may use the **force recovery flag**, as follows:

```kotlin
val status = flowClient.proxy.recoverFinalityFlow(flowHandle.id, forceRecover = true)
```

{{< note >}}
It is a common scenario for a `ReceiveFinalityFlow` receiver to be put into a hospitalized state should the
`FinalityFlow` initiator fail at certain specific points in the protocol.
{{< /note >}}

To recover a single finality flow by transaction id, call `recoverFinalityFlowByTxnId`:

```kotlin
val status = flowClient.proxy.recoverFinalityFlowByTxnId(stx.id)
```

To recover multiple finality flow(s) by transaction id, call `recoverFinalityFlowByTxnIds`:

```kotlin
val resultMap = flowClient.proxy.recoverFinalityFlowByTxnIds(setOf(stx1.id, stx2,id))
```

To recover all finality flow(s), call `recoverAllFinalityFlows`:

```kotlin
val resultMap = flowClient.proxy.recoverAllFinalityFlows()
```

To recover all finality flow(s) for a given timeframe using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
                        FlowRecoveryQuery(timeframe = FlowTimeWindow(
                                fromTime = startTime,
                                untilTime = endTime
                        )))

```

To recover all finality flow(s) initiated by Charlie using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
                        FlowRecoveryQuery(initiatedBy = CHARLIE_NAME))
```

To recover all finality flow(s) with Charlie as peer using a matching criteria, call `recoverFinalityFlowsMatching`:

```kotlin
val resultMap = flowRPC.proxy.recoverFinalityFlowsMatching(
                        FlowRecoveryQuery(counterParties = listOf(CHARLIE_NAME)))
```

To prevent server-side resource leakage, use `flowClient.close()` to close `flowClient` when finished.

### Querying Finality flows from RPC

Instantiate a `MultiRPCClient` for `NodeFlowStatusRpcOps` as follows:

```kotlin
val username = "testuser"
val password = "password"
val rpcHostAndPort = NetworkHostAndPort("localhost", 10006)
val flowClient = MultiRPCClient(rpcHostAndPort, NodeFlowStatusRpcOps::class.java, username, password).start().getOrThrow()
```

To query a flow transaction by flow id, call `getFlowTransaction`:

```kotlin
val flowInfo = flowClient.proxy.getFlowTransaction(flowHandle.id)
```

Similarly, to query a flow transaction by transaction id, call `getFlowTransactionByTxnId`:

```kotlin
val flowInfo = flowClient.proxy.getFlowTransactionByTxnId(txnId)
```

Both these methods will return a **FlowTransactionInfo** object if the flow transaction exists.

#### Implementation ####

Finality flow recovery uses a suite of internal flows which implement similar functionality to the actual `FinalityFlow`
and `ReceiveFinalityFlow`. These internal flows are:

```kotlin
net.corda.node.internal.recovery.FinalityRecoveryFlow
net.corda.node.internal.recovery.FinalityPeerRecoveryFlow
net.corda.node.internal.recovery.TransactionNotarisationCheckFlow
```

`TransactionNotarisationCheckFlow` is a helper flow used by the `FinalityPeerRecoveryFlow` that determines whether
a [SignedTransaction] has been previously notarised.

It builds a new transaction that has
 - a single input from the original [SignedTransaction] as a reference state.
   Reference states cannot be spent and are thus never recorded by the notary upon a notarisation check.
 - a dummy [RecoveryContract] to simulate creation of a new output and command.
Upon attempting to notarise this new dummy transaction, the flow can determine whether the inputs were previously spent
based on the information reported by a [NotaryError.Conflict] exception.

