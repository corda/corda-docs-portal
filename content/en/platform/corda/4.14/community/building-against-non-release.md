---
aliases:
- /head/building-against-non-release.html
- /HEAD/building-against-non-release.html
- /building-against-non-release.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4.14:
    identifier: corda-community-4.14-building-against-non-release
    parent: corda-community-4.14-building-a-cordapp-index
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

1. Clone the [Corda repository](https://github.com/corda/corda).
2. Check out the branch or commit of the Corda repository you want to work against.
3. Make a note of the `gradlePluginsVersion` in the root `constants.properties` file of the Corda repository.
4. Clone the [Corda Gradle plugins repository](https://github.com/corda/corda-gradle-plugins).
5. Check out the tag of the Corda Gradle Plugins repository corresponding to the `gradlePluginsVersion`.
6. Follow the instructions in the readme of the Corda Gradle plugins repository to install this version of the Corda Gradle plugins locally.
7. Open a terminal window in the folder where you cloned the Corda repository.
8. Publish Corda to your local Maven repository using the relevant command:

   * Unix/macOS: `./gradlew publishToMavenLocal`
   * Windows: `gradlew.bat publishToMavenLocal`

   {{< warning >}}
   If you do modify your local Corda repository after having published it to Maven local, then you must
   re-publish it to Maven local for the local installation to reflect the changes you have made.
   {{< /warning >}}

   {{< note >}}
   As the Corda repository evolves on a daily basis, two clones of an unstable branch at different points in
   time may differ. If you are using an unstable release and need help debugging an error, then please let us know the
   **commit** you are working from. This will help us ascertain the issue.
   {{< /note >}}

9. Make a note of the `corda_release_version` in the root `build.gradle` file of the Corda repository.
10. In your CorDapp’s root `build.gradle` file:
    1. Update `ext.corda_release_version` to the `corda_release_version` noted down earlier.
    2. Update `corda_gradle_plugins_version` to the `gradlePluginsVersion` noted down earlier: for Corda Enterprise Edition 4.12 this must be `ext.corda_gradle_plugins_version = '5.1.1'`.
