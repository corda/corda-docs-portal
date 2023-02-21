---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-cordapps
tags:
- cordapp
- build
- systems
title: Build a CorDapp
weight: 100
---

# Build a CorDapp

This article covers the steps you need to take to build a CorDapp from scratch. You'll learn how to:

* Set dependencies
* Create and install CorDapp `.jar` files
* Configure your CorDapp.
* Set minimum and target platform versions.
* Separate CorDapp contracts, flows, and services.
* Attach contracts.

Code samples guide you at every step.


## Before you start

You will need to:

* Know [what a CorDapp is](cordapp-overview.md).
* Set up your [development environment](getting-set-up.md).
* Run a [sample CorDapp](tutorial-cordapp.md) to see Corda in action (optional).
* Install the [CorDapp Gradle plugin](https://plugins.gradle.org/plugin/net.corda.plugins.cordapp). To ensure you are using the correct version of Gradle, use the Gradle wrapper provided. Copy across the following folder and files from the [Kotlin CorDapp Template](https://github.com/corda/cordapp-template-kotlin) or the [Java CorDapp Template](https://github.com/corda/cordapp-template-java) to your project's root directory:

    * `gradle/`
    * `gradlew`
    * `gradlew.bat`

{{< note >}}
You can write CorDapps in any language that targets the JVM. However, Corda itself and most of the samples are written in Kotlin. If you’re unfamiliar with Kotlin and want to learn more, you can refer to their [getting started guide](https://kotlinlang.org/docs/tutorials/), and series of [Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html).
{{< /note >}}


## Set dependencies

Your CorDapp will have certain *dependencies*, or requirements that must be met for the CorDapp to run correctly. You need to specify:
* Which versions of Corda, Quasar, and Kotlin your CorDapp requires.
* Any requirements for the user's Corda installation.
* If your CorDapp depends on other CorDapps.
* Any other dependences, such as on `apache-commons`.


### Define Corda, Quasar and Kotlin versions

A CorDapp's `build.gradle` file uses several `ext` variables to define version numbers. These match the version of Corda you’re developing against:

* `ext.corda_release_distribution` defines the Corda artifact group ID.
* `ext.corda_core_release_distribution` defines the artifact group ID for the open source core dependencies.
* `ext.corda_release_version` defines the Corda version.
* `ext.corda_core_release_version` defines the open source version for the core dependencies.
* `ext.corda_gradle_plugins_version` defines the version of the Corda Gradle Plugins.
* `ext.quasar_version` defines the version of Quasar, a library that we use to implement the flow framework.
* `ext.quasar_classifier` is used with `quasar_version` to set the version and classifier of the Quasar agent that the `quasar-utils` plugin will use. If `quasar_classifier` is not set as shown below, Gradle may not be able to resolve Quasar-related dependencies correctly.
* `ext.kotlin_version` defines the version of Kotlin (if using Kotlin to write your CorDapp).

Current versions:

```groovy
ext.corda_release_distribution = 'com.r3.corda'
ext.corda_core_release_distribution = 'net.corda'
ext.corda_release_version = '4.9'
ext.corda_core_release_version = '4.9'
ext.corda_gradle_plugins_version = '5.0.12'
ext.quasar_version = '0.7.14_r3'
ext.quasar_classifier=''
ext.kotlin_version = '1.2.71'
```
{{< note >}}
Corda Enterprise Edition 4 uses patched releases of Quasar and Caffeine to work around shortcomings identified in
these libraries while a fix is being developed. Add `corda-dependencies` to your list of Gradle repositories to get the patched versions of these libraries. This repository is required for any project referencing Corda Enterprise Edition 4 packages to provide transitive dependencies:

```groovy
repositories {
    // ... other dependencies
    maven { url "https://software.r3.com/artifactory/corda-dependencies" } // access to the patched Quasar and Caffeine version
}
```

{{< /note >}}

### Set Corda dependencies

There are a few guidelines to keep in mind when you set Corda dependencies.

* Always include `$corda_core_release_distribution:corda-core:$corda_core_release_version` as a
`cordaCompile` dependency, and `$corda_release_distribution:corda:$corda_release_version` as a `cordaRuntime` dependency
* When building an RPC client that communicates with a node (e.g. a webserver), you should include
`$corda_release_distribution:corda-rpc:$corda_release_version` as a `cordaCompile` dependency.
* When you need to use the network bootstrapper to bootstrap a local network (e.g. when using `Cordformation`), you
should include `$corda_release_distribution:corda-node-api:$corda_release_version` as either a `cordaRuntime` or a `runtimeOnly`
dependency. You may also wish to include an implementation of SLF4J as a `runtimeOnly` dependency for the network
bootstrapper to use.
* To use Corda’s test frameworks, add `$corda_release_distribution:corda-test-utils:$corda_release_version` as a `testCompile`
dependency. Never include `corda-test-utils` as a `compile` or `cordaCompile` dependency.
* Include any other Corda dependencies you need as `cordaCompile` dependencies.

#### Dependency list

* `corda` - The Corda fat `.jar`. Do not use as a compile dependency. Required as a `cordaRuntime` dependency when
using `Cordformation`.
* `corda-confidential-identities` - A part of the core Corda libraries. Automatically pulled in by other libraries.
* `corda-core` (*) - Usually automatically included by another dependency. Contains core Corda utilities, model, and
functionality. Include manually if the utilities are useful or you are writing a library for Corda.
* `corda-core-deterministic` (*) - Used by the Corda node for deterministic contracts. Not likely to be used externally.
* `corda-djvm` (*) - Used by the Corda node for deterministic contracts. Not likely to be used externally.
* `corda-finance-contracts` (*), `corda-finance-workflows` and deprecated `corda-finance`. Corda finance CorDapp, use contracts and flows parts respectively. Only include as a `cordaCompile` dependency if using as a dependent Cordapp or if you need access to the Corda finance types. Use as a `cordapp` dependency if using as a CorDapp dependency (see below).
* `corda-jackson` - Corda Jackson support. Use if you plan to serialise Corda objects to and/or from JSON.
* `corda-jfx` - JavaFX utilities with some Corda-specific models and utilities. Only use with JavaFX apps.
* `corda-mock` - A small library of useful mocks. Use if the classes fit your purpose.
* `corda-node` - The Corda node. Do not depend on this. Used only by the Corda fat `.jar` and indirectly in testing
frameworks. (If your CorDapp *must* depend on this for some reason then you can use the `compileOnly`
configuration here - however, this is not best practice).
* `corda-node-api` - The node API. Required to bootstrap a local network.
* `corda-node-driver` - Testing utility for programmatically starting nodes from JVM languages. Use for tests
* `corda-rpc` - The Corda RPC client library. Used when writing an RPC client.
* `corda-serialization` (*) - The Corda core serialization library. Automatically included by other dependencies
* `corda-serialization-deterministic` (*) - The Corda core serialization library. Automatically included by other
dependencies
* `corda-shell` - Used by the Corda node. Never depend on this directly.
* `corda-test-common` - A common test library. Automatically included by other test libraries.
* `corda-test-utils` - Used when writing tests against Corda/Cordapps.
* `corda-tools-explorer` - The Node Explorer tool. Do not depend on.
* `corda-tools-network-bootstrapper` - The Network Builder tool. Useful in build scripts.
* `corda-tools-shell-cli` - The Shell CLI tool. Useful in build scripts.

Any modules marked with (*) are part of the open core and must be pulled in from the matching Corda Community Edition distribution (using
`$corda_core_release_distribution` and `$corda_core_release_version`.

The `cordapp` plugin adds additional Gradle configurations:

* `cordaCompile`, which extends `compile`.
* `cordaRuntime`, which extends `runtime`.
* `cordapp`, which extends `compile`.

`cordaCompile` and `cordaRuntime` indicate dependencies that should not be included in the CorDapp `.jar`. Use these
configurations for any Corda dependency (for example, `corda-core`, `corda-node`) to prevent a
dependency from being included twice (once in the CorDapp `.jar` and once in the Corda `.jar`s). The `cordapp` dependency
is for declaring a compile-time dependency on a “semi-fat” CorDapp `.jar` in the same way as `cordaCompile`, except
that `Cordformation` will only deploy CorDapps contained within the `cordapp` configuration.

### Dependencies on other CorDapps

Your CorDapp may also depend on classes defined in another CorDapp, such as states, contracts and flows. There are two
ways to add another CorDapp as a dependency in your CorDapp’s `build.gradle` file:

* `cordapp project(":another-cordapp")`. Use this if the other CorDapp is defined in a module in the same project.
* `cordapp "net.corda:another-cordapp:1.0"` Use this for all other cases.

The `cordapp` Gradle configuration serves two purposes:

* Indicates that the `.jar` should be included on your node as a CorDapp when using the `cordformation` Gradle plugin.
* Prevents the dependency from being included in the CorDapp `.jar`.

{{< note >}}
The `cordformation` and `cordapp` Gradle plugins can be used at the same time.
{{< /note >}}

### Migrating to the latest version of Corda Gradle plugins

{{< note >}}
The latest version of Corda Gradle plugins is 5.1.x, which require Gradle 7.
{{< /note >}}

The `cordformation` plugin has been updated to enhance understanding of its use. It now creates the following Gradle configurations:

* `cordapp` - Used for any CorDapps you want to deploy, excluding any CorDapp built by the local project.
* `cordaDriver` - Used for any artifacts that must be added to each node's drivers/directory; for example, database drivers or the Corda shell.
* `corda` - The Corda artifact itself, or the Corda TestServer.
* `cordaBootstrapper` - Used for Corda's Bootstrapper artifact; i.e. a compatible version of `corda-node-api`. You may also wish to include an implementation of SLF4J for the Bootstrapper to use; for example, `slf4j-simple`.

The `corda` and `cordaBootstrapper` configurations replace the need for the `cordaRuntime` configuration when using `cordformation`. Using `cordaRuntime` was creating the false impression that CorDapps needed to declare runtime dependencies on either Corda, the Bootstrapper, or both.
There is no need to apply the `net.corda.plugins.cordapp` Gradle plugin along with `cordformation`, unless that project is also building a CorDapp.

### Other dependencies

You can specify any additional external dependencies using the same process you would for any Kotlin/Java dependencies in Gradle. See the example below, specifically the `apache-commons` include.

For further information about managing dependencies, see
[the Gradle docs](https://docs.gradle.org/current/userguide/dependency_management.html).


### Example

Below is a sample CorDapp Gradle dependencies block. When building your own CorDapp, use the `build.gradle` file of the
[Kotlin CorDapp Template](https://github.com/corda/cordapp-template-kotlin) or the
[Java CorDapp Template](https://github.com/corda/cordapp-template-java) as a starting point.

{{< tabs name="tabs-1" >}}
{{% tab name="groovy" %}}
```groovy
dependencies {
    // Corda integration dependencies
    cordaCompile "$corda_core_release_distribution:corda-core:$corda_core_release_version"
    cordaCompile "$corda_core_release_distribution:corda-finance-contracts:$corda_core_release_version"
    cordaCompile "$corda_release_distribution:corda-finance-workflows:$corda_release_version"
    cordaCompile "$corda_release_distribution:corda-jackson:$corda_release_version"
    cordaCompile "$corda_release_distribution:corda-rpc:$corda_release_version"
    cordaCompile "$corda_release_distribution:corda-node-api:$corda_release_version"
    cordaCompile "$corda_release_distribution:corda-webserver-impl:$corda_release_version"
    cordaRuntime "$corda_release_distribution:corda:$corda_release_version"
    cordaRuntime "$corda_release_distribution:corda-testserver:$corda_release_version"
    testCompile "$corda_release_distribution:corda-test-utils:$corda_release_version"

    // Corda Plugins: dependent flows and services
    // Identifying a CorDapp by its module in the same project.
    cordapp project(":cordapp-contracts-states")
    // Identifying a CorDapp by its fully-qualified name.
    cordapp "$corda_release_distribution:bank-of-corda-demo:1.0"

    // Some other dependencies
    compile "org.jetbrains.kotlin:kotlin-stdlib-jdk8:$kotlin_version"
    testCompile "org.jetbrains.kotlin:kotlin-test:$kotlin_version"
    testCompile "junit:junit:$junit_version"

    compile "org.apache.commons:commons-lang3:3.6"
}
```
{{% /tab %}}

{{< /tabs >}}



## Create the CorDapp `.jar`

After you have set your dependencies, build your CorDapp `.jar`(s) using the Gradle `jar` task:

* Unix/Mac OSX: `./gradlew jar`
* Windows: `gradlew.bat jar`

Each of the project’s modules is compiled into its own CorDapp `.jar`. You can find these CorDapp `.jar`s in the `build/libs` folders of each of the project’s modules.


{{< warning >}}
The hash of the generated CorDapp `.jar` is not deterministic, as it depends on variables such as the
timestamp at creation. Nodes running the same CorDapp must ensure they are using the exact same CorDapp
`.jar`, and not different versions of the `.jar` created from identical sources.

{{< /warning >}}


The filename of the `.jar` must include a unique identifier to deduplicate it from other releases of the same CorDapp.
This is typically done by appending the version string to the CorDapp’s name. This unique identifier should not change
once the `.jar` has been deployed on a node. If it does, make sure no one is relying on `FlowContext.appName` in their
flows (see [Versioning](versioning.md)).



## Sign the CorDapp

The `cordapp` plugin can sign the generated CorDapp `.jar` file using the [JAR signing and verification tool](https://docs.oracle.com/javase/tutorial/deployment/jar/signing.html).
Signing the CorDapp enables its contract classes to use signature constraints instead of other types of constraints.
See [Contract Constraints](api-contract-constraints.md) for more information.
The `.jar` file is signed by the Corda development certificate by default.

{{< warning >}}

Confidential identities are signed with development keys by default. You must self-sign the `.jar` file when you deploy it to production.

{{< /warning >}}

You can disable the signing process or configure it to use an external keystore.
The `signing` entry may contain the following parameters:

* `enabled`: The control flag to enable signing process. This is set to `true` by default. Set to `false` to disable signing.
* `options`: Any relevant parameters of [SignJar ANT task](https://ant.apache.org/manual/Tasks/signjar.html).
By default the `.jar` file is signed with Corda development key. You can specify the external keystore.
The minimum options are listed below. Find additional options in the [Apache manual](https://ant.apache.org/manual/Tasks/signjar.html).
    * `keystore`: The path to the keystore file. *cordadevcakeys.jks* keystore ships with the plugin by default.
    * `alias`: The alias to sign under. The default value is *cordaintermediateca*.
    * `storepass` The keystore password. The default value is *cordacadevpass*.
    * `keypass` The private key password if it is different than the password for the keystore. The default value is *cordacadevkeypass*.
    * `storetype` the keystore type, the default value is *JKS*.


You can also set parameters by passing system properties to Gradle during the build process.
Name the system properties using the relevant option name prefixed with ‘*signing.*’. For example,
a value for `alias` can be taken from the `signing.alias` system property.

You can use:
* `signing.enabled`
* `signing.keystore`
* `signing.alias`
* `signing.storepass`
* `signing.keypass`
* `signing.storetype`

The resolution order of a configuration value is:

1. The signing process takes a value specified in the `signing` entry. The empty string *“”* is also accepted.
2. If you have not set an option, the signing process tries the system property named *signing.option*.
3. If you have not set a  system property, the value defaults to the configuration of the Corda development certificate.

Here's an example of the `cordapp` plugin with the`signing` configuration:

```groovy
cordapp {
    signing {
        enabled true
        options {
            keystore "/path/to/jarSignKeystore.p12"
            alias "cordapp-signer"
            storepass "secret1!"
            keypass "secret1!"
            storetype "PKCS12"
        }
    }
    //...
```

### Auto-sign the CorDapp
CorDapp auto-signing lets you use signature constraints for contracts from that CorDapp without the need to create a
keystore or configuring the `cordapp` plugin. For a production deployment, make sure you sign the CorDapp with your own
certificate.

You could sign the CorDapp automatically by:
* Setting system properties to point to an external keystore, or
* Disabling signing in the `cordapp` plugin and signing the CorDapp `.jar` downstream in your build pipeline.

### Run development and production modes
Nodes only accept CorDapps signed by Corda development certificates when running in development mode. If you need to run a CorDapp signed by the (default) development key in the production mode (for example, for testing), add the `cordappSignerKeyFingerprintBlacklist = []` property set to an empty list. See [Configuring a node](../node/setup/corda-configuration-file.html#limitations)).


You can use one `build.gradle` file for both a development build (defaulting to the Corda development keystore) and for a production build (using an external keystore) by contexually overwriting signing options using system properties.

An example of the system properties setup for a build process that overrides signing options:

```shell
./gradlew -Dsigning.keystore="/path/to/keystore.jks" -Dsigning.alias="alias" -Dsigning.storepass="password" -Dsigning.keypass="password"
```

If you do not provide the system properties, the build signs the CorDapp with the default Corda development keystore:

```shell
./gradlew
```

You can disable CorDapp signing for a build:

```shell
./gradlew -Dsigning.enabled=false
```

To explicitly assign other system properties to options, call `System.getProperty` in the `cordapp` plugin
configuration. The configuration below sets the specific signing algorithm when a system property is
available. Otherwise, it defaults to an empty string:

```groovy
cordapp {
    signing {
        options {
            sigalg System.getProperty('custom.sigalg','')
        }
    }
    //...
```

The build process can then set the value for *custom.sigalg* system property and other system properties recognized by the
`cordapp` plugin:

```shell
./gradlew -Dcustom.sigalg="SHA256withECDSA" -Dsigning.keystore="/path/to/keystore.jks" -Dsigning.alias="alias" -Dsigning.storepass="password" -Dsigning.keypass="password"
```

To check if the CorDapp is signed, use the [JAR signing and verification tool](https://docs.oracle.com/javase/tutorial/deployment/jar/verify.html):

```shell
jarsigner --verify path/to/cordapp.jar
```

The Cordformation plugin can also sign CorDapp `.jar`s when [deploying a set of nodes](../node/deploy/generating-a-node.md).

If your build system post-processes the Cordapp `.jar`, then the modified `.jar` content may be out of date or missing a signature file. In this case, sign the Cordapp as a separate step and disable automatic signing by the `cordapp` plugin.

The `cordapp` plugin contains the standalone task `signJar`, which uses the same `signing` configuration. The task has two parameters:
* `inputJars` - to pass `.jar` files to be signed.
* An optional `postfix`, which is added to the name of signed `.jar`s (it defaults to “-signed”).

The signed `.jar`s are returned as the `outputJars` property.

For example, to sign a `.jar` modified by the *modifyCordapp* task:
1. Create an instance of the `net.corda.plugins.SignJar` task (named *sign* in the example below).
2. The output of the *modifyCordapp* task is passed to *inputJars*.
3. The *sign* task runs after *modifyCordapp*.
4. The task creates a new `.jar` file named *-signed.jar* for use later in your build/publishing process.

{{< note >}}
The best practice is to disable signing by the `cordapp` plugin, as shown in the example.
{{< /note >}}

```groovy
task sign(type: net.corda.plugins.SignJar) {
    inputJars modifyCordapp
}
modifyCordapp.finalizedBy sign
cordapp {
    signing {
        enabled false
    }
    //..
}
```



## CorDapp configuration files

Place the CorDapp configuration files in `<node_dir>/cordapps/config`. Match the filename to the
name of the CorDapp `.jar` (for example, if your CorDapp is called `hello-0.1.jar` the config should be `config/hello-0.1.conf`).

Config files are only available in the [Typesafe/Lightbend](https://github.com/lightbend/config) config format.
These files are loaded during node startup.

CorDapp configuration can be accessed from `CordappContext::config` whenever a `CordappContext` is available. For example:


### Using CorDapp configuration with the deployNodes task

If you want to configure a CorDapp when using the `deployNodes` Gradle task, then you can use the `cordapp` or `projectCordapp`
properties on the node. For example:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    nodeDefaults {
        // this external CorDapp will be included in each project
        cordapp("$corda_release_group:corda-finance-contracts:$corda_release_version")
        // this external CorDapp will be included in each project with the given config
        cordapp("$corda_release_group:corda-finance-workflows:$corda_release_version") {
            config "issuableCurrencies = [ USD ]"
        }
    }
    node {
        name "O=Bank A,L=London,C=GB"c
        ...
        // This adds configuration for another CorDapp project within the build
        cordapp (project(':my-project:workflow-cordapp')) {
            config "someStringValue=test"
        }
        cordapp(project(':my-project:another-cordapp')) {
            // Use a multiline string for complex configuration
            config '''
                someStringValue=test
                anotherStringValue=10
             '''
        }
    }
    node {
        name "O=Bank B,L=New York,C=US"
        ...
        // This adds configuration for the default CorDapp for this project
        projectCordapp {
            config project.file("src/config.conf")
        }
    }
}
```

You can find an example project that demonstrates this in the `samples` folder of the Corda Git repository, `cordapp-configuration` . You can also refer to the [API documentation](../../../../../../en/api-ref/api-ref-corda-4.html).


## Minimum and target platform version

CorDapps can advertise their minimum and target platform version. The minimum platform version indicates that a node has to run at least this
version in order to be able to run this CorDapp. The target platform version indicates that a CorDapp was tested with this version of the Corda
Platform and should be run at this API level if possible. It provides a means of maintaining behavioural compatibility for the cases where the
platform’s behaviour has changed. These attributes are specified in the `.jar` manifest of the CorDapp, for example:

```groovy
'Min-Platform-Version': 5
'Target-Platform-Version': 10
```

**Defaults**
* `Target-Platform-Version` (mandatory) is a whole number and must comply with the rules mentioned above.
* `Min-Platform-Version` (optional) will default to 1 if not specified.

Using the *cordapp* Gradle plugin, this can be achieved by putting this in your CorDapp’s *build.gradle*:

{{< tabs name="tabs-2" >}}
{{% tab name="groovy" %}}
```groovy
cordapp {
    targetPlatformVersion 10
    minimumPlatformVersion 5
}
```
{{% /tab %}}

{{< /tabs >}}



## Separate CorDapp contracts, flows, and services

Package **Contract** code (states, commands, verification logic) separately from **business flows** (and associated services).
This allows *contracts* to evolve independently from the *flows* and *services* that use them. Contracts may even be specified and implemented by different
providers. For example, Corda ships with a cash financial contract, which in turn is used in many other flows and many other CorDapps.

CorDapps can explicitly differentiate their type by specifying the following attributes in the `.jar` manifest:

```groovy
'Cordapp-Contract-Name'
'Cordapp-Contract-Version'
'Cordapp-Contract-Vendor'
'Cordapp-Contract-Licence'

'Cordapp-Workflow-Name'
'Cordapp-Workflow-Version'
'Cordapp-Workflow-Vendor'
'Cordapp-Workflow-Licence'
```

**Defaults**

`Cordapp-Contract-Name` (optional) you can specify contract-related attributes:

* `Cordapp-Contract-Version` (mandatory if `Cordapp-Contract-Name` is used). Must be a whole number starting from 1.
* `Cordapp-Contract-Vendor` (optional), defaults to UNKNOWN if not specified.
* `Cordapp-Contract-Licence` (optional), defaults to UNKNOWN if not specified.


`Cordapp-Workflow-Name` (optional) you can specify workflow-related attributes:

* `Cordapp-Workflow-Version` (mandatory if `Cordapp-Workflow-Name` is used). Must be a whole number starting from 1.
* `Cordapp-Workflow-Vendor` (optional), defaults to UNKNOWN if not specified.
* `Cordapp-Workflow-Licence` (optional), defaults to UNKNOWN if not specified.


You can specify your defaults using the Gradle *cordapp* plugin. For a contract-only CorDapp, specify the *contract* tag:

{{< tabs name="tabs-3" >}}
{{% tab name="groovy" %}}
```groovy
cordapp {
    targetPlatformVersion 10
    minimumPlatformVersion 5
    contract {
        name "my contract name"
        versionId 1
        vendor "my company"
        licence "my licence"
    }
}
```
{{% /tab %}}

{{< /tabs >}}

For a CorDapp that contains flows and/or services, specify the *workflow* tag:

{{< tabs name="tabs-4" >}}
{{% tab name="groovy" %}}
```groovy
cordapp {
    targetPlatformVersion 10
    minimumPlatformVersion 5
    workflow {
        name "my workflow name"
        versionId 1
        vendor "my company"
        licence "my licence"
    }
}
```
{{% /tab %}}

{{< /tabs >}}

{{< note >}}
It is possible, but *not recommended*, to include everything in a single CorDapp jar and use both the `contract` and `workflow` Gradle plugin tags.

{{< /note >}}

{{< warning >}}
Contract states may optionally specify a custom schema mapping (by implementing the `Queryable` interface) in its *contracts* `.jar`.
However, any associated database schema definition scripts (for example, Liquibase change set XML files) must currently be packaged in the *flows* `.jar`.
This is because the node requires access to these schema definitions on startup (*contract* `.jar`s are loaded in a separate attachments classloader).
This split enables scenarios where the same *contract* CorDapp may wish to target different database providers (and thus, the associated schema DDL may vary
to use native features of a particular database). The finance CorDapp provides an illustration of this packaging convention.
Future versions of Corda will de-couple this custom schema dependency to remove this anomaly.

{{< /warning >}}




## CorDapp Contract Attachments

CorDapp Contract `.jar`s must be installed on a node by a trusted uploader, either by:


* Installing manually as per [Installing the CorDapp JAR](#install-the-cordapp) and re-starting the node.
* Uploading the attachment `.jar` to the node via RPC, either programmatically (see [Connecting to a node via RPC](../node/operating/clientrpc.html#clientrpc-connect-ref))
or via the shell using the command: `>>> run uploadAttachment jar: path/to/the/file.jar`.

Contract attachments received over the p2p network are **untrusted** and throw a *UntrustedAttachmentsException* exception if they are processed by a listening flow that cannot resolve the attachment with its local attachment storage. The flow will be suspended and sent to the node's `node-flow-hospital` for recovery and retry.
The untrusted attachment `.jar` is stored in the node's local attachment store for review by a node operator. You can download it using a CRaSH shell command:

`>>> run openAttachment id: <hash of untrusted attachment given by `UntrustedAttachmentsException` exception`

If the node operator decides to trust the attachment, they can issue a CRaSH shell command to reload it and retry the failed flow. This requires a node restart.

`>>> run uploadAttachment jar: path/to/the/trusted-file.jar`



{{< note >}}
This behaviour protects the node from executing contract code that was not vetted. It is a temporary precaution until the
Deterministic JVM is integrated into Corda whereby execution takes place in a sandboxed environment which protects the node from malicious code.

{{< /note >}}

## Install the CorDapp

{{< note >}}
Before you install a CorDapp `.jar`, you must [create one or more nodes](../node/deploy/generating-a-node.md) to install it on.

{{< /note >}}
Nodes load any CorDapps present in their `cordapps` folder at startup. To install a CorDapp on a node, you must add the
CorDapp `.jar` to the `<node_dir>/cordapps/` folder (where `node_dir` is the folder in which the node’s `.jar`
and configuration files are stored) and restart the node.
