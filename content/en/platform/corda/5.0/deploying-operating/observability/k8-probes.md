---
date: '2023-05-10'
title: "Kubernetes Liveness and Readiness Probes"
menu:
  corda5:
    parent: corda5-cluster-observability
    identifier: corda5-cluster-k8-probes
    weight: 1000
section_menu: corda5
---

All the Corda worker pods are configured with Kubernetes liveness and readiness probes.
These poll the status of the worker’s internal component’s registry.

If any of the components report that it is in an error state, the liveness probe will fail and Kubernetes will eventually restart the pod.
During normal operation, pods should not cause failures of the liveness probe and the Cluster Operator should monitor for failures
in the Kubernetes events stream.

The readiness probe will fail if any Corda components report that they are down.
During worker startup, this is expected behaviour and all the components should eventually report
that they are up resulting in the pod being marked as ready. Failures in the readiness probe after a worker
has started successfully are typically the result of issues with downstream services (for example, Kafka or Postgres).
These situations should be recoverable, but a Cluster Operator should monitor for Kubernetes pods that are not marked
as ready as these will not be processing work. In regards to workers that expose HTTP endpoints (the REST and P2P Gateway workers),
Kubernetes will not route HTTP requests to a worker that is not ready.
