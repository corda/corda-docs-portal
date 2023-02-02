---
aliases:
- /releases/4.6/node-metrics.html
date: '2020-04-16T19:30:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- node
- metrics
title: Node metrics
weight: 6
---


# Node metrics

A Corda node exports a number of metrics for the purpose of monitoring the health of the node via JMX. These metrics are described below.

For more information on how to monitor a node, see [Node administration](node/operating/node-administration.md), [Node monitoring and logging](node/operating/monitoring-logging.md), and [Node monitoring scenarios](node/operating/monitoring-scenarios.md).


## Attachments


{{< table >}}

|Metric Query|Description|
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:name=Attachments|A count of the total number of attachments on the node.|

{{< /table >}}


## Caches

A Corda node maintains a number of caches. For each of the metrics below, the name of the cache must be supplied in the `component` field to
show metrics for that cache.

There are two types of caches: *size-based* and *weight-based*. Size-based caches are measured in the number
of entries in the cache, while weight-based caches are measured in the bytes of memory occupied by the entries.

{{< note >}}
The avalable set of metrics depends on the cache type. The `maximum-size` and `sizePercent` metrics are only available for size-based caches, while `maximum-weight`, `weight`, and `weightPercent` metrics are only available for weight-based caches.
{{< /note >}}

{{< table >}}

|Metric Query|Description|
|-------------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:type=Caches,component=<cache_name>,name=evictions|The number of items evicted from the cache.|
|net.corda:type=Caches,component=<cache_name>,name=evictions-weight|The total weight of items evicted from the cache.|
|net.corda:type=Caches,component=<cache_name>,name=hits|The number of cache hits.|
|net.corda:type=Caches,component=<cache_name>,name=loads|A histogram indicating how long loads into the cache are taking.|
|net.corda:type=Caches,component=<cache_name>,name=loads-failure|The number of items that could not be loaded into the cache.|
|net.corda:type=Caches,component=<cache_name>,name=loads-success|The number of items successfully loaded into the cache.|
|net.corda:type=Caches,component=<cache_name>,name=maximum-size|The maximum number of entries in the cache.|
|net.corda:type=Caches,component=<cache_name>,name=misses|The number of cache misses.|
|net.corda:type=Caches,component=<cache_name>,name=size|The current number of entries in the cache.|
|net.corda:type=Caches,component=<cache_name>,name=sizePercent|The current size of the cache expressed as a percentage of the maximum.|
|net.corda:type=Caches,component=<cache_name>,name=maximum-weight|The maximum size of the cache, expressed as a total weight.|
|net.corda:type=Caches,component=<cache_name>,name=weight|The current weight of the cache.|
|net.corda:type=Caches,component=<cache_name>,name=weightPercent|The current weight of the cache, expressed as a percentage of the maximum.|

{{< /table >}}


## Flows


{{< table >}}

|Metric Query|Description|
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:type=Flows,name=ActiveThreads|The total number of threads running flows.|
|net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondCurrent|The current rate at which checkpoint data is being persisted.|
|net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondHist|A histogram indicating the rate at which bytes are being checkpointed.|
|net.corda:type=Flows,name=Checkpointing Rate|The rate at which checkpoint events are occurring.|
|net.corda:type=Flows,name=Error|The total number of flows failed with an error.|
|net.corda:type=Flows,name=ErrorPerMinute|The rate at which flows fail with an error.|
|net.corda:type=Flows,name=Finished|The total number of completed flows (both successfully and unsuccessfully).|
|net.corda:type=Flows,name=InFlight|The number of in-flight flows.|
|net.corda:type=Flows,name=QueueSize|The current size of the queue for flows waiting to be executed.|
|net.corda:type=Flows,name=QueueSizeOnInsert|A histogram showing the queue size at the point new flows are added.|
|net.corda:type=Flows,name=Started|The total number of flows started.|
|net.corda:type=Flows,name=StartedPerMinute|The rate at which flows are started.|
|net.corda:type=Flows,name=Success|The total number of successful flows.|
|net.corda:type=Flows,name=<action_name>|A histogram indicating the time taken to execute a particular action. See the following section for more details.|

{{< /table >}}

### Actions


Actions are reified IO actions to execute as part of state machine transitions. These metrics are only exposed when the relevant action gets executed for the first time.

|Metric Query|Action description|
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:type=Flows,name=Actions.AcknowledgeMessages|Acknowledge messages|
|net.corda:type=Flows,name=Actions.AddSessionBinding|Create a session binding to allow routing of incoming messages.|
|net.corda:type=Flows,name=Actions.CancelFlowTimeout|Cancel the retry timeout for a flow.|
|net.corda:type=Flows,name=Actions.CommitTransaction|Commit the current database transaction.|
|net.corda:type=Flows,name=Actions.CreateTransaction|Create a new database transaction.|
|net.corda:type=Flows,name=Actions.ExecuteAsyncOperation|Execute the specified operation.|
|net.corda:type=Flows,name=Actions.PersistCheckpoint|Persist a checkpoint.|
|net.corda:type=Flows,name=Actions.PersistDeduplicationFacts|Persist deduplication facts.|
|net.corda:type=Flows,name=Actions.PropagateErrors|Propagate error messages to sessions.|
|net.corda:type=Flows,name=Actions.ReleaseSoftLocks|Release soft locks associated with a given ID.|
|net.corda:type=Flows,name=Actions.RemoveCheckpoint|Remove a checkpoint.|
|net.corda:type=Flows,name=Actions.RemoveFlow|Remove a flow.|
|net.corda:type=Flows,name=Actions.RemoveSessionBindings|Remove session bindings.|
|net.corda:type=Flows,name=Actions.RetryFlowFromSafePoint|Retry a flow from the last checkpoint. If there is no checkpoint, restart the flow with the same invocation details.|
|net.corda:type=Flows,name=Actions.RollbackTransaction|Roll back the current database transaction.|
|net.corda:type=Flows,name=Actions.ScheduleEvent|Schedule an event.|
|net.corda:type=Flows,name=Actions.ScheduleFlowTimeout|Schedule a flow to be retried if it does not complete within the timeout period specified in the configuration.|
|net.corda:type=Flows,name=Actions.SendExisting|Send a session message to a party with which there has been an established session.|
|net.corda:type=Flows,name=Actions.SendInitial|Send an initial session message to a destination.|
|net.corda:type=Flows,name=Actions.SendMultiple|Send session messages to multiple destinations.|
|net.corda:type=Flows,name=Actions.SignalFlowHasStarted|Signal that a flow is considered as started.|
|net.corda:type=Flows,name=Actions.SleepUntil|Sleep until a given moment in time.|
|net.corda:type=Flows,name=Actions.TrackTransaction|Track a transaction hash and notify the state machine once the corresponding transaction has committed.|


## Metering


{{< table >}}

|Metric Query|Description|
|-----------------------------------------------|---------------------------------------------------------------------------------------|
|net.corda:type=Metering,name=commandsPersisted|The number of unique sets of commands persisted.|
|net.corda:type=Metering,name=droppedCounts|The number of signing events not persisted.|
|net.corda:type=Metering,name=eventsProcessed|A histogram indicating the number of events processed on every aggregation interval.|
|net.corda:type=Metering,name=dataQueueSize|An instant value of the size of the queue of aggregation events.|
|net.corda:type=Metering,name=stacksPersisted|The number of unique CorDapp stacks persisted.|
|net.corda:type=Metering,name=totalCounts|The total number of signing events persisted.|

{{< /table >}}


## P2P


{{< table >}}

|Metric Query|Description|
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------|
|net.corda:type=P2P,name=ReceiveDuration|A histogram measuring latency between the node receiving a P2P message and delivering it to the state machine.|
|net.corda:type=P2P,name=ReceiveInterval|A histogram measuring the interval between received P2P messages.|
|net.corda:type=P2P,name=ReceiveMessageSize|A histogram measuring the size of received messages.|
|net.corda:type=P2P,name=SendLatency|A histogram measuring latency when sending P2P messages, between the message sending and the send acknowledgement by Artemis.|
|net.corda:type=P2P,name=SendMessageSize|A histogram measuring the size of sent messages.|
|net.corda:type=P2P,name=SendQueueSize|The size of the in-memory send queue in the state machine for messages waiting to be sent to Artemis.|
|net.corda:type=P2P,name=SendQueueSizeOnInsert|A histogram measuring the size of the in-memory send queue in the state machine when new messages are added.|

{{< /table >}}


## Other metrics


{{< table >}}

|Metric Query|Description|
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------|
|net.corda:type=NetworkParameter,name=UpdateProposed|A gauge with a `true` / `false` value to indicate that a network parameter update was proposed but it has not been accepted yet.|
|net.corda:type=Transaction,name=SignDuration|A histogram measuring the time taken to sign a transaction.|

{{< /table >}}
