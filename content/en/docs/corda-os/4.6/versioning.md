---
aliases:
- /head/versioning.html
- /HEAD/versioning.html
- /versioning.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-versioning
    parent: corda-os-4-6-versioning-and-upgrades
    weight: 1020
tags:
- versioning
title: Versioning
---


# Versioning

As the Corda platform evolves and new features are added it becomes important to have a versioning system which allows
its users to easily compare versions and know what feature are available to them. Each Corda release uses the standard
semantic versioning scheme of `major.minor`. This is useful when making releases in the public domain but is not
friendly for a developer working on the platform. It first has to be parsed and then they have three separate segments on
which to determine API differences. The release version is still useful and every MQ message the node sends attaches it
to the `release-version` header property for debugging purposes.


## Platform version

It is much easier to use a single incrementing integer value to represent the API version of the Corda platform, which
is called the *platform version*. It is similar to Android’s [API Level](https://developer.android.com/guide/topics/manifest/uses-sdk-element.html).
It starts at 1 and will increment by exactly 1 for each release which changes any of the publicly exposed APIs in the
entire platform. This includes public APIs on the node itself, the RPC system, messaging, serialisation, etc. API backwards
compatibility will always be maintained, with the use of deprecation to suggest migration away from old APIs. In very rare
situations APIs may have to be changed, for example due to security issues. There is no relationship between the platform version
and the release version - a change in the major or minor values may or may not increase the platform version. However
we do endeavour to keep them synchronised for now, as a convenience.

The platform version is part of the node’s `NodeInfo` object, which is available from the `ServiceHub`. This enables
a CorDapp to find out which version it’s running on and determine whether a desired feature is available. When a node
registers with the network map it will check its own version against the minimum version requirement for the network.


## Minimum platform version

Applications can advertise a *minimum platform version* they require. If your app uses new APIs that were added in (for example) Corda 5,
you should specify a minimum version of 5. This will ensure the app won’t be loaded by older nodes. If you can *optionally* use the new
APIs, you can keep the minimum set to a lower number. Attempting to use new APIs on older nodes can cause `NoSuchMethodError` exceptions
and similar problems, so you’d want to check the node version using `ServiceHub.myInfo`.


## Target version

Applications can also advertise a *target version*. This is similar to the concept of the same name in Android and iOS.
Apps should advertise the highest version of the platform they have been tested against. This allows the node to activate or deactivate
backwards compatibility codepaths depending on whether they’re necessary or not, as workarounds for apps designed for earlier versions.

For example, consider an app that uses new features introduced in Corda 4, but which has passed regression testing on Corda 5. It will
advertise a minimum platform version of 4 and a target version of 5. These numbers are published in the JAR manifest file.

If this app is loaded into a Corda 6 node, that node may implement backwards compatibility workarounds for your app that make it slower,
less secure, or less featureful. You can opt-in to getting the full benefits of the upgrade by changing your target version to 6. By doing
this, you promise that you understood all the changes in Corda 6 and have thoroughly tested your app to prove it works. This testing should
include ensuring that the app exhibits the correct behaviour on a node running at the new target version, and that the app functions
correctly in a network of nodes running at the same target version.

Target versioning is one of the mechanisms we have to keep the platform evolving and improving, without being permanently constrained to
being bug-for-bug compatible with old versions. When no apps are loaded that target old versions, any emulations of older bugs or problems
can be disabled.

## Platform version matrix

{{< table >}}
| Corda release  | Platform version |
| :------------- | :------------- |
| 4.6 | 8 |
| 4.5 | 7 |
| 4.4 | 6 |
| 4.3 | 5 |
| 4.2 | 4 |
| 4.1 | 4 |
| 4.0 | 4 |
| 3.3 | 3 |
{{< /table >}}

## Publishing versions in your `.jar` manifests

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
    targetPlatformVersion 5
    minimumPlatformVersion 4
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
    targetPlatformVersion 5
    minimumPlatformVersion 4
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

### CorDapp(s) `minimumPlatformVersion` is less than the required `minimumPlatformVersion`

The required minimum platform version that the nodes must be running on is defined. If any of the CorDapps is below this value, the node will shut down
and an `InvalidCordappException` will be thrown.
The following error message will be received before the node shuts down:

```
[ERROR] 17:10:11+0100 [main] internal.NodeStartupLogging. - Invalid Cordapps found, that couldn't be loaded:
[Problem: CorDapp requires minimumPlatformVersion: 7, but was: 2 in Cordapp
file:/corda-open-source/samples/bank-of-corda-demo/build/nodes/BankOfCorda/cordapps/bank-of-corda-demo-4.6-SNAPSHOT.jar
```

For more information on how to address this, see the [Release new CorDapp versions](upgrading-cordapps.md) page.
