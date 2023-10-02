---
date: '2023-10-02'
version: 'Corda 5.1'
title: "UTXO Ledger"
menu:
  corda51:
    parent: corda51-cluster-metrics
    identifier: corda51-cluster-ledger
    weight: 13000
section_menu: corda51
---

# UTXO Ledger

This document outlines the metrics that enable you to monitor the {{< tooltip >}}UTXO{{< /tooltip >}} ledger performance.

The UTXO ledger is built on Corda’s flow functionality with several specialised processors that execute various operations.
Each of these processors is connected via the message bus to flows. Therefore, the most prominent performance improvements
revolve around decreasing the number of times a flow suspends, reducing the time lost to the message bus.

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
| `corda_ledger_flow_verification_time_seconds` | Timer | None | The time taken from calling transaction verification within a flow until a response is returned to the calling code. |
| `corda_ledger_verification_time_seconds` | Timer | None | The time taken from receiving an event in the verification processor to completing the event's processing. |
| `corda_ledger_verification_contract_total_time_seconds` | Timer | None | The time taken to execute contracts when verifying a transaction. |
| `corda_ledger_verification_contract_time_seconds` | Timer | <ul><li>`ledger_contract_name`</li></ul> | The time taken to execute a contract’s contract code. |
| `corda_ledger_verification_contract_count` | Counter | None | The number of executed contracts when verifying a transaction. |
| `corda_ledger_flow_persistence_time_seconds` | Timer | <ul><li>`operation_name`</li></ul> | Then time taken from calling any ledger persistence operation within a flow until a response is returned to the calling code. |
| `corda_ledger_persistence_time_seconds` | Timer | <ul><li>`ledger_type`</li><li>`operation_name`</li></ul> | The time taken from receiving an event in the ledger persistence processor to completing the event's processing. |
| `corda_serialization_amqp_serialization_time_seconds` | Timer | <ul><li>`serialized_class`</li></ul> | The time taken to serialize an object. |
| `corda_serialization_amqp_deserialization_time_seconds` | Timer | <ul><li>`serialized_class`</li></ul> | The time taken to deserialize an object. |
| `corda_flow_run_time_seconds` | Timer | <ul><li>`flow_class_name`</li></ul> | The time taken to run a subflow to completion. This is the same metric as run time for top-level flows, rather than its own independent metric. |
| `corda_ledger_backchain_resolution_chain_length` | Counter | None | The number of transaction’s resolved within a transaction’s backchain. |


Tags:
* `ledger_contract_name`: Contract name.
* `operation_name`: Operation name.
* `ledger_type`: Ledger type.
* `serialized_class`: The class being serialized.
* `flow_class_name`: Flow class name.
