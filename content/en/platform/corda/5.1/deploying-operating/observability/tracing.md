---
date: '2023-05-10'
version: 'Corda 5.1'
title: "Tracing Framework"
menu:
  corda5:
    parent: corda51-cluster-observability
    identifier: corda51-cluster-tracing
    weight: 4000
section_menu: corda5
---

# Tracing Framework

As a Corda Cluster Operator, you may want to configure a tracing server and sample rate when deploying the {{< tooltip >}}Helm{{< /tooltip >}} chart.
The tracing configuration supported by the Helm chart contains the following configuration in the `values.yaml` file:

```
tracing:
  # -- URL for the endpoint to send Zipkin-format distributed traces to for example http://tempo:9411
  endpoint: ""
  # --  Number of request traces to sample per second, defaults to 1 sample per second. Set to 'unlimited' to record all
  traces, but in this case the amount of tracing data produced can be quite vast.
  samplesPerSecond: "1"
```
