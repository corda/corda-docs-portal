---
description: "Learn how Corda metrics can provide insight into the inner workings of Corda and can be used as the basis for monitoring and alerting."
date: '2023-06-14'
version: 'Corda 5.1'
title: "Metrics"
menu:
  corda51:
    parent: corda51-cluster-observability
    identifier: corda51-cluster-metrics
    weight: 2000
section_menu: corda51
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
If you are using the [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator), the Corda Helm chart supports the creation of a PodMonitor custom resource. You should configure the PodMonitor with the labels that the Prometheus Operator is set to discover. When using the [kube-prometheus-stack](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack) Helm chart, this is the name of the Helm release for the Prometheus stack. For example:

```yaml
metrics:
  podMonitor:
    enabled: true
    labels:
      release: [RELEASE_NAME]
```

You can also configure filters in the PodMonitor to reduce the metrics recorded by setting the following fields:

* `keepNames` — a list of regular expressions for the names of the metrics that Prometheus records. If empty, all metrics are recorded. Prometheus records the following metrics by default:
  * corda_flow_execution_time_seconds_(count|sum|max)
  * corda_http_server_request_time_seconds_(count|sum|max)
  * corda_p2p_gateway_inbound_request_time_seconds_(count|sum|max)
  * corda_p2p_gateway_outbound_request_time_seconds_(count|sum|max)
  * corda_p2p_gateway_outbound_tls_connections_total
  * corda_p2p_message_outbound_total
  * corda_p2p_message_outbound_replayed_total
  * corda_p2p_message_outbound_latency_seconds_(count|sum|max)
  * corda_p2p_message_inbound_total
  * corda_p2p_session_outbound_total
  * corda_p2p_session_inbound_total
  * corda_membership_actions_handler_time_seconds_(count|sum|max)
  * jvm_.*
  * process_cpu_usage
* `dropLabels` — a list of regular expressions for the labels that Prometheus drops for all metrics. If empty, all labels are recorded. Prometheus drops the following metrics by default:
  * virtualnode_destination
  * virtualnode_source

### Exported Metrics

The following Corda-specific metrics are exported and they have been added at the following levels:
{{< childpages >}}
