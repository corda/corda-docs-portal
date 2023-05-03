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

1. **Corda Package (CPK):** Represents a single code-entity authored by a CorDapp developer. CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application. Corda runs each CPK in its own sandbox, isolated from other CPKs. See [Build a CPK]({{< relref "./cpk.md">}}).
2. **Corda Package Bundle (CPB)** — built using a collection of CPKs, which represents a full application. CPBs are complete applications minus the “run time information” needed to onboard entities into it. CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an application network. See [Build a CPB]({{< relref "./cpb.md">}}).
3. **Corda Package Installer (CPI)** — contains the CPB and information about the network. The Network Operator builds this when [onboarding members]({{< relref "../../application-networks/creating/members/_index.md" >}}).