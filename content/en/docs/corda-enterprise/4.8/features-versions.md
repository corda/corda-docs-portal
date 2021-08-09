---
date: '2021-08-09'
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


Each version of Corda introduces new features. Features fall into one of three categories and each category has different implications for node operators, CorDapp developers, and business network operators. There are:

* Changes that may affect node operators, but don't impact CorDapp developers or the Corda network protocol. For example, introducing support for a new HSM or database system.
* New or updated APIs.
* Changes that affect the operation of a Corda network. For example, changes to the serialization format, flow/wire protocol, or the introduction of a new transaction component. These are changes to the core data model and should only be taken advantage of if they can be supported by all nodes on a network. Such features are only enabled in a node if the network it connects to has published a `minimumPlatformVersion` in its network parameters that is greater than or equal to the Corda platform version that introduced the feature. For example, Corda 4.0 nodes which implement Corda platform version 4, can only take advantage of the Corda reference states feature when connected to a network with a `minimumPlatformVersion` of 4.

When a release includes features from either of the last two categories, the [Corda platform version](#corda-features) is incremented by one.

Use `minimumPlatformVersion` to indicate the oldest platform version your CorDapp is compatible with. This prevents nodes that use an older platform version from running your CorDapp. Nodes that support newer platform versions may also use this field to trigger code paths that emulate behaviors that were in force on older platform versions to maximise compatibility.

If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can indicate this in `targetPlatformVersion`. This means it's possible to ship CorDapps that can run on all nodes supporting a minimum platform version of Corda, as well as take advantage of a newer platform version's behaviors and features should they happen to be available on any given node.

See [versioning](cordapps/versioning.md) for more information on how to set your CorDapp's `minimumPlatformVersion` and `targetPlatformVersion`.

{{< table >}}


## Corda features

The table below highlights key features and the corresponding version numbers.

|Feature|Corda platform version |Minimum network platform version (network mPV)|Introduced in OS version|Introduced in Enterprise version|
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
We recommend a network mPV of 5 for Corda 4.5 onwards.
{{< /note >}}
