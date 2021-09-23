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

In the Corda 5 Developer Preview, you can use the annotation `@CordaInject` to inject Corda Services into flows and other Corda Services.

Required services must be declared as uninitialized, settable class properties to be properly injected for use. Injection can be used for all access-level modifiers, and for properties on superclasses.

For example:

### Kotlin

``` kotlin
@CordaInject
lateinit var transactionService: TransactionService
```

This injection is for use within custom CorDapp classes instantiated by Corda using reflection. This is currently limited to CorDapp flows, custom Corda services, and notary services.

{{< note >}}
`@CordaInjectPreStart` is another injection annotation. It is specifically used for injection in Corda Services to support the Corda Service lifecycle.
{{< /note >}}

## Make a custom Corda Service injectable

In order to make a service injectable, you must first make it implement one or both of the injection interfaces:

* `CordaFlowInjectable`
* `CordaServiceInjectable`

These are empty interfaces used to indicate that a service can be injected, and where it can be injected. Implementing `CordaFlowInjectable` will allow for injection into a flow, and `CordaServiceInjectable` will allow for injection into a Corda Service or notary service.

### Signature of singleton injection registration

Registration of a singleton service stores a mapping from interface class type to implementation instance, and can be used for notary services and Corda Services.

The interface you provide during registration is the interface which should be used in flows/services with the `@CordaInject` annotation.

An implementation can be registered under multiple interfaces, but an interface can only have a single implementation registered. This is mostly used for injection for services which previously would have been made available via `ServiceHub`.

As below:

``` kotlin
/**
 * Register an implementation for an interface. The same singleton instance of the implementation will always be injected
 * for the interface.
 *
 * @param injectableInterface The interface for which the implementation will be injected for.
 * @param implementation The implementation which will be injected the the interface.
 * @param <U> The type of the implementation being registered. Must extend the interface it's being injected for.
 * @param <T> The type of the interface being registered for injection. Must extend `CordaInjectable`.
 */
fun <U : T, T : Any> registerSingletonService(
    injectableInterface: Class<T>,
    implementation: U
)
```

### Example of singleton registration

``` kotlin
dependencyInjectionService.registerSingletonService(
    IdentityService::class.java,
    PersistentIdentityService(cacheFactory, serializationEnvironment.storageSerialization)
)
```
This could be injected into a flow/service with the following syntax:

#### Kotlin

``` kotlin
@CordaInject
lateinit var identityService: IdentityService
```
#### Java

``` java
@CordaInject
IdentityService identityService;
```

### Signature of dynamic service injection registration

When registering service implementations which need a new instance to be instantiated each time they are injected, use dynamic service injection. For example, you should use this for services which require a reference to the state machine or the flow/service which the implementation is injected into.

In Corda 4, you could use this to inject functionality that would formerly have been in the `FlowLogic` class.

As below:

``` kotlin
/**
 * Register an injector for an interface. The injector is responsible for creating a new instance of the implementation
 * to be injector for the interface.
 *
 * @param injectableInterface The interface for which the implementation injector will create an implementation for.
 * @param implementationInjector The injector responsible for creating an instance of the implementation to be injected.
 * @param <U> The type of the implementation being registered. Must extend the interface it's being injected for.
 * @param <T> The type of the interface being registered for injection. Must extend `CordaInjectable`.
 */
fun <U : T, T : Any> registerDynamicService(
    injectableInterface: Class<T>,
    implementationInjector: DependencyInjector<U>
)
```
### Example of dynamic service registration

``` kotlin
registerDynamicService(
    FlowEngine::class.java
) {
    stateMachine, currentFlow, _ ->
        FlowEngineImpl(
            stateMachine!!,
            stateMachine.logger,
            currentFlow!!
        )
}
```

This could be injected into a flow/service with the same syntax as for singleton injectables:

#### Kotlin

``` kotlin
@CordaInject
lateinit var flowEngine: FlowEngine
```
#### Java

``` java
@CordaInject
FlowEngine flowEngine;
```

The signatures of the registration functions require the implementation to implement the interface and allow for base type `Any` for the interface. This `Any` type is because no common base interface for injectables is exposed. Instead, the interfaces are validated as implementing at least one of the injectable interfaces.

### Extension function for registering singleton services in `AbstractNode`

`AbstractNode` provides an extension function, `registerForInjection`, which can be called in an implementation which will register a singleton service for a given interface.

As below:

```kotlin
/**
 * Extension function for registering service implementations for dependency injection into flows and Corda services.
 */
private fun <IMPL : INTERFACE, INTERFACE : Any> IMPL.registerForInjection(injectableInterface: Class<INTERFACE>): IMPL {
    dependencyInjectionService.registerSingletonService(injectableInterface, this)
    return this
}
```

#### Example usage of extension function

```kotlin
val identityService = PersistentIdentityService(cacheFactory, serializationEnvironment.storageSerialization)
    .tokenize()
    .registerForInjection(IdentityService::class.java)
```

## Implementation injection

Custom Corda Services, implemented by you as a CorDapp developer, and platform Corda Services, such as `VaultService`, `IdentityService`, or `HashingService`, have slightly different requirements for being injectable.

## Platform Corda Service injection

When injecting Corda Services native to the Corda platform:

* All internal services must have an internal implementation implementing a public interface. This interface is what you use when registering the implementation for injection and when requesting a dependency is injected. This exposes an API that CorDapp developers can use within their flows/services while keeping our API implementations internal. Custom Corda Services are registered for injection based on the service implementation class rather than based on interfaces.

* Internal injectable Corda Services can be either singleton services or dynamic services. This means that our internal services can be long-lived singleton services, or they can be initialized each time they are injected with a reference to the current flow, custom Corda Service, or state machine. Custom Corda Services must all be singleton services, so they can only be registered to be injected as a singleton service and cannot be injected as dynamic services.

* Registration of internal injectable services must be done during node startup, so it's up to the developer of the service to implement the registration of the service. This is typically done within `AbstractNode` using the extension function `registerForInjection`. Custom Corda Services are scanned for during node startup by jar scanning or via OSGi registration and are automatically registered for injection as a singleton service.

{{< note >}}
Even though all custom Corda Services are registered for injection when loaded, they can only be injected if they implement at least one of the injection interfaces (`CordaFlowInjectable` or `CordaServiceInjectable`). If a custom Corda Service does not implement an injection interface, a warning will be logged to the node logs, but it will not fail node startup.
{{< /note >}}_

### Components of platform Corda Service injection

``` kotlin
// Injectable interface
interface SampleService : CordaFlowInjectable, CordaServiceInjectable

// Interface implemention
class SampleServiceImpl : SampleService

// Injection registration.
//Extension function called on implementation with interface class to inject for passed in.
abstract class AbstractNode<S>(...) {
    private val nodeSampleService = SampleServiceImpl()
        .registerForInjection(SampleService::class.java)
}

// Implementation injection into a flow
class MyFlow : Flow<Unit> {
    @CordaInject
    lateinit var sampleService: SampleService
}

// Implementation injection into a custom Corda service
class MyService : CordaService {
    @CordaInject
    lateinit var sampleService: SampleService
}
```

### Components of custom Corda Service injection

``` kotlin
// Custom Corda service (service is automatically scanned for, instantiated, and registered for injection as a singleton service during node startup)
class MyService : CordaService, CordaFlowInjectable, CordaServiceInjectable

// Implementation injection into a flow
class MyFlow : Flow<Unit> {
    @CordaInject
    lateinit var myService: MyService
}

// Implementation injection into a custom Corda service
class MyService : CordaService {
    @CordaInject
    lateinit var myService: MyService
}
```

### Flow injection

Flow instantiation is done in a number of situations and all require implementations to be injected. This includes when a flow is started, when a sub-flow is started, and when a flow is loaded from a checkpoint. At each point, the flow dependencies are injected using the `DependencyInjectionService`. When a flow is deserialized from a checkpoint, it maintains references to the injected services. The state machine reference is updated for any injectable dynamic service which requires one.

#### Injection service function

``` kotlin
/**
 * Inject all available dependencies into a given flow.
 */
fun injectDependencies(flow: Flow<*>, stateMachine: FlowStateMachine<*>)
```

#### Example of flow dependency injection (from `FlowCreator`)

``` kotlin
stateMachineServices.dependencyInjectionService.injectDependencies(fiber.logic, fiber)
```

#### Kotlin implementation

``` kotlin
class MyFlow : Flow<Unit> {
    @CordaInject
    lateinit var transactionService: TransactionService

    @Suspendable
    override fun call() {}
}
```

#### Java implementation

``` java
public class InjectIntoServiceFlow implements Flow<Void> {
    @CordaInject
    private TransactionService transactionService;

    @Override
    public Void call() {
        return null;
    }
}
```

## Corda Service injection

By default, all Corda Services are not injectable. They must implement one or more of the injection interfaces to be injectable. All Corda Services are registered for injection regardless of what interfaces they implement.

`CordaServiceInstaller` is responsible for instantiating all Corda Services. When this installer loads a service, it automatically registers that service for injection. Once all services are loaded it then injects all dependencies. Services are registered as injectable based on the service implementation class name. To inject a Corda Service, the implementation class must be used as opposed to the internal service injection which is done based on interface name.

#### Injection service function

``` kotlin
/**
 * Inject all available dependencies into a given singleton service.
 */
fun injectDependencies(singletonService: SerializeAsToken)
```

#### Injection within `CordaServiceInstaller`

``` kotlin
installedServices.values.forEach {
    log.debug("Injecting @${CordaInject::class.java.simpleName} dependencies for corda service: $it")
    dependencyInjectionService.injectDependencies(it)
}
```
#### Kotlin implementation

``` kotlin
class MyService : CordaService, CordaServiceInjectable, CordaFlowInjectable

class MyOtherService : CordaService {
    @CordaInject
    lateinit var myService: MyService
}

class MyFlow : Flow<Unit> {
    @CordaInject
    lateinit var myService: MyService

    @Suspendable
    override fun call() {}
}
```

#### Java implementation

``` java
public class MyService implements CordaService, CordaServiceInjectable, CordaFlowInjectable {}

public class MyOtherService implements CordaService {
    @CordaInject
    private MyService myService;
}

public class InjectIntoServiceFlow implements Flow<Void> {
    @CordaInject
    private MyService myService;

    @Override
    public Void call() {
        return null;
    }
}
```

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

## Notary service injection

The `NotaryLoader` class scans for and instantiates notary services. The `NotaryLoader` is also responsible for using the `DependencyInjectionService` to inject dependencies annotated with `@CordaInject` into the notary service after it has been initialized. There is no advantage to having a specific notary service injection interface, so any service which implements `CordaServiceInjectable` is injectable into both custom Corda Services and notary services.
