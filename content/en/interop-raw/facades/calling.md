---
date: '2023-08-02'
title: "Calling Facade"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interoperability-cordapp-api-calling
    parent: corda5-interoperability-cordapp-api-facades
    weight: 2000
section_menu: corda5
---

# Calling Facade

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
