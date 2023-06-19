---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Backing Store"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-backing-store
    weight: 9000
section_menu: corda5
---

# Backing Store

The backing store is responsible for abstracting database access from the uniqueness checker, and performs all read and write
operations against the uniqueness database. These metrics also have the `virtualnode_source` tag which allows metrics to be
associated with the holding IDs of specific notary virtual nodes.

Metrics of type Timer have further metrics with the suffixes `_count`, `_max`, and `_sum` that represent the number of events,
the maximum value, and the cumulative sum of values, respectively.

In addition, the Corda metrics endpoint also includes Caffeine cache metrics (`corda_cache_*`),
Kafka producer and consumer client metrics (`corda_kafka_*`), JVM metrics (`jvm_*`), process metrics (`process_*`),
and system metrics (`system_*`) provided by the corresponding Micrometer bindings.

<style>
table th:first-of-type {
    width: 25%;
}
table th:nth-of-type(2) {
    width: 10%;
}
table th:nth-of-type(3) {
    width: 20%;
}
table th:nth-of-type(4) {
    width: 45%;
}
</style>

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_backingstore_session_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The overall execution time for a (uniqueness checker) backing store session, which includes retrieving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context. |
| `corda_uniqueness_backingstore_transaction_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul>  | The execution time for a transaction within the context of a backing store session, which excludes retrieving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, then the execution time covers the cumulative duration of all retry attempts. |
| `corda_uniqueness_backingstore_transaction_error_count` | Counter | <ul><li>`virtualnode_source`</li><li>`error_type`</li></ul> | The cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. For example, a transaction that fails up to the maximum of 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error_type`). |
| `corda_uniqueness_backingstore_transaction_attempts` | DistributionSummary | <ul><li>`virtualnode_source`</li></ul> | 	The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `corda_uniqueness_backingstore_transaction_error_count` metric. |
| `corda_uniqueness_backingstore_db_commit_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The time taken by the backing store to commit a transaction (that is, write) to the database. Only updated if data is written to the database, so it is not cumulative across retry attempts for a given transaction. |
| `corda_uniqueness_backingstore_db_read_time_seconds` | Timer | <ul><li>`virtualnode_source`</li><li>`operation_name`</li></ul> | The time taken to perform a single read operation from the database. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries. |

Tags:
* `virtualnode_source`: The virtual node identity.
* `error_type`: The specific error class name.
* `operation_name`: The specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails`, or `getTransactionError`.
