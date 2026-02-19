---
date: '2021-08-11'
menu:
  corda-enterprise-4.14:
    identifier: "corda-enterprise-4.14-enterprise-cordapp-upgrade"
    parent: corda-enterprise-4.14-upgrading-menu
tags:
- app
- upgrade
- notes
- enterprise
title: Upgrading a CorDapp to Corda Enterprise Edition 4.14
weight: 20
---

# Upgrading a CorDapp to Corda Enterprise Edition 4.14

## Upgrading from Corda Open Source Edition

Before upgrading to Corda Enterprise Edition 4.14, upgrade your CorDapp to Corda Open Source Edition 4.14. See [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}) for detailed instructions.

You do not need to re-compile your CorDapp to Corda Enterprise for it to run on Corda Enterprise. If you want your CorDapp to
be compatible with nodes running open source, then compile it against Corda Open Source Edition 4.x.
However, if you want to leverage specific features of Corda Enterprise, such as third-party commercial database support, and do not envisage your CorDapp being run in an open source production environment, then follow the [re-compiling for Corda Enterprise Edition 4.13]({{< relref "#re-compiling-for-corda-enterprise-edition-413" >}}) guide.

{{< note >}}
Corda Enterprise and Corda Open Source Edition public APIs are currently identical. However, this may change for future releases.
See [Corda and Corda Enterprise compatibility]({{< relref "version-compatibility.md" >}}) guarantees for further information.

{{< /note >}}


### Re-compiling for Corda Enterprise Edition 4.14

To re-compile your CorDapp for Corda Enterprise Edition 4.14, you need to:

1. Update your Gradle build file as follows.
    ```shell
    corda_release_distribution = 'com.r3.corda'
    corda_core_release_distribution = 'net.corda'
    corda_release_version = '4.14'
    corda_core_release_version = '4.14'
    corda_gradle_plugins_version = '5.1.1'
    kotlin_version = '1.9.20'4
    quasar_version = '0.9.2_r3'
    ```
2. Specify an additional repository entry pointing to the location of the Corda Enterprise distribution and Corda dependencies. Any
dependencies on `corda-core` and/or `corda-serialization` must use the `corda_core_release_distribution` and
`corda_core_release_version`. As Corda is moving to an open core model, these core APIs are only available in open source and need to
be imported from there. Therefore, a repository entry pointing to a matching Corda Open Source Edition version is required.
3. Update your `quasar.jar` file. If your project is based on one of the official CordApp templates, you'll likely have a `lib/quasar.jar` file checked in. You'll only use this if you use the JUnit runner in IntelliJ. In the latest release of the CorDapp templates, this directory has
been removed. For example:
    ```shell
    repositories {
        // Example for Corda Enterprise
        maven {
            credentials {
                username "username"
                password "XXXXX"
            }
            url 'https://artifactory.mycompany.com/artifactory/corda-enterprise'
        }

        // Dependency on Corda Open Source Edition
        maven { url 'https://download.corda.net/maven/corda-releases' }
        maven { url 'https://download.corda.net/maven/corda-dependencies' }

        // Corda dependencies for the patched Quasar version
        maven { url "https://download.corda.net/maven/corda-dependencies" } // access to the patched Quasar version
    }
    ```

   You can do either of the following:

   * Upgrade your `quasar.jar` file to the version consistent with your Corda version.
   * Delete your `lib` directory and switch to using the Gradle test runner.

   You can find instructions for both options in [Running tests in IntelliJ]({{< relref "testing.md#running-tests-in-intellij" >}}).

4. Check you are using Corda Gradle plugins version 5.1.1 and that Corda Enterprise dependencies are referenced with the right distribution.


    For example:

    ```shell
    cordaCompile "net.corda:corda-core:$corda_release_version"
    testCompile "net.corda:corda-node-driver:$corda_release_version"
    ```


    Becomes:

    ```shell
    cordaCompile "$corda_core_release_distribution:corda-core:$corda_core_release_version" // core depends on open source
    testCompile "$corda_release_distribution:corda-node-driver:$corda_release_version"     // node based tests from Enterprise
    ```

{{< note >}}
Corda Enterprise Edition 4.14 binaries are not publicly available. To make the dependencies available for development, either
create a mirror repository and upload them there, or add them to your local Maven repository.

You can request a copy of the Corda Enterprise Developer Pack (contains a Maven repository mirror
of all Corda Enterprise artifacts and their dependencies) from your R3 support contact.

{{< /note >}}

{{< warning >}}

Version 4.x of the finance CorDapp is split into the following two signed JAR files:

 * `corda-finance-contracts.jar`
 * `corda-finance-workflows.jar`

As there should only be one unique hashed version of `corda-finance-contracts.jar` (the hash of a contract JAR file undergoes strict
security checking upon transaction resolution), only a single instance of `corda-finance-contracts.jar` is published, and this is from the open source repository.

Please ensure any CorDapps that depend on `corda-finance-contracts.jar` reference this open source dependency as follows:

```shell
cordapp "$os_corda_release_distribution:corda-finance-contracts:$os_corda_release_version"
```

Where:
* ext.os_corda_release_distribution = 'net.corda'.
* ext.os_corda_release_version = '4.13'.


{{< /warning >}}



## Upgrading from Enterprise 4.11 or earlier

Corda Enterprise Edition 4.12 moved to Java version 17 and Kotlin version 1.9 therefore CorDapps used with Corda 4.12 also need to be compiled with Java version 17 and Kotlin version 1.9. To make CorDapps backwards compatible there are a specific set of steps to follow, these are outlined in [Upgrade 4.11 CorDapps]({{< relref "upgrade-guide.md#upgrade-411-cordapps">}}).

## Upgrading from Enterprise 4.3 or earlier

Corda Enterprise Edition 4.4 moved towards an open core strategy. Therefore, the common APIs are only available in Corda
open source, and Corda Enterprise has a binary dependency on the matching open source version. As a result, any CorDapps written against
Corda Enterprise Edition 4.4 or later will have to depend on the open source version of `corda-core`.

Therefore, you have to add the following variables to your build configuration:

```shell
ext.corda_core_release_distribution = 'net.corda'
ext.corda_core_release_version = '4.12'
```

Any dependency on `corda-core` (or `corda-serialization`) has to use these new variables to depend on the open source version of those
libraries, as follows:

```shell
cordaCompile "$corda_release_distribution:corda-core:$corda_release_version"
```

Becomes:

```shell
cordaCompile "$ext.corda_core_release_distribution:corda-core:$ext.corda_core_release_version"
```


## Upgrading from Corda Enterprise 3.x

You can only upgrade to Corda Enterprise Edition 4.12 from a previous 4.x version. To upgrade from 3.x, first upgrade to 4.x and then to 4.12. For example, 3.3 to 4.5, and then 4.5 to 4.11.
