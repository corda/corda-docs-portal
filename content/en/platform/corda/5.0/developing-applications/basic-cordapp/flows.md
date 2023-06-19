---
date: '2023-05-03'
title: "Write Flows"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-develop-first-cordapp-flows
    parent: corda5-develop-first-cordapp
    weight: 4000
---

# Write Flows

In Corda, flows automate the process of agreeing ledger updates. They are a sequence of steps that tell the node how to achieve a specific ledger update, such as issuing an asset or making a deposit. Nodes communicate using these flows in point-to-point interactions, rather than a global broadcast system. Network participants must specify what information needs to be sent, to which counterparties.

This tutorial guides you through writing the three flows you need in your CorDapp. These are:

* `CreateAndIssueAppleStampFlow`
* `PackageApplesFlow`
* `RedeemApplesFlow`

You will be creating these flows in the `workflows/src/main/kotlin/com/r3/developers/apples/workflows` directory in this tutorial.

## Learning Objectives

After you have completed this tutorial, you will know how to write and implement flows in a CorDapp.

## Before You Start

Before you start writing flows, read more about [flows]({{< relref "../../key-concepts/fundamentals/ledger/flows/_index.md" >}}).

## Write the `CreateAndIssueAppleStampFlow`

The `CreateAndIssueAppleStampFlow` creates the `AppleStamp` and issues it to the customer.

### Write the Initiator Flow

The `CreateAndIssueAppleStampFlow` action requires interaction between the issuer and the customer. For this reason, you must create an initiator flow and a responder flow.


#### Implement the `CreateAndIssueAppleStampFlow` Class

1.	Go to `workflows/src/main/kotlin/com/r3/developers/apples` and right-click the `workflows` folder.
2.	Select **New > Kotlin Class**.
3.	Create a file called `CreateAndIssueAppleStampFlow`.


#### Make the `CreateAndIssueAppleStampFlow` Startable by REST

Add the `ClientStartableFlow` to the `CreateAndIssueAppleStampFlow`. This allows the flow to be started by REST.
You must implement this interface if you want to trigger the flow with REST via Corda’s HTTP endpoints. So far your code should look like this:

```kotlin
class CreateAndIssueAppleStampFlow : ClientStartableFlow
```

#### Allow `CreateAndIssueAppleStampFlow` to Initiate Flows with Peers

1. Add the `@InitiatingFlow` annotation to `CreateAndIssueAppleStampFlow`.

   This indicates that this flow is the initiating flow in an initiating and initiated flow pair.
2. 2.	Define a protocol for the initiating flow as a parameter to the annotation.
This will also be added to the initiated (responder) flow later. The protocol is a string name of your choice.

So far your code should look similar to this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : ClientStartableFlow
```


#### Add the `call` Method

1. Add the `call` method with an `ClientRequestBody` argument and `String` return type (that `ClientStartableFlow` requires to be implemented).
2. Add the `@Suspendable` annotation.

{{< note >}}
The `String` returned from the `call` method is the result of the flow which can be requested using one of Corda’s HTTP endpoints.
For more information, see [Corda REST API documentation]({{< relref "../../reference/rest-api/_index.md" >}}).
{{< /note >}}

Your code should now look like this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : ClientStartableFlow {

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {

    }
}
```


#### Inject the Required Services into `CreateAndIssueAppleStampFlow`

`CreateAndIssueAppleStampFlow` requires a number of services to be injected so that they can be used by the flow.

Add the following code to inject the services required by this flow. This code adds properties to the flow and should not be added inside the `call` method:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : ClientStartableFlow {

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
    override fun call(requestBody: ClientRequestBody): String {

    }
}
```


#### Extract the `CreateAndIssueAppleStampFlow`'s Request Parameters

`ClientRequestBody` contains the flow’s request parameters passed in via HTTP. To extract the data from the ClientRequestBody, you should create a class that represents the data.

1. Create `CreateAndIssueAppleStampRequest` as a private data class within your flow class, with the following properties:

   * `stampDescription` - A `String` description for the `AppleStamp`.
   * `holder` - A `MemberX500Name` for the participant who is issued an `AppleStamp`.

   This is how it should look like:

   ```kotlin
   data class CreateAndIssueAppleStampRequest(
       val stampDescription: String,
       val holder: MemberX500Name)
    ```

2. To extract the request data into a `CreateAndIssueAppleStampRequest`, add `ClientRequestBody.getRequestBodyAs` to `CreateAndIssueAppleStampFlow`.

3. Add variables for `stampDescription` and `holderName` and extract them from the `CreateAndIssueAppleStampRequest` instance.

   Your code should now look like this:

```kotlin
@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : ClientStartableFlow {

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

    private data class CreateAndIssueAppleStampRequest(
        val stampDescription: String,
        val holder: MemberX500Name
    )

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {
        val request = requestBody.getRequestBodyAs(
            jsonMarshallingService,
            CreateAndIssueAppleStampRequest::class.java)
        val stampDescription = request.stampDescription
        val holderName = request.holder
    }
}
```

#### Obtain a Reference for the Notary

Any flows using the UTXO ledger require a notary service to track the states created and consumed by transactions.

Add the following code to retrieve a notary:

```kotlin
// Retrieve the notaries public key (this will change)
val notaryInfo = notaryLookup.notaryServices.single()
```

{{< note >}}
This code assumes there is only one notary service on the network. If this assumption is false, an exception will be thrown.
For a network with multiple notary services, the CorDapp needs to implement logic to choose the appropriate notary service
for a transaction. Do not use `first()` instead of `single()` because it will result in non-deterministic selection of
a notary service when there are multiple notary services on the network.
{{</ note >}}


#### Lookup the Issuer and Holder of the New `AppleStamp` State

1. Use `memberLookup.myInfo` to lookup the current participant (who is executing the flow).
2. Extract the `name` and `ledgerKey`s (take the first one) of the participant and store the result in a `Party`.
3. Repeat the same process for the holder of the new `AppleStamp` state using the `holderName` from the flow’s input parameters.
4. Verify that the participant with the passed in `holderName` exists in the network.

Your code should now contain the following lines:

```kotlin
val issuer = memberLookup.myInfo().ledgerKeys.first()
val holder = memberLookup.lookup(holderName)
    ?.let { it.ledgerKeys.first() }
    ?: throw IllegalArgumentException("The holder $holderName does not exist within the network")
```

#### Build the Output `AppleStamp` State

In flows with inputs, you use those inputs to determine the outputs a flow will have. Since this flow is creating and issuing the `AppleStamp`, there are no inputs to utilize.

Build the output `newStamp` using the parameters from the `AppleStamp` state:

* `id`
* `stampDescription`
* `issuer`
* `holder`
* `UniqueIdentifier`


#### Encapsulate the Output and Notary into a Transaction

Use an `UtxoTransactionBuilder` to encapsulate everything into a transaction.

1. Use `UtxoLedgerService.createTransactionBuilder` to create a `UtxoTransactionBuilder`.
2. Use `setNotary` to set the name of the transaction’s notary.
3. Use `addOutputState` to add the `newStamp` (the created `AppleStamp`).
4. Use `addCommand` to add the `Issue` command of the `AppleStampContract`.
5. Use `addSignatories` to add the list of required signatories of the transaction. This should include the `issuer` and the `holder`.
6. Use `setTimeWindowUntil` to set a time window for the transaction in which the transaction is valid.
In Corda 5, all transactions using the UTXO ledger must specify an upper bound time window in this way.
7. Use `toSignedTransaction` to sign the transaction.

This is what your transaction creation code should look like now:

```kotlin
val newStamp = AppleStamp(
    id = UUID.randomUUID(),
    stampDesc = stampDescription,
    issuer = issuer,
    holder = holder,
    participants = listOf(issuer, holder)
)

val transaction = utxoLedgerService.createTransactionBuilder()
    .setNotary(notaryInfo.name)
    .addOutputState(newStamp)
    .addCommand(AppleCommands.Issue())
    .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
    .addSignatories(listOf(issuer, holder))
    .toSignedTransaction()

```

#### Finalize the Transaction

Finalizing a transaction does the following:

1. Sends it to counterparties to:
   * verify the transaction’s contracts.
   * validate the transaction’s contents.
   * sign the transaction.
2. Notarizes the transaction.
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


### Write the Responder Flow

As noted previously, the initiator flow needs a corresponding responder flow. The counterparty runs the responder flow.


#### Implement the `CreateAndIssueAppleStampResponderFlow` Class

1. Go to `workflows/src/main/kotlin/com/r3/developers/apples` and right-click the `workflows` folder.
2. Select **New > Kotlin Class**.
3. Create a file called `CreateAndIssueAppleStampResponderFlow`.
4. Make `CreateAndIssueAppleStampResponderFlow` implement `ResponderFlow`.
This allows the flow to be initiated when an initiating flow starts a session. You must implement this interface if
you want a flow to respond to initiation requests with an initiating flow.
5. Add the `@InitiatiedBy` annotation to `CreateAndIssueAppleStampResponderFlow`.


This indicates that this flow is the initiated flow in an initiating and initiated flow pair. A `protocol` must be
defined that both the initiating and initiated flow reference. You should use the same protocol name that you used
when creating the initiator flow earlier.

So far, your code should look like this:

```kotlin
@InitiatedBy(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampResponderFlow : ResponderFlow
```


#### Add the `call` Method

1. Add the `call` method with a `FlowSession` argument (that `ResponderFlow` requires implemented).
2. Add the `@Suspendable` annotation.

Your code should now look like this:

```kotlin
@InitiatedBy(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampResponderFlow : ResponderFlow {

    @Suspendable
    override fun call(session: FlowSession) {

    }
}
```

#### Inject the Required Services into `CreateAndIssueAppleStampResponderFlow`

Inject the UtxoLedgerService into `CreateAndIssueAppleStampResponderFlow`.

Your code should now look like this:

```kotlin
@InitiatedBy(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampResponderFlow : ResponderFlow {

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(session: FlowSession) {

    }
}
```

#### Finalize the Transaction in `CreateAndIssueAppleStampResponderFlow`

Call `UtxoLedgerService.receiveFinality` and pass in the `FlowSession` from `call`'s arguments to finalize a transaction. This is the responding side which matches the `UtxoLedgerService.finalize` called by `CreateAndIssueAppleStampResponderFlow`.

`receiveFinality` requires a callback to be defined that validates the received transaction, you can leave this empty for now.


#### Check Your Work

You have now written both `CreateAndIssueAppleStampFlow` and `CreateAndIssueAppleStampResponderFlow`. You code should look like this:

##### `CreateAndIssueAppleStampFlow`

```kotlin
package com.r3.developers.apples.workflows

import com.r3.developers.apples.contracts.AppleCommands
import com.r3.developers.apples.states.AppleStamp
import net.corda.v5.application.flows.ClientRequestBody
import net.corda.v5.application.flows.ClientStartableFlow
import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.InitiatingFlow
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.types.MemberX500Name
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.UtxoLedgerService
import java.time.Instant
import java.time.temporal.ChronoUnit
import java.util.*

@InitiatingFlow(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampFlow : ClientStartableFlow {
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

    private data class CreateAndIssueAppleStampRequest(
        val stampDescription: String,
        val holder: MemberX500Name
    )

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {
        val request = requestBody.getRequestBodyAs(
            jsonMarshallingService,
            CreateAndIssueAppleStampRequest::class.java)
        val stampDescription = request.stampDescription
        val holderName = request.holder

        val notaryInfo = notaryLookup.notaryServices.single()

        val issuer = memberLookup.myInfo().ledgerKeys.first()
        val holder = memberLookup.lookup(holderName)
            ?.let { it.ledgerKeys.first() }
            ?: throw IllegalArgumentException("The holder $holderName does not exist within the network")

        // Building the output AppleStamp state
        val newStamp = AppleStamp(
            id = UUID.randomUUID(),
            stampDesc = stampDescription,
            issuer = issuer,
            holder = holder,
            participants = listOf(issuer, holder)
        )

        val transaction = utxoLedgerService.createTransactionBuilder()
            .setNotary(notaryInfo.name)
            .addOutputState(newStamp)
            .addCommand(AppleCommands.Issue())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(issuer, holder))
            .toSignedTransaction()

        val session = flowMessaging.initiateFlow(holderName)

        return try {
            // Send the transaction and state to the counterparty and let them sign it
            // Then notarise and record the transaction in both parties' vaults.
            utxoLedgerService.finalize(transaction, listOf(session))
            newStamp.id.toString()
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}
```

##### `CreateAndIssueAppleStampResponderFlow`

```kotlin
package com.r3.developers.apples.workflows

import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.InitiatedBy
import net.corda.v5.application.flows.ResponderFlow
import net.corda.v5.application.messaging.FlowSession
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.utxo.UtxoLedgerService

@InitiatedBy(protocol = "create-and-issue-apple-stamp")
class CreateAndIssueAppleStampResponderFlow : ResponderFlow {

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(session: FlowSession) {
        // Receive, verify, validate, sign and record the transaction sent from the initiator
        utxoLedgerService.receiveFinality(session) { transaction ->
            /*
             * [receiveFinality] will automatically verify the transaction and its signatures before signing it.
             * However, just because a transaction is contractually valid doesn't mean we necessarily want to sign.
             * What if we don't want to deal with the counterparty in question, or the value is too high,
             * or we're not happy with the transaction's structure? [UtxoTransactionValidator] (the lambda created
             * here) allows us to define the additional checks. If any of these conditions are not met,
             * we will not sign the transaction - even if the transaction and its signatures are contractually valid.
             */
        }
    }
}
```

## Write the `PackageApplesFlow` and `RedeemApplesFlow`

Now that you have written the `CreateAndIssueAppleStampFlow`, try writing the `PackageApplesFlow` and `RedeemApplesFlow` on your own.


### Write the `PackageApplesFlow`

The `PackageApples` flow is simpler than the `CreateAndIssueAppleStamp` flow in that it only involves one party.
This flow represents Farmer Bob preparing the apples for Dave to collect.

Since the flow only involves one party (Farmer Bob), there is no need to initiate any sessions and therefore neither `@InitiatingFlow` or `@InitiatedBy` are required.

Include these variables in the flow:

* `appleDescription` - any relevant information, such as the type of apple. Use type `String`.
* `weight` - the weight of the apples. Use type `int`.


#### Check Your Work

After you've written the `PackageApplesFlow`, your code should look like this:

##### `PackageApplesFlow`

```kotlin
package com.r3.developers.apples.workflows

import com.r3.developers.apples.contracts.AppleCommands
import com.r3.developers.apples.states.BasketOfApples
import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.ClientRequestBody
import net.corda.v5.application.flows.ClientStartableFlow
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.UtxoLedgerService
import java.time.Instant
import java.time.temporal.ChronoUnit

class PackageApplesFlow : ClientStartableFlow {

    private data class PackApplesRequest(val appleDescription: String, val weight: Int)

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var memberLookup: MemberLookup

    @CordaInject
    lateinit var notaryLookup: NotaryLookup

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(requestBody: ClientRequestBody): String {
        val request = requestBody.getRequestBodyAs(jsonMarshallingService, PackApplesRequest::class.java)
        val appleDescription = request.appleDescription
        val weight = request.weight
        val notary = notaryLookup.notaryServices.single()
        val myKey = memberLookup.myInfo().ledgerKeys.first()

        // Building the output BasketOfApples state
        val basket = BasketOfApples(
            description = appleDescription,
            farm = myKey,
            owner = myKey,
            weight = weight,
            participants = listOf(myKey)
        )

        // Create the transaction
        val transaction = utxoLedgerService.createTransactionBuilder()
            .setNotary(notary.name)
            .addOutputState(basket)
            .addCommand(AppleCommands.PackBasket())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(myKey))
            .toSignedTransaction()

        return try {
            // Record the transaction, no sessions are passed in as the transaction is only being
            // recorded locally
            utxoLedgerService.finalize(transaction, emptyList()).toString()
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}
```

### Write the `RedeemApplesFlow`

The `RedeemApples` flow involves two parties: Farmer Bob and Dave. When this flow is called, Dave redeems his
`AppleStamp` for the `BasketOfApples` that Farmer Bob gives him. You will need an initiator and responder flow pair for this flow.

Include these variables in the flow:

* `buyer` - the customer buying the apples, in this case Dave.
* `stampId` - the unique identifier of the `AppleStamp`.

The `RedeemApplesFlow` has an additional step that you did not see in the previous two flows. It must query the output
states from the previous two transactions. These output states are the inputs for the `RedeemApplesFlow`. Use the
`UtxoLedgerService` to find these states.

You should check for the following in the flow:
* The specified `AppleStamp` is unconsumed.
* There is an unconsumed `BasketOfApples` where the current owner is the issuer of the `AppleStamp`.

#### Check Your Work

After you’ve written the `RedeemApplesFlow`, your code should look like this:

##### `RedeemApplesFlow`

```kotlin
package com.r3.developers.apples.workflows

import com.r3.developers.apples.contracts.AppleCommands
import com.r3.developers.apples.states.AppleStamp
import com.r3.developers.apples.states.BasketOfApples
import net.corda.v5.base.types.MemberX500Name
import java.util.*

import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.InitiatingFlow
import net.corda.v5.application.flows.ClientRequestBody
import net.corda.v5.application.flows.ClientStartableFlow
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.common.NotaryLookup
import net.corda.v5.ledger.utxo.UtxoLedgerService
import java.time.Instant
import java.time.temporal.ChronoUnit

@InitiatingFlow(protocol = "redeem-apples")
class RedeemApplesFlow : ClientStartableFlow {

    private data class RedeemApplesRequest(val buyer: MemberX500Name, val stampId: UUID)

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
    override fun call(requestBody: ClientRequestBody): String {
        val request = requestBody.getRequestBodyAs(jsonMarshallingService, RedeemApplesRequest::class.java)
        val buyerName = request.buyer
        val stampId = request.stampId

        // Retrieve the notaries public key (this will change)
        val notaryInfo = notaryLookup.notaryServices.single()

        val myKey = memberLookup.myInfo().let { it.ledgerKeys.first() }

        val buyer = memberLookup.lookup(buyerName)
            ?.let { it.ledgerKeys.first() }
            ?: throw IllegalArgumentException("The buyer does not exist within the network")

        val appleStampStateAndRef = utxoLedgerService.findUnconsumedStatesByType(AppleStamp::class.java)
            .firstOrNull { stateAndRef -> stateAndRef.state.contractState.id == stampId }
            ?: throw IllegalArgumentException("No apple stamp matching the stamp id $stampId")

        val basketOfApplesStampStateAndRef = utxoLedgerService.findUnconsumedStatesByType(BasketOfApples::class.java)
            .firstOrNull { basketStateAndRef -> basketStateAndRef.state.contractState.owner ==
        appleStampStateAndRef.state.contractState.issuer }
?: throw IllegalArgumentException("There are no eligible baskets of apples")


        val originalBasketOfApples = basketOfApplesStampStateAndRef.state.contractState

        val updatedBasket = originalBasketOfApples.changeOwner(buyer)

        // Create the transaction
        val transaction = utxoLedgerService.createTransactionBuilder()
            .setNotary(notaryInfo.name)
            .addInputStates(appleStampStateAndRef.ref, basketOfApplesStampStateAndRef.ref)
            .addOutputState(updatedBasket)
            .addCommand(AppleCommands.Redeem())
            .setTimeWindowUntil(Instant.now().plus(1, ChronoUnit.DAYS))
            .addSignatories(listOf(myKey, buyer))
            .toSignedTransaction()

        val session = flowMessaging.initiateFlow(buyerName)

        return try {
            // Send the transaction and state to the counterparty and let them sign it
            // Then notarise and record the transaction in both parties' vaults.
            utxoLedgerService.finalize(transaction, listOf(session)).toString()
        } catch (e: Exception) {
            "Flow failed, message: ${e.message}"
        }
    }
}
```

##### `RedeemApplesResponderFlow`

```kotlin
package com.r3.developers.apples.workflows

import net.corda.v5.application.flows.CordaInject
import net.corda.v5.application.flows.InitiatedBy
import net.corda.v5.application.flows.ResponderFlow
import net.corda.v5.application.messaging.FlowSession
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.ledger.utxo.UtxoLedgerService

@InitiatedBy(protocol = "redeem-apples")
class RedeemApplesResponderFlow : ResponderFlow {

    @CordaInject
    lateinit var utxoLedgerService: UtxoLedgerService

    @Suspendable
    override fun call(session: FlowSession) {
        // Receive, verify, validate, sign and record the transaction sent from the initiator
        utxoLedgerService.receiveFinality(session) { transaction ->
            /*
             * [receiveFinality] will automatically verify the transaction and its signatures before signing it.
             * However, just because a transaction is contractually valid doesn't mean we necessarily want to sign.
             * What if we don't want to deal with the counterparty in question, or the value is too high,
             * or we're not happy with the transaction's structure? [UtxoTransactionValidator] (the lambda created
             * here) allows us to define the additional checks. If any of these conditions are not met,
             * we will not sign the transaction - even if the transaction and its signatures are contractually valid.
             */
        }
    }
}
```

## Next Steps

Follow the [Test Your CorDapp]({{< relref "./testing.md">}}) tutorial to continue on this learning path.
