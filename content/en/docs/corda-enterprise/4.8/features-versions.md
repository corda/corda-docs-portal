---
date: '2021-07-05'
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
* New or changed APIs that will affect CorDapp developers. When a release of Corda ships such features, the Corda platform version (PV) of that node is incremented so that a CorDapp that relies on such a new or changed feature can detect this. It prevents CorDapps from running on a node without the feature or to trigger an alternative optimised codepath if the feature is present). The CorDapp developer sets the CorDapp’s minimumPlatformVersion parameter to signal the minimum Platform Version against which the app can run or has been tested. If the application has also been tested against a greater platform version and can exploit it if present, the node can also set the targetPlatformVersion field.
* Changes that affect the operation of a Corda network. For example, changes to the serialisation format or flow/wire protocol, or the introduction of a new transaction component.  These are changes to the core data model and these features have the property that it is not safe for any node or application to take advantage of until all nodes on the network are capable of understanding them. Such features are thus only enabled in a node if the network to which it is connected has published a minimumPlatformVersion in its network parameters that is greater than or equal to the Corda Platform Version that introduced the feature. For example, Corda 4.0 nodes, which implement Corda Platform Version 4, can only take advantage of the Corda Reference States feature when connected to a network with mPV 4.

You can use the `CorDapp.mPV` element to identify the oldest PV with which your CorDapp is compatible. This prevents nodes that use an older PV from running your CorDapp. Nodes that support newer PVs may also use this field to trigger code paths that emulate behaviours that were in force on older PVs to maximise compatibility. 

If you have tested your CorDapp against newer versions of Corda and found it to be compatible, to take advantage of the new PV's behaviours, you can show this in `CorDapp.targetPV`.  field to declare the latest Platform Version against which the app has been tested
and is known to work. In this way, it is possible to ship CorDapps that can both run on all nodes supporting some minimum Platform Version
of Corda as well as opt in to newer features should they happen to be available on any given node.


{{< table >}}


# Corda features

**The table below highlights key features** 

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
