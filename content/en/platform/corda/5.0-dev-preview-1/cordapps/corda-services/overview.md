---
date: '2021-09-22'
title: Corda Services
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1000
project: corda-5
section_menu: corda-5-dev-preview
---

Corda Services are classes that provide methods to both flows and other Corda Services. Each service and method allows flows and Corda Services to perform specific functions. 

In technical terms, a Corda Service is any class that needs to be a long-lived singleton that can be injected into flows and other services via the `@CordaInject` dependency injection mechanism. You can use them to create classes external to flows where you can logically group code that isn't directly related to the execution of a flow.

For a complete overview of each Corda Service and its methods, use the [Corda 5 Developer Preview list of injectable services](injectable-services.md).

The best way to learn how to use Corda Services in the Corda 5 Developer Preview is to use the [Build a CorDapp tutorial](../tutorials/building-cordapp/overview.html).

## Basics of injecting a Corda Service

To inject Corda Services, define a field annotated with the `@CordaInject` annotation. The system will set the field before the `call` method is called.

{{< note >}}
You cannot use the injected services before the `call` method has been called as they will not be available to the constructor.
{{< /note >}}

## Flow examples

In the following examples, the `FlowEngine` service is injected before the `call` method is called and used within the `call` method.

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
