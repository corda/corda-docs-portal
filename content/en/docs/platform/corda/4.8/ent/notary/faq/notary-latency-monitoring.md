---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-running-a-notary-cluster-faq-toctree
tags:
- notary
- monitoring
- latency
- eta
title: Monitoring Notary Latency
weight: 2
---

# Monitoring Notary Latency

Three metrics should be combined when measuring notary latency:

 - `P2P.ReceiveLatency` - The time between receiving a message to queueing a flow.
 - `Flows.StartupQueueTime` - The time flows spends in the queue.
 - `FlowDuration.(Non)ValidatingFLow` - The time the flow spends being running.

## When latency elements are counted

`P2P.ReceiveLatency` measures the latency for a consumer to deliver the message to the state machine. At the end of the delivery, a flow state machine is created. The `Flows.StartupQueueTime` timer starts after the flow state machine is created, and ends when `FlowDuration` starts. The `FlowDuration` timer starts immediately before the flow state machine calls the flow's `call()` function.

Using `Flows.StartupQueueTime` alone to measure latency doesn't take account of the queue time or the time until a flow is queued.

## Additional performance indicators that can be monitored

If notary workers are performing badly, the latency of the entire cluster can be affected. There are several metrics that you can monitor to alert you to problems within your notary cluster:

 - `Flows.Actions.PersistCheckpoint` - This measures checkpoint latency and should remain stable. If it increases, there is likely a problem with the notary worker database.
 - `Flows.Actions.CommitTransaction` - This metric can vary, but a sudden spike can indicate problems with the notary worker database.

For cluster-specific monitoring:

 - `UniquenessProvider.Rollback` - This counter increases every time a transaction fails and is rolled back. This may indicate attempted double-spends, race conditions between workers, and database errors. This metric should remain stable.
 - `UniquenessProvider.BatchSignLatency` - This metric provides insights about how long generating a batch signature takes. This includes the building of a merkle tree, so it is expected that the time will vary depending on the number of events to be signed. This metric should remain stable.
 - `P2P.SendQueueSize` - This metric should be monitored to ensure the outbound bandwidth is sufficient. If the outbound bandwidth is not sufficient, the cluster may fail.
