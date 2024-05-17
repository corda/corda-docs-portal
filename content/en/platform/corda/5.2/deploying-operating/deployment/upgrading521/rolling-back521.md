---
description: "Learn how to roll back the Corda 5.1 to Corda 5.2 upgrade process if an issue occurs."
date: '2023-11-09'
title: "Rolling Back"
menu:
  corda52:
    parent: corda52-cluster-upgrade521
    identifier: corda521-cluster-rollback
    weight: 1000
---

# Rolling Back

In summary, the upgrade from Corda 5.2 to 5.2.1 requires you to perform the following steps:
* Scale back all Corda workers to zero replicas.
* Upgrade all persisted state schemas.
* Migrate data from Kafka to the database.
* Bring the workers back at the latest version.

To roll back this process, all that you need to do is to reinstate the database backups and bring Corda 5.2 workers back up. Database backup and rollback procedures are not described by this document as they are not under the scope of Corda.

You can roll back an upgrade up until the point where Corda 5.2.1 workers are brought back up to a running state. At this point, the 5.2.1 workers start publishing the 5.2.1 messages to Kafka and the 5.2 worker software cannot necessarily read them.

To bring Corda 5.2 workers back you can use `kubectl scale` with a replica count greater than 1, reversing the step below where they were scaled to zero replicas. Or you can issue a helm upgrade command which resets the values you installed Corda 5.2 with, which includes replica counts, for example:

```
helm upgrade corda -n corda \
oci://corda-os-docker.software.r3.com/helm-charts/release-5.2.0.0/corda \
--version "5.2.0" \
--values artifactory_values.yaml \
--wait
```
