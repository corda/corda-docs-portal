---
date: '2023-05-10'
version: 'Corda 5.0 Beta 4'
title: "Tracing Framework"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-tracing
    weight: 4000
section_menu: corda5
---

# Tracing Framework

As a Corda Cluster Operator, you may want to configure sample rate when deploying the Helm chart. You can do this using the
`--trace-samples-per-second` command line option that:

* defaults to 1 sample per second if not set
* allows specifying unsigned numeric values as samples per second
* allows `unlimited` value to to sample all requests

The tracing configuration supported by the Helm chart contains the following information in the `values.yaml` file:

```
tracing:
  # -- URL for endpoint to send Zipkin-format distributed traces to e.g. http://tempo:9411
  endpoint: ""
  # --  Number of request traces to sample per second, defaults to 1 sample per second. Set to 'unlimited' to record all
  traces, but in this case amount of tracing data produced can be quite vast.
  samplesPerSecond: "1"
```
