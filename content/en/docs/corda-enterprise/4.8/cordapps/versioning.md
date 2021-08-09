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

As the Corda platform evolves and new features are added it is important to have a versioning system which allows
its users to easily compare versions and know what features are available to them. Each Corda release uses the standard
semantic versioning scheme of `major.minor`. This is useful when referring to releases in the public domain, but is not
a practical platform versioning system for a developer.

The release version is still useful as every MQ message the node sends includes
the `release-version` header property for debugging purposes.


## Platform versioning

The **platform version** is an incrementing integer which represents the API version of the Corda platform.
It is similar to Android’s [API Level](https://developer.android.com/guide/topics/manifest/uses-sdk-element.html).
It starts at 1 and increments by 1 for each release which changes any of the publicly exposed APIs in the platform.
This includes public APIs on the node itself, the RPC system, messaging, and serialization. API backwards
compatibility will always be maintained, with the use of deprecation to suggest migration away from old APIs. In very rare
situations APIs may have to be changed, for example due to security issues.

There is no relationship between the platform version
and the release version - a change in the major or minor values may or may not increase the platform version.

The platform version is part of the node’s `NodeInfo` object, which is available from the `ServiceHub`. This is used by
CorDapps to find out which version a node is running and to determine whether a desired feature is available. When a node
registers with a network map it will check its own version against the network's `minimumPlatformVersion` parameter.

### Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.8 | 10 |
| 4.7 | 9 |
| 4.6 | 8 |
| 4.5 | 7 |
| 4.4 | 6 |
| 4.3 | 5 |
| 4.2 | 4 |
| 4.1 | 4 |
| 4.0 | 4 |
| 3.3 | 3 |
{{< /table >}}


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
