---
aliases:
- /releases/3.2/version-compatibility.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-version-compatibility
    parent: corda-enterprise-3-2-corda-enterprise
    weight: 30
tags:
- version
- compatibility
title: Corda and Corda Enterprise compatibility
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Corda and Corda Enterprise compatibility

Corda Enterprise 3.1 provides a baseline for wire stability and compatibility with future versions of Corda Enterprise, and open-source releases of Corda starting from version 3.0.

Future versions of Corda Enterprise will be backward compatible with Corda Enterprise 3.1:



* Corda Enterprise 3.1 nodes can be upgraded to future version of Corda Enterprise. The upgrade will preserve transaction, configuration and other data.
* Corda Enterprise 3.1 nodes will be able to transact with nodes running future versions of Corda Enterprise, providing the CorDapp is compatible with and between platform versions.
* Future versions of Corda Enterprise will be able to run CorDapps developed for, and packaged on Corda Enterprise 3.1.


Corda Enterprise 3.1 and Corda Enterprise 3.2 can be used in mixed-version/mixed-distribution networks seamlessly transacting with nodes running Corda 3.x and future versions.



* Corda Enterprise 3.1 and Corda Enterprise 3.2 nodes can transact with nodes running Corda 3.0 and future versions, providing the CorDapp is compatible with and between platform versions and distributions.
* CorDapps originally written for Corda 3.x are API compatible with Corda Enterprise 3.1 and future versions.
Developers can switch their IDE to Corda Enterprise 3.1 or Corda Enterprise 3.2 without any code changes in their CorDapp.
* Corda Enterprise 3.1 and Corda Enterprise 3.2 nodes can run, without recompilation, CorDapps developed on and packaged for Corda 3.x.


{{< note >}}
These compatibility commitments are subject to the standard Corda Enterprise software support policy.

{{< /note >}}

{{< table >}}

|Compatibility with Corda Enterprise 3.x|DP3|DP2|DP1|Corda 3.x|Corda 2|Corda 1|Corda pre 1|
|------------------------------------------------|-------------|---------------|---------------|------------------|-----------------|-----------------|---------------------|
|**API compatibility**, i.e. CorDapps developed
for this Corda version can be compiled and run
on Corda Enterprise 3.x nodes|Yes|Yes|Yes|Yes|Yes|Yes|No|
|**Binary compatibility**, i.e. CorDapps
compiled on this Corda version can be run on
Corda Enterprise 3.x nodes|Yes|Yes|Yes|Yes|Yes|Yes|No|
|**Network compatibility**, i.e., nodes running
this Corda version can transact with Corda
Enterprise 3.x nodes|No*|Yes|Yes|Yes|No|No|No|
|**RPC compatibility**, i.e, a client
application developed for this Corda version
can interact via RPC with a CorDapp running on
the Corda Enterprise 3.x node|Yes|Yes|Yes|No|No|No|No|
|Samples and community apps from
[https://www.corda.net/samples/](https://www.corda.net/samples/) for this Corda
version can be compiled and run on Corda
Enterprise 3.x nodes|Yes|Yes|Yes|Yes|Yes|Yes|No|
|Bootstrapper tool from this Corda version can
be used to build Corda Enterprise 3.x test
networks|No*|Yes|Yes|No|No|No|No|

{{< /table >}}

{{< note >}}
Greyed out releases are out of support.

Cells denoted with asterisk (*) refer to development-mode only. The incompatibility is caused by a change to the truststore for development-mode certificates between
Developer Preview 3 (DP3) and Corda Enterprise 3.x. In other words, DP3 is network compatible with Corda Enterprise 3.x provided that development-mode is disabled.

{{< /note >}}
