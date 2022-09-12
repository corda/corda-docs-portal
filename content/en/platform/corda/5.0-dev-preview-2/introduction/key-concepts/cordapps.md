---
date: '2020-07-15T12:00:00Z'
title: "CorDapps"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 2000
section_menu: corda-5-dev-preview
---

## CorDapps

CorDapps are built as a layered package. At the lowest level, a [Corda Package (CPK)](#cordapp-packages-cpks) represents a single code-entity authored by a CorDapp developer. For example, a library of flows to perform some task. A [Corda Package Bundle (CPB)](#cordapp-package-bundles-cpbs) is built using a collection of these packages, which represents a full application. Finally, information about the network can be added to a CPB to create a [Corda Package Installer (CPI)](#cordapp-package-installer-cpi) file. When this is installed into the system, the cluster knows that any entity using this file must join the specified network, and so can handle network onboarding accordingly.



A CorDapp provides a solution to a problem that is only solved by distribution and the engagement of multiple parties.
