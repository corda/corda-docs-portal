---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Flow Session"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-flow-session
    weight: 6000
section_menu: corda5
---

# Flow Session

Sessions are used by flows to communicate with counterparties. Session metrics provide some insight into how peer-to-peer
communications are behaving at the level of the flow engine.

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
| `corda_flow_session_messages_incoming_count` | Counter | <ul><li>`virtualnode`</li><li>`flow_class`</li></ul> | The number of messages received by sessions. |
| `corda_flow_session_messages_outgoing_count` | Counter | <ul><li>`virtualnode`</li><li>`flow_class`</li></ul> | The number of messages sent by sessions. |

Tags:
* `virtualnode`: The short hash of the virtual node to which a metric applies.
* `flow_class`: The flow class for the metric.
