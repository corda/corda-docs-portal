---
date: '2021-09-2012:00:00Z'
title: "CorDapp CPK and CPB Gradle plugins"
linktitle: "Gradle plugins"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-packaging
    identifier: corda-5-dev-preview-1-packaging-gradle-plugin
    weight: 100
section_menu: corda-5-dev-preview
description: >
  Documentation for the CorDapp CPK and CorDapp CPB Gradle plugins
expiryDate: '2022-09-28'  
---

# CorDapp CPK and CPB Gradle plugins

In the Corda 5 Developer Preview, CorDapps are distributed as Corda package files (`.cpk` files), and Corda package bundles (`.cpb` files).

## CorDapp CPK Gradle plugin

Applying the CorDapp CPK Gradle plugin to a Gradle project declares that the project should create a Corda package file (a `.cpk` file).

Corda package files are the standard way to distribute CorDapps for Corda 5. A Corda package file is a `.zip` file with a `.cpk` extension. It is a "jar-of-jars" single distributable for the CorDapp. It contains META-INF files for publisher content signing, and that define versioning and dependencies. The dependency information in the Corda package file defines dependencies based upon version, hash, and publisher key.

The `.cpk` file also contains the main CorDapp `.jar` file and its dependencies, _except_ for Corda's own `.jar` files and `.jar` files that are provided by Corda (such as Kotlin and Quasar).

The main `.jar` file contains enough OSGi metadata to be a valid OSGi bundle.

{{< note >}}
Corda package files are the Corda 5 equivalent of Corda 4's "semi-fat" CorDapp `.jar` files.
{{< /note >}}

### Apply the plugin

Follow these steps to apply the plugin to your Gradle project.

1. In `settings.gradle` for the root Gradle project, make sure the `cordap-configuration` and `cordapp-cpk` plugins are declared.
    ```gradle
            pluginManagement {
            plugins {
                id 'net.corda.cordapp.cordapp-configuration' version cordaReleaseVersion
                id 'net.corda.plugins.cordapp-cpk' version cpkPluginVersion
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
    ```    
    Where `cpkPluginVersion` and `cordaReleaseVersion` are both Gradle properties, for example:

    ```gradle
    cpkPluginVersion = '6.0.0'
    cordaReleaseVersion = '5.0.0'
    ```

    The artifacts for this release are available from https://software.r3.com/artifactory/corda-releases/.

2. Make sure the `build.gradle` file for the root project applies the `cordapp-configuration` plugin.
   ```gradle
        plugins {
            id 'net.corda.cordapp.cordapp-configuration'
        }
   ```
3. Add the following lines to the top of your CPK project's `build.gradle` file.
   ```gradle
        plugins {
            id 'net.corda.plugins.cordapp-cpk'
        }
   ```
    If you just have a single project that builds a `.cpk` file, then you will only have one `build.gradle` file, and the lines from these two steps should be combined.

    ````gradle
    plugins {
        id 'net.corda.cordapp.cordapp-configuration'
        id 'net.corda.plugins.cordapp-cpk'
    }
    ````

4. Add a `cordapp` block to the CPK project's `build.gradle`. For example,
   ```gradle
        cordapp {
            targetPlatformVersion = 999
            workflow {
              name = 'Example CorDapp'
              versionId = 1
              licence = 'Test-Licence'
              vendor = 'R3'
            }
        }
   ```
    The CorDapp block is [described below](#the-cordapp-block). For an example, see the [DSL section](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk#dsl) of the [cordapp-cpk README](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk).

#### The `cordapp` block

The `cordapp` block _must_ contain a `targetPlatformVersion` field, and either a `workflow` or `contract` block. It may also contain a `signing` block as well as `minimumPlatformVersion`, `sealing`, and `hashAlgorithm` fields.

{{% table %}}
| Field name             | Description                             |
|------------------------|-----------------------------------------|
|`targetPlatformVersion` | The target Corda Platform version       |
|`minimumPlatformVersion`| The minimum Corda Platform version      |
|`sealing`               | Set to `true` or `false`                |
|`hashAlgorithm`         | The hash algorithm, such as `'SHA-256'` |
{{% /table %}}

For development purposes, it is usually safe to use the defaults for  `signing`, `sealing`, `minimumPlatformVersion` and `hashAlgorithm`.

The `cordapp-cpk` plugin signs with a development key by default. When generating a `.cpk` file for production, you will need to provide a key of your own.

You can also configure a signing key by setting these Java system properties on the Gradle command line:

* `signing.alias`
* `signing.storepass`
* `signing.keystore`
* `signing.storetype`
* `signing.keypass`
* `signing.sigfile`


##### The `workflow` and `contract` blocks

The `workflow` and `contract` blocks should contain the following fields.

{{% note %}}
Remember, you should only use a `workflow` block _or_ a `contract` block, not both. The plugin does not enforce this; however, a `contract` `.cpk` will be added to the ledger and so R3 strongly advises you to keep the contracts and the workflows separate!
{{% /note %}}

{{% table %}}

| Field name | Description                                                             |
|------------|-------------------------------------------------------------------------|
|`name`      | The CorDapp's name. Maps to `Bundle-Name` OSGi manifest tag.            |
|`versionID` | The CorDapp's version.                                                  |
|`licence`   | The CorDapp's license name. Maps to `Bundle-License` OSGi manifest tag. |
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

### Generate the Corda package file

To generate the `.cpk` file, run `./gradlew build`. The `.cpk` file will be generated alongside the `.jar` file.

## Tuning the OSGi Metadata

In most circumstances, the `cordapp-cpk` plugin correctly generates the OSGi metadata. However, the `cordapp-cpk` plugin also extends Gradle's `jar` task with an `osgi` block. This can be used to tune the OSGi metadata. For more information, see [Tuning OSGi metadata](../../../../../../en/platform/corda/5.0-dev-preview-1/packaging/gradle-plugin/tuning-osgi-metadata.md).

## CorDapp CPB Gradle plugin

Applying the CorDapp CPB Gradle plugin to a Gradle project declares that the project should create a Corda package bundle (a `.cpb` file).

The point of the `.cpb` is to contain all of the `.cpk`s that are expected to be deployed together as a single application. So in a typical example, you would apply `net.corda.plugins.cordapp-cpk` for the contract CPK project, and `net.corda.plugins.cordapp-cpb` in the workflows CPB project. The `.cpb` file would then contain both your contracts and your workflows' `.cpk`s.

### Apply the plugin

The CorDapp CPB Gralde plugin automatically applies the CorDapp CPK plugin, so before appling the CPB plugin, you should make sure the CPK plugin is configured as described above.

1. In `settings.gradle` for the root Gradle project, make sure the `cordapp-cpb` plugin is declared.
   ```gradle
        pluginManagement {
            plugins {
                // Other plugins will also be declared here
                id 'net.corda.plugins.cordapp-cpb' version cpkPluginVersion
            }
        }
   ```
2. Add the following lines to the top of the sub-project's `build.gradle` file.
   ```gradle
        plugins {
            id 'net.corda.plugins.cordapp-cpb'
        }
   ```
The plugin will normally determine all of the CorDapp's transient `.cpk` dependencies, although it is your responsibility to ensure that this set is complete. See [CPK inspection tool](../../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/commands.md) for details of how to inspect the contents of the bundle.

Any extra package references can be added to the bundle using the `cpb` Gradle configuration. For example:
   ```gradle
        dependencies {
            cpb "com.example.foo:some-cpk:1.0.0"
            cpb "com.example.bar:other-cpk:2.0.0"
        }
   ```
### Generate the Corda package bundle

To generate the `.cpb` file, run `./gradlew build`. The `.cpk` file will be generated in the normal Gradle output directory.
