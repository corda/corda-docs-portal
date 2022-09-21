---
date: '2022-09-20'
title: "Your first flow"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-flow
    weight: 5000
section_menu: corda-5-dev-preview
---
<!-- Now that we have the Simulator test framework for triggering and testing flows, we can look at the anatomy of the `MyFirstFlow` and `MyFirstResponderFlow` flows.-->
The `MyFirstFlow` and `MyFirstResponderFlow` flows are basic flows that illustrate the main features of Corda 5 flows.
Many of the features will be familiar to those Developers who have written Corda 4 CorDapps. However, there are some important differences when using Corda 5:
* Services are injected on an as-needed basis.  
* Flows are started via HTTP RPC, rather than a Java client sending Java classes over AMQP.
* Initiating and responder flows are linked with a protocol rather than class names.
* Singletons should be avoided in flow code because there is no guarantee that the same flow worker will continue to execute a flow after it has been check-pointed and restarted.
<!--Although these changes seem a little strange at first, once you get used to them they will become second nature.-->
It is also worth noting that, as of Developer Preview 2, there is no ledger service available to the flows. This means that you can not create tokens, transactions, or states yet.

## MyFirstFlow use case
The use case in the example is very simple:
* The initiating flow is called on the initiating node with another member of the Application network being specified as the input argument.
* The initiating flow send the message “Hello from <initiator>.” to the specified recipient.
* The responder flow receives the message and replies with “Hello <initiator>, best wishes from <responder>
* The initiator returns the message received from the responder as a String

# Flow Code
The code for the flows and supporting classes can be found in the CSDE repo at `src/main/com/r3/developers/csdetemplate/MyFirstFlow.kt`.

The full listing with explanatory comments is as follows:
```kotlin
package com.r3.developers.csdetemplate

import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.application.messaging.FlowSession
import net.corda.v5.base.annotations.CordaSerializable
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.types.MemberX500Name
import net.corda.v5.base.util.contextLogger

// A class to hold the arguments required to start the flow
class MyFirstFlowStartArgs(val otherMember: MemberX500Name)


// A class which will contain a message, It must be marked with @CordaSerializable for Corda
// to be able to send from one virtual node to another.
@CordaSerializable
class Message(val sender: MemberX500Name, val message: String)


// MyFirstFlow is an initiating flow, it's corresponding responder flow is called MyFirstFlowResponder (defined below)
// to link the two sides of the flow together they need to have the same protocol.
@InitiatingFlow(protocol = "my-first-flow")
// MyFirstFlow should inherit from RPCStartableFlow, which tells Corda it can be started via an RPC call
class MyFirstFlow: RPCStartableFlow {

    // It is useful to be able to log messages from the flows for debugging.
    private companion object {
        val log = contextLogger()
    }

    // Corda has a set of injectable services which are injected into the flow at runtime.
    // Flows declare them with @CordaInjectable, then the flows have access to their services.

    // JsonMarshallingService provides a Service for manipulating json
    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    // FlowMessaging provides a service for establishing flow sessions between Virtual Nodes and
    // sending and receiving payloads between them
    @CordaInject
    lateinit var flowMessaging: FlowMessaging

    // MemberLookup provides a service for looking up information about members of the Virtual Network which
    // this CorDapp is operating in.
    @CordaInject
    lateinit var memberLookup: MemberLookup



    // When a flow is invoked it's call() method is called.
    // call() methods must be marked as @Suspendable, this allows Corda to pause mid-execution to wait
    // for a response from the other flows and services
    @Suspendable
    override fun call(requestBody: RPCRequestData): String {

        // Useful logging to follow what's happening in the console or logs
        log.info("MFF: MyFirstFlow.call() called")

        // Show the requestBody in the logs - this can be used to help establish the format for starting a flow on corda
        log.info("MFF: requestBody: ${requestBody.getRequestBody()}")

        // Deserialize the Json requestBody into the MyfirstFlowStartArgs class using the JsonSerialisation Service
        val flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs::class.java)

        // Obtain the MemberX500Name of counterparty
        val otherMember = flowArgs.otherMember

        // Get our identity from the MemberLookup service.
        val ourIdentity = memberLookup.myInfo().name

        // Create the message payload using the MessageClass we defined.
        val message = Message(otherMember, "Hello from $ourIdentity.")

        // Log the message to be sent.
        log.info("MFF: message.message: ${message.message}")

        // Start a flow session with the otherMember using the FlowMessaging service
        // The otherMember's Virtual Node will run the corresponding MyFirstFlowResponder responder flow
        val session = flowMessaging.initiateFlow(otherMember)

        // Send the Payload using the send method on the session to the MyFirstFlowResponder Responder flow
        session.send(message)

        // Receive a response from the Responder flow
        val response = session.receive(Message::class.java)

        // The return value of a RPCStartableFlow must always be a String, this string will be passed
        // back as the REST RPC response when the status of the flow is queried on Corda, or as the return
        // value from the flow when testing using the Simulator
        return response.message
    }
}

// MyFirstFlowResponder is a responder flow, it's corresponding initiating flow is called MyFirstFlow (defined above)
// to link the two sides of the flow together they need to have the same protocol.
@InitiatedBy(protocol = "my-first-flow")
// Responder flows must inherit from ResponderFlow
class MyFirstFlowResponder: ResponderFlow {

    // It is useful to be able to log messages from the flows for debugging.
    private companion object {
        val log = contextLogger()
    }

    // MemberLookup provides a service for looking up information about members of the Virtual Network which
    // this CorDapp is operating in.
    @CordaInject
    lateinit var memberLookup: MemberLookup


    // Responder flows are invoked when an initiating flow makes a call via a session set up with the Virtual
    // node hosting the Responder flow. When a responder flow is invoked it's call() method is called.
    // call() methods must be marked as @Suspendable, this allows Corda to pause mid-execution to wait
    // for a response from the other flows and services/
    // The Call method has the flow session passed in as a parameter by Corda so the session is available to
    // responder flow code, you don't need to inject the FlowMessaging service.
    @Suspendable
    override fun call(session: FlowSession) {

        // Useful logging to follow what's happening in the console or logs
        log.info("MFF: MyFirstResponderFlow.call() called")

        // Receive the payload and deserialize it into a Message class
        val receivedMessage = session.receive(Message::class.java)

        // Log the message as a proxy for performing some useful operation on it.
        log.info("MFF: Message received from ${receivedMessage.sender}: ${receivedMessage.message} ")

        // Get our identity from the MemberLookup service.
        val ourIdentity = memberLookup.myInfo().name

        // Create a response to greet the sender
        val response = Message(ourIdentity,
            "Hello ${session.counterparty.commonName}, best wishes from ${ourIdentity.commonName}")

        // Log the response to be sent.
        log.info("MFF: response.message: ${response.message}")

        // Send the response via the send method on the flow session
        session.send(response)
    }
}
/*
RequestBody for triggering the flow via http-rpc:
{
    "clientRequestId": "r1",
    "flowClassName": "com.r3.developers.csdetemplate.MyFirstFlow",
    "requestData": {"otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB","message":"Hello Bob"}
}
 */
 ```
## Helper classes
Before we get to the main flow classes there are two helper classes. The first is ‘MyFirstFlowStartArgs’, we used this in the ‘Testing Cordapps with the Simulator’ section. It provides a wrapper around the single arguments that need to be passed into the flow: the other member of the application network who the message should be sent to:
``kotlin
class MyFirstFlowStartArgs(val otherMember: MemberX500Name)
```
The second helper is the Message class. This is used for the message which is sent from the initiator to the responder and again for the message sent back from the responder to the initiator.  Note, as this is a Class defined in the CorDapp and it is going to be sent ‘down the wire’ between two Virtual nodes, it requires the @CordaSerializable annotation.
```kotlin
@CordaSerializable
class Message(val sender: MemberX500Name, val message: String)
```
## Initiating and Responding flows
To trigger a flow from http-rpc it needs to inherit from RPCStartableFlow. Most flows will come in pairs one initiating flow and a corresponding responder flow. The responder flow must inherit from ResponderFlow. The two flows are linked by adding the `@InitiatingFlow` and `@InitiatedBy` annotations which will both specify the same protocol in this case “my-first-flow:
```kotlin
@InitiatingFlow(protocol = "my-first-flow")
class MyFirstFlow: RPCStartableFlow { ... }
```
```kotlin
@InitiatedBy(protocol = "my-first-flow")
class MyFirstFlowResponder: ResponderFlow { ... }
```
## Logging
In both the Initiating and responder flows it is useful to add logging statements. To do this we add a logger to each class. when running tests locally the log entries will be displayed in the console. When running on Corda they will be displayed in the log files.
```kotlin
    private companion object {
        val log = contextLogger()
    }
```    
The log files for CSDE are located in the logs folder in the root of the project.
A new log file will be started each time a new instance of Corda is created, or if the log file gets too big.
Because the Corda combined worker runs all the corda processes in one JVM process there are a lot of log entries. It is helpful to add an easily searchable Tag to the from of each log message, for example:
```kotlin
        log.info("MFF: MyFirstFlow.call() called")
```
## The call() method
As with flows in Corda 4 each flow has a call() method. This is the method which Corda will invoke when the flow is invoked.

When a flow is started via http-rpc, the requestBody from the http request is passed into the call method as ‘requestBody’ parameter, thus giving the rest of the call method access to the parameters passed in via http.

When a responder flow is invoked as a result of an initiator flow on another node the Flow
Session with the initiating node is passed in as the parameter ‘session’.

The call() method in both flows must be marked as @Suspendable. This is an indicator to Corda that this method can be paused and persisted to the database whilst the flow waits for an asynchronous response. It will be rehydrated and continue to execute once the appropriate response is received. It is this mechanism that allows the CorDapp writer to write what appears to be synchronous, blocking code. which executes asynchronously and doesn’t block the Corda Cluster.

In the initiating flow:
```kotlin
    @Suspendable
    override fun call(requestBody: RPCRequestData): String { ... }
```    
In the responder flow:
```kotlin
    @Suspendable
    override fun call(session: FlowSession) { ... }        
```
## Injecting Service
Corda 5 requires the Cordapp writer to explicitly specify which Corda Services are required by the Flow. In this simple example we will use three services:
* JsonMarshallingService - A service CorDapps and other services may use to marshall arbitrary content in and out of JSON format using standard/approved* mappers.
* FlowMessaging  - A service CorDapps can use to create communication sessions between two virtual nodes. Once set up you can send/ receive using the session object.
* MemberLookup - A service Cordapps can use to lookup information about virtual nodes on the network.
There are other services such as the Persistence and Serialization services which are beyond the scope of this getting started example.
Services are declared as properties in the flow class with the @CordaInject annotation:
```kotlin
class MyFirstFlow: RPCStartableFlow {

    ...

    @CordaInject
    lateinit var jsonMarshallingService: JsonMarshallingService

    @CordaInject
    lateinit var flowMessaging: FlowMessaging

    @CordaInject
    lateinit var memberLookup: MemberLookup

    ...

    }
```    
They are then available in the call function, for example to initiate a FlowSession with the other party:
```kotlin
    val session = flowMessaging.initiateFlow(otherMember)
 ```
## Obtaining the http-rpc requestBody
The first thing that the MyFirstFlow.call() method does is to convert the requestBody parameters into a Kotlin Class. It does this using the getRequestBodyAs() method. This takes the jsonMarshallingService and the class that the requestBody Parameters should be parsed into. The flowArgs variable will have the type MyFirstFlowStartArgs (the helper class we declared above and used in the test.)
```kotlin
@Suspendable
    override fun call(requestBody: RPCRequestData): String {

        ...

        val flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs::class.java)

        ...

        }
```        
We can now obtain the MemberX500Name of the other virtual node that we want to send the message to from flowArgs which we will need later to set up the FlowSession:
```kotlin
        val otherMember = flowArgs.otherMember   
```         
## Creating the Message
To create the message we will need to know our own identity. Remember that this flow could run on any node, so the identity of the initiator cannot be hard coded. To find out the identity of the virtual node running the initiator flow we can use the injected  memberLookup service:
```kotlin
        val otherMember = flowArgs.otherMember
        val ourIdentity = memberLookup.myInfo().name
        val message = Message(otherMember, "Hello from $ourIdentity.")
        log.info("MFF: message.message: ${message.message}")
```
## Setting up the FlowSession
We can now start sending messages to the Responder. First we need to set up a FlowSession between the initiator and responder node:
```kotlin
        val session = flowMessaging.initiateFlow(otherMember)
```        
Then we simply call send() on the session and pass a payload:
```kotlin
        session.send(message)
```        
The code will continue to execute until it reaches the session.receive() method. At that point the flow will checkpoint and persist its state to the database. It will resume when it receives a message back from the responder. This frees up the Corda cluster flow workers to perform other tasks. Note, that there is no guarantee that the same flow worker will resume the completion of the flow, so singleton objects should be avoided in Corda 5 flows.
```kotlin
        val response = session.receive(Message::class.java)
 ```
When the send() is sent to the responder Corda will execute the MyFirstResponderFlow responder flow’s call() method down to the session.receive(), which will return the payload that was sent in the initiator's send() method.
```kotlin
    @Suspendable
    override fun call(session: FlowSession) {

        log.info("MFF: MyFirstResponderFlow.call() called")

        val receivedMessage = session.receive(Message::class.java)
```
The responder flow then obtains it’s own identity from it’s injected memberLookup Service, creates a response and sends the response back using session.send()
```kotlin
        val ourIdentity = memberLookup.myInfo().name

        val response = Message(ourIdentity,
            "Hello ${session.counterparty.commonName}, best wishes from ${ourIdentity.commonName}")

        log.info("MFF: response.message: ${response.message}")

        session.send(response)
```        
There is no return value for a ResponderFlow.

Back on the Initiating virtual node, Corda will detect that there is a send coming in from the responder and rehydrate the initiating flow from the database and resume it from where it was check-pointed.

The response is received and response.message is returned by the flow.
```kotlin
        val response = session.receive(Message::class.java)

        return response.message
```        
The response from the Initiating Flow is always a String so it can be returned when the flow status is queried by http-rpc.

## Other Considerations for FlowSessions
It is important that the sends and receives in the initiator and responder flows match up. If the initiator sends a Foo and the responder expects a Bar, the flow will hang and likely result in a timeout error.

As with Corda 4 there is a sendAndReceive method on FlowSession which will send a payload, check-point the flow then wait for a response to be received. (Not used in this example)
```kotlin
val response = sendAndReceive(<ReceiveType>::class.java, payload)
```
In Corda 4 when payloads were received they were wrapped in an UntrustworthyData class which required unwrapping:
```kotlin
// (Corda 4)
val Corda4Response = sendAndReceive(<ReceiveType>::class.java, payload).unwrap {<validationcode>}
```
This has been removed in Corda 5 because we found CorDapp writers used other methods to validate the data.         
