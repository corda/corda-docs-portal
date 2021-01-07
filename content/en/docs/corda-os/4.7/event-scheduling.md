---
aliases:
- /head/event-scheduling.html
- /HEAD/event-scheduling.html
- /event-scheduling.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-event-scheduling
    parent: corda-os-4-7-supplementary-tutorials-index
    weight: 1060
tags:
- event
- scheduling
title: Scheduling time-based events
---




# Scheduling time-based events

This tutorial explains our approach to modelling time based events in code.

It explains how a contract state can expose an upcoming event and what action to take if the scheduled time for that event is reached.


## Introduction

Many financial instruments have time sensitive components to them.  For example, an Interest Rate Swap has a schedule
for when:


* Interest rate fixings should take place for floating legs, so that the interest rate used as the basis for payments
can be agreed.
* Any payments between the parties are expected to take place.
* Any payments between the parties become overdue.

Each of these is dependent on the current state of the financial instrument. What payments and interest rate fixings
have already happened should already be recorded in the state, for example. This means that the *next* time sensitive
event is thus a property of the current contract state. By next, we mean earliest in chronological terms, that is still
due.  If a contract state is consumed in the UTXO model, then what *was* the next event becomes irrelevant and obsolete
and the next time sensitive event is determined by any successor contract state.

Knowing when the next time sensitive event is due to occur is useful, but typically some *activity* is expected to take
place when this event occurs. We already have a model for business processes in the form of [flows](flow-state-machines.md),
so in the platform we have introduced the concept of *scheduled activities* that can invoke flow state machines
at a scheduled time. A contract state can optionally described the next scheduled activity for itself. If it omits
to do so, then nothing will be scheduled.


## Implementing scheduled events

There are two main steps to implementing scheduled events:

* Have your `ContractState` implementation also implement `SchedulableState`.  This requires a method named
`nextScheduledActivity` to be implemented which returns an optional `ScheduledActivity` instance.
`ScheduledActivity` captures what `FlowLogic` instance each node will run to perform the activity, and a `java.time.Instant` describes when it will run.
Once your state implements this interface and is tracked by the
vault, it can expect to be queried for the next activity when committed to the vault. The `FlowLogic` must be
annotated with `@SchedulableFlow`.
* If nothing suitable exists, implement a `FlowLogic` to be executed by each node as the activity itself.
The important thing to remember is that in the current implementation, each node that is party to the transaction
will execute the same `FlowLogic`, so it needs to establish roles in the business process based on the contract
state and the node it is running on. Each side will follow different but complementary paths through the business logic.

{{< note >}}
For uniformity, the scheduler’s clock always operates in the UTC time zone, so any time zone logic must be
performed by the contract, using `ZonedDateTime`.
{{< /note >}}

The production and consumption of `ContractStates` is observed by the scheduler and the activities associated with
any consumed states are unscheduled. Any newly produced states are then queried via the `nextScheduledActivity`
method and if they do not return `null` then that activity is scheduled based on the content of the
`ScheduledActivity` object returned. Be aware that this *only* happens if the vault considers the state to be
“relevant”, for example, because the owner of the node also owns that state. States that your node happens to
encounter but which aren’t related to yourself will not have any activities scheduled.


## Example

Let’s take the example of heartbeat sample in our `samples` repositories ([Kotlin](https://github.com/corda/samples-kotlin/tree/master/Features/schedulableState-heartbeat), [Java](https://github.com/corda/samples-java/tree/master/Features/schedulablestate-heartbeat)). The first task is to implement the
`nextScheduledActivity` method on the `State`.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
// Defines the scheduled activity to be conducted by the SchedulableState.
    override fun nextScheduledActivity(thisStateRef: StateRef, flowLogicRefFactory: FlowLogicRefFactory): ScheduledActivity? {
        // A heartbeat will be emitted every second. We get the time when the scheduled activity will occur in the constructor rather than in this method. This is
        // because calling Instant.now() in nextScheduledActivity returns the time at which the function is called, rather than the time at which the state was created.
        return ScheduledActivity(flowLogicRefFactory.create("com.heartbeat.flows.HeartbeatFlow", thisStateRef), nextActivityTime)
    }

```
{{% /tab %}}

{{% tab name="java" %}}
```java
// Defines the scheduled activity to be conducted by the SchedulableState.
    @Nullable
    @Override
    public ScheduledActivity nextScheduledActivity(@NotNull StateRef thisStateRef, @NotNull FlowLogicRefFactory flowLogicRefFactory) {
        // A heartbeat will be emitted every second.
        // We get the time when the scheduled activity will occur in the constructor rather than in this method. This is
        // because calling Instant.now() in nextScheduledActivity returns the time at which the function is called, rather
        // than the time at which the state was created.
        return new ScheduledActivity(flowLogicRefFactory.create("net.corda.samples.heartbeat.flows.HeartbeatFlow", thisStateRef), nextActivityTime);
    }

```
{{% /tab %}}
{{< /tabs >}}
