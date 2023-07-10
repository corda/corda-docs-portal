---
date: '2023-04-18'
title: "Notary Uniqueness Metrics"
menu:
  corda-5-beta:
    parent: corda-5-beta-operate
    identifier: corda-5-beta-notary-uniqueness-metrics
    weight: 2010
section_menu: corda-5-beta

---

<style>
table th:first-of-type {
    width: 20%;
}
table th:nth-of-type(2) {
    width: 25%;
}
table th:nth-of-type(3) {
    width: 25%;
}
table th:nth-of-type(4) {
    width: 30%;
}
</style>

# Notary Uniqueness Metrics

This section outlines the metrics that are provided in Corda 5 for notary and uniqueness checking functionality. Metrics have been added at the following levels:

* Ledger uniqueness checker client service
* Uniqueness checker
* Backing store

{{< note >}}
The ledger uniqueness checker client service metrics are from the perspective of the notarization flow running on a notary virtual node. The uniqueness checker and backing store metrics are from the perspective of uniqueness processing, which runs independently from flow processing.
{{< /note >}}

## Ledger Uniqueness Checker Client Service

|Metric name|Type|Tags| Description|
|-------------------------------------|-------|--------------|--------------------------------------------|
| `ledger.uniqueness.client.run.time` | Timer |`result.type` | The time taken from requesting a uniqueness check to a response being received. The `result.type` tag is set to the specific type of uniqueness check result that was returned.|

## Uniqueness Checker

The uniqueness checker handles the business logic of uniqueness checking. The implemenation is batched at two levels and three categories of metrics are provided:

* Metrics starting with `uniqueness.checker.batch` relate to "top level" metrics, which apply to a single batch processed by the uniqueness checker. As a batch may contain requests from different notary services and/or virtual nodes, these metrics provide no context as to the identities of the batch being processed.
* Metrics starting with `uniqueness.checker.subbatch` relate to "sub-batch level" metrics. Each sub-batch represents a partition for each notary virtual node identity within a batch. The virtual node identity is captured via the existing `virtualnode.source` tag.
* Metrics starting with `uniqueness.checker.request` relate to metrics applicable to specific requests within a sub-batch, such as the result of a request. Like the sub-batch metrics, these are also associated with the `virtualnode.source` tag.

|Metric Name|Type|Tags|Description|
|-------------------------------|------------------|------------------|------------------------|
| `uniqueness.checker.batch.execution.time`    | Timer    | None    | The overall execution time for a batch, inclusive of all sub-batches. |
| `uniqueness.checker.batch.size`    | DistributionSummary    | None    | The number of requests in a batch.  |
| `uniqueness.checker.subbatch.execution.time`    | Timer    | `virtualnode.source`    | The execution time for a specific sub-batch.  |
| `uniqueness.checker.subbatch.size`    | DistributionSummary    | `virtualnode.source`    |The number of requests in a sub-batch.  |
| `uniqueness.checker.request.count`    | Counter    | `virtualnode.source`, `result.type`, `duplicate`   | A count of the number of requests processed. On its own this simply duplicates information that is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context not available in the other metrics. The `result.type` tag can be used to understand the number of successful vs failed requests, and the type of failures. The `duplicate` tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result. Otherwise, it is `false`.  |

## Backing Store

The backing store is responsible for abstracting database access from the uniqueness checker, and performs all read and write operations against the uniqueness database. These metrics also have the `virtualnode.source` tag which allows metrics to be associated with the holding IDs of specific notary virtual nodes.

|Metric Name|Type|Tags|Description|
|-------------------------------|------------------|------------------|------------------------|
|`uniqueness.backingstore.session.execution.time`|Timer|`virtualnode.source`|The overall execution time for a session, which includes retriving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context.|
|`uniqueness.backingstore.transaction.execution.time`|Timer|`virtualnode.source`|The execution time for a transaction, which excludes retriving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, the execution time covers the cumulative duration of all retry attempts.|
|`uniqueness.backingstore.transaction.error.count`|Counter|`virtualnode.source`, `error.type`| The cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. For example, a transaction that fails up to the maximum of 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error.type`). |
|`uniqueness.backingstore.transaction.attempts`|DistributionSummary|`virtualnode.source`|The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `uniqueness.backingstore.transaction.error.count` metric.|
|`uniqueness.backingstore.db.commit.time`|Timer|`virtualnode.source`|The time taken to commit a transaction (i.e. write) to the database. This metric is only updated if data is written to the database, so is not cumulative across retry attempts for a given transaction.|
|`uniqueness.backingstore.db.read.time`|Timer|`virtualnode.source`, `operation.name`|The time taken to perform a single read operation from the database. The existing `operation.name` tag is re-purposed to reflect the specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails` or `getTransactionError`. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries.|