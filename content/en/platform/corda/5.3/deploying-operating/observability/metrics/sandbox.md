---
description: "Review the metrics generated for the Corda sandbox. The sandbox supports Corda's stability and security when operating in a highly-available and multi-tenant configuration."
date: '2023-06-14'
title: "Sandbox"
menu:
  corda53:
    parent: corda53-cluster-metrics
    identifier: corda53-cluster-sandbox
    weight: 1400
---

# Sandbox

The Corda 5 {{< tooltip >}}sandbox{{< /tooltip >}} is used to support Corda's stability and security when operating in a highly-available and multi-tenant configuration, allowing a safe execution environment within a JVM process that provides isolation for {{< tooltip >}}CorDapps{{< /tooltip >}}.

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
* `virtualnode`: A {{< tooltip >}}virtual node{{< /tooltip >}} the sandbox applies to.
* `sandbox_type`: The type of sandbox.
