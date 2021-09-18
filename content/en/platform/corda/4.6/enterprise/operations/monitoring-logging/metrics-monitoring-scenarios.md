---
date: '2020-06-18T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-ops-monitoring-logging
tags:
- operations
- deployment
- planning
title: Metrics data and monitoring
weight: 20
---
# Metrics data and monitoring scenarios

You can monitor the metrics data from your node for a variety of reasons, and in different ways. Some suggested scenarios for monitoring are:

* **Risk of out of memory error** - Monitor the used memory in your node's `HeapMemoryUsage` attribute.
* **High CPU usage** - Monitor the `SystemCpuLoad` property of your node, to check for high CPU measurements.
* **High flow error rate** - Check for repeated errors in the flows being used on your node. Flows are the way CorDapps perform their functions, if there is a high level of errors, there may be either an issue with your node, or a bug in the CorDapp or flow itself.
* **Network parameter update proposal not accepted** - Check to see whether network parameters that you or another party has proposed to the Network Map have yet been accepted. The updates could still be awaiting approval.
* **Processing messages takes too long** - Measure the time taken for Peer to Peer (P2P) messaging to be processed. If there is a high latency, you can choose to flag this as an error.
* **Committing transactions time** - Measure how long it takes to commit an executed action on the network.
* **Signing transactions time** - Where a signature is required for a transaction, you can measure the time being taken for this to be completed.

You can see a complete list, and guidance on monitoring specific scenarios in the [Monitoring scenarios docs](../../node/operating/monitoring-scenarios.md/).

## Metrics data

A Corda node exports a number of metrics for the purpose of monitoring the health of the node via JMX.

You can get metrics for your node from these key sources:

* **Caches** - A Corda node maintains a number of caches. For each of the metrics below, the name of the cache must be supplied in the component field to show metrics for that cache.
* **Flows** - Flow metrics can be used to measure key data about the activity on your node. Metrics include the total number of flows in flight at a given time, the total number of completed flows, and the total number of flows that failed with an error.
* **Actions** - Actions are reified IO actions to execute as part of state machine transitions. These metrics are only exposed when the relevant action gets executed for the first time.
* **Metering** - Metering metrics can be used to get an overview of the performance of commands that are persisted, the number of persisted signing events, the length of a queue of events waiting to be persisted, and more.
* **P2P** - Messaging between parties can be measured in a number of ways, including metrics for latency between messages being sent and received between nodes, the size of sent messages, the interval between received P2P messages.
* **Other metrics** - Measure the tine taken to sign a transaction or check whether proposed network parameter updates have been accepted yet.

Take a look at the [Node metrics documentation](../../node-metrics.md/) for a complete range of the metrics data available from your node.
