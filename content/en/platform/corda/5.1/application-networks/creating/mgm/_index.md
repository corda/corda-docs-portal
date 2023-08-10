---
date: '2023-08-10'
title: "Onboarding the MGM"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    parent: corda51-networks-create
    identifier: corda51-networks-mgm
    weight: 1000
section_menu: corda51
---

# Onboarding the MGM

This section describes how to configure the {{< tooltip >}}MGM{{< /tooltip >}}, through which a {{< tooltip >}}membership group{{< /tooltip >}} is created for a dynamic network. The sections must be completed in the order in which they are presented:
{{< childpages >}}

These sections describe a standard configuration. You can read about alternative configurations in the [Optional Configurations]({{< relref"../optional/_index.md">}}) section.

{{< note >}}
These tutorials all assume that you have:
* [deployed Corda 5 to a Kubernetes cluster]({{< relref "../../../deploying-operating/deployment/deploying/_index.md" >}}).
* cloned the [GitHub corda-runtime-os repository](https://github.com/corda/corda-runtime-os).

The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.

{{< /note >}}
