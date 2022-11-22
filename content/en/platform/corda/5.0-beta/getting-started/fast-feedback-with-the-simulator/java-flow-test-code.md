---
date: '2022-09-20'
title: "Java Flow Test Code"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-simulator
    identifier: corda-5-dev-preview-flow-test-java
    weight: 2000
section_menu: corda-5-dev-preview2
---

First the test class instantiates `MemberX500Name` for two actors. `MemberX500Name` is the primary way that identities are represented on a Corda [application network](../../introduction/key-concepts.html#application-network). `MemberX500Name` has a static method `parse()` that turns the string representation of a members identity into a `MemberX500Name` object.
1. Set up Alice and Bob identities:
   ```java
   class MyFirstFlowTest {

       // Names picked to match the corda network in config/dev-net.json
       private MemberX500Name aliceX500 = MemberX500Name.parse("CN=Alice, OU=Test Dept, O=R3, L=London, C=GB");
       private MemberX500Name bobX500 = MemberX500Name.parse("CN=Bob, OU=Test Dept, O=R3, L=London, C=GB");
   ...
   }
   ```
2. Declare the test method in the standard way for JUnit test, with a `@Test` annotation:
   ```java
   @Test
   @SuppressWarnings("unchecked")
   public void test_that_MyFirstFLow_returns_correct_message() {
     ...
   }
   ```      
3. Instantiate a `Simulator` class:
   ```java
   // Instantiate an instance of the Simulator
   Simulator simulator = new Simulator();
    ```
   To find out more about this class, read the [README.md from the source code](https://github.com/corda/corda-runtime-os/blob/release/os/5.0/simulator/README.md).

4. Convert the `MemberX500Name` for Alice and Bob into `HoldingIdentities` using the `HoldingIdentity` static method. The `HoldingIdentity` in Corda holds the `MemberX500Name` and the `GroupId` which is the unique identifier for the application network. However, the class used here is the simulated version provided by Simulator; that is `net.corda.simulator.HoldingIdentity` rather than `net.corda.virtualnode.HoldingEntity`.
   ```java
   // Create Alice's and Bob HoldingIDs
   HoldingIdentity aliceHoldingID = HoldingIdentity.Companion.create(aliceX500);
   HoldingIdentity bobHoldingID = HoldingIdentity.Companion.create(bobX500)
   ```        
5. Use Simulator to create virtual nodes for Alice and Bob from their respective holding identities. The second argument allows you to specify which flows should be loaded up to each virtual node. In this case, Alice runs the initiating flow, with Bob running the responder flow.
   ```java
   // Create Alice and Bob's virtual nodes, including the Class's of the flows which will be registered on each node.
   // We don't assign Bob's virtual node to a variable because we don't need it for this particular test.
   SimulatedVirtualNode aliceVN = simulator.createVirtualNode(aliceHoldingID, MyFirstFlow.class);
   simulator.createVirtualNode(bobHoldingID, MyFirstFlowResponder.class);
   ```
   You can read more about initiating flows and responder flows in the section on [Your first flow ](../first-flow.html#initiating-and-responding-flows).
6. Create the arguments to pass to the flow. In the flow file `MyFirstFlowStartArgs.java`, create a class `MyFirstFlowStartArgs` specifically for holding the flow start arguments:
   ```java
   // A class to hold the arguments required to start the flow
   public class MyFirstFlowStartArgs {
     ...
   }
   ```
   Use the same class to specify that the message should go to Bob:
   ```java
   // Create an instance of the MyFirstFlowStartArgs which contains the request arguments for starting the flow
   MyFirstFlowStartArgs myFirstFlowStartArgs = new MyFirstFlowStartArgs(bobX500);
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
   ```java
   // Create a requestData object
   RequestData requestData = RequestData.Companion.create(
           "request no 1",        // A unique reference for the instance of the flow request
           MyFirstFlow.class,              // The name of the flow class which is to be started
           myFirstFlowStartArgs            // The object which contains the start arguments of the flow
   );
   ```
7. Pass the `requestData` to the `callflow()` function on Alice’s virtual node, to trigger the flow on Simulator.
   Simulator simulates running the flow and responder flow, substituting simulated services as required, and returning a flow response string.
   ```java
   // Call the Flow on Alice's virtual node and capture the response from the flow
   String flowResponse = aliceVN.callFlow(requestData);
   ```
8. Test that the response received matches the response expected using an assert method:
   ```java
   // Check that the flow has returned the expected string
   assert(flowResponse.equals("Hello Alice, best wishes from Bob"));
   ```        
   If the assert evaluates to true, the test has passed.
