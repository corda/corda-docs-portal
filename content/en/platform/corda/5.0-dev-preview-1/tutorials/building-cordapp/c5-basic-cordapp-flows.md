---
date: '2021-09-16'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-flows
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1050
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell a group of nodes how to achieve a specific ledger update, such as issuing an asset or making a deposit. Each node has a specific role to play in the transaction and they communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

In this tutorial, top-level flows refer to those that encapsulate the business logic behind the interaction between the users and your CorDapp. They can have multiple subflows and can be started via RPC. However, not all top-level flows govern interactions with users, some could be admin or maintenance flows for example.

The Corda-provided subflows are common tasks performed in Corda, such as gathering signatures from counterparty nodes or notarizing and recording a transaction. As a developer, you only need to implement flows for the business logic of your specific use case.

The `Flow` interface is used to implement a flow. When you use this interface, your business logic will override the `call` method. Flows access version 2 of the Corda API through injectable services using the `@CordaInject` tag. See the [services documentation](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/injectable-services.md) for a list of all services available in the Corda 5 Developer Preview.

Using the `Flow` interface allows you to add the services you need, and leave out those that you don't. This makes your CorDapp much more lightweight, and will reduce development time in future production-ready versions of Corda 5.

This tutorial walks you through writing the three top-level flows you need in your sample CorDapp:

* <a href="#write-the-createandissuemarsvoucher-flow">`CreateAndIssueMarsVoucher`</a>
* <a href="#write-the-createboardingticket-flow">`CreateBoardingTicket`</a>
* <a href="#write-the-redeemboardingticketwithvoucher-flow">`RedeemBoardingTicketWithVoucher`</a>

You will be creating these flows in the `workflows/src/main/kotlin/net/corda/missionMars/flows` directory. Refer to the `TemplateFlow.kt` file in this directory to see a template flow.

## Learning objectives

After you have completed this tutorial, you will know how to create and implement flows in a CorDapp.

## Before you start

Before you start building flows, read:

* [Key concepts: Flows](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/flows/overview.md)
* [Writing flows](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/flows/writing-flows.md)
* [Injectable services](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/injectable-services.md)

## Write the `CreateAndIssueMarsVoucher` flow

The `CreateAndIssueMarsVoucher` flow is used to create a voucher for a trip to Mars and then issue that voucher to a designated party.

### Write the initiating flow

The `CreateAndIssueMarsVoucher` flow action requires interaction between the issuer and the owner. For this reason, you must create an initiator flow and a responder flow.

After you create the `CreateAndIssueMarsVoucher` file, your code should look like this:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

class CreateAndIssueMarsVoucher {
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

public class CreateAndIssueMarsVoucher {

    public static class CreateAndIssueMarsVoucherInitiator {
    }
}
```
{{% /tab %}}

{{< /tabs >}}

#### Add annotations

1. Add an `@InitiatingFlow` annotation. This indicates that this flow is the initiating flow.
2. Add the `@StartableByRPC` annotation. This annotation allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC Client.

So far, your code should look like this:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

import net.corda.v5.application.flows.InitiatingFlow
import net.corda.v5.application.flows.StartableByRPC

@InitiatingFlow
@StartableByRPC
class CreateAndIssueMarsVoucher {
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

public class CreateAndIssueMarsVoucher {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueMarsVoucherInitiator {
    }
}
```
{{% /tab %}}

{{< /tabs >}}


#### Define the `CreateAndIssueMarsVoucherInitiator` class

Define the `CreateAndIssueMarsVoucherInitiator` class to begin writing your flow. If you plan to use the RPC Client, you must add a `@JsonConstructor` to the class. This tells the RPC Client two things:

* The RPC Client must call this constructor.
* The flow can pass in JSON parameters.

As noted in the [Write states](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state.md) tutorial, parameters must be passed in JSON format to return the output over RPC. The flow must take the `RpcStartFlowRequestParameters` parameter to be callable by RPC.

To ensure that values are returned in JSON format, use the new return type `SignedTransactionDigest`. This is a new type that returns transaction IDs, signatures, and states in a JSON format, allowing you to send the type over RPC.

1. Add the class `CreateAndIssueMarsVoucherInitiator`.
2. Add the `@JsonConstructor`.
3. Add the `RpcStartFlowRequestParameters` parameter.
4. Add a `SignedTransactionDigest` return type.

After adding these elements, your code should look like this:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
import net.corda.v5.application.flows.*
import net.corda.v5.ledger.transactions.SignedTransactionDigest

@InitiatingFlow
@StartableByRPC
class CreateAndIssueMarsVoucher2 @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {
    override fun call(): SignedTransactionDigest {
        TODO("Not yet implemented")
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

public class CreateAndIssueMarsVoucher {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueMarsVoucherInitiator implements Flow<SignedTransactionDigest> {

        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public CreateAndIssueMarsVoucherInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {
            TODO("Not yet implemented");
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}


#### Inject services

When writing flows with the Corda 5 Developer Preview, you can inject whichever services you need, and exclude those you don't.

Use the `@CordaInject` annotation to define a field to be set by Corda before the call method is called. See this [list of services](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/injectable-services.md) to find out what services you can add to a CorDapp.

In this sample CorDapp, add these services:

* `FlowEngine`: Provides basic control over a flow it is injected into, such as calling subflows, performing asynchronous tasks and putting the flow to sleep for a period of time. This flow needs `FlowEngine` because you are utilizing subflows such as `FinalityFlow` and `CollectSignaturesFlow`.
* `FlowIdentity`: Obtains the identity of the node running the flow. You must inject this service because one of the output states needs its own identity.
* `FlowMessaging`: Used for creating and closing flow sessions as well as sending and receiving data between flows via a flow session. Use this service to create flow sessions that allow communication between counterparties.
* `TransactionBuilderFactory`: Constructs, verifies and signs the transactions. In this case, it builds a transaction.
* `IdentityService`: Provides methods to retrieve `Party` and `AnonymousParty` instances. You need it because your flow involves counterparties.
* `NotaryLookupService`: Finds information on notaries in the network. Add it because your transaction requires a notary.
* `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers. You need it because in Corda 5 all flow parameters are in the JSON format.

After you've added the services, your code should look like this:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.missionMars.states.MarsVoucher
import net.corda.missionMars.states.TemplateState
import net.corda.systemflows.CollectSignaturesFlow
import net.corda.systemflows.FinalityFlow
import net.corda.systemflows.ReceiveFinalityFlow
import net.corda.systemflows.SignTransactionFlow
import net.corda.v5.application.flows.*
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.flows.flowservices.FlowMessaging
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.IdentityService
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.transactions.SignedTransaction
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory

@InitiatingFlow
@StartableByRPC
class CreateAndIssueMarsVoucherInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.flows.flowservices.FlowMessaging;
import net.corda.v5.application.services.IdentityService;
import net.corda.v5.application.services.json.JsonMarshallingService;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.SignedTransactionDigest;

public class CreateAndIssueMarsVoucher {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueMarsVoucherInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private FlowMessaging flowMessaging;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private IdentityService identityService;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;

        .......
    }
}
```
{{% /tab %}}

{{< /tabs >}}


#### Write your business logic

##### Add the flow implementation

Next you must add the flow implementation to the initiating flow by encapsulating it within the `call` method.

1. Add the `@Suspendable` annotation.
2. Add the `call` method with the return type `SignedTransactionDigest`.
3. Parse your parameters using the `mapOfParams` value. Since the parameters the flow will use come in JSON format, the JSON object must be parsed to extract the parameters so the flow can run.
4. Add appropriate error handling - exceptions must be thrown when required fields (`voucherDesc`, `holder`, `recipientParty`) are not found.
5. Insert the following method for finding the notary: `notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!`.

  {{< note >}}

  In Corda 5, the notary is predefined. You will be "spending" your state with a particular notary tieing that state to it (notary change excepted). Thus, you cannot just pick the first one as the list order may change, especially in a multi-network or app environment where different notaries are whitelisted for different apps. You can find the full status of the notary by starting the network and printing out its status.

  {{< /note >}}

6. Build the output `MarsVoucher` state with a `UniqueIdentifier`.

##### Build the transaction

Your transaction is a proposal to the ledger that the counterparty must agree to. You must ensure that the proposal adheres to the rules of the smart contract and you must sign it before sending it to the counterparty. Also, ensure your transaction is valid from a business perspective. The proposal here is that you'll create a voucher for a trip to Mars and then issue that voucher to a notary and a designated party - Peter.

1. Build the transaction using a `txCommand` and the `transactionBuilderFactory` service you added when injecting services.
2. Verify that the transaction is valid using the `txBuilder.verify` method.
3. Sign the transaction using the `txBuilder.sign` method.
   Once the transaction is signed, you cannot remove a signature from it.

##### Interact with the counterparty

This is where you send the proposal to Peter. When consensus that the transaction's elements are unique and understood is achieved, the transaction is notarized by the notary and stored in both parties' vaults.

1. Send the state to the counterparty and receive it back with their signature. Use the `flowMessaging` service to send the state to the `recipientParty`. Use the `flowEngine` service with the subflow `CollectSignaturesFlow` to get the signature of the counterparty.
   In this specific example, there is no possibility for the counterparty to reject the transaction. However, when writing your CorDapps, you must handle the case where the counterparty rejects it.
2. Get the transaction notarized and recorded in both parties' vaults using `FinalityFlow` with a `fullySignedTx`.
3. Return a `SignedTransactionDigest`. Use the `jsonMarshallingService` to parse the transaction's output. Include the transaction's output states, ID, and signatures.
   This is optional and only relevant to the RPC-invoked flows as a way to return data to an interface.

After adding these elements, your code should look like this:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.missionMars.states.MarsVoucher
import net.corda.missionMars.states.TemplateState
import net.corda.systemflows.CollectSignaturesFlow
import net.corda.systemflows.FinalityFlow
import net.corda.systemflows.ReceiveFinalityFlow
import net.corda.systemflows.SignTransactionFlow
import net.corda.v5.application.flows.*
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.flows.flowservices.FlowMessaging
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.IdentityService
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.transactions.SignedTransaction
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory

@InitiatingFlow
@StartableByRPC
class CreateAndIssueMarsVoucherInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @Suspendable
    override fun call(): SignedTransactionDigest {

        // Parse parameters.
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
        val voucherDesc = with(mapOfParams["voucherDesc"] ?: throw BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherDesc\" missing.")) {
            this
        }
        val target = with(mapOfParams["holder"] ?: throw BadRpcStartFlowRequestException("MarsVoucher State Parameter \"holder\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(target) ?: throw NoSuchElementException("No party found for X500 name $target")

        //Find the notary.
        val notary = notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!

        //Building the output MarsVoucher state.
        val uniqueID = UniqueIdentifier()
        val newVoucher = MarsVoucher(voucherDesc, flowIdentity.ourIdentity, recipientParty, uniqueID)

        //Build transaction.
        val txCommand = Command(MarsVoucherContract.Commands.Issue(), listOf(flowIdentity.ourIdentity.owningKey,recipientParty.owningKey))
        val txBuilder = transactionBuilderFactory.create()
                .setNotary(notary)
                .addOutputState(newVoucher, MarsVoucherContract.ID)
                .addCommand(txCommand)

        // Verify that the transaction is valid.
        txBuilder.verify()

        // Sign the transaction.
        val partSignedTx = txBuilder.sign()

        // Send the state to the counterparty, and receive it back with their signature.
        val otherPartySession = flowMessaging.initiateFlow(recipientParty)
        val fullySignedTx = flowEngine.subFlow(CollectSignaturesFlow(partSignedTx, setOf(otherPartySession)))

        // Notarize and record the transaction in both parties' vaults.
        val notarisedTx = flowEngine.subFlow(FinalityFlow(fullySignedTx, setOf(otherPartySession)))

        return SignedTransactionDigest(
                notarisedTx.id,
                notarisedTx.tx.outputStates.map { output -> jsonMarshallingService.formatJson(output) },
                notarisedTx.sigs
        )
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
public class CreateAndIssueMarsVoucher {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateAndIssueMarsVoucherInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private FlowMessaging flowMessaging;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private IdentityService identityService;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;

        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public CreateAndIssueMarsVoucherInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {

            //Getting Notary
            Party notary = notaryLookupService.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"));

            //Retrieve JSON params
            Map<String, String> parametersMap = jsonMarshallingService.parseJson(params.getParametersInJson(), Map.class);

            //Retrieve State parameter fields from JSON
            Party issuer = flowIdentity.getOurIdentity();
            String voucherDesc;
            if (!parametersMap.containsKey("voucherDesc"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherDesc\" missing.");
            else
                voucherDesc = parametersMap.get("voucherDesc");
            CordaX500Name target;
            if (!parametersMap.containsKey("holder"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"holder\" missing.");
            else
                target = CordaX500Name.parse(parametersMap.get("holder"));
            Party holder;
            holder = identityService.partyFromName(target);

            //Building the output MarsVoucher state
            UniqueIdentifier uniqueID = new UniqueIdentifier();
            MarsVoucher newVoucher = new MarsVoucher(voucherDesc, issuer, holder, uniqueID);
            Command txCommand = new Command(new MarsVoucherContract.Commands.Issue(), Arrays.asList(issuer.getOwningKey(), holder.getOwningKey()));

            //Build transaction
            TransactionBuilder transactionBuilder = transactionBuilderFactory.create()
                    .setNotary(notary)
                    .addOutputState(newVoucher, MarsVoucherContract.ID)
                    .addCommand(txCommand);

            // Verify that the transaction is valid.
            transactionBuilder.verify();

            // Sign the transaction.
            SignedTransaction partialSignedTx = transactionBuilder.sign();

            // Send the state to the counterparty, and receive it back with their signature.
            FlowSession receiverSession = flowMessaging.initiateFlow(holder);

            SignedTransaction fullySignedTx = flowEngine.subFlow(
                    new CollectSignaturesFlow(partialSignedTx, Arrays.asList(receiverSession)));

            // Notarise and record the transaction in both parties' vaults
            SignedTransaction notarisedTx = flowEngine.subFlow(
                    new FinalityFlow(fullySignedTx, Arrays.asList(receiverSession)));

            // Return Json output
            return new SignedTransactionDigest(notarisedTx.getId(),
                    Collections.singletonList(jsonMarshallingService.formatJson(notarisedTx.getTx().getOutputStates().get(0))),
                    notarisedTx.getSigs());
        }

        public FlowEngine getFlowEngine() {
            return flowEngine;
        }

        public NotaryLookupService getNotaryLookup() {
            return this.notaryLookupService;
        }

        public IdentityService getIdentityService() {
            return identityService;
        }

        public JsonMarshallingService getJsonMarshallingService() {
            return jsonMarshallingService;
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Write the responder flow

Now that you've written the initiating flow, write the responder flow that responds to the request to update the ledger. The responder flow in the `CreateAndIssueMarsVoucher` flow is very simple and in the context of the Mission Mars CorDapp, you don't need to verify anything. However, when signing a responder flow in a "real-life context", do not sign it before verifying its contents and ensuring you are accepting what you want to accept.

1. Add the `@InitiatedBy` annotation. This indicates that this is the responder flow.

2. Add in a responder flow.

When the responder receives a half-signed transaction from an initiating party, it is most likely being asked to sign the transaction. The responder flow will go through some checks on the transaction (implemented in the responder flow). If all the checks are passed, it will sign the transaction and return it back to the initiating party. Next, it will add a fully-signed transaction to its local ledger. This is done by the `ReceiveFinalityFlow` subflow.

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatedBy(CreateAndIssueMarsVoucherInitiator::class)
class CreateAndIssueMarsVoucherResponder(val otherPartySession: FlowSession) : Flow<SignedTransaction> {
    @CordaInject
    lateinit var flowEngine: FlowEngine

    @Suspendable
    override fun call(): SignedTransaction {
        val signTransactionFlow = object : SignTransactionFlow(otherPartySession) {
            override fun checkTransaction(stx: SignedTransaction) {

            }
        }
        val txId = flowEngine.subFlow(signTransactionFlow).id
        return flowEngine.subFlow(ReceiveFinalityFlow(otherPartySession, expectedTxId = txId))
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
@InitiatedBy(CreateAndIssueMarsVoucherInitiator.class)
    public static class CreateAndIssueMarsVoucherResponder implements Flow<SignedTransaction> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;

        //private variable
        private FlowSession counterpartySession;

        //Constructor
        public CreateAndIssueMarsVoucherResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            SignedTransaction signedTransaction = flowEngine.subFlow(
                    new CreateAndIssueMarsVoucherResponder.signingTransaction(counterpartySession));
            return flowEngine.subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
        }

        public static class signingTransaction extends SignTransactionFlow {
            signingTransaction(FlowSession counterpartySession) {
                super(counterpartySession);
            }
            @Override
            protected void checkTransaction(@NotNull SignedTransaction stx) {
            }
        }
    }
```
{{% /tab %}}

{{< /tabs >}}

## Write the `CreateBoardingTicket` flow

The `CreateBoardingTicket` flow lets Mars Express self-issue a `BoardingTicket` to later be exchanged with the voucher.

Now that you've written the `CreateAndIssueMarsVoucher` flow, try writing the `CreateBoardingTicket` flow.

You will need these variables:

* `ticketDescription`
* `launchDate`

You must inject these services:

* `FlowEngine`: Provides basic control over a flow it is injected into, such as calling subflows, performing asynchronous tasks and putting the flow to sleep for a period of time. This flow needs `FlowEngine` because you are utilizing subflows such as `FinalityFlow`.
* `FlowIdentity`: Obtains the identity of the node running the flow. You must inject this service because one of the output states needs its own identity.
* `TransactionBuilderFactory`: Used for constructing, verifying and signing the transactions. In this case, it builds a transaction.
* `NotaryLookupService`: Finds information on notaries in the network. Add it because your transaction requires a notary.
* `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers. You need it because in Corda 5 all flow parameters are in the JSON format.

{{< note >}}
This flow only needs an initiating flow; you don't need to include a responder flow. However, you must still add the `@InitiatingFlow` annotation.
{{< /note >}}

After you've written the `CreateBoardingTicket` flow, it should look like this:

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

import net.corda.missionMars.contracts.BoardingTicketContract
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.missionMars.states.BoardingTicket
import net.corda.systemflows.FinalityFlow
import net.corda.v5.application.flows.*
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory
import java.text.DateFormat
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.util.*

@InitiatingFlow
@StartableByRPC
data class CreateBoardingTicketInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService
    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService

    @Suspendable
    override fun call(): SignedTransactionDigest {

        // Parse parameters.
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
        val ticketDescription = with(mapOfParams["ticketDescription"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"ticketDescription\" missing.")) {
            this
        }
        val launchDate = with(mapOfParams["launchDate"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"launchDate\" missing.")) {
            this.toInt()
        }

        //Find notary.
        val notary = notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!

        //Building the output BoardingTicket state.
        val basket = BoardingTicket(description = ticketDescription,marsExpress = flowIdentity.ourIdentity,launchDate = launchDate)


        //Building the transaction.
        val txCommand = Command(BoardingTicketContract.Commands.CreateTicket(), listOf(flowIdentity.ourIdentity.owningKey))
        val txBuilder = transactionBuilderFactory.create()
                .setNotary(notary)
                .addOutputState(basket, BoardingTicketContract.ID)
                .addCommand(txCommand)

        // Verify that the transaction is valid.
        txBuilder.verify()

        // Sign the transaction.
        val partSignedTx = txBuilder.sign()

        // Notarize and record the transaction in both parties' vaults.
        val notarisedTx = flowEngine.subFlow(FinalityFlow(partSignedTx, setOf()))

        return SignedTransactionDigest(
                notarisedTx.id,
                notarisedTx.tx.outputStates.map { output -> jsonMarshallingService.formatJson(output) },
                notarisedTx.sigs
        )
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

import net.corda.missionMars.contracts.BoardingTicketContract;
import net.corda.missionMars.contracts.MarsVoucherContract;
import net.corda.missionMars.states.BoardingTicket;
import net.corda.systemflows.FinalityFlow;
import net.corda.v5.application.flows.*;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.identity.CordaX500Name;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.application.services.IdentityService;
import net.corda.v5.application.services.json.JsonMarshallingService;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.ledger.contracts.Command;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.SignedTransactionDigest;
import net.corda.v5.ledger.transactions.TransactionBuilder;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;
import net.corda.v5.legacyapi.flows.FlowLogic;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;

public class CreateBoardingTicket {

    @InitiatingFlow
    @StartableByRPC
    public static class CreateBoardingTicketInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;

        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public CreateBoardingTicketInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {

            //Getting Notary
            Party notary = notaryLookupService.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"));

            //Retrieve JSON params
            Map<String, String> parametersMap = jsonMarshallingService.parseJson(params.getParametersInJson(), Map.class);

            //Retrieve State parameter fields from JSON
            String ticketDescription;
            if(!parametersMap.containsKey("ticketDescription"))
                throw new BadRpcStartFlowRequestException("BoardingTicket State Parameter \"ticketDescription\" missing.");
            else
                ticketDescription = parametersMap.get("ticketDescription");

            LocalDate launchDate;
            if(!parametersMap.containsKey("launchDate"))
                throw new BadRpcStartFlowRequestException("BoardingTicket State Parameter \"launchDate\" missing.");
            else
                launchDate = LocalDate.parse(parametersMap.get("launchDate"));

            //Building the output MarsVoucher state
            Party marsExpress = flowIdentity.getOurIdentity();
            BoardingTicket ticket = new BoardingTicket(ticketDescription,marsExpress,launchDate);
            Command txCommand = new Command(new BoardingTicketContract.Commands.CreateTicket(), Arrays.asList(marsExpress.getOwningKey()));

            //Build transaction
            TransactionBuilder transactionBuilder = transactionBuilderFactory.create()
                    .setNotary(notary)
                    .addOutputState(ticket, BoardingTicketContract.ID)
                    .addCommand(txCommand);


            // Verify that the transaction is valid.
            transactionBuilder.verify();

            // Sign the transaction.
            SignedTransaction partialSignedTx = transactionBuilder.sign();

            // Notarise and record the transaction in both parties' vaults
            SignedTransaction notarisedTx = flowEngine.subFlow(
                    new FinalityFlow(partialSignedTx, Collections.emptyList()));

            // Return Json output
            return new SignedTransactionDigest(notarisedTx.getId(),
                    Collections.singletonList(jsonMarshallingService.formatJson(notarisedTx.getTx().getOutputStates().get(0))),
                    notarisedTx.getSigs());
        }
        public FlowEngine getFlowEngine() {
            return flowEngine;
        }

        public NotaryLookupService getNotaryLookup() {
            return this.notaryLookupService;
        }

        public JsonMarshallingService getJsonMarshallingService() {
            return jsonMarshallingService;
        }
    }

}
```
{{% /tab %}}

{{< /tabs >}}

## Write the `GiftVoucherToFriend` flow

In Corda, you can transfer a state to another party on the network. The `GiftVoucherToFriend` flow lets you transfer the ownership of the issued voucher to another person.

Now that you've written the `CreateAndIssueMarsVoucher` and `CreateBoardingTicket` flows, try writing the `GiftVoucherToFriend` flow.

You will need these variables:

* `voucherID`: ID of the issued voucher whose ownership is to be transferred.
* `holder`: The new voucher owner.

You must inject these services:

* `FlowEngine`: Provides basic control over a flow it is injected into, such as calling subflows, performing asynchronous tasks and putting the flow to sleep for a period of time. This flow needs `FlowEngine` because you are utilizing subflows such as `FinalityFlow`.
* `FlowIdentity`: Obtains the identity of the node running the flow. You must inject this service because one of the output states needs its own identity.
* `FlowMessaging`: Used for creating and closing flow sessions as well as sending and receiving data between flows via a flow session. Use this service to create flow sessions that allow communication between counterparties.
* `TransactionBuilderFactory`: Used for constructing, verifying, and signing transactions. In this case, it builds a transaction.
* `IdentityService`: Provides methods to retrieve `Party` and `AnonymousParty` instances. You need it because your flow involves counterparties.
* `NotaryLookupService`: Finds information on notaries in the network. Add it because your transaction requires a notary.
* `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers. You need it because in Corda 5 all flow parameters are in JSON format.
* `PersistenceService`: Provides an API for interacting with the database. It has functions mirroring Java’s `EntityManager` for working with entities. Also, it provides functions for executing predefined named queries and polling for results. It hides the complexity of asynchronously interacting with the database which, in a high-availability environment, could be running on a separate process.

{{< note >}}
Like the `CreateAndIssueMarsVoucher` flow, the `GiftVoucherToFriend` flow needs a [responder flow](#write-the-responder-flow) that responds to the request to update the ledger.

You also need to query the `MarsVoucher` and the `BoardingTicket`. Refer to the section on [implementing queries](#implement-queries) for the `RedeemBoardingTicketWithVoucher` for guidance.
{{< /note >}}

After you've written the `GiftVoucherToFriend` flow, it should look like this:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin

package net.corda.missionMars.flows

import net.corda.missionMars.contracts.BoardingTicketContract
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.missionMars.states.MarsVoucher
import net.corda.systemflows.CollectSignaturesFlow
import net.corda.systemflows.FinalityFlow
import net.corda.systemflows.ReceiveFinalityFlow
import net.corda.systemflows.SignTransactionFlow
import net.corda.v5.application.flows.*
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.flows.flowservices.FlowMessaging
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.IdentityService
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.application.services.persistence.PersistenceService
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.util.seconds
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.contracts.StateAndRef
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.services.vault.StateStatus
import net.corda.v5.ledger.transactions.SignedTransaction
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory
import java.util.*
import kotlin.NoSuchElementException

@InitiatingFlow
@StartableByRPC
class GiftVoucherToFriendInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): SignedTransactionDigest {

        // parse parameters
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
        val voucherID = with(mapOfParams["voucherID"] ?: throw BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.")) {
            this
        }
        val holder = with(mapOfParams["holder"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"holder\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(holder) ?: throw NoSuchElementException("No party found for X500 name $holder")

        //Query the MarsVoucher & the boardingTicket
        val cursor = persistenceService.query<StateAndRef<MarsVoucher>>(
                "LinearState.findByUuidAndStateStatus",
                mapOf(
                        "uuid" to UUID.fromString(voucherID),
                        "stateStatus" to StateStatus.UNCONSUMED
                ),
                "Corda.IdentityStateAndRefPostProcessor"
        )
        val marsVoucherStateAndRef = cursor.poll(100, 20.seconds).values.first()
        val inputMarsVoucher = marsVoucherStateAndRef.state.data

        if (inputMarsVoucher.holder != flowIdentity.ourIdentity){
            throw FlowException("Only the voucher current holder can initiate a gifting transaction")
        }

        //Building the output
        val outputMarsVoucher = inputMarsVoucher.changeOwner(recipientParty)

        //Get the Notary from inputRef
        val notary = marsVoucherStateAndRef.state.notary

        //Building the transaction
        val signers = (inputMarsVoucher.participants + recipientParty).map { it.owningKey }
        val txCommand = Command(MarsVoucherContract.Commands.Transfer(), signers)
        val txBuilder = transactionBuilderFactory.create()
                .setNotary(notary)
                .addInputState(marsVoucherStateAndRef)
                .addOutputState(outputMarsVoucher, MarsVoucherContract.ID)
                .addCommand(txCommand)

        // Verify that the transaction is valid.
        txBuilder.verify()

        // Sign the transaction.
        val partSignedTx = txBuilder.sign()

        // Send the state to the counterparty, and receive it back with their signature.
        val sessions = (inputMarsVoucher.participants - flowIdentity.ourIdentity + recipientParty).map { flowMessaging.initiateFlow(it) }.toSet()
        val fullySignedTx = flowEngine.subFlow(
                CollectSignaturesFlow(
                        partSignedTx, sessions,
                )
        )
        // Notarise and record the transaction in both parties' vaults.
        val notarisedTx = flowEngine.subFlow(
                FinalityFlow(
                        fullySignedTx, sessions,
                )
        )

        return SignedTransactionDigest(
                notarisedTx.id,
                notarisedTx.tx.outputStates.map { it -> jsonMarshallingService.formatJson(it) },
                notarisedTx.sigs
        )
    }


    }

@InitiatedBy(GiftVoucherToFriendInitiator::class)
class GiftVoucherToFriendResponder(val otherPartySession: FlowSession) : Flow<SignedTransaction> {
    @CordaInject
    lateinit var flowEngine: FlowEngine

    @Suspendable
    override fun call(): SignedTransaction {
        val signTransactionFlow = object : SignTransactionFlow(otherPartySession) {
            override fun checkTransaction(stx: SignedTransaction) {

            }
        }
        val txId = flowEngine.subFlow(signTransactionFlow).id
        return flowEngine.subFlow(ReceiveFinalityFlow(otherPartySession, expectedTxId = txId))
    }
}

```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

import net.corda.missionMars.contracts.BoardingTicketContract;
import net.corda.missionMars.contracts.MarsVoucherContract;
import net.corda.missionMars.states.MarsVoucher;
import net.corda.systemflows.CollectSignaturesFlow;
import net.corda.systemflows.FinalityFlow;
import net.corda.systemflows.ReceiveFinalityFlow;
import net.corda.systemflows.SignTransactionFlow;
import net.corda.v5.application.flows.*;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.flows.flowservices.FlowMessaging;
import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.CordaX500Name;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.application.services.IdentityService;
import net.corda.v5.application.services.json.JsonMarshallingService;
import net.corda.v5.application.services.persistence.PersistenceService;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.base.stream.Cursor;
import net.corda.v5.ledger.contracts.StateAndRef;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.services.vault.StateStatus;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.SignedTransactionDigest;
import net.corda.v5.ledger.transactions.TransactionBuilder;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;
import net.corda.v5.legacyapi.flows.FlowLogic;
import org.jetbrains.annotations.NotNull;

import java.time.Duration;
import java.util.*;

public class GiftVoucherToFriend {

    @InitiatingFlow
    @StartableByRPC
    public static class GiftVoucherToFriendInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private FlowMessaging flowMessaging;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private IdentityService identityService;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;
        @CordaInject
        private PersistenceService persistenceService;
        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public GiftVoucherToFriendInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {

            //Retrieve JSON params
            Map<String, String> parametersMap = jsonMarshallingService.parseJson(params.getParametersInJson(), Map.class);

            //Retrieve State parameter fields from JSON
            //Voucher ID
            String voucherID;
            if(!parametersMap.containsKey("voucherID"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.");
            else
                voucherID = parametersMap.get("voucherID");
            //RecipientParty
            CordaX500Name holder;
            if(!parametersMap.containsKey("holder"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"holder\" missing.");
            else
                holder = CordaX500Name.parse(parametersMap.get("holder"));
            Party recipientParty;
            recipientParty = identityService.partyFromName(holder);

            //Query the MarsVoucher & the boardingTicket
            Map <String, Object> namedParameters = new LinkedHashMap<String,Object>();
            namedParameters.put("uuid", UUID.fromString(voucherID));
            namedParameters.put("stateStatus", StateStatus.UNCONSUMED);
            Cursor cursor = persistenceService.query(
                    "LinearState.findByUuidAndStateStatus",
                    namedParameters,
                    "Corda.IdentityStateAndRefPostProcessor"
            );
            StateAndRef<MarsVoucher> marsVoucherStateAndRef = (StateAndRef<MarsVoucher>) cursor.poll(100, Duration.ofSeconds(20)).getValues().get(0);
            MarsVoucher inputMarsVoucher = marsVoucherStateAndRef.getState().getData();

            //Check if the initiator is indeed the holder of the mars voucher
            if(!(inputMarsVoucher.getHolder().getOwningKey().equals(flowIdentity.getOurIdentity().getOwningKey())))
                throw new FlowException("Only the voucher current holder can initiate a gifting transaction");

            //Building the output
            MarsVoucher outputMarsVoucher = inputMarsVoucher.changeOwner(recipientParty);

            //Get the Notary from inputRef
            Party notary = marsVoucherStateAndRef.getState().getNotary();

            TransactionBuilder transactionBuilder = transactionBuilderFactory.create()
                    .setNotary(notary)
                    .addInputState(marsVoucherStateAndRef)
                    .addOutputState(outputMarsVoucher, MarsVoucherContract.ID)
                    .addCommand(new MarsVoucherContract.Commands.Transfer(),
                            Arrays.asList(recipientParty.getOwningKey(),
                                    inputMarsVoucher.getHolder().getOwningKey(),
                                    inputMarsVoucher.getIssuer().getOwningKey()));

            // Verify that the transaction is valid.
            transactionBuilder.verify();

            // Sign the transaction.
            SignedTransaction partialSignedTx = transactionBuilder.sign();

            // Send the state to the counterparty, and receive it back with their signature.
            List<FlowSession> receiverSession = new ArrayList<>();

            for (AbstractParty participant: inputMarsVoucher.getParticipants()) {
                Party partyToInitiateFlow = (Party) participant;
                if (!partyToInitiateFlow.getOwningKey().equals(flowIdentity.getOurIdentity().getOwningKey())) {
                    receiverSession.add(flowMessaging.initiateFlow(partyToInitiateFlow));
                }
            }
            receiverSession.add(flowMessaging.initiateFlow(recipientParty));

            SignedTransaction fullySignedTx = flowEngine.subFlow(
                    new CollectSignaturesFlow(partialSignedTx, receiverSession));

            // Notarise and record the transaction in both parties' vaults
            SignedTransaction notarisedTx = flowEngine.subFlow(
                    new FinalityFlow(fullySignedTx, receiverSession));

            // Return Json output
            return new SignedTransactionDigest(notarisedTx.getId(),
                    Collections.singletonList(jsonMarshallingService.formatJson(notarisedTx.getTx().getOutputStates().get(0))),
                    notarisedTx.getSigs());
        }
    }


    @InitiatedBy(GiftVoucherToFriendInitiator.class)
    public static class GiftVoucherToFriendResponder implements Flow<SignedTransaction> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;

        //private variable
        private FlowSession counterpartySession;

        //Constructor
        public GiftVoucherToFriendResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            SignedTransaction signedTransaction = flowEngine.subFlow(
                    new CreateAndIssueMarsVoucher.CreateAndIssueMarsVoucherResponder.signingTransaction(counterpartySession));
            return flowEngine.subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
        }

        public static class signingTransaction extends SignTransactionFlow {
            signingTransaction(FlowSession counterpartySession) {
                super(counterpartySession);
            }
            @Override
            protected void checkTransaction(@NotNull SignedTransaction stx) {
            }
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}

## Write the `RedeemBoardingTicketWithVoucher` flow

The `RedeemBoardingTicketWithVoucher` flow lets Peter redeem his `MarsVoucher` for a `BoardingTicket` and take his trip to Mars.

Since this flow is performing a redemption, you must have both an initiating flow and a responder flow.

### Write the initiating flow

Start writing your initiating flow following the same process used when writing the <a href="#write-the-createandissuemarsvoucher-flow">`CreateAndIssueMarsVoucher`</a> flow.

1. Add these annotations:
   * `@InitiatingFlow`: Indicates that this flow is the initiating flow.
   * `@StartableByRPC`: Allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC Client.

2. Define the `RedeemBoardingTicketWithVoucherInitiator` class with a `@JsonConstructor`, `RpcStartFlowRequestParameters`, and returning a `SignedTransactionDigest`.
3. Inject these services:

    * `FlowEngine`: Provides basic control over a flow it is injected into, such as calling subflows, performing asynchronous tasks and putting the flow to sleep for a period of time. This flow needs `FlowEngine` because you are utilizing subflows such as `FinalityFlow` and `CollectSignaturesFlow`.
    * `FlowIdentity`: Obtains the identity of the node running the flow. You must inject this service because one of the output states needs its own identity.
    * `FlowMessaging`: Used for creating and closing flow sessions as well as sending and receiving data between flows via a flow session. Use this service to create flow sessions that allow communication between counterparties.
    * `TransactionBuilderFactory`: Used for constructing, verifying and signing the transactions. In this case, it builds a transaction.
    * `IdentityService`: Provides methods to retrieve `Party` and `AnonymousParty` instances. You need it because your flow involves counterparties.
    * `NotaryLookupService`: Finds information on notaries in the network. Add it because your transaction requires a notary.
    * `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers. You need it because in Corda 5 all flow parameters are in the JSON format.
    * `PersistenceService`: Provides an API for interacting with the database. It has functions mirroring Java's `EntityManager` for working with entities. Also, it provides functions for executing predefined named queries and polling for results. It hides the complexity of asynchronously interacting with the database which, in a high-availability environment, could be running on a separate process.

4. Add the `@Suspendable` annotation.
5. Encapsulate the flow implementation into a call method that returns the `SignedTransactionDigest`.

6. Parse these parameters and add exceptions for when these parameters are incorrect or not present:
    * `voucherID`
    * `holder`
    * `recipientParty`

7. Insert the following method for finding the notary: `notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!`

#### Implement queries

In the implementation of this initiating flow, you must query the `MarsVoucher` and the `BoardingTicket`. You can use the `PersistenceService` to perform these queries.

##### Add a query for the `MarsVoucher`

1. Use a `cursor` to point to a specific line in the query results.
2. Add a `persistenceService.query` to get the `StateAndRef` of the `MarsVoucher`.
3. Use the [predefined query](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#query-for-states-when-your-state-does-not-have-a-mapped-schema) `findByUuidAndStateStatus` to find the `MarsVoucher` you need by the state's unique identifier and status.
4. To return a `StateAndRef`, use Corda's built-in `Corda.IdentityStateAndRefPostProcessor`.
5. To return a `ContractState`, use Corda's built-in `IdentityContractStatePostProcessor`.
6. Use the `poll` function to set a maximum poll size and timeout duration for the query.

##### Add a query for the `BoardingTicket`

1. Use an additional cursor (`cursor2`) to point to a specific line in the query results.
2. Add a `persistenceService.query` to get the `StateAndRef` of the `BoardingTicket`.
3. Use the [predefined query](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#query-for-states-when-your-state-does-not-have-a-mapped-schema) `findByStateStatusAndContractStateClassName` to find the `BoardingTicket` you need by the state's status and contract state class name.
4. To return a `StateAndRef`, use Corda's built-in `Corda.IdentityStateAndRefPostProcessor`.
5. To return a `ContractState`, use Corda's built-in `IdentityContractStatePostProcessor`.
6. Use the `poll` function to set a maximum poll size and timeout duration for the query.

Your code should now look like this:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
@InitiatingFlow
@StartableByRPC
class RedeemBoardingTicketWithVoucherInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService
    @CordaInject
    lateinit var persistenceService: PersistenceService


    @Suspendable
    override fun call(): SignedTransactionDigest {

        // Parse parameters.
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
        val voucherID = with(mapOfParams["voucherID"] ?: throw BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.")) {
            this
        }
        val holder = with(mapOfParams["holder"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"holder\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(holder) ?: throw NoSuchElementException("No party found for X500 name $holder")

        //Find notary.
        val notary = notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!

        //Query the MarsVoucher and the boardingTicket.
        val cursor = persistenceService.query<StateAndRef<MarsVoucher>>(
                "LinearState.findByUuidAndStateStatus",
                mapOf(
                        "uuid" to UUID.fromString(voucherID),
                        "stateStatus" to StateStatus.UNCONSUMED
                ),
                "Corda.IdentityStateAndRefPostProcessor"
        )
        val marsVoucherStateAndRef = cursor.poll(100, 20.seconds).values.first()

        val cursor2 = persistenceService.query<StateAndRef<BoardingTicket>>(
                "VaultState.findByStateStatusAndContractStateClassName",
                mapOf(
                        "contractStateClassName" to BoardingTicket::class.java.name,
                        "stateStatus" to StateStatus.UNCONSUMED
                ),
                IdentityContractStatePostProcessor.POST_PROCESSOR_NAME
        )
        val boardingTicketStateAndRef= cursor2.poll(100, 20.seconds).values.first()
        val originalBoardingTicketState= boardingTicketStateAndRef.state.data
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

import net.corda.missionMars.contracts.BoardingTicketContract;
import net.corda.missionMars.contracts.MarsVoucherContract;
import net.corda.missionMars.states.MarsVoucher;
import net.corda.systemflows.CollectSignaturesFlow;
import net.corda.systemflows.FinalityFlow;
import net.corda.systemflows.ReceiveFinalityFlow;
import net.corda.systemflows.SignTransactionFlow;
import net.corda.v5.application.flows.*;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.flows.flowservices.FlowMessaging;
import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.CordaX500Name;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.application.services.IdentityService;
import net.corda.v5.application.services.json.JsonMarshallingService;
import net.corda.v5.application.services.persistence.PersistenceService;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.base.stream.Cursor;
import net.corda.v5.ledger.contracts.StateAndRef;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.services.vault.StateStatus;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.SignedTransactionDigest;
import net.corda.v5.ledger.transactions.TransactionBuilder;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;
import net.corda.v5.legacyapi.flows.FlowLogic;
import org.jetbrains.annotations.NotNull;

import java.time.Duration;
import java.util.*;

public class GiftVoucherToFriend {

    @InitiatingFlow
    @StartableByRPC
    public static class GiftVoucherToFriendInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private FlowMessaging flowMessaging;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private IdentityService identityService;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;
        @CordaInject
        private PersistenceService persistenceService;
        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public GiftVoucherToFriendInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {

            //Retrieve JSON params
            Map<String, String> parametersMap = jsonMarshallingService.parseJson(params.getParametersInJson(), Map.class);

            //Retrieve State parameter fields from JSON
            //Voucher ID
            String voucherID;
            if(!parametersMap.containsKey("voucherID"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.");
            else
                voucherID = parametersMap.get("voucherID");
            //RecipientParty
            CordaX500Name holder;
            if(!parametersMap.containsKey("holder"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"holder\" missing.");
            else
                holder = CordaX500Name.parse(parametersMap.get("holder"));
            Party recipientParty;
            recipientParty = identityService.partyFromName(holder);

            //Query the MarsVoucher & the boardingTicket
            Map <String, Object> namedParameters = new LinkedHashMap<String,Object>();
            namedParameters.put("uuid", UUID.fromString(voucherID));
            namedParameters.put("stateStatus", StateStatus.UNCONSUMED);
            Cursor cursor = persistenceService.query(
                    "LinearState.findByUuidAndStateStatus",
                    namedParameters,
                    "Corda.IdentityStateAndRefPostProcessor"
            );
            StateAndRef<MarsVoucher> marsVoucherStateAndRef = (StateAndRef<MarsVoucher>) cursor.poll(100, Duration.ofSeconds(20)).getValues().get(0);
            MarsVoucher inputMarsVoucher = marsVoucherStateAndRef.getState().getData();

            //Check if the initiator is indeed the holder of the mars voucher
            if(!(inputMarsVoucher.getHolder().getOwningKey().equals(flowIdentity.getOurIdentity().getOwningKey())))
                throw new FlowException("Only the voucher current holder can initiate a gifting transaction");

            //Building the output
            MarsVoucher outputMarsVoucher = inputMarsVoucher.changeOwner(recipientParty);

            //Get the Notary from inputRef
            Party notary = marsVoucherStateAndRef.getState().getNotary();

            TransactionBuilder transactionBuilder = transactionBuilderFactory.create()
                    .setNotary(notary)
                    .addInputState(marsVoucherStateAndRef)
                    .addOutputState(outputMarsVoucher, MarsVoucherContract.ID)
                    .addCommand(new MarsVoucherContract.Commands.Transfer(),
                            Arrays.asList(recipientParty.getOwningKey(),
                                    inputMarsVoucher.getHolder().getOwningKey(),
                                    inputMarsVoucher.getIssuer().getOwningKey()));

            // Verify that the transaction is valid.
            transactionBuilder.verify();

            // Sign the transaction.
            SignedTransaction partialSignedTx = transactionBuilder.sign();

            // Send the state to the counterparty, and receive it back with their signature.
            List<FlowSession> receiverSession = new ArrayList<>();

            for (AbstractParty participant: inputMarsVoucher.getParticipants()) {
                Party partyToInitiateFlow = (Party) participant;
                if (!partyToInitiateFlow.getOwningKey().equals(flowIdentity.getOurIdentity().getOwningKey())) {
                    receiverSession.add(flowMessaging.initiateFlow(partyToInitiateFlow));
                }
            }
            receiverSession.add(flowMessaging.initiateFlow(recipientParty));

            SignedTransaction fullySignedTx = flowEngine.subFlow(
                    new CollectSignaturesFlow(partialSignedTx, receiverSession));

            // Notarise and record the transaction in both parties' vaults
            SignedTransaction notarisedTx = flowEngine.subFlow(
                    new FinalityFlow(fullySignedTx, receiverSession));

            // Return Json output
            return new SignedTransactionDigest(notarisedTx.getId(),
                    Collections.singletonList(jsonMarshallingService.formatJson(notarisedTx.getTx().getOutputStates().get(0))),
                    notarisedTx.getSigs());
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}

#### Finish the initiating flow

Finish the initiating flow by continuing with the same steps you followed when creating the first two flows.

1. Build the transaction's output. Output the `BoardingTicket` and change the owner.
2. Build the transaction using the `TransactionBuilderFactory` service.
3. Verify that the transaction is valid with the `txBuilder.verify` method.
4. Sign the transaction using the `txBuilder.sign` method.
   Once the transaction is signed, you cannot remove a signature from it.
5. Send the state to Peter using the `flowMessaging` service, then receive it using the `FlowEngine` and the subflow `CollectSignaturesFlow`.
6. Get the transaction notarized in both parties' vaults using the `FlowEngine` service and the subflow `FinalityFlow`.
   After the transaction is performed, the issuer will have the consumed state in their vault and they won't have a reference to the new state. The new state generated by this transaction will be stored in the counterparty's vault.
7. Return a `SignedTransactionDigest`.


### Write the responder flow

Now that you've written the initiating flow, try writing the responder flow.
Once you're done, your code should look like this:

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.flows

import net.corda.missionMars.contracts.BoardingTicketContract
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.missionMars.states.BoardingTicket
import net.corda.missionMars.states.MarsVoucher
import net.corda.systemflows.CollectSignaturesFlow
import net.corda.systemflows.FinalityFlow
import net.corda.systemflows.ReceiveFinalityFlow
import net.corda.systemflows.SignTransactionFlow
import net.corda.v5.application.flows.*
import net.corda.v5.application.flows.flowservices.FlowEngine
import net.corda.v5.application.flows.flowservices.FlowIdentity
import net.corda.v5.application.flows.flowservices.FlowMessaging
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.application.injection.CordaInject
import net.corda.v5.application.services.IdentityService
import net.corda.v5.application.services.json.JsonMarshallingService
import net.corda.v5.application.services.json.parseJson
import net.corda.v5.application.services.persistence.PersistenceService
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.contracts.StateAndRef
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.services.vault.StateStatus
import net.corda.v5.ledger.transactions.SignedTransaction
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory
import java.util.*
import kotlin.NoSuchElementException
import net.corda.v5.base.util.seconds
import net.corda.v5.ledger.services.vault.IdentityContractStatePostProcessor

@InitiatingFlow
@StartableByRPC
class RedeemBoardingTicketWithVoucherInitiator @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<SignedTransactionDigest> {

    @CordaInject
    lateinit var flowEngine: FlowEngine
    @CordaInject
    lateinit var flowIdentity: FlowIdentity
    @CordaInject
    lateinit var flowMessaging: FlowMessaging
    @CordaInject
    lateinit var transactionBuilderFactory: TransactionBuilderFactory
    @CordaInject
    lateinit var identityService: IdentityService
    @CordaInject
    lateinit var notaryLookup: NotaryLookupService
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService
    @CordaInject
    lateinit var persistenceService: PersistenceService


    @Suspendable
    override fun call(): SignedTransactionDigest {

        // Parse parameters.
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
        val voucherID = with(mapOfParams["voucherID"] ?: throw BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.")) {
            this
        }
        val holder = with(mapOfParams["holder"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"holder\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(holder) ?: throw NoSuchElementException("No party found for X500 name $holder")

        //Find notary.
        val notary = notaryLookup.getNotary(CordaX500Name.parse("O=notary, L=London, C=GB"))!!

        //Query the MarsVoucher and the boardingTicket.
        val cursor = persistenceService.query<StateAndRef<MarsVoucher>>(
                "LinearState.findByUuidAndStateStatus",
                mapOf(
                        "uuid" to UUID.fromString(voucherID),
                        "stateStatus" to StateStatus.UNCONSUMED
                ),
                "Corda.IdentityStateAndRefPostProcessor"
        )
        val marsVoucherStateAndRef = cursor.poll(100, 20.seconds).values.first()

        val cursor2 = persistenceService.query<StateAndRef<BoardingTicket>>(
                "VaultState.findByStateStatusAndContractStateClassName",
                mapOf(
                        "contractStateClassName" to BoardingTicket::class.java.name,
                        "stateStatus" to StateStatus.UNCONSUMED
                ),
                IdentityContractStatePostProcessor.POST_PROCESSOR_NAME
        )
        val boardingTicketStateAndRef= cursor2.poll(100, 20.seconds).values.first()
        val originalBoardingTicketState= boardingTicketStateAndRef.state.data

        //Building the output.
        val outputBoardingTicket = originalBoardingTicketState.changeOwner(recipientParty)

        //Building the transaction.
        val txCommand = Command(BoardingTicketContract.Commands.RedeemTicket(), listOf(flowIdentity.ourIdentity.owningKey,recipientParty.owningKey))
        val txBuilder = transactionBuilderFactory.create()
                .setNotary(notary)
                .addInputState(marsVoucherStateAndRef)
                .addInputState(boardingTicketStateAndRef)
                .addOutputState(outputBoardingTicket, BoardingTicketContract.ID)
                .addCommand(txCommand)

        // Verify that the transaction is valid.
        txBuilder.verify()

        // Sign the transaction.
        val partSignedTx = txBuilder.sign()

        // Send the state to the counterparty, and receive it back with their signature.
        val otherPartySession = flowMessaging.initiateFlow(recipientParty)
        val fullySignedTx = flowEngine.subFlow(
                CollectSignaturesFlow(
                        partSignedTx, setOf(otherPartySession),
                )
        )

        // Notarize and record the transaction in both parties' vaults.
        val notarisedTx = flowEngine.subFlow(
                FinalityFlow(
                        fullySignedTx, setOf(otherPartySession),
                )
        )

        return SignedTransactionDigest(
                notarisedTx.id,
                notarisedTx.tx.outputStates.map { it -> jsonMarshallingService.formatJson(it) },
                notarisedTx.sigs
        )
    }
}


@InitiatedBy(RedeemBoardingTicketWithVoucherInitiator::class)
class RedeemBoardingTicketWithVoucherResponder(val otherPartySession: FlowSession) : Flow<SignedTransaction> {
    @CordaInject
    lateinit var flowEngine: FlowEngine

    @Suspendable
    override fun call(): SignedTransaction {
        val signTransactionFlow = object : SignTransactionFlow(otherPartySession) {
            override fun checkTransaction(stx: SignedTransaction) {

            }
        }
        val txId = flowEngine.subFlow(signTransactionFlow).id
        return flowEngine.subFlow(ReceiveFinalityFlow(otherPartySession, expectedTxId = txId))
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.flows;

import net.corda.missionMars.contracts.BoardingTicketContract;
import net.corda.missionMars.states.BoardingTicket;
import net.corda.missionMars.states.MarsVoucher;
import net.corda.systemflows.CollectSignaturesFlow;
import net.corda.systemflows.FinalityFlow;
import net.corda.systemflows.ReceiveFinalityFlow;
import net.corda.systemflows.SignTransactionFlow;
import net.corda.v5.application.flows.*;
import net.corda.v5.application.flows.flowservices.FlowEngine;
import net.corda.v5.application.flows.flowservices.FlowIdentity;
import net.corda.v5.application.flows.flowservices.FlowMessaging;
import net.corda.v5.application.identity.CordaX500Name;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.application.services.IdentityService;
import net.corda.v5.application.services.json.JsonMarshallingService;
import net.corda.v5.application.services.persistence.PersistenceService;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.base.stream.Cursor;
import net.corda.v5.ledger.contracts.StateAndRef;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.services.vault.SetBasedVaultQueryFilter;
import net.corda.v5.ledger.services.vault.StateStatus;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.SignedTransactionDigest;
import net.corda.v5.ledger.transactions.TransactionBuilder;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;
import net.corda.v5.legacyapi.flows.FlowLogic;
import org.jetbrains.annotations.NotNull;

import java.time.Duration;
import java.util.*;

public class RedeemBoardingTicketWithVoucher {

    @InitiatingFlow
    @StartableByRPC
    public static class RedeemBoardingTicketWithVoucherInitiator implements Flow<SignedTransactionDigest> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;
        @CordaInject
        private FlowIdentity flowIdentity;
        @CordaInject
        private FlowMessaging flowMessaging;
        @CordaInject
        private TransactionBuilderFactory transactionBuilderFactory;
        @CordaInject
        private IdentityService identityService;
        @CordaInject
        private NotaryLookupService notaryLookupService;
        @CordaInject
        private JsonMarshallingService jsonMarshallingService;
        @CordaInject
        private PersistenceService persistenceService;

        //Private variable
        private RpcStartFlowRequestParameters params;

        //Constructor
        @JsonConstructor
        public RedeemBoardingTicketWithVoucherInitiator(RpcStartFlowRequestParameters params) {
            this.params = params;
        }

        @Override
        @Suspendable
        public SignedTransactionDigest call() {

            //Retrieve JSON params
            Map<String, String> parametersMap = jsonMarshallingService.parseJson(params.getParametersInJson(), Map.class);

            //Retrieve State parameter fields from JSON

            //Voucher ID
            String voucherID;
            if(!parametersMap.containsKey("voucherID"))
                throw new BadRpcStartFlowRequestException("MarsVoucher State Parameter \"voucherID\" missing.");
            else
                voucherID = parametersMap.get("voucherID");
            //RecipientParty
            CordaX500Name holder;
            if(!parametersMap.containsKey("holder"))
                throw new BadRpcStartFlowRequestException("BoardingTicket State Parameter \"holder\" missing.");
            else
                holder = CordaX500Name.parse(parametersMap.get("holder"));
            Party recipientParty;
            recipientParty = identityService.partyFromName(holder);

            //Query the MarsVoucher & the boardingTicket
            Map <String, Object> namedParameters = new LinkedHashMap<String,Object>();
            namedParameters.put("uuid", UUID.fromString(voucherID));
            namedParameters.put("stateStatus", StateStatus.UNCONSUMED);
            Cursor cursor = persistenceService.query(
                    "LinearState.findByUuidAndStateStatus",
                    namedParameters,
                    "Corda.IdentityStateAndRefPostProcessor"
            );
            StateAndRef<MarsVoucher> marsVoucherStateAndRef = (StateAndRef<MarsVoucher>) cursor.poll(100, Duration.ofSeconds(20)).getValues().get(0);

            Map <String, Object> namedParameters2 = new LinkedHashMap<String,Object>();
            namedParameters2.put("stateStatus", StateStatus.UNCONSUMED);
            Set<String> ContractStateClassName = new LinkedHashSet<>();
            ContractStateClassName.add(BoardingTicket.class.getName());

            Cursor cursor2 = persistenceService.query(
                    "VaultState.findByStateStatus",
                    namedParameters2,
                    new SetBasedVaultQueryFilter.Builder()
                            .withContractStateClassNames(ContractStateClassName)
                            .build(),
                    "Corda.IdentityStateAndRefPostProcessor"
            );
            StateAndRef<BoardingTicket> boardingTicketStateAndRef = (StateAndRef<BoardingTicket>) cursor2.poll(100, Duration.ofSeconds(20)).getValues().get(0);
            BoardingTicket originalBoardingTicketState= boardingTicketStateAndRef.getState().getData();

            //Building the output
            BoardingTicket outputBoardingTicket = originalBoardingTicketState.changeOwner(recipientParty);

            //Getting Notary
            Party notary = boardingTicketStateAndRef.getState().getNotary();

            //Build transaction
            TransactionBuilder transactionBuilder = transactionBuilderFactory.create()
                    .setNotary(notary)
                    .addInputState(marsVoucherStateAndRef)
                    .addInputState(boardingTicketStateAndRef)
                    .addOutputState(outputBoardingTicket, BoardingTicketContract.ID)
                    .addCommand(new BoardingTicketContract.Commands.RedeemTicket(),
                            Arrays.asList(recipientParty.getOwningKey(),flowIdentity.getOurIdentity().getOwningKey()));

            // Verify that the transaction is valid.
            transactionBuilder.verify();

            // Sign the transaction.
            SignedTransaction partialSignedTx = transactionBuilder.sign();

            // Send the state to the counterparty, and receive it back with their signature.
            FlowSession receiverSession = flowMessaging.initiateFlow(recipientParty);

            SignedTransaction fullySignedTx = flowEngine.subFlow(
                    new CollectSignaturesFlow(partialSignedTx, Arrays.asList(receiverSession)));

            // Notarise and record the transaction in both parties' vaults
            SignedTransaction notarisedTx = flowEngine.subFlow(
                    new FinalityFlow(fullySignedTx, Arrays.asList(receiverSession)));

            // Return Json output
            return new SignedTransactionDigest(notarisedTx.getId(),
                    Collections.singletonList(jsonMarshallingService.formatJson(notarisedTx.getTx().getOutputStates().get(0))),
                    notarisedTx.getSigs());
        }
    }


    @InitiatedBy(RedeemBoardingTicketWithVoucherInitiator.class)
    public static class RedeemBoardingTicketWithVoucherResponder implements Flow<SignedTransaction> {

        //Node Injectables
        @CordaInject
        private FlowEngine flowEngine;

        //private variable
        private FlowSession counterpartySession;

        //Constructor
        public RedeemBoardingTicketWithVoucherResponder(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        @Suspendable
        @Override
        public SignedTransaction call() throws FlowException {
            SignedTransaction signedTransaction = flowEngine.subFlow(
                    new CreateAndIssueMarsVoucher.CreateAndIssueMarsVoucherResponder.signingTransaction(counterpartySession));
            return flowEngine.subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
        }

        public static class signingTransaction extends SignTransactionFlow {
            signingTransaction(FlowSession counterpartySession) {
                super(counterpartySession);
            }
            @Override
            protected void checkTransaction(@NotNull SignedTransaction stx) {
            }
        }
    }

}
```
{{% /tab %}}

{{< /tabs >}}

## Next steps

Follow the [Run your CorDapp](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-running.md) tutorial to continue on this learning path.
