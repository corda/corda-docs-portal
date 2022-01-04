---
date: '2021-09-16'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-flows
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1040
tags:
- tutorial
- cordapp
title: Write flows
---

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

Top-level flows encapsulate the business logic behind the interaction between the users and your CorDapp. They can have multiple subflows and can be started via RPC.

Subflows or built-in flows are common tasks performed in Corda, such as gathering signatures from counterparty nodes or notarising and recording a transaction. As a developer, you only need to implement flows for the business logic of your specific use case.

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

```kotlin
package net.corda.missionMars.flows

class CreateAndIssueMarsVoucher {
}
```

#### Add annotations

1. Add an `@InitiatingFlow` annotation. This indicates that this flow is the initiating flow.
2. Add the `@StartableByRPC` annotation. This annotation allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC Client.

So far, your code should look like this:

```kotlin
package net.corda.missionMars.flows

import net.corda.v5.application.flows.InitiatingFlow
import net.corda.v5.application.flows.StartableByRPC

@InitiatingFlow
@StartableByRPC
class CreateAndIssueMarsVoucher {
}
```

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

#### Inject services

When writing flows with the Corda 5 Developer Preview, you can inject whichever services you need, and exclude those you don't.

Use the `@CordaInject` annotation to define a field to be set by Corda before the call method is called. See this [list of services](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/injectable-services.md) to find out what services you can add to a CorDapp.

In this sample CorDapp, add these services:

* `FlowEngine`
* `FlowIdentity`
* `FlowMessaging`
* `TransactionBuilderFactory`
* `IdentityService`: Provides methods to retrieve `Party` and `AnonymousParty` instances.
* `NotaryLookupService`
* `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers.

After you've added the services, your code should look like this:

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

#### Write your business logic

##### Add the flow implementation

Next you must add the flow implementation to the initiating flow by encapsulating it within the `call` method.

1. Add the `@Suspendable` annotation.
2. Add the `call` method with the return type `SignedTransactionDigest`.
3. Parse your parameters using the `mapOfParams` value. Since the parameters the flow will use come in JSON format, the JSON object must be parsed to extract the parameters so the flow can run.
4. Add appropriate error handling - exceptions must be thrown when required fields (`voucherDesc`, `holder`, `recipientParty`) are not found.
5. Insert the following method for finding the notary: `notaryLookup.notaryIdentities.<notary name>()`.
6. Build the output `MarsVoucher` state with a `UniqueIdentifier`.

##### Build the transaction

Your transaction is a proposal to the ledger that the counterparty must agree to. You must ensure that the proposal adheres the rules of the smart contract and sign it before sending it to the counterparty. The proposal here is that you'll create a voucher for a trip to Mars and then issue that voucher to a designated party - Peter.

1. Build the transaction using a `txCommand` and the `transactionBuilderFactory` service you added when injecting services.
2. Verify that the transaction is valid using the `txBuilder.verify` method.
3. Sign the transaction using the `txBuilder.sign` method.

##### Interact with the counterparty

This is where you send the proposal to Peter. When consensus that the transaction's elements are unique and understood is achieved, the transaction is notarized in both parties' vaults.

1. Send the state to the counterparty and receive it back with their signature. Use the `flowMessaging` service to send the state to the `recipientParty`. Use the `flowEngine` service with the subflow `CollectSignaturesFlow` to get the signature of the counterparty.
2. Get the transaction notarized and recorded in both parties' vaults using `FinalityFlow` with a `fullySignedTx`.
3. Return a `SignedTransactionDigest`. Use the `jsonMarshallingService` to parse the transaction's output. Include the transaction's output states, ID, and signatures.

After adding these elements, your code should look like this:

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
        val notary = notaryLookup.notaryIdentities.<notary name>()

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

### Write the responder flow

Now that you've written the initiating flow, write the responder flow that responds to the request to update the ledger. The responder flow in the `CreateAndIssueMarsVoucher` flow is very simple and in the context of the Mission Mars CorDapp, you don't need to verify anything. However, when signing a responder flow in a "real-life context", do not sign it before verifying its contents and ensuring you are accepting what you want to accept.

1. Add the `@InitiatedBy` annotation. This indicates that this is the responder flow.

2. Add in a responder flow.

When the responder receives a half-signed transaction from an initiating party, it is most likely being asked to sign the transaction. The responder flow will go through some checks on the transaction (implemented in the responder flow). If all the checks are passed, it will sign the transaction and return it back to the initiating party. Next, it will add a fully-signed transaction to its local ledger. This is done by the `ReceiveFinalityFlow` subflow.

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

## Write the `CreateBoardingTicket` flow

The `CreateBoardingTicket` flow lets Mars Express self-issue a `BoardingTicket` to later be exchanged with Peter's voucher.

Now that you've written the `CreateAndIssueMarsVoucher` flow, try writing the `CreateBoardingTicket` flow.

You will need these variables:

* `ticketDescription`
* `daysUntilLaunch`

You must inject these services:
* `JsonMarshallingService`
* `FlowEngine`
* `FlowIdentity`
* `TransactionBuilderFactory`
* `NotaryLookupService`

{{< note >}}
This flow only needs an initiating flow; you don't need to include a responder flow. However, you must still add the `@InitiatingFlow` annotation.
{{< /note >}}

After you've written the `CreateBoardingTicket` flow, it should look like this:

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
        val daysUntilLaunch = with(mapOfParams["daysUntilLaunch"] ?: throw BadRpcStartFlowRequestException("BoardingTicket State Parameter \"daysUntilLaunch\" missing.")) {
            this.toInt()
        }

        //Find notary.
        val notary = notaryLookup.notaryIdentities.<notary name>()

        //Building the output BoardingTicket state.
        val basket = BoardingTicket(description = ticketDescription,marsExpress = flowIdentity.ourIdentity,daysUntilLaunch = daysUntilLaunch)


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

## Write the `RedeemBoardingTicketWithVoucher` flow

The `RedeemBoardingTicketWithVoucher` flow lets Peter redeem his `MarsVoucher` for a `BoardingTicket` and take his trip to Mars.

Since this flow is performing a redemption, you must have both an initiating flow and a responder flow.

### Write the initiating flow

Start writing your initiating flow following the same process used when writing the <a href="#write-the-createandissuemarsvoucher-flow">`CreateAndIssueMarsVoucher`</a> flow.

1. Add these annotations:
   * `@InitiatingFlow`: This indicates that this flow is the initiating flow.
   * `@StartableByRPC`: This annotation allows the flow to be started by RPC. You **must** use this annotation if you want to run the flow with the RPC Client.

2. Define the `RedeemBoardingTicketWithVoucherInitiator` class with a `@JsonConstructor`, `RpcStartFlowRequestParameters`, and returning a `SignedTransactionDigest`.
3. Inject these services:
    * `FlowEngine`
    * `FlowIdentity`
    * `FlowMessaging`
    * `TransactionBuilderFactory`
    * `IdentityService`: Provides methods to retrieve `Party` and `AnonymousParty` instances.
    * `NotaryLookupService`
    * `JsonMarshallingService`: Parses arbitrary content in and out of JSON using standard, approved mappers.
    * `PersistenceService`

4. Add the `@Suspendable` annotation.
5. Encapsulate the flow implementation into a call method that returns the `SignedTransactionDigest`.

6. Parse these parameters and add exceptions for when these parameters are incorrect or not present:
    * `voucherID`
    * `holder`
    * `recipientParty`

7. Insert the following method for finding the notary: `notaryLookup.notaryIdentities.<notary name>()`

#### Implement queries

In the implementation of this initiating flow, you must query the `MarsVoucher` and the `BoardingTicket`. You can use the `PersistenceService` to perform these queries.

##### Add a query for the `MarsVoucher`

1. Use a `cursor` to point to a specific line in the query results.
2. Add a `persistenceService.query` to get the `StateAndRef` of the `MarsVoucher`.
3. Use the [predefined query](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#query-for-states-when-your-state-does-not-have-a-mapped-schema) `findByUuidAndStateStatus` to find the `MarsVoucher` you need by the state's unique identifier and status.
4. Because you need to return a `StateAndRef`, use Corda's built-in `Corda.IdentityStateAndRefPostProcessor`.
5. Because you need to return a `ContractState`, use Corda's built-in `IdentityContractStatePostProcessor`.
6. Use the `poll` function to set a maximum poll size and timeout duration for the query.

##### Add a query for the `BoardingTicket`

1. Use an additional cursor (`cursor2`) to point to a specific line in the query results.
2. Add a `persistenceService.query` to get the `StateAndRef` of the `BoardingTicket`.
3. Use the [predefined query](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#query-for-states-when-your-state-does-not-have-a-mapped-schema) `findByStateStatusAndContractStateClassName` to find the `BoardingTicket` you need by the state's status and contract state class name.
4. Because you need to return a `StateAndRef`, use Corda's built-in `Corda.IdentityStateAndRefPostProcessor`.
5. Because you need to return a `ContractState`, use Corda's built-in `IdentityContractStatePostProcessor`.
6. Use the `poll` function to set a maximum poll size and timeout duration for the query.

Your code should now look like this:

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
        val notary = notaryLookup.notaryIdentities.<notary name>()

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

#### Finish the initiating flow

Finish the initiating flow by continuing with the same steps you followed when creating the first two flows.

1. Build the transaction's output. Output the `BoardingTicket` and change the owner.
2. Build the transaction using the `TransactionBuilderFactory` service.
3. Verify that the transaction is valid with the `txBuilder.verify` method.
4. Sign the transaction using the `txBuilder.sign` method.
5. Send the state to Peter using the `flowMessaging` service, then receive it using the `FlowEngine` and the subflow `CollectSignaturesFlow`.
6. Get the transaction notarized in both parties' vaults using the `FlowEngine` service and the subflow `FinalityFlow`.
   After the transaction is performed, the issuer will have the consumed state in their vault and they won't have a reference to the new state. The new state generated by this transaction will be stored in the counterparty's vault.
7. Return a `SignedTransactionDigest`.


### Write the responder flow

Now that you've written the initiating flow, try writing the responder flow.
Once you're done, your code should look like this:

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
        val notary = notaryLookup.notaryIdentities.<notary name>()

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

## Next steps

Follow the [Run your CorDapp](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-running.md) tutorial to continue on this learning path.
