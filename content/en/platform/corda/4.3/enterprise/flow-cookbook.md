---
aliases:
- /releases/4.3/flow-cookbook.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-flow-cookbook
    parent: corda-enterprise-4-3-building-a-cordapp-index
    weight: 1100
tags:
- flow
- cookbook
title: Flow cookbook
---




# Flow cookbook

This flow showcases how to use Corda’s API, in both Java and Kotlin.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
@file:Suppress("UNUSED_VARIABLE", "unused", "DEPRECATION")

package net.corda.docs.kotlin

import co.paralleluniverse.fibers.Suspendable
import net.corda.core.contracts.*
import net.corda.core.crypto.SecureHash
import net.corda.core.crypto.TransactionSignature
import net.corda.core.crypto.generateKeyPair
import net.corda.core.flows.*
import net.corda.core.identity.CordaX500Name
import net.corda.core.identity.Party
import net.corda.core.identity.PartyAndCertificate
import net.corda.core.internal.FetchDataFlow
import net.corda.core.node.services.Vault.Page
import net.corda.core.node.services.queryBy
import net.corda.core.node.services.vault.QueryCriteria.VaultQueryCriteria
import net.corda.core.transactions.LedgerTransaction
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
import net.corda.core.utilities.ProgressTracker
import net.corda.core.utilities.ProgressTracker.Step
import net.corda.core.utilities.UntrustworthyData
import net.corda.core.utilities.seconds
import net.corda.core.utilities.unwrap
import net.corda.finance.contracts.asset.Cash
import net.corda.testing.contracts.DummyContract
import net.corda.testing.contracts.DummyState
import java.security.PublicKey
import java.security.Signature
import java.time.Instant

// ``InitiatorFlow`` is our first flow, and will communicate with
// ``ResponderFlow``, below.
// We mark ``InitiatorFlow`` as an ``InitiatingFlow``, allowing it to be
// started directly by the node.
@InitiatingFlow
// We also mark ``InitiatorFlow`` as ``StartableByRPC``, allowing the
// node's owner to start the flow via RPC.
@StartableByRPC
// Every flow must subclass ``FlowLogic``. The generic indicates the
// flow's return type.
class InitiatorFlow(val arg1: Boolean, val arg2: Int, private val counterparty: Party, val regulator: Party) : FlowLogic<Unit>() {

    /**---------------------------------
     * WIRING UP THE PROGRESS TRACKER *
    ---------------------------------**/
    // Giving our flow a progress tracker allows us to see the flow's
    // progress visually in our node's CRaSH shell.
    // DOCSTART 17
    companion object {
        object ID_OTHER_NODES : Step("Identifying other nodes on the network.")
        object SENDING_AND_RECEIVING_DATA : Step("Sending data between parties.")
        object EXTRACTING_VAULT_STATES : Step("Extracting states from the vault.")
        object OTHER_TX_COMPONENTS : Step("Gathering a transaction's other components.")
        object TX_BUILDING : Step("Building a transaction.")
        object TX_SIGNING : Step("Signing a transaction.")
        object TX_VERIFICATION : Step("Verifying a transaction.")
        object SIGS_GATHERING : Step("Gathering a transaction's signatures.") {
            // Wiring up a child progress tracker allows us to see the
            // subflow's progress steps in our flow's progress tracker.
            override fun childProgressTracker() = CollectSignaturesFlow.tracker()
        }

        object VERIFYING_SIGS : Step("Verifying a transaction's signatures.")
        object FINALISATION : Step("Finalising a transaction.") {
            override fun childProgressTracker() = FinalityFlow.tracker()
        }

        fun tracker() = ProgressTracker(
                ID_OTHER_NODES,
                SENDING_AND_RECEIVING_DATA,
                EXTRACTING_VAULT_STATES,
                OTHER_TX_COMPONENTS,
                TX_BUILDING,
                TX_SIGNING,
                TX_VERIFICATION,
                SIGS_GATHERING,
                VERIFYING_SIGS,
                FINALISATION
        )
    }
    // DOCEND 17

    override val progressTracker: ProgressTracker = tracker()

    @Suppress("RemoveExplicitTypeArguments")
    @Suspendable
    override fun call() {
        // We'll be using a dummy public key for demonstration purposes.
        val dummyPubKey: PublicKey = generateKeyPair().public

        /**--------------------------
         * IDENTIFYING OTHER NODES *
        --------------------------**/
        // DOCSTART 18
        progressTracker.currentStep = ID_OTHER_NODES
        // DOCEND 18

        // A transaction generally needs a notary:
        //   - To prevent double-spends if the transaction has inputs
        //   - To serve as a timestamping authority if the transaction has a
        //     time-window
        // We retrieve the notary from the network map.
        // DOCSTART 01
        val notaryName: CordaX500Name = CordaX500Name(
                organisation = "Notary Service",
                locality = "London",
                country = "GB")
        val specificNotary: Party = serviceHub.networkMapCache.getNotary(notaryName)!!
        // Alternatively, we can pick an arbitrary notary from the notary
        // list. However, it is always preferable to specify the notary
        // explicitly, as the notary list might change when new notaries are
        // introduced, or old ones decommissioned.
        val firstNotary: Party = serviceHub.networkMapCache.notaryIdentities.first()
        // DOCEND 01

        // We may also need to identify a specific counterparty. We do so
        // using the identity service.
        // DOCSTART 02
        val counterpartyName: CordaX500Name = CordaX500Name(
                organisation = "NodeA",
                locality = "London",
                country = "GB")
        val namedCounterparty: Party = serviceHub.identityService.wellKnownPartyFromX500Name(counterpartyName) ?:
                throw IllegalArgumentException("Couldn't find counterparty for NodeA in identity service")
        val keyedCounterparty: Party = serviceHub.identityService.partyFromKey(dummyPubKey) ?:
                throw IllegalArgumentException("Couldn't find counterparty with key: $dummyPubKey in identity service")
        // DOCEND 02

        /**-----------------------------
         * SENDING AND RECEIVING DATA *
        -----------------------------**/
        progressTracker.currentStep = SENDING_AND_RECEIVING_DATA

        // We start by initiating a flow session with the counterparty. We
        // will use this session to send and receive messages from the
        // counterparty.
        // DOCSTART initiateFlow
        val counterpartySession: FlowSession = initiateFlow(counterparty)
        // DOCEND initiateFlow

        // We can send arbitrary data to a counterparty.
        // If this is the first ``send``, the counterparty will either:
        // 1. Ignore the message if they are not registered to respond
        //    to messages from this flow.
        // 2. Start the flow they have registered to respond to this flow,
        //    and run the flow until the first call to ``receive``, at
        //    which point they process the message.
        // In other words, we are assuming that the counterparty is
        // registered to respond to this flow, and has a corresponding
        // ``receive`` call.
        // DOCSTART 04
        counterpartySession.send(Any())
        // DOCEND 04

        // We can wait to receive arbitrary data of a specific type from a
        // counterparty. Again, this implies a corresponding ``send`` call
        // in the counterparty's flow. A few scenarios:
        // - We never receive a message back. In the current design, the
        //   flow is paused until the node's owner kills the flow.
        // - Instead of sending a message back, the counterparty throws a
        //   ``FlowException``. This exception is propagated back to us,
        //   and we can use the error message to establish what happened.
        // - We receive a message back, but it's of the wrong type. In
        //   this case, a ``FlowException`` is thrown.
        // - We receive back a message of the correct type. All is good.
        //
        // Upon calling ``receive()`` (or ``sendAndReceive()``), the
        // ``FlowLogic`` is suspended until it receives a response.
        //
        // We receive the data wrapped in an ``UntrustworthyData``
        // instance. This is a reminder that the data we receive may not
        // be what it appears to be! We must unwrap the
        // ``UntrustworthyData`` using a lambda.
        // DOCSTART 05
        val packet1: UntrustworthyData<Int> = counterpartySession.receive<Int>()
        val int: Int = packet1.unwrap { data ->
            // Perform checking on the object received.
            // T O D O: Check the received object.
            // Return the object.
            data
        }
        // DOCEND 05

        // We can also use a single call to send data to a counterparty
        // and wait to receive data of a specific type back. The type of
        // data sent doesn't need to match the type of the data received
        // back.
        // DOCSTART 07
        val packet2: UntrustworthyData<Boolean> = counterpartySession.sendAndReceive<Boolean>("You can send and receive any class!")
        val boolean: Boolean = packet2.unwrap { data ->
            // Perform checking on the object received.
            // T O D O: Check the received object.
            // Return the object.
            data
        }
        // DOCEND 07

        // We're not limited to sending to and receiving from a single
        // counterparty. A flow can send messages to as many parties as it
        // likes, and each party can invoke a different response flow.
        // DOCSTART 06
        val regulatorSession: FlowSession = initiateFlow(regulator)
        regulatorSession.send(Any())
        val packet3: UntrustworthyData<Any> = regulatorSession.receive<Any>()
        // DOCEND 06

        // We may also batch receives in order to increase performance. This
        // ensures that only a single checkpoint is created for all received
        // messages.
        // Type-safe variant:
        val signatures: List<UntrustworthyData<Signature>> =
                receiveAll(Signature::class.java, listOf(counterpartySession, regulatorSession))
        // Dynamic variant:
        val messages: Map<FlowSession, UntrustworthyData<*>> =
                receiveAllMap(mapOf(
                        counterpartySession to Boolean::class.java,
                        regulatorSession to String::class.java
                ))

        /**-----------------------------------
         * EXTRACTING STATES FROM THE VAULT *
        -----------------------------------**/
        progressTracker.currentStep = EXTRACTING_VAULT_STATES

        // Let's assume there are already some ``DummyState``s in our
        // node's vault, stored there as a result of running past flows,
        // and we want to consume them in a transaction. There are many
        // ways to extract these states from our vault.

        // For example, we would extract any unconsumed ``DummyState``s
        // from our vault as follows:
        val criteria: VaultQueryCriteria = VaultQueryCriteria() // default is UNCONSUMED
        val results: Page<DummyState> = serviceHub.vaultService.queryBy<DummyState>(criteria)
        val dummyStates: List<StateAndRef<DummyState>> = results.states

        // For a full list of the available ways of extracting states from
        // the vault, see the Vault Query docs page.

        // When building a transaction, input states are passed in as
        // ``StateRef`` instances, which pair the hash of the transaction
        // that generated the state with the state's index in the outputs
        // of that transaction. In practice, we'd pass the transaction hash
        // or the ``StateRef`` as a parameter to the flow, or extract the
        // ``StateRef`` from our vault.
        // DOCSTART 20
        val ourStateRef: StateRef = StateRef(SecureHash.sha256("DummyTransactionHash"), 0)
        // DOCEND 20
        // A ``StateAndRef`` pairs a ``StateRef`` with the state it points to.
        // DOCSTART 21
        val ourStateAndRef: StateAndRef<DummyState> = serviceHub.toStateAndRef<DummyState>(ourStateRef)
        // DOCEND 21

        /**-----------------------------------------
         * GATHERING OTHER TRANSACTION COMPONENTS *
        -----------------------------------------**/
        progressTracker.currentStep = OTHER_TX_COMPONENTS

        // Reference input states are constructed from StateAndRefs.
        // DOCSTART 55
        val referenceState: ReferencedStateAndRef<DummyState> = ourStateAndRef.referenced()
        // DOCEND 55
        // Output states are constructed from scratch.
        // DOCSTART 22
        val ourOutputState: DummyState = DummyState()
        // DOCEND 22
        // Or as copies of other states with some properties changed.
        @Suppress("MagicNumber") // literally a magic number
        // DOCSTART 23
        val ourOtherOutputState: DummyState = ourOutputState.copy(magicNumber = 77)
        // DOCEND 23

        // We then need to pair our output state with a contract.
        // DOCSTART 47
        val  ourOutput: StateAndContract = StateAndContract(ourOutputState, DummyContract.PROGRAM_ID)
        // DOCEND 47

        // Commands pair a ``CommandData`` instance with a list of
        // public keys. To be valid, the transaction requires a signature
        // matching every public key in all of the transaction's commands.
        // DOCSTART 24
        val commandData: DummyContract.Commands.Create = DummyContract.Commands.Create()
        val ourPubKey: PublicKey = serviceHub.myInfo.legalIdentitiesAndCerts.first().owningKey
        val counterpartyPubKey: PublicKey = counterparty.owningKey
        val requiredSigners: List<PublicKey> = listOf(ourPubKey, counterpartyPubKey)
        val ourCommand: Command<DummyContract.Commands.Create> = Command(commandData, requiredSigners)
        // DOCEND 24

        // ``CommandData`` can either be:
        // 1. Of type ``TypeOnlyCommandData``, in which case it only
        //    serves to attach signers to the transaction and possibly
        //    fork the contract's verification logic.
        val typeOnlyCommandData: TypeOnlyCommandData = DummyContract.Commands.Create()
        // 2. Include additional data which can be used by the contract
        //    during verification, alongside fulfilling the roles above.
        val commandDataWithData: CommandData = Cash.Commands.Issue()

        // Attachments are identified by their hash.
        // The attachment with the corresponding hash must have been
        // uploaded ahead of time via the node's RPC interface.
        // DOCSTART 25
        val ourAttachment: SecureHash = SecureHash.sha256("DummyAttachment")
        // DOCEND 25

        // Time windows can have a start and end time, or be open at either end.
        // DOCSTART 26
        val ourTimeWindow: TimeWindow = TimeWindow.between(Instant.MIN, Instant.MAX)
        val ourAfter: TimeWindow = TimeWindow.fromOnly(Instant.MIN)
        val ourBefore: TimeWindow = TimeWindow.untilOnly(Instant.MAX)
        // DOCEND 26

        // We can also define a time window as an ``Instant`` +/- a time
        // tolerance (e.g. 30 seconds):
        // DOCSTART 42
        val ourTimeWindow2: TimeWindow = TimeWindow.withTolerance(serviceHub.clock.instant(), 30.seconds)
        // DOCEND 42
        // Or as a start-time plus a duration:
        // DOCSTART 43
        val ourTimeWindow3: TimeWindow = TimeWindow.fromStartAndDuration(serviceHub.clock.instant(), 30.seconds)
        // DOCEND 43

        /**-----------------------
         * TRANSACTION BUILDING *
        -----------------------**/
        progressTracker.currentStep = TX_BUILDING

        // If our transaction has input states or a time-window, we must instantiate it with a
        // notary.
        // DOCSTART 19
        val txBuilder: TransactionBuilder = TransactionBuilder(specificNotary)
        // DOCEND 19

        // Otherwise, we can choose to instantiate it without one:
        // DOCSTART 46
        val txBuilderNoNotary: TransactionBuilder = TransactionBuilder()
        // DOCEND 46

        // We add items to the transaction builder using ``TransactionBuilder.withItems``:
        // DOCSTART 27
        txBuilder.withItems(
                // Inputs, as ``StateAndRef``s that reference the outputs of previous transactions
                ourStateAndRef,
                // Outputs, as ``StateAndContract``s
                ourOutput,
                // Commands, as ``Command``s
                ourCommand,
                // Attachments, as ``SecureHash``es
                ourAttachment,
                // A time-window, as ``TimeWindow``
                ourTimeWindow
        )
        // DOCEND 27

        // We can also add items using methods for the individual components.

        // The individual methods for adding input states and attachments:
        // DOCSTART 28
        txBuilder.addInputState(ourStateAndRef)
        txBuilder.addAttachment(ourAttachment)
        // DOCEND 28

        // An output state can be added as a ``ContractState``, contract class name and notary.
        // DOCSTART 49
        txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary)
        // DOCEND 49
        // We can also leave the notary field blank, in which case the transaction's default
        // notary is used.
        // DOCSTART 50
        txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID)
        // DOCEND 50
        // Or we can add the output state as a ``TransactionState``, which already specifies
        // the output's contract and notary.
        // DOCSTART 51
        val txState: TransactionState<DummyState> = TransactionState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary)
        // DOCEND 51

        // Commands can be added as ``Command``s.
        // DOCSTART 52
        txBuilder.addCommand(ourCommand)
        // DOCEND 52
        // Or as ``CommandData`` and a ``vararg PublicKey``.
        // DOCSTART 53
        txBuilder.addCommand(commandData, ourPubKey, counterpartyPubKey)
        // DOCEND 53

        // We can set a time-window directly.
        // DOCSTART 44
        txBuilder.setTimeWindow(ourTimeWindow)
        // DOCEND 44
        // Or as a start time plus a duration (e.g. 45 seconds).
        // DOCSTART 45
        txBuilder.setTimeWindow(serviceHub.clock.instant(), 45.seconds)
        // DOCEND 45

        /**----------------------
         * TRANSACTION SIGNING *
        ----------------------**/
        progressTracker.currentStep = TX_SIGNING

        // We finalise the transaction by signing it, converting it into a
        // ``SignedTransaction``.
        // DOCSTART 29
        val onceSignedTx: SignedTransaction = serviceHub.signInitialTransaction(txBuilder)
        // DOCEND 29
        // We can also sign the transaction using a different public key:
        // DOCSTART 30
        val otherIdentity: PartyAndCertificate = serviceHub.keyManagementService.freshKeyAndCert(ourIdentityAndCert, false)
        val onceSignedTx2: SignedTransaction = serviceHub.signInitialTransaction(txBuilder, otherIdentity.owningKey)
        // DOCEND 30

        // If instead this was a ``SignedTransaction`` that we'd received
        // from a counterparty and we needed to sign it, we would add our
        // signature using:
        // DOCSTART 38
        val twiceSignedTx: SignedTransaction = serviceHub.addSignature(onceSignedTx)
        // DOCEND 38
        // Or, if we wanted to use a different public key:
        val otherIdentity2: PartyAndCertificate = serviceHub.keyManagementService.freshKeyAndCert(ourIdentityAndCert, false)
        // DOCSTART 39
        val twiceSignedTx2: SignedTransaction = serviceHub.addSignature(onceSignedTx, otherIdentity2.owningKey)
        // DOCEND 39

        // We can also generate a signature over the transaction without
        // adding it to the transaction itself. We may do this when
        // sending just the signature in a flow instead of returning the
        // entire transaction with our signature. This way, the receiving
        // node does not need to check we haven't changed anything in the
        // transaction.
        // DOCSTART 40
        val sig: TransactionSignature = serviceHub.createSignature(onceSignedTx)
        // DOCEND 40
        // And again, if we wanted to use a different public key:
        // DOCSTART 41
        val sig2: TransactionSignature = serviceHub.createSignature(onceSignedTx, otherIdentity2.owningKey)
        // DOCEND 41

        // In practice, however, the process of gathering every signature
        // but the first can be automated using ``CollectSignaturesFlow``.
        // See the "Gathering Signatures" section below.

        /**---------------------------
         * TRANSACTION VERIFICATION *
        ---------------------------**/
        progressTracker.currentStep = TX_VERIFICATION

        // Verifying a transaction will also verify every transaction in
        // the transaction's dependency chain, which will require
        // transaction data access on counterparty's node. The
        // ``SendTransactionFlow`` can be used to automate the sending and
        // data vending process. The ``SendTransactionFlow`` will listen
        // for data request until the transaction is resolved and verified
        // on the other side:
        // DOCSTART 12
        subFlow(SendTransactionFlow(counterpartySession, twiceSignedTx))

        // Optional request verification to further restrict data access.
        subFlow(object : SendTransactionFlow(counterpartySession, twiceSignedTx) {
            override fun verifyDataRequest(dataRequest: FetchDataFlow.Request.Data) {
                // Extra request verification.
            }
        })
        // DOCEND 12

        // We can receive the transaction using ``ReceiveTransactionFlow``,
        // which will automatically download all the dependencies and verify
        // the transaction
        // DOCSTART 13
        val verifiedTransaction = subFlow(ReceiveTransactionFlow(counterpartySession))
        // DOCEND 13

        // We can also send and receive a `StateAndRef` dependency chain
        // and automatically resolve its dependencies.
        // DOCSTART 14
        subFlow(SendStateAndRefFlow(counterpartySession, dummyStates))

        // On the receive side ...
        val resolvedStateAndRef = subFlow(ReceiveStateAndRefFlow<DummyState>(counterpartySession))
        // DOCEND 14

        // We can now verify the transaction to ensure that it satisfies
        // the contracts of all the transaction's input and output states.
        // DOCSTART 33
        twiceSignedTx.verify(serviceHub)
        // DOCEND 33

        // We'll often want to perform our own additional verification
        // too. Just because a transaction is valid based on the contract
        // rules and requires our signature doesn't mean we have to
        // sign it! We need to make sure the transaction represents an
        // agreement we actually want to enter into.

        // To do this, we need to convert our ``SignedTransaction``
        // into a ``LedgerTransaction``. This will use our ServiceHub
        // to resolve the transaction's inputs and attachments into
        // actual objects, rather than just references.
        // DOCSTART 32
        val ledgerTx: LedgerTransaction = twiceSignedTx.toLedgerTransaction(serviceHub)
        // DOCEND 32

        // We can now perform our additional verification.
        // DOCSTART 34
        val outputState: DummyState = ledgerTx.outputsOfType<DummyState>().single()
        if (outputState.magicNumber == 777) {
            // ``FlowException`` is a special exception type. It will be
            // propagated back to any counterparty flows waiting for a
            // message from this flow, notifying them that the flow has
            // failed.
            throw FlowException("We expected a magic number of 777.")
        }
        // DOCEND 34

        // Of course, if you are not a required signer on the transaction,
        // you have no power to decide whether it is valid or not. If it
        // requires signatures from all the required signers and is
        // contractually valid, it's a valid ledger update.

        /**-----------------------
         * GATHERING SIGNATURES *
        -----------------------**/
        progressTracker.currentStep = SIGS_GATHERING

        // The list of parties who need to sign a transaction is dictated
        // by the transaction's commands. Once we've signed a transaction
        // ourselves, we can automatically gather the signatures of the
        // other required signers using ``CollectSignaturesFlow``.
        // The responder flow will need to call ``SignTransactionFlow``.
        // DOCSTART 15
        val fullySignedTx: SignedTransaction = subFlow(CollectSignaturesFlow(twiceSignedTx, setOf(counterpartySession, regulatorSession), SIGS_GATHERING.childProgressTracker()))
        // DOCEND 15

        /**-----------------------
         * VERIFYING SIGNATURES *
        -----------------------**/
        progressTracker.currentStep = VERIFYING_SIGS

        // We can verify that a transaction has all the required
        // signatures, and that they're all valid, by running:
        // DOCSTART 35
        fullySignedTx.verifyRequiredSignatures()
        // DOCEND 35

        // If the transaction is only partially signed, we have to pass in
        // a vararg of the public keys corresponding to the missing
        // signatures, explicitly telling the system not to check them.
        // DOCSTART 36
        onceSignedTx.verifySignaturesExcept(counterpartyPubKey)
        // DOCEND 36

        // There is also an overload of ``verifySignaturesExcept`` which accepts
        // a ``Collection`` of the public keys corresponding to the missing
        // signatures.
        // DOCSTART 54
        onceSignedTx.verifySignaturesExcept(listOf(counterpartyPubKey))
        // DOCEND 54

        // We can also choose to only check the signatures that are
        // present. BE VERY CAREFUL - this function provides no guarantees
        // that the signatures are correct, or that none are missing.
        // DOCSTART 37
        twiceSignedTx.checkSignaturesAreValid()
        // DOCEND 37

        /**-----------------------------
         * FINALISING THE TRANSACTION *
        -----------------------------**/
        progressTracker.currentStep = FINALISATION

        // We notarise the transaction and get it recorded in the vault of
        // the participants of all the transaction's states.
        // DOCSTART 09
        val notarisedTx1: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, listOf(counterpartySession), FINALISATION.childProgressTracker()))
        // DOCEND 09
        // We can also choose to send it to additional parties who aren't one
        // of the state's participants.
        // DOCSTART 10
        val partySessions: List<FlowSession> = listOf(counterpartySession, initiateFlow(regulator))
        val notarisedTx2: SignedTransaction = subFlow(FinalityFlow(fullySignedTx, partySessions, FINALISATION.childProgressTracker()))
        // DOCEND 10
    }
}

// ``ResponderFlow`` is our second flow, and will communicate with
// ``InitiatorFlow``.
// We mark ``ResponderFlow`` as an ``InitiatedByFlow``, meaning that it
// can only be started in response to a message from its initiating flow.
// That's ``InitiatorFlow`` in this case.
// Each node also has several flow pairs registered by default - see
// ``AbstractNode.installCoreFlows``.
@InitiatedBy(InitiatorFlow::class)
class ResponderFlow(val counterpartySession: FlowSession) : FlowLogic<Unit>() {

    companion object {
        object RECEIVING_AND_SENDING_DATA : Step("Sending data between parties.")
        object SIGNING : Step("Responding to CollectSignaturesFlow.")
        object FINALISATION : Step("Finalising a transaction.")

        fun tracker() = ProgressTracker(
                RECEIVING_AND_SENDING_DATA,
                SIGNING,
                FINALISATION
        )
    }

    override val progressTracker: ProgressTracker = tracker()

    @Suspendable
    override fun call() {
        // The ``ResponderFlow` has all the same APIs available. It looks
        // up network information, sends and receives data, and constructs
        // transactions in exactly the same way.

        /**-----------------------------
         * SENDING AND RECEIVING DATA *
        -----------------------------**/
        progressTracker.currentStep = RECEIVING_AND_SENDING_DATA

        // We need to respond to the messages sent by the initiator:
        // 1. They sent us an ``Any`` instance
        // 2. They waited to receive an ``Integer`` instance back
        // 3. They sent a ``String`` instance and waited to receive a
        //    ``Boolean`` instance back
        // Our side of the flow must mirror these calls.
        // DOCSTART 08
        val any: Any = counterpartySession.receive<Any>().unwrap { data -> data }
        val string: String = counterpartySession.sendAndReceive<String>(99).unwrap { data -> data }
        counterpartySession.send(true)
        // DOCEND 08

        /**----------------------------------------
         * RESPONDING TO COLLECT_SIGNATURES_FLOW *
        ----------------------------------------**/
        progressTracker.currentStep = SIGNING

        // The responder will often need to respond to a call to
        // ``CollectSignaturesFlow``. It does so my invoking its own
        // ``SignTransactionFlow`` subclass.
        // DOCSTART 16
        val signTransactionFlow: SignTransactionFlow = object : SignTransactionFlow(counterpartySession) {
            override fun checkTransaction(stx: SignedTransaction) = requireThat {
                // Any additional checking we see fit...
                val outputState = stx.tx.outputsOfType<DummyState>().single()
                require(outputState.magicNumber == 777)
            }
        }

        val idOfTxWeSigned = subFlow(signTransactionFlow).id
        // DOCEND 16

        /**-----------------------------
         * FINALISING THE TRANSACTION *
        -----------------------------**/
        progressTracker.currentStep = FINALISATION

        // As the final step the responder waits to receive the notarised transaction from the sending party
        // Since it knows the ID of the transaction it just signed, the transaction ID is specified to ensure the correct
        // transaction is received and recorded.
        // DOCSTART ReceiveFinalityFlow
        subFlow(ReceiveFinalityFlow(counterpartySession, expectedTxId = idOfTxWeSigned))
        // DOCEND ReceiveFinalityFlow
    }
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
package net.corda.docs.java;

import co.paralleluniverse.fibers.Suspendable;
import com.google.common.collect.ImmutableList;
import net.corda.core.contracts.*;
import net.corda.core.crypto.SecureHash;
import net.corda.core.crypto.TransactionSignature;
import net.corda.core.flows.*;
import net.corda.core.identity.CordaX500Name;
import net.corda.core.identity.Party;
import net.corda.core.identity.PartyAndCertificate;
import net.corda.core.internal.FetchDataFlow;
import net.corda.core.node.services.Vault;
import net.corda.core.node.services.Vault.Page;
import net.corda.core.node.services.vault.QueryCriteria.VaultQueryCriteria;
import net.corda.core.transactions.LedgerTransaction;
import net.corda.core.transactions.SignedTransaction;
import net.corda.core.transactions.TransactionBuilder;
import net.corda.core.utilities.ProgressTracker;
import net.corda.core.utilities.ProgressTracker.Step;
import net.corda.core.utilities.UntrustworthyData;
import net.corda.finance.contracts.asset.Cash;
import net.corda.testing.contracts.DummyContract;
import net.corda.testing.contracts.DummyState;
import org.jetbrains.annotations.NotNull;

import java.security.GeneralSecurityException;
import java.security.PublicKey;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.Set;

import static com.google.common.base.Preconditions.checkArgument;
import static java.util.Collections.*;
import static net.corda.core.contracts.ContractsDSL.requireThat;
import static net.corda.core.crypto.Crypto.generateKeyPair;

@SuppressWarnings("unused")
public class FlowCookbook {
    // ``InitiatorFlow`` is our first flow, and will communicate with
    // ``ResponderFlow``, below.
    // We mark ``InitiatorFlow`` as an ``InitiatingFlow``, allowing it to be
    // started directly by the node.
    @InitiatingFlow
    // We also mark ``InitiatorFlow`` as ``StartableByRPC``, allowing the
    // node's owner to start the flow via RPC.
    @StartableByRPC
    // Every flow must subclass ``FlowLogic``. The generic indicates the
    // flow's return type.
    public static class InitiatorFlow extends FlowLogic<Void> {

        private final boolean arg1;
        private final int arg2;
        private final Party counterparty;
        private final Party regulator;

        public InitiatorFlow(boolean arg1, int arg2, Party counterparty, Party regulator) {
            this.arg1 = arg1;
            this.arg2 = arg2;
            this.counterparty = counterparty;
            this.regulator = regulator;
        }

        /*----------------------------------
         * WIRING UP THE PROGRESS TRACKER *
        ----------------------------------*/
        // Giving our flow a progress tracker allows us to see the flow's
        // progress visually in our node's CRaSH shell.
        // DOCSTART 17
        private static final Step ID_OTHER_NODES = new Step("Identifying other nodes on the network.");
        private static final Step SENDING_AND_RECEIVING_DATA = new Step("Sending data between parties.");
        private static final Step EXTRACTING_VAULT_STATES = new Step("Extracting states from the vault.");
        private static final Step OTHER_TX_COMPONENTS = new Step("Gathering a transaction's other components.");
        private static final Step TX_BUILDING = new Step("Building a transaction.");
        private static final Step TX_SIGNING = new Step("Signing a transaction.");
        private static final Step TX_VERIFICATION = new Step("Verifying a transaction.");
        private static final Step SIGS_GATHERING = new Step("Gathering a transaction's signatures.") {
            // Wiring up a child progress tracker allows us to see the
            // subflow's progress steps in our flow's progress tracker.
            @Override
            public ProgressTracker childProgressTracker() {
                return CollectSignaturesFlow.tracker();
            }
        };
        private static final Step VERIFYING_SIGS = new Step("Verifying a transaction's signatures.");
        private static final Step FINALISATION = new Step("Finalising a transaction.") {
            @Override
            public ProgressTracker childProgressTracker() {
                return FinalityFlow.tracker();
            }
        };

        private final ProgressTracker progressTracker = new ProgressTracker(
                ID_OTHER_NODES,
                SENDING_AND_RECEIVING_DATA,
                EXTRACTING_VAULT_STATES,
                OTHER_TX_COMPONENTS,
                TX_BUILDING,
                TX_SIGNING,
                TX_VERIFICATION,
                SIGS_GATHERING,
                FINALISATION
        );
        // DOCEND 17

        @Suspendable
        @Override
        public Void call() throws FlowException {
            // We'll be using a dummy public key for demonstration purposes.
            PublicKey dummyPubKey = generateKeyPair().getPublic();

            /*---------------------------
             * IDENTIFYING OTHER NODES *
            ---------------------------*/
            // DOCSTART 18
            progressTracker.setCurrentStep(ID_OTHER_NODES);
            // DOCEND 18

            // A transaction generally needs a notary:
            //   - To prevent double-spends if the transaction has inputs
            //   - To serve as a timestamping authority if the transaction has a
            //     time-window
            // We retrieve a notary from the network map.
            // DOCSTART 01
            CordaX500Name notaryName = new CordaX500Name("Notary Service", "London", "GB");
            Party specificNotary = Objects.requireNonNull(getServiceHub().getNetworkMapCache().getNotary(notaryName));
            // Alternatively, we can pick an arbitrary notary from the notary
            // list. However, it is always preferable to specify the notary
            // explicitly, as the notary list might change when new notaries are
            // introduced, or old ones decommissioned.
            Party firstNotary = getServiceHub().getNetworkMapCache().getNotaryIdentities().get(0);
            // DOCEND 01

            // We may also need to identify a specific counterparty. We do so
            // using the identity service.
            // DOCSTART 02
            CordaX500Name counterPartyName = new CordaX500Name("NodeA", "London", "GB");
            Party namedCounterparty = getServiceHub().getIdentityService().wellKnownPartyFromX500Name(counterPartyName);
            Party keyedCounterparty = getServiceHub().getIdentityService().partyFromKey(dummyPubKey);
            // DOCEND 02

            /*------------------------------
             * SENDING AND RECEIVING DATA *
            ------------------------------*/
            progressTracker.setCurrentStep(SENDING_AND_RECEIVING_DATA);

            // We start by initiating a flow session with the counterparty. We
            // will use this session to send and receive messages from the
            // counterparty.
            // DOCSTART initiateFlow
            FlowSession counterpartySession = initiateFlow(counterparty);
            // DOCEND initiateFlow

            // We can send arbitrary data to a counterparty.
            // If this is the first ``send``, the counterparty will either:
            // 1. Ignore the message if they are not registered to respond
            //    to messages from this flow.
            // 2. Start the flow they have registered to respond to this flow,
            //    and run the flow until the first call to ``receive``, at
            //    which point they process the message.
            // In other words, we are assuming that the counterparty is
            // registered to respond to this flow, and has a corresponding
            // ``receive`` call.
            // DOCSTART 04
            counterpartySession.send(new Object());
            // DOCEND 04

            // We can wait to receive arbitrary data of a specific type from a
            // counterparty. Again, this implies a corresponding ``send`` call
            // in the counterparty's flow. A few scenarios:
            // - We never receive a message back. In the current design, the
            //   flow is paused until the node's owner kills the flow.
            // - Instead of sending a message back, the counterparty throws a
            //   ``FlowException``. This exception is propagated back to us,
            //   and we can use the error message to establish what happened.
            // - We receive a message back, but it's of the wrong type. In
            //   this case, a ``FlowException`` is thrown.
            // - We receive back a message of the correct type. All is good.
            //
            // Upon calling ``receive()`` (or ``sendAndReceive()``), the
            // ``FlowLogic`` is suspended until it receives a response.
            //
            // We receive the data wrapped in an ``UntrustworthyData``
            // instance. This is a reminder that the data we receive may not
            // be what it appears to be! We must unwrap the
            // ``UntrustworthyData`` using a lambda.
            // DOCSTART 05
            UntrustworthyData<Integer> packet1 = counterpartySession.receive(Integer.class);
            Integer integer = packet1.unwrap(data -> {
                // Perform checking on the object received.
                // T O D O: Check the received object.
                // Return the object.
                return data;
            });
            // DOCEND 05

            // We can also use a single call to send data to a counterparty
            // and wait to receive data of a specific type back. The type of
            // data sent doesn't need to match the type of the data received
            // back.
            // DOCSTART 07
            UntrustworthyData<Boolean> packet2 = counterpartySession.sendAndReceive(Boolean.class, "You can send and receive any class!");
            Boolean bool = packet2.unwrap(data -> {
                // Perform checking on the object received.
                // T O D O: Check the received object.
                // Return the object.
                return data;
            });
            // DOCEND 07

            // We're not limited to sending to and receiving from a single
            // counterparty. A flow can send messages to as many parties as it
            // likes, and each party can invoke a different response flow.
            // DOCSTART 06
            FlowSession regulatorSession = initiateFlow(regulator);
            regulatorSession.send(new Object());
            UntrustworthyData<Object> packet3 = regulatorSession.receive(Object.class);
            // DOCEND 06

            /*------------------------------------
             * EXTRACTING STATES FROM THE VAULT *
            ------------------------------------*/
            progressTracker.setCurrentStep(EXTRACTING_VAULT_STATES);

            // Let's assume there are already some ``DummyState``s in our
            // node's vault, stored there as a result of running past flows,
            // and we want to consume them in a transaction. There are many
            // ways to extract these states from our vault.

            // For example, we would extract any unconsumed ``DummyState``s
            // from our vault as follows:
            VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.UNCONSUMED);
            Page<DummyState> results = getServiceHub().getVaultService().queryBy(DummyState.class, criteria);
            List<StateAndRef<DummyState>> dummyStates = results.getStates();

            // For a full list of the available ways of extracting states from
            // the vault, see the Vault Query docs page.

            // When building a transaction, input states are passed in as
            // ``StateRef`` instances, which pair the hash of the transaction
            // that generated the state with the state's index in the outputs
            // of that transaction. In practice, we'd pass the transaction hash
            // or the ``StateRef`` as a parameter to the flow, or extract the
            // ``StateRef`` from our vault.
            // DOCSTART 20
            StateRef ourStateRef = new StateRef(SecureHash.sha256("DummyTransactionHash"), 0);
            // DOCEND 20
            // A ``StateAndRef`` pairs a ``StateRef`` with the state it points to.
            // DOCSTART 21
            StateAndRef ourStateAndRef = getServiceHub().toStateAndRef(ourStateRef);
            // DOCEND 21

            /*------------------------------------------
             * GATHERING OTHER TRANSACTION COMPONENTS *
            ------------------------------------------*/
            progressTracker.setCurrentStep(OTHER_TX_COMPONENTS);

            // Reference input states are constructed from StateAndRefs.
            // DOCSTART 55
            ReferencedStateAndRef referenceState = ourStateAndRef.referenced();
            // DOCEND 55
            // Output states are constructed from scratch.
            // DOCSTART 22
            DummyState ourOutputState = new DummyState();
            // DOCEND 22
            // Or as copies of other states with some properties changed.
            // DOCSTART 23
            DummyState ourOtherOutputState = ourOutputState.copy(77);
            // DOCEND 23

            // We then need to pair our output state with a contract.
            // DOCSTART 47
            StateAndContract ourOutput = new StateAndContract(ourOutputState, DummyContract.PROGRAM_ID);
            // DOCEND 47

            // Commands pair a ``CommandData`` instance with a list of
            // public keys. To be valid, the transaction requires a signature
            // matching every public key in all of the transaction's commands.
            // DOCSTART 24
            DummyContract.Commands.Create commandData = new DummyContract.Commands.Create();
            PublicKey ourPubKey = getServiceHub().getMyInfo().getLegalIdentitiesAndCerts().get(0).getOwningKey();
            PublicKey counterpartyPubKey = counterparty.getOwningKey();
            List<PublicKey> requiredSigners = ImmutableList.of(ourPubKey, counterpartyPubKey);
            Command<DummyContract.Commands.Create> ourCommand = new Command<>(commandData, requiredSigners);
            // DOCEND 24

            // ``CommandData`` can either be:
            // 1. Of type ``TypeOnlyCommandData``, in which case it only
            //    serves to attach signers to the transaction and possibly
            //    fork the contract's verification logic.
            TypeOnlyCommandData typeOnlyCommandData = new DummyContract.Commands.Create();
            // 2. Include additional data which can be used by the contract
            //    during verification, alongside fulfilling the roles above
            CommandData commandDataWithData = new Cash.Commands.Issue();

            // Attachments are identified by their hash.
            // The attachment with the corresponding hash must have been
            // uploaded ahead of time via the node's RPC interface.
            // DOCSTART 25
            SecureHash ourAttachment = SecureHash.sha256("DummyAttachment");
            // DOCEND 25

            // Time windows represent the period of time during which a
            // transaction must be notarised. They can have a start and an end
            // time, or be open at either end.
            // DOCSTART 26
            TimeWindow ourTimeWindow = TimeWindow.between(Instant.MIN, Instant.MAX);
            TimeWindow ourAfter = TimeWindow.fromOnly(Instant.MIN);
            TimeWindow ourBefore = TimeWindow.untilOnly(Instant.MAX);
            // DOCEND 26

            // We can also define a time window as an ``Instant`` +/- a time
            // tolerance (e.g. 30 seconds):
            // DOCSTART 42
            TimeWindow ourTimeWindow2 = TimeWindow.withTolerance(getServiceHub().getClock().instant(), Duration.ofSeconds(30));
            // DOCEND 42
            // Or as a start-time plus a duration:
            // DOCSTART 43
            TimeWindow ourTimeWindow3 = TimeWindow.fromStartAndDuration(getServiceHub().getClock().instant(), Duration.ofSeconds(30));
            // DOCEND 43

            /*------------------------
             * TRANSACTION BUILDING *
            ------------------------*/
            progressTracker.setCurrentStep(TX_BUILDING);

            // If our transaction has input states or a time-window, we must instantiate it with a
            // notary.
            // DOCSTART 19
            TransactionBuilder txBuilder = new TransactionBuilder(specificNotary);
            // DOCEND 19

            // Otherwise, we can choose to instantiate it without one:
            // DOCSTART 46
            TransactionBuilder txBuilderNoNotary = new TransactionBuilder();
            // DOCEND 46

            // We add items to the transaction builder using ``TransactionBuilder.withItems``:
            // DOCSTART 27
            txBuilder.withItems(
                    // Inputs, as ``StateAndRef``s that reference to the outputs of previous transactions
                    ourStateAndRef,
                    // Outputs, as ``StateAndContract``s
                    ourOutput,
                    // Commands, as ``Command``s
                    ourCommand,
                    // Attachments, as ``SecureHash``es
                    ourAttachment,
                    // A time-window, as ``TimeWindow``
                    ourTimeWindow
            );
            // DOCEND 27

            // We can also add items using methods for the individual components.

            // The individual methods for adding input states and attachments:
            // DOCSTART 28
            txBuilder.addInputState(ourStateAndRef);
            txBuilder.addAttachment(ourAttachment);
            // DOCEND 28

            // An output state can be added as a ``ContractState``, contract class name and notary.
            // DOCSTART 49
            txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID, specificNotary);
            // DOCEND 49
            // We can also leave the notary field blank, in which case the transaction's default
            // notary is used.
            // DOCSTART 50
            txBuilder.addOutputState(ourOutputState, DummyContract.PROGRAM_ID);
            // DOCEND 50
            // Or we can add the output state as a ``TransactionState``, which already specifies
            // the output's contract and notary.
            // DOCSTART 51
            TransactionState txState = new TransactionState<>(ourOutputState, DummyContract.PROGRAM_ID, specificNotary);
            // DOCEND 51

            // Commands can be added as ``Command``s.
            // DOCSTART 52
            txBuilder.addCommand(ourCommand);
            // DOCEND 52
            // Or as ``CommandData`` and a ``vararg PublicKey``.
            // DOCSTART 53
            txBuilder.addCommand(commandData, ourPubKey, counterpartyPubKey);
            // DOCEND 53

            // We can set a time-window directly.
            // DOCSTART 44
            txBuilder.setTimeWindow(ourTimeWindow);
            // DOCEND 44
            // Or as a start time plus a duration (e.g. 45 seconds).
            // DOCSTART 45
            txBuilder.setTimeWindow(getServiceHub().getClock().instant(), Duration.ofSeconds(45));
            // DOCEND 45

            /*-----------------------
             * TRANSACTION SIGNING *
            -----------------------*/
            progressTracker.setCurrentStep(TX_SIGNING);

            // We finalise the transaction by signing it,
            // converting it into a ``SignedTransaction``.
            // DOCSTART 29
            SignedTransaction onceSignedTx = getServiceHub().signInitialTransaction(txBuilder);
            // DOCEND 29
            // We can also sign the transaction using a different public key:
            // DOCSTART 30
            PartyAndCertificate otherIdentity = getServiceHub().getKeyManagementService().freshKeyAndCert(getOurIdentityAndCert(), false);
            SignedTransaction onceSignedTx2 = getServiceHub().signInitialTransaction(txBuilder, otherIdentity.getOwningKey());
            // DOCEND 30

            // If instead this was a ``SignedTransaction`` that we'd received
            // from a counterparty and we needed to sign it, we would add our
            // signature using:
            // DOCSTART 38
            SignedTransaction twiceSignedTx = getServiceHub().addSignature(onceSignedTx);
            // DOCEND 38
            // Or, if we wanted to use a different public key:
            PartyAndCertificate otherIdentity2 = getServiceHub().getKeyManagementService().freshKeyAndCert(getOurIdentityAndCert(), false);
            // DOCSTART 39
            SignedTransaction twiceSignedTx2 = getServiceHub().addSignature(onceSignedTx, otherIdentity2.getOwningKey());
            // DOCEND 39

            // We can also generate a signature over the transaction without
            // adding it to the transaction itself. We may do this when
            // sending just the signature in a flow instead of returning the
            // entire transaction with our signature. This way, the receiving
            // node does not need to check we haven't changed anything in the
            // transaction.
            // DOCSTART 40
            TransactionSignature sig = getServiceHub().createSignature(onceSignedTx);
            // DOCEND 40
            // And again, if we wanted to use a different public key:
            // DOCSTART 41
            TransactionSignature sig2 = getServiceHub().createSignature(onceSignedTx, otherIdentity2.getOwningKey());
            // DOCEND 41

            /*----------------------------
             * TRANSACTION VERIFICATION *
            ----------------------------*/
            progressTracker.setCurrentStep(TX_VERIFICATION);

            // Verifying a transaction will also verify every transaction in
            // the transaction's dependency chain, which will require
            // transaction data access on counterparty's node. The
            // ``SendTransactionFlow`` can be used to automate the sending and
            // data vending process. The ``SendTransactionFlow`` will listen
            // for data request until the transaction is resolved and verified
            // on the other side:
            // DOCSTART 12
            subFlow(new SendTransactionFlow(counterpartySession, twiceSignedTx));

            // Optional request verification to further restrict data access.
            subFlow(new SendTransactionFlow(counterpartySession, twiceSignedTx) {
                @Override
                protected void verifyDataRequest(@NotNull FetchDataFlow.Request.Data dataRequest) {
                    // Extra request verification.
                }
            });
            // DOCEND 12

            // We can receive the transaction using ``ReceiveTransactionFlow``,
            // which will automatically download all the dependencies and verify
            // the transaction and then record in our vault
            // DOCSTART 13
            SignedTransaction verifiedTransaction = subFlow(new ReceiveTransactionFlow(counterpartySession));
            // DOCEND 13

            // We can also send and receive a `StateAndRef` dependency chain and automatically resolve its dependencies.
            // DOCSTART 14
            subFlow(new SendStateAndRefFlow(counterpartySession, dummyStates));

            // On the receive side ...
            List<StateAndRef<DummyState>> resolvedStateAndRef = subFlow(new ReceiveStateAndRefFlow<>(counterpartySession));
            // DOCEND 14

            try {

                // We can now verify the transaction to ensure that it satisfies
                // the contracts of all the transaction's input and output states.
                // DOCSTART 33
                twiceSignedTx.verify(getServiceHub());
                // DOCEND 33

                // We'll often want to perform our own additional verification
                // too. Just because a transaction is valid based on the contract
                // rules and requires our signature doesn't mean we have to
                // sign it! We need to make sure the transaction represents an
                // agreement we actually want to enter into.

                // To do this, we need to convert our ``SignedTransaction``
                // into a ``LedgerTransaction``. This will use our ServiceHub
                // to resolve the transaction's inputs and attachments into
                // actual objects, rather than just references.
                // DOCSTART 32
                LedgerTransaction ledgerTx = twiceSignedTx.toLedgerTransaction(getServiceHub());
                // DOCEND 32

                // We can now perform our additional verification.
                // DOCSTART 34
                DummyState outputState = ledgerTx.outputsOfType(DummyState.class).get(0);
                if (outputState.getMagicNumber() != 777) {
                    // ``FlowException`` is a special exception type. It will be
                    // propagated back to any counterparty flows waiting for a
                    // message from this flow, notifying them that the flow has
                    // failed.
                    throw new FlowException("We expected a magic number of 777.");
                }
                // DOCEND 34

            } catch (GeneralSecurityException e) {
                // Handle this as required.
            }

            // Of course, if you are not a required signer on the transaction,
            // you have no power to decide whether it is valid or not. If it
            // requires signatures from all the required signers and is
            // contractually valid, it's a valid ledger update.

            /*------------------------
             * GATHERING SIGNATURES *
            ------------------------*/
            progressTracker.setCurrentStep(SIGS_GATHERING);

            // The list of parties who need to sign a transaction is dictated
            // by the transaction's commands. Once we've signed a transaction
            // ourselves, we can automatically gather the signatures of the
            // other required signers using ``CollectSignaturesFlow``.
            // The responder flow will need to call ``SignTransactionFlow``.
            // DOCSTART 15
            SignedTransaction fullySignedTx = subFlow(new CollectSignaturesFlow(twiceSignedTx, emptySet(), SIGS_GATHERING.childProgressTracker()));
            // DOCEND 15

            /*------------------------
             * VERIFYING SIGNATURES *
            ------------------------*/
            progressTracker.setCurrentStep(VERIFYING_SIGS);

            try {

                // We can verify that a transaction has all the required
                // signatures, and that they're all valid, by running:
                // DOCSTART 35
                fullySignedTx.verifyRequiredSignatures();
                // DOCEND 35

                // If the transaction is only partially signed, we have to pass in
                // a vararg of the public keys corresponding to the missing
                // signatures, explicitly telling the system not to check them.
                // DOCSTART 36
                onceSignedTx.verifySignaturesExcept(counterpartyPubKey);
                // DOCEND 36

                // There is also an overload of ``verifySignaturesExcept`` which accepts
                // a ``Collection`` of the public keys corresponding to the missing
                // signatures. In the example below, we could also use
                // ``Arrays.asList(counterpartyPubKey)`` instead of
                // ``Collections.singletonList(counterpartyPubKey)``.
                // DOCSTART 54
                onceSignedTx.verifySignaturesExcept(singletonList(counterpartyPubKey));
                // DOCEND 54

                // We can also choose to only check the signatures that are
                // present. BE VERY CAREFUL - this function provides no guarantees
                // that the signatures are correct, or that none are missing.
                // DOCSTART 37
                twiceSignedTx.checkSignaturesAreValid();
                // DOCEND 37
            } catch (GeneralSecurityException e) {
                // Handle this as required.
            }

            /*------------------------------
             * FINALISING THE TRANSACTION *
            ------------------------------*/
            progressTracker.setCurrentStep(FINALISATION);

            // We notarise the transaction and get it recorded in the vault of
            // the participants of all the transaction's states.
            // DOCSTART 09
            SignedTransaction notarisedTx1 = subFlow(new FinalityFlow(fullySignedTx, singleton(counterpartySession), FINALISATION.childProgressTracker()));
            // DOCEND 09
            // We can also choose to send it to additional parties who aren't one
            // of the state's participants.
            // DOCSTART 10
            List<FlowSession> partySessions = Arrays.asList(counterpartySession, initiateFlow(regulator));
            SignedTransaction notarisedTx2 = subFlow(new FinalityFlow(fullySignedTx, partySessions, FINALISATION.childProgressTracker()));
            // DOCEND 10

            return null;
        }
    }

    // ``ResponderFlow`` is our second flow, and will communicate with
    // ``InitiatorFlow``.
    // We mark ``ResponderFlow`` as an ``InitiatedByFlow``, meaning that it
    // can only be started in response to a message from its initiating flow.
    // That's ``InitiatorFlow`` in this case.
    // Each node also has several flow pairs registered by default - see
    // ``AbstractNode.installCoreFlows``.
    @InitiatedBy(InitiatorFlow.class)
    public static class ResponderFlow extends FlowLogic<Void> {

        private final FlowSession counterpartySession;

        public ResponderFlow(FlowSession counterpartySession) {
            this.counterpartySession = counterpartySession;
        }

        private static final Step RECEIVING_AND_SENDING_DATA = new Step("Sending data between parties.");
        private static final Step SIGNING = new Step("Responding to CollectSignaturesFlow.");
        private static final Step FINALISATION = new Step("Finalising a transaction.");

        private final ProgressTracker progressTracker = new ProgressTracker(
                RECEIVING_AND_SENDING_DATA,
                SIGNING,
                FINALISATION
        );

        @Suspendable
        @Override
        public Void call() throws FlowException {
            // The ``ResponderFlow` has all the same APIs available. It looks
            // up network information, sends and receives data, and constructs
            // transactions in exactly the same way.

            /*------------------------------
             * SENDING AND RECEIVING DATA *
             -----------------------------*/
            progressTracker.setCurrentStep(RECEIVING_AND_SENDING_DATA);

            // We need to respond to the messages sent by the initiator:
            // 1. They sent us an ``Object`` instance
            // 2. They waited to receive an ``Integer`` instance back
            // 3. They sent a ``String`` instance and waited to receive a
            //    ``Boolean`` instance back
            // Our side of the flow must mirror these calls.
            // DOCSTART 08
            Object obj = counterpartySession.receive(Object.class).unwrap(data -> data);
            String string = counterpartySession.sendAndReceive(String.class, 99).unwrap(data -> data);
            counterpartySession.send(true);
            // DOCEND 08

            /*-----------------------------------------
             * RESPONDING TO COLLECT_SIGNATURES_FLOW *
            -----------------------------------------*/
            progressTracker.setCurrentStep(SIGNING);

            // The responder will often need to respond to a call to
            // ``CollectSignaturesFlow``. It does so my invoking its own
            // ``SignTransactionFlow`` subclass.
            // DOCSTART 16
            class SignTxFlow extends SignTransactionFlow {
                private SignTxFlow(FlowSession otherSession, ProgressTracker progressTracker) {
                    super(otherSession, progressTracker);
                }

                @Override
                protected void checkTransaction(@NotNull SignedTransaction stx) {
                    requireThat(require -> {
                        // Any additional checking we see fit...
                        DummyState outputState = (DummyState) stx.getTx().getOutputs().get(0).getData();
                        checkArgument(outputState.getMagicNumber() == 777);
                        return null;
                    });
                }
            }

            SecureHash idOfTxWeSigned = subFlow(new SignTxFlow(counterpartySession, SignTransactionFlow.tracker())).getId();
            // DOCEND 16

            /*------------------------------
             * FINALISING THE TRANSACTION *
            ------------------------------*/
            progressTracker.setCurrentStep(FINALISATION);

            // As the final step the responder waits to receive the notarised transaction from the sending party
            // Since it knows the ID of the transaction it just signed, the transaction ID is specified to ensure the correct
            // transaction is received and recorded.
            // DOCSTART ReceiveFinalityFlow
            subFlow(new ReceiveFinalityFlow(counterpartySession, idOfTxWeSigned));
            // DOCEND ReceiveFinalityFlow

            return null;
        }
    }
}

```
{{% /tab %}}




[FlowCookbook.kt](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/FlowCookbook.kt) | [FlowCookbook.java](https://github.com/corda/corda/blob/release/os/4.3/docs/source/example-code/src/main/java/net/corda/docs/java/FlowCookbook.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}
