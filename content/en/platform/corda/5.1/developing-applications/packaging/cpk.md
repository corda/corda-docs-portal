---
description: "Learn how to create a Corda Package (CPK) file."
date: '2023-02-23'
title: "Build a CPK"
menu:
  corda51:
    parent: corda51-develop-packaging
    identifier: corda51-develop-packaging-cpk
    weight: 1000
---
# Build a CPK

This section describes how to create CPKs. It contains the following:

* [Configure your Project]({{< relref "#configure-your-project" >}})
* [Sign Your Code]({{< relref "#sign-your-code" >}})
* [Create the CPK File]({{< relref "#create-the-cpk-file" >}})

## Configure your Project

To configure your CPK project:

1. Add the CPK plugin to your project by adding the following to the start of the `build.gradle` file of your {{< tooltip >}}CorDapp{{< /tooltip >}} Gradle project:
   ```
   plugins {
       id 'net.corda.plugins.cordapp-cpk2'
   }
   ```
2. Apply the `net.corda.cordapp.cordapp-configuration plugin` to your root Gradle project, to configure the `cordapp-cpk2` plugin for your version of Corda:
   ```
   plugins {
       id 'net.corda.cordapp.cordapp-configuration'
   }
   ```
   If your Gradle project only contains a single module, apply both plugins together:
   ```
   plugins {
       id 'net.corda.cordapp.cordapp-configuration'
       id 'net.corda.plugins.cordapp-cpk2'
    }
   ```

3. Declare both plugins' versions in the `settings.gradle` file:
   ```
   pluginManagement {
       plugins {
           id 'net.corda.cordapp.cordapp-configuration' version cordaReleaseVersion
           id 'net.corda.plugins.cordapp-cpk2' version cpkPluginVersion
       }
   }
   ```
   `cpkPluginVersion` and `cordaReleaseVersion` are both Gradle properties. For example:
   ```
   cpkPluginVersion = '6.0.0'
   cordaReleaseVersion = '{{<version-num>}}.0'
   ```

## Sign Your Code

{{< note >}}
By default, the CPK plugin signs with a default key. This key should only be used for local testing. It is not secure and not intended for use in an environment that is long lived or visible to many people.
{{< /note >}}

To sign with a key other than the default key, add a `cordapp/signing` section to the project `settings.gradle` file.

## Create the CPK File

1. Run the `jar` Gradle task:
   ```
   ./gradlew jar
   ```
