~~---
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

# Document content

This document explains Corda's interoperability features that allow your Cordapp to communicate with external Cordapps
from other application networks. In this document, you will learn about:

* Facades - How facades provide a common interface to enable interoperation between Cordapps while maintaining
  separation.
* Defining facades - The JSON format for specifying facade interfaces along with methods, parameters and return types.
* Mapping facades - Using annotations to map the facade definition to Java or Kotlin interfaces in your Cordapp code.
* Calling facades - Obtaining a proxy and invoking facade methods on a remote Cordapp.
* Implementing facades - Implementing the facade interface in a responder flow and handling requests.
* APIs - An overview of Corda APIs like FacadeService and ResponderFlow that facilitate interoperability.

By the end of this document, you will understand the key concepts, APIs and steps involved in augmenting your Cordapp
with facades for interoperation between Corda application networks.

# Introduction

Interoperability is a capability of Cordapps to communicate and coordinate activities with peers from
other Application Networks. These interactions between two different application networks often involve modifying their
respective ledgers to achieve shared objectives. For instance, one example of interoperability is atomic swap. Atomic
exchange of one asset inside Application Network for another asset in the other Application Network.
Atomic swaps represent just one of the various business use cases enabled by interoperability, which are further
explored in here [TODO link].
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
based on Façade text definition only, with implied simple semantics.
The facade definition is represented as a JSON document, offering a lightweight way to describe the methods
and their associated parameters and return values. Below we have a simple Facade definition:

```json
{
  "id": "org.corda.interop/platform/tokens/v1.0",
  "aliases": {
    "denomination": "string (org.corda.interop/platform/tokens/types/denomination/1.0)"
  },
  "queries": {
    "getBalance": {
      "in": {
        "denomination": "denomination"
      },
      "out": {
        "balance": "decimal"
      }
    }
  },
  "commands": {
    "reserve-tokens": {
      "in": {
        "denomination": "denomination",
        "amount": "decimal"
      },
      "out": {
        "reservation-ref": "uuid"
      }
    }
  }
}
```

The JSON document consists of the following elements:

- `"id"`: This field represents the fully qualified name of the facade and its version. For example, "
  org.example.facade:
  v1.0" uniquely identifies the façade.
- `"aliases"`: This section allows defining custom data types with descriptive names. The map consists of keys with
  custom
  type name, and values has format of basic type and qualifier name in brackets, in this example a custom type called
  `denomination` is of `string`type and have qualifier `org.corda.interop/platform/tokens/types/denomination/1.0)`
- `"commands"`: The "commands" section lists the methods supported by the façade. In the example,
  there's one command named `reserve-tokens`.
- `"in"`: The "in" section of a command or a query lists its input parameters, where each parameter has a descriptive
  name and a type. The type can be a primitive data type like `string`, `decimal`, or `UUID`, or it can refer to a custom
  type defined in the `aliases` section. This allows for a flexible yet expressive way to define the data expected by the
  command. In the example abow `reserve-tokens`has to input parameters `denomination`and `amount` of types (respectively)
  `demonomination` and `decimal`. The first type, as non-basic one, is defined in `aliases`section.
- `"out"`: The "out" section defines the output or return values of a command or a query. Similar to the "in" section,
  the output types can also be primitive or custom types.
- `"queries"` the section has the same structure as `commands`, it defines operations which semantic doesn't mutate
  the state as opposed to commands. The example contains a single query `getBalance` returning a value as opposed to
  `reserve-tokens` which should also change a state.

Overall, this JSON representation of the façade definition provides a clear and concise way to specify the interface
that systems can use to communicate with each other.
Implementations of a Façade can be solely based on a JSON definition.

## Mapping Façade onto a Java Interface

When defining a Façade using the JSON schema, it provides a platform-independent and descriptive way to specify the
methods and data types that a system should support. To map a Façade JSON into a Java interface, we can use
annotations to link interface methods and parameters to the corresponding Façade methods and types. This allows for a
flexible and decoupled approach, where the implementation naming of methods/parameters can differ from the Façade names.

Corda provides the following annotations to map a Java (or Kotlin) interface onto a Façade JSON specification:

* `@BindsFacade` associates the Java interface with the Façade name.
* `@FacadeVersions` indicates the supported versions of the Façade by the Java interface.
* `@BindsFacadeMethod` specifies the corresponding command or query from the Façade JSON for each interface method.
* annotation type definition is declared for each alias, annotate all method parameters which type is defined in alias
  section.

Below a sample Java interface which maps the Facade definition from the previous paragraph:

```java

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@interface Denomination {
  String value() default "org.corda.interop/platform/tokens/types/denomination/1.0";
}

public interface TokensFacade {

  @BindsFacade("org.corda.interop/platform/tokens")
  @FacadeVersions({"v1.0", "v2.0"})
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

When a Cordapp calls a Facade , no other code required apart from Corda Interoperable service which will create
a facade Proxy object from the Java interface.
For the other side of interoperable call - the Cordapp will need to implementing the interface to provide the actual
logic behind the facade. Both steps are described in the following paragraphs.

## Calling Facade

1. Interface Proxy Generation: To enable communication between two Cordapps using the Facade pattern, the first
   Cordapp ("Caller Cordapp") needs to obtain a proxy object that corresponds to the Facade interface. This proxy object
   will serve as a client-side representation of the Facade and allows the Caller Cordapp to call methods on the Facade
   in a straightforward and strongly typed manner. The proxy is generated based on the interface that represents the
   Facade, and the Corda framework handles the communication with the other Cordapp (Callee Cordapp).

   ```java
    package net.corda.v5.application.interop;

    public interface FacadeService {
        <T> T getFacade(String facadeId, Class<T> expectedType, MemberX500Name alias, String interopGroup);
        // ...
    }
   ```
   To obtain a Facade proxy use `getFacade` method from the `FacadeService` Corda Service. The method requires 4
   parameters: a Facade ID of the Facade text specification, the interface class which proxy object implements,
   and identity of the peer from other application network denoted by it's interop identity name and interop group ID.
   A sample code obtaining the ``TokensFacade`` proxy:
   ```java
   TokensFacade tokens = facadeService.getProxy(facadeId, TokensFacade::class.java, interopX500Name, interopGroupId);
   ```
2. Facade Invocation: With the Facade interface proxy in hand, the Caller Cordapp can invoke any method defined in the
   Facade. These method calls are synchronous, meaning the Caller Cordapp will wait for the response from the Callee
   Cordapp before proceeding further. This allows for a straightforward request-response pattern and simplifies the
   development of interoperable Cordapps. A sample code calling the method ``reserveTokensV1`` on the proxy
   object `tokens`:
   ```java
      TokensReservation result = tokens.reserveTokensV1("USD", amount);
   ```
   The getFacade method is strongly typed because it returns a proxy object that adheres to the Facade interface's
   methods.
   This ensures that the Caller Cordapp can call methods on the proxy with the correct parameters and return types,
   providing type safety in the communication.
3. Selecting identity: In the first point to create a proxy object we needed to provides the coordinates
   to a peer from other application network (interop identity name and interop group ID), however hwo to get this
   information?
   The Corda service `InteropIdentityLookUp` allows to retrieve registered Interop Identities, including their own
   Interop Identity.
   The registration process is described in the other document, and it's an administrative task [TODO link].
   Developers can call the `lookup` method of the service by providing the `applicationName` as a parameter. The
   method will return the corresponding `InterOpIdentityInfo` containing the interop member information:
   identity, associated with a particular X.500 name and the host network.
   ```java
    package net.corda.v5.application.interop;

    public interface InteropIdentityLookUp {
        InterOpIdentityInfo lookup(String applicationName);
   }
   ```
4. Calling a Proxy in a responder flow [TODO]

## Implementing Facade

1. Cordapp Service and Implementation: In the Callee Cordapp, the Facade is implemented as a Java or Kotlin class that
   contains the full business logic for processing the Facade methods and it's also a responder flow.
2. Dispatching Requests: The second `FacadeService` service method `dispatchFacadeRequest`
   is used by the Callee Cordapp to process incoming requests from other Cordapp. It takes the target implementation
   object (the Flow) and the request (usually in the form of a string) and dispatches it to the appropriate method
   within the Flow based on the request content.
   ```java
   package net.corda.v5.application.interop;

   public interface FacadeService {
     // ...
     String dispatchFacadeRequest(Object target, String request);
   }
   ```
   The dispatchFacadeRequest method deals with requests in a string format. Since the Corda
   interoperability world often deals with data in string form (e.g., JSON), this method takes the request as a string,
   processes it, and invokes the appropriate method in the Flow based on the request content.

3. In order to enable the processing of Façade calls on the server-side, the actual implementation of the Façade needs
   to be provided in the Callee Cordapp. This implementation class is typically a Corda responder flow, which extends
   the ResponderFlow interface.
   (The ResponderFlow interface is a part of Corda flows and is used to define the business logic for responding to
   incoming messages).
   When a Façade call is received, the `call` method of the `ResponderFlow` interface is invoked.
   This method receives a single string session message, which represents the incoming Façade request from the Caller
   Cordapp. To handle the incoming Façade request, the call method should invoke the
   `dispatchFacadeRequest` method from the `FacadeService`. The `dispatchFacadeRequest` method takes the implementation
   object (the ResponderFlow) as a parameter, along with the request in string format. The method will transform the
   request
   into concrete parameters and then call the appropriate Façade method based on the request content.
   The call method essentially acts as plumbing code, receiving the request and forwarding it to the
   appropriate method within the Facade implementation. In most cases, the implementation of the call method remains the
   same for different Facade methods. Corda provides a base class that includes the extracted call method, allowing
   developers to focus solely on implementing the specific Façade methods in the extending class.
   Here's an example of a base class that implements the ResponderFlow:
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
   method with itself as the implementation object (this). The result from the dispatchFacadeRequest method is then
   sent back as the response to the Caller Cordapp.
   Implementing the Façade business logic involves providing the concrete implementation of a Façade interface in a
   Corda responder flow. The call method within the responder flow acts as plumbing code, handling incoming
   Façade requests and dispatching them to the appropriate methods. Developers can focus on implementing the Façade
   methods with their business logic, while the Corda framework takes care of the communication and message handling
   aspects.
