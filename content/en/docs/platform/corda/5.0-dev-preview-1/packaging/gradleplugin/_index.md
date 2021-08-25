---
title: "CorDapp CPK Gradle plugin"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-packaging
    identifier: corda-5-dev-preview-1-packaging-gradle
    weight: 100
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Documentation for the CordDapp CPK Gradle plugin
---

# CorDapp CPK Gradle plugin


Applying the CorDapp CPK Gradle plugin to a Gradle project declares that the project should create a Corda package file (a `.cpk` file).

Corda package files are the standard way to distribute CorDapps for Corda 5. A Corda package file is a `.zip` file with a `.cpk` extension. It is a "jar-of-jars" single distributable for the CorDapp. It contains META-INF files for publisher content signing, and that define versioning and dependencies. The dependency information in the Corda package file defines dependencies based upon version, hash, and publisher key.

The `.cpk` file also contains the main CorDapp `.jar` file and its dependencies, _except_ for Corda's own `.jar` files and `.jar` files that are provided by Corda (such as Kotlin and Quasar).

The main `.jar` file contains enough OSGi metadata to be a valid OSGi bundle.

For more information, see [The Proposed Packaging Model](/engineering-central/teams/architecture/cordapp-packaging-and-isolation/#the-proposed-packaging-model).

{{% note %}}
Corda package files are the Corda 5 equivalent of Corda 4's "semi-fat" CorDapp `.jar` files.
{{% /note %}}

{{% note %}}
If your project requires access to private artifacts, always use tokens in preference to passwords, whenever your credentials need to be stored in the clear. Never store or write down your password. For more information, see [Add Artifactory credentials locally to your build](/library/developer-tips/add-artifactory-cred-local/).
{{% /note %}}

## Apply the plugin

Follow these steps to apply the plugin to your Gradle project.

1. In `settings.gradle` for the root Gradle project, make sure the `cordap-configuration` and `cordapp-cpk` plugins are declared.

        pluginManagement {
            plugins {
                id 'net.corda.cordapp.cordapp-configuration' version cordaReleaseVersion
                id 'net.corda.plugins.cordapp-cpk' version gradlePluginsVersion
            }
            repositories {
                maven {
                    // Corda Gradle plugins fetched from here.
                   url = 'https://software.r3.com/artifactory/corda-releases'
                }
                maven {
                    // Corda Configuration plugin fetched from here
                    url = 'https://software.r3.com/artifactory/corda'
                }
            }
        }

    {{% note %}}
The beta release URL is https://software.r3.com/artifactory/corda-dev. The dev preview artifacts will be available from a different URL.
    {{% /note %}}

2. Make sure the `build.gradle` file for the root project applies the `cordapp-configuration` plugin.

        plugins {
            id 'net.corda.cordapp.cordapp-configuration'
        }

3. Add the following lines to the top of the sub-project's `build.gradle` file.

        plugins {
            id 'net.corda.plugins.cordapp-cpk'
        }

    {{% note %}}
If you just have a single project that builds a `.cpk` file, then you will only have one `build.gradle` file, and the lines from these two steps should be combined.

````
plugins {
    id 'net.corda.cordapp.cordapp-configuration'
    id 'net.corda.plugins.cordapp-cpk'
}
````
    {{% /note %}}  

4. Add a `cordapp` block to the sub-project's `build.gradle`. For example,

        cordapp {
            targetPlatformVersion = 999
            workflow {
              name = 'Example CorDapp'
              versionId = 1
              licence = 'Test-Licence'
              vendor = 'R3'
            }
        }

    The CorDapp block is [described below](#the-cordapp-block). For an example, see the [DSL section](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk#dsl) of the [`cordapp-cpk` README](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk).

### The `cordapp` block

The `cordapp` block _must_ contain a `targetPlatformVersion` field, and either a `workflow` or `contract` block. It may also contain a `signing` block as well as `minimumPlatformVersion`, `sealing`, and `hashAlgorithm` fields.

{{% table %}}
| Field name             | Description                             |
|------------------------|-----------------------------------------|
|`targetPlatformVersion` | The target Corda Platform version       |
|`minimumPlatformVersion`| The minimum Corda Platform version      |
|`sealing`               | Set to `true` or `false`                |
|`hashAlgorithm`         | The hash algorithm, such as `'SHA-256'` |
{{% /table %}}

For develeopment purposes, it is usually safe to use the defaults for  `signing`, `sealing`, `minimumPlatformVersion` and `hashAlgorithm`.

The `cordapp-cpk` plugin signs with a development key by default. When generating a `.cpk` file for production, you will need to provide a key of your own.

You can also configure a signing key by setting these Java system properties on the Gradle command line:

* `signing.alias`
* `signing.storepass`
* `signing.keystore`
* `signing.storetype`
* `signing.keypass`
* `signing.sigfile`


#### The `workflow` and `contract` blocks

The `workflow` and `contract` blocks should contain the following fields.

{{% note %}}
Remember, you should only use a `workflow` block _or_ a `contract` block, not both.
{{% /note %}}

{{% table %}}

| Field name | Description                                                             |
|------------|-------------------------------------------------------------------------|
|`name`      | The CorDapp's name. Maps to `Bundle-Name` OSGi manifest tag.            |
|`versionID` | The CorDapp's version.                                                  |
|`licence`   | The Cordapp's license name. Maps to `Bundle-License` OSGi manifest tag. |
|`vendor`    | The vendor's name. Maps tp `Bundle-Vendor` OSGi manifest tag.           |
{{% /table %}}

#### The `signing` block

The `signing` block contains an `enabled` field and an `options` block.

Set `enabled` to `true` to enable signing, and to `false` to disable.

The `options` block contains the following fields, which mirror Ant's `signJar` task options.

* `alias`
* `storePassword`
* `keyStore`
* `storeType`
* `keyPassword`
* `signatureFileName`
* `signedJar`
* `verbose`
* `strict`
* `internalSF`
* `sectionsOnly`
* `lazy`
* `maxMemory`
* `preserveLastModified`
* `tsaUrl`
* `tsaCert`
* `tsaProxyHost`
* `tsaProxyPort`
* `executable`
* `force`
* `signatureAlgorithm`
* `digestAlgorithm`
* `tsaDigestAlgorithm`

### Tuning the OSGi Metadata

In most circumstances, the `cordapp-cpk` plugin correctly generates the OSGi metadata. However, the `cordapp-cpk` plugin also extends Gradle's `jar` task with an `osgi` block. This can be used to tune the OSGi metadata. For more information, see [Tuning OSGi metadata](tuningosgimetadata.md)

## Generate the CPK file

To generate the `.cpk` file, run `./gradlew build`. The `.cpk` file will be generated alongside the `.jar` file.

## Further reading
* [The Proposed Packaging Model](/engineering-central/teams/architecture/cordapp-packaging-and-isolation/#the-proposed-packaging-model)
* [Cordapp CPK Gradle Plugin Readme](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk)
* [Corda CPK Metadata Format](https://github.com/corda/platform-eng-design/blob/996d0e31a9991b509b41db29f528fac208b91ba8/core/corda-5/corda-5.0/cpk/cpk-metadata-format.md)
