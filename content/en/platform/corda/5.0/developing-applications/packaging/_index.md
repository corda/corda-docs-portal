---
date: '2023-02-23'
title: "Packaging"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-packaging
    parent: corda5-develop
    weight: 4000
section_menu: corda5
---
Just like a regular application, your CorDapp must be packaged for distribution and installation. Corda takes a three-layered model to its packaging design to allow maximum reusability and portability:

1. **Corda Package (CPK)** — represents a single code-entity authored by a CorDapp developer. CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application. Corda runs each CPK in its own sandbox, isolated from other CPKs.
2. **Corda Package Bundle (CPB)** — built using a collection of CPKs, which represents a full application. CPBs are complete applications minus the “run time information” needed to onboard entities into it. CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an application network.
3. **Corda Package Installer (CPI)** — contains the CPB and information about the network. The Network Operator builds this when [onboarding members]({{< relref "../../application-networks/creating/members/_index.md" >}}).

## Configure the Packaging Plugins in Gradle

To add the CPK plugin to your project, add the following to the top of the `build.gradle` file of your CorDapp Gradle project:
```
plugins {
    id 'net.corda.plugins.cordapp-cpk2'
}
```

To add the CPB plugin to your project, add the following to the top of the `build.gradle` file of your CorDapp Gradle project:
```
plugins {
    id 'net.corda.plugins.cordapp-cpb2'
}
```

If your Gradle project only contains a single module, apply both plugins together.

## Build a CPK

## Build a CPB