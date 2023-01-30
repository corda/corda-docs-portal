---
date: '2021-11-14'
title: "Cluster Health"
menu:
  corda-5-beta:
    parent: corda-5-beta-deploy-troubleshoot
    identifier: corda-5-beta-deploy-cluster-health
    weight: 1000
section_menu: corda-5-beta
---
<!-- https://r3-cev.atlassian.net/browse/DOC-4187-->

This page describes how to determine whether your cluster is currently healthy and some steps to debug common issues.
If you are unable to resolve your issue, see the [Support Bundles](support-bundles.html) section for details of information to collect so that R3 can provide further assistance.

## Pre-install Jobs

At install time, two Kubernetes jobs run sequentially prior to the deployment of the Corda workers (unless [Manual Bootstrapping](../deployment-tutorials/manual.html) is used).
Assuming a Helm release is called `corda`, these jobs are called `corda-create-topics` and `corda-setup-db`.
These jobs each create a pod that executes a number of containers and should then run through to completion.

If `kubectl get pods` shows that the jobs failed to start, use `kubectl describe` to determine the reason for the failure.
For example:

```shell
kubectl describe pod corda-setup-db-n6p8s
```

If the pod is unable to pull the Docker images, check that the image registry and image pull secret are configured correctly.

If the pods start but then fail to complete, this may indicate an issue with the connection settings.
For Kafka, ensure that the list of bootstrap servers is correct, and that the TLS and authentication settings provided to Corda match those for the Kafka cluster.
For PostgreSQL, ensure that the host name, port, and credentials provided to Corda are correct.

The container logs may help diagnose any issues.
Use the `--all-containers` option to retrieve the logs for all of the containers that run within the pod.
For example:

```shell
kubectl logs job/corda-setup-db --all-containers
```

{{< note >}}
These jobs only run on a Helm install, not on a Helm upgrade.
{{< /note >}}

## Corda Workers

Once the pre-install jobs have completed, the Kubernetes deployments for the Corda workers are created with the requested number of replicas.
Each Corda worker has an associated readiness probe.
If all is well, all of the pods should reach the `Running` state and then the post-install job will run.

If one or more of the pods do not start, use `kubectl describe` to determine the cause.
This may indicate that the Kubernetes cluster does not have sufficient resources to deploy all of the workers.
If so, increase the number of nodes allocated to the cluster, or the size of the instances for each node.

If one of the pods restarts, use `kubectl describe` to determine why the pod restarted.
It may be that the pod does not have sufficient resources and was terminated by Kubernetes due to an out of memory condition.
If this is the case, increase the requested resources in the deployment configuration YAML file and then upgrade the Helm install.
For example:

```shell
helm upgrade corda --namespace corda -f updated-values.yaml
```

If a pod is being terminated because the liveness probe has failed, or does restart but fails to reach the `Running` state, then further investigation is required.
The logs for a pod may help determine the cause of the failure.
Retrieve the logs using `kubectl logs`.
For example:

```shell
kubectl logs corda-db-worker-f9994f756-tqtx7
```

If a pod has restarted, it may be worth looking at the logs from the terminated instance using the `--previous` option.
For example:

```shell
kubectl logs --previous corda-db-worker-f9994f756-tqtx7
```

The type of the failing worker may also give a clue to the root cause.
For example, all of the workers connect to Kafka but only the database and Crypto workers connect to PostgreSQL.
Failures in the pods for these two workers may therefore indicate an issue with PostgreSQL.

## Post-install Job

Once all of the workers are ready, the Helm install executes a post-install job.
For a Helm release called `corda`, this is called `corda-setup-rbac`.
This job runs a pod with three containers that each create an RBAC role.
The containers use the REST API to create the roles so failures here tend to represent issues with the REST API.

As with the pre-install jobs, retrieve the logs to identify any failures:

```shell
kubectl logs job/corda-setup-rbac --all-containers
```

If errors are being returned from the REST API, check the logs for the RPC workers:

```shell
kubectl logs deployment/corda-rpc-worker
```
