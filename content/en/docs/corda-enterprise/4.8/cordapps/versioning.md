---
date: '2020-08-09'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-cordapps-versioning
tags:
- versioning
title: Versioning
weight: 2
---


# Versioning

As the Corda platform evolves and new features are added,
it is important to have a versioning system that allows users to easily compare versions and know what features are available.

Each Corda release uses the standard semantic versioning scheme of `major.minor`.
This is useful when referring to releases in the public domain, but is not a practical platform versioning system for a developer.

{{< note >}}

The public release versions are still useful as every MQ message the node sends includes the `release-version` header property for debugging purposes.

{{< /note >}}

Each version of Corda introduces new features. Features fall into one of three categories and each category has different implications for node operators, CorDapp developers, and business network operators. There are:

* Changes that may affect node operators, but don't impact CorDapp developers or the Corda network protocol. For example, introducing support for a new HSM or database system.
* New or updated APIs.
* Changes that affect the operation of a Corda network. For example, changes to the serialization format, flow/wire protocol, or the introduction of a new transaction component. These are changes to the core data model and should only be taken advantage of if they can be supported by all nodes on a network. Such features are only enabled in a node if the network it connects to has published a `minimumPlatformVersion` in its network parameters that is greater than or equal to the Corda platform version that introduced the feature. For example, Corda 4.0 nodes can only take advantage of the Corda reference states feature when connected to a network with a `minimumPlatformVersion` of 4 (Corda 4.0 is equivalent to Corda platform version 4).

When a release includes features from either of the last two categories, the [Corda platform version](#platform-versioning) is incremented by one.








For a node to run on a network, the node's platform version must be greater than or equal to the `minimumPlatformVersion` network parameter. For example, if the `minimumPlatformVersion` of a network is 5, then nodes must be running Corda 4.3 or above to run on the network.

Use your CorDapp's `minimumPlatformVersion` parameter to indicate the oldest platform version your CorDapp is compatible with. This prevents nodes that use an older platform version from running your CorDapp. Nodes that support newer platform versions may also use this field to trigger code paths that emulate behaviors that were in force on older platform versions to maximise compatibility.

If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can indicate this in `targetPlatformVersion`. This means it's possible to ship CorDapps that can run on all nodes supporting a minimum platform version of Corda, as well as take advantage of a newer platform version's behaviors and features should they happen to be available on any given node.






## Platform versioning

The **platform version** is an incrementing integer which represents the API version of the Corda platform.
It is similar to Android’s [API Level](https://developer.android.com/guide/topics/manifest/uses-sdk-element.html).
It starts at 1 and increments by 1 for each release that changes any of the publicly exposed APIs in the platform.
This includes public APIs on the node itself, the RPC system, messaging, and serialization. API backwards
compatibility will always be maintained, using deprecation to migrate away from old APIs. In very rare
situations APIs may have to be changed, for example due to security issues.

There is no relationship between the platform version
and the release version - a change in the major or minor values may or may not increase the platform version.

The platform version is part of the node’s `NodeInfo` object, which is available from the `ServiceHub`. This is used by
CorDapps to find out which version a node is running and to determine whether a desired feature is available. When a node
registers with a network map it will check its own version against the network's `minimumPlatformVersion` parameter.

### Platform version matrix

The table below highlights key features and the corresponding version numbers.

{{< table >}}

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


## Minimum platform version

Your CorDapp's `minimumPlatformVersion` indicates the oldest platform version your CorDapp is compatible with.
For example, if your CorDapp uses APIs that were added in Corda 4.3, you should specify a `minimumPlatformVersion` of 5.
This prevents nodes that use an older platform version from running your CorDapp.
If your CorDapp can use the new APIs as well as older ones, you can set your CorDapp's `minimumPlatformVersion` to an older version.
Attempting to use new APIs on older nodes can cause `NoSuchMethodError` exceptions and similar problems, so you’d want to check the node version using `ServiceHub.myInfo`.


## Target platform version

If you have tested your CorDapp against newer versions of Corda and found it to be compatible, you can indicate this in `targetPlatformVersion`.
This allows the node to activate or deactivate backwards compatibility code paths depending on whether they’re necessary or not, as workarounds for CorDapps designed for earlier versions.

For example, if a CorDapp uses features introduced in Corda 4.5 and has passed regression testing on Corda 4.6. It will have a `minimumPlatformVersion` of 7 and a `targetPlatformVersion` of 8.
If this CorDapp is then loaded into a node running Corda 4.7 (platform version 9), that node may implement backwards compatibility workarounds,
potentially making the CorDapp slower, less secure, or less featureful.

Specifying a higher `targetPlatformVersion` allows your CorDapp

You can opt-in to getting the full benefits of the upgrade by changing your target version to 6. By doing
this, you promise that you understood all the changes in Corda 6 and have thoroughly tested your app to prove it works. This testing should
include ensuring that the app exhibits the correct behaviour on a node running at the new target version, and that the app functions
correctly in a network of nodes running at the same target version.

Target versioning is one of the mechanisms we have to keep the platform evolving and improving, without being permanently constrained to
being bug-for-bug compatible with old versions. When no apps are loaded that target old versions, any emulations of older bugs or problems
can be disabled.


## Publishing versions in your JAR manifests

These numbers are published in the JAR manifest file.

A well structured CorDapp should be split into two separate modules:


* A contracts jar, that contains your states and contract logic.
* A workflows jar, that contains your flows, services and other support libraries.

The reason for this split is that the contract JAR will be attached to transactions and sent around the network, because this code is what
defines the data structures and smart contract logic all nodes will validate. If the rest of your app is a part of that same JAR, it’ll get
sent around the network too even though it’s not needed and will never be used. By splitting your app into a contracts JAR and a workflows
JAR that depends on the contracts JAR, this problem is avoided.

In the `build.gradle` file for your contract module, add a block like this:

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

This will put the necessary entries into your JAR manifest to set both platform version numbers. If they aren’t specified, both default to 1.
Your app can itself has a version number, which should always increment and must also always be an integer.

And in the `build.gradle` file for your workflows jar, add a block like this:

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

It’s entirely expected and reasonable to have an open source contracts module and a proprietary workflow module - the latter may contain
sophisticated or proprietary business logic, machine learning models, even user interface code. There’s nothing that restricts it to just
being Corda flows or services.


{{< important >}}
The `versionId` specified for the JAR manifest is currently used for informative purposes only.


{{< /important >}}
