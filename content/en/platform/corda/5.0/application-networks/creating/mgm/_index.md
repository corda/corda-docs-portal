---
date: '2023-04-07'
title: "Onboarding the MGM"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    parent: corda5-networks-create
    identifier: corda5-networks-mgm
    weight: 1000
section_menu: corda5
---

# Onboarding the MGM

This section describes how to configure the MGM, through which a membership group is created for a dynamic network. The sections must be completed in the order in which they are presented:
{{< childpages >}}

These sections describe a standard configuration. You can read about alternative configurations in the [Optional Configurations]({{< relref"../optional/_index.md">}}) section.

{{< note >}}
These tutorials all assume that you have:
* [deployed Corda 5 to a Kubernetes cluster](../../../deploying-operating/deploying/_index.md).
* cloned the [GitHub corda-runtime-os repository](https://github.com/corda/corda-runtime-os).

The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.

{{< /note >}}
