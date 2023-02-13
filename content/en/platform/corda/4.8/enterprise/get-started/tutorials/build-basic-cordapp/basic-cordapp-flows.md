---
date: '2023-01-13'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-tutorial-basic-cordapp-flows
    parent: corda-enterprise-4-8-tutorial-basic-cordapp-intro
    weight: 90
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

This tutorial guides you through writing the three flows you need in your CorDapp. These are:

* `CreateAndIssueAppleStamp` flow
* `PackageApples` flow
* `RedeemApples` flow

You will be creating these flows in the `workflows/src/main/java/com/tutorial/flows` directory in this tutorial. Refer to the `TemplateInitiator.java` and `TemplateResponder.java` files in this directory to see template initiator and responder flows.

## Learning objectives

After you have completed this tutorial, you will know how to write and implement flows in a CorDapp.

## Before you start

Before you start writing flows, read [Key concepts: Flows](../../../key-concepts-flows.md).

## Write the `CreateAndIssueAppleStamp` flow

The `CreateAndIssueAppleStamp` flow creates the `AppleStamp` and issues it to the customer.

### Write the initiator flow

The `CreateAndIssueAppleStamp` flow action requires interaction between the issuer and the customer. For this reason, you must create an initiator flow and a responder flow.

#### Implement the `CreateAndIssueAppleStamp` class

Add the `CreateAndIssueAppleStamp` public class. When naming a public class, the class name must match the name of the file. You will fill this class in subsequent sections of the tutorial.

#### Add annotations

1. Add the `@InitiatingFlow` annotation. This indicates that this flow is the initiating flow.
2. Add the `@StartableByRPC` annotation. This annotation allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC client.

So far your code should look like this:

```java
public class CreateAndIssueAppleStamp {

    @InitiatingFlow
    @StartableByRPC
}
```

#### Add the `CreateAndIssueAppleStampInitiator` subclass

Add the `CreateAndIssueAppleStampInitiator` public static class to extend `FlowLogic`. Include a `SignedTransaction` return type.

#### Add variables

Add the following private variables to the subclass:

* `stampDescription` - Information included with the `AppleStamp`. This must be a `String` type.
* `holder` - The holder of the `AppleStamp`. This must be a `Party` type.

{{< note >}}
When writing flows, it's important that you consider who is calling the flow - this affects the parameters you need.
{{< /note >}}

#### Add a constructor

The constructor must have the same name as the subclass. Include the `holder` and `stampDescription` variables in the constructor.

Let's check in on your code. It should now look like this:

```java
public class CreateAndIssueAppleStamp {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueAppleStampInitiator  extends FlowLogic<SignedTransaction>{

        private String stampDescription;
        private Party holder;

        public CreateAndIssueAppleStampInitiator(String stampDescription,  Party holder) {
            this.stampDescription = stampDescription;
            this.holder = holder;
        }
```

{{< note >}}

After implementing the constructor, IntelliJ will add a red curly line under the `createAndIssueAppleStampInitiator` subclass. Here you need to add a method. Luckily IntelliJ can do this for you.

1. Click the subclass.
2. * On macOS press option + Enter.
    * On Windows press Alt + Enter.

You have now added the required `@OverRide` method.

{{< /note >}}

#### Add the `call` method

1. Add the `@Suspendable` annotation.
2. Add the `call` method with a `SignedTransaction` return type.

#### Obtain a reference for the notary

In transactions with multiple parties, you need a notary service to reach consensus between the parties. Since this flow is communicating with Farmer Bob and Peter, you need the notary.

You can add a notary service in one of two ways:
1. Use the `getServiceHub`, `getNetworkMapCache`, `getNotaryIdentities`, and `get` methods to get the services of the first available notary on the network. In this CorDapp there is only one notary, so it will always select the same one. This is fine for a simple application with one notary but should not be used in production environments.
2. Use the `getServiceHub`, `getNetworkMapCache`, and `getNotary` methods, specifying the notary's x500 name, to select a specific notary. This is the recommended option for production environments.

#### Build the output `AppleStamp` state

In flows with inputs, you use those inputs to determine the outputs a flow will have. Since this flow is creating and issuing the `AppleStamp`, there are no inputs to utilize.

Build the output `newStamp` using the parameters from the `AppleStamp` state:

* `stampDescription`
* `holder`
* `UniqueIdentifier`

#### Encapsulate the output and notary into the transaction

Use the `TransactionBuilder` Corda object to encapsulate everything into the transaction.

1. Add `TransactionBuilder TxBuilder = new TransactionBuilder`.
1. Insert the `notary`.
2. Use the `addOutputState` method to add the `newStamp`.
3. Use the `addCommand` method to add the `Issue` command and a list of required signees (the initiator and the `holder`). Use `getOurIdentity` and `getOwningKey` methods to get the required signees.

#### Verify that the transaction is valid

Use the `verify` method to trigger contract verification of the `txBuilder` from the `getServiceHub`.

#### Sign the transaction

The initiator needs to sign the transaction for the transaction to be valid.

1. Add `final SignedTransaction partSignedTx`.
2. Use the `getServiceHub` method to `signInitialTransaction`. Insert the `txBuilder`.

#### Send the state to the counterparty and receive it back with their signature

After the initiator signs, the counterparty must also sign the transaction.

1. Start a `FlowSession` with the counterparty using the `InitiateFlow` method. Add this line to start the flow session with the `holder`:
```
FlowSession otherPartySession = initiateFlow(holder);
```
2. Call a subflow to collect signatures. Introduce the `CollectSignaturesFlow` with the `partSignedTx` and the `otherPartySession`.

#### Notarize and record the transaction in both parties' vaults

Use the subflow `FinalityFlow` to update the ledger and record changes.

The `FinalityFlow` must contain the `fullySignedTx` and the `otherPartySession`.

### Write the responder flow

As noted above, the initiator flow needs a corresponding responder flow. The counterparty runs the responder flow.

#### Add annotation

Add the `@InitiatedBy` annotation with the `CreateAndIssueAppleStampInitiator` class to indicate that this is the responder flow.

#### Add the `CreateAndIssueAppleStampResponder` subclass

Add the `CreateAndIssueAppleStampResponder` public static class to extend `FlowLogic`. The return type here is `Void`.

#### Add variables

1. Add the `FlowSession Counterparty session`.
2. Add the public variable `CreateAndIssueAppleStampResponder` with a `FlowSession` to open the `counterpartySession`.

Your variables should look like this:

```java
        private FlowSession counterpartySession;

        public CreateAndIssueAppleStampResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
```

#### Add the `call` method

1. Add the `@Suspendable` annotation.
2. Add the `@Override` annotation.
3. Add the `call` method with a `subFlow` that will sign the partially signed transaction from the initiator:
```java
SignedTransaction signedTransaction = subFlow(new SignTransactionFlow(counterpartySession)
```
4. Inside the subflow, you can perform checks on the transaction using `checkTransaction`. If these checks fail, an exception is thrown. You do not need to add any checks for this CorDapp.
5. Store the transactions in the database using the subflow `ReceiveFinalityFlow` with the `counterpartySession` and the `signedTransaction.`

You have now written the `CreateAndIssueAppleStamp` flow. Your code should look like this:

```java
package com.tutorial.flows;

import co.paralleluniverse.fibers.Suspendable;
import com.tutorial.contracts.AppleStampContract;
import com.tutorial.states.AppleStamp;
import net.corda.core.contracts.UniqueIdentifier;
import net.corda.core.flows.*;
import net.corda.core.identity.Party;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;

import java.util.ArrayList;
import java.util.Arrays;

public class CreateAndIssueAppleStamp {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueAppleStampInitiator  extends FlowLogic<SignedTransaction>{

        private String stampDescription;
        private Party holder;

        public CreateAndIssueAppleStampInitiator(String stampDescription,  Party holder) {
            this.stampDescription = stampDescription;
            this.holder = holder;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {

            /* Obtain a reference to a notary we wish to use.
             * METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
             *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flows or parsed from config (Preferred)
             *  * - For production you always want to1 use Method 2 as it guarantees the expected notary is returned.
             */
            final Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0); // METHOD 1
            //final Party notary = getServiceHub().getNetworkMapCache().getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")); // METHOD 2

            //Building the output AppleStamp state
            UniqueIdentifier uniqueID = new UniqueIdentifier();
            AppleStamp newStamp = new AppleStamp(this.stampDescription,this.getOurIdentity(),this.holder,uniqueID);

            //Compositing the transaction
            TransactionBuilder txBuilder = new TransactionBuilder(notary)
                    .addOutputState(newStamp)
                    .addCommand(new AppleStampContract.Commands.Issue(),
                            Arrays.asList(getOurIdentity().getOwningKey(),holder.getOwningKey()));

            // Verify that the transaction is valid.
            txBuilder.verify(getServiceHub());

            // Sign the transaction.
            final SignedTransaction partSignedTx = getServiceHub().signInitialTransaction(txBuilder);

            // Send the state to the counterparty, and receive it back with their signature.
            FlowSession otherPartySession = initiateFlow(holder);
            final SignedTransaction fullySignedTx = subFlow(
                    new CollectSignaturesFlow(partSignedTx, Arrays.asList(otherPartySession)));

            // Notarise and record the transaction in both parties' vaults.
            return subFlow(new FinalityFlow(fullySignedTx, Arrays.asList(otherPartySession)));
        }
    }

    @InitiatedBy(CreateAndIssueAppleStampInitiator.class)
    public static class CreateAndIssueAppleStampResponder extends FlowLogic<Void>{

        //private variable
        private FlowSession counterpartySession;

        public CreateAndIssueAppleStampResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        @Override
        @Suspendable
        public Void call() throws FlowException {
            SignedTransaction signedTransaction = subFlow(new SignTransactionFlow(counterpartySession) {
                @Override
                @Suspendable
                protected void checkTransaction(SignedTransaction stx) throws FlowException {
                    /*
                     * SignTransactionFlow will automatically verify the transaction and its signatures before signing it.
                     * However, just because a transaction is contractually valid doesn’t mean we necessarily want to sign.
                     * What if we don’t want to deal with the counterparty in question, or the value is too high,
                     * or we’re not happy with the transaction’s structure? checkTransaction
                     * allows us to define these additional checks. If any of these conditions are not met,
                     * we will not sign the transaction - even if the transaction and its signatures are contractually valid.
                     * ----------
                     * For this hello-world cordapp, we will not implement any additional checks.
                     * */
                }
            });

            //Stored the transaction into data base.
            subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
            return null;
        }
    }

}
```

## Write the `PackageApples` and `RedeemApples` flows

Now that you have written the `CreateAndIssueAppleStamp` flow, try writing the `PackageApples` and `RedeemApples` flows on your own.

### `PackageApples` flow

The `PackageApples` flow is simpler than the `CreateAndIssueAppleStamp` flow, in that it only involves one party. This flow represents Farmer Bob preparing the apples for Peter to collect.

Since the flow only involves one party (Farmer Bob), you only need an initiator flow, not a pair of initiator and responder flows. However, you still must add the `@InitiatingFlow` annotation to the initiating flow.

Include these variables in the flow:

* `appleDescription` - Relevant information, such as the type of apple. Use type `String`.
* `weight` - The weight of the apples. Use type `int`.

Though you don't need a notary in a single-party flow, all standard flows include a notary. You can add one to this flow, although it won't do anything in your transaction.

#### Check your work

After you've written the `PackageApples` flow, your code should look like this:

```java
package com.tutorial.flows;

import co.paralleluniverse.fibers.Suspendable;
import com.tutorial.contracts.BasketOfAppleContract;
import com.tutorial.states.BasketOfApple;
import net.corda.core.flows.*;
import net.corda.core.identity.Party;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;

import java.util.Collections;

public class PackageApples {

    @InitiatingFlow
    @StartableByRPC
    public static class PackApplesInitiator extends FlowLogic<SignedTransaction> {

        private String appleDescription;
        private int weight;

        public PackApplesInitiator(String appleDescription, int weight) {
            this.appleDescription = appleDescription;
            this.weight = weight;
        }

        @Override
        @Suspendable
        public SignedTransaction call() throws FlowException {

            /* Obtain a reference to a notary we wish to use.
             * METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
             *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flows or parsed from config (Preferred)
             *  * - For production you always want to use Method 2 as it guarantees the expected notary is returned.
             */
            final Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0); // METHOD 1
            //final Party notary = getServiceHub().getNetworkMapCache().getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")); // METHOD 2

            //Create the output object
            BasketOfApples basket = new BasketOfApple(this.appleDescription,this.getOurIdentity(),this.weight);

            //Building transaction
            TransactionBuilder txBuilder = new TransactionBuilder(notary)
                    .addOutputState(basket)
                    .addCommand(new BasketOfAppleContract.Commands.packToBasket(), this.getOurIdentity().getOwningKey());

            // Verify the transaction
            txBuilder.verify(getServiceHub());

            // Sign the transaction
            SignedTransaction signedTransaction = getServiceHub().signInitialTransaction(txBuilder);

            // Notarise the transaction and record the states in the ledger.
            return subFlow(new FinalityFlow(signedTransaction, Collections.emptyList()));
        }
    }

}
```

### `RedeemApples` flow

The `RedeemApples` flow involves two parties: Farmer Bob and Peter. When this flow is called, Peter redeems his `AppleStamp` for the `BasketOfApples` that Famrer Bob gives him.

You will need an initiator and responder flow pair for this flow.

Include these variables in the flow:

* `buyer` - The customer buying the apples, in this case Peter.
* `stampId` - The unique identifier of the `AppleStamp`.

{{< note >}}
The `RedeemApples` flow has an additional step that you did not see in the previous two flows. It must query the output states from the previous two transactions. These output states are the inputs for the `RedeemApples` flow.
{{< /note >}}

#### Check your work

After you've written the `PackageApples` flow, your code should look like this:

```java
package com.tutorial.flows;

import co.paralleluniverse.fibers.Suspendable;
import com.tutorial.contracts.AppleStampContract;
import com.tutorial.contracts.BasketOfAppleContract;
import com.tutorial.states.AppleStamp;
import com.tutorial.states.BasketOfApple;
import net.corda.core.contracts.StateAndRef;
import net.corda.core.contracts.UniqueIdentifier;
import net.corda.core.flows.*;
import net.corda.core.identity.Party;
import net.corda.core.node.services.Vault;
import net.corda.core.node.services.vault.QueryCriteria;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;

import java.util.Arrays;
import java.util.UUID;

public class RedeemApples {

    @InitiatingFlow
    @StartableByRPC
    public static class RedeemApplesInitiator extends FlowLogic<SignedTransaction>{

        private Party buyer;
        private UniqueIdentifier stampId;

        public RedeemApplesInitiator(Party buyer, UniqueIdentifier stampId) {
            this.buyer = buyer;
            this.stampId = stampId;
        }

        @Override
        @Suspendable
        public SignedTransaction call() throws FlowException {

            /* Obtain a reference to a notary we wish to use.
             * METHOD 1: Take first notary on network, WARNING: use for test, non-prod environments, and single-notary networks only!*
             *  METHOD 2: Explicit selection of notary by CordaX500Name - argument can by coded in flows or parsed from config (Preferred)
             *  * - For production you always want to use Method 2 as it guarantees the expected notary is returned.
             */
            final Party notary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0); // METHOD 1
            //final Party notary = getServiceHub().getNetworkMapCache().getNotary(CordaX500Name.parse("O=Notary,L=London,C=GB")); // METHOD 2

            //Query the AppleStamp
            QueryCriteria.LinearStateQueryCriteria inputCriteria = new QueryCriteria.LinearStateQueryCriteria()
                    .withUuid(Arrays.asList(UUID.fromString(stampId.toString())))
                    .withStatus(Vault.StateStatus.UNCONSUMED)
                    .withRelevancyStatus(Vault.RelevancyStatus.RELEVANT);
            StateAndRef appleStampStateAndRef = getServiceHub().getVaultService().queryBy(AppleStamp.class, inputCriteria).getStates().get(0);

            //Query output BasketOfApples
            QueryCriteria.VaultQueryCriteria outputCriteria = new QueryCriteria.VaultQueryCriteria()
                    .withStatus(Vault.StateStatus.UNCONSUMED)
                    .withRelevancyStatus(Vault.RelevancyStatus.RELEVANT);
            StateAndRef basketOfAppleStateAndRef = getServiceHub().getVaultService().queryBy(BasketOfApple.class, outputCriteria).getStates().get(0);
            BasketOfApples originalBasketOfApples = (BasketOfApples) basketOfAppleStateAndRef.getState().getData();

            //Modify output to address the owner change
            BasketOfApples output = originalBasketOfApple.changeOwner(buyer);

            //Build Transaction
            TransactionBuilder txBuilder = new TransactionBuilder(notary)
                    .addInputState(appleStampStateAndRef)
                    .addInputState(basketOfAppleStateAndRef)
                    .addOutputState(output, BasketOfAppleContract.ID)
                    .addCommand(new BasketOfAppleContract.Commands.Redeem(),
                            Arrays.asList(getOurIdentity().getOwningKey(),this.buyer.getOwningKey()));

            // Verify that the transaction is valid.
            txBuilder.verify(getServiceHub());

            // Sign the transaction.
            final SignedTransaction partSignedTx = getServiceHub().signInitialTransaction(txBuilder);

            // Send the state to the counterparty, and receive it back with their signature.
            FlowSession otherPartySession = initiateFlow(buyer);
            final SignedTransaction fullySignedTx = subFlow(
                    new CollectSignaturesFlow(partSignedTx, Arrays.asList(otherPartySession)));

            // Notarise and record the transaction in both parties' vaults.
            SignedTransaction result = subFlow(new FinalityFlow(fullySignedTx, Arrays.asList(otherPartySession)));

            return result;
        }
    }

    @InitiatedBy(RedeemApplesInitiator.class)
    public static class RedeemApplesResponder extends FlowLogic<Void>{
        //private variable
        private FlowSession counterpartySession;

        public RedeemApplesResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        @Override
        @Suspendable
        public Void call() throws FlowException {
            SignedTransaction signedTransaction = subFlow(new SignTransactionFlow(counterpartySession) {
                @Override
                protected void checkTransaction(SignedTransaction stx) throws FlowException {
                }
            });

            //Stored the transaction into data base.
            subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
            return null;
        }
    }

}
```

## Next steps

Follow the [Write unit tests](basic-cordapp-unit-testing.md) tutorial to continue on this learning path.
