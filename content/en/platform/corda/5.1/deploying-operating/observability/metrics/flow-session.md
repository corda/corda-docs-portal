---
description: "Review the metrics generated for flow sessions. Sessions are used by flows to communicate with counterparties."
date: '2023-06-14'
<<<<<<< HEAD
=======
version: 'Corda 5.1'
>>>>>>> release/platform/4.12
title: "Flow Session"
menu:
  corda51:
    parent: corda51-cluster-metrics
    identifier: corda51-cluster-flow-session
    weight: 600
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

* `virtualnode`: The short hash of the {{< tooltip >}}virtual node{{< /tooltip >}} to which a metric applies.
* `flow_class`: The flow class for the metric.
