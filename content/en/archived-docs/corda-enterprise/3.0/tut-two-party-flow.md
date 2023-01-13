---
aliases:
- /releases/3.0/tut-two-party-flow.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-tut-two-party-flow
    parent: corda-enterprise-3-0-tut-two-party-introduction
    weight: 1020
tags:
- tut
- party
- flow
title: Updating the flow
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}




# Updating the flow

We now need to update our flow to achieve three things:


* Verifying that the transaction proposal we build fulfills the `IOUContract` constraints
* Updating the lender’s side of the flow to request the borrower’s signature
* Creating a response flow for the borrower that responds to the signature request from the lender

We’ll do this by modifying the flow we wrote in the previous tutorial.


## Verifying the transaction

In `IOUFlow.java`/`App.kt`, change the imports block to the following:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
import co.paralleluniverse.fibers.Suspendable
import net.corda.core.contracts.Command
import net.corda.core.contracts.StateAndContract
import net.corda.core.flows.CollectSignaturesFlow
import net.corda.core.flows.FinalityFlow
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.InitiatingFlow
import net.corda.core.flows.StartableByRPC
import net.corda.core.identity.Party
import net.corda.core.transactions.TransactionBuilder
import net.corda.core.utilities.ProgressTracker


```
{{% /tab %}}

{{% tab name="java" %}}
```java
import co.paralleluniverse.fibers.Suspendable;
import com.google.common.collect.ImmutableList;
import net.corda.core.contracts.Command;
import net.corda.core.contracts.StateAndContract;
import net.corda.core.flows.*;
import net.corda.core.identity.Party;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;
import net.corda.core.utilities.ProgressTracker;

import java.security.PublicKey;
import java.util.List;

```
{{% /tab %}}


{{< /tabs >}}

And update `IOUFlow.call` by changing the code following the retrieval of the notary’s identity from the network as
follows:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// We create a transaction builder.
val txBuilder = TransactionBuilder(notary = notary)

// We create the transaction components.
val outputState = IOUState(iouValue, ourIdentity, otherParty)
val outputContractAndState = StateAndContract(outputState, IOU_CONTRACT_ID)
val cmd = Command(IOUContract.Create(), listOf(ourIdentity.owningKey, otherParty.owningKey))

// We add the items to the builder.
txBuilder.withItems(outputContractAndState, cmd)

// Verifying the transaction.
txBuilder.verify(serviceHub)

// Signing the transaction.
val signedTx = serviceHub.signInitialTransaction(txBuilder)

// Creating a session with the other party.
val otherpartySession = initiateFlow(otherParty)

// Obtaining the counterparty's signature.
val fullySignedTx = subFlow(CollectSignaturesFlow(signedTx, listOf(otherpartySession), CollectSignaturesFlow.tracker()))

// Finalising the transaction.
subFlow(FinalityFlow(fullySignedTx))

```
{{% /tab %}}

{{% tab name="java" %}}
```java
// We create a transaction builder.
final TransactionBuilder txBuilder = new TransactionBuilder();
txBuilder.setNotary(notary);

// We create the transaction components.
IOUState outputState = new IOUState(iouValue, getOurIdentity(), otherParty);
StateAndContract outputContractAndState = new StateAndContract(outputState, IOUContract.IOU_CONTRACT_ID);
List<PublicKey> requiredSigners = ImmutableList.of(getOurIdentity().getOwningKey(), otherParty.getOwningKey());
Command cmd = new Command<>(new IOUContract.Create(), requiredSigners);

// We add the items to the builder.
txBuilder.withItems(outputContractAndState, cmd);

// Verifying the transaction.
txBuilder.verify(getServiceHub());

// Signing the transaction.
final SignedTransaction signedTx = getServiceHub().signInitialTransaction(txBuilder);

// Creating a session with the other party.
FlowSession otherpartySession = initiateFlow(otherParty);

// Obtaining the counterparty's signature.
SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(
        signedTx, ImmutableList.of(otherpartySession), CollectSignaturesFlow.tracker()));

// Finalising the transaction.
subFlow(new FinalityFlow(fullySignedTx));

return null;

```
{{% /tab %}}


{{< /tabs >}}

In the original CorDapp, we automated the process of notarising a transaction and recording it in every party’s vault
by invoking a built-in flow called `FinalityFlow` as a subflow. We’re going to use another pre-defined flow,
`CollectSignaturesFlow`, to gather the borrower’s signature.

First, we need to update the command. We are now using `IOUContract.Create`, rather than
`TemplateContract.Commands.Action`. We also want to make the borrower a required signer, as per the contract
constraints. This is as simple as adding the borrower’s public key to the transaction’s command.

We also need to add the output state to the transaction using a reference to the `IOUContract`, instead of to the old
`TemplateContract`.

Now that our state is governed by a real contract, we’ll want to check that our transaction proposal satisfies these
requirements before kicking off the signing process. We do this by calling `TransactionBuilder.verify` on our
transaction proposal before finalising it by adding our signature.


## Requesting the borrower’s signature

We now need to communicate with the borrower to request their signature over the transaction. Whenever you want to
communicate with another party in the context of a flow, you first need to establish a flow session with them. If the
counterparty has a `FlowLogic` registered to respond to the `FlowLogic` initiating the session, a session will be
established. All communication between the two `FlowLogic` instances will then place as part of this session.

Once we have a session with the borrower, we gather the borrower’s signature using `CollectSignaturesFlow`, which
takes:


* A transaction signed by the flow initiator
* A list of flow-sessions between the flow initiator and the required signers

And returns a transaction signed by all the required signers.

We can then pass this fully-signed transaction into `FinalityFlow`.


## Creating the borrower’s flow

On the lender’s side, we used `CollectSignaturesFlow` to automate the collection of signatures. To allow the lender
to respond, we need to write a response flow as well. In a new `IOUFlowResponder.java` file in Java, or within the
`App.kt` file in Kotlin, add the following class:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
// Add these imports:
import net.corda.core.contracts.requireThat
import net.corda.core.transactions.SignedTransaction

// Define IOUFlowResponder:
@InitiatedBy(IOUFlow::class)
class IOUFlowResponder(val otherPartySession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val signTransactionFlow = object : SignTransactionFlow(otherPartySession, SignTransactionFlow.tracker()) {
            override fun checkTransaction(stx: SignedTransaction) = requireThat {
                val output = stx.tx.outputs.single().data
                "This must be an IOU transaction." using (output is IOUState)
                val iou = output as IOUState
                "The IOU's value can't be too high." using (iou.value < 100)
            }
        }

        subFlow(signTransactionFlow)
    }
}

```
{{% /tab %}}

{{% tab name="java" %}}
```java
// Add these imports:
import co.paralleluniverse.fibers.Suspendable;
import net.corda.core.contracts.ContractState;
import net.corda.core.flows.*;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.utilities.ProgressTracker;

import static net.corda.core.contracts.ContractsDSL.requireThat;

// Define IOUFlowResponder:
@InitiatedBy(IOUFlow.class)
public class IOUFlowResponder extends FlowLogic<Void> {
    private final FlowSession otherPartySession;

    public IOUFlowResponder(FlowSession otherPartySession) {
        this.otherPartySession = otherPartySession;
    }

    @Suspendable
    @Override
    public Void call() throws FlowException {
        class SignTxFlow extends SignTransactionFlow {
            private SignTxFlow(FlowSession otherPartySession, ProgressTracker progressTracker) {
                super(otherPartySession, progressTracker);
            }

            @Override
            protected void checkTransaction(SignedTransaction stx) {
                requireThat(require -> {
                    ContractState output = stx.getTx().getOutputs().get(0).getData();
                    require.using("This must be an IOU transaction.", output instanceof IOUState);
                    IOUState iou = (IOUState) output;
                    require.using("The IOU's value can't be too high.", iou.getValue() < 100);
                    return null;
                });
            }
        }

        subFlow(new SignTxFlow(otherPartySession, SignTransactionFlow.Companion.tracker()));

        return null;
    }
}

```
{{% /tab %}}



{{< /tabs >}}

As with the `IOUFlow`, our `IOUFlowResponder` flow is a `FlowLogic` subclass where we’ve overridden
`FlowLogic.call`.

The flow is annotated with `InitiatedBy(IOUFlow.class)`, which means that your node will invoke
`IOUFlowResponder.call` when it receives a message from a instance of `Initiator` running on another node. What
will this message from the `IOUFlow` be? If we look at the definition of `CollectSignaturesFlow`, we can see that
we’ll be sent a `SignedTransaction`, and are expected to send back our signature over that transaction.

We could write our own flow to handle this process. However, there is also a pre-defined flow called
`SignTransactionFlow` that can handle the process automatically. The only catch is that `SignTransactionFlow` is an
abstract class - we must subclass it and override `SignTransactionFlow.checkTransaction`.


### CheckTransactions

`SignTransactionFlow` will automatically verify the transaction and its signatures before signing it. However, just
because a transaction is contractually valid doesn’t mean we necessarily want to sign. What if we don’t want to deal
with the counterparty in question, or the value is too high, or we’re not happy with the transaction’s structure?

Overriding `SignTransactionFlow.checkTransaction` allows us to define these additional checks. In our case, we are
checking that:


* The transaction involves an `IOUState` - this ensures that `IOUContract` will be run to verify the transaction
* The IOU’s value is less than some amount (100 in this case)

If either of these conditions are not met, we will not sign the transaction - even if the transaction and its
signatures are contractually valid.

Once we’ve defined the `SignTransactionFlow` subclass, we invoke it using `FlowLogic.subFlow`, and the
communication with the borrower’s and the lender’s flow is conducted automatically.


## Conclusion

We have now updated our flow to verify the transaction and gather the lender’s signature, in line with the constraints
defined in `IOUContract`. We can now re-run our updated CorDapp, using the
[same instructions as before](hello-world-running.md).

Our CorDapp now imposes restrictions on the issuance of IOUs. Most importantly, IOU issuance now requires agreement
from both the lender and the borrower before an IOU can be created on the ledger. This prevents either the lender or
the borrower from unilaterally updating the ledger in a way that only benefits themselves.

After completing this tutorial, your CorDapp should look like this:


* Java: [https://github.com/corda/corda-tut2-solution-java](https://github.com/corda/corda-tut2-solution-java)
* Kotlin: [https://github.com/corda/corda-tut2-solution-kotlin](https://github.com/corda/corda-tut2-solution-kotlin)

You should now be ready to develop your own CorDapps. You can also find a list of sample CorDapps
[here](https://www.corda.net/samples/). As you write CorDapps, you’ll also want to learn more about the
[Corda API](corda-api.md).

If you get stuck at any point, please reach out on [Slack](https://slack.corda.net/) or
[Stack Overflow](https://stackoverflow.com/questions/tagged/corda).
