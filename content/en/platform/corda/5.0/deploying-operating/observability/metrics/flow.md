---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Flow"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-flow
    weight: 4000
section_menu: corda5
---

# Flow

Flow metrics measure the execution of flow classes provided by the CorDapp, providing an indication of the performance
and health of the flow engine Corda uses to execute these flows.

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
| `corda_flow_run_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`flow_class`</li><li>`status`</li></ul> | The time it took for a flow to complete successfully or to produce an error. |
| `corda_flow_fiber_serialization_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_fiber_deserialization_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to serialize a flow fiber. |
| `corda_flow_start_lag_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The lag between flow start event, the REST API, and the flow processor. |
| `corda_flow_execution_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`status`</li></ul> | The time it took to execute the flow (excluding any start lag). |
| `corda_flow_event_lag_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow_event`</li></ul> | The lag between flow event publication and processing. |
| `corda_flow_event_pipeline_execution_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow.event`</li></ul> | The time it took to execute the pipeline for given flows and flow event types. |
| `corda_flow_event_fiber_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time it took to execute the fiber for a single suspension point. |
| `corda_flow_pipeline_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The total time that a flow spent processing in the pipeline, rather than queued (includes fiber execution time.) |
| `corda_flow_fiber_execution_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The total time a flow spent executing user code in the fiber. |
| `corda_flow_suspension_wait_time_seconds` | Timer | <ul><li>`flow_class`</li></ul> | The time a flow spent waiting to awake from a suspension. |
| `corda_flow_event_suspension_wait_time_seconds` | Timer | <ul><li>`flow_class`</li><li>`flow_suspension_action`</li></ul> | The time a flow spent waiting to awake from a single suspension, broken down by action. |
| `corda_flow_scheduled_wakeup_count` | Counter | None | The number of times a scheduled wakeup is published for flows. |

Tags:
* `virtualnode`: The short hash of the virtual node to which a metric applies.
* `flow_class`: The flow class for the metric.
* `status`: Indicates whether an operation succeeded or failed.
* `flow_event`: The type of event that was being processed for a given metric.
* `flow_suspension_action`: The action that triggered the flow to suspend.
