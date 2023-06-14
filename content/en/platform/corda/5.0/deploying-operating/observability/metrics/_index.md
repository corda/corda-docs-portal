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
* general membership actions (which at the moment only include the distribution of network data by the MGM)
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
