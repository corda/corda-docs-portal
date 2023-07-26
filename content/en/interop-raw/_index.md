---
title: "Interoperability Cordapp API"
date: 2023-07-25
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interoperability-cordapp-api
    parent: corda5-develop
    weight: 2000
section_menu: corda5
---

# Interoperability

# Summary

The overarching goal is to enable different Cordapps and networks to interoperate.

* The Façade interface definition provides a common specification that Cordapps can implement to communicate. The JSON format allows a platform-independent description of the interface.
* Mapping the JSON Façade to Java/Kotlin interfaces bridges the gap between interface definition and implementation. Annotations associate code elements with the Façade spec.
* On the client side, the FacadeService generates a proxy from the interface to invoke Façade methods. This connects the calling Cordapp's code to the interface.
* The server side implements the Façade interface in a ResponderFlow. The FacadeService dispatches requests to the appropriate Façade method for processing. This handles and implements the defined interface.
* Corda's base class reduces boilerplate code in the ResponderFlow. Developers can focus on the specific Façade logic.

In essence, the Façade interface definition and mapping enable common understanding between Cordapps. The FacadeService
and ResponderFlow provide the wiring to connect interface with implementation. Corda's APIs facilitate smooth
inter-network communications with minimal code exposure. The points build on each other to deliver the complete
Interoperability solution.

Interoperability is a capability of Cordapps to communicate and coordinate activities with peers from
other Application Networks. These interactions between two different application networks often involve modifying their
respective
ledgers to achieve shared objectives. For instance, one example of interoperability is an atomic swap of an item within
one application network between two parties in exchange for an item in another application network. Atomic swaps
represent just one of the various business use cases enabled by interoperability, which are further explored in
here [TODO link].
This document focuses on the API that empowers Cordapps with Interoperability capabilities. To achieve this, Cordapp
code needs to be aware of peers (identities) outside its own application network. Additionally, the Cordapp must be
capable of communicating or invoking actions on a different Cordapp that does not share a common codebase.
[TODO this is not the final diagram and the right scale]

![Application Networks and Interop Groups](interopgroup.png "Application Networks and Interop Groups")

The Interoperability API addresses these requirements, built on the principle of minimizing the exposure of code between
two different Cordapps. This is achieved through the introduction of Façade and Façade Proxy objects and Corda services
for used in Corda flows.
The Façade API acts as a bridge, facilitating seamless and secure communication between distinct Cordapps. It enables
them to interact and exchange data while maintaining a clear separation of concerns. The Façade serves as a common
interface definition, abstracting away the implementation details from the underlying Cordapps.
By incorporating Façade Proxy objects alongside other Corda APIs, developers can leverage the power of Interoperability
while maintaining a consistent and familiar development experience.
In the subsequent sections, we delve into the Façade API, exploring its components, functionality, and usage in depth.
We aim to provide a comprehensive guide that empowers developers to harness the full potential of Interoperability in
Cordapps, facilitating cross-network interactions and supporting diverse use cases.

## Façade Definition

Façade definition is a text file with minimal semantics consisting of a list of methods with parameters and return
values. The definition is an IDL (Interface Definition Language) oriented for the request/response paradigm with a
common set of data types. The definition of methods/operations in IDL allows abstracting away any programming language
details or ledger details.
Systems wishing to communicate via Façade with each other need to implement its definition. The implementation can be
based on Façade text definition only, with implied simple semantics. Façade is defined in text form in JSON format.

```json
{
  "id": "fully qualified facade name : facade version",
  "aliases": {
    "customType": "type (qualifier)"
  },
  "commands": {
    "firstCommand": {
      "in": {
        "1-st parameter name": "parameter type",
        "n-th parameter name": "parameter type"
      },
      "out": {
        "result name": "result type"
      }
    }
  }
}
```

The facade definition is represented as a JSON document, offering a lightweight way to describe the methods
and their associated parameters and return values. The JSON schema provides a formal structure for this definition,
allowing different systems to understand and implement the façade consistently.

The JSON document consists of the following elements:

- "id": This field represents the fully qualified name of the facade and its version. For example, "org.example.facade:
  v1.0" uniquely identifies the façade.
- "aliases": This section allows defining custom data types with descriptive names. The map consists of keys with custom
  type name, and values
  has format of basic type and qualifier name in brackets, for example
  "denomination" : "string (org.corda.interop/platform/tokens/types/denomination/1.0)"
- "commands": The "commands" section lists the methods supported by the façade. In the generic example,
  there's one command named "firstCommand".
- "in": The "in" section of a command lists its input parameters, where each parameter has a descriptive name and a
  type. The type can be a primitive data type like "string", "decimal", or "UUID", or it can refer to a custom type
  defined in the "aliases" section. This allows for a flexible yet expressive way to define the data expected by the
  command.
- "out": The "out" section defines the output or return values of the command. Similar to the "in" section, the output
  types can also be primitive or custom types.

Overall, this JSON representation of the façade definition provides a clear and concise way to specify the interface
that systems can use to communicate with each other.

Implementations of the façade can be solely based on this JSON definition.

## Mapping Façade onto a Java Interface

When defining a Façade using the JSON schema, it provides a platform-independent and descriptive way to specify the
methods and data types that a system should support. To map a Façade JSON into a Java interface, we can use
annotations to link interface methods and parameters to the corresponding Façade methods and types. This allows for a
flexible and decoupled approach, where the implementation naming of methods/parameters can differ from the Façade names.

Façade provides the following annotations to map the Java (or Kotlin) interface to the Façade JSON specification:
@BindsFacade: Associates the Java interface with the Façade name.
@FacadeVersions: Indicates the supported versions of the Façade by the Java interface.
@BindsFacadeMethod: Specifies the corresponding command or query from the Façade JSON for each interface method.
annotation type definition: for any alias type from Facade specification define a matching annotation type definition,
use this annotation for any method parameter which relevant Facade's parameter type was a custom type (defined in
aliases section).

```java

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@interface Denomination {
  String value() default "org.corda.interop/platform/tokens/types/denomination/1.0";
}

public interface TokensFacade {

  @BindsFacade("org.corda.interop/platform/tokens")
  @FacadeVersions({"v1.0", "v2.0", "v3.0"})
  public interface TokensFacade {

    @BindsFacadeMethod
    @Suspendable
    Double getBalance(@Denomination String denomination);

    @FacadeVersions("v1.0")
    @BindsFacadeMethod("reserve-tokens")
    @Suspendable
    UUID reserveTokensV1(@Denomination String denomination, BigDecimal amount);
  }
}
```

When a Cordapp invokes a Facade, then there is no other code required apart from Interoperable service which will create
facadeProxy object from the Java interface.
For the other side of interoperable call - the Cordapp will need to implementing the interface to provide the actual
logic behind the facade. Both steps are described in the following paragraphs.

## Calling Facade Services

1. Interface Proxy Generation: To enable communication between two Cordapps using the Facade pattern, the first
   Cordapp ("Caller Cordapp") needs to obtain a proxy object that corresponds to the Facade interface. This proxy object
   will serve as a client-side representation of the Facade and allows the Caller Cordapp to call methods on the Facade
   in a straightforward and strongly typed manner. The proxy is generated based on the interface that represents the
   Facade, and the Corda framework handles the communication with the other Cordapp (Callee Cordapp).

   ```java
    public interface FacadeService {
    <T> T getFacade(String facadeId, Class<T> expectedType, MemberX500Name alias, String interopGroup);
    ///...
    }
   ```
   To obtain a Facade proxy use `getFacade` method from the `FacadeService` Corda Service. The method requires 4
   parameters:
   a Facade ID of the Facade text specification, the interface class which proxy object implements,
   and identity of the peer from other application network denoted by it's application name and interop group
   ID [TODO this will change].
2. Facade Invocation: With the Facade interface proxy in hand, the Caller Cordapp can invoke any method defined in the
   Facade. These method calls are synchronous, meaning the Caller Cordapp will wait for the response from the Callee
   Cordapp before proceeding further. This allows for a straightforward request-response pattern and simplifies the
   development of interoperable Cordapps. A sample code obtaining a ``TokensFacade`` proxy and invoiking a
   method ``reserveTokensV1``:
   ```java
      TokensFacade tokens = facadeService.getProxy(facadeId, TokensFacade::class.java, interopX500Name, interopGroupId)
      TokensReservation result = tokens.reserveTokensV1("USD", msg.toReserve)
   ```
   The getFacade method is strongly typed because it returns a proxy
   object that adheres to the Facade interface's methods. This ensures that the Caller Cordapp can call methods on the
   proxy with the correct parameters and return types, providing type safety in the communication.
3. The InteropIdentityLookUp interface is a part of the Interoperability feature in Corda Cordapps. It allows flows to
   retrieve information about registered Interop Alias Identities, including their own Alias Identity.
   InteropIdentityLookUp provides a mechanism for flows to access the details of Interop Alias Identities that have been
   registered. This interface allows flows to inquire about the InterOpIdentityInfo for any specific Alias Identity
   associated with a given applicationName.
   Developers can call the lookup method of InteropIdentityLookUp by providing the applicationName as a parameter. The
   method will return the corresponding InterOpIdentityInfo containing the alias member information for the specified
   Alias
   Identity, associated with a particular X.500 name and the host network.
   ```java
    package net.corda.v5.application.interop;

    public interface InteropIdentityLookUp {
        InterOpIdentityInfo lookup(String applicationName);
   }
   ```
4. Cordapp Service and Implementation: In the Callee Cordapp, the Facade is implemented as a Java or Kotlin class that
   contains the full business logic for processing the Facade methods and it's also a responder flow.
5. Dispatching Requests: The second `FacadeService` service method `dispatchFacadeRequest`
   is used by the Callee Cordapp to process incoming requests from other Cordapp. It takes the target implementation
   object (the Flow) and the request (usually in the form of a string) and dispatches it to the appropriate method
   within the Flow based on the request content.
   ```java
   import net.corda.core.identity.MemberX500Name;
   public interface FacadeService {
     <T> T getFacade(String facadeId, Class<T> expectedType, MemberX500Name alias, String interopGroup);
     String dispatchFacadeRequest(Object target, String request);
   }
   ```
   The dispatchFacadeRequest method deals with requests in a string format. Since the Corda
   interoperability world often deals with data in string form (e.g., JSON), this method takes the request as a string,
   processes it, and invokes the appropriate method in the Flow based on the request content.

6. In order to enable the processing of Façade calls on the server-side, the actual implementation of the Façade needs
   to be provided in the Callee Cordapp. This implementation class is typically a Corda responder flow, which extends
   the
   ResponderFlow interface.
   ResponderFlow Interface: The ResponderFlow interface is a fundamental part of Corda flows and is used to define the
   business logic for responding to incoming messages or requests. When a Façade call is received, the call method of
   the
   ResponderFlow interface is invoked. This method receives a single string session message, which represents the
   incoming
   Façade request from the Caller Cordapp.
   FacadeService - Dispatching Requests: To handle the incoming Façade request, the call method should invoke the
   dispatchFacadeRequest method from the FacadeService. The dispatchFacadeRequest method takes the implementation
   object (
   the ResponderFlow) as a parameter, along with the request in string format. The method will transform the request
   into
   concrete parameters and then call the appropriate Façade method based on the request content.
   Plumbing Code: The call method essentially acts as plumbing code, receiving the request and forwarding it to the
   appropriate method within the Facade implementation. In most cases, the implementation of the call method remains the
   same for different Facade methods. Corda provides a base class that includes the extracted call method, allowing
   developers to focus solely on implementing the specific Façade methods.
   Base Class Implementation: A common approach to implementing the ResponderFlow is to create a class that extends the
   base class provided by Corda. The base class will handle the call method, and developers can then override specific
   Façade methods with their own business logic.
   Here's an example of a base class that implements the ResponderFlow:

  ```java
     class FacadeDispatcherFlow extends ResponderFlow {
  void call(FlowSession session) {
    FacadeRequest request = session.receive(String:: class.java);
    FacadeResponse facadeResponse = facadeService.dispatchFacadeRequest(this, request);
    session.send(facadeResponse);
  }
}
   ```

In this example, the call method receives the request from the session and then invokes the dispatchFacadeRequest method
with itself as the implementation object (this). The result from the dispatchFacadeRequest method is then sent back as
the response to the Caller Cordapp.
Implementing the Façade business logic on the server-side involves providing the concrete implementation of
the Façade in a Corda responder flow. The call method within the responder flow acts as plumbing code, handling incoming
Façade requests and dispatching them to the appropriate methods. Developers can focus on implementing the Façade methods
with their business logic, while the Corda framework takes care of the communication and message handling aspects. This
enables smooth and secure communication between Cordapps, making the Interoperable Cordapp with Facade pattern a
powerful solution for building distributed and secure applications on the Corda platform.


