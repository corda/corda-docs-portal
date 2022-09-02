---
date: '2020-07-15T12:00:00Z'
title: "Packaging"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 2000
section_menu: corda-5-dev-preview
---

## CorDapps

CorDapps are built as a layered package. At the lowest level, a [Corda Package (CPK)](#cordapp-packages-cpks) represents a single code-entity authored by a CorDapp developer. For example, a library of flows to perform some task. A [Corda Package Bundle (CPB)](#cordapp-package-bundles-cpbs) is built using a collection of these packages, which represents a full application. Finally, information about the network can be added to a CPB to create a [Corda Package Installer (CPI)](#cordapp-package-installer-cpi) file. When this is installed into the system, the cluster knows that any entity using this file must join the specified network, and so can handle network onboarding accordingly.

## CorDapp Packages (CPKs)
The building blocks of CorDapps are a new file format called CorDapp Packages (.`cpk`s). This includes workflow and contract packages, additional metadata, a dependency tree, and version information. You can independently version `.cpk`s. Each .`cpk` runs in its own [sandbox](#sandboxes), isolated from other CPKs. This prevents dependency clashes and facilitates faster CorDapp development.

## CorDapp Package Bundles (CPBs)
The application publisher brings individual `.cpk` files together to make a single CorDapp Package Bundle (`.cpb`). The application publisher is a single entity that coordinates multiple parties to create a single application bundle for a network. When multiple firms compose CorDapps together, it creates a strong technical dependency that facilitates development, distribution, and upgrades.

## CorDapp Package Installer (CPI)
CorDapps are packaged in a single `.jar` file called a CorDapp Package Installer (.`cpi`) containing all the pieces required to join and participate in an application network:
* The location of the network operator.
* A list of membership requirements.
* Third party dependencies.
* CorDapp logic.

The only difference between a development and a production CPI is the network information, so you can use the same software for testing environments.

The CPI file simplifies the onboarding process. A prospective customer must only obtain a single file that contains all necessary information to be able to request membership. This lets each member understand the pre-requisites of membership and configure required attributes or get artifacts from third parties as needed.
