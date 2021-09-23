---
date: '2020-09-08'
title: Flows
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-flows
    weight: 1000
project: corda-5
section_menu: corda-5-dev-preview
---

Corda networks use point-to-point messaging instead of a global broadcast. This means that coordinating a ledger update requires network participants to specify exactly what information needs to be sent, to which counterparties, and in what order. Rather than having to specify these steps manually, Corda automates the process using flows. A flow is a sequence of steps that tells a node how to achieve a specific ledger update, such as issuing an asset or settling a trade.

Once a given business process has been encapsulated in a flow and installed on the node as part of a CorDapp, a member of a network can instruct the node to kick off this business process at any time via their node.

All activity on the node occurs in the context of these flows. Unlike contracts, flows do not execute in a sandbox, meaning that nodes can perform actions such as networking, I/O, and use sources of randomness within the execution of a flow.

## Flows in the Corda 5 Developer Preview

In the Corda 5 Developer Preview, the `Flow` interface is used to implement a flow. Implementing `Flow` will define the `call` method which holds your business logic. The Corda 5 Developer Preview API is provided to the flow by injectable services, accessible by defining a field and annotating with `@CordaInject`.

## Changes from Corda 4

The `FlowLogic` abstract class used in Corda 4 has been broken up into a set of smaller interfaces. In place of
`FlowLogic`, implement the `Flow` interface which holds the `call` method.

The `progressTracker` has been removed, use logging instead.

All methods that used to exist on the `FlowLogic` abstract class are now available as injectable services using property
injection. An implementation of `FlowLogic` still exists to ease migration to Corda 5 and implements the `Flow` interface.

This move away from an abstract class to injectable services allows you to use only what you need. Features that you
don’t use do not need to be present on your flow classes.

## Flow interface

The `Flow` interface defines the `call` method that contains the flow's business logic. Implementing `Flow` is the minimum requirement to
implement a flow in the Corda 5 Developer Preview.

{{< note >}}
The `@Suspendable` annotation needs to be present on the `call` method when implementing this interface.
{{< /note >}}

```kotlin
package net.corda.v5.application.flows

import net.corda.v5.base.annotations.Suspendable
import net.corda.v5.base.exceptions.CordaRuntimeException

interface Flow<out T> {
    /**
     * This is where you fill out your business logic.
     *
     * @throws FlowException It can be thrown at any point of a [Flow] logic to bring it to a permanent end. The exception will be
     * propagated to all counterparty flows.
     * @throws CordaRuntimeException General type of exception thrown by most Corda APIs.
     * @throws UnexpectedFlowEndException Thrown when a flow session ends unexpectedly.
     */
    @Suspendable
    fun call(): T
}
```

## Service injection

The methods that previously existed on `FlowLogic` have been extracted
into injectable services. [Corda Services](../corda-services/overview.md) contains more information.

To use these services, define a field annotated with the
`@CordaInject` annotation. The system will set the field before the
`call` method is called.

{{< note >}}
You cannot use the injected services before the `call` method has
been called as they will not be available to the constructor.
{{< /note >}}

## Flow examples

In the following examples, the `FlowEngine` service is injected before
the `call` method is called and used within the `call` method.

#### Java example

```java
@InitiatingFlow
@StartableByRPC
public class FlowInjectionInJavaFlow implements Flow<Boolean> {

    @CordaInject
    public FlowEngine flowEngine;

    @Override
    public Boolean call() {
        return flowEngine.isKilled();
    }
}
```

#### Kotlin example

```kotlin
@InitiatingFlow
@StartableByRPC
class FlowInjectionInKotlinFlow : Flow<Boolean> {

    @CordaInject
    lateinit var flowEngine: FlowEngine

    @Suspendable
    override fun call(): Boolean {
        return flowEngine.isKilled
    }
}
```
