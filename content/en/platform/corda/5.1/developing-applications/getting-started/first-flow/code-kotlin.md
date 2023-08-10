---
date: '2023-08-10'
version: 'Corda 5.1'
title: "Kotlin Flow Code Walkthrough"
menu:
  corda51:
    parent: corda51-flow
    identifier: corda51-flow-kotlin
    weight: 1000
section_menu: corda51
---
# Kotlin Flow Code Walkthrough
The Kotlin code for the {{< tooltip >}}flows{{< /tooltip >}} and supporting classes can be found in the CSDE repo at `workflows/src/main/kotlin/com/r3/developers/csdetemplate/flowexample/workflows/MyFirstFlow.kt`.

The full listing with explanatory comments is as follows:
```kotlin
package com.r3.developers.csdetemplate.flowexample.workflows

import net.corda.v5.application.flows.*
import net.corda.v5.application.marshalling.JsonMarshallingService
import net.corda.v5.application.membership.MemberLookup
import net.corda.v5.application.messaging.FlowMessaging
import net.corda.v5.application.messaging.FlowSession
import net.corda.v5.base.annotations.CordaSerializable
import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.types.MemberX500Name
import org.slf4j.LoggerFactory

// A class to hold the deserialized arguments required to start the flow
class MyFirstFlowStartArgs(val otherMember: MemberX500Name)


// A class which will contain a message, It must be marked with @CordaSerializable for Corda
// to be able to send from one virtual node to another.
@CordaSerializable
class Message(val sender: MemberX500Name, val message: String)


// MyFirstFlow is an initiating flow, it's corresponding responder flow is called MyFirstFlowResponder (defined below)
// to link the two sides of the flow together they need to have the same protocol.
@InitiatingFlow(protocol = "my-first-flow")
// MyFirstFlow should inherit from ClientStartableFlow, which tells Corda it can be started via an REST call from a client
class MyFirstFlow: ClientStartableFlow {

  // It is useful to be able to log messages from the flows for debugging.
  private companion object {
    val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
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
  override fun call(requestBody: ClientRequestBody): String {

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

    // The return value of a ClientStartableFlow must always be a String, this string will be passed
    // back as the REST response when the status of the flow is queried on Corda.
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
    val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
  }

  // MemberLookup provides a service for looking up information about members of the Virtual Network which
  // this CorDapp is operating in.
  @CordaInject
  lateinit var memberLookup: MemberLookup


  // Responder flows are invoked when an initiating flow makes a call via a session set up with the Virtual
  // node hosting the Responder flow. When a responder flow is invoked, its call() method is called.
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
RequestBody for triggering the flow via REST:
{
    "clientRequestId": "r1",
    "flowClassName": "com.r3.developers.csdetemplate.flowexample.workflows.MyFirstFlow",
    "requestBody": {
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB"
        }
}
 */
 ```
## Helper Classes
There are two helper classes:
* `MyFirstFlowStartArgs` — provides a wrapper around the single arguments that need to be passed into the flow — the other member of the {{< tooltip >}}application network{{< /tooltip >}} who the message should be sent to:
   ```kotlin
   class MyFirstFlowStartArgs(val otherMember: MemberX500Name)
   ```
* `Message` —  specifies the sender and the message. This is used for both the message sent from the initiator to the responder and subsequently the message sent back from the responder to the initiator. Note, as this is a class defined in a {{< tooltip >}}CorDapp{{< /tooltip >}} and it is going to be sent ‘down the wire’ between two virtual nodes, it requires the `@CordaSerializable` annotation.
   ```kotlin
   @CordaSerializable
   class Message(val sender: MemberX500Name, val message: String)
   ```
## Initiating and Responding Flows
To trigger a flow from REST, the flow must  inherit from `ClientStartableFlow`. Most flows will come in pairs; one initiating flow and a corresponding responder flow. The responder flow must inherit from `ResponderFlow`. The two flows are linked by adding the `@InitiatingFlow` and `@InitiatedBy` annotations which both specify the same protocol in this case "my-first-flow":
```kotlin
@InitiatingFlow(protocol = "my-first-flow")
class MyFirstFlow: ClientStartableFlow { ... }
```
```kotlin
@InitiatedBy(protocol = "my-first-flow")
class MyFirstFlowResponder: ResponderFlow { ... }
```
## Logging
It is useful to add logging statements to both the initiating and responder flows.
To do this, add a logger to each class.
When running tests locally, the console displays log entries.
When running on Corda, the log files are updated.
```kotlin
    private companion object {
        val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
    }
```
The log files for CSDE are located in the logs folder in the root of the project.
The CSDE starts a new log file each time a new instance of Corda is created or when the log file grows too large. The logging can be configured by editing the `config/log4j2.xml` file.
Because the Corda combined worker runs all of the Corda processes in one JVM process, there are a lot of log entries.
We recommend adding an easily searchable tag to each log message. For example:
```kotlin
        log.info("MFF: MyFirstFlow.call() called")
```
## call() Method
Each flow has a `call()` method. This is the method which Corda invokes when the flow is invoked.

When a flow is started via REST, the `requestBody` from the HTTP request is passed into the `call` method as the  `requestBody` parameter, giving the rest of the call method access to the parameters passed in via HTTP.

When a responder flow is invoked as a result of an initiator flow on another node, the flow session with the initiating node is passed in as the parameter `session`.

The `call()` method in both flows must be marked as `@Suspendable`. This is an indicator to Corda that this method can be paused and persisted to the database whilst the flow waits for an asynchronous response. It will be rehydrated and continue to execute once the appropriate response is received. It is this mechanism that allows a CorDapp Developer to write what appears to be synchronous, blocking code that executes asynchronously and does not block the Corda Cluster.

In the initiating flow:
```kotlin
    @Suspendable
    override fun call(requestBody: ClientRequestBody): String { ... }
```
In the responder flow:
```kotlin
    @Suspendable
    override fun call(session: FlowSession) { ... }
```
## Injecting Services
Corda 5 requires a CorDapp Developer to explicitly specify which Corda services are required by the flow. In this simple example we use three services:
* `JsonMarshallingService` — a service that CorDapps and other services may use to marshal arbitrary content in and out of JSON format using standard approved mappers.
* `FlowMessaging`  — a service that CorDapps can use to create communication sessions between two virtual nodes. Once set up, you can send and receive using the session object.
* `MemberLookup`  — a service that CorDapps can use to retrieve information about virtual nodes on the network.

There are other services, such as the `Persistence` and `Serialization` services, which are beyond the scope of this Getting Started example.

Services are declared as properties in the flow class with the `@CordaInject` annotation:
```kotlin
class MyFirstFlow: ClientStartableFlow {

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
The services are then available in the call function. For example to initiate a `FlowSession` with the other party:
```kotlin
    val session = flowMessaging.initiateFlow(otherMember)
 ```
## Obtaining the REST requestBody
The first thing that the `MyFirstFlow.call()` method does is convert the `requestBody` parameters into a Kotlin class.
It does this using the `getRequestBodyAs()` method. This takes the `jsonMarshallingService` and the class that the `requestBody` parameters should be parsed into. The `flowArgs` variable has the type `MyFirstFlowStartArgs`, the helper class we declared in [the Helper classes section](#helper-classes).
```kotlin
@Suspendable
    override fun call(requestBody: ClientRequestBody): String {

        ...

        val flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs::class.java)

        ...

        }
```
We can now obtain the X500 name of the other virtual node that we want to send the message to from `flowArgs`, which we will need later to set up the `FlowSession`:
```kotlin
        val otherMember = flowArgs.otherMember
```
## Creating the Message
To create the message, you must know the identity of the initiator. Remember that this flow could run on any node, so the identity cannot be hard coded. To find out the identity of the virtual node running the initiator flow, use the injected  `memberLookup` service:
```kotlin
        val otherMember = flowArgs.otherMember
        val ourIdentity = memberLookup.myInfo().name
        val message = Message(otherMember, "Hello from $ourIdentity.")
        log.info("MFF: message.message: ${message.message}")
```
## Setting up the FlowSession
We can now start sending messages to the responder:
1. Set up a `FlowSession` between the initiator and responder node:
   ```kotlin
        val session = flowMessaging.initiateFlow(otherMember)
   ```
2. Simply call `send()` on the session and pass a payload:
   ```kotlin
        session.send(message)
   ```
   The code continues to execute until it reaches the `session.receive()` method. At that point, the flow checkpoints and persists its {{< tooltip >}}state{{< /tooltip >}} to the database. It resumes when it receives a message back from the responder. This frees up the Corda cluster {{< tooltip >}}flow workers{{< /tooltip >}} to perform other tasks.
   {{< note >}}
   There is no guarantee that the same flow worker resumes the completion of the flow and so singleton objects should be avoided in Corda 5 flows.
   {{< /note >}}
   ```kotlin
           val response = session.receive(Message::class.java)
    ```
   When the message is sent to the responder via the `send()` method, Corda executes `session.receive()` in the `MyFirstResponderFlow` responder flow's `call()` method. This `session.receive()` method retrieves the message that was sent in the initiator's `send()` method.
   ```kotlin
       @Suspendable
       override fun call(session: FlowSession) {

           log.info("MFF: MyFirstResponderFlow.call() called")

           val receivedMessage = session.receive(Message::class.java)
   ```
   The responder flow then obtains its own identity from its injected `memberLookup` service, creates a response, and sends the response back using `session.send()`:
   ```kotlin
        val ourIdentity = memberLookup.myInfo().name

        val response = Message(ourIdentity,
            "Hello ${session.counterparty.commonName}, best wishes from ${ourIdentity.commonName}")

        log.info("MFF: response.message: ${response.message}")

        session.send(response)
   ```
   There is no return value for a ResponderFlow.

   Back on the Initiating virtual node, Corda detects the send coming from the responder and rehydrates the initiating flow from the database and resumes it from where it was checkpointed.

   The response is received and `response.message` is returned by the flow.
   ```kotlin
        val response = session.receive(Message::class.java)

        return response.message
   ```
   The response from the initiating flow is always a string, which can be returned when the flow status is queried by REST.

## Other Considerations for FlowSessions
It is important that the sends and receives in the initiator and responder flows match. If the initiator sends a Foo and the responder expects a Bar, the flow hangs and likely results in a timeout error.

The `sendAndReceive` method on `FlowSession` sends a payload, check-points the flow, and then waits for a response to be received:
```kotlin
val response = myFlowSession.sendAndReceive(<ReceiveType>::class.java, payload)
```
In Corda 4, when payloads were received they were wrapped in an `UntrustworthyData` class which required unwrapping:
```kotlin
// (Corda 4)
val Corda4Response = myFlowSession.sendAndReceive(<ReceiveType>::class.java, payload).unwrap {<validationcode>}
```
This has been removed in Corda 5 because CorDapp Developers usually use other methods to validate the data.
