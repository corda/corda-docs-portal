---
title: "Writing custom services"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1070
section_menu: corda-5-dev-preview
description: >
  Write your own Corda Services and make them injectable.
expiryDate: '2022-09-28'  
---

The method of defining a custom Corda service in the Corda 5 Developer Preview makes use of the Corda Service interface. Use this document to help you write custom Corda Services which are:

* Singleton services.
* Automatically instantiated by Corda upon node start-up.
* Serialized as tokens.


## New in the Corda 5 Developer Preview

To create a Corda Service in Corda 4, you have to create a class annotated with `@CordaService` which extends the `SingletonSerializeAsToken` abstract class or the implemented `SerializeAsToken` interface, and have a constructor which accepts `AppServiceHub` as a single input parameter. In the Corda 5 Developer preview, it is more straightforward to define a service, thanks to the Corda Service interface.

The introduction of this interface changes how Corda Services are defined. The `@CordaService` annotation has been removed, it is no longer necessary to have a constructor with `AppServiceHub` as the only parameter, and it's no longer necessary to explicitly extend `SingletonSerializeAsToken`.

## Using the Corda Service interface

The Corda Service interface is implemented by all Corda Services, and is useful for controlling the service evolution throughout the node lifecycle.

The `CordaService` interface is not injectable by default. If it is required, you must specify the scope of injection by implementing `CordaServiceInjectable` to allow injection in to other Corda Services and notary services, or `CordaFlowInjectable` to allow injection in to flows.

For more detail on injection refer to the section on [service injection](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/overview.md).

Necessary services and functionality that were previously provided by the `AppServiceHub` can be accessed using injection. Refer to the section on [service injection](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/overview.md) for more information.

This interface extends the `SingletonSerializeAsToken` interface. Previously it was expected that the CorDapp developer would extend the `SingletonSerializeAsToken` abstract class. This is no longer the case as `SingletonSerializeAsToken` has been converted to an interface.

`CordaService` extends `ServiceLifecycleObserver` to provide a service with the ability to manage its lifecycle. It does this through the `onEvent` function which receives a `ServiceLifecycleEvent` as an argument and executes at important points in a service's lifecycle. This is described in more detail in the next section.


## CordaService interface samples

``` kotlin
interface CordaService : ServiceLifecycleObserver, SingletonSerializeAsToken
```

### Basic sample of `CordaService`

A service _must_ declare and implement its own interface, and these interfaces must be unique.

``` kotlin
interface MyServiceInterface : CordaService {
  fun doSomething()
}

class MyService : MyServiceInterface {
    override fun doSomething() {
        println("Printing from MyService")
    }
}
```

{{< note >}}
The interface `MyServiceInterface` will be registered and injected and _not_ the implementation MyService.
{{< /note >}}

## Corda Service lifecycle

The `CordaService` interface extends `ServiceLifecycleObserver` which contains a default function, `onEvent`, for reacting to service lifecycle events. This is a default function with an empty function body so that it is optional for a Corda Service to override this function, meaning that having code to react to specific lifecycle events is opt-in.

```kotlin
// [CordaService] provides the ability to subscribe to lifecycle events due to inheriting [ServiceLifecycleObserver]'s behaviour.
interface CordaService : ServiceLifecycleObserver, SingletonSerializeAsToken

interface ServiceLifecycleObserver {

    /**
     * Method allowing a service to react to certain lifecycle events. Default implementation does nothing so services only need to
     * implement the method if specific behaviour is required.
     *
     * @see ServiceLifecycleEvent
     */
    @JvmDefault
    fun onEvent(event: ServiceLifecycleEvent) {}
}
```

The `onEvent` function takes in a single parameter which is of type `ServiceLifecycleEvent`. `ServiceLifecycleEvent` is an interface which is the base interface for all service lifecycle events to which a service can react to. Currently, the available events are limited to two implementations, `StateMachineStarted` and `ServiceStart`.

`StateMachineStarted` is distributed to all Corda Services once the `NodeLifecycleEvent.StateMachineStarted` has been distributed by the node lifecycle event distributor, which occurs once the node has started the state machine.

`ServiceStart` is distributed to all Corda Services by the `CordaServiceInstaller`, while loading all services. This allows the service to run any setup logic it may need, such as code that would have previously been in the service constructor.

The `CordaServiceInstaller` scans for services, instantiates them, and then can inject dependencies. If a constructor relies on using an injected service then an exception will be thrown because the dependency will not have been initialized at that point.

An injection annotation has been added specifically for use with the service start event. `@CordaInjectPreStart` is an injection annotation which identifies injectable dependencies which are required in order to start the service. The `CordaServiceInstaller` scans for services and instantiates them, then injects pre-start dependencies, distributes the service start event, and finally injects the remaining injectable dependencies annotated with `@CordaInject`. Refer to the document on [service injection](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/overview.md) for more detailed information, including information on the order of pre-start injection.

### `ServiceLifecycleEvent`

``` kotlin
/**
 * This is the parent interface for all service lifecycle events. This type is passed in the CordaService::onEvent method.
 * Inherit from this interface for your own custom event types.
 */
interface ServiceLifecycleEvent
```

### `ServiceStart`

``` kotlin
/**
 * This event is dispatched once all Corda services have been instantiated and registered as injectable services.
 *
 * Any logic required to start the service should be added in response to this event. Services are ordered based on their usages of
 * [CordaInjectPreStart] such that all [CordaInjectPreStart] annotated services have this event distributed to them before the parent
 * service, which annotated the previously mentioned services, receives notification of this event. This event is then distributed to
 * the remaining services which are not using the [CordaInjectPreStart] annotation.
 */
interface ServiceStart : ServiceLifecycleEvent
```

### `StateMachineStarted`

``` kotlin
/**
 * This event is dispatched when State Machine is fully started.
 *
 * If a handler for this event throws [CordaServiceCriticalFailureException] - this is the way to flag that it will not make
 * sense for Corda node to continue its operation. The lifecycle events dispatcher will endeavor to terminate node's JVM as soon
 * as practically possible.
 */
interface StateMachineStarted : ServiceLifecycleEvent
```

### Service using the service start event

``` kotlin
interface ConfigHolderInterface : CordaService
class ConfigHolder : ConfigHolderInterface {

    @CordaInjectPreStart
    lateinit var cordappProvider: CordappProvider

    override fun onEvent(event: ServiceLifecycleEvent) {
        if (event is ServiceStart) {
            val config = cordappProvider.appConfig

            /*
            * `config` can now be used here.
            * Omitted usage to remove clutter in doc.
            */
        }
    }
}
```
### Service using state machine started event

``` kotlin
interface BroadcastServiceInterface : CordaService
class BroadcastService : BroadcastServiceInterface {
    private companion object {
        val log = loggerFor<BroadcastService>()
        val executor: Executor = Executors.newFixedThreadPool(8)!!
    }

    @CordaInject
    lateinit var flowStarterService: FlowStarterService

    @CordaInject
    lateinit var vaultStateEventService: VaultStateEventService

    override fun onEvent(event: ServiceLifecycleEvent) {
        // Wait for the state machine to confirm it's ready before starting to watch for vault updates
        if (event is StateMachineStarted) {
            watchVaultUpdateEvents()
            log.info("Tracking new things I say")
        }
    }

    @Suppress("unchecked_cast")
    private fun watchVaultUpdateEvents() {
        // Monitor vault updates
        vaultStateEventService.subscribe("Broadcast service") { _, event ->
            if (event.stateAndRef.state.data is ISayState && event.eventType == VaultEventType.PRODUCE) {
                val stateAndRef = event.stateAndRef as StateAndRef<ISayState>
                executor.execute {
                    log.info(stateAndRef.state.data.message)
                    flowStarterService.startFlow(SendSomeoneSaidFlow.Initiator(stateAndRef))
                }
            }
        }
    }
}
```
