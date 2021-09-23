---
title: "Injecting Corda Services"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1050
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Injection of Corda Services into flows and other Corda Services.
---

In the Corda 5 Developer Preview, you can use the annotation `@CordaInject` to inject Corda Services into flows and other Corda Services. The best way to learn how to inject services is to follow the building a CorDapp tutorial.

## Make a custom Corda Service injectable

In order to make a service injectable, you must first make it implement one or both of the injection interfaces:

* `CordaFlowInjectable`
* `CordaServiceInjectable`

These are empty interfaces used to indicate that a service can be injected, and where it can be injected. Implementing `CordaFlowInjectable` will allow for injection into a flow, and `CordaServiceInjectable` will allow for injection into a Corda Service or notary service.

## `CordaInjectPrestart`

The `CordaService` interface provides lifecycle support for the service implementing the interface. This allows you to write functions to respond to specific lifecycle events. One of these lifecycle events is when the service is starting, so any logic needed to set up a service is added for this event. If one Corda Service depends on another Corda Service during the services start event, then the latter service must be started first and have all it's dependencies injected to guarantee that it is safe to use. To allow for the service start functionality to be added and still allow injection, use the annotation `@CordaInjectPreStart`.

Use `@CordaInjectPreStart` to indicate that a dependency needs to be injected before the service start event is distributed. When Corda Services are being set up:

1. They are initialized and registered for injection.
2. Dependencies annotated with `@CordaInjectPreStart` are injected.
3. The service start lifecycle event is distributed to all Corda Services.
4. All service dependencies annotated with `@CordaInject` are injected.

During the handling of the `@CordaInjectPreStart` dependencies, Corda Services are topological sorted based on the `@CordaInjectPreStart` dependencies in each service. This ensures that services are started in the right order based on their pre-start dependencies. A service can only be started once all of its dependencies annotated with `@CordaInjectPreStart` have successfully started, and all of those dependencies have had _all_ of their dependencies initialized. This means that a service cannot inject another service as a pre-start dependency unless that service to be injected has either no injectable dependencies, or all its injectable dependencies are annotated with `@CordaInjectPreStart`. If the topological sort of pre-start dependencies finds that there is a circular dependency, then an exception is thrown as it would be impossible to start the services in the correct order.

### Examples of valid and invalid pre-start dependency injection

These examples show where pre-start injection has been added correctly, and cases where it would fail and why.

### Valid pre-start dependency injection

This is a basic example of a valid case where `MyOtherService` has behaviour defined for during service startup which requires the use of `MyService`. `MyService` is annotated as `@CordaInjectPreStart` and has no dependencies of its own, so it's safe to inject it as a pre-start dependency of `MyOtherService`:

``` kotlin
class MyService : CordaService, CordaServiceInjectable {
    fun doSomething() { println("Doing something in MyService") }
}

class MyOtherService : CordaService {
    @CordaInjectPreStart
    lateinit var myService: MyService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if(event == SERVICE_START) {
            myService.doSomething()
        }
    }
}
```

### Valid pre-start dependency injection chaining

This is another example of a case where `MyService` is injected into `MyOtherService` before starting, but `MyService` also has a pre-start dependency. In this case, `SimpleService` has no dependencies, so it will be injected into `MyService`, the service start event will be distributed to `MyService`, then `MyService` will be injected into `MyOtherService` before it also receives the service start event.

``` kotlin
class SimpleService: CordaService, CordaServiceInjectable {
    fun doSomething() { println("Doing something in SimpleService") }
}

class MyService : CordaService, CordaServiceInjectable {
    @CordaInjectPreStart
    lateinit var simpleService: SimpleService

    fun doSomething() {
        simpleService.doSomething()
        println("Doing something in MyService")
    }
}

class MyOtherService : CordaService {
    @CordaInjectPreStart
    lateinit var myService: MyService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if(event == SERVICE_START) {
            myService.doSomething()
        }
    }
}
```

### Invalid pre-start dependency injection circular dependency chain

This example will result in an exception being thrown because there is a circular dependency of pre-start dependencies. For pre-start injection, `MyOtherService` depends on `MyService`, `MyService` depends on `SimpleService`, and `SimpleService` depends on `MyOtherService`. It is impossible to instantiate these in order:

``` kotlin
class SimpleService: CordaService, CordaServiceInjectable {
    @CordaInjectPreStart
    lateinit var myOtherService: MyOtherService

    fun doSomething() {
        println("Doing something in SimpleService")
        myOtherService.doSomething()
    }
}

class MyService : CordaService, CordaServiceInjectable {
    @CordaInjectPreStart
    lateinit var simpleService: SimpleService

    fun doSomething() {
        println("Doing something in MyService")
        simpleService.doSomething()
    }
}

class MyOtherService : CordaService, CordaServiceInjectable {
    @CordaInjectPreStart
    lateinit var myService: MyService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if(event == SERVICE_START) {
            myService.doSomething()
        }
    }

    fun doSomething() {
        println("Doing something in MyOtherService")
    }
}
```

#### Invalid pre-start dependency injection due to a post-start injectable

This is another example of an invalid case. `MyOtherService` requires `MyService` as a pre-start dependency, but `MyService` depends on `SimpleService` after starting. You cannot guarantee that `MyService` will be usable by `MyOtherService` during startup since its own dependency will not have been initialized:

``` kotlin
class SimpleService: CordaService , CordaServiceInjectable

class MyService : CordaService, CordaServiceInjectable {
    @CordaInject
    lateinit var simpleService: SimpleService

    fun doSomething() {
        simpleService.doSomething()
        println("Doing something in MyService")
    }
}

class MyOtherService : CordaService {
    @CordaInjectPreStart
    lateinit var myService: MyService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if(event == SERVICE_START) {
            myService.doSomething()
        }
    }
}
```
