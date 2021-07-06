---
date: '2021-07-06'
menu:
  corda-enterprise-4-8:
    identifier: "corda-enterprise-4-8-features-versions"
    name: "Corda features and versions"
    parent: corda-enterprise-4-8-upgrading-menu
tags:
- features
- versions
title: Corda features and versions
weight: 70
---


# Corda features and versions


Each version of Corda introduces new features. Features fall into one of three categories, and each category has different implications for node operators, CorDapp developers, and business network operators. There are:

* Changes that don't impact CorDapp developers or the Corda network protocol, but will be of interest to a node's operator. For example, introducing support for a new HSM or database system.
* New or updated APIs that will affect CorDapp developers. 
* Changes that affect the operation of a Corda network. For example, changes to the serialization format, flow/wire protocol, or the introduction of a new transaction component.  These are changes to the core data model and therefore should only be taken advantage of if all nodes on the network can support them. Such features are only enabled in a node if the network to which it is connected has published a `minimumPlatformVersion` in its network parameters that is greater than or equal to the Corda platform version that introduced the feature. For example, Corda 4.0 nodes, which implement Corda Platform Version 4, can only take advantage of the Corda reference states feature when connected to a network with mPV 4. 

When a release includes features that fall into the last two categories, the Corda platform version of that node is incremented so that a CorDapp that relies on a new or changed feature can detect this. It prevents CorDapps from running on a node without the feature or triggers an alternative optimized code path if the feature is present. 

You can use `CorDapp.mPV` to identify the oldest PV with which your CorDapp is compatible. This prevents nodes that use an older PV from running your CorDapp. Nodes that support newer PVs may also use this field to trigger code paths that emulate behaviours that were in force on older PVs to maximise compatibility. If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can show this in `CorDapp.targetPV`. This means it's possible to ship CorDapps that can run on all nodes supporting a minimum PV of Corda, as well as take advantage of a newer PV's behaviours and features should they happen to be available on any given node.

You can use `minimumPlatformVersion` to identify the oldest PV with which your CorDapp is compatible. This prevents nodes that use an older PV from running your CorDapp. Nodes that support newer PVs may also use this field to trigger code paths that emulate behaviours that were in force on older PVs to maximise compatibility. If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can show this in `CorDapp.targetPV`. This means it's possible to ship CorDapps that can run on all nodes supporting a minimum PV of Corda, as well as take advantage of a newer PV's behaviours and features should they happen to be available on any given node.

The CorDapp's developer can set the CorDapp’s `minimumPlatformVersion` parameter to signal the minimum Platform Version (mPV) against which the CorDapp can run or has been tested. If the CorDapp has been tested against a newer PV, the CorDapp's developer can set the `targetPlatformVersion` parameter.

<!--
CorDapp.mPV and CorDapp.targetPV - have these been replaced by `minimumPlatformVersion` and `targetPlatformVersion`?
-->

{{< table >}}


## Corda features

The table below highlights key features and the corresponding version numbers. 

|Feature|Corda platform version (PV)|Minimum network platform version (network mPV)|Introduced in OS version|Introduced in Enterprise version|
|--------------------|--------------------|--------------------|--------------------|--------------------|
|API update|10|4|4.8|4.8|
|API update|9|4|4.7|4.7|
|API update|8|4|4.6|4.6|
|New flow framework APIs|7|4|4.5|4.5|
|Prevent CorDapp hosting issue|6|4|4.4|4.4|
|Underlying support for accounts|5|4|4.3|4.3|
|Signature constraints|4|4|4.0|4.0|
|Reference states|4|4|4.0|4.0|
|Inline finality flow|4|3|4.0|4.0|
|Whitelist constraints|3|3|3.0|3.0|
|Corda serialization framework|3|3|3.0|3.0|
|Observer nodes|2|2|2.0|n/a|
|Hash constraints|1|1|1.0|1.0|

{{< /table >}}

{{< note >}}
We recommend a network mPV of 5 for Corda 4.5 onwards; however, a network mPV of 4 may continue to work in some instances.
{{< /note >}}
