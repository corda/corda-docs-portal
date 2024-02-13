---
description: "Learn how to "
title: "Configuring the Master Wrapping Key"
date: '2024-02-12'
menu:
  corda52:
    identifier: corda52-cluster-wrapping-master
    parent: corda52-cluster-wrapping-keys
    weight: 1000
---

# Configuring the Master Wrapping Key

The master wrapping key, or the information required to generate this key, must be stored and managed outside Corda.
You can achieve this in one of the following ways:

* Pass a passphrase and salt, to generate the master key, into the crypto worker processes. For more information, see [Default Secrets Service]({{< relref "../../deploying-operating/deployment/deploying/_index.md#default-secrets-service" >}}).
* {{< enterprise-icon noMargin="true" >}} Store and manage the master in an external key management system for Corda to retrieve when required. For more information, see [External Secrets Service]({{< relref "../../deploying-operating/deployment/deploying/_index.md#external-secrets-service" >}}).

Corda stores the master wrapping key settings in the `corda.crypto` configuration section.
For information about the configuration fields in this section, see [corda.crypto]({{< relref "../config/fields/crypto.md" >}}).
For information about how to retrieve the current values of a configuration section, see [Retrieving Current Configuration Values]({{< relref "../config/dynamic.md#retrieving-current-configuration-values" >}}).
