---
description: "Learn how to upgrade your cluster from Corda 5.2.1 to Corda 5.2.2."
date: '2024-11-12'
title: "Upgrading from 5.2.1 to 5.2.2"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-upgrade522
    weight: 6000
---
# Upgrading from 5.2.1 to 5.2.2

This section describes how to upgrade a Corda cluster from version 5.2.1 to 5.2.2.

{{< note >}}
You cannot upgrade Corda 5.1 directly to 5.2.2. You must first upgrade Corda 5.1 to version 5.2, then to 5.2.1, and finally to 5.2.2. For information on the previous upgrade processes, see:
* [Upgrading from 5.1 to 5.2]({{< relref "../upgrading/_index.md" >}})
* [Upgrading from 5.2 to 5.2.1]({{< relref "../upgrading521/_index.md" >}})

{{< /note >}}

The examples provided in this section assume that you installed Corda 5.2.1 in a namespace called `corda`. This is different to other deployments.

To perform an upgrade, you must fulfill the required [prerequisites](#prerequisites) and go through the following steps:

1. [Scale Down the Running Corda Worker Instances](#scale-down-the-running-corda-worker-instances)
2. [Launch the Corda 5.2.2 Workers](#launch-the-corda-522-workers)

For information about how to roll back an upgrade, see [Rolling Back]({{< relref "rolling-back521.md" >}}).

## Prerequisites

Corda 5 relies on certain underlying prerequisites, namely Kafka and PostgreSQL, administered by the Cluster Administrators.

{{< note >}}
This guide assumes that the Cluster Administrator assigned to upgrade Corda has full administrator access to these prerequisites.
{{< /note >}}

Developers, including customer CorDapp developers, or those trialing Corda, can use the R3-provided [Corda Helm chart]({{< relref "../deploying/_index.md#download-the-corda-helm-chart" >}}) which installs these prerequisites. The Corda Helm chart can also configure Corda, so it can reach these prerequisites, allowing a quick and convenient installation of Corda 5.

Customers in production are not expected to follow this path, and generally use managed services for these prerequisites. There are likely to be significant privilege restrictions in terms of who can administer these services. This guide cannot provide instructions on how to gain administrator access to customer-managed or self-hosted services.

### Downloads

Install Kubernetes command line tool (`kubectl`) on your local machine.

## Scale Down the Running Corda Worker Instances

You can scale down the workers using any tool of your choice. For example, run the following commands if using `kubectl`:

```
kubectl scale --replicas=0 deployment/corda-crypto-worker -n corda
kubectl scale --replicas=0 deployment/corda-db-worker -n corda
kubectl scale --replicas=0 deployment/corda-flow-mapper-worker -n corda
kubectl scale --replicas=0 deployment/corda-flow-worker -n corda
kubectl scale --replicas=0 deployment/corda-membership-worker -n corda
kubectl scale --replicas=0 deployment/corda-p2p-gateway-worker -n corda
kubectl scale --replicas=0 deployment/corda-p2p-link-manager-worker -n corda
kubectl scale --replicas=0 deployment/corda-persistence-worker -n corda
kubectl scale --replicas=0 deployment/corda-rest-worker -n corda
kubectl scale --replicas=0 deployment/corda-token-selection-worker -n corda
kubectl scale --replicas=0 deployment/corda-uniqueness-worker -n corda
kubectl scale --replicas=0 deployment/corda-verification-worker -n corda
```

If you are scripting these commands, you can wait for the workers to be scaled down using something similar to the following:

```
while [ "$(kubectl get pods --field-selector=status.phase=Running -n corda | grep worker | wc -l | tr -d ' ')" != 0 ]
do
sleep 1
done
```

## Launch the Corda 5.2.2 Workers

If Corda 5.2.1 was deployed using Corda Helm chart, you can deploy Corda 5.2.2 the same way. This updates the deployments with the new image versions and scales them to the defined replica counts. The Corda version is overridden at the command line, and selecting the 5.2.2 Corda Helm chart defaults to the 5.2.2 worker images. If you provide your own values in a YAML file, ensure it does not refer to 5.2.1 images.

For more information, see the [Corda Helm chart]({{< relref "../deploying/_index.md#download-the-corda-helm-chart" >}}) instructions.
