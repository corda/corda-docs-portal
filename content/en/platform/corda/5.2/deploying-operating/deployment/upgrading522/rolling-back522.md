---
description: "Learn how to roll back the Corda 5.2.1 to Corda 5.2.2 upgrade process if an issue occurs."
date: '2024-11-13'
title: "Rolling Back"
menu:
  corda52:
    parent: corda52-cluster-upgrade522
    identifier: corda522-cluster-rollback
    weight: 1000
---

# Rolling Back

In summary, the upgrade from Corda 5.2.1 to 5.2.2 requires you to perform the following steps:
* Scale back all Corda workers to zero replicas.
* Bring the workers back at the latest version.

To roll back this process, all that you need to do is bring Corda 5.2.1 workers back up.

You can roll back an upgrade up until the point where Corda 5.2.2 workers are brought back up to a running state. At this point, the 5.2.2 workers start publishing the 5.2.1 messages to Kafka and the 5.2.1 worker software cannot necessarily read them.

To bring Corda 5.2.1 workers back, perform one of the following actions:

* You can use `kubectl scale` with a replica count greater than one, reversing the step below where they were scaled to zero replicas.
* Or you can issue a Helm upgrade command which resets the values you installed Corda 5.2.1 with, including replica counts, for example:

```
helm upgrade corda -n corda \
helm fetch oci://registry-1.docker.io/corda/corda --version 5.2.1
--version "5.2.1" \
--values artifactory_values.yaml \
--wait
```
