---
date: '2025-04-20'
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-cordapps-flows-segthreadpools
    parent: corda-enterprise-4-13-cordapps-flows
tags:
- api
- service
- classes
title: Using additional thread pools
weight: 10
---

Corda Enterprise executes flows in *thread pools*. A thread pool is a group of pre-created, idle threads, ready to execute tasks. The default Corda Enterprise configuration creates a single thread pool, whose size is configured by the *[flowThreadPoolSize]({{< relref "../node/setup/corda-configuration-fields.md#enterpriseconfiguration" >}})* parameter. Open Source Corda is single-threaded.

In Corda 4.12 and previous versions, only the single, default thread pool described above was supported. From Corda 4.13 onward, the Enterprise version enables operators to define *multiple* thread pools and assign flows to them. The reason for this is to enable operators to prioritize particular flows and to segregate them from other flows.

For example, if there are slow-running reporting flows and more important transactional flows on the same system, the reporting flows can be separated into a dedicated thread pool so that they do not block the transactional flows.

Corda Enterprise targets the flow thread pools directly when it starts a flow. Therefore, there is no conflict between starting flows if one pool is performing badly and has a big queue.

## Configuring thread pools

Thread pools are defined in the [node configuration]({{< relref "../node/setup/corda-configuration-file.md" >}}) by adding an `additionalFlowThreadPools` array within the `tuning` object. The `additionalFlowThreadPools` array can contain one or more objects, each specifying the details of an additional thread pool. Each object contains a `threadpool` and `size` property, respectively defining the name of the thread pool and its size in number of threads.

### Example 1: Two Defined Thread Pools

The following sample configuration defines two thread pools based on the example above, `reporting` and `transactions`, each with three available threads:

```json
enterpriseConfiguration {
    tuning {
        additionalFlowThreadPools= [
            {
                threadPool=reporting,
                size=3
            },
            {
                threadPool=transactions,
                size=3
            },
        ]
    }
}
```

The related flows then need to be tagged accordingly:

```
@FlowThreadPool("reporting")
```

and

```
@FlowThreadPool("transactions")
```

### Example 2: One Defined Thread Pool and Default Thread Pool

An alternative configuration, rather than defining two thread pools, could instead define one thread pool (in this case, `reporting`) but also use the default thread pool, defining its size using `flowThreadPoolSize`. As in previous versions of Corda, the size of the default thread pool (name: "default") is still specified by the *[flowThreadPoolSize]({{< relref "../node/setup/corda-configuration-fields.md#enterpriseconfiguration" >}})* parameter. 

```json
enterpriseConfiguration {
    tuning {
        flowThreadPoolSize = 3,
        additionalFlowThreadPools= [
            {
                threadPool=reporting,
                size=3
            },
        ]
    }
}
```

Only the flows related to reporting then need to be tagged accordingly:

```
@FlowThreadPool("reporting")
```

## Logging

The Corda node's [startup log]({{< relref "../node/operating/monitoring-and-logging/overview.md" >}}) outputs the defined thread pools and their sizes; for example:

```
Created flow thread pools: reporting(3), transactions(3), default(20)
```

## Default flow-to-thread pool mapping rules

How flows are mapped to thread pools depends on:

- The thread pool configuration
- Whether or not the CorDapps installed have customized thread pool rules

The Corda default FlowSchedulerMapper follows these rules, in order of highest priority first:

1. If a flow is annotated with `@FlowThreadPool("threadpoolname")` and the referenced thread pool is defined in the configuration, then that flow is executed in the specified pool. 
   If the specified thread pool is not present in the node configuration, then the default thread pool is used instead.

2. If a thread pool named `Peer-Origin` is defined, then all flows started via a peer Corda node and **not** annotated with a specific thread pool will be executed in that thread pool. Otherwise, such flows are executed in the default thread pool.

3. If a thread pool named `RPC-Origin` is defined, then all flows started via RPC (for example, by a client application) and **not** annotated with a specific thread pool will be executed in that thread pool. Otherwise, such flows are executed in the default thread pool.

4. If none of the above rules apply to a flow, then the default behavior is the same as in previous versions of Corda: the flow is executed in the default thread pool.


## Customizing flow-to-thread pool mapping rules

CorDapps can override the above default flow mapping logic by defining a class which implements [the FlowSchedulerMapper interface](https://github.com/corda/corda/blob/release/os/4.13/core/src/main/kotlin/net/corda/core/flows/scheduler/mapper/FlowSchedulerMapper.kt); for example:

```java
interface FlowSchedulerMapper {
    fun getScheduler(
            invocationContext: InvocationContext,
            flowLogic: Class<out FlowLogic<*>>,
            ourIdentity: CordaX500Name
    ): String
}
```

The default mapping logic is available [here](https://github.com/corda/corda/blob/release/os/4.13/core/src/main/kotlin/net/corda/core/flows/scheduler/mapper/FlowSchedulerMapperImpl.kt).


Corda scans CorDapps at startup time for classes implementing the FlowSchedulerMapper interface.
Corda logs this message if it finds a single candidate:

```
Using custom flow scheduler mapper. Class {classname}
```

If it has a constructor which accepts a set of Strings, it will use that class as a flow mapper.
Corda aborts with an exception if there is more than one class or there are no matching constructors.

FlowSchedulerMapper constructors get the set of available additional thread pool names as an argument.
Its `getScheduler` method is called when a flow is scheduled.
Its expected return value is the thread pool's name, which is where the flow should be executed.

Users should package their custom scheduler mapper in a separate CorDapp. This simplifies adding or removing it from the system.
Also, having the mapper in the same package as the main app would make installing multiple apps impossible due to multiple custom scheduler mappers.

## Thread pool metrics

The following [metric]({{< relref "../node/operating/monitoring-and-logging/node-metrics.md" >}}) was introduced in 4.13 specifically for thread pools:

| Name                     | Description                         |
|--------------------------|-------------------------------------|
| QueueSizeTotal           | The sum of all thread pool queues   |

The following metrics have now been updated to be divided by thread pool:

| Previously                                     | Corda 4.13 onward                                                  |
|------------------------------------------------|--------------------------------------------------------------------|
| ActiveThreads                                  | ActiveThreads.{threadpoolname}                                     | 
| QueueSize                                      | QueueSize.{threadpoolname}                                         | 
| QueueSizeOnInsert                              | QueueSizeOnInsert.{threadpoolname}                                 |
| StartupQueueTime                               | StartupQueueTime.{threadpoolname}                                  |
| FlowDuration.{Success/Failure}.{flowclassname} | FlowDuration.{Success/Failure}.{flowclassname}.{threadpoolname>}   |

Metrics related to the default thread pool do not have a *.default* suffix; this is for backward compatibility.

