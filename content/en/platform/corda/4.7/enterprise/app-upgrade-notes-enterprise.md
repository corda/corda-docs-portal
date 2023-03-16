---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: "corda-enterprise-4-7-enterprise-cordapp-upgrade"
    parent: corda-enterprise-4-7-upgrading-menu
tags:
- app
- upgrade
- notes
- enterprise
title: Upgrading a CorDapp to Corda Enterprise Edition 4.7
weight: 20
---




# Upgrading a CorDapp to Corda Enterprise Edition 4.7

{{< warning >}}
Corda Enterprise Edition 4.7.1 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise Edition 4.7.1 please read the guidance on [upgrading your notary service]({{< relref "../../../../../en/platform/corda/4.7/enterprise/notary/upgrading-the-ha-notary-service.md" >}}).
{{< /warning >}}

## Upgrading from Open Source


### Running on Corda Enterprise Edition 4.7

A prerequisite to upgrade to Corda Enterprise Edition 4.7 is to ensure your CorDapp is upgraded to Corda open source 4.7.
Please follow the instructions in [Upgrading CorDapps to newer Platform Versions](app-upgrade-notes.md) section to complete this initial step.

There is no requirement to re-compile your CorDapp to Corda Enterprise in order to run it on Corda Enterprise. If you wish your CorDapp to
be compatible with nodes running Open Source, then compiling against Open Source Corda V4.x will suffice.
However, if you wish to leverage Corda Enterprise specific features, such as 3rd party commercial database support, and do not intend
for your CorDapp to run in an open source production environment, then please follow the instructions [here](#re-compiling-for-corda-enterprise-47)

{{< note >}}
Corda open source and Enterprise Public APIs are currently identical but this may change in future releases of Corda Enterprise.
Please read [Corda and Corda Enterprise compatibility](version-compatibility.md) guarantees.

{{< /note >}}


### Re-compiling for Corda Enterprise Edition 4.7

Re-compiling your CorDapp requires updating its associated Gradle build file as follows:

```shell
corda_release_distribution = 'com.r3.corda'
corda_core_release_distribution = 'net.corda'
corda_release_version = '4.7'
corda_core_release_version = '4.7'
corda_gradle_plugins_version = '5.0.12'
kotlin_version = '1.2.71'
quasar_version = '0.7.13_r3'
```

and specifying an additional repository entry to point to the location of the Corda Enterprise distribution and Corda dependencies. Any
dependencies on `corda-core` and/or `corda-serialization` must use the `corda_core_release_distribution` and
`corda_core_release_version` - as Corda is moving to an open core model, these core APIs are only available in open source and need to
be imported from there. Therefore, a repository entry pointing to a matching Corda Open Source version is always required.

If your project is based on one of the official cordapp templates, it is likely you have a `lib/quasar.jar` checked in.  It is worth noting
that you only use this if you use the JUnit runner in IntelliJ.  In the latest release of the cordapp templates, this directory has
been removed.

As an example:

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

    // Dependency on Corda Open Source
    maven { url "https://software.r3.com/artifactory/corda" }

    // Corda dependencies for the patched Quasar version
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Quasar version
}
```


* Upgrade your `quasar.jar` to the version consistent with your Corda version
* Delete your `lib` directory and switch to using the Gradle test runner

While the Corda Gradle Plugins need no changes apart from the version, ensure that Corda Enterprise dependencies are referenced with the right distribution. As an example:

```shell
cordaCompile "net.corda:corda-core:$corda_release_version"
testCompile "net.corda:corda-node-driver:$corda_release_version"
```

becomes:

```shell
cordaCompile "$corda_core_release_distribution:corda-core:$corda_core_release_version" // core depends on Open Source
testCompile "$corda_release_distribution:corda-node-driver:$corda_release_version"     // node based tests from Enterprise
```

{{< note >}}
Corda Enterprise Edition 4.7 binaries are not available in a public repository. In order to make the dependencies available for development, either
create a mirror repository and upload them there, or add them to the local Maven repository.

Please consult your R3 support contact to request a copy of the Corda Enterprise Developer Pack (this contains a Maven repository mirror
of all Corda Enterprise artifacts and their dependencies).

{{< /note >}}

{{< warning >}}
In Corda 4 the original Finance CorDapp was split into two CorDapps: Contracts and Workflows, both of which are signed JAR files.
To ensure there is only one unique hashed version of the Finance Contracts JAR file (recall, the hash of a Contract JAR file undergoes strict
security checking upon transaction resolution) we only publish a single instance of the Finance Contracts JAR file (from the open source repository).
Please ensure any CorDapps that depend on Finance Contract JAR file reference this open source dependency as follows:

```shell
cordapp "$os_corda_release_distribution:corda-finance-contracts:$os_corda_release_version"
```

where

```shell
ext.os_corda_release_distribution = 'net.corda'
ext.os_corda_release_version = '4.0'
```

{{< /warning >}}



## Upgrading from Enterprise 4.3 or earlier

As of Corda Enterprise Edition 4.4 we have moved towards an open core strategy. Therefore, the common APIs are only available in Corda
Open Source, and Corda Enterprise has a binary dependency on the matching Open Source version. As a result, any CorDapps written against
Corda Enterprise Edition 4.4 or later will have to depend on the open source version of `corda-core`.

Therefore you have to add the following variables to your build configuration:

```shell
corda_core_release_distribution = 'net.corda'
corda_core_release_version = '4.7'
```

Any dependency on `corda-core` (or `corda-serialization`) has to use these new variables to depend on the open source version of those
libraries, so:

```shell
cordaCompile "$corda_release_distribution:corda-core:$corda_release_version"
```

becomes:

```shell
cordaCompile "$corda_core_release_distribution:corda-core:$corda_core_release_version"
```


## Upgrading from Corda Enterprise 3.x

You can only upgrade to Corda Enterprise Edition 4.7 from 4.x. To upgrade from 3.x, first upgrade to 4.x and then to 4.7.
