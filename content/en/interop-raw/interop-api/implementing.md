---
date: '2023-08-02'
title: "Implementing Façade"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-implementing
    parent: corda5-interop-cordapp-api
    weight: 6000
section_menu: corda5
---

# Implementing Façades

[Add short intro that references the Calling Façades section]

### CorDapp Service and Implementation

In the Callee CorDapp, the Façade is implemented as a Java or Kotlin class that
contains the full business logic for processing the Façade methods and it's also a responder flow.

### Dispatching Requests

The second `FacadeService` service method `dispatchFacadeRequest` is used by the Callee CorDapp to process incoming requests
from other CorDapp. It takes the target implementation object (the flow) and the request (usually in the form of a string)
and dispatches it to the appropriate method within the flow based on the request content.
   ```java
   package net.corda.v5.application.interop;

   public interface FacadeService {
     // ...
     String dispatchFacadeRequest(Object target, String request);
   }
   ```
The `dispatchFacadeRequest` method deals with requests in a string format. Since the Corda
Interoperability world often deals with data in string form (for example, JSON), this method takes the request as a string,
processes it, and invokes the appropriate method in the flow based on the request content.

### Enabling the Processing of the Façade Calls on the Server-Side

You must provide the actual implementation of the Façade in the Callee CorDapp. This implementation class is typically a
Corda responder flow, which extends the `ResponderFlow` interface. The `ResponderFlow` interface is a part of Corda flows
and is used to define the business logic for responding to incoming messages.
When a Façade call is received, the `call` method of the `ResponderFlow` interface is invoked.
This method receives a single string session message, which represents the incoming Façade request from the Caller
CorDapp. To handle the incoming Façade request, the call method should invoke the
`dispatchFacadeRequest` method from the `FacadeService`. The `dispatchFacadeRequest` method takes the implementation
object (the `ResponderFlow`) as a parameter, along with the request in string format. The method will transform the
request into concrete parameters and then call the appropriate Façade method based on the request content.
The call method essentially acts as plumbing code, receiving the request and forwarding it to the
appropriate method within the Façade implementation. In most cases, the implementation of the call method remains the
same for different Façade methods. Corda provides a base class that includes the extracted call method, allowing
developers to focus solely on implementing the specific Façade methods in the extending class.
Here's an example of a base class that implements the `ResponderFlow`:
```java
  class FacadeDispatcherFlow extends ResponderFlow {
     void call(FlowSession session) {
        FacadeRequest request = session.receive(String.class.java);
        FacadeResponse facadeResponse = facadeService.dispatchFacadeRequest(this, request);
        session.send(facadeResponse);
     }
     Double getBalance(denomination String) {
        // ledger bussines logic
     }
     SimpleTokenReservation reserveTokensV1(denomination String, amount BigDecimal) {
       // ledger bussines logic
     }
  }
```

In this example, the call method receives the request from the session and then invokes the `dispatchFacadeRequest`
method with itself as the implementation object (this). The result from the `dispatchFacadeRequest` method is then
sent back as the response to the Caller CorDapp.
Implementing the Façade business logic involves providing the concrete implementation of a Façade interface in a
Corda responder flow. The call method within the responder flow acts as plumbing code, handling incoming
Façade requests and dispatching them to the appropriate methods. Developers can focus on implementing the Façade
methods with their business logic, while the Corda framework takes care of the communication and message handling
aspects.

