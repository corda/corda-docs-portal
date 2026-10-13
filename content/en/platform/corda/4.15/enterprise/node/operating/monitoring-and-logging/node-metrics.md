---
aliases:
- /releases/4.15/node-metrics.html
date: '2020-04-16T19:30:25Z'
menu:
  corda-enterprise-4-15:
    parent: corda-enterprise-4-15-monitoring-logging
tags:
- node
- metrics
title: Node metrics
weight: 200
---


# Node metrics

A Corda node exports a number of metrics for the purpose of monitoring the health of the node via JMX. These metrics are described below.

For more information on how to monitor a node, see:
- [Node administration]({{< relref "../node-administration.md" >}})
- [Node monitoring and logging]({{< relref "overview.md" >}})
- [Node monitoring scenarios]({{< relref "monitoring-scenarios.md" >}})

## Node status

The node status, indicating what the node is currently doing, is published as `net.corda.Node.Status`, and is available almost immediately at startup.

## Metric accuracy and performance

Histogram and timer-based metrics use internal data reservoirs to compute percentile-based metric data. By default, the metrics produced by Corda nodes rely on the reservoir implementation provided by the DropWizard metrics library, which is an exponentially decaying reservoir (EDR). These reservoirs sample the data and do not keep a full set of data over time. This can cause outlying data points to be missed if they are not included in the sample set.

Alternatively, a node can be configured to use a time window reservoir by adding the following configuration block to the `node.conf` file:

```
enterpriseConfiguration {
    metricsConfiguration {
        reservoirType = TIME_WINDOW // Can also be EDR, but this is the default if this item is absent
        timeWindow = <Duration> // Optional - will default to 5m if not specified
    }
```

The `reservoirType` configuration option can be set as either `TIME_WINDOW` or `EDR`, and will default to `EDR` if the configuration block is missing.

Time window data reservoirs record all data points across the specified time window. This ensures that outliers are accurately recorded for metrics calculation, and contain a bias towards more recent results.

Using time window reservoirs increases heap memory usage proportionally to the amount of load on the system.

## Attachments


{{< table >}}

|Metric Query|Description|
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:name=Attachments|A count of the total number of attachments on the node.|

{{< /table >}}


## Caches

A Corda node maintains a number of caches. For each of the metrics below, the name of the cache must be supplied in the `component` field to
show metrics for that cache.

There are two types of cache:
- **Size-based:** Measured by the number of entries in the cache
- **Weight-based:**. Measured by the number of bytes of memory occupied by the entries

{{< note >}}
The available set of metrics depends on the cache type. The `maximum-size` and `sizePercent` metrics are only available for size-based caches, while `maximum-weight`, `weight`, and `weightPercent` metrics are only available for weight-based caches.
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


## Certificates

General information about the node’s certificates.

{{< table >}}

| Metric Query                                           | Description                                                                                                                                                    |
|--------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| net.corda:type=Certificates,name=Identity.Alias        | The key store alias of the node's legal identity certificate (by default, `identity-private-key`).                                                             |
| net.corda:type=Certificates,name=Identity.DaysToExpiry | The number of whole days left before the node's legal identity certificate expires, rounded down. The value becomes negative once the certificate has expired. |
| net.corda:type=Certificates,name=Identity.SerialNumber | The serial number, in hexadecimal, of the node's legal identity certificate (as shown by `keytool -list -v`).                                                  |
| net.corda:type=Certificates,name=NodeCA.Alias          | The key store alias of the node CA certificate, which issued the node's legal identity certificate (by default, `cordaclientca`).                              |
| net.corda:type=Certificates,name=NodeCA.DaysToExpiry   | The number of whole days left before the node CA certificate expires, rounded down. The value becomes negative once the certificate has expired.               |
| net.corda:type=Certificates,name=NodeCA.SerialNumber   | The serial number, in hexadecimal, of the node CA certificate.                                                                                                 |
| net.corda:type=Certificates,name=TLS.Alias             | The key store alias of the node's TLS certificate (by default, `cordaclienttls`).                                                                              |
| net.corda:type=Certificates,name=TLS.DaysToExpiry      | The number of whole days left before the node's TLS certificate expires, rounded down. The value becomes negative once the certificate has expired.            |
| net.corda:type=Certificates,name=TLS.SerialNumber      | The serial number, in hexadecimal, of the node's TLS certificate.                                                                                              |

{{< /table >}}


## Flows

Note that metrics related to the default thread pool do not have a *.default* suffix; this is for backward compatibility.

{{< table >}}

|Metric Query|Description|
|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
|net.corda:type=Flows,name=ActiveThreads.{threadpool}|The total number of threads running flows for the specified [thread pool](../../../cordapps/thread-pools.md).|
|net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondCurrent|The current rate at which checkpoint data is being persisted.|
|net.corda:type=Flows,name=CheckpointVolumeBytesPerSecondHist|A histogram indicating the rate at which bytes are being checkpointed.|
|net.corda:type=Flows,name=Checkpointing Rate|The rate at which checkpoint events are occurring.|
|net.corda:type=Flows,name=Error|The total number of flows failed with an error.|
|net.corda:type=Flows,name=ErrorPerMinute|The rate at which flows fail with an error.|
|net.corda:type=Flows,name=Finished|The total number of completed flows (both successfully and unsuccessfully).|
|net.corda:type=Flows,name=Hospitalized | Number of flows that are currently hospitalized. |
|net.corda:type=Flows,name=HospitalizedPerMinute | Number of flows being hospitalized per minute. |
|net.corda:type=Flows,name=InFlight|The number of in-flight flows.|
|net.corda:type=Flows,name=QueueSize.{threadpool}|The current size of the queue for flows waiting to be executed for the specified thread pool|
|net.corda:type=Flows,name=QueueSizeOnInsert.{threadpool}|A histogram showing the queue size at the point new flows are added for the specified thread pool|
|net.corda:type=Flows,name=QueueSizeTotal | The sum of all thread pool queues. |
|net.corda:type=Flows,name=Started|The total number of flows started.|
|net.corda:type=Flows,name=StartedPerMinute|The rate at which flows are started.|
|net.corda:type=Flows,name=StartupQueueTime.{threadpool} |This timer measures the time a flow spends queued before it is executed for the specified thread pool. |
|net.corda:type=Flows,name=Success|The total number of successful flows.|
|net.corda:type=Flows,name=<action_name>|A histogram indicating the time taken to execute a particular action. See the following section for more details.|
|net.corda:type=Flows,name=FlowDuration.Success.{flowclassname} | The flow duration for the default thread pool of the specified flow, if successful. |
|net.corda:type=Flows,name=FlowDuration.Failure.{flowclassname}|  The flow duration for the default thread pool of the specified flow, if failed. |
|net.corda:type=Flows,name=FlowDuration.Success.{flowclassname}.{threadpoolname} |  The flow duration for the specified thread pool of the specified flow, if successful. |
|net.corda:type=Flows,name=FlowDuration.Failure.{flowclassname}.{threadpoolname} | The flow duration for the specified thread pool of the specified flow, if failed. |
| net.corda:type=Flows,name=HeartbeatLatencyInMilliseconds | Indicates the time, in milliseconds, required to start a flow. |
| net.corda:type=Flows,name=TimeSinceLastPickedUpInSeconds | Indicates the elapsed time since the last flow was picked up from the queue, assuming other flows are still waiting to be processed. A high value suggests that flows are being starved. |
| net.corda:type=Flows,name=TimeInQueueOldestInSeconds | Indicates how long the oldest flow has been waiting in the flow executor queue. |
| net.corda:type=Flows,name=SuspendedDurationMax | Longest suspension duration among all currently suspended flows. |
| net.corda:type=Flows,name=SuspendedForMoreThanThreshold.Count | Number of flows suspended longer than the configured threshold, which is set via NodeConfiguration.flowMonitorSuspensionLoggingThresholdMillis. |
| net.corda:type=Flows,name=SuspendedForMoreThanThreshold.ThresholdInSeconds | The value in seconds to which the threshold is set. |
| net.corda:type=Flows,name=Paused | The number of flows that are currently paused, for example because the node was started in safe mode or the flows were paused from the shell. Paused flows do not progress until they are retried, so a value greater than zero usually requires an operator to act. |
| net.corda:type=Flows,name=WaitingOnNotary.Count | The number of flows on this node that are currently suspended waiting for a response from a notary. A value that keeps rising means the notary is slow or cannot be reached. This includes the case where the notary is failing internally. For example, because of a database problem, since the notary retries the request instead of rejecting it. |
| net.corda:type=Flows,name=WaitingOnNotary.MaxAgeSeconds | How long, in seconds, the oldest flow waiting for a notary response has been waiting. The value is zero if no flow is waiting. A value that keeps growing indicates that notarisation is stuck. |
| net.corda:type={hikariConfigConnectionPoolName},name=pool.Status | Database reachability status: OK if reachable, FAILED if the node cannot connect. |
{{< /table >}}

### Actions


Actions are reified IO actions to execute as part of state machine transitions. These metrics are only exposed when the relevant action gets executed for the first time.

{{<table>}}

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

{{</table>}}

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


## Node


{{< table >}}

| Metric Query                                    | Description                                                                                                                                                                                                                                                                                                                                          |
|-------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| net.corda:type=Node,name=Mode                   | The mode the node is running in. Possible values: `NORMAL` (processing flows normally), `DRAINING` (flows draining mode is enabled, so the node finishes in-flight flows but does not start new ones) or `READ_ONLY` (the node was started in read-only mode). If the node is read-only, `READ_ONLY` is reported regardless of the draining setting. |
| net.corda:type=Node,name=PlatformVersion        | The platform version of the Corda software the node is running (for example, `170`). It can be compared with the minimum platform version of the network to check whether the node is compatible.                                                                                                                                                    |
| net.corda:type=Node,name=ReleaseVersion         | The Corda release version the node is running (for example, `4.15`).                                                                                                                                                                                                                                                                                 |
| net.corda:type=Node,name=Revision               | The source code revision (commit ID) the node was built from. Together with `ReleaseVersion`, it identifies the exact build the node is running, including snapshot builds.                                                                                                                                                                          |
| net.corda:type=Node,name=StartTime              | When the node was started, as an ISO-8601 UTC timestamp (for example, `2026-10-08T13:10:05.959Z`). A change in this value indicates that the node has restarted.                                                                                                                                                                                     |
| net.corda:type=Node,name=UptimeSeconds          | The number of seconds since the node was started. A drop in this value indicates that the node has restarted.                                                                                                                                                                                                                                        |
| net.corda:type=Node,name=StartupDurationSeconds | How long, in seconds with millisecond precision, the node took to start, from when it was created until it was fully started. The value is `-1` while the node is still starting.                                                                                                                                                                    |

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
|net.corda:type=P2P,name=inbound.QueueLength | The number of inbound P2P messages waiting to be processed.|
|net.corda:type=P2P,name=outbound.LongestQueueLength | The number of P2P messages in the longest outbound queue to a peer node.|
|net.corda:type=P2P,name=outbound.LongestQueueNodeName | The node to which messages in the longest P2P outbound queue are waiting to be sent.|
|net.corda:type=P2P,name=outbound.OldestFirstMessageAge | The age, in milliseconds, of the oldest message across all P2P outbound queues.|
|net.corda:type=P2P,name=outbound.OldestFirstMessageNodeName | The node to which the oldest message across all P2P outbound queues is intended to be sent.|
|net.corda:type=P2P,name=outbound.{legalIdentity}.FirstMessageAge | The age, in milliseconds, of the oldest message in the P2P outbound queue destined for the node with {legalIdentity}.|
|net.corda:type=P2P,name=outbound.{legalIdentity}.QueueLength | The number of messages in the P2P outbound queue waiting to be sent to the node with {legalIdentity}.|

{{< /table >}}


## Other metrics


{{< table >}}

|Metric Query|Description|
|----------------------------------------------|-----------------------------------------------------------------------------------------------------------|
|net.corda:type=NetworkParameter,name=UpdateProposed|A gauge with a `true` / `false` value to indicate that a network parameter update was proposed but it has not been accepted yet.|
|net.corda:type=Transaction,name=SignDuration|A histogram measuring the time taken to sign a transaction.|
|net.corda:type=Transaction,name=NotarisationRejected.Conflict|The number of notarisation requests from this node that the notary rejected because one or more input states had already been consumed by another transaction (a double-spend attempt). It usually points to an application issue, or two transactions competing for the same states.|
|net.corda:type=Transaction,name=NotarisationRejected.TimeWindowInvalid|The number of notarisation requests from this node that the notary rejected because the transaction's time window did not include the notary's current time. It can point to clock differences between nodes or to time windows that are too narrow.|
|net.corda:type=Transaction,name=NotarisationRejected.TransactionInvalid|The number of notarisation requests from this node that the notary rejected because the transaction was invalid. For example, because contract verification failed on a validating notary or the notary does not trust the CorDapp used by the transaction.|
|net.corda:type=Transaction,name=NotarisationRejected.General|The number of notarisation requests from this node that the notary rejected with a general (internal) error. |
|net.corda:type=Transaction,name=NotarisationRejected.Other|The number of notarisation requests from this node that the notary rejected for any other reason, such as the request being sent to the wrong notary or an invalid request signature.|

{{< /table >}}

The `Transaction.NotarisationRejected` metrics count the rejections seen when the node finalises a transaction or recovers its finality. They do not count notarisation requests made directly by CorDapps through `NotaryFlow.Client`, or by `NotaryChangeFlow`. The counters only go up while the node is running and are reset to zero when it restarts, so monitoring should alert on their increase over time rather than on their absolute value.
