---
title: "VaultStateEventService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 8000
section_menu: corda-5-dev-preview
description: >
  Listen for vault state changes with the `VaultStateEventService`.
expiryDate: '2022-09-28'  
---

Accessed only via `CordaService`s, the `VaultStateEventService` reliably allows you to listen to vault state changes triggered by the transactions persisted to the vault. It guarantees that every emitted event is processed *at least once* by all subscribers/listeners. Every state change that is persisted to the vault produces a **vault state event** that can be listened for and processed.

The `VaultStateEventService` allows any application using the service to crash or stop processing temporarily without preventing it from recovering after a restart. In the event of a restart, the processing of events resumes from the last committed position. This may lead to some events being processed more than once, but this can be mitigated by deduplication or handling duplicate events within your CorDapp's processing. You can check the Durable Cursor documentation for more information.

You may wish to make one of the following happen whenever a particular vault state event occurs:

* Start a flow.
* Send a request to an external system.
* Execute some other code within a CorDapp.

## Self-managed and fully-managed solutions

There are two functions to register intent to listen to these events:

* Self-managed solution - Returns a `DurableCursor<VaultStateEvent<ContractState>>` that is used to retrieve events using `DurableCursor.poll`.

  When using this API you must manually handle retrieval of events and ensure that the cursor's position is committed to prevent it from processing the same events again.

* Fully-managed solution - Takes in a `BiConsumer<Long, VaultStateEvent<ContractState>>` function that is executed for every produced vault state event.

  Management of the underlying `DurableCursor` is fully-managed by Corda, including retrieval of events and committing the cursor's position after successfully processing a batch of events.

{{< note >}}
Both of these APIs provide *at least once* guarantees.
{{< /note >}}

## Event generation

`VaultStateEvent`s are generated whenever a state is produced or consumed.

This means if a transaction with two input states and three output states is created, then two events with type `VaultEventType.CONSUMED` and three events with type `VaultEventType.PRODUCED` are sent to subscribers or cursors listening for these events.

## Event structure

A `VaultStateEvent<ContractState>` contains the following properties:

- `stateAndRef` (`StateAndRef<ContractState>`).
- `eventType` (`VaultEventType`) which can have two values, `PRODUCED` and `CONSUMED` representing what happened to the state that the event is related to.
- `timestamp` (`Instant`) representing the time that the event was created.

## Start a flow triggered by a vault state event

If you plan to start flows within the the `VaultStateEventService.subscribe` callback or in the processing logic of the `DurableCursor` returned by the other version of `VaultStateEventService.subscribe`, then you need to call subscribe only when you have received a `StateMachineStarted` lifecycle event.

## Self-managed solution

Subscribe to vault events and receive a `DurableCursor` that polls for `VaultStateEvent`s emitted by the vault which can then be processed. These events are emitted when states are produced or consumed (saved to the vault as output or input states).

Subscription using this method provides full control over the retrieval and processing of events. Events must be polled and the cursor's position must be maintained and committed to ensure that events are not reprocessed.

To achieve reliable behaviour, this method must be executed when the Corda process is restarted, returning a new cursor to continue processing from the last committed position. The consistent lifecycle of `CordaService`s provides a safe location to execute `subscribe`.

You should use the `PositionedValue.position` property found in the `PositionedValue`s contained in the `PollResult` returned from `Cursor.poll` as a way to manage deduplication, which is important when executing actions that must only happen once.

This overload of `subscribe` provides a self-managed solution which is handled by interacting with the `DurableCursor`. For a simpler and fully-managed solution, see the overload of `subscribe` that receives a `function`/`callback` as input.

Example usage of this API from a `CordaService`:
{{< tabs name="SelfManaged">}}
{{% tab name="Kotlin"%}}
```kotlin
class LoggingVaultEventCursor : CordaService {

    @CordaInjectPreStart
    private lateinit var vaultEventService: VaultEventService

    private lateinit var thread: Thread

    override fun onEvent(event: ServiceLifecycleEvent) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {
            val cursor: VaultEventCursor = vaultEventService.subscribe("Logging vault event cursor")
            thread = thread(name = "Logging vault event cursor", isDaemon = true) {
                while (!thread.isInterrupted) {
                    val result = cursor.poll(50, 5.minutes);
                    if (!result.isEmpty) {
                        for (positionedValue in result.positionedValues) {
                            when (val state: ContractState = positionedValue.value.stateAndRef.state.data) {
                                is LinearState -> log.info("Processing linear state: $state at position: ${positionedValue.position}")
                                is FungibleState<*> -> log.info("Processing fungible state: $state at position: $positionedValue.position")
                            }
                        }
                        cursor.commit(result.lastPosition)
                    }
                }
            }
        }
    }
}
```
{{% /tab %}}

{{% tab name="Java"%}}
```java
public class LoggingVaultEventCursor implements CordaService {

    @CordaInjectPreStart
    private VaultEventService vaultEventService;

    private Thread thread;

    @Override
    public void onEvent(@NotNull ServiceLifecycleEvent event) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {

            ThreadGroup threadGroup = new ThreadGroup("Logging vault event cursor");
            threadGroup.setDaemon(true);

            VaultEventCursor cursor = vaultEventService.subscribe("Logging vault event cursor");

            thread = new Thread(threadGroup, () -> {
                while (!thread.isInterrupted()) {
                    PollResult<VaultEvent> result = cursor.poll(50, Duration.of(5, ChronoUnit.MINUTES));
                    if (!result.isEmpty()) {
                        for (PositionedValue<VaultEvent> positionedValue : result.getPositionedValues()) {
                            ContractState state = positionedValue.getValue().getStateAndRef().getState().getData();
                            if (state instanceof LinearState) {
                                log.info("Processing linear state: " + state + " at position: " + positionedValue.getPosition());
                            } else if (state instanceof FungibleState) {
                                log.info("Processing fungible state: " + state + " at position: " + positionedValue.getPosition());
                            }
                        cursor.commit(result.getLastPosition());
                    }
                }
            });
            thread.start();
        }
    }
}
```
{{% /tab %}}
{{< /tabs >}}
## Fully-managed solution

Subscribe to vault events and execute the given `function` using each `VaultStateEvent`. These events are emitted when states are produced or consumed (saved to the vault as output or input states).

Subscription using this method is reliable, meaning all events will eventually be processed even if the process crashes. To achieve this behaviour, this method must be executed when the Corda process is restarted. The consistent lifecycle of `CordaService`s provides a safe location to execute `subscribe`.

Uncaught exceptions thrown within the provided `function` are caught within the platform code. When this happens the subscriber will continue onto the next event and update its position, meaning that the event will never be processed again by the subscriber.

The `Long` returned by the `BiConsumer` represents the deduplication ID of the event. This is the same value found in `PositionedValue.position` if you are using the self-managed solution. This value should be used to handle deduplication, which is important when executing actions that must only happen once.

This overload of `subscribe` provides a fully-managed solution, that moves the position of processed `VaultStateEvent`s after each event is processed. For more control over the position of processed events, see the overload of `subscribe` that returns a `DurableCursor`.

{{< note >}}
Names passed into `VaultStateEventService.subscribe` must be unique. There can only be a single cursor or call to subscribe with a certain name. The code currently throws a `CordaRuntimeException` if this rule is broken.
{{< /note >}}

Example usage of this API from a `CordaService`:

{{< tabs name="FullyManaged">}}
{{% tab name="Kotlin"%}}
```kotlin
class LoggingVaultEventSubscriber : CordaService {

    @CordaInjectPreStart
    private lateinit var vaultEventService: VaultEventService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {
            vaultStateEventService.subscribe("Logging vault event subscriber") { deduplicationId: Long, event: VaultStateEvent<ContractState> ->
                when (val state = event.stateAndRef.state.data) {
                    is LinearState -> log.info("Processing value linear state: $state with deduplicationId: $deduplicationId")
                    is FungibleState<*> -> log.info("Processing value fungible state: $state with deduplicationId: $deduplicationId")
                }
            }
        }
    }
}
  ```
  {{% /tab %}}

  {{% tab name="Java"%}}
```java
public class LoggingVaultEventSubscriber implements CordaService {

    @CordaInjectPreStart
    private VaultEventService vaultEventService;

    @Override
    public void onEvent(@NotNull ServiceLifecycleEvent event) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {
            vaultStateEventService.subscribe("Logging vault event subscriber", (Long deduplicationId, VaultStateEvent<ContractState> event) -> {
                ContractState state = event.getStateAndRef().getState().getData();
                if (state instanceof LinearState) {
                    log.info("Processing linear state: " + state + " with deduplicationId: " + deduplicationId);
                } else if(state instanceof FungibleState) {
                    log.info("Processing fungible state: " + state + " with deduplicationId: " + deduplicationId);
                }
            });
        }
    }
}
  ```
  {{% /tab %}}
  {{< /tabs >}}
## Preferred usage

Run at startup of Corda Services and continue until the process shuts down.

You could have one cursor or subscriber that receives all events and decides what to do with them (like the previous example),
or you could have many cursors or subscribers that each handle single every possible state type, or have something between them. It is up to your code to determine what happens.

A benefit for having multiple cursors or subscribers is concurrent processing. As each cursor and subscriber runs independently (assuming you are running cursors on individual threads), then if the logic executed for one type of state is particularly slow, it will not impact other cursors or subscribers. Each one will continue and process independently and in parallel. Slow cursors or subscribers will fall behind faster ones, but they are all guaranteed to eventually process all state events.

This is an example of using `subscribe` multiple times to only process a single type of state per subscriber:

{{< tabs name="Preferred">}}
{{% tab name="Kotlin"%}}
```kotlin
```kotlin
class LoggingVaultEventSubscriber : CordaService {

    @CordaInjectPreStart
    private lateinit var vaultEventService: VaultEventService

    override fun onEvent(event: ServiceLifecycleEvent) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {

            vaultStateEventService.subscribe("Logging linear state event subscriber") { deduplicationId: Long, event: VaultStateEvent<ContractState> ->
                val state = event.stateAndRef.state.data
                if (state is LinearState) {
                    log.info("Processing value linear state: $state with deduplicationId: $deduplicationId")
            }

            vaultStateEventService.subscribe("Logging fungible state event subscriber") { deduplicationId: Long, event: VaultStateEvent<ContractState> ->
                val state = event.stateAndRef.state.data
                if (state is FungibleState<*>) {
                    log.info("Processing value fungible state: $state with deduplicationId: $deduplicationId")
            }
        }
    }
}
```
{{% /tab %}}

{{% tab name="Java"%}}
```java
public class LoggingVaultEventSubscriber implements CordaService {

    @CordaInjectPreStart
    private VaultEventService vaultEventService;

    @Override
    public void onEvent(@NotNull ServiceLifecycleEvent event) {
        if (event == ServiceLifecycleEvent.SERVICE_START) {

            vaultStateEventService.subscribe("Logging contract state event subscriber", (Long deduplicationId, VaultStateEvent<ContractState> event) -> {
                ContractState state = event.getStateAndRef().getState().getData();
                if (state instanceof LinearState) {
                    log.info("Processing linear state: " + state + " with deduplicationId: " + deduplicationId);
                }
            });

            vaultStateEventService.subscribe("Logging fungible state event subscriber", (Long deduplicationId, VaultStateEvent<ContractState> event) -> {
                ContractState state = event.getStateAndRef().getState().getData();
                if(state instanceof FungibleState) {
                    log.info("Processing fungible state: " + state + " with deduplicationId: " + deduplicationId);
                }
            });
        }
    }
}
{{% /tab %}}
{{< /tabs >}}
