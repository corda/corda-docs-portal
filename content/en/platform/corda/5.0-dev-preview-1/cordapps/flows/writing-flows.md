---
date: '2020-09-08'
title: Writing flows
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-flows
    weight: 1000
project: corda-5
section_menu: corda-5-dev-preview
---

In the Corda 5 Developer Preview, use the `Flow` interface to implement a flow. Implementing `Flow` will define the `call` method which holds your business logic.

A flow is where you put your business logic and how you build, sign, and send states to others for signing.

Flows are written as sequential code. Where you may normally expect to see blocking or async code, Corda will pause and resume the flow transparently. A running flow can survive the restart of the Corda node. The basics of flows are covered in the [overview](overview.md) .

## A simple flow

Here is a simple flow that returns `true` as a result:

```java
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.StartableByRPC;
import net.corda.v5.base.annotations.Suspendable;

@StartableByRPC
public class SimpleFlow implements Flow<Boolean> {
    @Override
    @Suspendable
    public Boolean call() {
        return true;
    }
}
```

About this flow:

- `@StartableByRPC` - Allows the flow to be started by HTTP-RPC.
- `implements Flow<Boolean>` - The interface to implement when writing a flow. The type parameter is the return value of the flow.
- `@Suspendable` - The `call` method must always have this annotation as it allows the flow to be suspended by Corda.
- `call()` - This method is called by Corda when the flow is started.

# Using injected services

This flow makes use of an injected service:

```java
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.StartableByRPC;
import net.corda.v5.application.flows.StateMachineRunId;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.dependencies.CordaInject;
import net.corda.v5.base.annotations.Suspendable;

@StartableByRPC
public class UsingAnInjectedService implements Flow<StateMachineRunId> {

    @CordaInject
    public FlowEngine flowEngine;

    @Override
    @Suspendable
    public StateMachineRunId call() {
        return flowEngine.getRunId();
    }
}
```

About this flow:

- `@CordaInject` - Defines a field to be set by Corda before the `call` method is called.

  _The injected field will not be ready to use in the constructor. A flow should avoid accessing the field in constructors._

# Communication example

This flow demonstrates communication between two flows. It's an extract of the [hello world example](https://docs.corda.net/docs/corda-os/4.8/hello-world-flow.html).

```java
import net.corda.systemflows.FinalityFlow;
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.FlowSession;
import net.corda.v5.application.flows.InitiatingFlow;
import net.corda.v5.application.flows.StartableByRPC;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.flows.flowservices.FlowMessaging;
import net.corda.v5.application.flows.flowservices.dependencies.CordaInject;
import net.corda.v5.application.identity.Party;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.ledger.contracts.Command;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.TransactionBuilder;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;

@InitiatingFlow
@StartableByRPC
public class IOUFlow implements Flow<Void> {

    @CordaInject
    public NotaryLookupService notaryLookupService;

    @CordaInject
    public FlowEngine flowEngine;

    @CordaInject
    public FlowMessaging flowMessaging;

    @CordaInject
    public FlowIdentity flowIdentity;

    @CordaInject
    public TransactionBuilderFactory transactionBuilderFactory;

    private final Integer iouValue;
    private final Party otherParty;

    public IOUFlow(Integer iouValue, Party otherParty) {
        this.iouValue = iouValue;
        this.otherParty = otherParty;
    }

    @Override
    @Suspendable
    public Void call() {

        Party notary = notaryLookupService.getNotaryIdentities().get(0);
        IOUState outputState = new IOUState(iouValue, flowIdentity.getOurIdentity(), otherParty);
        Command command = new Command<>(new TemplateContract.Commands.Send(), flowIdentity.getOurIdentity().getOwningKey());

        // We create a transaction builder and add the components.
        TransactionBuilder txBuilder = transactionBuilderFactory
                .create()
                .setNotary(notary)
                .addOutputState(outputState, TemplateContract.ID)
                .addCommand(command);

        // Signing the transaction.
        SignedTransaction signedTx = txBuilder.sign();

        // Creating a session with the other party.
        FlowSession otherPartySession = flowMessaging.initiateFlow(otherParty);

        // We finalise the transaction and then send it to the counterparty.
        flowEngine.subFlow(new FinalityFlow(signedTx, otherPartySession));
        return null;
    }
}
```

About this flow:

- `@InitiatingFlow` - This flow starts flows on other parties by communicating with other parties.
- `public IOUFlow(Integer iouValue, Party otherParty)` - The flow constructor parameters are still used for flow parameters.

```java
import net.corda.systemflows.ReceiveFinalityFlow;
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.FlowSession;
import net.corda.v5.application.flows.InitiatedBy;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.dependencies.CordaInject;
import net.corda.v5.base.annotations.Suspendable;

@SuppressWarnings("unused")
@InitiatedBy(IOUFlow.class)
public class IOUFlowResponder implements Flow<Void> {

    @CordaInject
    public FlowEngine flowEngine;

    private final FlowSession otherPartySession;

    public IOUFlowResponder(FlowSession otherPartySession) {
        this.otherPartySession = otherPartySession;
    }

    @Override
    @Suspendable
    public Void call() {
        flowEngine.subFlow(new ReceiveFinalityFlow(otherPartySession));
        return null;
    }
}
```

About this flow:

- `@InitiatedBy` - This flow is started by communication from another flow.
