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
* Crypto worker

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
| `corda_sandbox_create_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`sandbox_type`</li></ul> | The time it took to create the sandbox. The `virtualnode` tag indicates a virtual node the sandbox applies to. The `sandbox_type` tag indicates the type of sandbox. |

#### Messaging

The messaging patterns library contains several embedded metrics that provide measurements for all workers through their Kafka consumers and producers.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_messaging_processor_time_seconds` | Timer | <ul><li>`messagepattern_type`</li><li>`messagepattern_clientid`</li><li>`operation_name`</li></ul> | The time spent in the consumer’s `onNext` or `onSnapshot` functions. The following subscription processors have this metric wrapping the calls to `onNext` functions: <ul><li>`PubSubSubscriptionImpl`</li><li>`CordaRPCSenderImpl`</li><li>`CompactedSubscriptionImpl` (`onNext` and `onSnapshot`)</li><li>`EventLogSubscriptionImpl`</li><li>`PubSubSubscriptionImpl`</li><li>`RPCSubscriptionImpl`</li><li>`StateAndEventSubscriptionImpl`</li></ul> |
| `corda_consumer_records_consumed` | Gauge | <ul><li>`messagepattern_clientid`</li><li>`partition`</li></ul> | The size of batches polled from Kafka in consumers. The `partition` tag is the partition of the Kafka topic published to or consumed from. |
| `corda_corda_consumer_poll_time_seconds` | Timer | <ul><li>`messagepattern_clientid`</li></ul> | Poll times for all Kafka consumers. These are identifiable by the `messagepatter_clientid` which includes the message pattern type, and in some instances the operation type. |
| `corda_consumer_partitioned_inmemory_store` | Gauge | <ul><li>`messagepattern_type`</li><li>`messagepattern.clientid`</li><li>`partition`</li></ul> | Measure for the number of in-memory states held in consumers with partitions. |
| `corda_consumer_compacted_inmemory_store` | Gauge | <ul><li>`messagepattern_type`</li><li>`messagepattern.clientid`</li></ul> | Measure for the number of in-memory states held in compacted consumers. |
| `corda_producer_chunks_generated` | DistributionSummary | <ul><li>`messagepattern_clientid`</li><li>`topic`</li></ul> | The number of chunks generated by Kafka producers. The `topic` tag is the name of the Kafka topic published to or consumed from. |


#### Flow

Flow metrics measure the execution of flow classes provided by the CorDapp, providing an indication of the performance
and health of the flow engine Corda uses to execute these flows.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_run_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`flow_class`</li><li>`status`</li></ul> | The time it took for a flow to complete successfully or to produce an error. The `virtualnode` tag is the short hash of the virtual node to which a metric applies. The `flow_class` tag is the flow class for the metric. The `status` tag indicates whether an operation succeeded or failed. |
| `corda_flow_fiber_serialization_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_fiber_deserialization_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_start_lag_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The lag between flow start event, the REST API, and the flow processor. |
| `corda_flow_execution_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`status`</li></ul> | The time it took to execute the flow (excluding any start lag). |
| `corda_flow_event_lag_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow_event`</li></ul> | The lag between flow event publication and processing. The `flow_event` tag is the type of event that was being processed for a given metric. |
| `corda_flow_event_pipeline_execution_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow.event`</li></ul> | The time it took to execute the pipeline for given flows and flow event types. |
| `corda_flow_event_fiber_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to execute the fiber for a single suspension point. |
| `corda_flow_pipeline_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The total time that a flow spent processing in the pipeline, rather than queued (includes fiber execution time.) |
| `corda_flow_fiber_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The total time a flow spent executing user code in the fiber. |
| `corda_flow_suspension_wait_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time a flow spent waiting to awake from a suspension. |
| `corda_flow_event_suspension_wait_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow_suspension_action`</li></ul> | The time a flow spent waiting to awake from a single suspension, broken down by action. The `flow_suspension_action` tag indicates the action that triggered the flow to suspend. |
| `corda_flow_scheduled_wakeup_count` | Counter | None | The number of times a scheduled wakeup is published for flows. |

#### Flow Mapper

The flow mapper acts as a gateway component in the flow engine, to ensure that requests originating from outside the
Corda cluster are deduplicated correctly. Mapper metrics give an indication of the health and performance of this component.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_mapper_event_processing_time_seconds` | Timer | <ul><li>`flow_event`</li></ul> | The time it took to process a single message in the flow mapper. |
| `corda_flow_mapper_deduplication_count` | Counter | <ul><li>`flow_event`</li></ul> | The number of events dropped due to deduplication of start events by the mapper. |
| `corda_flow_mapper_creation_count` | Counter | <ul><li>`flow_event`</li></ul> | The number of new states being created. |
| `corda_flow_mapper_cleanup_count` | Counter | None | The number of states being cleaned up. |
| `corda_flow_mapper_event_lag` | Counter | <ul><li>`flow_event`</li></ul> | The time between a mapper event being published and processed. |
| `corda_flow_mapper_expired_session_event_count` | Counter | None | The number of expired session events dropped by the mapper. |

#### Flow Session

Sessions are used by flows to communicate with counterparties. Session metrics provide some insight into how peer-to-peer
communications are behaving at the level of the flow engine.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_flow_session_messages_incoming_count` | Counter | <ul><li>`virtualnode`</li><li>`flow_class`</li></ul> | The number of messages received by sessions. |
| `corda_flow_session_messages_outgoing_count` | Counter | <ul><li>`virtualnode`</li><li>`flow_class`</li></ul> | The number of messages sent by sessions. |

#### Peer-to-peer Messages and Sessions

The peer-to-peer layer is responsible for delivering messages between virtual nodes.
When these virtual nodes are hosted in separate clusters, the exchange of messages occurs securely through end-to-end
authenticated sessions. The following metrics are associated with both the messages and the sessions.

| Metric                                       | Type          | Tags                                                                                                                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:---------------------------------------------|:--------------|:------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `corda_p2p_message_outbound`                 | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li><li>`message_type`</li></ul> | The number of outbound peer-to-peer data messages sent. The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message. The `message_type` tag indicates the type of the message.                                                                                                                                                                                                                                                                                                                               |
| `corda_p2p_message_outbound_replayed`        | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer data messages replayed. Messages are replayed if they are not acknowledged as delivered by the peer within a configurable time window. The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged.                                                                                                                                                                                                                                                                                                                                                 |
| `corda_p2p_message_outbound_latency_seconds` | Timer         | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The time it took for an outbound peer-to-peer message to be delivered end-to-end (from initial processing on the sender side to acknowledgement from the recipient side). The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message.                                                                                                                                                                                                                                                                       |
| `corda_p2p_message_outbound_expired`         | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The number of outbound peer-to-peer data messages that were discarded because their TTL expired. The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message.                                                                                                                                                                                                                                                                                                                                                |
| `corda_p2p_message_inbound`                  | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li><li>`message_type`</li></ul> | The number of inbound peer-to-peer data messages received. The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. The `subsystem` tag indicates the upstream component that sent the message. The `message_type` tag indicates the type of the message.                                                                                                                                                                                                                                                                                                                            |
| `corda_p2p_session_outbound_timeout`         | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer sessions that timed out (indicating communication issues with peers). Health of end-to-end sessions is monitored via heartbeat mechanism. In case of network disruption of process failures on a peer cluster, heartbeats will stop and sessions will be declared unhealthy and replaced with fresh ones. The `virtualnode_source` and `virtualnode_destination` tags indicate the source and destination virtual node of the message. The `group` tag indicates the network within which a message is exchanged. |
| `corda_p2p_session_outbound`                 | SettableGauge | None                                                                                                                                | The number of outbound peer-to-peer sessions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `corda_p2p_session_inbound`                  | SettableGauge | None                                                                                                                                | The number of inbound peer-to-peer sessions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

#### Ledger Uniqueness Checker Client Service

The ledger uniqueness checker client service metrics are from the perspective of the notarization flow running on a notary virtual node.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_ledger_uniqueness_client_run_time_seconds` | Timer | <ul><li>`result_type`</li></ul> | The time taken from requesting a uniqueness check to a response being received. The `result_type` tag is set to the specific type of uniqueness check result that was returned. |

#### Uniqueness Checker

The uniqueness checker and backing store metrics are from the perspective of uniqueness processing, which runs independently of the flow processing.

The uniqueness checker handles the business logic of uniqueness checking.
The implementation is batched at two levels and three categories of metrics are provided:

* Metrics starting with `uniqueness_checker_batch` relate to “top level” metrics, which apply to a single batch
processed by the uniqueness checker. As a batch may contain requests from different notary services and/or virtual nodes,
these metrics provide no context as to the identities of the batch being processed.

* Metrics starting with `uniqueness_checker_subbatch` relate to “sub-batch level” metrics. Each sub-batch represents
a partition for each notary virtual node identity within a batch. The virtual node identity is captured via the existing `virtualnode.source` tag.

* Metrics starting with `uniqueness_checker_request` relate to metrics applicable to specific requests within a sub-batch,
such as the result of a request. Like the sub-batch metrics, these are also associated with the `virtualnode.source` tag.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_checker_batch_execution_time_seconds` | Timer | None | The overall time for the uniqueness checker to process a batch, inclusive of all sub-batches. |
| `corda_uniqueness_checker_batch_size` | DistributionSummary | None | The number of requests in a batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_subbatch_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The time for the uniqueness checker to process a sub-batch, that is, a partition of a batch segregated by notary virtual node holding identity. |
| `corda_uniqueness_checker_subbatch_size` | DistributionSummary | <ul><li>`virtualnode_source`</li></ul> | The number of requests in a sub-batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_request_count` | Counter | <ul><li>`virtualnode_source`</li><li>`result_type`</li><li>`duplicate`</li></ul> | A count of the number of requests processed. On its own this simply duplicates information that is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context not available in the other metrics. The `result_type` tag can be used to understand the number of successful vs failed requests, and the type of failures. The `duplicate` tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result. Otherwise, it is `false`. |

#### Backing Store

The backing store is responsible for abstracting database access from the uniqueness checker, and performs all read and write
operations against the uniqueness database. These metrics also have the `virtualnode_source` tag which allows metrics to be
associated with the holding IDs of specific notary virtual nodes.


| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_uniqueness_backingstore_session_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The overall execution time for a (uniqueness checker) backing store session, which includes retrieving uniqueness database connection details, getting a database connection, as well as all database operations (both read and write) carried out within a session context. |
| `corda_uniqueness_backingstore_transaction_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul>  | The execution time for a transaction within the context of a backing store session, which excludes retrieving uniqueness database connection details and getting a database connection. If a transaction needs to be retried due to database exceptions, then the execution time covers the cumulative duration of all retry attempts. |
| `corda_uniqueness_backingstore_transaction_error_count` | Counter | <ul><li>`virtualnode_source`</li><li>`error_type`</li></ul> | The cumulative number of errors raised by the backing store when executing a transaction. This is incremented regardless of whether an expected or unexpected error is raised, and is incremented on each retry. For example, a transaction that fails up to the maximum of 10 retries with the same error will increment by 10 in total. The tags provide the context as to the affected holding identity and the specific error class name (captured by `error_type`). |
| `corda_uniqueness_backingstore_transaction_attempts` | DistributionSummary | <ul><li>`virtualnode_source`</li></ul> | 	The number of attempts that were made before a transaction ultimately succeeded. Generally, this should return 1. In the event that a transaction was unsuccessful due to reaching the maximum number of attempts, this metric is not updated and the failure would be reflected in the `corda_uniqueness_backingstore_transaction_error_count` metric. |
| `corda_uniqueness_backingstore_db_commit_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The time taken by the backing store to commit a transaction (that is, write) to the database. Only updated if data is written to the database, so it is not cumulative across retry attempts for a given transaction. |
| `corda_uniqueness_backingstore_db_read_time_seconds` | Timer | <ul><li>`virtualnode_source`</li><li>`operation_name`</li></ul> | The time taken to perform a single read operation from the database. The existing `operation_name` tag is re-purposed to reflect the specific type of read operation being performed, currently one of `getStateDetails`, `getTransactionDetails`, or `getTransactionError`. If a transaction is retried, each retry contributes independently to this metric, meaning the number is not cumulative across retries. |


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

The ledger persistence requests metrics measure the time taken to handle the ledger persistence requests.

The membership persistence requests metrics presented in this section measure:
* The time taken to handle the membership persistence requests, which included acquiring a connection and executing a transaction.
* The time taken to execute a transaction, which allows you to compare against the previous metric to determine the
percentage of time spent acquiring connections vs executing transactions.

Additionally, there are background processes occurring within the database worker, namely the reconciliations. The
reconciliations are responsible for ensuring the alignment of Kafka compacted topics with the database
(the database being the primary source of truth). The reconciliations run at regular intervals, loading in-memory database
and Kafka records, identifying the differences (delta), and synchronizing the Kafka state to match that of the database.
The reconciliations metrics listed in this section measure:

* The time taken for a reconciliation run to complete.
* The number of reconciled records per reconciliation. This could be useful to identify cases where a reconciliation run could be over-reconciling
things (for example, up-to-date Kafka records could be re-published from the database when they shouldn't).

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_db_entity_persistence_request_time_seconds` | Timer | <ul><li>`entityRequest_type`</li><li>`entityRequest_outcome`</li></ul> | The time it takes to process an entity persistence request, from the moment the request is received from Kafka. The `entityRequest.type` tag is the type of persistence request, The `entityRequest_outcome` tag is the outcome of processing a request (SUCCESS, FAILURE). |
| `corda_db_entity_persistence_request_lag_seconds` | Timer | <ul><li>`entityRequest_type`</li></ul> | The lag between the flow putting the entity persistence request to Kafka and the EntityMessageProcessor. |
| `corda_ledger_persistence_time_seconds` | Timer | <ul><li>`flowId`</li><li>`ledger_type`</li><li>`operation_name`</li></ul> | The time it takes to execute ledger transaction database request against the database. The `flowId` tag represents the flow ID to correlate with the flow. The `ledger_type` can be UTXO or CONSENSUAL. The `operation_name` tag is the persistence operation. |
| `corda_membership_persistence_transaction_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time it takes to execute membership persistence transactions. Excludes time spent acquiring a database connection. |
| `corda_membership_persistence_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time it takes to execute membership persistence handlers. Includes time taken to get database connection and execute the transaction. The `operation_name` tag is the MGM persistence request name/type. The `group` tag is the membership group within which peer-to-peer communication happens. |
| `corda_db_reconciliation_run_time_seconds` | Timer | <ul><li>`reconciliation_reconciler_type`</li><li>`reconciliation_outcome`</li></ul> | The time needed for a full reconciliation run. The `reconciliation_reconciler_type` tag is the type of reconciler that run, for example, CPI metadata, virtual node metadata. The `reconciliation_outcome` tag is the outcome of a reconciliation run (SUCCESS, FAILURE). |
| `corda_db_reconciliation_records_count` | Counter | <ul><li>`reconciliation_reconciler_type`</li><li>`reconciliation_outcome`</li></ul></ul> | The number of reconciled records for a reconciliation run. |

#### Membership Worker

The membership worker is responsible for the processing of application network functionality either on behalf of an MGM,
a network member, or both. For an MGM, examples of this application functionality include:
* handling incoming registration requests
* network management
* ensuring the network participants are all in sync with the latest network data

For a network member, examples include:
* registering with an MGM to join a network
* managing network data sent from the MGM
* periodically syncing network data with the MGM

The timer metrics of the membership worker focus on the areas mentioned above. Specifically, the timer metrics cover:
* each stage of registration on both the MGM and membership side
* general membership actions (which at the moment only include the distribution of network data by the MGM),
* synchronisation of network data handling on both the MGM and member sides

These metrics are tagged with the name of the handler so that you can observe at a low-level exactly where time is spent
across different processes. These handler names are tagged as the operation name. They are also tagged with the short
hash ID and the group ID of the virtual node the operation is performed on behalf of in order to determine if certain
virtual nodes or groups are taking longer than others to process.

The membership worker also includes a single gauge metric which shows the size of the network member list held in memory
at any point. It is useful to compare any changes in the performance returned by the timer metrics to the size of the
member list at the time to see if timings could be impacted by a growing network. The gauge metrics are also tagged by
virtual node short hash and group ID so that it is possible to see the overall size of the member lists held in memory
but also view it per application network.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_membership_actions_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time spent on membership actions. The `operation_name` tag is the name of the operation that the metric is related to. For example, `DistributeMemberInfo`, `StartRegistration`, `QueryMemberInfo`, and so on. The `group` tag is the membership group ID of the virtual node performing an operation or being monitored. It can also appear as `not_applicable` when a membership group identifier is not accessible when the metric was collected. The `virtualnode` tag is the virtual node short hash of the virtual node performing an operation or being monitored. This can also appear as `not_applicable` when a virtual node identifier was not accessible when the metric was collected.  |
| `corda_membership_registration_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | Registration is broken down into a series of stages, each with its own handler. This metric measures the time taken to execute each stage.  |
| `corda_membership_sync_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | Measures how long it takes for each stage of synchronisation to complete. Synchronisation is split between different handler stages. It is processed on the MGM side and the network data package in constructed, and on the member side it is validated and persisted.  |
| `membership_memberlist_cache_size` | Gauge | <ul><li>`group`</li><li>`virtualnode`</li></ul> | Gauge of the member list cache size to monitor how the cache size grows or shrinks. |

#### Crypto Worker

The crypto worker is responsible for handling crypto operations in Corda, such as signing. It is the only worker that
hosts keys owned by the Corda cluster, as well as keys owned by the virtual nodes required for crypto operations.

The keys of the virtual nodes are stored in dedicated databases per virtual node, while the keys of the Corda cluster
are stored in a dedicated database for cluster keys. In addition to the database, there are caches universal to all
virtual nodes that hold the keys in memory for faster lookup.

The crypto requests could be categorized into flow requests and everything else. Flow requests are, seemingly,
of more importance in terms of metrics as they are directly involved in flows lifecycle.
With the crypto worker metrics, you can measure the below crypto requests within the crypto worker:

* Flow-crypto requests, which consist of the operations:
  * `SigningService.sign`: The `sign` operation is performed on the flow side and sends to the crypto worker the bytes
    to be signed along with the public part of the signing key and the signature spec.
    On the crypto worker side, the crypto worker attempts to find the key in the keys hosted for the virtual node that
    sent the request and if found, it signs the bytes and returns the signature.
    Regarding metrics for the `sign` operation, the following metrics pertain to the time taken to handle the entire
    `sign` request. Additionally, there are more detailed metrics related to key caches and the 'sign' operation itself.
  * `SigningService.findMySigningKeys`: The `findMySigningKeys` operation sends a set of keys to the crypto worker,
    which then filters and returns the keys owned by the calling virtual node.
    Regarding metrics for the `findMySigningKeys` operation, the following metrics are related to the time taken to
    handle the entire `findMySigningKeys` request. Additionally, there are metrics related to key caches.

* Admin or other requests, which involve operations such as creating a new key (pair) for a virtual node, or list
information about the keys owned by a virtual node. Regarding metrics for these requests, the following metrics pertain
to the time taken to handle the requests as a whole.

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_crypto_flow_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested by flow operations. |
| `corda_crypto_processor_execution_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken by crypto worker to process operations requested from other endpoints. |
| `corda_crypto_wrapping_key_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken for wrapping key creation in crypto operations. The `tenant` tag is the identifier of a tenant: it's either a virtual node identifier or cluster level tenant ID. |
| `corda_entity_manager_factory_creation_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to create entity manager factories. |
| `corda_crypto_sign_time_seconds` | Timer | <ul><li>`signature_spec`</li></ul> | The time taken for crypto signing. The `signature_spec` identifies the signature signing scheme name to create signatures during crypto signing operations. |
| `corda_crypto_sigining_key_lookup_time_seconds` | Timer | <ul><li>`lookup_method`</li></ul> | The time taken for crypto signing key lookup. The `lookup_method` tag indicates the method used to look up signing key IDs, either public key IDs or public key short IDs. |
| `corda_crypto_signing_repository_get_instance_time_seconds` | Timer | <ul><li>`tenant`</li></ul> | The time taken to get crypto signing repository instances. |
| `corda_crypto_get_owned_key_record_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`publickey_type`</li></ul> | The time taken to look up tenant’s owned keys. The `publickey_type` is the type of public key used in sign operations. |
| `corda_crypto_cipher_scheme_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto cipher scheme encoding and decoding operations. |
| `corda_crypto_signature_spec_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | The time taken for crypto signature spec operations including deserializing wire objects to signature spec and vice versa. |
