---
title: "Configuring Corda"
project: corda
version: 'Corda 5.1'
date: '2023-05-16'
menu:
  corda51:
    identifier: corda51-cluster-config
    parent: corda51-cluster
    weight: 3050
section_menu: corda51
---

# Configuring Corda

Corda 5 uses a [dynamic configuration system]({{< relref "./dynamic.md" >}}), enabling you to configure Corda centrally through the REST API. This configuration is then distributed to all relevant {{< tooltip >}}worker{{< /tooltip >}} processes through the {{< tooltip >}}Kafka{{< /tooltip >}} message bus.
This standard dynamic configuration system is not suitable in the following instances:
* Boot configuration — the necessary configurations required to start a worker process, such as sufficient messaging configuration for the worker to connect to the `config.topic` Kafka topic. For more information, see the [Bootstrapping deployment section]({{< relref "../deployment/deploying/_index.md#bootstrapping" >}}). Typically, this type of configuration can later be overridden by dynamic configuration.
* Sensitive configuration — information that is not appropriate to publish to the `config.topic` topic because it is private, such as [database connection configuration]({{< relref "./database-connection.md" >}}) or private key material. The Corda configuration system allows for any string configuration value to be marked as [“secret”]({{< relref "./secrets.md" >}}). Sensitive configuration can also be saved to the configuration database itself ({{< tooltip >}}virtual node{{< /tooltip >}} connection details, for example), in which case it becomes dynamic configuration, but managed through a different interface.

This section contains the following:
{{< childpages >}}
