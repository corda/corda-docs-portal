---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Database Worker"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-db-worker
    weight: 10000
section_menu: corda5
---

# Database Worker

The database worker is the sole worker with access to the database (apart from the crypto worker, which has its
own dedicated database). As a result, the activities carried out within the database worker pertain to the database.

The database worker is responsible for handling and serving persistence requests originating from various Corda worker types,
such as the flow worker or the MGM worker. The flow persistence requests metrics presented in this section measure:

* The time taken to handle the flow persistence requests.
* The time the flow persistence requests remained on Kafka, from the moment they were added by flows until they were received
  by the database worker (Kafka lag).

The ledger persistence requests metrics measure the time needed to execute the ledger transaction database requests against the database.

The membership persistence requests metrics presented in this section measure:
* The time taken to handle the membership persistence requests, which included acquiring a connection and executing a transaction.
* The time taken to execute a transaction, which allows you to compare against the previous metric to determine the
  percentage of time spent acquiring connections vs executing transactions.

Additionally, there are background processes occurring within the database worker, namely the reconciliations. The
reconciliations are responsible for ensuring the alignment of Kafka compacted topics with the database
(the database being the primary source of truth). The reconciliations run at regular intervals, loading in-memory database
and Kafka records, identifying the differences, and synchronizing the Kafka state to match that of the database.
The reconciliations metrics listed in this section measure:

* The time taken for a reconciliation run to complete.
* The number of reconciled records per reconciliation. This could be useful to identify cases where a reconciliation run could be over-reconciling
  things (for example, up-to-date Kafka records could be re-published from the database when they shouldn't).

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
| `corda_db_entity_persistence_request_time_seconds` | Timer | <ul><li>`entityRequest_type`</li><li>`entityRequest_outcome`</li></ul> | The time it takes to process an entity persistence request, from the moment the request is received from Kafka. |
| `corda_db_entity_persistence_request_lag_seconds` | Timer | <ul><li>`entityRequest_type`</li></ul> | The lag between the flow putting the entity persistence request to Kafka and the EntityMessageProcessor. |
| `corda_ledger_persistence_time_seconds` | Timer | <ul><li>`flowId`</li><li>`ledger_type`</li><li>`operation_name`</li></ul> | The time it takes to execute ledger transaction database request against the database. |
| `corda_membership_persistence_transaction_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time it takes to execute membership persistence transactions. Excludes time spent acquiring a database connection. |
| `corda_membership_persistence_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time it takes to execute membership persistence handlers. Includes time taken to get database connection and execute the transaction. |
| `corda_db_reconciliation_run_time_seconds` | Timer | <ul><li>`reconciliation_reconciler_type`</li><li>`reconciliation_outcome`</li></ul> | The time needed for a full reconciliation run. |
| `corda_db_reconciliation_records_count` | Counter | <ul><li>`reconciliation_reconciler_type`</li><li>`reconciliation_outcome`</li></ul></ul> | The number of reconciled records for a reconciliation run. |
Tags:
* `entityRequest.type`: The type of persistence request.
* `entityRequest_outcome`: The outcome of processing a request (SUCCESS, FAILURE).
* `flowId`: The flow ID to correlate with the flow.
* `ledger_type`: It can be UTXO or CONSENSUAL.
* `operation_name`: The MGM persistence request name/type.
* `group`: The membership group within which peer-to-peer communication happens.
* `virtualnode`: The virtual node identity.
* `reconciliation_reconciler_type`: The type of reconciler that run, for example, CPI metadata, virtual node metadata.
* `reconciliation_outcome`: The outcome of a reconciliation run (SUCCESS or FAILURE).
