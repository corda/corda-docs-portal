---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Flow Mapper"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-flow-mapper
    weight: 5000
section_menu: corda5
---

# Flow Mapper

The flow mapper acts as a gateway component in the flow engine, to ensure that requests originating from outside the
Corda cluster are deduplicated correctly. Mapper metrics give an indication of the health and performance of this component.

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
| `corda_flow_mapper_event_processing_time_seconds` | Timer | <ul><li>`flow_event`</li></ul> | The time it took to process a single message in the flow mapper. |
| `corda_flow_mapper_deduplication_count` | Counter | <ul><li>`flow_event`</li></ul> | The number of events dropped due to deduplication of start events by the mapper. |
| `corda_flow_mapper_creation_count` | Counter | <ul><li>`flow_event`</li></ul> | The number of new states being created. |
| `corda_flow_mapper_cleanup_count` | Counter | None | The number of states being cleaned up. |
| `corda_flow_mapper_event_lag` | Counter | <ul><li>`flow_event`</li></ul> | The time between a mapper event being published and processed. |
| `corda_flow_mapper_expired_session_event_count` | Counter | None | The number of expired session events dropped by the mapper. |

Tags:
* `flow_event`: The type of event that was being processed for a given metric.
