---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-corda-nodes-deploying-node-generating-cordform
    parent: corda-enterprise-4-8-corda-nodes-deploying-generate
tags:
- generating
- node
title: Cordform task
weight: 2
---

# Tasks using Cordform

This example task creates the following three nodes in the `build/nodes` directory:

A `Notary` node, which:
* Provides a validating Notary service.
* Runs the `corda-finance` CorDapp.

`PartyA` and `PartyB` nodes, each of which:
* Does not provide any services.
* Runs the `corda-finance` CorDapp.
* Has an RPC (Remote Procedure Call) user (`user1`), which enables you to log in the node via RPC.

All three nodes also include any CorDapps defined in the project's source directories, even if these CorDapps are not listed in each node's `cordapps` setting. As a result, if you run the `deployNodes` task from the template CorDapp, for example, it will automatically build and add the template CorDapp to each node.

{{< note >}}
The three nodes described here are just an example. `Cordform` allows you to specify any number of nodes. You can define their configurations and names as needed.
{{< /note >}}

The following example, as defined in the [Kotlin CorDapp Template](https://github.com/corda/cordapp-template-kotlin/blob/release-V4/build.gradle#L120), shows a `Cordform` task called `deployNodes` that creates the three nodes described above: `Notary`, `PartyA`, and `PartyB`.

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    directory "./build/nodes"
    node {
        name "O=Notary,L=London,C=GB"
        // The Notary will offer a validating Notary service.
        notary = [validating : true]
        p2pPort  10002
        rpcSettings {
            port 10003
            adminPort 10023
        }
        h2Port   10004
        // Starts an internal SSH server providing a management shell on the node.
        sshdPort 2223
        // Includes the corda-finance CorDapp on our node.
        cordapps = ["$corda_release_distribution:corda-finance:$corda_release_version"]
        extraConfig = [
            // Setting the JMX reporter type.
            jmxReporterType: 'JOLOKIA',
            // Setting the H2 address.
            h2Settings: [ address: 'localhost:10030' ]
        ]
    }
    node {
        name "O=PartyA,L=London,C=GB"
        p2pPort  10005
        rpcSettings {
            port 10006
            adminPort 10026
        }
        h2Port   10008
        cordapps = ["$corda_release_distribution:corda-finance:$corda_release_version"]
        // Grants user1 all RPC permissions.
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["ALL"]]]
    }
    node {
        name "O=PartyB,L=New York,C=US"
        p2pPort  10009
        rpcSettings {
            port 10010
            adminPort 10030
        }
        h2Port   10012
        cordapps = ["$corda_release_distribution:corda-finance:$corda_release_version"]
        // Grants user1 the ability to start the MyFlow flow.
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["StartFlow.net.corda.flows.MyFlow"]]]
    }
}
```

{{< note >}}
Make sure to use Corda Gradle plugin version 5.0.10 or above.
{{< /note >}}

The configuration values used in the example are described below.

You can turn off deploying the local project's CorDapp to each node by adding the following code to your node configuration:

```
projectCordapp {
    deploy = false
}
```

The `Cordform` and `Dockerform` also support a `nodeDefaults` block, which can
contain configuration common to all nodes, for example:

```
nodeDefaults {
    cordapp project(':contracts')
    cordapp project(':workflows')
    runSchemaMigration = true
    rpcUsers = [[user: "user1", "password": "test", "permissions": ["ALL"]]
}
```

You can override these defaults for each node:

```
node {
    name = "O=Notary,L=London,C=GB"
    notary = [ validating: true ]
    rpcUsers = []
}
```

## Required configuration

* `name` &lt;string&gt; - use this configuration option to specify the legal identity name of the Corda node. For more information, see [myLegalName](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#mylegalname). For example:

```kotlin
name "O=PartyA,L=London,C=GB"
```
* `p2pAddress` &lt;string&gt; - use this configuration option to specify the address/port the node uses for inbound communication from other nodes. For more information, see [p2pAddress](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#p2paddress). **Required if `p2pPort` is not specified**. For example:

```kotlin
p2pAddress "example.com:10002"
```
* `p2pPort` &lt;integer&gt; - use this configuration option to specify the port the node uses for inbound communication from other nodes. The assumed IP address is `localhost`. For more information, see [p2pAddress](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#p2paddress). For example:

```kotlin
p2pPort 10006  // "localhost:10006"
```

* `rpcSettings` &lt;config&gt; - use this configuration option to specify RPC settings for the node. For more information, see [rpcSettings](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#rpcsettings). For example:

```kotlin
rpcSettings {
  port 10006
  adminPort 10026
}
```

## Optional configuration

* `notary` &lt;config&gt; - use this configuration option to specify the node as a Notary node. **Required**> for Notary nodes. For more information, see [notary](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#notary).

* `devMode` &lt;boolean&gt; - use this configuration option to enable development mode when you set its value to `true`. For more information, see [devMode](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#devmode). For example:

```kotlin
devMode true
```

* `rpcUsers` &lt;list&gt; - use this configuration option to set the RPC users for the node. For more information, see [rpcUsers](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#rpcusers). You can use arbitrary values in this configuration block - "incorrect" settings will not cause a DSL error. An example follows below:

```kotlin
rpcUsers = [[ user: "user1", "password": "test", "permissions": ["StartFlow.net.corda.flows.MyFlow"]]]
```

* `configFile` &lt;string&gt; - use this configuration option to generate an extended node configuration. For more information, see [extended node configuration](../setup/corda-configuration-file.md). For example:

```kotlin
configFile = "samples/trader-demo/src/main/resources/node-b.conf"
```

* `sshdPort` &lt;integer&gt; - use this configuration option to specify the SSH port for the Docker container. This will be mapped to the same port on the host.  If `sshdPort` is specified, then that port must be available on the host and not in use by some other service. If `sshdPort` is not specified, then a default value will be used for the SSH port on the container. Use the `docker port <container_name>` command to check which port has been allocated on the host for your container. For more information, see [sshd](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-fields.html#sshd). For example:

```kotlin
sshd {
  port = 2222
}
```

You can extend the `deployNodes` task with more `node {}` blocks to generate as many nodes as necessary for your application.

{{< warning >}}
When adding nodes, make sure that there are no port clashes!
{{< /warning >}}

To extend node configuration beyond the properties defined in the `deployNodes` task, use the `configFile` property with the file path (relative or absolute) set to an additional configuration file. This file should follow the standard [Node configuration](../../../../../../../en/platform/corda/4.8/enterprise/node/setup/corda-configuration-file.md) format of `node.conf`. The properties set there will be appended to the generated node configuration.

{{< note >}}
If you add a property to the additional configuration file that has already been created by the `deployNodes` task, both properties will be present in generated node configuration.
{{< /note >}}

Alternatively, you can also add the path to the additional configuration file while running the gradle task via the `-PconfigFile` command-line option. However, this will result in the same configuration file being applied to all nodes.

Following on from the previous example, the `PartyB` node in the next example below has additional configuration options added from a file called `none-b.conf`:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    [...]
    node {
        name "O=PartyB,L=New York,C=US"
        [...]
        // Grants user1 the ability to start the MyFlow flow.
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["StartFlow.net.corda.flows.MyFlow"]]]
        configFile = "samples/trader-demo/src/main/resources/node-b.conf"
    }
}
```

The `drivers` parameter in the `node` entry lists paths of the files to be copied to the `drivers` sub-directory of the node.

To add any drivers as dependencies of the `cordaDriver` configuration, use the following code (option recommended over using the `drivers` parameter):

```
dependencies {
    cordaDriver "net.corda:corda-shell:$corda_release_version"
    cordaDriver files('lib/my_specific_jar.jar')
}
```

The `Cordform` and `Dockerform` tasks copy the resolved contents of Gradle's
`cordaDriver` configuration into each node's `drivers` directory before
running the bootstrapper.

## Package namespace ownership

To configure [package namespace ownership](../../../../../../../en/platform/corda/4.8/enterprise/node/deploy/env-dev.html#package-namespace-ownership), use the optional `networkParameterOverrides` and `packageOwnership` blocks, in a similar way to how the configuration file is used by the [Network Bootstrapper](../../../../../../../en/platform/corda/4.8/enterprise/network-bootstrapper.md) tool. For example:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    [...]
    networkParameterOverrides {
        packageOwnership {
            "com.mypackagename" {
                keystore = "_teststore"
                keystorePassword = "MyStorePassword"
                keystoreAlias = "MyKeyAlias"
            }
        }
    }
    [...]
}
```

## Sign CorDapp `.jar` files

The default Cordform behaviour is to deploy CorDapp `.jar` files “as built”.

* Prior to Corda 4.0, all CorDapp `.jar` files were unsigned.
* As of Corda 4.0, CorDapp `.jar` files created by the gradle `cordapp` plug-in are signed by a Corda development certificate by default.

You can use the Cordform `signing` entry to override and customise the signing of CorDapp `.jar` files.
Signing a CorDapp enables its contract classes to use signature constraints instead of other types of constraints, such as [Contract Constraints](../../../../../../../en/platform/corda/4.8/enterprise/cordapps/api-contract-constraints.md).

The signing task may use an external keystore, or create a new one.
You can use the following parameters in the `signing` entry:


* `enabled` - the control flag to enable the signing process. It is set to `false` by default. Set to `true` to enable signing.
* `all` - if set to `true` (default), all CorDapps inside the `cordapp` sub-directory will be signed. If set to `false`, only the generated CorDapp will be signed.
* `options` - any relevant parameters of [SignJar ANT task](https://ant.apache.org/manual/Tasks/signjar.html) and [GenKey ANT task](https://ant.apache.org/manual/Tasks/genkey.html). By default the `.jar` file is signed by a Corda development key. You can specify the external keystore can be specified. The minimal list of required options is shown below. For other options, see [SignJar task](https://ant.apache.org/manual/Tasks/signjar.html).
  * `keystore` - the path to the keystore file. The default setting is `cordadevcakeys.jks`. The keystore is shipped with the plug-in.
  * `alias` - the alias to sign under. The default value is `cordaintermediateca`.
  * `storepass` - the keystore password. The default value is `cordacadevpass`.
  * `keypass` - the private key password, if it is different from the keystore password. The default value is `cordacadevkeypass`.
  * `storetype` - the keystore type. The default value is `JKS`.
  * `dname` - the distinguished name for the entity. Only use this option when `generateKeystore` is set to `true` (see below).
  * `keyalg` - the method to use when generating a name-value pair. The default value is `RSA` because Corda does not support `DSA`. Only use this option when `generateKeystore` is set to `true` (see below).
* `generateKeystore` - the flag to generate a keystore. The default value is `false`. If set to `true`, an "ad hoc" keystore is created and its key is used instead of the default Corda development key or any external key. The same `options` to specify an external keystore are used to define the newly created keystore. In addition,
  `dname` and `keyalg` are required. Other options are described in [GenKey task](https://ant.apache.org/manual/Tasks/genkey.html). If the existing keystore is already present, the task will reuse it. However if the file is inside the `build` directory,
  then it will be deleted when the gradle `clean` task is run.

The example below shows the minimal set of `options` required to create a dummy keystore:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
     signing {
        enabled true
        generateKeystore true
        all false
        options {
            keystore "./build/nodes/jarSignKeystore.p12"
            alias "cordapp-signer"
            storepass "secret1!"
            storetype "PKCS12"
            dname "OU=Dummy Cordapp Distributor, O=Corda, L=London, C=GB"
            keyalg "RSA"
        }
    }
    //...
```

Contracts classes from signed CorDapp `.jar` files are checked by signature constraints by default.
You can force them to be checked by zone constraints by adding contract class names to the `includeWhitelist` entry - the list will generate an `include_whitelist.txt` file used internally by the [Network Bootstrapper](../../../../../../../en/platform/corda/4.8/enterprise/network-bootstrapper.md) tool.
Before you add `includeWhitelist` to the `deployNodes` task, see [Contract Constraints](../../../../../../../en/platform/corda/4.8/enterprise/cordapps/api-contract-constraints.md) to understand the implications of using different constraint types.
The snippet below configures contracts classes from the Finance CorDapp to be verified using zone constraints instead of signature constraints:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    includeWhitelist = [ "net.corda.finance.contracts.asset.Cash", "net.corda.finance.contracts.asset.CommercialPaper" ]
    //...
```
## Optional migration step

If you are migrating your database schema from an older Corda version to Corda 4.8, you must add the following parameter to the node section in the `build.gradle` and set it to `true`, as follows:

```
        runSchemaMigration = true
```

This step runs the full schema migration process as the last step of the Cordform task, and leave the nodes ready to run.

## Run the Cordform task

To create the nodes defined in the `deployNodes` task example above, run the following command in a command prompt or a terminal window, from the root of the project where the `deployNodes` task is defined:

* Linux/macOS: `./gradlew deployNodes`
* Windows: `gradlew.bat deployNodes`

This command creates the nodes in the `build/nodes` directory. A node directory is generated for each node defined in the `deployNodes` task, plus a `runnodes` shell script (or a batch file on Windows) to run all the nodes at once for testing and development purposes. If you make any changes to your CorDapp source or `deployNodes` task, you will need to re-run the task to see the changes take effect.
