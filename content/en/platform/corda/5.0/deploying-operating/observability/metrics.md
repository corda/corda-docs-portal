---
date: '2023-05-10'
title: "Metrics"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-metrics
    weight: 2000
section_menu: corda5
---

Metrics provide greater insight into the inner workings of Corda 5 and can be used as the basis for monitoring and alerting.

## Collecting Metrics

All the Corda worker pods expose metrics in Prometheus text format at `/metrics` on port 7000.
By default, this port is not exposed outside the Kubernetes cluster but most observability platforms support
running an agent within the cluster that dynamically detects Kubernetes pods exposing Prometheus endpoints and then polls for metrics.

By default, the pods have the following Kubernetes annotations which may be sufficient for some monitoring agents
to automatically scrape the endpoints:

```yaml
prometheus.io/scrape: "true"
prometheus.io/path: "/metrics"
prometheus.io/port: "7000"
```

You can disable these annotations by providing the following overrides on the Corda Helm chart:

```yaml
metrics:
    scrape: false
```
If you are using the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator),
the Corda Helm chart supports the creation of a PodMonitor custom resource.
The PodMonitor should be configured with the labels that the Prometheus Operator is set to discover.
When using the [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
Helm chart, this is the name of the Helm release for the Prometheus stack. For example:

```yaml
metrics:
podMonitor:
enabled: true
labels:
release: [RELEASE_NAME]
```

### Exported Metrics

The following Corda-specific metrics are exported and they have been added at the following levels:

* HTTP requests
* Sandobox
* Messaging
* Flow
* Peer-to-peer messages and sessions
* Ledger uniqueness checker client service
* Uniqueness checker
* Backing store

#### HTTP Requests

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_http_server_request` | Counter |  | The number of HTTP requests. |
| `corda_http_server_request_time_seconds` | Timer |  | HTTP requests time. |

#### Sandbox

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_sandbox_create_time_seconds` | Timer |  | The time it took to create the sandbox. |

#### Messaging

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_messaging_processor_time_seconds` | Timer |  | The time it took to execute a message pattern processor. |

#### Flow

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_run_time_seconds` | Timer |  | The time it took for a flow to complete successfully or to produce an error. |
| `corda_flow_fiber_serialization_time_seconds` | Timer |  | Metric for flow fiber serialization. |
| `corda_flow_fiber_deserialization_time_seconds` | Timer |  | Metric for flow fiber deserialization. |

#### Peer-to-peer Messages and Sessions

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_p2p_message_outbound` | Counter |  | The number of outbound peer-to-peer data messages sent. |
| `corda_p2p_message_outbound_replayed` | Counter |  | The number of outbound peer-to-peer data messages replayed. |
| `corda_p2p_message_outbound_latency_seconds` | Timer |  | The time it took for an outbound peer-to-peer message to be delivered end-to-end (from initial processing to acknowledgement). |
| `corda_p2p_message_outbound_expired` | Counter |  | The number of outbound peer-to-peer data messages that were discarded because their TTL expired. |
| `corda_p2p_message_inbound` | Counter |  | The number of inbound peer-to-peer data messages received. |
| `corda_p2p_session_outbound_timeout` | Counter |  | The number of outbound peer-to-peer sessions that timed out (indicating communication issues with peers). |
| `corda_p2p_session_outbound` | SettableGauge |  | The number of outbound peer-to-peer sessions. |
| `corda_p2p_session_inbound` | SettableGauge |  | The number of inbound peer-to-peer sessions. |

#### Ledger Uniqueness Checker Client Service

The ledger uniqueness checker client service metrics are from the perspective of the notarization flow running on a notary virtual node.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_ledger_uniqueness_client_run_time_seconds` | Timer | `result.type` | The time taken from requesting a uniqueness check to a response being received. The `result.type` tag is set to the specific type of uniqueness check result that was returned. |

#### Uniqueness Checker

The uniqueness checker and backing store metrics are from the perspective of uniqueness processing, which runs independently of the flow processing.

The uniqueness checker handles the business logic of uniqueness checking.
The implementation is batched at two levels and three categories of metrics are provided:

* Metrics starting with `uniqueness.checker.batch` relate to “top level” metrics, which apply to a single batch
processed by the uniqueness checker. As a batch may contain requests from different notary services and/or virtual nodes,
these metrics provide no context as to the identities of the batch being processed.

* Metrics starting with `uniqueness.checker.subbatch` relate to “sub-batch level” metrics. Each sub-batch represents
a partition for each notary virtual node identity within a batch. The virtual node identity is captured via the existing `virtualnode.source` tag.

* Metrics starting with `uniqueness.checker.request` relate to metrics applicable to specific requests within a sub-batch,
such as the result of a request. Like the sub-batch metrics, these are also associated with the `virtualnode.source` tag.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_checker_batch_execution_time_seconds` | Timer | None | The overall time for the uniqueness checker to process a batch, inclusive of all sub-batches. |
| `corda_uniqueness_checker_batch_size` | DistributionSummary | None | The number of requests in a batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_subbatch_execution_time_seconds` | Timer | `virtualnode.source` | The time for the uniqueness checker to process a sub-batch, that is, a partition of a batch segregated by notary virtual node holding identity. |
| `corda_uniqueness_checker_subbatch_size` | DistributionSummary | `virtualnode.source` | The number of requests in a sub-batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_request_count` | Counter | `virtualnode.source`, `result.type`, `duplicate` | A count of the number of requests processed. On its own this simply duplicates information that is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context not available in the other metrics. The `result.type` tag can be used to understand the number of successful vs failed requests, and the type of failures. The `duplicate` tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result. Otherwise, it is `false`. |

#### Backing Store

The backing store is responsible for abstracting database access from the uniqueness checker, and performs all read and write
operations against the uniqueness database. These metrics also have the `virtualnode.source` tag which allows metrics to be
associated with the holding IDs of specific notary virtual nodes.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_backingstore_session_execution_time_seconds` | Timer | `virtualnode.source` | The overall execution time for a (uniqueness checker) backing store session, which includes retrieving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context. |
| `corda_uniqueness_backingstore_transaction_execution_time_seconds` | Timer | `virtualnode.source`  | The execution time for a transaction within the context of a backing store session, which excludes retrieving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, then the execution time covers the cumulative duration of all retry attempts. |
| `corda_uniqueness_backingstore_transaction_error_count` | Counter | `virtualnode.source`, `error.type` | The cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. For example, a transaction that fails up to the maximum of 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error.type`). |
| `corda_uniqueness_backingstore_transaction_attempts` | DistributionSummary | `virtualnode.source` | 	The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `uniqueness.backingstore.transaction.error.count` metric. |
| `corda_uniqueness_backingstore_db_commit_time_seconds` | Timer | `virtualnode.source` | The time taken by the backing store to commit a transaction (that is, write) to the database. Only updated if data is written to the database, so it is not cumulative across retry attempts for a given transaction. |
| `corda_uniqueness_backingstore_db_read_time_seconds` | Timer | `virtualnode.source`, `operation.name` | The time taken to perform a single read operation from the database. The existing `operation.name` tag is re-purposed to reflect the specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails`, or `getTransactionError`. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries. |

Metrics of type Timer have further metrics with the suffixes `_count`, `_max`, and `_sum` that represent the number of events,
the maximum value, and the cumulative sum of values, respectively.

In addition, the Corda metrics endpoint also includes Caffeine cache metrics (`corda_cache_*`),
Kafka producer and consumer client metrics (`corda_kafka_*`), JVM metrics (`jvm_*`), process metrics (`process_*`),
and system metrics (`system_*`) provided by the corresponding Micrometer bindings.
