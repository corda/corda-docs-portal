---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-cordapps
tags:
- cordapp
- compatibility
title: CorDapp compatibility between Corda and Corda Enterprise
weight: 4
---


# CorDapp compatibility between Corda and Corda Enterprise

Corda and Corda Enterprise have an Open Core approach. This means that both Corda and Corda Enterprise are compiled
against the Corda Core library.

This allows CorDapps to be developed for compatibility between Corda and Corda Enterprise.

In order to develop a CorDapp for compatibility between Corda and Corda Enterprise follow these steps:


* Ensure your CorDapp is designed per [Structuring a CorDapp](writing-a-cordapp.md) and annotated according to [CorDapp separation](cordapp-build-systems.md#cordapp-separation-ref).
In particular, it is critical to separate the consensus-critical parts of your application (contracts, states and their dependencies) from
the rest of the business logic (flows, APIs, etc).
The former - the **CorDapp kernel** - is the Jar that will be attached to transactions creating/consuming your states and is the Jar
that any node on the network verifying the transaction must execute.

{{< note >}}
It is also important to understand how to manage any dependencies a CorDapp may have on 3rd party libraries and other CorDapps.
Please read [Setting your dependencies](cordapp-build-systems.md#cordapp-dependencies-ref) to understand the options and recommendations with regards to correctly Jar’ing CorDapp dependencies.

{{< /note >}}

* Compile this **CorDapp kernel** Jar once, and then depend on it from your workflows Jar. In terms of Corda depdendencies,this should only
depend on the `corda-core` package from the Corda Open Source distribution.

{{< note >}}
As of Corda 4 it is recommended to use [CorDapp Jar signing](cordapp-build-systems.md#cordapp-build-system-signing-cordapp-jar-ref) to leverage the new signature constraints functionality.

{{< /note >}}

* Your workflow Jar(s) should depend on the **CorDapp kernel** (contract, states and dependencies). Importantly, you can create different workflow
Jars for Corda and Corda Enterprise, because the workflows Jar is not consensus critical. For example, you may wish to add additional features
to your CorDapp for when it is run on Corda Enterprise (perhaps it uses advanced features of one of the supported enterprise databases or includes
advanced database migration scripts, or some other Enterprise-only feature).When building a CorDapp against Corda Enterprise, please note that the `corda-core` library still needs to come from the open source
distribution, so you will have dependencies on Corda Enterprise and a matching open core distribution. Specifically, any CorDapp targeted
to run on Corda Enterprise should have unit and integration tests using Corda Enterprise.

In summary, structure your app as kernel (contracts, states, dependencies) and workflow (the rest) and be sure to compile the kernel
against Corda open source. You can compile your workflow (Jars) against the distribution of Corda that they target.

