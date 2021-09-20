---
aliases:
- /head/building-against-non-release.html
- /HEAD/building-against-non-release.html
- /building-against-non-release.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-building-against-non-release
    parent: corda-os-4-6-building-a-cordapp-index
    weight: 1065

tags:
- building
- against
- release
title: Building CorDapps against a non-release branch
---


# Building CorDapps against a non-release branch

It is advisable to develop CorDapps against the most recent Corda stable release. However, you may need to build a CorDapp
against an unstable non-release branch if your CorDapp uses a very recent feature, or you are using the CorDapp to test a PR
on the main codebase.

To work against a non-release branch, proceed as follows:


* Clone the [Corda repository](https://github.com/corda/corda)
* Check out the branch or commit of the Corda repository you want to work against
* Make a note of the `gradlePluginsVersion` in the root `constants.properties` file of the Corda repository
* Clone the [Corda Gradle Plugins repository](https://github.com/corda/corda-gradle-plugins)
* Check out the tag of the Corda Gradle Plugins repository corresponding to the `gradlePluginsVersion`
* Follow the instructions in the readme of the Corda Gradle Plugins repository to install this version of the Corda Gradle plugins locally
* Open a terminal window in the folder where you cloned the Corda repository
* Publish Corda to your local Maven repository using the following commands:



* Unix/Mac OSX: `./gradlew install`
* Windows: `gradlew.bat install`


{{< warning >}}
If you do modify your local Corda repository after having published it to Maven local, then you must
re-publish it to Maven local for the local installation to reflect the changes you have made.

{{< /warning >}}



{{< warning >}}
As the Corda repository evolves on a daily basis, two clones of an unstable branch at different points in
time may differ. If you are using an unstable release and need help debugging an error, then please let us know the
**commit** you are working from. This will help us ascertain the issue.

{{< /warning >}}




* Make a note of the `corda_release_version` in the root `build.gradle` file of the Corda repository.
* In your CorDapp’s root `build.gradle` file:
  * Update `ext.corda_release_version` to the `corda_release_version` noted down earlier.
  * Update `corda_gradle_plugins_version` to the `gradlePluginsVersion` noted down earlier - for Corda Enterprise 4.6 this must be `ext.corda_gradle_plugins_version = '5.0.12'`.
