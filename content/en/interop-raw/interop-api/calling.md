---
date: '2023-08-02'
title: "Calling Façades"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-calling
    parent: corda5-interop-cordapp-api
    weight: 5000
section_menu: corda5
---

# Calling Façades

[Add short intro that references the Implementing Façades section]

### Generating Interface Proxy

To enable communication between two CorDapps using the Façade pattern, the first CorDapp ("Caller CorDapp") needs to obtain
a proxy object that corresponds to the Façade interface. This proxy object will serve as a client-side representation of
the Façade and allows the Caller CorDapp to call methods on the Façade in a straightforward and strongly typed manner.
The proxy is generated based on the interface that represents the Façade, and the Corda framework handles the communication
with the other CorDapp ("Callee Cordapp").

   ```java
    package net.corda.v5.application.interop;

    public interface FacadeService {
        <T> T getFacade(String facadeId, Class<T> expectedType, MemberX500Name alias, String interopGroup);
        // ...
    }
   ```
To obtain a Façade proxy, use the `getFacade` method from the `FacadeService` Corda Service. The method requires four
parameters:
* a Façade ID of the Façade text specification
* The interface class implemented by the proxy object
* Identity of the peer from other application network denoted by its Interoperability identity name
* Interoperability group ID

An example code obtaining the ``TokensFacade`` proxy:
```java
TokensFacade tokens = facadeService.getProxy(facadeId, TokensFacade::class.java, interopX500Name, interopGroupId);
```
### Invoking a Façade

With the Façade interface proxy in hand, the Caller CorDapp can invoke any method defined in the
Façade. These method calls are synchronous, meaning the Caller CorDapp will wait for the response from the Callee
CorDapp before proceeding further. This allows for a straightforward request-response pattern and simplifies the
development of interoperable CorDapps. An example code calling the method ``reserveTokensV1`` on the proxy
object `tokens`:
```java
   TokensReservation result = tokens.reserveTokensV1("USD", amount);
```
The `getFacade` method is strongly typed because it returns a proxy object that adheres to the Façade interface's
methods. This ensures that the Caller CorDapp can call methods on the proxy with the correct parameters and return types,
providing type safety in the communication.

### Selecting an Identity

In the first step for creating a proxy object you needed to provide the coordinates
to a peer from other application network (Interoperability identity name and Interoperability group ID).
The Corda service `InteropIdentityLookUp` allows to retrieve registered Interoperability identities, including their own
Interoperability identity.
The registration process is an administrative task. For more information, see [Interoperability Administration and Identity Management Guide](../interop-admin).
Developers can call the `lookup` method of the service by providing the `applicationName` as a parameter. The
method will return the corresponding `InterOpIdentityInfo` containing the Interoperability member information:
identity, associated with a particular X.500 name and the host network.
```java
 package net.corda.v5.application.interop;

 public interface InteropIdentityLookUp {
     InterOpIdentityInfo lookup(String applicationName);
 }
```

### Calling a Proxy in a Responder Flow [TODO]
