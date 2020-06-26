---
aliases:
- /releases/4.3/running-a-notary-cluster/notary-metrics.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-notary-metrics
    parent: corda-enterprise-4-3-ha-notary-service-overview
    weight: 1110
tags:
- notary
- metrics
title: Highly-available notary metrics
---


# Highly-available notary metrics


## Available metrics

A notary exports the standard metrics exported by all Corda nodes. See [Node administration](../node-administration.md). In addition, a
highly-available notary exports the following metrics:


{{< table >}}

| Metric Name | Type | Description |
|:-----------------------------|:-----------|:-------------------------------------------------------------------|
| Commit | Timer | Measures the time taken to commit a single transaction and the number of transactions per second (TPS). |
| IPS | Meter | Measures the number of comitted input states per second (IPS). |
| Rollback|Counter | Tracks the number of database transaction rollbacks. These might occur due to transient SQL exceptions, which are mitigated by retrying, or unexpected errors that cause the notarisation to be aborted. |
| `ConnectionException` | Counter | Tracks the number of times that the notary service is unable to obtain a database connection. |
| Conflicts | Counter | Tracks the number of double spend attempts. Note that this will also include notarisation retries. |
| `NumberOfInputStates` | Histogram | Tracks the statistical distribution of the number of input states per transaction. |
| `requestQueueSize` | Gauge | Tracks the number of transactions in the notarisation queue at a point in time. |
| `requestQueue.queuedStates` | Histogram | Tracks the statistical distribution of the total number of states in the notarisation queue. |
| `requestQueue.size` | Histogram | Tracks the statistical distribution of the number of transactions in the notarisation queue. |
| `requestProcessingETASeconds` | Histogram | Tracks the statistical distribution of the measured estimated time for processing a given request. A notary service that is aware of its own throughput can return an estimate of how long requests will be queued for before they can be processed. Note that a default ETA is returned if there are no transactions currently in the queue.
| `NumberOfUniqueTxHashes` | Histogram | Tracks the statistical distribution of the number of unique transactions that contributed states to a each transaction. This is mainly intended for trend analysis of the number of transactions a given transaction depends on. |
| `ProcessedBatchSize` | Histogram | Measures the statistical distribution of the number of states notarised per batch. The notary groups and processes states in batches for performance reasons. |
| `BatchCommit` | Timer | Measures the time taken to commit a single batch and the number of batches per second. |

{{< /table >}}


## Notary monitoring recommendations

For each metric, a number of values are provided, including:


* `Mean`: Representative of roughly the last five minutes of received data. It is not derived from the entire
history. Uses exponentially decaying reservoirs
* `x th percentile`: The value y such that x% of captured values are less than y. For example, a 95% percentile of 2
means that 95% of captured values are less than 2
* `Count`: Number of times the metric was collected. This has been found to be unreliable during testing, and should
be ignored
* `Snapshot size`: The current size of the reservoir of metrics. Should be ignored

The key metrics to track are:


* `Commit.Mean`, `Commit.95 th percentile` and `Commit.99 th percentile`: Information on the duration of
transaction commits over the last five minutes
* `requestQueue.size.Mean`: The mean number of requests in the notary queue over the last five minutes

There is no “correct” base value for each metric, but a substantial increase in one of these metrics over time may
indicate an issue.

Notary operators may also want to track:


* `requestProcessingETASeconds`: The notary’s ETA for processing each request
* `FlowDuration` for the `Success.net.corda.node.services.transactions.NonValidatingNotaryFlow` flow: The amount
of time it takes a non-validating notary to complete a successful notarisation flow, excluding time spent in the
Artemis queue)

Notary operators should also track non-Corda metrics of interest:


* Notary database metrics: These will be database-specific. One area to monitor would be changes in cluster
composition, and changes in leadership in particular. For example, Percona offers notification commands
* JVM metrics: The node should be monitored in the same way as any critical JVM process. See
[Sizing and performance](../sizing-and-performance.md)

Although Corda exports Artemis metrics, these are for internal purposes only, as they are hard to interpret.
