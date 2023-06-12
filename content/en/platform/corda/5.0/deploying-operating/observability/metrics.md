---
date: '2023-05-10'
version: 'Corda 5.0'
title: "Metrics"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-metrics
    weight: 2000
section_menu: corda5
---

# Metrics

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
* Sandbox
* Messaging
* Flow
* Flow mapper
* Flow session
* Peer-to-peer messages and sessions
* Ledger uniqueness checker client service
* Uniqueness checker
* Backing store
* Database worker
* Membership worker
* Crypto processor

#### HTTP Requests

The REST server acts as a mediator, converting HTTP requests into messages that can be consumed by the Corda workers.
Two metrics offer insights into the HTTP requests: the cumulative count of requests received over a specific duration,
and the processing time for each request. There is a maximum time limit, or timeout, imposed on the processing of each
HTTP request. If a timeout is reached, an error message is dispatched to the HTTP client.

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
| `corda_http_server_request_total` | Counter | <ul><li>`address`</li></ul> | The number of HTTP requests. The `address` tag is the address that the metric is applicable to. |
| `corda_http_server_request_time_seconds` | Timer | <ul><li>`address`</li></ul> | HTTP requests processing time; the `address` tag is the address to which the metric is applicable. |

#### Sandbox

Corda 5 sandbox is used to support Corda's stability and security when operating in a highly-available and multi-tenant
configuration, allowing a safe execution environment within a JVM process that provides isolation for CorDapps.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_sandbox_create_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`sandbox.type`</li></ul> | The time it took to create the sandbox. The `virtualnode` tag indicates a virtual node the sandbox applies to. The `sandbox.type` tag indicates the type of sandbox. |

#### Messaging

The messaging patterns library contains several embedded metrics that provide measurements for all workers through their Kafka consumers and producers.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_messaging_processor_time_seconds` | Timer | <ul><li>`messagepattern.type`</li><li>`messagepattern.clientid`</li><li>`operation.name`</li></ul> | The time spent in the consumer’s `onNext` or `onSnapshot` functions. The following subscription processors have this metric wrapping the calls to `onNext` functions: <ul><li>`PubSubSubscriptionImpl`</li><li>`CordaRPCSenderImpl`</li><li>`CompactedSubscriptionImpl` (`onNext` and `onSnapshot`)</li><li>`EventLogSubscriptionImpl`</li><li>`PubSubSubscriptionImpl`</li><li>`RPCSubscriptionImpl`</li><li>`StateAndEventSubscriptionImpl`</li></ul> |
| `corda_consumer_records_consumed` | Gauge | <ul><li>`messagepattern.clientid`</li><li>`partition`</li></ul> | The size of batches polled from Kafka in consumers. The `partition` tag is the partition of the Kafka topic published to or consumed from. |
| `corda_corda_consumer_poll_time_seconds` | Timer | <ul><li>`messagepattern.clientid`</li></ul> | Poll times for all Kafka consumers. These are identifiable by the `messagepatter.clientid` which includes the message pattern type, and in some instances the operation type. |
| `corda_consumer_partitioned_inmemory_store` | Gauge | <ul><li>`messagepattern.type`</li><li>`messagepattern.clientid`</li><li>`partition`</li></ul> | Measure for the number of in-memory states held in consumers with partitions. |
| `corda_consumer_compacted_inmemory_store` | Gauge | <ul><li>`messagepattern.type`</li><li>`messagepattern.clientid`</li></ul> | Measure for the number of in-memory states held in compacted consumers. |
| `corda_producer_chunks_generated` | DistributionSummary | <ul><li>`messagepattern.clientid`</li><li>`topic`</li></ul> | The number of chunks generated by Kafka producers. The `topic` tag is the name of the Kafka topic published to or consumed from. |


#### Flow

Flow metrics measure the execution of flow classes provided by the CorDapp, providing an indication of the performance
and health of the flow engine Corda uses to execute these flows.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_run_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`flow.class`</li><li>`status`</li></ul> | The time it took for a flow to complete successfully or to produce an error. The `virtualnode` tag is the short hash of the virtual node to which a metric applies. The `flow.class` tag is the flow class for the metric. The `status` tag indicates whether an operation succeeded or failed. |
| `corda_flow_fiber_serialization_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_fiber_deserialization_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_start_lag_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The lag between flow start event, the REST API, and the flow processor. |
| `corda_flow_execution_time_seconds` | Timer | <ul><li>`flow.class`</li><li>`status`</li></ul> | The time it took to execute the flow (excluding any start lag). |
| `corda_flow_event_lag_seconds` | Timer | <ul><li>`flow.class`</li><li>`flow.event`</li></ul> | The lag between flow event publication and processing. The `flow.event` tag is the type of event that was being processed for a given metric. |
| `corda_flow_event_pipeline_execution_time_seconds` | Timer | <ul><li>`flow.class`</li><li>`flow.event`</li></ul> | The time it took to execute the pipeline for given flows and flow event types. |
| `corda_flow_event_fiber_execution_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The time it took to execute the fiber for a single suspension point. |
| `corda_flow_pipeline_execution_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The total time that a flow spent processing in the pipeline, rather than queued (includes fiber execution time.) |
| `corda_flow_fiber_execution_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The total time a flow spent executing user code in the fiber. |
| `corda_flow_suspension_wait_time_seconds` | Timer | <ul><li>`flow.class`</li></ul> | The time a flow spent waiting to awake from a suspension. |
| `corda_flow_event_suspension_wait_time_seconds` | Timer | <ul><li>`flow.class`</li><li>`flow.suspension.action`</li></ul> | The time a flow spent waiting to awake from a single suspension, broken down by action. The `flow.suspension.action` tag indicates the action that triggered the flow to suspend. |
| `corda_flow_scheduled_wakeup_count` | Counter | None | The number of times a scheduled wakeup is published for flows. |

#### Flow Mapper

The flow mapper acts as a gateway component in the flow engine, to ensure that requests originating from outside the
Corda cluster are deduplicated correctly. Mapper metrics give an indication of the health and performance of this component.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_mapper_event_processing_time_seconds` | Timer | <ul><li>`flow.event`</li></ul> | The time it took to process a single message in the flow mapper. |
| `corda_flow_mapper_deduplication_count` | Counter | <ul><li>`flow.event`</li></ul> | The number of events dropped due to deduplication of start events by the mapper. |
| `corda_flow_mapper_creation_count` | Counter | <ul><li>`flow.event`</li></ul> | The number of new states being created. |
| `corda_flow_mapper_cleanup_count` |Counter | None | The number of states being cleaned up. |
| `corda_flow_mapper_event_lag` | Counter | <ul><li>`flow.event`</li></ul> | The time between a mapper event being published and processed. |
| `corda_flow_mapper_expired_session_event_count` | Counter | None | The number of expired session events dropped by the mapper. |

#### Flow Session

Sessions are used by flows to communicate with counterparties. Session metrics provide some insight into how peer-to-peer
communications are behaving at the level of the flow engine.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_session_messages_incoming_count` | Counter | <ul><li>`virtualnode`</li><li>`flow.class`</li></ul> | The number of messages received by sessions. |
| `corda_flow_session_messages_outgoing_count` | Counter | <ul><li>`virtualnode`</li><li>`flow.class`</li></ul> | The number of messages sent by sessions. |

#### Peer-to-peer Messages and Sessions

The peer-to-peer layer is responsible for delivering messages between virtual nodes.
When these virtual nodes are hosted in separate clusters, the exchange of messages occurs securely through end-to-end
authenticated sessions. The following metrics are associated with both the messages and the sessions.

| Metric                                       | Type          | Tags                                                                                                                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:---------------------------------------------|:--------------|:------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `corda_p2p_message_outbound`                 | Counter       | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li><li>`subsystem`</li><li>`message.type`</li></ul> | The number of outbound peer-to-peer data messages sent. The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message. The `message.type` tag indicates the type of the message.                                                                                                                                                                                                                                                                                                                               |
| `corda_p2p_message_outbound_replayed`        | Counter       | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer data messages replayed. Messages are replayed if they are not acknowledged as delivered by the peer within a configurable time window. The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged.                                                                                                                                                                                                                                                                                                                                                 |
| `corda_p2p_message_outbound_latency_seconds` | Timer         | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The time it took for an outbound peer-to-peer message to be delivered end-to-end (from initial processing on the sender side to acknowledgement from the recipient side). The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message.                                                                                                                                                                                                                                                                       |
| `corda_p2p_message_outbound_expired`         | Counter       | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The number of outbound peer-to-peer data messages that were discarded because their TTL expired. The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message.                                                                                                                                                                                                                                                                                                                                                |
| `corda_p2p_message_inbound`                  | Counter       | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li><li>`subsystem`</li><li>`message.type`</li></ul> | The number of inbound peer-to-peer data messages received. The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message. The `message.type` tag indicates the type of the message.                                                                                                                                                                                                                                                                                                                            |
| `corda_p2p_session_outbound_timeout`         | Counter       | <ul><li>`virtualnode.source`</li><li>`virtualnode.destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer sessions that timed out (indicating communication issues with peers). Health of end-to-end sessions is monitored via heartbeat mechanism. In case of network disruption of process failures on a peer cluster, heartbeats will stop and sessions will be declared unhealthy and replaced with fresh ones. The `virtualnode.source` and `virtualnode.destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. |
| `corda_p2p_session_outbound`                 | SettableGauge | None                                                                                                                                | The number of outbound peer-to-peer sessions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `corda_p2p_session_inbound`                  | SettableGauge | None                                                                                                                                | The number of inbound peer-to-peer sessions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

#### Ledger Uniqueness Checker Client Service

The ledger uniqueness checker client service metrics are from the perspective of the notarization flow running on a notary virtual node.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_ledger_uniqueness_client_run_time_seconds` | Timer | <ul><li>`result.type`</li></ul> | The time taken from requesting a uniqueness check to a response being received. The `result.type` tag is set to the specific type of uniqueness check result that was returned. |

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
| `corda_uniqueness_checker_subbatch_execution_time_seconds` | Timer | <ul><li>`virtualnode.source`</li></ul> | The time for the uniqueness checker to process a sub-batch, that is, a partition of a batch segregated by notary virtual node holding identity. |
| `corda_uniqueness_checker_subbatch_size` | DistributionSummary | <ul><li>`virtualnode.source`</li></ul> | The number of requests in a sub-batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_request_count` | Counter | <ul><li>`virtualnode.source`</li><li>`result.type`</li><li>`duplicate`</li></ul> | A count of the number of requests processed. On its own this simply duplicates information that is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context not available in the other metrics. The `result.type` tag can be used to understand the number of successful vs failed requests, and the type of failures. The `duplicate` tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result. Otherwise, it is `false`. |

#### Backing Store

The backing store is responsible for abstracting database access from the uniqueness checker, and performs all read and write
operations against the uniqueness database. These metrics also have the `virtualnode.source` tag which allows metrics to be
associated with the holding IDs of specific notary virtual nodes.


| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_backingstore_session_execution_time_seconds` | Timer | <ul><li>`virtualnode.source`</li></ul> | The overall execution time for a (uniqueness checker) backing store session, which includes retrieving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context. |
| `corda_uniqueness_backingstore_transaction_execution_time_seconds` | Timer | <ul><li>`virtualnode.source`</li></ul>  | The execution time for a transaction within the context of a backing store session, which excludes retrieving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, then the execution time covers the cumulative duration of all retry attempts. |
| `corda_uniqueness_backingstore_transaction_error_count` | Counter | <ul><li>`virtualnode.source`</li><li>`error.type`</li></ul> | The cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. For example, a transaction that fails up to the maximum of 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error.type`). |
| `corda_uniqueness_backingstore_transaction_attempts` | DistributionSummary | <ul><li>`virtualnode.source`</li></ul> | 	The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `uniqueness.backingstore.transaction.error.count` metric. |
| `corda_uniqueness_backingstore_db_commit_time_seconds` | Timer | <ul><li>`virtualnode.source`</li></ul> | The time taken by the backing store to commit a transaction (that is, write) to the database. Only updated if data is written to the database, so it is not cumulative across retry attempts for a given transaction. |
| `corda_uniqueness_backingstore_db_read_time_seconds` | Timer | <ul><li>`virtualnode.source`</li><li>`operation.name`</li></ul> | The time taken to perform a single read operation from the database. The existing `operation.name` tag is re-purposed to reflect the specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails`, or `getTransactionError`. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries. |


Metrics of type Timer have further metrics with the suffixes `_count`, `_max`, and `_sum` that represent the number of events,
the maximum value, and the cumulative sum of values, respectively.

In addition, the Corda metrics endpoint also includes Caffeine cache metrics (`corda_cache_*`),
Kafka producer and consumer client metrics (`corda_kafka_*`), JVM metrics (`jvm_*`), process metrics (`process_*`),
and system metrics (`system_*`) provided by the corresponding Micrometer bindings.

#### Database Worker

The database worker is the sole worker with access to the database (apart from the crypto worker, which has its
own dedicated database). As a result, the activities carried out within the database worker pertain to the database.

The database worker is responsible for handling and serving persistence requests originating from various Corda worker types,
such as the flow worker or the MGM worker. The flow persistence requests metrics presented in this section measure:

* The time taken to handle the flow persistence requests.
* The time the flow persistence requests remained on Kafka, from the moment they were added by flows until they were received
by the database worker (Kafka lag).

Additionally, there are background processes occurring within the database worker, namely the reconciliations. The
reconciliations are responsible for ensuring the alignment of Kafka compacted topics with the database
(the database being the primary source of truth). The reconciliations run at regular intervals, loading in-memory database
and Kafka records, identifying the differences (delta), and synchronizing the Kafka state to match that of the database.
The reconciliations metrics listed in this section measure:

* The time taken for a reconciliation run to complete.
* The number of reconciled records per reconciliation. This could be useful to identify cases where you could be over-reconciling
things, that is, up-to-date Kafka records could be re-published from the database when they shouldn't.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_ledger_persistence_time_seconds` | Timer | <ul><li>`flowId`</li><li>`ledger.type`</li><li>`operation.name`</li></ul> | The time it takes to execute ledger transaction database request against the database. The `flowId` tag represents the flow ID to correlate with the flow. The `ledger.type` can be UTXO or CONSENSUAL. The `operation.name` tag is the persistence operation. |
| `corda_db_entity_persistence_request_time_seconds` | Timer | <ul><li>`entityRequest.type`</li><li>`entityRequest.outcome`</li></ul> | The time it takes to process an entity persistence request, from the moment the request is received from Kafka. The `entityRequest.type` tag is the type of persistence request, The `entityRequest.outcome` tag is the outcome of processing a request (SUCCESS, FAILURE). |
| `corda_db_entity_persistence_request_lag_seconds` | Timer | <ul><li>`entityRequest.type`</li></ul> | The lag between the flow putting the entity persistence request to Kafka and the EntityMessageProcessor. |
| `corda_db_reconciliation_run_time_seconds` | Timer | <ul><li>`reconciliation.reconciler.type`</li><li>`reconciliation.outcome`</li></ul> | The time needed for a full reconciliation run. The `reconciliation.reconciler.type` tag is the type of reconciler that run, for example, CPI metadata, virtual node metadata. The `reconciliation.outcome` tag is the outcome of a reconciliation run (SUCCESS, FAILURE). |
| `corda_db_reconciliation_records_count` | Counter | <ul><li>`reconciliation.reconciler.type`</li><li>`reconciliation.outcome`</li></ul></ul> | The number of reconciled records for a reconciliation run. |
| `corda_membership_persistence_handler_time_seconds` | Timer | <ul><li>`operation.name`</li><li>`group`</li></ul> | The time it takes to execute membership persistence handlers. Includes time to get database connection and execute the transaction. The `operation.name` tag is the MGM persistence request name/type. The `group` tag is the membership group within which peer-to-peer communication happens. |

#### Membership Worker

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| corda_persistence_transaction_time_seconds | Timer | <ul><li></li></ul> | The time it takes for a membership persistence transaction to complete. |
| corda_registration_handler_time_seconds | Timer | <ul><li></li></ul> | The time taken by each stage of network registration. |
| corda_actions_handler_time_seconds | Timer | <ul><li></li></ul> | The time taken by each membership actions handler, for example, distribute network data. |
| corda_sync_handler_time_seconds | Timer | <ul><li></li></ul> | The time it takes to execute each stage of network synchronisation between members and the MGM. |
| corda_memberlist_cache_size | Gauge | <ul><li></li></ul> | Metric to capture the changes in group size. |

#### Crypto Processor

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_crypto_flow_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested by flow operations. |
| `corda_crypto_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested from other endpoints. |
| `corda_crypto_wrapping_key_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken for wrapping key creation in crypto operations. The `tenant` tag is the identifier of a tenant: it's either a virtual node identifier or cluster level tenant ID. |
| `corda_entity_manager_factory_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to create entity manager factories. |
| `corda_crypto_sign_time_seconds` | Timer | <ul><li>`signature_spec`</li></ul> | The time taken for crypto signing. The `signature_spec` identifies the signature signing scheme name to create signatures during crypto signing operations. |
| `corda_crypto_sigining_key_lookup_time_seconds` | Timer | <ul><li>`lookup_method`</li></ul> | The time taken for crypto signing key lookup. The `lookup_method` tag indicates the method used to look up signing key hashes, either public key hashes or public key short hashes. |
| `corda_crypto_signing_repository_get_instance_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to get crypto signing repository instances. |
| `corda_crypto_get_owned_key_record_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`publickey_type`</li></ul> | The time taken to look up tenant’s owned keys. The `publickey_type` is the type of public key used in sign operations. |
| `corda_crypto_cipher_scheme_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto cipher scheme encoding and decoding operations. |
| `corda_crypto_signature_spec_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto signature spec operations including deserializing wire objects to signature spec and vice versa. |
