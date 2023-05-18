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

The following Corda-specific metrics are exported:

| Metric | Type | Description |
| :----------- | :----------- | :----------- |
| `corda_http_server_request` | Counter | The number of HTTP requests. |
| `corda_http_server_request_time` | Timer | HTTP requests time. |
| `corda_sandbox_create_time` | Timer | The time it took to create the sandbox. |
| `corda_messaging_processor_time` | Timer | The time it took to execute a message pattern processor. |
| `corda_flow_run_time_seconds` | Timer | The time it took for a flow to complete successfully or to produce an error. |
| `corda_flow_fiber_serialization_time` | Timer | Metric for flow fiber serialization. |
| `corda_flow_fiber_deserialization_time` | Timer | Metric for flow fiber deserialization. |
| `corda_p2p_message_outbound` | Counter | The number of outbound peer-to-peer data messages sent. |
| `corda_p2p_message_outbound_replayed` | Counter | The number of outbound peer-to-peer data messages replayed. |
| `corda_p2p_message_outbound_latency` | Timer | The time it took for an outbound peer-to-peer message to be delivered end-to-end (from initial processing to acknowledgement). |
| `corda_p2p_message_outbound_expired` | Counter | The number of outbound peer-to-peer data messages that were discarded because their TTL expired. |
| `corda_p2p_message_inbound` | Counter | The number of inbound peer-to-peer data messages received. |
| `corda_p2p_session_outbound_timeout` | Counter | The number of outbound peer-to-peer sessions that timed out (indicating communication issues with peers). |
| `corda_p2p_session_outbound` | SettableGauge | The number of outbound peer-to-peer sessions. |
| `corda_p2p_session_inbound` | SettableGauge | The number of inbound peer-to-peer sessions. |
| `corda_ledger_uniqueness_client_run_time` | Timer | The time taken from requesting a uniqueness check to a response being received from the perspective of a client (requesting) node. |
| `corda_uniqueness_checker_batch_execution_time` | Timer | The overall time for the uniqueness checker to process a batch, inclusive of all sub-batches. |
| `corda_uniqueness_checker_batch_size` | DistributionSummary | The number of requests in a batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_subbatch_execution_time` | Timer | The time for the uniqueness checker to process a sub-batch, that is, a partition of a batch segregated by notary virtual node holding identity. |
| `corda_uniqueness_checker_subbatch_size` | DistributionSummary | The number of requests in a sub-batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_request_count` | Counter | Cumulative number of requests processed by the uniqueness checker, irrespective of batch. |
| `corda_uniqueness_backingstore_session_execution_time` | Timer | The overall execution time for a (uniqueness checker) backing store session, which includes retrieving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context. |
| `corda_uniqueness_backingstore_transaction_execution_time` | Timer | The execution time for a transaction within the context of a backing store session, which excludes retrieving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, then the execution time covers the cumulative duration of all retry attempts. |
| `corda_uniqueness_backingstore_transaction_error_count` | Counter | Cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. |
| `corda_uniqueness_backingstore_transaction_attempts` | DistributionSummary | The number of attempts that were made by the backing store before a transaction ultimately succeeded. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated. |
| `corda_uniqueness_backingstore_db_commit_time` | Timer | The time taken by the backing store to commit a transaction (that is, write) to the database. Only updated if data is written to the database, so it is not cumulative across retry attempts for a given transaction. |
| `corda_uniqueness_backingstore_db_read_time` | Timer | The time taken by the backing store to perform a single read operation from the database. |



Metrics of type Timer have further metrics with the suffixes `_count`, `_max`, and `_sum` that represent the number of events,
the maximum value, and the cumulative sum of values, respectively.

In addition, the Corda metrics endpoint also includes Caffeine cache metrics (`corda_cache_*`),
Kafka producer and consumer client metrics (`corda_kafka_*`), JVM metrics (`jvm_*`), process metrics (`process_*`),
and system metrics (`system_*`) provided by the corresponding Micrometer bindings.
