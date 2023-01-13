---
date: '2023-01-11'
title: "Write Flows"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorial-develop-building-your-first-basic-cordapp
    identifier: corda-5-beta-tutorial-develop-write-flows
    weight: 1400
section_menu: corda-5-beta
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

This tutorial guides you through writing the three flows you need in your CorDapp. These are:

* `CreateAndIssueAppleStampFlow`
* `PackageApplesFlow`
* `RedeemApplesFlow`

You will be creating these flows in the `ledger-utxo-example-apples-app/src/main/kotlin/net/cordapp/utxo/apples/flows` directory in this tutorial.

## Learning Objectives

After you have completed this tutorial, you will know how to write and implement flows in a CorDapp.

## Before You Start

Before you start writing flows, read more about [flows](../../ledger/flows.md).

## Write the `CreateAndIssueAppleStampFlow`

The `CreateAndIssueAppleStampFlow` creates the `AppleStamp` and issues it to the customer.

### Write the Initiator Flow

The `CreateAndIssueAppleStampFlow` action requires interaction between the issuer and the customer. For this reason, you must create an initiator flow and a responder flow.


#### Implement the `CreateAndIssueAppleStampFlow` class

Add the `CreateAndIssueAppleStampFlow` class to `net/cordapp/utxo/apples/flowsnet/cordapp/utxo/apples/flows/issue`.


#### Make the `CreateAndIssueAppleStampFlow` Startable by RPC

Add the `RPCStartableFlow` to the `CreateAndIssueAppleStampFlow`.

This allows the flow to be started by RPC. You must implement this interface if you want to trigger the flow with RPC via Corda’s HTTP endpoints.

So far your code should look like this:

```kotlin
class CreateAndIssueAppleStampFlow : RPCStartableFlow
```

#### Allow `CreateAndIssueAppleStampFlow` to Initiate Flows with Peers

Add the `@InitiatingFlow` annotation to `CreateAndIssueAppleStampFlow`.

This indicates that this flow is the initiating flow in an initiating and initiated flow pair. A `protocol` must be defined that both the initiating and initiated flow reference. // THIS DOESN'T MAKE SENSE TO ME. IS IT "DEFINED THAT BOTH..." OR "DEFINED IN BOTH"

So far your code should look like this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : RPCStartableFlow
```


#### Add the `call` Method

1. Add the `call` method with an `RPCRequestData` argument and `String` return type (that `RPCStartableFlow` requires implemented).

2. Add the `@Suspendable` annotation.

{{< note >}}
The `String` returned from the `call` method is the result of the flow which can be requested using one of Corda’s HTTP endpoints.
{{< /note >}}

Your code should now look like this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : RPCStartableFlow {

    @Suspendable
    override fun call(requestBody: RPCRequestData): String {

    }
}
```


#### Inject the Required Services into `CreateAndIssueAppleStampFlow`

`CreateAndIssueAppleStampFlow` requires a number of services to be injected so that they can be used by the flow.

Add the following code to inject the services required by this flow. This code adds properties to the flow and should not be added inside the `call` method:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : RPCStartableFlow {

    @CordaInject
    lateinit var flowMessaging: FlowMessaging

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var memberLookup: MemberLookup

    @CordaInject
    lateinit var notaryLookup: NotaryLookup

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(requestBody: RPCRequestData): String {

    }
}
```


#### Extract the `CreateAndIssueAppleStampFlow`'s Request Parameters

`RPCRequestData` contains the flow’s request parameters passed in via HTTP. To extract the data from the RPCRequestData, you should create a class that represents the data.

1. Create `CreateAndIssueAppleStampRequest` with the following properties:

* `stampDescription` - A `String` description for the `AppleStamp`.
* `holder` - A `MemberX500Name` for the participant who is issued an `AppleStamp`.

This is how it should look like:

```kotlin
data class CreateAndIssueAppleStampRequest(
    val stampDescription: String,
    val holder: MemberX500Name
)
```

2. To extract the request data into a `CreateAndIssueAppleStampRequest`, add `RPCRequestData.getRequestBodyAs` to `CreateAndIssueAppleStampFlow`.

3. Add variables for `stampDescription` and `holderName` and extract them from the `CreateAndIssueAppleStampRequest` instance.

Your code should now look like this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : RPCStartableFlow {

    @CordaInject
    lateinit var flowMessaging: FlowMessaging

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var memberLookup: MemberLookup

    @CordaInject
    lateinit var notaryLookup: NotaryLookup

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(requestBody: RPCRequestData): String {
        val request = requestBody.getRequestBodyAs<CreateAndIssueAppleStampRequest>(jsonMarshallingService)
        val stampDescription = request.stampDescription
        val holderName = request.holder
    }
}
```


#### Obtain a Reference for the Notary

In transactions with multiple parties, you need a notary service to reach consensus between the parties. Since this flow is communicating with Farmer Bob and Peter, you need the notary.

Add the following code to retrieve a notary:

```kotlin
// Retrieve the notaries public key (this will change)
val notaryInfo = notaryLookup.notaryServices.single()
val notaryKey = memberLookup.lookup().single {
    it.memberProvidedContext["corda.notary.service.name"] == notaryInfo.name.toString()
}.ledgerKeys.first()
val notary = Party(notaryInfo.name, notaryKey)
```


#### Lookup the Issuer and Holder of the New `AppleStamp` State

1. Use `memberLookup.myInfo` to lookup the current participant (who is executing the flow).

2. Extract the `name` and `ledgerKey`s (take the first one) of the participant and store the result in a `Party`.

3. Repeat the same process for the holder of the new `AppleStamp` state using the `holderName` from the flow’s input parameters.

4. Verify that this participant exists in the network. //WHICH PARTICIPANT? THE ONE THAT IS EXECUTING THE FLOW OR HOLDER OR BOTH?

Your code should now contain the following lines:

```kotlin
val issuer = memberLookup.myInfo().let { Party(it.name, it.ledgerKeys.first()) }
val holder = memberLookup.lookup(holderName)
    ?.let { Party(it.name, it.ledgerKeys.first()) }
    ?: throw IllegalArgumentException("The holder $holderName does not exist within the network")
```


#### Build the Output `AppleStamp` State

In flows with inputs, you use those inputs to determine the outputs a flow will have. Since this flow is creating and issuing the `AppleStamp`, there are no inputs to utilize. //IS THIS INTRO CORRECT? YOU DELETED IT IN YOUR DOC.

Build the output `newStamp` using the parameters from the `AppleStamp` state:

* `id`
* `stampDescription`
* `issuer`
* `holder`
* `UniqueIdentifier`


#### Encapsulate the Output and Notary into a Transaction

Use an `UtxoTransactionBuilder` to encapsulate everything into a transaction.

1. Use `UtxoLedgerService.getTransactionBuilder` to create a `UtxoTransactionBuilder`.

2. Use `setNotary` to set the transaction’s notary.

3. Use `addOutputState` to add the `newStamp`(the created `AppleStamp`).

4. Use `addCommand` to add the `Issue` command of the `AppleStampContract`.

5. Use `addSignatories` to add the list of required signatories of the transaction. This should include the `issuer`'s and `holder`'s `owningKey`.

6. Use `setTimeWindowUntil` to set a time window for the transaction in which the transaction is valid.

7. Use `toSignedTransaction` to sign the transaction. You must pass in the issuer's (the participant creating the transaction) `owningKey`.

This is what your transaction creation code should look like now:

```kotlin
val transaction = utxoLedgerService.getTransactionBuilder()
      .setNotary(notary)
      .addOutputState(newStamp)
      .addCommand(AppleStampContract.Commands.Issue())
      .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
      .addSignatories(listOf(issuer.owningKey, holder.owningKey))
      .toSignedTransaction(issuer.owningKey)
```


#### Finalize the Transaction

Finalizing a transaction does the following:

1. Sends it to counterparties to:
* Verify the transaction’s contracts.
* Validate the transaction’s contents.
* Sign the transaction.

2. Notarises the transaction.

3. Records the transaction for the current participant.

4. Sends the counterparties the finalized transaction signatures.

5. The counterparties record the transaction.

To finalize a transaction:

1. Start a `FlowSession` with the `holder` using `FlowMessaging.initiateFlow`:

```kotlin
val session = flowMessaging.initiateFlow(holderName)
```

2. Call `UtxoLedgerService.finalize` and pass the transaction and session in. Include a `try/catch` block around the call:

```kotlin
try {
    // Send the transaction and state to the counterparty and let them sign it
    // Then notarise and record the transaction in both parties' vaults.
    utxoLedgerService.finalize(transaction, listOf(session))
} catch (e: Exception) {

}
```


#### Return a Result from the Flow

The transaction will now be successfully finalized and the end of the flow has been reached.

The flow must return a `String` representation of the result of the flow.

Extract and return the `id` of the `newStamp` created earlier (this will be useful in later flows) and return it from the flow. A `String` should also be returned to represent failures occurring inside the finalize call.

This should look like:

```kotlin
return try {
    // Send the transaction and state to the counterparty and let them sign it
    // Then notarise and record the transaction in both parties' vaults.
    utxoLedgerService.finalize(transaction, listOf(session))
    newStamp.id.toString()
} catch (e: Exception) {
    "Flow failed, message: ${e.message}"
}
```


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
