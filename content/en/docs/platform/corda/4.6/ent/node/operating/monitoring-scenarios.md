---
aliases:
- /releases/4.6/node-metrics.html
date: '2020-04-16T19:30:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-monitoring-logging
tags:
- node
- monitoring
- scenarios
title: Node monitoring scenarios
weight: 100
---


# Node monitoring scenarios

Some common node monitoring scenarios are described below that you may observe when using [node metrics data](../../node-metrics.md).

One important reason to monitor a node is to decide when to failover.

## Risk of `OutOfMemoryError`

The `HeapMemoryUsage` attribute of the `java.lang:type=Memory` [MBean](https://docs.oracle.com/javase/tutorial/jmx/mbeans/index.html) contains a [MemoryUsage](https://docs.oracle.com/javase/8/docs/api/java/lang/management/MemoryUsage.html) object that represents a snapshot of heap memory usage. The value of the `used` variable in this object indicates the amount of memory currently used, and the value of the `max` variable indicates the maximum amount of memory that can be used for memory management.

If the proportion of these two values is repeatedly over 0.85, this could indicate a condition where there is a risk of reaching [OutOfMemoryError](https://docs.oracle.com/javase/8/docs/api/java/lang/OutOfMemoryError.html) condition.

## High CPU usage

The `SystemCpuLoad` property of the `java.lang:type=OperatingSystem` is a `double data type` value that indicates the "recent CPU usage" for the entire system. The maximum value of this property is 1, which corresponds to a 100% CPU usage.

If the `SystemCpuLoad` value is repeatedly close to 1 (for example, over 0.9), this means that the overall system CPU usage is consistently high.

## High flow error rate

The `net.corda:name=StartedPerMinute,type=Flows` and `net.corda:name=ErrorPerMinute,type=Flows` metrics data is collected using meters. A meter measures the rate of events over time - for example, “flows per second”. In addition to the average rate, meters also track 1-minute, 5-minute, and 15-minute moving averages. The value of the `oneMinuteRate` property for each of these metrics indicates, respectively, the rates of flows started and flows failed with an error during the past minute.

It is an indication of a high flow error rate if the "flows failed with an error" rate for the past minute reaches a significant percentage of the "flows started" - for example, over 10%.

## Network parameter update proposed and not accepted

If the value of the `net.corda:name=UpdateProposed,type=NetworkParameter` boolean type of metric is `true`, this can indicate that a network parameter update was proposed but it has not yet been accepted.

## Processing messages takes too long

The `net.corda:type=P2P,name=ReceiveDuration` metric is a histogram that measures the latency between the node receiving a P2P message and delivering it to the state machine. The properties of this metric can be combined to detect a delay in message processing.

For example, if you assume that a sufficient number of messages have been received during the past minute (at least three per second) in order to make a decision, you can flag up an error if 25% of the messages took significantly longer (at least 50%) than the average message process duration. The example below shows how scenario would look like using the properties of the metric:

`oneMinuteRate >3.0, 75thPercentile() > mean * 1.5`

## Committing transactions takes too long

The `net.corda:name=Actions.CommitTransaction,type=Flows` metric is a histogram that indicates the time taken to execute the `CommitTransaction` action. You can combine the properties of this metric to detect if the execution of this action takes an unexpectedly long time.

For example, if you assume that a sufficient number of actions have been executed during the past minute (at least three per second) in order to make a decision, you can flag up an error if 25% of the actions took significantly longer (at least 50%) to execute than the average duration of the `CommitTransaction` action. The example below shows how scenario would look like using the properties of the metric:

`oneMinuteRate >3.0, 75thPercentile() > mean * 1.5`

## Signing transactions takes too long

The `net.corda:name=SignDuration,type=Transaction` metric is a histogram that indicates the duration of signing a transaction.

You can combine the properties of this metric to detect if signing a transaction takes an unexpectedly long time.

For example, if you assume that a sufficient number of transactions have been signed during the past minute (at least three per second)in order to make a decision, you can flag up an error if 25% of the transactions took significantly longer (at least 50%) to sign than the average time it takes to sign a transaction. The example below shows how scenario would look like using the properties of the metric:

`oneMinuteRate >3.0, 75thPercentile() > mean * 1.5`

## Signing events

The total number of signing events on the node can be found by looking at the `totalCounts` metric.
