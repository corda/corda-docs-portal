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
* add links
* 

{{< note >}}
These tutorials all assume that you have:
* [deployed Corda 5 to a Kubernetes cluster](../../../deploying/deployment-tutorials/deploy-corda-cluster.html).
* cloned the [corda-runtime-os repository](https://github.com/corda/corda-runtime-os).

The PowerShell commands listed are for use with PowerShell 7.0 and will not execute correctly with PowerShell 5.x.

{{< /note >}}