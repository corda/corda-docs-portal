---
date: '2022-09-20'
title: "MyFirstFlowTest Kotlin Walkthrough"
menu:
  corda-5-beta:
    parent: corda-5-beta-simulator
    identifier: corda-5-beta-flow-test-kotlin
    weight: 1000
section_menu: corda-5-beta
---

First the test class instantiates `MemberX500Name` for two actors. `MemberX500Name` is the primary way that identities are represented on a Corda [application Network](../../../introduction/key-concepts.html#application-network). `MemberX500Name` has a static method `parse()` that turns the string representation of a members identity into a `MemberX500Name` object.
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
   simulator.createVirtualNode(bobHoldingID, MyFirstFlowResponder::class.java)
   ```
    You can read more about initiating flows and responder flows in the section on [Your first flow ](../first-flow/code-kotlin.md#initiating-and-responding-flows).
6. Create the arguments to pass to the flow. In the flow file `MyFirstFlow.kt`, create a class `MyFirstFlowStartArgs` specifically for holding the flow start arguments:
   ```kotlin
   // A class to hold the arguments required to start the flow
   class MyFirstFlowStartArgs(val otherMember: MemberX500Name, val message: String)
   ```
   Use the same class to specify that the message should go to Bob:
   ```kotlin
   // Create an instance of the MyFirstFlowStartArgs which contains the request arguments for starting the flow
   val myFirstFlowStartArgs = MyFirstFlowStartArgs(bobX500)
   ```
   If running this flow on Corda itself, you would send the following `requestBody` over HTTP-RPC:
   ```http
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
   Simulator simulates running the flow and responder flow, substituting simulated services as required, and returning a flow response string.
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
