---
date: '2020-08-10'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-cordapps-versioning
tags:
- versioning
title: Versioning
weight: 2
---


# Versioning

As the Corda platform evolves and new features are added, it's important the versioning system allows users to easily compare versions and know what features are available.

Each Corda release uses the standard semantic versioning scheme of `major.minor`.
This is useful when referring to releases in the public domain, but is not a practical platform versioning system for a developer.

{{< note >}}

The public release version numbers are still useful as every MQ message the node sends includes the `release-version` header property for debugging.

{{< /note >}}

## Platform versioning

The **platform version** is an integer which represents the API version of the Corda platform.
It is similar to Android’s [API Level](https://developer.android.com/guide/topics/manifest/uses-sdk-element.html).
It starts at 1 and increments by 1 for each release which changes any of the publicly exposed APIs in the platform.
This includes public APIs on the node itself, the RPC system, messaging, and serialization. APIs are backwards
compatible and deprecation mechanisms are used to migrate away from old APIs. In very rare
situations APIs may have to be changed, for example due to security issues.

There is no relationship between the platform version
and the release version—a change in the major or minor values may or may not increase the platform version.

The platform version is part of the node’s `NodeInfo` object, which is available from the `ServiceHub`. CorDapps use this to
find out which version a node is running and to determine whether a desired feature is available. When a node
registers with a network map it will check its own version against the network's `minimumPlatformVersion` parameter.
For a node to run on a network, the node's platform version must be greater than or equal to the `minimumPlatformVersion` network parameter. For example, if the `minimumPlatformVersion` of a network is 5, then nodes must be running Corda 4.3 or above to run on the network.

### Features

Features fall into one of three categories and each category has different implications for node operators, CorDapp developers, and business network operators. There are:

* Changes that may affect node operators, but don't impact CorDapp developers or the Corda network protocol. For example, introducing support for a new HSM or database system.
* New or updated APIs.
* Changes that affect the operation of a Corda network. For example, changes to the serialization format, flow/wire protocol, or the introduction of a new transaction component. These are changes to the core data model and should only be taken advantage of if they can be supported by all nodes on a network. Such features are only enabled in a node if the network it connects to has published a `minimumPlatformVersion` in its network parameters that is greater than or equal to the Corda platform version that introduced the feature. For example, Corda 4.0 nodes can only take advantage of the Corda reference states feature when connected to a network with a `minimumPlatformVersion` of 4 (Corda 4.0 is equivalent to Corda platform version 4).

When a release includes features from either of the last two categories, the [Corda platform version](#platform-versioning) is incremented by one.

### Platform version matrix

The table below highlights key features and the corresponding version numbers.

{{< table >}}
|Feature|Corda platform version |Minimum network platform version |Introduced in OS version|Introduced in Enterprise version|
|--------------------|--------------------|--------------------|--------------------|--------------------|
|API update|12|4|4.10|4.10|
|API update|11|4|4.9|4.9|
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
We recommend a minimum network platform version of 5 for Corda 4.5 onwards.
{{< /note >}}

## Minimum platform version

Set your CorDapp's `minimumPlatformVersion` to indicate the oldest compatible platform version.
For example, if your CorDapp uses APIs that were added in Corda 4.3, you should specify a `minimumPlatformVersion` of 5.
This prevents nodes that use an older platform version from running your CorDapp. Nodes that support newer platform versions may also use this field to trigger code paths that emulate behaviors of older platform versions to maximise compatibility.
If your CorDapp can use the new APIs as well as older ones, you can set your CorDapp's `minimumPlatformVersion` to an older version.
Attempting to use new APIs on older nodes can cause `NoSuchMethodError` exceptions and similar problems, so you’d want to check the node version using `ServiceHub.myInfo`.

## Target platform version

If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can indicate this in the `targetPlatformVersion` field.
This allows the node to activate or deactivate backwards compatibility code paths depending on whether they’re necessary or not, as workarounds for CorDapps designed for earlier versions.

For example, if a CorDapp uses features introduced in Corda 4.5 and has passed regression testing on Corda 4.6. It will have a `minimumPlatformVersion` of 7 and a `targetPlatformVersion` of 8.
If the CorDapp is then loaded onto a node running Corda 4.7 (platform version 9), that node may implement backwards compatibility workarounds.
This may impact the CorDapp's performance, security, and features.

Specifying a higher `targetPlatformVersion` allows your CorDapp to take advantage of a newer platform version's behaviors and features if they are available on any given node. However, before doing this you need to thoroughly test your CorDapp against the new platform version. For example, you should ensure your CorDapp exhibits the correct behavior on a node running the new target version, and that it functions
correctly across a network of nodes running the same target version.

We use target versioning as one of the mechanisms to keep evolving and improving the platform, without being permanently constrained to
being bug-for-bug compatible with old versions. When no CorDapps are loaded that target old versions, any emulations of older bugs or problems
can be disabled.


## Publishing versions in your JAR manifest files

The `minimumPlatformVersion` and `targetPlatformVersion` are published in your CorDapp's JAR manifest file of its contract `.jar`.

A well-structured CorDapp should be split into:

* A contracts `.jar` that contains your states and contract logic.
* A workflows `.jar` that contains your flows, services, and other support libraries.

The contract `.jar` defines the data structures and smart contract logic and is attached to each transaction. Nodes on a network then use the contract `.jar` to validate received transactions. Therefore, you need to split your CorDapp across two `.jar`s to avoid sending your flow logic code over the network to third-party peers that don’t need it.

In the `build.gradle` file for your contract `.jar`, add a block like this:

```kotlin
cordapp {
    targetPlatformVersion 10
    minimumPlatformVersion 5
    contract {
        name "MegaApp Contracts"
        vendor "MegaCorp"
        licence "MegaLicence"
        versionId 1
    }
}
```

This will add the necessary entries into your JAR manifest file to set both platform version numbers. If they aren’t specified, both default to 1.
Your CorDapp also has a version number, which should also be an incremental integer.

In the `build.gradle` file for your workflows `.jar`, add a block like this:

```kotlin
cordapp {
    targetPlatformVersion 10
    minimumPlatformVersion 5
    workflow {
        name "MegaApp"
        vendor "MegaCorp"
        licence "MegaLicence"
        versionId 1
    }
}
```

{{< important >}}

The `versionId` specified for the JAR manifest file is currently used for informative purposes only.

{{< /important >}}
