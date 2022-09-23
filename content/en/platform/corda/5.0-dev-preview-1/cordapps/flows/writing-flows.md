---
date: '2020-09-08'
title: Writing flows
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-flows
    weight: 1000
section_menu: corda-5-dev-preview
---

In the Corda 5 Developer Preview, use the `Flow` interface to implement a flow. Implementing `Flow` will define the `call` method which holds your business logic.

A flow is where you put your business logic and how you build, sign, and send states to others for signing.

Flows are written as sequential code. Where you may normally expect to see blocking or async code, Corda will pause and resume the flow transparently. A running flow can survive the restart of the Corda node. The basics of flows are covered in the [overview](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/flows/overview.md) .

## Example of a simple flow

Here is a simple flow that returns `true` as a result:

```java
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.StartableByRPC;
import net.corda.v5.base.annotations.Suspendable;

@StartableByRPC
public class SimpleFlow implements Flow<Boolean> {

    @JsonConstructor
    public SimpleFlow(RpcStartFlowRequestParameters params) { }

    @Override
    @Suspendable
    public Boolean call() {
        return true;
    }
}
```

About this flow:

- `@StartableByRPC` - Allows the flow to be started by HTTP-RPC.
- `@JsonConstructor` - Flows startable by RPC must have a constructor with this annotation that takes a `RpcStartFlowRequestParameters`.
- `implements Flow<Boolean>` - The interface to implement when writing a flow. The type parameter is the return value of the flow.
- `@Suspendable` - The `call` method must always have this annotation as it allows the flow to be suspended by Corda.
- `call()` - This method is called by Corda when the flow is started.

## Use injected services

This flow makes use of an injected service:

```java
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.flows.StartableByRPC;
import net.corda.v5.application.flows.StateMachineRunId;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.base.annotations.Suspendable;

@StartableByRPC
public class UsingAnInjectedService implements Flow<StateMachineRunId> {

    @JsonConstructor
    public SimpleFlow(RpcStartFlowRequestParameters params) { }

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

## Communication example

This flow demonstrates communication between two flows.

```kotlin
import net.corda.solarsystem.contracts.ProbeContract
import net.corda.solarsystem.states.ProbeState
import net.corda.systemflows.CollectSignaturesFlow
import net.corda.systemflows.FinalityFlow
import net.corda.v5.application.flows.BadRpcStartFlowRequestException
import net.corda.v5.application.flows.Flow
import net.corda.v5.application.flows.InitiatingFlow
import net.corda.v5.application.flows.JsonConstructor
import net.corda.v5.application.flows.RpcStartFlowRequestParameters
import net.corda.v5.application.flows.StartableByRPC
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.flows.flowservices.FlowMessaging
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.IdentityService
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.services.TransactionService
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory

/**
 * This flow allows two parties (the [Launcher] and the [Target]) to say hello to one another via the [ProbeState].
 *
 * In our simple example, the [Acceptor] will only accepts a valid Probe.
 *
 * These flows have deliberately been implemented by using only the call() method for ease of understanding. In
 * practice, we would recommend splitting up the various stages of the flow into sub-routines.
 */
@InitiatingFlow
@StartableByRPC
class LaunchProbeFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) :
    Flow<SignedTransactionDigest> {
    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionService: TransactionService
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    /**
     * The flow logic is encapsulated within the call() method.
     */
    @Suspendable
    override fun call(): SignedTransactionDigest {
        // parse parameters
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)

        val message = with(mapOfParams["message"] ?: throw BadRpcStartFlowRequestException("Parameter \"message\" missing.")) {
            this
        }

        val planetaryOnly = with(mapOfParams["planetaryOnly"] ?: throw BadRpcStartFlowRequestException("Parameter \"planetaryOnly\" missing.")) {
            this.toBoolean()
        }

        val target = with(mapOfParams["target"] ?: throw BadRpcStartFlowRequestException("Parameter \"target\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(target)
            ?: throw NoSuchElementException("No party found for X500 name $target")

        val notary = notaryLookup.notaryIdentities.first()

        // Stage 1.
        // Generate an unsigned transaction.
        val probeState = ProbeState(message, planetaryOnly, flowIdentity.ourIdentity, recipientParty)
        val txCommand = Command(ProbeContract.Commands.Create(), probeState.participants.map { it.owningKey })
        val txBuilder = transactionBuilderFactory.create()
            .setNotary(notary)
            .addOutputState(probeState, ProbeContract.ID)
            .addCommand(txCommand)

        // Stage 2.
        // Verify that the transaction is valid.
        txBuilder.verify()

        // Stage 3.
        // Sign the transaction.
        val partSignedTx = txBuilder.sign()

        // Stage 4.
        // Send the state to the counterparty, and receive it back with their signature.
        val otherPartySession = flowMessaging.initiateFlow(recipientParty)
        val fullySignedTx = flowEngine.subFlow(
            CollectSignaturesFlow(
                partSignedTx, setOf(otherPartySession),
            )
        )

        // Stage 5.
        // Notarise and record the transaction in both parties' vaults.
        val notarisedTx = flowEngine.subFlow(
            FinalityFlow(
                fullySignedTx, setOf(otherPartySession),
            )
        )

        return SignedTransactionDigest(
            notarisedTx.id,
            notarisedTx.tx.outputStates.map { output -> jsonMarshallingService.formatJson(output) },
            notarisedTx.sigs
        )
    }
}
```

About this flow:

- `@InitiatingFlow` - This flow starts flows on other parties by communicating with other parties.
- The flow is annotated with `@StartableByRPC` and has a constructor annotated with `@JsonConstructor` allowing this flow to be started from HTTP-RPC.

```kotlin
import net.corda.solarsystem.states.ProbeState
import net.corda.systemflows.ReceiveFinalityFlow
import net.corda.systemflows.SignTransactionFlow
import net.corda.v5.application.flows.Flow
import net.corda.v5.application.flows.FlowSession
import net.corda.v5.application.flows.InitiatedBy
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.SignedTransaction

@InitiatedBy(LaunchProbeFlow::class)
class LaunchProbeFlowAcceptor(val otherPartySession: FlowSession) : Flow<SignedTransaction> {
    @CordaInject
    lateinit var flowEngine: FlowEngine

    // instead, for now, doing this so it can be unit tested separately:
    fun isValid(stx: SignedTransaction) {
        requireThat {

            val output = stx.tx.outputs.single().data
            "This must be an Probe transaction." using (output is ProbeState)
        }
    }

    @Suspendable
    override fun call(): SignedTransaction {
        val signTransactionFlow = object : SignTransactionFlow(otherPartySession) {
            override fun checkTransaction(stx: SignedTransaction) = isValid(stx)
        }
        val txId = flowEngine.subFlow(signTransactionFlow).id
        return flowEngine.subFlow(ReceiveFinalityFlow(otherPartySession, expectedTxId = txId))
    }
}
```

About this flow:

- `@InitiatedBy` - This flow is started by communication from another flow.
