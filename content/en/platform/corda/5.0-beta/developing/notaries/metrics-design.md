---
date: '2023-04-18'
title: "Notary Metrics Design"
menu:
  corda-5-beta:
    parent: corda-5-beta-notaries-overview
    identifier: corda-5-beta-notary-metrics-design
    weight: 6010
section_menu: corda-5-beta

---
# Notary Metrics Design

This document outlines the metrics that are provided in the Corda 5.0 (GA) release for notary and uniqueness checking functionality.

## Corda 5 Metric Architecture

Before outlining the metrics that are provided, it is worth briefly summarising how metrics work in Corda 5. The [Dropwizard](https://metrics.dropwizard.io/4.2.0/) metrics library which was used in Corda 4 has been replaced with [Micrometer](https://micrometer.io/). One of the key differences is that Micrometer supports dimensional instead of hierarchical metrics. This is much more powerful and allows querying of the metrics based on different criteria.

This factors into the design, and this section will cover both the tags used for notary and uniqueness metrics, as well as the metrics themselves.

## Metric Categories

Notarisation is formed of three main stages:

* Initiation of a notary client flow on the requesting (application) virtual node. This is done as part of a sub-flow of the UTXO ledger finalisation.

* Sending a payload across to a notary virtual node, which initiates a notary server responder flow to perform notary protocol specific verification. This then uses a uniqueness checker client service to initiate uniqueness checking. 

* A uniqueness processor picks up uniqueness check requests, and performs double spend, time window checks etc. This delegates database operations to a backing store component.

No metrics to the flows will be introduced at this point; flows already have a standard set of metrics available, although the existing metrics capture needs to be extended to capture subflow, as well as top level flow metrics, in order to do this for the notary client flow. The non-validating notary protocol is sufficiently straightforward that it is not deemed worthwhile to add any metrics specific to this protocol. Its main actions are to request uniqueness checking, which has its own metrics, and signing via the signing service, which should similarly have service level metrics added.

Instead, metrics will be added at the following levels:

* (Ledger) uniqueness checker client service
* Uniqueness checker
* Backing store

## Metric Definitions

### Ledger Uniqueness Checker Client Service

The context exposed to this service is minimal. As a result, only a single metric is captured for this service:

{{< table >}}

|Metric name|Type|Tags|Description|
|-------------------------------|------------------|------------------|------------------------|
|`ledger.uniqueness.client.run.time`|Timer|`result.type`|The time taken from requesting a uniqueness check to a response being received. The `result.type` tag is set to the relevant simple class name of the specific `UniquenessCheckResult` subclass.|

{{< /table >}}

### Uniqueness Checker

This handles the business logic of uniqueness checking. As our implemenation is batched at two levels, three categories of metrics are provided:

* Metrics starting with `uniqueness.checker.batch` relate to "top level" metrics, which apply to a single batch processed by the uniqueness checker. As a batch may contain requests from different notary services and/or virtual nodes, these metrics provide no context as to the identities of the batch being processed.
* Metrics starting with `uniqueness.checker.subbatch` relate to "sub-batch level" metrics. Each sub-batch represents a partition for each notary virtual node identity within a batch, and therefore are associated with this context via the existing `virtualnode.source` tag, which is already used in the context of P2P metrics.
* Metrics starting with `uniqueness.checker.request` relate to metrics applicable to specific requests within a sub-batch, such as the result of a request. These are also tagged with the `virtualnode.source`.

{{< table >}}

|Metric Name|Type|Tags|Description|
|-------------------------------|------------------|------------------|------------------------|
| `uniqueness.checker.batch.execution.time`    | Timer    | None    | The overall execution time for a batch, inclusive of all sub-batches. |
| `uniqueness.checker.batch.size`    | DistributionSummary    | None    | The number of requests in a batch.  |
| `uniqueness.checker.subbatch.execution.time`    | Timer    | `virtualnode.source`    | The execution time for a specific sub-batch.  |
| `uniqueness.checker.subbatch.size`    | DistributionSummary    | `virtualnode.source`    |The number of requests in a sub-batch.  |
| `uniqueness.checker.request.count`    | Counter    | `virtualnode.source`, `result.type`, `duplicate`   | A count of the number of requests processed. Not useful on its own as this information is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context. The `result.type` tag can be used to understand the number of successful vs failed requests, and the type of failures. The `duplicate` tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result, and is `false` otherwise.  |

{{< /table >}}

## Backing Store 

This is responsible for abstracting database access from the uniqueness checker, and performs all read and write operations against the uniqueness database. These metrics also have the `virtualnode.source` tag which allows metrics to be associated with the holding IDs of specific notary virtual nodes.

{{< table >}}

|Metric Name|Type|Tags|Description|
|-------------------------------|------------------|------------------|------------------------|
|`uniqueness.backingstore.session.execution.time`|Timer|`virtualnode.source`|The overall execution time for a session, which includes retriving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context.|
|`uniqueness.backingstore.transaction.execution.time`|Timer|`virtualnode.source`|The execution time for a transaction, which excludes retriving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, the execution time covers the cumulative duration of all retry attempts.|
|`uniqueness.backingstore.transaction.error.count`|Counter|`virtualnode.source`, `error.type`|Cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry, so a transaction that fails up to the maximum 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error.type`). |
|`uniqueness.backingstore.transaction.attempts`|DistributionSummary|`virtualnode.source`|The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `uniqueness.backingstore.transaction.error.count` metric.|
|`uniqueness.backingstore.db.commit.time`|Timer|`virtualnode.source`|The time taken to commit a transaction (meaning write) to the database.  This metric is only updated if data is written to the database, so is not cumulative across retry attempts for a given transaction.|
|`uniqueness.backingstore.db.read.time`|Timer|`virtualnode.source`, `operation.name`|The time taken to perform a single read operation from the database. The existing `operation.name` tag is re-purposed to reflect the specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails` or `getTransactionError`. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries.|

{{< /table >}}

### Time Metric Visualisation

The diagram below shows a composition of the different time based metrics. Note that the size of the bars is not indicative of the expected proportion of time for a metric with respect to its parent. These are arbitrary and for visualisation purposes only.

{{< figure src="C5-Notary-Metrics.png" figcaption="Corda 5 notary metric timings" alt="Corda 5 notary metric timings" >}}