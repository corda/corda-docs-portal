---
title: "Observability"
date: 2023-07-24
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-admin-observability
    parent: corda5-key-concepts-cluster-admin
    weight: 5000
section_menu: corda5
---

# Observability

## Logging

All components in a Corda cluster produce logs at level INFO by default. There are send to stdout/stderr and can easily be integrated with a log collector or aggregator of choice. All application-level logging is handled by log4J which means the log level and target can be changed through customizing the log4J config.

For more information about retrieving logs from Kubernetes, see [Metrics]({{< relref "../../../deploying-operating/observability/logs.md" >}}).

## Metrics

Corda workers expose metrics to provide a better insight into the system as a whole. These metrics are exposed as [prometheus](https://prometheus.io/) compatible HTTP endpoints that can be consumed by a collector and visualisation tool of choice. For more information, see [Metrics]({{< relref "../../../deploying-operating/observability/metrics/_index.md" >}}).