---
description: "Learn how to use Kubernetes liveness and readiness probes with Corda."
date: '2023-05-10'
version: 'Corda 5.2'
title: "Kubernetes Liveness and Readiness Probes"
menu:
  corda52:
    parent: corda52-cluster-observability
    identifier: corda52-cluster-k8-probes
    weight: 1000
section_menu: corda52
---
# Kubernetes Liveness and Readiness Probes

All Corda worker pods are configured with {{< tooltip >}}Kubernetes{{< /tooltip >}} liveness and readiness probes.
These poll the status of the worker’s internal component registry.

If any component reports that it is in an error state, the liveness probe fails and Kubernetes eventually restarts the pod.
During normal operation, pods should not cause failures of the liveness probe and the Cluster Administrator should monitor for failures in the Kubernetes events stream.

The readiness probe fails if any Corda components report that they are down.
During worker startup, this is expected behavior and all the components should eventually report that they are up, resulting in the pod being marked as ready. Failures in the readiness probe after a worker has started successfully are typically the result of issues with downstream services (for example, {{< tooltip >}}Kafka{{< /tooltip >}} or Postgres).
These situations should be recoverable, but a Cluster Administrator should monitor for Kubernetes pods that are not marked as ready as these will not be processing work.
In regard to workers that expose HTTP endpoints (the {{< tooltip >}}gateway worker{{< /tooltip >}} and {{< tooltip >}}P2P Link Manager worker{{< /tooltip >}}), Kubernetes will not route HTTP requests to a worker that is not ready.
