---
date: '2023-05-10'
version: 'Corda 5.0'
title: "Metrics"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-metrics
    weight: 2000
section_menu: corda5
---

# Metrics

Metrics provide greater insight into the inner workings of Corda and can be used as the basis for monitoring and alerting.

## Collecting Metrics

All the Corda worker pods expose metrics in Prometheus text format at `/metrics` on port 7000.
By default, this port is not exposed outside the {{< tooltip >}}Kubernetes{{< /tooltip >}} cluster but most observability platforms support
running an agent within the cluster that dynamically detects Kubernetes pods exposing Prometheus endpoints and then polls for metrics.

By default, the pods have the following Kubernetes annotations which may be sufficient for some monitoring agents
to automatically scrape the endpoints:

```yaml
prometheus.io/scrape: "true"
prometheus.io/path: "/metrics"
prometheus.io/port: "7000"
```

You can disable these annotations by providing the following overrides on the Corda {{< tooltip >}}Helm{{< /tooltip >}} chart:

```yaml
metrics:
    scrape: false
```
If you are using the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator),
the Corda Helm chart supports the creation of a PodMonitor custom resource.
The PodMonitor should be configured with the labels that the Prometheus Operator is set to discover.
When using the [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
Helm chart, this is the name of the Helm release for the Prometheus stack. For example:

```yaml
metrics:
  podMonitor:
    enabled: true
    labels:
      release: [RELEASE_NAME]
```

### Exported Metrics

The following Corda-specific metrics are exported and they have been added at the following levels:
{{< childpages >}}
