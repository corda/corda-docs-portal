---
title: "How to write a flow"
date: 2021-04-28T17:24:21+01:00
linkTitle: "How to write a flow"
weight: 200
type: "docs"
author: "Joseph Zuniga-Daly"
lastmod: 2021-04-28
description: >
  How to write a Flow
---

A Flow is where you put your business logic. It is where you build states, sign them and send them to others for signing.

If you are not yet familiar with writing applications for Corda, you should note that flows are written as sequential code. Where you may  normally expect to see blocking or async code, Corda will pause and resume the flow transparently. A running flow can survive restarting the Corda Node. You can read more about the basics of [flows in this overview](flows).

## A simple flow

Here is a simple flow that returns true as a result:

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

Some details about this flow:

- `@StartableByRPC` - Allows the flow to be started by RPC
- `implements Flow<Boolean>` - The interface to implement when writing a flow. The type parameter is the return value of the flow.
- `@Suspendable` - The `call` method must always have this annotation, it allows the flow to be suspended by Corda
- `call()` - This method is called by Corda when the flow is started

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

Some details about this flow:

- `@CordaInject` - Defines a field to be set by Corda before the `call` method is called.

  _The injected field will not be ready to use in the constructor. A flow should avoid accessing the field in constructors._

# Communication example

This flow demonstrates communication between two flows. It is a port of the hello world example seen here: https://docs.corda.net/docs/corda-os/4.8/hello-world-flow.html

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

Some details about this flow:

- `@InitiatingFlow` - This flow starts flows on other parties by communicating with other parties
- `public IOUFlow(Integer iouValue, Party otherParty)` - The flow constructor parameters are still used for flow parameters

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

Some details about this flow:

- `@InitiatedBy` - This flow is started by communication from another flow
