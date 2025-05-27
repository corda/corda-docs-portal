---
description: "Understand how to package a CorDapps."
date: '2023-02-23'
title: "Packaging"
menu:
  corda52:
    identifier: corda52-develop-packaging
    parent: corda52-develop
    weight: 6050
---
# Packaging

Just like a regular application, your {{< tooltip >}}CorDapp{{< /tooltip >}} must be packaged for distribution and installation. Corda takes a three-layered model to its packaging design to allow maximum reusability and portability:

1. **Corda Package (CPK):** Represents a single code-entity authored by a CorDapp Developer. CPKs are the Corda equivalent of a software library. They represent testable, reusable, sub-components of a final application. See [Build a CPK]({{< relref "./cpk.md">}}).
2. **Corda Package Bundle (CPB):** Built using a collection of CPKs, which represents a full application. CPBs are complete applications minus the “run time information” needed to onboard entities into it. CPBs represent the final efforts of the development team, a discrete and testable application, encapsulating the solution to a problem that can be deployed to form an {{< tooltip >}}application network{{< /tooltip >}}. See [Build a CPB]({{< relref "./cpb.md">}}).
3. **Corda Package Installer (CPI):** Contains the CPB and information about the network. The Network Operator builds this when [onboarding members]({{< relref "../../application-networks/creating/members/_index.md" >}}).
