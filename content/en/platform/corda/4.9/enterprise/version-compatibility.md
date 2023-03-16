---
date: '2021-08-12'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-upgrading-menu
tags:
- version
- compatibility
title: Corda and Corda Enterprise compatibility
weight: 80
---


# Corda and Corda Enterprise compatibility

Corda Enterprise Edition 4.0 guarantees the wire stability and compatibility baseline introduced in Corda Open Source 3.0
is maintained with future versions of Corda Enterprise.

Corda Enterprise Edition 4.0 can be used in mixed-version/mixed-distribution networks seamlessly, transacting with nodes running on a minimum platform version of 4.

See [versioning]({{< relref "../../../../../en/platform/corda/4.9/enterprise/cordapps/versioning.md" >}}) for further information.


{{< note >}}

These compatibility commitments are subject to the standard Corda Enterprise software support policy.

{{< /note >}}

{{< table >}}

|Compatibility with Corda Enterprise Edition 4.0|Corda Open Source 4.x|Enterprise Corda 3.x|Corda Open Source 3.x|
|-------------------------------------------------|-------------|-----------------------|---------------|
|**API compatibility**, CorDapps developed for this Corda version can be compiled and run on Corda Enterprise Edition 4.0 nodes.|Yes|Yes|Yes|
|**Binary compatibility**, CorDapps compiled on this Corda version can be run on Corda Enterprise Edition 4.0 nodes.|Yes|Yes|Yes|
|**Network compatibility**, nodes running this Corda version can transact with Corda Enterprise Edition 4.0 nodes.|Yes|Yes|Yes|
|**RPC compatibility**, a client application developed for this Corda version can interact via RPC with a CorDapp running on a Corda Enterprise Edition 4.0 node.|Yes|Yes|No|
|Samples and community apps from [https://github.com/corda/samples](https://github.com/corda/samples) for this Corda version can be compiled and run on Corda Enterprise Edition 4.0 nodes.|Yes|Yes|Yes|

{{< /table >}}

You should also be aware of the following:

* Corda Enterprise Edition 4.0 nodes can transact with nodes running Corda Open Source 4.0 and future versions, providing the CorDapp is compatible with and between platform versions and distributions.

* CorDapps written for Corda Open Source 4.x are API compatible with Corda Enterprise Edition 4.0 and future versions.
  Developers can switch their IDE to Corda Enterprise Edition 4.0 without making any code changes in their CorDapp.{{< note >}}
  The reverse is not true. We do not guarantee that CorDapps compiled against Corda Enterprise will run on Corda Open Source.{{< /note >}}

* Corda Enterprise Edition 4.0 nodes can run CorDapps developed on and packaged for Corda 4.x, without recompilation.
  However, due to Corda Enterprise's advanced features, such as database migration scripting support, we anticipate application developers
  will build their CorDapp kernels (contracts, states) against Corda Open Source, and supply two separate workflow JARs (that depend on the same kernel)
  that are optimized for each distribution. See [separation of CorDapp contracts, flows and services](../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-build-systems.html#separate-cordapp-contracts-flows-and-services) for further information.

{{< note >}}

Compatibility guarantees apply to the latest minor release version of both Corda Enterprise and Corda Open Source, including any subsequent patches.

{{< /note >}}
