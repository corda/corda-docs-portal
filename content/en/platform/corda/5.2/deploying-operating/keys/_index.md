---
description: "Learn how to upload and rotate Corda 5 wrapping keys."
title: "Managing Wrapping Keys"
date: '2024-02-12'
menu:
  corda52:
    identifier: corda52-cluster-wrapping-keys
    parent: corda52-cluster
    weight: 3025
---

# Managing Wrapping Keys

As described in the [Architecture for Cluster Administrators]({{< relref "../../key-concepts/cluster-admin/_index.md#key-management" >}}) section, Corda keys are stored in the cluster and virtual node `Crypto` databases and encrypted at rest with wrapping keys.
These managed wrapping keys are in turn wrapped by a master wrapping key.
This section describes how Corda stores the master wrapping key and how to rotate master and managed wrapping keys. It contains the following:

{{< childpages >}}
