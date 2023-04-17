---
date: '2023-04-13'
title: "Onboarding Members"
menu:
  corda-5-beta:
    identifier: corda-5-beta-app-networks-members
    parent: corda-5-beta-app-networks-create
    weight: 2000
section_menu: corda-5-beta
---
This section describes how to onboard new members to a dynamic network. It assumes that you have configured the [MGM for the network]({{< relref "../mgm/overview.md" >}}). The sections must be completed in the order in which they are presented:

1. [Build the member CPI]({{< relref "./cpi.md">}}).
2. [Create a virtual node]({{< relref "./virtual-node.md">}}).
3. [Configure key pairs and certificates]({{< relref "./key-pairs.md">}}).
5. [Configure communication properties]({{< relref "./config-node.md">}}).
4. [Register the member]({{< relref "./register.md">}}).

These sections describe a standard configuration. You can read about alternative configurations in the [Mutual TLS Connections]({{< relref "../optional/mutual-tls-connections.md">}}) and [Session Certificates]({{< relref "../optional/session-certificates.md">}}) sections.

{{< note >}}
The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.
{{< /note >}}