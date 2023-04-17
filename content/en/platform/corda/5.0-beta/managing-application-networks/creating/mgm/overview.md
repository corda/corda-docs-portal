---
date: '2023-04-07'
title: "Onboarding the MGM"
menu:
  corda-5-beta:
    parent: corda-5-beta-app-networks-create
    identifier: corda-5-beta-app-networks-mgm
    weight: 1000
section_menu: corda-5-beta
---
This section describes how to configure the MGM, through which a membership group is created for a dynamic network. The sections must be completed in the order in which they are presented:

1. [Build the MGM CPI]({{< relref "./cpi.md">}}).
2. [Create a virtual node]({{< relref "./virtual-node.md">}}).
3. [Configure key pairs and certificates]({{< relref "./key-pairs.md">}}).
4. [Register the MGM]({{< relref "./register.md">}}).
5. [Configure communication properties]({{< relref "./config-node.md">}}).

These sections describe a standard configuration. You can read about alternative configurations in the [Mutual TLS Connections]({{< relref "../optional/mutual-tls-connections.md">}}) and [Session Certificates]({{< relref "../optional/session-certificates.md">}}) sections.

{{< note >}}
These tutorials all assume that you have:
* [deployed Corda 5 to a Kubernetes cluster]({{< relref "../../../deploying/deployment-tutorials/deploy-corda-cluster.html">}}).
* cloned the [GitHub corda-runtime-os repository](https://github.com/corda/corda-runtime-os).

The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.

{{< /note >}}
