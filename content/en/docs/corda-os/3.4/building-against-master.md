---
aliases:
- /releases/release-V3.4/building-against-master.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-4:
    identifier: corda-os-3-4-building-against-master
    parent: corda-os-3-4-building-a-cordapp-index
    weight: 1070
tags:
- building
- against
- master
title: Building against Master
---


# Building against Master

It is advisable to develop CorDapps against the most recent Corda stable release. However you may need to build
against the unstable Master branch if you are using a very recent feature, or are testing a PR on the main codebase.

To work against the Master branch, proceed as follows:


* Open a terminal window in the folder where you cloned the Corda repository


(available [here](https://github.com/corda/corda))



* Use the following command to check out the latest master branch:> 
`git checkout master; git pull`

* Publish Corda to your local Maven repository using the following commands:



* Unix/Mac OSX: `./gradlew install`
* Windows: `gradlew.bat install`

By default, the Maven local repository is found at:


* `~/.m2/repository` on Unix/Mac OS X
* `%HOMEPATH%\.m2` on Windows

This step is not necessary when using a stable releases, as the stable releases are published online


{{< warning >}}
If you do modify your local Corda repository after having published it to Maven local, then you must
re-publish it to Maven local for the local installation to reflect the changes you have made.

{{< /warning >}}



{{< warning >}}
As the Corda repository evolves on a daily basis, two clones of the Master branch at different points in
time may differ. If you are using a Master release and need help debugging an error, then please let us know the
**commit** you are working from. This will help us ascertain the issue.

{{< /warning >}}




* Update the `ext.corda_release_version` property in your CorDapp’s root `build.gradle` file to match the version
here: [https://github.com/corda/corda/blob/master/build.gradle#L7](https://github.com/corda/corda/blob/master/build.gradle#L7)

