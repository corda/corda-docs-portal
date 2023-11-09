---
date: '2023-11-09'
version: 'Corda 5.1'
title: "Rolling Back"
menu:
  corda51:
    parent: corda51-cluster-upgrade
    identifier: corda51-cluster-rollback
    weight: 1000
section_menu: corda51
---
# Rolling Back

To roll back the Corda 5.0 to Corda {{< version-num >}} upgrade process, restore the [database backups]({{< relref "./index.md#back-up-the-corda-database" >}}) and restart the Corda 5.0 workers.

{{< note >}}

You can no longer roll back an upgrade after:

* Kafka topics or ACLs are deleted. R3 recommends that you do not delete old topics or ACLs until the upgrade to Corda {{< version-num >}} is complete.
* Corda {{< version-num >}} workers are launched and marked as `READY` in Kubernetes.

{{< /note >}}

To restart the Corda 5.0 workers, you can do one of the following:

* Reverse the commands in [Scale Down the Running Corda Worker Instances]({{< relref "./index.md#scale-down-the-running-corda-worker-instances" >}}) that scaled the workers to zero replicas.
* Issue a helm upgrade command that resets the values you installed Corda 5.0 with, which includes replica counts, for example:

   ```
   helm upgrade corda -n corda \
  oci://corda-os-docker.software.r3.com/helm-charts/release-5.0.0.0/corda \
  --version "5.0.0" \
  --values artifactory_values.yaml \
  --wait
   ```