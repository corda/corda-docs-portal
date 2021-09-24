---
date: '2021-09-07'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    weight: 9300
project: corda-5
section_menu: corda-5-dev-preview
title: Running integration tests
---

Integration testing lets you combine different CorDapp elements and test them as a group against a Corda network that has been deployed locally.

Corda 5 introduces the `corda-dev-network-lib` test library, which you can use to run integration tests on your CorDapp. It connects your test code with the specified test network and its nodes. Do not use `corda-dev-network-lib` in production code.

This guide provides code to create a sample CorDapp. You'll create and deploy your sample CorDapp to a local network, then create and run a Corda 5 network integration test for the CorDapp.

## Before you start

Before you can deploy your sample CorDapp and perform Corda 5 network integration tests, you must [set up a Corda 5 network locally](../getting-started/setup-network.md).

## Create your CorDapp

You can add integration tests to your CorDapp to test it against a local network.
In this example, your flow and contract code look like this:

### Flow code

```kotlin
package net.corda.samples.iou.flows

import net.corda.samples.iou.contracts.IOUContract
import net.corda.samples.iou.states.IOUState
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
import net.corda.v5.ledger.contracts.Command
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.services.NotaryLookupService
import net.corda.v5.ledger.transactions.SignedTransaction
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import net.corda.v5.ledger.transactions.TransactionBuilderFactory

/**
 * This flow allows two parties (the [Initiator] and the [Acceptor]) to come to an agreement about the IOU encapsulated
 * within an [IOUState].
 *
 * In this example, the [Acceptor] always accepts a valid IOU.
 *
 * These flows have deliberately been implemented by using only the call() method for ease of understanding. In
 * practice, it is recommended splitting up the various stages of the flow into sub-routines.
 *
 * All methods called within the [Flow] sub-class need to be annotated with the @Suspendable annotation.
 */
@InitiatingFlow
@StartableByRPC
class ExampleFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) :
    Flow<SignedTransactionDigest> {
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

    /**
     * The flow logic is encapsulated within the call() method.
     */
    @Suspendable
    override fun call(): SignedTransactionDigest {
        // parse parameters
        val mapOfParams: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)

        val iouValue = with(mapOfParams["iouValue"] ?: throw BadRpcStartFlowRequestException("Parameter \"iouValue\" missing.")) {
            this.toInt()
        }

        val recipient = with(mapOfParams["recipient"] ?: throw BadRpcStartFlowRequestException("Parameter \"recipient\" missing.")) {
            CordaX500Name.parse(this)
        }
        val recipientParty = identityService.partyFromName(recipient)
            ?: throw NoSuchElementException("No party found for X500 name $recipient")

        val notary = notaryLookup.notaryIdentities.first()

        // Stage 1.
        // Generate an unsigned transaction.
        val iouState = IOUState(iouValue, flowIdentity.ourIdentity, recipientParty)
        val txCommand = Command(IOUContract.Commands.Create(), iouState.participants.map { it.owningKey })
        val txBuilder = transactionBuilderFactory.create()
            .setNotary(notary)
            .addOutputState(iouState, IOUContract.ID)
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

@InitiatedBy(ExampleFlow::class)
class ExampleFlowAcceptor(val otherPartySession: FlowSession) : Flow<SignedTransaction> {
    @CordaInject
    lateinit var flowEngine: FlowEngine

    fun isValid(stx: SignedTransaction) {
        requireThat {
            val output = stx.tx.outputs.single().data
            "This must be an IOU transaction." using (output is IOUState)
            val iou = output as IOUState
            "I won't accept IOUs with a value over 100." using (iou.value <= 100)
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

### Contract code

```kotlin
package net.corda.samples.iou.contracts

import net.corda.samples.iou.states.IOUState
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireSingleCommand
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction
import net.corda.v5.ledger.transactions.outputsOfType

/**
 * An implementation of a basic smart contract in Corda.
 *
 * This contract enforces rules regarding the creation of a valid [IOUState], which in turn encapsulates an [IOUState].
 *
 * For a new [IOUState] to be issued onto the ledger, a transaction is required. The transaction takes:
 * - Zero input states.
 * - One output state: the new [IOUState].
 * - A Create() command with the public keys of both the lender and the borrower.
 *
 * All contracts must sub-class the [Contract] interface.
 */
class IOUContract : Contract {
    companion object {
        @JvmStatic
        val ID = IOUContract::class.java.canonicalName
    }

    /**
     * The verify() function of all the states' contracts must not throw an exception for a transaction to be
     * considered valid.
     */
    override fun verify(tx: LedgerTransaction) {
        val command = tx.commands.requireSingleCommand<Commands.Create>()
        requireThat {
            // Generic constraints around the IOU transaction.
            "No inputs should be consumed when issuing an IOU." using (tx.inputs.isEmpty())
            "Only one output state should be created." using (tx.outputs.size == 1)
            val out = tx.outputsOfType<IOUState>().single()
            "The lender and the borrower cannot be the same entity." using (out.lender != out.borrower)
            "All of the participants must be signers." using (command.signers.containsAll(out.participants.map { it.owningKey }))

            // IOU-specific constraints.
            "The IOU's value must be non-negative." using (out.value > 0)
        }
    }

    /**
     * This contract only implements one command, Create.
     */
    interface Commands : CommandData {
        class Create : Commands
    }
}
```


## Deploy your CorDapp

Now, [deploy your sample CorDapp to a local Corda 5 development network](deploy-cordapps.md).

In this example, your CorDapp has been deployed to a local network called `sample-network`: `corda-cli network deploy -n sample-network | docker-compose -f - up`


## Create integration tests

The integrations tests run against a "real" Corda network. You can use the `corda-dev-network-lib` library to create tests against this network.

{{< note >}}

The test _does not_ create or configure the network. It assumes that the network already exists.

{{< /note >}}

To create an integration test:

1. Create an `integrationTest` subdirectory in your workflow project.

2. Add the following code to your `build.gradle` file:

   ```groovy
   sourceSets {
     integrationTest {
          kotlin {
              srcDirs += "src/integrationTest/kotlin"
            }
            java {
              srcDirs += "src/integrationTest/java"
            }
            resources {
              srcDirs += "src/integrationTest/resources"
            }
            compileClasspath += main.output + test.output
            runtimeClasspath += main.output + test.output
          }
        }

        kotlin {
          target {
            java
              compilations.integrationTest {
                associateWith compilations.main
                associateWith compilations.test

                configurations {
                  integrationTestApi.extendsFrom testApi
                  integrationTestImplementation.extendsFrom testImplementation
                  integrationTestRuntimeOnly.extendsFrom testRuntimeOnly
                }

                tasks.register('integrationTest', Test) {
                  description = "Runs integration tests."
                  group = "verification"

                  testClassesDirs = project.sourceSets["integrationTest"].output.classesDirs
                  classpath = project.sourceSets["integrationTest"].runtimeClasspath
                }
              }
            }
          }
          ```

3. Reference the integration test library:

   ```groovy
   integrationTestImplementation "net.corda:corda-dev-network-lib:5.0.0-DevPreview"
   ```

   {{< note >}}

   * The `corda-dev-network-lib` is simply "glue" between your test code and the network. It uses a HTTP connection to the node as well as the docker APIs to discover the network.
   * Because it is using the HTTP RPC API, it is asynchronous. Your test will need to take this into account.

   {{< /note >}}

4. Now you can create a Kotlin or Java source folder and add your integration test class(es). For example:

    ```kotlin
    package net.corda.samples.iou

    import com.google.gson.Gson
    import com.google.gson.GsonBuilder
    import net.corda.client.rpc.flow.FlowStarterRPCOps
    import net.corda.client.rpc.flow.RpcStartFlowRequest
    import net.corda.samples.iou.flows.ExampleFlow
    import net.corda.samples.iou.states.IOUStateDto
    import net.corda.test.dev.network.FlowUtils.returnValue
    import net.corda.test.dev.network.TestNetwork
    import net.corda.test.dev.network.httpRpcClient
    import net.corda.v5.application.flows.RpcStartFlowRequestParameters
    import net.corda.v5.base.util.seconds
    import net.corda.v5.ledger.transactions.SignedTransactionDigest
    import org.assertj.core.api.Assertions.assertThat
    import org.assertj.core.api.SoftAssertions.assertSoftly
    import org.junit.jupiter.api.Test
    import org.junit.jupiter.api.assertDoesNotThrow
    import java.time.Duration
    import java.util.*

    class ExampleFlowTest {
        @Test
        fun `Start Flow`() {
            TestNetwork.forNetwork("sample-network").use {

                // Find bob...
                val bob = getNode("bob").x500Name
                val tx = getNode("alice").httpRpcClient<FlowStarterRPCOps, SignedTransactionDigest> {
                    // Pay Bob
                    val startFlowParams = RpcStartFlowRequestParameters(
                        GsonBuilder().create()
                            .toJson(
                                mapOf(
                                    "iouValue" to "20",
                                    "recipient" to bob.toString()
                                )
                            )
                    )
                    val clientId = "client-${UUID.randomUUID()}"
                    val flowResponse = startFlow(
                        RpcStartFlowRequest(
                            ExampleFlow::class.java.name,
                            clientId,
                            startFlowParams
                        )
                    )

                    assertThat(flowResponse).isNotNull

                    eventually(30.seconds) {
                        assertDoesNotThrow { flowResponse.returnValue(this) }
                    }
                }

                // Verify that the transaction had greeting from Alice
                assertThat(tx.outputStates).hasSize(1)

                val state = Gson().fromJson(tx.outputStates.single(), IOUStateDto::class.java)
                assertSoftly {
                    it.assertThat(state.borrower).isEqualTo(bob.toString())
                    it.assertThat(state.lender).isEqualTo(getNode("alice").x500Name.toString())
                    it.assertThat(state.value).isEqualTo(20)
                }

                // Verify that two parties sign the greeting
                assertThat(tx.signatures)
                    .hasSize(2)
            }
        }

        inline fun <R> eventually(
            duration: Duration = Duration.ofSeconds(5),
            waitBetween: Duration = Duration.ofMillis(100),
            waitBefore: Duration = waitBetween,
            test: () -> R
        ): R {
            val end = System.nanoTime() + duration.toNanos()
            var times = 0
            var lastFailure: AssertionError? = null

            if (!waitBefore.isZero) Thread.sleep(waitBefore.toMillis())

            while (System.nanoTime() < end) {
                try {
                    return test()
                } catch (e: AssertionError) {
                    if (!waitBetween.isZero) Thread.sleep(waitBetween.toMillis())
                    lastFailure = e
                }
                times++
            }

            throw AssertionError("Test failed with \"${lastFailure?.message}\" after $duration; attempted $times times")
        }
    }
    ```

`TestNetwork.forNetwork("sample-network")` creates a connection to the `sample-network` network created by the Corda CLI. Behind the scenes, conventions discover the containers that make up the network. The `use` method returns an abstraction of the network. This lets you connect to a node.

Use `getNode("alice")` where `alice` is the name of the node you configured when you created the test network. This returns an abstraction of a Corda node. You can use this to connect to the node and start a flow.


## Run your tests

Run your tests from the IDE as you usually would, or from Gradle by running `gradle integrationTest`.

## Re-using the network

The integration test library does not create or configure the network. This means that many tests can run against the same network and node, which speeds up the tests. Tests should tolerate existing states.

To re-run your tests after making a change to your CorDapp, redeploy your CorDapp using `corda-cli` before running the tests.

## Debugging

You can debug Integration tests from the IDE. However, often it is useful to debug the node, too. The node runs on a remote process in a Docker container, and _not_ in the same process as the test, so you need to attach a remote debugger to any node you would like to debug.

For more information on how to debug a node in the Corda 5 development network, see [Debugging CorDapps](debugging-cordapps.md).

## Removal of the mock network feature in Corda 5

The `MockNetwork` functionality (in-memory testing) has been removed and replaced with [testing capabilities in the Corda CLI](../corda-cli/commands.md). This update dramatically speeds up node start times and reduces memory requirements.
- For [unit testing](flow-unit-testing.md), you can use the `corda-dev-network-lib` library with the unit testing framework of your choice.
- For [integration testing](#running-integration-tests.md), you can [deploy a network](../getting-started/setup-network.md) with Docker, locally or in a remote environment.

Classes related to `MockNetwork` have been removed:

* `MockAttachmentStorage`
* `MockMessagingService.Companion`
* `MockNetFlowTimeOut`
* `MockNetNotaryConfig`
* `MockNetwork`
* `MockNetworkNotarySpec`
* `MockNetworkParameters`
* `MockNodeConfigOverrides`
* `MockNodeParameters`
* `MockServices`
* `MockServices.Companion`
* `MockServicesKt`
