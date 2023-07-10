---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "HTTP Requests"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-http
    weight: 1000
section_menu: corda5
---

# HTTP Requests

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
| `corda_http_server_request_total` | Counter | <ul><li>`address`</li></ul> | The number of HTTP requests. |
| `corda_http_server_request_time_seconds` | Timer | <ul><li>`address`</li></ul> | HTTP requests processing time. |

Tags:
* `address`: The address that the metric is applicable to.
