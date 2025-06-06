---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-corda-notary-metrics
    parent: corda-enterprise-4-9-corda-nodes-notary-operate
tags:
- notary
- metrics
title: Notary metrics and performance
weight: 4
---


# Highly-available notary metrics


## Available metrics

A notary exports the standard metrics exported by all Corda nodes. For more detail on this, see the [node administration page]({{< relref "../node/operating/node-administration" >}}), plus the
highly-available notary metrics below. Note that all timers and histograms use exponentially decaying reservoirs, and
all meters use exponential moving averages. These are explained in the [node metrics documentation]({{< relref "../node/operating/node-administration.md" >}}).


{{< table >}}

|Metric Name|Type|Description|
|:-----------------------------------|:--------------------------------|:-------------------------------------------------------------------|
| `Commit` | Timer | Measures the time taken in milliseconds to commit a single transaction and the number of transactions per second (TPS).|
| `IPS` | Meter | Measures the number of committed input states per second (IPS).|
| `Rollback` (Percona only)| Counter | Tracks the number of database transaction rollbacks. These might occur due to transient SQL exceptions, which are mitigated by retrying, or unexpected errors that cause the notarization to be aborted.|
| `DatabaseRetry` (JPA only)| Counter | Tracks the number of times the notary worker has attempted to retry committing a transaction to the database following a failed transaction. This might occur due to transient SQL exceptions, attempting to spend the same states on multiple notary workers in parallel, or due to issues with the underlying database.|
| `ConnectionException` | Counter |Tracks the number of times that the notary service is unable to obtain a database connection.|
| `Conflicts` | Counter | Tracks the number of double spend attempts. Note that this will also include notarisation retries.|
| `NumberOfInputStates` | Histogram | Tracks the statistical distribution of the number of input states per transaction.|
| `requestQueueSize` | Gauge | Tracks the number of transactions in the notarisation queue at a point in time.|
| `requestQueue.queuedStates` | Histogram | Tracks the statistical distribution of the total number of states in the notarisation queue.|
| `requestQueue.size` | Histogram | Tracks the statistical distribution of the number of transactions in the notarisation queue.|
| `requestProcessingETASeconds` | Histogram | Tracks the statistical distribution of the measured estimated time taken in seconds to process a given request. A notary service that is aware of its own throughput can return an estimate of how long requests will be queued for before they can be processed. Note that a default ETA is returned if there are no transactions currently in the queue.|
| `NumberOfUniqueTxHashes` | Histogram | Tracks the statistical distribution of the number of unique transactions that contributed states to each transaction. This is mainly intended for trend analysis of the number of transactions a given transaction depends on.|
| `ProcessedBatchSize` | Histogram | Measures the statistical distribution of the number of states notarised per batch. The notary groups and processes states in batches for performance reasons.|
| `BatchCommit` | Timer | Measures the time taken in milliseconds to commit a single batch and the number of batches per second.|
| `BatchSignLatency` | Timer | This metric represents the time elapsed during a batch signature, measured in milliseconds. It includes building the merkle tree for all the participating transactions using a cryptographic hash function and then signing over the root. |
{{< /table >}}


## Notary monitoring recommendations

For each metric, a number of values are provided, including:

* `Mean`: Representative of the last five minutes of received data, rather than the entire
history. Technically, uses an exponentially decaying reservoir of 1028 elements, which offers a 99.9%
confidence level with a 5% margin of error assuming a normal distribution, and an alpha
factor of 0.015, which heavily biases the reservoir to the past 5 minutes of measurements.
* `xth percentile`: Representative of the last five minutes of received data, rather than the entire
history. The value y such that x% of captured values are less than y. For example, a 95% percentile of two
means that 95% of captured values are less than two.
* `Count`: Number of times the metric was collected. This has been found to be unreliable during testing, and should
be ignored.
* `Snapshot size`: The current size of the reservoir of metrics. Should be ignored.

The key metrics to track are:


* `Commit.Mean`, `Commit.95th percentile` and `Commit.99th percentile`: Information on the duration of
transaction commits over the last five minutes.
* `requestQueue.size.Mean`: The mean number of requests in the notary queue over the last five minutes.

There is no “correct” base value for each metric, but a substantial increase in one of these metrics over time may
indicate an issue.

Notary operators may also want to track:


* `requestProcessingETASeconds`: The notary’s ETA for processing each request.
* `FlowDuration` for the `Success.net.corda.node.services.transactions.NonValidatingNotaryFlow` flow: The amount
of time it takes a non-validating notary to complete a successful notarisation flow, excluding time spent in the
Artemis queue).

Notary operators should also track non-Corda metrics of interest:


* Notary database metrics: These will be database-specific. One area to monitor would be changes in cluster
composition, and changes in leadership in particular. For example, Percona offers notification commands.
* JVM metrics: The node should be monitored in the same way as any critical JVM process.

Although Corda exports Artemis metrics, these are for internal purposes only, as they are hard to interpret.
