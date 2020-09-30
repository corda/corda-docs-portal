---
aliases:
- /head/tut-two-party-flow.html
- /HEAD/tut-two-party-flow.html
- /tut-two-party-flow.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-tut-two-party-flow
    parent: corda-os-4-6-tut-two-party-introduction
    weight: 1020
tags:
- tut
- party
- flow
title: Updating the flow
---




# Updating the flow

After you have written the contract and defined any necessary constraints, as described in [Writing the contract](tut-two-party-contract.md), you now need to update your flow to achieve three things:

* Verifying that the transaction proposal you build fulfills the `IOUContract` constraints
* Updating the lender’s side of the flow to request the borrower’s signature
* Creating a response flow for the borrower that responds to the signature request from the lender

To do this, modifying the flow that you created earlier as part of [Writing the flow](hello-world-flow.md).


## Verifying the transaction

In `IOUFlow.java`/`Flows.kt`, change the imports block to the following:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
import co.paralleluniverse.fibers.Suspendable
import net.corda.core.contracts.Command
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
import net.corda.core.contracts.Command;
import net.corda.core.flows.*;
import net.corda.core.identity.Party;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;
import net.corda.core.utilities.ProgressTracker;

import java.security.PublicKey;
import java.util.Arrays;
import java.util.List;

```
{{% /tab %}}

{{< /tabs >}}

Next, update `IOUFlow.call` to the following:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// You retrieve the notary identity from the network map.
val notary = serviceHub.networkMapCache.notaryIdentities[0]

// You create the transaction components.
val outputState = IOUState(iouValue, ourIdentity, otherParty)
val command = Command(IOUContract.Create(), listOf(ourIdentity.owningKey, otherParty.owningKey))

// You create a transaction builder and add the components.
val txBuilder = TransactionBuilder(notary = notary)
        .addOutputState(outputState, IOUContract.ID)
        .addCommand(command)

// Verifying the transaction.
txBuilder.verify(serviceHub)

// Signing the transaction.
val signedTx = serviceHub.signInitialTransaction(txBuilder)

// Creating a session with the other party.
val otherPartySession = initiateFlow(otherParty)

// Obtaining the counterparty's signature.
val fullySignedTx = subFlow(CollectSignaturesFlow(signedTx, listOf(otherPartySession), CollectSignaturesFlow.tracker()))

// Finalising the transaction.
subFlow(FinalityFlow(fullySignedTx, otherPartySession))

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// You retrieve the notary identity from the network map.
Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0);

// You create the transaction components.
IOUState outputState = new IOUState(iouValue, getOurIdentity(), otherParty);
List<PublicKey> requiredSigners = Arrays.asList(getOurIdentity().getOwningKey(), otherParty.getOwningKey());
Command command = new Command<>(new IOUContract.Create(), requiredSigners);

// You create a transaction builder and add the components.
TransactionBuilder txBuilder = new TransactionBuilder(notary)
        .addOutputState(outputState, IOUContract.ID)
        .addCommand(command);

// Verifying the transaction.
txBuilder.verify(getServiceHub());

// Signing the transaction.
SignedTransaction signedTx = getServiceHub().signInitialTransaction(txBuilder);

// Creating a session with the other party.
FlowSession otherPartySession = initiateFlow(otherParty);

// Obtaining the counterparty's signature.
SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(
        signedTx, Arrays.asList(otherPartySession), CollectSignaturesFlow.tracker()));

// Finalising the transaction.
subFlow(new FinalityFlow(fullySignedTx, otherPartySession));

return null;

```
{{% /tab %}}

{{< /tabs >}}

In the original CorDapp, you automated the process of notarising a transaction and recording it in every party’s vault
by invoking a built-in flow called `FinalityFlow` as a subflow. Now, you're going to use another pre-defined flow,
`CollectSignaturesFlow`, to gather the borrower’s signature.

First, you need to update the command to use `IOUContract.Create`, rather than
`TemplateContract.Commands.Action`. You'll also want to make the borrower a required signer, as per the contract
constraints. To do this, simply add the borrower’s public key to the transaction’s command.

You'll also need to add the output state to the transaction using a reference to the `IOUContract`, instead of to the old
`TemplateContract`.

Now that the output state is governed by a real contract, you'll want to check that your transaction proposal satisfies these
requirements before kicking off the signing process. To do this, you'll call `TransactionBuilder.verify` on your
transaction proposal before finalising it by adding the signature.


## Requesting the borrower’s signature

In the flow that you created earlier, you wrote a responder flow for the borrower in order to receive the finalised transaction from the lender.
You'll now use this same flow to first request their signature over the transaction.

To gather the borrower’s signature, you'll use `CollectSignaturesFlow`, which takes:

* A transaction signed by the flow initiator
* A list of flow-sessions between the flow initiator and the required signers

It then returns a transaction signed by all the required signers.

You can pass this fully-signed transaction into `FinalityFlow`.


## Updating the borrower’s flow

On the lender’s side, you used `CollectSignaturesFlow` to automate the collection of signatures. To allow the borrower
to respond, you need to update its responder flow to first receive the partially signed transaction for signing. Update
`IOUFlowResponder.call` to be the following:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call() {
    val signTransactionFlow = object : SignTransactionFlow(otherPartySession) {
        override fun checkTransaction(stx: SignedTransaction) = requireThat {
            val output = stx.tx.outputs.single().data
            "This must be an IOU transaction." using (output is IOUState)
            val iou = output as IOUState
            "The IOU's value can't be too high." using (iou.value < 100)
        }
    }
    val expectedTxId = subFlow(signTransactionFlow).id
    subFlow(ReceiveFinalityFlow(otherPartySession, expectedTxId))
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
@Suspendable
@Override
public Void call() throws FlowException {
    class SignTxFlow extends SignTransactionFlow {
        private SignTxFlow(FlowSession otherPartySession) {
            super(otherPartySession);
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

    SecureHash expectedTxId = subFlow(new SignTxFlow(otherPartySession)).getId();

    subFlow(new ReceiveFinalityFlow(otherPartySession, expectedTxId));

    return null;
}

```
{{% /tab %}}

{{< /tabs >}}

You could write your own flow to handle this process. However, there is also a pre-defined flow called
`SignTransactionFlow` that can handle the process automatically. The only catch is that `SignTransactionFlow` is an
abstract class - you must subclass it and override `SignTransactionFlow.checkTransaction`.


### CheckTransactions

`SignTransactionFlow` will automatically verify the transaction and its signatures before signing it. However, just
because a transaction is contractually valid doesn’t mean the parties to the contract will necessarily want to sign. What if one party doesn’t want to deal
with the counterparty in question, or the value is too high, or a party is not happy with the transaction’s structure?

Overriding `SignTransactionFlow.checkTransaction` allows you to define any additional checks that you may wish to add. For the purposes of this tutorial, you will want to
check the following:


* The transaction involves an `IOUState` - this ensures that `IOUContract` will be run to verify the transaction.
* The IOU’s value is less than some amount (100 in this case).

If either of these conditions are not met, the transaction will not be signed - even if the transaction and its
signatures are contractually valid.

Once you've defined the `SignTransactionFlow` subclass, you invoke it using `FlowLogic.subFlow`, and the
communication with the borrower’s and the lender’s flow is conducted automatically.

`SignedTransactionFlow` returns the newly signed transaction. You pass in the transaction’s ID to `ReceiveFinalityFlow`
to ensure you are recording the correct notarised transaction from the lender.


## Conclusion

You have now updated your flow to verify the transaction and gather the lender’s signature, in line with the constraints
defined in `IOUContract`. You can now re-run your updated CorDapp, as described in
[Running your CorDapp](hello-world-running.md).

Our CorDapp now imposes restrictions on the issuance of IOUs. Most importantly, IOU issuance now requires agreement
from both the lender and the borrower before an IOU can be created on the blockchain. This prevents either the lender or
the borrower from unilaterally updating the ledger in a way that only benefits themselves.

After completing this tutorial, your CorDapp should look like this:


* Java: [https://github.com/corda/corda-tut2-solution-java](https://github.com/corda/corda-tut2-solution-java)
* Kotlin: [https://github.com/corda/corda-tut2-solution-kotlin](https://github.com/corda/corda-tut2-solution-kotlin)

You should now be ready to develop your own CorDapps. You can also find a list of sample CorDapps
[here](https://www.corda.net/samples/). You are now ready to learn more about the Corda API.

If you get stuck at any point, please reach out on [Slack](https://slack.corda.net/) or
[Stack Overflow](https://stackoverflow.com/questions/tagged/corda).
