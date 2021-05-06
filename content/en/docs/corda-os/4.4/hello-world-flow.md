---
aliases:
- /head/hello-world-flow.html
- /HEAD/hello-world-flow.html
- /hello-world-flow.html
- /releases/release-V4.4/hello-world-flow.html
- /docs/corda-os/head/hello-world-flow.html
- /docs/corda-os/hello-world-flow.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-4:
    identifier: corda-os-4-4-hello-world-flow
    parent: corda-os-4-4-hello-world-introduction
    weight: 1030
tags:
- flow
title: Writing the flow
---




# Writing the flow

A flow encodes a sequence of steps that a node can perform to achieve a specific ledger update. Installing new flows
on a node allows the node to handle new business processes. The flow that you define will allow a node to issue an
`IOUState` onto the ledger.


## Flow outline

The goal of your flow will be to orchestrate an IOU issuance transaction. Transactions in Corda are the atomic units of
change that update the ledger. Each transaction is a proposal to mark zero or more existing states as historic (the
inputs), while creating zero or more new states (the outputs).

The process of creating and applying this transaction to a ledger will be conducted by the IOU’s lender, and will
require the following steps:

* Building the transaction proposal for the issuance of a new IOU onto a ledger.
* Signing the transaction proposal.
* Recording the transaction and sending it to the IOU’s borrower so that they can record it too.

You also need the borrower to receive the transaction and record it for themselves. At this stage, you do not require the borrower
to approve and sign IOU issuance transactions. You will be able to impose this requirement when you look at contracts in the
next tutorial.


{{< warning >}}
The execution of a flow is distributed in space and time, as the flow crosses node boundaries and each
participant may have to wait for other participants to respond before it can complete its part of the
overall work. While a node is waiting, the state of its flow may be persistently recorded to disk as a
restorable checkpoint, enabling it to carry on where it left off when a counterparty responds. However,
before a node can be upgraded to a newer version of Corda, or of your CorDapp, all flows must have
completed, as there is no mechanism to upgrade a persisted flow checkpoint. It is therefore undesirable
to model a long-running business process as a single flow: it should rather be broken up into a series
of transactions, with flows used only to orchestrate the completion of each transaction.
{{< /warning >}}

### Subflows

Tasks like recording a transaction or sending a transaction to a counterparty are very common in Corda. Instead of
forcing each developer to reimplement their own logic to handle these tasks, Corda provides a number of library flows
to handle these tasks. Flows that are invoked in the context of a larger flow to handle a repeatable task are called
*subflows*.


## FlowLogic

All flows must subclass `FlowLogic`. You then define the steps taken by the flow by overriding `FlowLogic.call`.

Let’s define your `IOUFlow`. Replace the definition of `Initiator` with the following:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
// Add these imports:
import net.corda.core.contracts.Command;
import net.corda.core.identity.Party;
import net.corda.core.transactions.TransactionBuilder;
import com.template.states.IOUState;
import com.template.contracts.TemplateContract;
import net.corda.core.flows.FlowSession;
import net.corda.core.flows.FinalityFlow;

// Replace Initiator's definition with:
@InitiatingFlow
@StartableByRPC
class IOUFlow(val iouValue: Int,
              val otherParty: Party) : FlowLogic<Unit>() {

    /** The progress tracker provides checkpoints indicating the progress of
    the flow to observers. */
    override val progressTracker = ProgressTracker()

    /** The flow logic is encapsulated within the call() method. */
    @Suspendable
    override fun call() {
        // We retrieve the notary identity from the network map.
        val notary = serviceHub.networkMapCache.notaryIdentities[0]

        // We create the transaction components.
        val outputState = IOUState(iouValue, ourIdentity, otherParty)
        val command = Command(TemplateContract.Commands.Action(), ourIdentity.owningKey)

        // We create a transaction builder and add the components.
        val txBuilder = TransactionBuilder(notary = notary)
                .addOutputState(outputState, TemplateContract.ID)
                .addCommand(command)

        // We sign the transaction.
        val signedTx = serviceHub.signInitialTransaction(txBuilder)

        // Creating a session with the other party.
        val otherPartySession = initiateFlow(otherParty)

        // We finalise the transaction and then send it to the counterparty.
        subFlow(FinalityFlow(signedTx, otherPartySession))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Add these imports:
import net.corda.core.contracts.Command;
import net.corda.core.identity.Party;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;

// Replace Initiator's definition with:
@InitiatingFlow
@StartableByRPC
public class IOUFlow extends FlowLogic<Void> {
    private final Integer iouValue;
    private final Party otherParty;

    /**
     * The progress tracker provides checkpoints indicating the progress of
     the flow to observers.
     */
    private final ProgressTracker progressTracker = new ProgressTracker();

    public IOUFlow(Integer iouValue, Party otherParty) {
        this.iouValue = iouValue;
        this.otherParty = otherParty;
    }

    @Override
    public ProgressTracker getProgressTracker() {
        return progressTracker;
    }

    /**
     * The flow logic is encapsulated within the call() method.
     */
    @Suspendable
    @Override
    public Void call() throws FlowException {
        // We retrieve the notary identity from the network map.
        Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0);

        // We create the transaction components.
        IOUState outputState = new IOUState(iouValue, getOurIdentity(), otherParty);
        Command command = new Command<>(new TemplateContract.Commands.Send(), getOurIdentity().getOwningKey());

        // We create a transaction builder and add the components.
        TransactionBuilder txBuilder = new TransactionBuilder(notary)
                .addOutputState(outputState, TemplateContract.ID)
                .addCommand(command);

        // Signing the transaction.
        SignedTransaction signedTx = getServiceHub().signInitialTransaction(txBuilder);

        // Creating a session with the other party.
        FlowSession otherPartySession = initiateFlow(otherParty);

        // We finalise the transaction and then send it to the counterparty.
        subFlow(new FinalityFlow(signedTx, otherPartySession));

        return null;
    }
}

```
{{% /tab %}}

{{< /tabs >}}

If you’re following along in Java, you’ll also need to rename `Initiator.java` to `IOUFlow.java`.

Let’s walk through this code step-by-step.

You’ve defined your own `FlowLogic` subclass that overrides `FlowLogic.call`. `FlowLogic.call` has a return type
that must match the type parameter passed to `FlowLogic` - this type is returned by running the flow.

`FlowLogic` subclasses can optionally have constructor parameters, which can be used as arguments to
`FlowLogic.call`. In our case, we have two:


* `iouValue`, which is the value of the IOU being issued.
* `otherParty`, the IOU’s borrower (the node running the flow is the lender).

`FlowLogic.call` is annotated `@Suspendable` - this allows the flow to be check-pointed and serialised to disk when
it encounters a long-running operation, allowing your node to move on to running other flows. Leaving this
annotation out will lead to some very weird error messages!

There are also a few more annotations, on the `FlowLogic` subclass itself:

* `@InitiatingFlow` means that this flow is part of a flow pair and that it triggers the other side to run the
the counterpart flow (which in our case is the `IOUFlowResponder` defined below).
* `@StartableByRPC` allows the node owner to start this flow via an RPC call.


Let’s walk through the steps of `FlowLogic.call` itself. This is where we actually describe the procedure for
issuing the `IOUState` onto a ledger.


### Choosing a notary

Every transaction requires a notary to prevent double spends and serve as a timestamping authority. The first thing you must
do in your flow is retrieve the notary from the node’s `ServiceHub`. `ServiceHub.networkMapCache` provides
information about the other nodes on the network and the services that they offer.

{{< note >}}
Whenever you need information within a flow - whether it’s about your own node’s identity, the node’s local storage,
or the rest of the network - you generally obtain it via the node’s `ServiceHub`.
{{< /note >}}

### Building the transaction

You’ll build your transaction proposal in two steps:


* Creating the transaction’s components.
* Adding these components to a transaction builder.


#### Transaction items

Our transaction will have the following structure:


{{< figure alt="simple tutorial transaction" zoom="/en/images/simple-tutorial-transaction.png" >}}


* The output `IOUState` on the right represents the state you will be adding to the ledger. As you can see, there are
no inputs - you are not consuming any existing ledger states in the creation of your IOU.
* An `Action` command listing the IOU’s lender as a signer.

We’ve already talked about the `IOUState`, but we haven’t looked at commands yet. Commands serve two functions:


* They indicate the intent of a transaction - issuance, transfer, redemption, revocation. This will be crucial when we
discuss contracts in the next tutorial.
* They allow us to define the required signers for the transaction. For example, IOU creation might require signatures
from the lender only, whereas the transfer of an IOU might require signatures from both the IOU’s borrower and lender.

Each `Command` contains a command type plus a list of public keys. For now, you will use the pre-defined
`TemplateContract.Action` as your command type, and you'll list the lender as the only public key. This means that for
the transaction to be valid, the lender is required to sign the transaction.


#### Creating a transaction builder

To actually build the proposed transaction, you need a `TransactionBuilder`. This is a mutable transaction class to
which you can add inputs, outputs, commands, and any other items the transaction needs. You create a
`TransactionBuilder` that uses the notary retrieved earlier.

Once you have the `TransactionBuilder`, you add your components:


* The command is added directly using `TransactionBuilder.addCommand`.
* The output `IOUState` is added using `TransactionBuilder.addOutputState`. As well as the output state itself,
this method takes a reference to the contract that will govern the evolution of the state over time. Here you are
passing in a reference to the `TemplateContract`, which imposes no constraints. You will define a contract imposing
real constraints in the next tutorial.


### Signing the transaction

Now that you have a valid transaction proposal, you need to sign it. Once the transaction is signed, no one will be able
to modify the transaction without invalidating this signature. This effectively makes the transaction immutable.

You sign the transaction using `ServiceHub.signInitialTransaction`, which returns a `SignedTransaction`. A
`SignedTransaction` is an object that pairs a transaction with a list of signatures over that transaction.


### Finalising the transaction

You now have a valid signed transaction. All that’s left to do is to have the notary sign it, have that recorded
locally, and then send it to all the relevant parties. Once that happens the transaction will become a permanent part of the
ledger. Here you use `FinalityFlow` which does all of this for the lender.

For the borrower to receive the transaction they just need a flow that responds to the seller’s flow.


### Creating the borrower’s flow

The borrower has to use `ReceiveFinalityFlow` in order to receive and record the transaction; it needs to respond to
the lender’s flow. Change the `Responder` flow file name to `IOUFlowResponder` and replace the template definition with the following:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Replace Responder's definition with:
@InitiatedBy(IOUFlow::class)
class IOUFlowResponder(private val otherPartySession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        subFlow(ReceiveFinalityFlow(otherPartySession))
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Add this import:
import net.corda.core.flows.ReceiveFinalityFlow;

// Replace Responder's definition with:
@InitiatedBy(IOUFlow.class)
public class IOUFlowResponder extends FlowLogic<Void> {
    private final FlowSession otherPartySession;

    public IOUFlowResponder(FlowSession otherPartySession) {
        this.otherPartySession = otherPartySession;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException {
        subFlow(new ReceiveFinalityFlow(otherPartySession));

        return null;
    }
}

```
{{% /tab %}}

{{< /tabs >}}

As with the `IOUFlow`, our `IOUFlowResponder` flow is a `FlowLogic` subclass where we’ve overridden `FlowLogic.call`.

The flow is annotated with `InitiatedBy(IOUFlow.class)`, which means that your node will invoke
`IOUFlowResponder.call` when it receives a message from a instance of `IOUFlow` running on another node. This message
will be the finalised transaction which will be recorded in the borrower’s vault.


## Progress so far

Your flow, and your CorDapp, are now ready! We have now defined a flow that we can start on our node to completely
automate the process of issuing an IOU onto the ledger. All that’s left is to spin up some nodes and test our CorDapp.
