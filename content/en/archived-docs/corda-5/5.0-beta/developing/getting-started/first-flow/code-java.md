---
date: '2022-10-19'
title: "Java Flow Code Walkthrough"
menu:
  corda-5-beta:
    parent: corda-5-beta-flow
    identifier: corda-5-beta-flow-java
    weight: 2000
section_menu: corda-5-beta
---

The Java code for the flows and supporting classes can be found in the CSDE repo in the `src/main/java/com/r3/developers/csdetemplate/flowexample/workflows` folder.

## Java Flow Files

The `src/main/java/com/r3/developers/csdetemplate/flowexample/workflows` folder contains the following files:
* [Message.java](#messagejava)
* [MyFirstFlow.java](#myfirstflowjava)
* [MyFirstFlowResponder.java](#myfirstflowresponderjava)
* [MyFirstFlowStartArgs.java](#myfirstflowstartargsjava)

### Message.java

```java
package com.r3.developers.csdetemplate.flowexample.workflows;

import net.corda.v5.base.annotations.CordaSerializable;
import net.corda.v5.base.types.MemberX500Name;

// A class which will contain a message, It must be marked with @CordaSerializable for Corda
// to be able to send from one virtual node to another.
@CordaSerializable
public class Message {
    public Message(MemberX500Name sender, String message) {
        this.sender = sender;
        this.message = message;
    }

    public MemberX500Name getSender() {
        return sender;
    }

    public String getMessage() {
        return message;
    }

    public MemberX500Name sender;
    public String message;
}
```

### MyFirstFlow.java

```java
package com.r3.developers.csdetemplate.flowexample.workflows;

import net.corda.v5.application.flows.*;
import net.corda.v5.application.marshalling.JsonMarshallingService;
import net.corda.v5.application.membership.MemberLookup;
import net.corda.v5.application.messaging.FlowMessaging;
import net.corda.v5.application.messaging.FlowSession;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.base.types.MemberX500Name;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


// MyFirstFlow is an initiating flow, it's corresponding responder flow is called MyFirstFlowResponder (defined below)
// to link the two sides of the flow together they need to have the same protocol.
@InitiatingFlow(protocol = "my-first-flow")
// MyFirstFlow should inherit from ClientStartableFlow, which tells Corda it can be started via an REST call
public class MyFirstFlow implements ClientStartableFlow {

  // Log messages from the flows for debugging.
  private final static Logger log = LoggerFactory.getLogger(MyFirstFlow.class);

  // Corda has a set of injectable services which are injected into the flow at runtime.
  // Flows declare them with @CordaInjectable, then the flows have access to their services.

  // JsonMarshallingService provides a service for manipulating JSON.
  @CordaInject
  public JsonMarshallingService jsonMarshallingService;

  // FlowMessaging provides a service that establishes flow sessions between virtual nodes
  // that send and receive payloads between them.
  @CordaInject
  public FlowMessaging flowMessaging;

  // MemberLookup provides a service for looking up information about members of the virtual network which
  // this CorDapp operates in.
  @CordaInject
  public MemberLookup memberLookup;

  public MyFirstFlow() {}

  // When a flow is invoked its call() method is called.
  // Call() methods must be marked as @Suspendable, this allows Corda to pause mid-execution to wait
  // for a response from the other flows and services.

  @Suspendable
  @Override
  public String call(ClientRequestBody requestBody) {

    // Follow what happens in the console or logs.
    log.info("MFF: MyFirstFlow.call() called");

    // Show the requestBody in the logs - this can be used to help establish the format for starting a flow on Corda.
    log.info("MFF: requestBody: " + requestBody.getRequestBody());

    // Deserialize the Json requestBody into the MyfirstFlowStartArgs class using the JsonSerialisation service.
    MyFirstFlowStartArgs flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs.class);

    // Obtain the MemberX500Name of the counterparty.
    MemberX500Name otherMember = flowArgs.getOtherMember();

    // Get our identity from the MemberLookup service.
    MemberX500Name ourIdentity = memberLookup.myInfo().getName();

    // Create the message payload using the MessageClass we defined.
    Message message = new Message(otherMember, "Hello from " + ourIdentity + ".");

    // Log the message to be sent.
    log.info("MFF: message.message: " + message.getMessage());

    // Start a flow session with the otherMember using the FlowMessaging service.
    // The otherMember's virtual node will run the corresponding MyFirstFlowResponder responder flow.
    FlowSession session = flowMessaging.initiateFlow(otherMember);

    // Send the Payload using the send method on the session to the MyFirstFlowResponder responder flow.
    session.send(message);

    // Receive a response from the responder flow.
    Message response = session.receive(Message.class);

    // The return value of a ClientStartableFlow must always be a String. This will be passed
    // back as the REST response when the status of the flow is queried on Corda, or as the return
    // value from the flow when testing using the simulator.
    return response.getMessage();
  }
}

/*
RequestBody for triggering the flow via REST:
{
    "clientRequestId": "r1",
    "flowClassName": "com.r3.developers.csdetemplate.flowexample.workflows.MyFirstFlow",
    "requestData": {
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB"
        }
}
 */

```

### MyFirstFlowResponder.java

```java
package com.r3.developers.csdetemplate.flowexample.workflows;

import net.corda.v5.application.flows.*;
import net.corda.v5.application.marshalling.JsonMarshallingService;
import net.corda.v5.application.membership.MemberLookup;
import net.corda.v5.application.messaging.FlowMessaging;
import net.corda.v5.application.messaging.FlowSession;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.base.types.MemberX500Name;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


// MyFirstFlow is an initiating flow, it's corresponding responder flow is called MyFirstFlowResponder (defined below)
// to link the two sides of the flow together they need to have the same protocol.
@InitiatingFlow(protocol = "my-first-flow")
// MyFirstFlow should inherit from ClientStartableFlow, which tells Corda it can be started via an REST call
public class MyFirstFlow implements ClientStartableFlow {

  // Log messages from the flows for debugging.
  private final static Logger log = LoggerFactory.getLogger(MyFirstFlow.class);

  // Corda has a set of injectable services which are injected into the flow at runtime.
  // Flows declare them with @CordaInjectable, then the flows have access to their services.

  // JsonMarshallingService provides a service for manipulating JSON.
  @CordaInject
  public JsonMarshallingService jsonMarshallingService;

  // FlowMessaging provides a service that establishes flow sessions between virtual nodes
  // that send and receive payloads between them.
  @CordaInject
  public FlowMessaging flowMessaging;

  // MemberLookup provides a service for looking up information about members of the virtual network which
  // this CorDapp operates in.
  @CordaInject
  public MemberLookup memberLookup;

  public MyFirstFlow() {}

  // When a flow is invoked its call() method is called.
  // Call() methods must be marked as @Suspendable, this allows Corda to pause mid-execution to wait
  // for a response from the other flows and services.

  @Suspendable
  @Override
  public String call(ClientRequestBody requestBody) {

    // Follow what happens in the console or logs.
    log.info("MFF: MyFirstFlow.call() called");

    // Show the requestBody in the logs - this can be used to help establish the format for starting a flow on Corda.
    log.info("MFF: requestBody: " + requestBody.getRequestBody());

    // Deserialize the Json requestBody into the MyfirstFlowStartArgs class using the JsonSerialisation service.
    MyFirstFlowStartArgs flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs.class);

    // Obtain the MemberX500Name of the counterparty.
    MemberX500Name otherMember = flowArgs.getOtherMember();

    // Get our identity from the MemberLookup service.
    MemberX500Name ourIdentity = memberLookup.myInfo().getName();

    // Create the message payload using the MessageClass we defined.
    Message message = new Message(otherMember, "Hello from " + ourIdentity + ".");

    // Log the message to be sent.
    log.info("MFF: message.message: " + message.getMessage());

    // Start a flow session with the otherMember using the FlowMessaging service.
    // The otherMember's virtual node will run the corresponding MyFirstFlowResponder responder flow.
    FlowSession session = flowMessaging.initiateFlow(otherMember);

    // Send the Payload using the send method on the session to the MyFirstFlowResponder responder flow.
    session.send(message);

    // Receive a response from the responder flow.
    Message response = session.receive(Message.class);

    // The return value of a ClientStartableFlow must always be a String. This will be passed
    // back as the REST response when the status of the flow is queried on Corda.
    return response.getMessage();
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

### MyFirstFlowStartArgs.java

```java
package com.r3.developers.csdetemplate.flowexample.workflows;

import net.corda.v5.base.types.MemberX500Name;

// A class to hold the arguments required to start the flow
public class MyFirstFlowStartArgs {
    public MemberX500Name otherMember;

    public MyFirstFlowStartArgs(MemberX500Name otherMember) {
        this.otherMember = otherMember;
    }

    // The JSON Marshalling Service, which handles serialisation, needs this constructor.
    public MyFirstFlowStartArgs() {}
}
```

## Helper Classes
There are two helper classes:
* `MyFirstFlowStartArgs` — provides a wrapper around the single arguments that need to be passed into the flow — the other member of the application network who the message should be sent to:
   ```java
   public class MyFirstFlowStartArgs {
    public MemberX500Name otherMember;

    public MyFirstFlowStartArgs(MemberX500Name otherMember) {
        this.otherMember = otherMember;
    }

    // The JSON Marshalling Service, which handles serialisation, needs this constructor.
    public MyFirstFlowStartArgs() {}
   }
   ```

* `Message` —  specifies the sender and the message. This is used for both the message sent from the initiator to the responder and subsequently the message sent back from the responder to the initiator. Note, as this is a class defined in a CorDapp and it is going to be sent ‘down the wire’ between two virtual nodes, it requires the `@CordaSerializable` annotation.
   ```java
   @CordaSerializable
   public class Message {
       public Message(MemberX500Name sender, String message) {
           this.sender = sender;
           this.message = message;
       }

       public MemberX500Name getSender() {
           return sender;
       }

       public String getMessage() {
           return message;
       }

       public MemberX500Name sender;
       public String message;
   }
   ```
## Initiating and Responding Flows
To trigger a flow from REST, the flow must  inherit from `ClientStartableFlow`. Most flows will come in pairs; one initiating flow and a corresponding responder flow. The responder flow must inherit from `ResponderFlow`. The two flows are linked by adding the `@InitiatingFlow` and `@InitiatedBy` annotations which both specify the same protocol in this case "my-first-flow":
```java
@InitiatingFlow(protocol = "my-first-flow")
public class MyFirstFlow implements ClientStartableFlow  { ... }
```
```java
@InitiatedBy(protocol = "my-first-flow")
public class MyFirstFlowResponder implements ResponderFlow  { ... }
```

## Logging

It is useful to add logging statements to both the initiating and responder flows.
To do this, add a logger to each class.
When running tests locally, the console displays log entries.
When running on Corda, the log files are updated.
```java
    private final static Logger log = LoggerFactory.getLogger(MyFirstFlowResponder.class);
```
The log files for CSDE are located in the logs folder in the root of the project.
The CSDE starts a new log file each time a new instance of Corda is created or when the log file grows too large. The logging can be configured by editing `config/static-network-config.json` file.
Because the Corda combined worker runs all of the Corda processes in one JVM process, there are a lot of log entries.
We recommend adding an easily searchable tag to each log message. For example:
```java
        log.info("MFF: MyFirstFlow.call() called");
```
## call() Method
As with flows in Corda 4, each flow has a `call()` method. This is the method which Corda invokes when the flow is invoked.

When a flow is started via REST, the `requestBody` from the HTTP request is passed into the `call` method as the  `requestBody` parameter, giving the rest of the call method access to the parameters passed in via HTTP.

When a responder flow is invoked as a result of an initiator flow on another node, the flow session with the initiating node is passed in as the parameter `session`.

The `call()` method in both flows must be marked as `@Suspendable`. This is an indicator to Corda that this method can be paused and persisted to the database whilst the flow waits for an asynchronous response. It will be rehydrated and continue to execute once the appropriate response is received. It is this mechanism that allows a CorDapp Developer to write what appears to be synchronous, blocking code that executes asynchronously and does not block the Corda Cluster.

In the initiating flow:
```java
   @Suspendable
   @Override
   public String call(ClientRequestBody requestBody)  { ... }
```
In the responder flow:
```java
   @Suspendable
   @Override
   public void call(FlowSession session) { ... }
```
## Injecting Services
Corda 5 requires a CorDapp Developer to explicitly specify which Corda services are required by the flow. In this simple example we use three services:
* `JsonMarshallingService` — a service that CorDapps and other services may use to marshal arbitrary content in and out of JSON format using standard approved mappers.
* `FlowMessaging`  — a service that CorDapps can use to create communication sessions between two virtual nodes. Once set up, you can send and receive using the session object.
* `MemberLookup`  — a service that CorDapps can use to retrieve information about virtual nodes on the network.

There are other services, such as the `Persistence` and `Serialization` services, which are beyond the scope of this Getting Started example.

Services are declared as properties in the flow class with the `@CordaInject` annotation:
```java
public class MyFirstFlow implements ClientStartableFlow {

    ...

    @CordaInject
    public JsonMarshallingService jsonMarshallingService;

    @CordaInject
    public FlowMessaging flowMessaging;

    @CordaInject
    public MemberLookup memberLookup;

    ...

    }
```
The services are then available in the call function. For example to initiate a `FlowSession` with the other party:
```java
    FlowSession session = flowMessaging.initiateFlow(otherMember);
 ```

## Obtaining the REST requestBody

The first thing that the `MyFirstFlow.call()` method does is convert the `requestBody` parameters into a Kotlin class.
It does this using the `getRequestBodyAs()` method. This takes the `jsonMarshallingService` and the class that the `requestBody` parameters should be parsed into. The `flowArgs` variable has the type `MyFirstFlowStartArgs`, the helper class we declared in [the Helper classes section](#helper-classes) and used in the test.
```java
   @Suspendable
    @Override
    public String call(ClientRequestBody requestBody) {

        ...

        MyFirstFlowStartArgs flowArgs = requestBody.getRequestBodyAs(jsonMarshallingService, MyFirstFlowStartArgs.class);

        ...

        }
```
We can now obtain the X500 name of the other virtual node that we want to send the message to from `flowArgs`, which we will need later to set up the `FlowSession`:
```java
        MemberX500Name otherMember = flowArgs.otherMember;
```
## Creating the Message
To create the message, you must know the identity of the initiator. Remember that this flow could run on any node, so the identity cannot be hard coded. To find out the identity of the virtual node running the initiator flow, use the injected  `memberLookup` service:
```java
MemberX500Name otherMember = flowArgs.otherMember;
MemberX500Name ourIdentity = memberLookup.myInfo().getName();
Message message = new Message(otherMember, "Hello from " + ourIdentity + ".");
log.info("MFF: message.message: " + message.message);
```
## Setting up the FlowSession
We can now start sending messages to the responder:
1. Set up a `FlowSession` between the initiator and responder node:
   ```java
        FlowSession session = flowMessaging.initiateFlow(otherMember);
   ```
2. Simply call `send()` on the session and pass a payload:
   ```java
        session.send(message);
   ```
   The code continues to execute until it reaches the `session.receive()` method. At that point, the flow checkpoints and persists its state to the database. It resumes when it receives a message back from the responder. This frees up the Corda cluster flow workers to perform other tasks.
   {{< note >}}
   There is no guarantee that the same flow worker resumes the completion of the flow and so singleton objects should be avoided in Corda 5 flows.
   {{< /note >}}
   ```java
           Message response = session.receive(Message.class);
    ```
    When the `send()` is sent to the responder, Corda executes the `MyFirstResponderFlow` responder flow `call()` method down to the `session.receive()`, which returns the payload that was sent in the initiator's `send()` method.
    ```java
    @Suspendable
    @Override
    public void call(FlowSession session) {
      log.info("MFF: MyFirstResponderFlow.call() called");
      Message receivedMessage = session.receive(Message.class);
      ...
    }
    ```

   The responder flow then obtains its own identity from its injected `memberLookup` service, creates a response, and sends the response back using `session.send()`:
   ```java
      MemberX500Name ourIdentity = memberLookup.myInfo().getName();
      Message response = new Message(ourIdentity,
             "Hello " + session.getCounterparty().getCommonName() + ", best wishes from " + ourIdentity.getCommonName());
     log.info("MFF: response.message: " + response.message);
     session.send(response);
   ```
   There is no return value for a ResponderFlow.

   Back on the Initiating virtual node, Corda detects the send coming from the responder and rehydrates the initiating flow from the database and resumes it from where it was checkpointed.

   The response is received and `response.message` is returned by the flow.
   ```java
      Message response = session.receive(Message.class);
      return response.message;
   ```
   The response from the initiating flow is always a string, which can be returned when the flow status is queried by REST.

## Other Considerations for FlowSessions
It is important that the sends and receives in the initiator and responder flows match. If the initiator sends a Foo and the responder expects a Bar, the flow hangs and likely results in a timeout error.

As with Corda 4, there is also a `sendAndReceive` method on `FlowSession` that sends a payload, check-points the flow, and then waits for a response to be received:
```java
<ReceiveType> response = myFlowSession.sendAndReceive(<ReceiveType>.class, payload);
```
In Corda 4, when payloads were received they were wrapped in an `UntrustworthyData` class which required unwrapping:
```java
// (Corda 4)
<ReceiveType> corda4Response = myFlowSession.sendAndReceive(<ReceiveType>.class, payload).unwrap( it->{
   <validationcode>
});
```
This has been removed in Corda 5 because CorDapp Developers usually use other methods to validate the data.
