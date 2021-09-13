---
aliases:
- /head/contributing-flow-state-machines.html
- /HEAD/contributing-flow-state-machines.html
- /contributing-flow-state-machines.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-contributing-flow-state-machines
    parent: corda-os-4-5-contributing-index
    weight: 1090
tags:
- contributing
- flow
- state
- machines
title: Extending the state machine
---




# Extending the state machine

This article explains how to extend the state machine code that underlies flow execution. It is intended for Corda
contributors.


## How to add suspending operations

To add a suspending operation for a simple request-response type function that perhaps involves some external IO we can
use `FlowExternalOperation` or `FlowExternalAsyncOperation`. These interfaces represent the public versions of the internal
`FlowAsyncOperation`.

See [calling external systems inside of flows](api-flows.md#api-flows-external-operations) for more information on these public interfaces.


## How to test

The recommended way to test flows and the state machine is using the Driver DSL. This ensures that you will test your
flow with a full node.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
    @Test(timeout=300_000)
	fun summingWorks() {
        driver(DriverParameters(startNodesInProcess = true, cordappsForAllNodes = listOf(cordappWithPackages("net.corda.docs.kotlin.tutorial.flowstatemachines")))) {
            val aliceUser = User("aliceUser", "testPassword1", permissions = setOf(Permissions.all()))
            val alice = startNode(providedName = ALICE_NAME, rpcUsers = listOf(aliceUser)).getOrThrow()
            val aliceClient = CordaRPCClient(alice.rpcAddress)
            val aliceProxy = aliceClient.start("aliceUser", "testPassword1").proxy
            val answer = aliceProxy.startFlow(::ExampleSummingFlow).returnValue.getOrThrow()
            assertEquals(3, answer)
        }
    }

```
{{% /tab %}}



{{% tab name="java" %}}
```java
    @Test
    public void summingWorks() {
        driver(new DriverParameters(singletonList(cordappWithPackages("net.corda.docs.java.tutorial.flowstatemachines"))), (DriverDSL dsl) -> {
            User aliceUser = new User("aliceUser", "testPassword1", singleton(Permissions.all()));
            Future<NodeHandle> aliceFuture = dsl.startNode(new NodeParameters()
                    .withProvidedName(ALICE_NAME)
                    .withRpcUsers(singletonList(aliceUser))
            );
            NodeHandle alice = KotlinUtilsKt.getOrThrow(aliceFuture, null);
            CordaRPCClient aliceClient = new CordaRPCClient(alice.getRpcAddress());
            CordaRPCOps aliceProxy = aliceClient.start("aliceUser", "testPassword1").getProxy();
            Future<Integer> answerFuture = aliceProxy.startFlowDynamic(ExampleSummingFlow.class).getReturnValue();
            int answer = KotlinUtilsKt.getOrThrow(answerFuture, null);
            assertEquals(3, answer);
            return null;
        });
    }

```
{{% /tab %}}

{{< /tabs >}}

The above will spin up a node and run our example flow.


## How to debug issues

Let’s assume we made a mistake in our summing operation:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
class SummingOperationThrowing(val a: Int, val b: Int) : FlowExternalAsyncOperation<Int> {
    override fun execute(deduplicationId: String): CompletableFuture<Int> {
        throw IllegalStateException("You shouldn't be calling me")
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
public final class SummingOperationThrowing implements FlowAsyncOperation<Integer> {
    private final int a;
    private final int b;

    @NotNull
    @Override
    public CordaFuture<Integer> execute(String deduplicationId) {
        throw new IllegalStateException("You shouldn't be calling me");
    }

    public final int getA() {
        return this.a;
    }

    public final int getB() {
        return this.b;
    }

    public SummingOperationThrowing(int a, int b) {
        this.a = a;
        this.b = b;
    }
}

```
{{% /tab %}}

{{< /tabs >}}

The operation now throws a rude exception. If we modify the example flow to use this and run the same test we will get
a lot of logs about the error condition (as we are in dev mode). The interesting bit looks like this:

```none
[WARN ] 18:38:52,613 [Node thread-1] (DumpHistoryOnErrorInterceptor.kt:39) interceptors.DumpHistoryOnErrorInterceptor.executeTransition - Flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] errored, dumping all transitions:

 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.426Z
  Event: DoRemainingWork
  Actions:
    CreateTransaction
    PersistCheckpoint(id=[03ab886e-3fd3-4667-b944-ab6a3b1f90a7], checkpoint=Checkpoint(invocationContext=InvocationContext(origin=RPC(actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES)), trace=Trace(invocationId=26bcf0c3-f1d8-4098-a52d-3780f4095b7a, timestamp: 2018-06-01T17:38:52.234Z, entityType: Invocation, sessionId=393d1175-3bb1-4eb1-bff0-6ba317851260, timestamp: 2018-06-01T17:38:52.169Z, entityType: Session), actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES), externalTrace=null, impersonatedActor=null), ourIdentity=O=Alice Corp, L=Madrid, C=ES, sessions={}, subFlowStack=[Inlined(flowClass=class net.corda.docs.tutorial.flowstatemachines.ExampleSummingFlow, subFlowVersion=CorDappFlow(platformVersion=1, corDappName=net.corda.docs-c6816652-f975-4fb2-aa09-ef1dddea19b3, corDappHash=F4012397D8CF97926B5998E046DBCE16D497318BB87DCED66313912D4B303BB7))], flowState=Unstarted(flowStart=Explicit, frozenFlowLogic=74BA62EC5821EBD4FC4CBE129843F9ED6509DB37E6E3C8F85E3F7A8D84083500), errorState=Clean, numberOfSuspends=0, deduplicationSeed=03ab886e-3fd3-4667-b944-ab6a3b1f90a7))
    PersistDeduplicationFacts(deduplicationHandlers=[net.corda.node.internal.FlowStarterImpl$startFlow$startFlowEvent$1@69326343])
    CommitTransaction
    AcknowledgeMessages(deduplicationHandlers=[net.corda.node.internal.FlowStarterImpl$startFlow$startFlowEvent$1@69326343])
    SignalFlowHasStarted(flowId=[03ab886e-3fd3-4667-b944-ab6a3b1f90a7])
    CreateTransaction
  Continuation: Resume(result=null)
  Diff between previous and next state:
isAnyCheckpointPersisted:
    false
    true
pendingDeduplicationHandlers:
    [net.corda.node.internal.FlowStarterImpl$startFlow$startFlowEvent$1@69326343]
    []
isFlowResumed:
    false
    true


 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.487Z
  Event: Suspend(ioRequest=ExecuteAsyncOperation(operation=net.corda.docs.tutorial.flowstatemachines.SummingOperationThrowing@40f4c23d), maySkipCheckpoint=false, fiber=15EC69204562BB396846768169AD4A339569D97AE841D805C230C513A8BA5BDE, )
  Actions:
    PersistCheckpoint(id=[03ab886e-3fd3-4667-b944-ab6a3b1f90a7], checkpoint=Checkpoint(invocationContext=InvocationContext(origin=RPC(actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES)), trace=Trace(invocationId=26bcf0c3-f1d8-4098-a52d-3780f4095b7a, timestamp: 2018-06-01T17:38:52.234Z, entityType: Invocation, sessionId=393d1175-3bb1-4eb1-bff0-6ba317851260, timestamp: 2018-06-01T17:38:52.169Z, entityType: Session), actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES), externalTrace=null, impersonatedActor=null), ourIdentity=O=Alice Corp, L=Madrid, C=ES, sessions={}, subFlowStack=[Inlined(flowClass=class net.corda.docs.tutorial.flowstatemachines.ExampleSummingFlow, subFlowVersion=CorDappFlow(platformVersion=1, corDappName=net.corda.docs-c6816652-f975-4fb2-aa09-ef1dddea19b3, corDappHash=F4012397D8CF97926B5998E046DBCE16D497318BB87DCED66313912D4B303BB7))], flowState=Started(flowIORequest=ExecuteAsyncOperation(operation=net.corda.docs.tutorial.flowstatemachines.SummingOperationThrowing@40f4c23d), frozenFiber=15EC69204562BB396846768169AD4A339569D97AE841D805C230C513A8BA5BDE), errorState=Clean, numberOfSuspends=1, deduplicationSeed=03ab886e-3fd3-4667-b944-ab6a3b1f90a7))
    PersistDeduplicationFacts(deduplicationHandlers=[])
    CommitTransaction
    AcknowledgeMessages(deduplicationHandlers=[])
    ScheduleEvent(event=DoRemainingWork)
  Continuation: ProcessEvents
  Diff between previous and next state:
checkpoint.numberOfSuspends:
    0
    1
checkpoint.flowState:
    Unstarted(flowStart=Explicit, frozenFlowLogic=74BA62EC5821EBD4FC4CBE129843F9ED6509DB37E6E3C8F85E3F7A8D84083500)
    Started(flowIORequest=ExecuteAsyncOperation(operation=net.corda.docs.tutorial.flowstatemachines.SummingOperationThrowing@40f4c23d), frozenFiber=15EC69204562BB396846768169AD4A339569D97AE841D805C230C513A8BA5BDE)
isFlowResumed:
    true
    false


 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.549Z
  Event: DoRemainingWork
  Actions:
    ExecuteAsyncOperation(operation=net.corda.docs.tutorial.flowstatemachines.SummingOperationThrowing@40f4c23d)
  Continuation: ProcessEvents
  Diff between previous and intended state:
null
  Diff between previous and next state:
checkpoint.errorState:
    Clean
    Errored(errors=[FlowError(errorId=-8704604242619505379, exception=java.lang.IllegalStateException: You shouldn't be calling me)], propagatedIndex=0, propagating=false)


 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.555Z
  Event: DoRemainingWork
  Actions:

  Continuation: ProcessEvents
  Diff between previous and next state:
null

 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.556Z
  Event: StartErrorPropagation
  Actions:
    ScheduleEvent(event=DoRemainingWork)
  Continuation: ProcessEvents
  Diff between previous and next state:
checkpoint.errorState.propagating:
    false
    true


 --- Transition of flow [03ab886e-3fd3-4667-b944-ab6a3b1f90a7] ---
  Timestamp: 2018-06-01T17:38:52.606Z
  Event: DoRemainingWork
  Actions:
    PropagateErrors(errorMessages=[ErrorSessionMessage(flowException=null, errorId=-8704604242619505379)], sessions=[], senderUUID=861f07d6-4b8f-42bd-9b52-5152812db2ba)
    CreateTransaction
    RemoveCheckpoint(id=[03ab886e-3fd3-4667-b944-ab6a3b1f90a7])
    PersistDeduplicationFacts(deduplicationHandlers=[])
    ReleaseSoftLocks(uuid=03ab886e-3fd3-4667-b944-ab6a3b1f90a7)
    CommitTransaction
    AcknowledgeMessages(deduplicationHandlers=[])
    RemoveSessionBindings(sessionIds=[])
    RemoveFlow(flowId=[03ab886e-3fd3-4667-b944-ab6a3b1f90a7], removalReason=ErrorFinish(flowErrors=[FlowError(errorId=-8704604242619505379, exception=java.lang.IllegalStateException: You shouldn't be calling me)]), lastState=StateMachineState(checkpoint=Checkpoint(invocationContext=InvocationContext(origin=RPC(actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES)), trace=Trace(invocationId=26bcf0c3-f1d8-4098-a52d-3780f4095b7a, timestamp: 2018-06-01T17:38:52.234Z, entityType: Invocation, sessionId=393d1175-3bb1-4eb1-bff0-6ba317851260, timestamp: 2018-06-01T17:38:52.169Z, entityType: Session), actor=Actor(id=Id(value=aliceUser), serviceId=AuthServiceId(value=NODE_CONFIG), owningLegalIdentity=O=Alice Corp, L=Madrid, C=ES), externalTrace=null, impersonatedActor=null), ourIdentity=O=Alice Corp, L=Madrid, C=ES, sessions={}, subFlowStack=[Inlined(flowClass=class net.corda.docs.tutorial.flowstatemachines.ExampleSummingFlow, subFlowVersion=CorDappFlow(platformVersion=1, corDappName=net.corda.docs-c6816652-f975-4fb2-aa09-ef1dddea19b3, corDappHash=F4012397D8CF97926B5998E046DBCE16D497318BB87DCED66313912D4B303BB7))], flowState=Started(flowIORequest=ExecuteAsyncOperation(operation=net.corda.docs.tutorial.flowstatemachines.SummingOperationThrowing@40f4c23d), frozenFiber=15EC69204562BB396846768169AD4A339569D97AE841D805C230C513A8BA5BDE), errorState=Errored(errors=[FlowError(errorId=-8704604242619505379, exception=java.lang.IllegalStateException: You shouldn't be calling me)], propagatedIndex=1, propagating=true), numberOfSuspends=1, deduplicationSeed=03ab886e-3fd3-4667-b944-ab6a3b1f90a7), flowLogic=net.corda.docs.tutorial.flowstatemachines.ExampleSummingFlow@600b0c6c, pendingDeduplicationHandlers=[], isFlowResumed=false, isTransactionTracked=false, isAnyCheckpointPersisted=true, isStartIdempotent=false, isRemoved=true, senderUUID=861f07d6-4b8f-42bd-9b52-5152812db2ba))
  Continuation: Abort
  Diff between previous and next state:
checkpoint.errorState.propagatedIndex:
    0
    1
isRemoved:
    false
    true
```

Whoa that’s a lot of stuff. Now we get a glimpse into the bowels of the flow state machine. As we can see the flow did
quite a few things, even though the flow code looks simple.

What we can see here is the different transitions the flow’s state machine went through that led up to the error
condition. For each transition we see what *Event* triggered the transition, what *Action* s were taken as a consequence,
and how the internal *State* of the state machine was modified in the process. It also prints the transition’s
*Continuation*, which indicates how the flow should proceed after the transition.

For example in the first transition we can see that the triggering event was a `DoRemainingWork`, this is a generic
event that instructs the state machine to check its own state to see whether there’s any work left to do, and does it if
there’s any.

In this case the work involves persisting a checkpoint together with some deduplication data in a database transaction,
then acknowledging any triggering messages, signalling that the flow has started, and creating a fresh database
transaction, to be used by user code.

The continuation is a `Resume`, which instructs the state machine to hand control to user code. The state change is
a simple update of bookkeeping data.

In other words the first transition concerns the initialization of the flow, which includes the creation of the
checkpoint.

The next transition is the suspension of our summing operation, triggered by the `Suspend` event. As we can see in
this transition we aren’t doing any work related to the summation yet, we’re merely persisting the checkpoint that
indicates that we want to do the summation. Had we added a `toString` method to our `SummingOperationThrowing` we
would see a nicer message.

The next transition is the faulty one, as we can see it was also triggered by a `DoRemainingWork`, and executed our
operation. We can see that there are two state “diff”s printed, one that would’ve happened had the transition succeeded,
and one that actually happened, which marked the flow’s state as errored. The rest of the transitions involve error
propagation (triggered by the `FlowHospital`) and notification of failure, which ultimately raises the exception on
the RPC `resultFuture`.
