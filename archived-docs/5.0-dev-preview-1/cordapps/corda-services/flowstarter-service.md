---
title: "FlowStarterService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 2000
section_menu: corda-5-dev-preview
description: >
  An overview of `FlowStarterService`.
expiryDate: '2022-09-28'  
---

Use the `FlowStarterService` to start flows from Corda Services.

## How to inject FlowStarterService

Use the `@CordaInject` mechanism to inject `FlowStarterService` into services.

{{< note >}}
This is injectable into Corda Services only. For starting flows from inside flows, see `FlowEngine.subFlow`.
{{< /note >}}

### Java

Define a property of type `FlowStarterService` and annotate with `@CordaInject`:

```java
@CordaInject
public FlowStarterService flowStarterService;
```

### Kotlin

Define a `lateinit` property of type `FlowStarterService` and annotate with `@CordaInject`:

```kotlin
@CordaInject
lateinit var flowStarterService: FlowStarterService
```

## Using the API

The `FlowStarterService` provides a single method called `startFlow`, taking a `Flow` as a parameter.

When defining your Corda Service, you need to wait for the `StateMachineStarted` lifecycle event before starting flows.
You can do this by implementing the `onEvent` method and waiting for an event of type `StateMachineStarted`.

### Java example

```java
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.application.services.CordaService;
import net.corda.v5.application.services.flows.FlowStarterService;
import net.corda.v5.application.services.lifecycle.ServiceLifecycleEvent;
import net.corda.v5.application.services.lifecycle.StateMachineStarted;
import org.jetbrains.annotations.NotNull;

public class FlowStarterExample implements CordaService {

    @CordaInject
    public FlowStarterService flowStarterService;

    @Override
    public void onEvent(@NotNull ServiceLifecycleEvent event) {
        if (event instanceof StateMachineStarted){
            flowStarterService.startFlow(new MyFlow());
        }
    }
}
```
