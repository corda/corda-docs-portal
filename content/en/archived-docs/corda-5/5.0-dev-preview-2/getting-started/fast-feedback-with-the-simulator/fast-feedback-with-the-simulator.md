---
date: '2022-09-20'
title: "Fast Feedback With Simulator"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-simulator
    weight: 4000
section_menu: corda-5-dev-preview2
---
When writing any application, including CorDapps, it is helpful to have a fast feedback loop: code > test > debug > modify.
This accelerates the development process.
Although it is possible to develop directly against a Corda cluster (as described in [Running your first CorDapp](../running-your-first-cordapp/run-first-cordapp.html)), to deploy a CorDapp onto a Corda cluster is time-consuming, and unit testing by manually hitting endpoints is clumsy.

To make the development process much easier, R3 have developed **Simulator**.
Simulator is a lightweight testing and demo tool that simulates a Corda 5 network, enabling you to run CorDapps, demonstrate realistic behaviour, and receive feedback on how the CorDapp is likely to behave with a real Corda network.
Importantly, it is not a "light" version of Corda. There is no Corda code running under the hood.
Think of it as a framework for executing flow code that injects simulated Corda services into the flows at the same point that Corda would inject the real services.
Simulator runs in-process so it is easy to set breakpoints in the code and use it for debugging.
{{< note >}}
As Simulator is not executing Corda code, the error messages are likely to be different from Corda. While the intention is to simulate all of the Corda API, there may be small differences.
{{< /note >}}

## Using Simulator

Simulator is designed to be used within a normal Java or Kotlin testing framework. In this documentation, we describe using JUnit. [MyFirstFlow](../first-flow/first-flow.html) has a corresponding test class `MyFirstFlowTest` that demonstrates how to use Simulator. This file is in `/src/test/kotlin/com.r3.developers.csdetemplate.MyFirstFlowTest.kt` in the [CSDE](../cordapp-standard-development-environment/csde.html) template repository.

The full listing with explanatory comments:
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
To run the test, click the green triangle next to the test method and select **Run 'MyFirstFlowTest…'**:
{{< figure src="run-test.png" width="50%" figcaption="Run MyFirstFlowTest" alt="Command to run MyFirstFlowTest in IntelliJ" >}}

Alternatively, if you have multiple tests in the class, you can click the double triangle next to the class declaration to run all of the tests in the class.

The output should look as follows:
{{< figure src="test-result.png" figcaption="MyFirstFlowTest result" >}}
Note the green tick on the left indicating that the test was successful. You can also see various log messages from the code logged to the console.

## MyFirstFlowTest

First the test class instantiates `MemberX500Name` for two actors. `MemberX500Name` is the primary way that identities are represented on a Corda [application Network](../../introduction/key-concepts.html#application-networks). `MemberX500Name` has a state method `parse()` that turns the string representation of a members identity into a `MemberX500Name` object.
1. Set up Alice and Bob identities:
   ```kotlin
   MyFirstFlowTest {

       // Names picked to match the corda network in config/dev-net.json
       private val aliceX500 = MemberX500Name.parse("CN=Alice, OU=Test Dept, O=R3, L=London, C=GB")
       private val bobX500 = MemberX500Name.parse("CN=Bob, OU=Test Dept, O=R3, L=London, C=GB")
   ```
2. Declare the test method in the standard way for JUnit test, with a `@Test` annotation:
   ```kotlin
       @Test
       fun `test that MyFirstFLow returns correct message`() {
   ```      
3. Instantiate a `Simulator` class:
   ```kotlin
          // Instantiate an instance of the Simulator
           val simulator = Simulator()
    ```
   To find out more about this class, read the [README.md from the source code](https://github.com/corda/corda-runtime-os/blob/release/os/5.0/simulator/README.md).

4. Convert the `MemberX500Name` for Alice and Bob into `HoldingIdentities` using the `HoldingIdentity` static method. The `HoldingIdentity` in Corda holds the `MemberX500Name` and the `GroupId` which is the unique identifier for the application network. However, the class used here is the simulated version provided by Simulator; that is `net.corda.simulator.HoldingIdentity` rather than `net.corda.virtualnode.HoldingEntity`.
   ```kotlin
           // Create Alice's and Bob HoldingIDs
           val aliceHoldingID = HoldingIdentity.Companion.create(aliceX500)
           val bobHoldingID = HoldingIdentity.Companion.create(bobX500)
   ```        
5. Use Simulator to create virtual nodes for Alice and Bob from their respective holding identities. The second argument allows you to specify which flows should be loaded up to each virtual node. In this case, Alice runs the initiating flow, with Bob running the responder flow.
   ```kotlin
           // Create Alice and Bob's virtual nodes, including the classes of the flows which will be registered on each node.
           val aliceVN = simulator.createVirtualNode(aliceHoldingID, MyFirstFlow::class.java)
           val bobVN = simulator.createVirtualNode(bobHoldingID, MyFirstFlowResponder::class.java)
    ```
    You can read more about initiating flows and responder flows in the section on *[Your first flow ](../first-flow/first-flow.html#initiating-and-responding-flows)*.
6. Create the arguments to pass to the flow. In the flow file `MyFirstFlow.kt`, create a class `MyFirstFlowArguments` specifically for holding the flow start arguments:
   ```kotlin
   // A class to hold the arguments required to start the flow
   class MyFirstFlowStartArgs(val otherMember: MemberX500Name, val message: String)
   ```
   Use the same class to specify that the message needs to go to Bob and the message should be "Hello Bob":
   ```kotlin
           // Create an instance of the MyFirstFlowStartArgs which contains the request arguments for starting the flow
           val myFirstFlowStartArgs = MyFirstFlowStartArgs(bobX500, "Hello Bob")
   ```
   If running this flow on Corda itself, you would send the following `requestBody` over HTTP-RPC:
   ```kotlin
    {
       "clientRequestId": "r1",
       "flowClassName": "com.r3.developers.csdetemplate.MyFirstFlow",
       "requestData": {"otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB","message":"Hello Bob"}
   }
   ```
   When using Simulator in tests, use the `RequestData` class, which simulates the `requestBody`:
   ```kotlin
           // Create a requestData object
           val requestData = RequestData.create(
               "request no 1",        // A unique reference for the instance of the flow request
               MyFirstFlow::class.java,        // The name of the flow class which is to be started
               myFirstFlowStartArgs            // The object which contains the start arguments of the flow
           )
   ```
7. Pass the `requestData` to the `callflow()` function on Alice’s virtual node, to trigger the flow on Simulator.
   Simulator simulates running the flow and responder flow, substituting simulated services as required, and returning a flow response String.
   ```kotlin
           // Call the Flow on Alice's virtual node and capture the response from the flow
           val flowResponse = aliceVN.callFlow(requestData)
   ```
8. Test that the response received matches the response expected using an assert method:
   ```kotlin
           // Check that the flow has returned the expected string
           assert(flowResponse == "Hello Alice, best wishes from Bob")
   ```        
   If the assert evaluates to true, the test has passed.
