---
date: '2022-09-20'
title: "Testing CorDapps with Simulator"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-simulator
    weight: 4000
section_menu: corda-5-dev-preview
---
When writing any application, including CorDapps, it is helpful to have a fast feedback loop: code-test-debug-modify.
This accelerates the development process.
Although it is possible to develop directly against a Corda cluster, (as described in [Running your first CorDapp](../running-first-cordapp/run-first-cordapp.html)), to deploy a CorDapp onto a Corda cluster takes some time and manually hitting endpoints is a clumsy way to unit test.

To make the development process much slicker, R3 have developed **Simulator**.
Simulator is a lightweight testing and demo tool that simulates a Corda 5 network, enabling you to run CorDapps, demonstrate realistic behaviour, and receive feedback on how the CorDapp is likely to behave with a real Corda network.
Importantly, it is not a ‘light’ version of Corda. There is no Corda code running under the hood.
Think of it as a framework for executing flow code that injects simulated Corda services into the flows at the same point Corda would inject the real services.
Simulator runs in-process so it easy to set breakpoints in the code and use it for debugging.
{{< note >}}
As Simulator is not executing Corda code, the error messages are likely to be different from Corda. Whilst the intention is to simulate all of the Corda API, there may be small differences.
{{< /note >}}

## Using Simulator
Simulator is designed to be used within a normal Java or Kotlin testing framework. In this documentation, we describe using JUnit. `MyFirstFlow` has a corresponding test class `MyFirstFlowTest` that demonstrates how to use Simulator. The file is in `/src/test/kotlin/com.r3.developers.csdetemplate.MyFirstFlowTest.kt` in the [CSDE](../cordapp-standard-development-environment/csde.html) template repository.

The full listing with explanatory comments is as follows:
```kotlin
package com.r3.developers.csdetemplate

import net.corda.simulator.HoldingIdentity
import net.corda.simulator.RequestData
import net.corda.simulator.Simulator
import net.corda.v5.base.types.MemberX500Name
import org.junit.jupiter.api.Test

class MyFirstFlowTest {

    // Names picked to match the corda network in config/dev-net.json
    private val aliceX500 = MemberX500Name.parse("CN=Alice, OU=Test Dept, O=R3, L=London, C=GB")
    private val bobX500 = MemberX500Name.parse("CN=Bob, OU=Test Dept, O=R3, L=London, C=GB")

    @Test
    fun `test that MyFirstFLow returns correct message`() {

        // Instantiate an instance of the Simulator
        val simulator = Simulator()

        // Create Alice's and Bob HoldingIDs
        val aliceHoldingID = HoldingIdentity.Companion.create(aliceX500)
        val bobHoldingID = HoldingIdentity.Companion.create(bobX500)

        // Create Alice and Bob's virtual nodes, including the Class's of the flows which will be registered on each node.
        val aliceVN = simulator.createVirtualNode(aliceHoldingID, MyFirstFlow::class.java)
        val bobVN = simulator.createVirtualNode(bobHoldingID, MyFirstFlowResponder::class.java)

        // Create an instance of the MyFirstFlowStartArgs which contains the request arguments for starting the flow
        val myFirstFlowStartArgs = MyFirstFlowStartArgs(bobX500)

        // Create a requestData object
        val requestData = RequestData.create(
            "request no 1",        // A unique reference for the instance of the flow request
            MyFirstFlow::class.java,        // The name of the flow class which is to be started
            myFirstFlowStartArgs            // The object which contains the start arguments of the flow
        )

        // Call the Flow on Alice's virtual node and capture the response from the flow
        val flowResponse = aliceVN.callFlow(requestData)

        // Check that the flow has returned the expected string
        assert(flowResponse == "Hello Alice, best wishes from Bob")
    }
}
```
To run the test, click the green triangle next to the test method and select Run **MyFirstFlowTest…**:
{{< figure src="run-test.png" figcaption="Run MyFirstFlowTest" alt="Command to run MyFirstFlowTest in IntelliJ" >}}
Alternatively, if you had multiple tests in the class, you could click the double triangle next to the class declaration to run all of the tests in the class.

The output should look as follows:
{{< figure src="test-result.png" figcaption="MyFirstFlowTest result" >}}
Note the green tick on the left indicating that the test was successful. You can also see various log messages from the code logged to the console.

## MyFirstFlowTest

First the test class instantiates MemberX500Name(s) for two Actors. MemberX500Name is the primary way which identities are represented on a Corda Application Network. The MemberX500Name has a state method parse() which turns the string representation of a members identity into an MemberX500Name object. We will set up an Alice and Bob identity for the purpose of our test.
```Kotlinclass
MyFirstFlowTest {

    // Names picked to match the corda network in config/dev-net.json
    private val aliceX500 = MemberX500Name.parse("CN=Alice, OU=Test Dept, O=R3, L=London, C=GB")
    private val bobX500 = MemberX500Name.parse("CN=Bob, OU=Test Dept, O=R3, L=London, C=GB")
```
We declare the test method, in the standard way for JUnit test, with a `@Test` annotation.
```Kotlinclass
    @Test
    fun `test that MyFirstFLow returns correct message`() {
```      
Then we instantiate a Simulator Class. To find out more about Simulator, you can read the README.md from the source code: corda-runtime-os/README.md at release/os/5.0 · corda/corda-runtime-os
```Kotlinclass
       // Instantiate an instance of the Simulator
        val simulator = Simulator()
 ```
Next we convert the MemberX500Name for Alice and Bob into HoldingIdentities using the HoldingIdentity Static method. The HoldingIdentity in Corda holds the MemberX500Name and the GroupId which is the unique identifier for the Application network. However, the class used here is the simulated version provided by Simulator, ie net.corda.simulator.HoldingIdentity rather than net.corda.virtualnode.HoldingEntity
```Kotlinclass
        // Create Alice's and Bob HoldingIDs
        val aliceHoldingID = HoldingIdentity.Companion.create(aliceX500)
        val bobHoldingID = HoldingIdentity.Companion.create(bobX500)
```        
Next we use our simulator to create virtual nodes for Alice and Bob from their respective Holding Identities. The second argument allows you to specify which flows should be loaded up to each virtual node. In this case Alice will run the initiating Flow, with Bob running the Responder flow. (see the Writing a Flow section for an explanation of Initiating flows and Responder flows.
```Kotlinclass
        // Create Alice and Bob's virtual nodes, including the Class's of the flows which will be registered on each node.
        val aliceVN = simulator.createVirtualNode(aliceHoldingID, MyFirstFlow::class.java)
        val bobVN = simulator.createVirtualNode(bobHoldingID, MyFirstFlowResponder::class.java)
 ```
The next step is to create the arguments that are going to be passed to the flow. In the flow file MyFirstFlow.kt we create a class 'MyFirstFlowArguments' specifically for holding the flow start arguments:
(From MyFirstFlow.kt)
```Kotlinclass
// A class to hold the arguments required to start the flow
class MyFirstFlowStartArgs(val otherMember: MemberX500Name, val message: String)
```
We will use the same class here to specify that the message needs to go to Bob and the message should be ‘Hello Bob’:
```Kotlinclass
        // Create an instance of the MyFirstFlowStartArgs which contains the request arguments for starting the flow
        val myFirstFlowStartArgs = MyFirstFlowStartArgs(bobX500, "Hello Bob")
```
If we were running this flow on real Corda we would send the following requestBody over http-rpc:
```Kotlinclass
 {
    "clientRequestId": "r1",
    "flowClassName": "com.r3.developers.csdetemplate.MyFirstFlow",
    "requestData": {"otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB","message":"Hello Bob"}
}
```
When using Simulator in tests we can use the RequestData class which simulates the requestBody:
```Kotlinclass
        // Create a requestData object
        val requestData = RequestData.create(
            "request no 1",        // A unique reference for the instance of the flow request
            MyFirstFlow::class.java,        // The name of the flow class which is to be started
            myFirstFlowStartArgs            // The object which contains the start arguments of the flow
        )
```
To trigger the flow on Simulator, simply pass the requestData to the callflow() function on Alice’s virtual node. Simulator will simulate running the flow and responder flow, substituting simulated Services as required, returning a flow response String.
```Kotlinclass
        // Call the Flow on Alice's virtual node and capture the response from the flow
        val flowResponse = aliceVN.callFlow(requestData)
```
The last step is to test that the response received matches the response expected using an assert method:
```Kotlinclass
        // Check that the flow has returned the expected string
        assert(flowResponse == "Hello Alice, best wishes from Bob")
```        
If the assert evaluates to true, the test has passed.
