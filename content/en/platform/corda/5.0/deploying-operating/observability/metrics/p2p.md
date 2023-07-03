---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Peer-to-peer Messages and Sessions"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-p2p
    weight: 6000
section_menu: corda5
---

# Peer-to-peer Messages and Sessions

The peer-to-peer layer is responsible for delivering messages between virtual nodes.
When these virtual nodes are hosted in separate clusters, the exchange of messages occurs securely through end-to-end
authenticated sessions. The following metrics are associated with both the messages and the sessions.

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
| `corda_p2p_message_outbound`                 | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li><li>`message_type`</li></ul> | The number of outbound peer-to-peer data messages sent. |
| `corda_p2p_message_outbound_replayed`        | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer data messages replayed. Messages are replayed if they are not acknowledged as delivered by the peer within a configurable time window. |
| `corda_p2p_message_outbound_latency_seconds` | Timer         | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The time it took for an outbound peer-to-peer message to be delivered end-to-end (from initial processing on the sender side to acknowledgement from the recipient side) |
| `corda_p2p_message_outbound_expired`         | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li></ul>                        | The number of outbound peer-to-peer data messages that were discarded because their TTL expired. |
| `corda_p2p_message_inbound`                  | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li><li>`subsystem`</li><li>`message_type`</li></ul> | The number of inbound peer-to-peer data messages received. |
| `corda_p2p_session_outbound_timeout`         | Counter       | <ul><li>`virtualnode_source`</li><li>`virtualnode_destination`</li><li>`group`</li></ul>                                            | The number of outbound peer-to-peer sessions that timed out (indicating communication issues with peers). Health of end-to-end sessions is monitored via heartbeat mechanism. In case of network disruption of process failures on a peer cluster, heartbeats will stop and sessions will be declared unhealthy and replaced with fresh ones. |
| `corda_p2p_session_outbound`                 | SettableGauge | None                                                                                                                                | The number of outbound peer-to-peer sessions. |
| `corda_p2p_session_inbound`                  | SettableGauge | None                                                                                                                                | The number of inbound peer-to-peer sessions.  |

Tags:
* `virtualnode_source`: The source virtual node of the message.
* `virtualnode_destination`: The destination virtual node of the message.
* `group`: The network within which a message is exchanged.
* `subsystem`: The upstream component that sent the message.
* `message_type`: The type of the message.
