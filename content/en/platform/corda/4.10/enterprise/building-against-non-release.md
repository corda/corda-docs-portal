---
date: '2021-07-15'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-cordapps

tags:
- building
- against
- release
title: Building CorDapps against a non-release branch
weight: 110
---


# Build a CorDapp against a non-release branch

You should generally develop CorDapps against the most recent Corda stable release. However, you may need to build a CorDapp
against an unstable non-release branch if your CorDapp uses a very recent feature, or you are using the CorDapp to test a PR
on the main codebase.

To work against a non-release branch:


1. Clone the [Corda repository](https://github.com/corda/corda).
2. Check out the branch or commit of the Corda repository you want to work against.
3. Make a note of the `gradlePluginsVersion` in the root `constants.properties` file of the Corda repository.
4. Clone the [Corda Gradle Plugins repository](https://github.com/corda/corda-gradle-plugins).
5. Check out the tag of the Corda Gradle Plugins repository corresponding to the `gradlePluginsVersion`.
6. Follow the instructions in the README of the Corda Gradle Plugins repository to install the correct version of the Corda Gradle plugins locally.
7. Open a terminal window in the folder where you cloned the Corda repository.
8. Publish Corda to your local Maven repository using the following commands:


* Unix/Mac OSX: `./gradlew install`
* Windows: `gradlew.bat install`


{{< warning >}}
If you modify your local Corda repository after publishing it to Maven local, then you must
re-publish it to Maven local for your local installation to reflect the changes you have made.

{{< /warning >}}



{{< warning >}}
As the Corda repository evolves on a daily basis, two clones of an unstable branch at different points in
time may differ. If you are using an unstable release and need help debugging an error, then please let us know the
**commit** you are working from. This will help us ascertain the issue.

{{< /warning >}}




9. Make a note of the `corda_release_version` in the root `build.gradle` file of the Corda repository.
10. In your CorDapp’s root `build.gradle` file:
  1. Update `ext.corda_release_version` to the `corda_release_version` you noted earlier.
  2. Update `corda_gradle_plugins_version` to the `gradlePluginsVersion` you noted earlier - for Corda Enterprise Edition 4.10, this must be `ext.corda_gradle_plugins_version = '5.0.12'`.
