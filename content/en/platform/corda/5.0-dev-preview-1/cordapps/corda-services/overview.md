---
date: '2021-09-22'
title: Corda Services
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1000
section_menu: corda-5-dev-preview
---

Corda Services are classes that provide methods to both flows and other Corda Services. Each service and method allows flows and Corda Services to perform specific functions.

In technical terms, a Corda Service is any class that needs to be a long-lived singleton that can be injected into flows and other services via the `@CordaInject` dependency injection mechanism. You can use them to create classes external to flows where you can logically group code that isn't directly related to the execution of a flow.

For example:

**Kotlin:**
```kotlin
@CordaInject
lateinit var transactionService: TransactionService
```
**Java:**
```Java
@CordaInject
TransactionService transactionService;
```

This injection is intended for use within custom CorDapp classes instantiated by Corda using reflection. This is currently limited to CorDapp flows, custom Corda Services, and notary services.

For a complete overview of each Corda Service and its methods, use the [Corda 5 Developer Preview list of injectable services](injectable-services.md).

{{< note >}}
The best way to learn how to use Corda Services in the Corda 5 Developer Preview, is to follow the [Build a CorDapp tutorial](../../tutorials/building-cordapp/overview.html).
{{< /note >}}

## Make a service injectable

In order to make a service injectable, it must first implement one or both of the injection interfaces:
* `CordaFlowInjectable`
* `CordaServiceInjectable`

These are empty interface used to indicate that a service can be injected, and where it can be injected. Implementing CordaFlowInjectable will allow for injection into a Flow, and CordaServiceInjectable will allow for injection in to a Corda service or notary service.

## Basics of injecting a Corda Service

To inject Corda Services, define a field annotated with the `@CordaInject` annotation. The system will set the field before the `call` method is called.

{{< note >}}
You cannot use the injected services before the `call` method has been called as they will not be available to the constructor.
{{< /note >}}

## Flow examples

In the following examples, the `FlowEngine` service is injected before the `call` method is called and used within the `call` method.

### Java example

```java
interface FooService extends CordaService, CordaFlowInjectable, CordaServiceInjectable {
    Boolean canFoo();
}
class FooServiceImpl implements FooService {
    @Override
    public Boolean canFoo() {
        return true;
    }
}
interface BarService extends CordaService, CordaFlowInjectable, CordaServiceInjectable {
    String getFooBar();
}
class BarServiceImpl implements BarService {
    @CordaInject
    private FooService fooService;
    @Override
    public String getFooBar() {
        if(fooService.canFoo()) {
            return "foobar";
        } else {
            return "bar";
        }
    }
}
@StartableByRPC
class FooBarFlow implements Flow<String> {
    @CordaInject
    private BarService barService;

    @Override
    public String call() {
        return barService.getFooBar();
    }
}
```

### Kotlin example

```kotlin
interface FooService : CordaService, CordaFlowInjectable, CordaServiceInjectable {​
    fun canFoo(): Boolean
}​
class FooServiceImpl : FooService {​
    override fun canFoo(): Boolean {​
        return true
}​
}​
interface BarService : CordaService, CordaFlowInjectable, CordaServiceInjectable {​
    fun getFooBar(): String
}​
class BarServiceImpl : BarService {​
    @CordaInject
private lateinit var fooService: FooService
    override fun getFooBar(): String {​
        return if(fooService.canFoo()) {​
            "foobar"
}​ else {​
            "bar"
}​
    }​
}​
@StartableByRPC
class FooBarFlow : Flow<String> {​
    @CordaInject
private lateinit var barService: BarService
    override fun call(): String {​
        return barService.getFooBar()
    }​
}​
```
