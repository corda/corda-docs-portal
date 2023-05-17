---
title: "Configuring Corda"
project: corda
version: 'Corda 5.0'
date: '2023-05-16'
menu:
  corda5:
    identifier: corda5-cluster-config
    parent: corda5-cluster
    weight: 3050
section_menu: corda5
---

Corda 5 uses a [dynamic configuration system]({{< relref "./dynamic.md" >}}), enabling you to configure Corda centrally through the REST API. This configuration is then distributed to all relevant worker processes through the Kafka message bus.

Standard dynamic configuration is not suitable in the following instances:
* Boot configuration — the necessary configurations required to start a worker process, such as sufficient messaging configuration for the worker to connect to the `config.topic` Kafka topic. For more information, see the [Manual Bootstrappping section]({{< relref "../deploying/bootstrapping.md" >}}). Typically, this type of configuration can later be overridden by dynamic configuration.
* Sensitive configuration — information that is not appropriate to publish to the `config.topic` topic because it is private, such as [database connection configuration]({{< relref "./database-connection.md" >}}) or private key material. The Corda configuration system allows for any string configuration value to be marked as [“secret”]({{< relref "./secrets.md" >}}). Sensitive configuration can also be saved to the configuration database itself (virtual node connection details, for example), in which case it becomes dynamic configuration, but managed through a different interface. 

This section contains the following:
{{< childpages >}}