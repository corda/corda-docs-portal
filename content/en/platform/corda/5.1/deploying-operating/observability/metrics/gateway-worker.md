---
description: "Review the metrics generated for the gateway worker. The gateway worker is responsible for sending outbound messages to virtual nodes located in different clusters and receiving inbound messages from virtual nodes within different clusters."
date: '2023-08-10'
version: 'Corda 5.1'
title: "Gateway Worker"
menu:
  corda51:
    parent: corda51-cluster-metrics
    identifier: corda51-cluster-gateway-worker
    weight: 700
section_menu: corda51
---

# Gateway Worker

The P2P {{< tooltip >}}gateway worker{{< /tooltip >}} is tasked with sending outbound messages to virtual nodes located in different clusters and receiving inbound messages from virtual nodes within different clusters. To accomplish this, a gateway worker establishes {{< tooltip >}}TLS{{< /tooltip >}} connections with gateway workers in other clusters and exchanges messages through HTTPS requests.

In the outbound direction, internal components within the cluster forward messages intended for the gateway worker through a message bus (for example, Kafka). Similarly, in the inbound direction, the gateway worker forwards any messages received via HTTPS from other clusters to the local cluster through the message bus.

The P2P gateway worker is additionally tasked with conducting certificate {{< tooltip >}}revocation checks{{< /tooltip >}}. These checks are carried out either as part of the TLS handshake with other gateway workers or on behalf of other components within the internal network zone of the cluster that cannot reach out to the public Internet. The gateway worker receives requests to perform these revocation checks and returns the results via a message bus.

You can observe the behavior of these functions using the following metrics: rate or latency of inbound/outbound requests, number of inbound/outbound TLS connections, and rate or latency of revocation checks.

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
| `corda_p2p_gateway_inbound_request_time_seconds` | Timer | <ul><li>`response.type`</li><li>`endpoint.source`</li></ul> | The latency and the number of requests from a gateway worker to peer gateway workers in other clusters. |
| `corda_p2p_gateway_outbound_request_time_seconds` | Timer | <ul><li>`response.type`</li><li>`endpoint.destination`</li></ul> | The number of incoming requests from peer gateway workers in other clusters and the time it took to process them. |
| `corda_p2p_gateway_inbound_tls_connections_count` | Counter | <ul><li>`connection.result`</li><li>`endpoint.source`</li></ul> | The number of inbound TLS connections from other gateway workers. Connections are kept open while there is activity. |
| `corda_p2p_gateway_outbound_tls_connections_count` | Counter | <ul><li>`connection.result`</li><li>`endpoint.destination`</li></ul> | The number of outbound TLS connections from other gateway workers. Connections are kept open while there is activity. |
| `corda_p2p_gateway_cert_revocation_check_time_seconds` | Timer | None | The number of certificate revocation check requests and the time it took to process them. These requests are sent to the gateway worker from internal components when they want to check revocation of a certificate. An example is the link manager checking revocation of session certificates when these are used (by default, session PKI is turned off). |

Tags:

* `response.type`: The status code of an HTTP request.
* `endpoint.source`: The source endpoint of a peer-to-peer message.
* `endpoint.destination`: The destination endpoint of a peer-to-peer message.
* `connection.result`: The result of a TLS connection, for example, “success” or “failure".
