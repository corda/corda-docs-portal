---
date: '2021-09-16'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-int-test
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1080
tags:
- tutorial
- cordapp
title: Write and run integration tests
---

After you've built your CorDapp, it can be useful to write and run integration tests to be sure that all parts of your application are working together as they should be. Use integration tests to test the CorDapp's elements as a group against a locally-deployed Corda 5 network.

In the Corda 5 Developer Preview you can use the `corda-dev-network-lib` to run these tests. This test library connects your test code with the specified test network and its node.

You should create a testing case to correspond with each flow in the app. In this tutorial you will be writing integration tests for all three flows:

* `CreateAndIssueMarsVoucher` flow
* `CreateBoardingTicket` flow
* `RedeemBoardingTicketWithVoucher` flow

You will create these tests in the `workflows/src/integrationTest/kotlin/net/corda/missionMars` directory in this tutorial. Refer to the `TemplateFlowTest.kt` file in this directory to see a template state.

## Learning objectives

After you have completed this tutorial, you will know how to write and run integration tests for CorDapps built on the Corda 5 Developer Preview.

## Before you start

Before you start writing integration tests you must [deploy your CorDapp to a local Corda 5 network](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-running.html#deploy-your-cordapp-to-a-local-corda-5-network).

## Create an integration test for the `CreateAndIssueMarsVoucher` flow

This integration test checks that your `CreateAndIssueMarsVoucher` flow has executed and that it has come back as `COMPLETED`. Create an integration test for this flow by following these steps:

### Modify the `build.gradle` file

You need to make a few changes in the `build.gradle` file of your CorDapp to connect your test code to the network where you've deployed your CorDapp.

1. Register your integration test:

   ```kotlin
   tasks.register('integrationTest', Test) {
       description = "Runs integration tests."
       group = "verification"

       testClassesDirs = project.sourceSets["integrationTest"].output.classesDirs
       classpath = project.sourceSets["integrationTest"].runtimeClasspath
   }
   ```

2. Add a dependency referencing the test library:

   ```kotlin
   integrationTestImplementation "net.corda:corda-dev-network-lib:$cordaAPIVersion"
   ```
This ensures that your integration tests can use the network created using Corda CLI.

### Copy the `TemplateFlowTest`

When writing integration tests, it's helpful to start from the template as some features of your test will be identical to the template.

1. Copy the contents of the `TemplateFlowTest` file.
2. Paste the contents into a new Kotlin file called `CreateAndIssueMarsVoucherTest`.

### Change `TemplateFlow` to `CreateAndIssueMarsVoucher`

Change all instances of `TemplateFlow` throughout the template to `CreateAndIssueMarsVoucher`.

### Add the details of the network you are running

In the first block of code you are connecting your integration tests to the network you have deployed.

<!---
`PartyA` and `PartyB` are pulled from your network `.yaml` file, in this case `mission-mars.yaml`.--->

Under `networkName`, change `template-network` to `missionmars-network`.

### Keep helper methods

There are three helper methods in the template that translate what you put into your test to JSON in order to populate the API. You do not need to make any changes to these methods.

Leave these methods as they are:

* `startFlow`
* `eventually`

### Change the `templateFlowParams` to `CreateAndIssueMarsVoucherParams` helper method

You must change the `templateFlowParams` to the `CreateAndIssueMarsVoucherParams` helper method. The `CreateAndIssueMarsVoucherParams` helper method takes parameters specific to this flow (`voucherDesc` and `holder`) and converts them into JSON. This performs the same function as the template helper methods, but covers parameters specific to this flow.

Add the helper function with `voucherDesc` and `holder` parameters, and return a `GsonBuilder`.

### Add the test content

Make changes in the `template Test` code block to add your testing content.

1. Indicate the network the test will use: `networkName: missionmars-network`.
2. In the next line, get the identity of `PartyB`. This is done for you in the template code.
3. Use the built-in `getNode` method to add `PartyA`'s credentials and log in. These are listed in the network `.yaml` file.
4. Assign a launch pad to the `clientId`.
5. Under the `flowId`, you are calling `startFlow` to return the `flowId`. Fill in details for the `voucherDesc` and `holder` parameters. The helper method converts these to JSON. Whether the flow fails or succeeds, it will have a `flowId`.
6. You do not need to modify the next block of code. These `Assertions` check that:
    * The HTTP status of the flow is OK.
    * The `clientId`s match.
    * The `flowId` is correct in the JSON Object.
    * The `flowId` is not null. If it is null, that means your flow is stuck.
    * The `flowId` is returned as a `String`.
7. You do not need to modify the next block of code. The block that begins with `eventually` is executing the `retrieveOutcome` method and passing the `flowId`. It checks that:
    * The HTTP status of the flow is OK.
    * The status of the flow is `COMPLETED`.

You have finished writing the integration test for the `CreateAndIssueMarsVoucher` flow. Your test should look like this:

```kotlin
package net.corda.missionMars

import com.google.gson.GsonBuilder
import kong.unirest.HttpResponse
import kong.unirest.JsonNode
import kong.unirest.Unirest
import kong.unirest.json.JSONObject
import net.corda.missionMars.flows.CreateAndIssueMarsVoucherInitiator
import net.corda.missionMars.flows.TemplateFlow
import net.corda.test.dev.network.Credentials
import net.corda.test.dev.network.TestNetwork
import net.corda.test.dev.network.withFlow
import net.corda.test.dev.network.x500Name
import org.apache.http.HttpStatus
import org.assertj.core.api.Assertions
import org.junit.jupiter.api.BeforeAll
import org.junit.jupiter.api.Test
import java.time.Duration
import java.util.*

class CreateAndIssueMarsVoucherTest {
    companion object {
        @JvmStatic
        @BeforeAll
        fun setup() {
            TestNetwork.forNetwork("missionmars-network").verify {
                hasNode("PartyA").withFlow<TemplateFlow>()
                hasNode("PartyB").withFlow<TemplateFlow>()
            }
        }
    }

    @Test
    fun `Create And Issue MarsVoucher Test`(){
        TestNetwork.forNetwork("missionmars-network").use {
            val partyB = getNode("PartyB")
            getNode("PartyA").httpRpc(Credentials("angelenos","password")){
                val clientId = "Launch Pad 1"
                val flowId = with(startFlow(
                        flowName = CreateAndIssueMarsVoucherInitiator::class.java.name,
                        clientId = clientId,
                        parametersInJson = CreateAndIssueMarsVoucherParams(
                                voucherDesc = "Space Shuttle 323",
                                holder = partyB.x500Name.toString(),
                        )
                )){
                    Assertions.assertThat(status).isEqualTo(HttpStatus.SC_OK)
                    Assertions.assertThat(body.`object`.get("clientId")).isEqualTo(clientId)
                    val flowId = body.`object`.get("flowId") as JSONObject
                    Assertions.assertThat(flowId).isNotNull
                    flowId.get("uuid") as String
                }
                eventually {
                    with(retrieveOutcome(flowId)) {
                        Assertions.assertThat(status).isEqualTo(HttpStatus.SC_OK)
                        Assertions.assertThat(body.`object`.get("status")).isEqualTo("COMPLETED")
                    }
                }
            }
        }
    }
    //helper method.
    private fun CreateAndIssueMarsVoucherParams(voucherDesc: String, holder: String): String {
        return GsonBuilder()
                .create()
                .toJson(mapOf("voucherDesc" to voucherDesc, "holder" to holder))
    }





    private fun startFlow(
            flowName: String,
            clientId: String = "client-${UUID.randomUUID()}",
            parametersInJson: String
    ): HttpResponse<JsonNode> {
        val body = mapOf(
                "rpcStartFlowRequest" to
                        mapOf(
                                "flowName" to flowName,
                                "clientId" to clientId,
                                "parameters" to mapOf("parametersInJson" to parametersInJson)
                        )
        )
        val request = Unirest.post("flowstarter/startflow")
                .header("Content-Type", "application/json")
                .body(body)

        return request.asJson()
    }

    private fun retrieveOutcome(flowId: String): HttpResponse<JsonNode> {
        val request = Unirest.get("flowstarter/flowoutcome/$flowId").header("Content-Type", "application/json")
        return request.asJson()
    }

    private inline fun <R> eventually(
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

## Create integration tests for the `CreateBoardingTicket` flow and the `RedeemBoardingTicketWithVoucher` flow

Now that you've written the integration test for `CreateAndIssueMarsVoucher`, try writing the tests for the two other flows in your CorDapp: `CreateBoardingTicket` and `RedeemBoardingTicketWithVoucher`. Check your work against the [missionmars solution](https://github.com/corda/samples-kotlin-corda5/tree/main/Tutorial/missionmars).
