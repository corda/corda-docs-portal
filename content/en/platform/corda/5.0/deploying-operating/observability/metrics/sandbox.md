---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Sandbox"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-sandbox
    weight: 2000
section_menu: corda5
---

# Sandbox

Corda 5 sandbox is used to support Corda's stability and security when operating in a highly-available and multi-tenant
configuration, allowing a safe execution environment within a JVM process that provides isolation for CorDapps.

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
| `corda_sandbox_create_time_seconds` | Timer | <ul><li>`virtualnode`</li><li>`sandbox_type`</li></ul> | The time it took to create the sandbox. |

Tags:
* `virtualnode`: A virtual node the sandbox applies to.
* `sandbox_type`: The type of sandbox.
