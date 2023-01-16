---
aliases:
- /head/api-service-classes.html
- /HEAD/api-service-classes.html
- /api-service-classes.html
- /releases/release-V4.4/api-service-classes.html
- /docs/corda-os/head/api-service-classes.html
- /docs/corda-os/api-service-classes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-4:
    identifier: corda-os-4-4-api-service-classes
    parent: corda-os-4-4-corda-api
    weight: 260
tags:
- api
- service
- classes
title: 'API: Service Classes'
---




# API: Service Classes

Service classes are long-lived instances that can trigger or be triggered by flows from within a node. A Service class is limited to a
single instance per node. During startup, the node handles the creation of the service. If there is problem when instantiating service
the node will report in the log what the problem was and terminate.

Services allow related, reusable, functions to be separated into their own class where their functionality is
grouped together. These functions can then be called from other services or flows.


## Creating a Service

To define a Service class:



* Add the `CordaService` annotation
* Add a constructor with a single parameter of `AppServiceHub`
* Extend `SingletonSerializeAsToken`


Below is an empty implementation of a Service class:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
@CordaService
class MyCordaService(private val serviceHub: AppServiceHub) : SingletonSerializeAsToken() {

    init {
        // Custom code ran at service creation

        // Optional: Express interest in receiving lifecycle events
        services.register { processEvent(it) }
    }

    private fun processEvent(event: ServiceLifecycleEvent) {
        // Lifecycle event handling code including full use of serviceHub
        when (event) {
            STATE_MACHINE_STARTED -> {
                services.vaultService.queryBy(...)
                services.startFlow(...)
            }
            else -> {
                // Process other types of events
            }
        }
    }

    // public api of service
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
@CordaService
public class MyCordaService extends SingletonSerializeAsToken {

    private final AppServiceHub serviceHub;

    public MyCordaService(AppServiceHub serviceHub) {
        this.serviceHub = serviceHub;
        // Custom code ran at service creation

        // Optional: Express interest in receiving lifecycle events
        serviceHub.register(SERVICE_PRIORITY_NORMAL, this::processEvent);
    }

    private void processEvent(ServiceLifecycleEvent event) {
        switch (event) {
            case STATE_MACHINE_STARTED:
                serviceHub.getVaultService().queryBy(...)
                serviceHub.startFlow(...)
                break;
            default:
                // Process other types of events
                break;
        }
    }

    // public api of service
}
```
{{% /tab %}}

{{< /tabs >}}

The `AppServiceHub` provides the `ServiceHub` functionality to the Service class, with the extra ability to start flows. Starting flows
from `AppServiceHub` is explained further in [Starting Flows from a Service](#starting-flows-from-a-service).

The `AppServiceHub` also provides access to `database` which will enable the Service class to perform DB transactions from the threads
managed by the Service.

Also the `AppServiceHub` provides ability for `CordaService` to subscribe for lifecycle events of the node, such that it will get notified
about node finishing initialisation and when the node is shutting down such that `CordaService` will be able to perform clean-up of some
critical resources. For more details please have refer to KDocs for `ServiceLifecycleObserver`.


## Retrieving a Service

A Service class can be retrieved by calling `ServiceHub.cordaService` which returns the single instance of the class passed into the function:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val service: MyCordaService = serviceHub.cordaService(MyCordaService::class.java)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
MyCordaService service = serviceHub.cordaService(MyCordaService.class);
```
{{% /tab %}}

{{< /tabs >}}


{{< warning >}}
`ServiceHub.cordaService` should not be called during initialisation of a flow and should instead be called in line where
needed or set after the flow’s `call` function has been triggered.

{{< /warning >}}




## Starting Flows from a Service

Starting flows via a service can lead to deadlock within the node’s flow worker queue, which will prevent new flows from
starting. To avoid this, the rules bellow should be followed:



* When called from a running flow, the service must invoke the new flow from another thread. The existing flow cannot await the
execution of the new flow.
* When `ServiceHub.trackBy` is placed inside the service, flows started inside the observable must be placed onto another thread.
* Flows started by other means, do not require any special treatment.


{{< note >}}
It is possible to avoid deadlock without following these rules depending on the number of flows running within the node. But, if the
number of flows violating these rules reaches the flow worker queue size, then the node will deadlock. It is best practice to
abide by these rules to remove this possibility.

{{< /note >}}
