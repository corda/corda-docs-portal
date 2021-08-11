---
aliases:
- /releases/release-V4.1/generating-a-node.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-1:
    identifier: corda-os-4-1-generating-a-node
    parent: corda-os-4-1-corda-nodes-index
    weight: 1110
tags:
- generating
- node
title: Creating nodes locally
---


# Creating nodes locally



## Handcrafting a node

A node can be created manually by creating a folder that contains the following items:


* The Corda JAR>

    * Can be downloaded from [https://r3.bintray.com/corda/net/corda/corda/](https://r3.bintray.com/corda/net/corda/corda/) (under /4.1/corda-4.1.jar)



* A node configuration file entitled `node.conf`, configured as per [Node configuration](corda-configuration-file.md)
* A folder entitled `cordapps` containing any CorDapp JARs you want the node to load
* **Optional:** A webserver JAR entitled `corda-webserver.jar` that will connect to the node via RPC>

    * The (deprecated) default webserver can be downloaded from [http://r3.bintray.com/corda/net/corda/corda-webserver/](http://r3.bintray.com/corda/net/corda/corda-webserver/) (under /4.1/corda-4.1.jar)
    * A Spring Boot alternative can be found here: [https://github.com/corda/spring-webserver](https://github.com/corda/spring-webserver)




The remaining files and folders described in [Node folder structure](node-structure.md) will be generated at runtime.


## The Cordform task

Corda provides a gradle plugin called `Cordform` that allows you to automatically generate and configure a set of
nodes for testing and demos. Here is an example `Cordform` task called `deployNodes` that creates three nodes, defined
in the [Kotlin CorDapp Template](https://github.com/corda/cordapp-template-kotlin/blob/release-V4/build.gradle#L120):

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    directory "./build/nodes"

    nodeDefaults {
            cordapps = [
            "net.corda:corda-finance-contracts:$corda_release_version",
            "net.corda:corda-finance-workflows:$corda_release_version",
            "net.corda:corda-confidential-identities:$corda_release_version"
            ]
    }

    node {
        name "O=Notary,L=London,C=GB"
        // The notary will offer a validating notary service.
        notary = [validating : true]
        p2pPort  10002
        rpcSettings {
            port 10003
            adminPort 10023
        }
        // No webport property, so no webserver will be created.
        h2Port   10004
        // Starts an internal SSH server providing a management shell on the node.
        sshdPort 2223
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
        webPort  10007
        h2Port   10008
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
        webPort  10011
        h2Port   10012
        // Grants user1 the ability to start the MyFlow flow.
        rpcUsers = [[ user: "user1", "password": "test", "permissions": ["StartFlow.net.corda.flows.MyFlow"]]]
    }
}
```

Running this task will create three nodes in the `build/nodes` folder:


* A `Notary` node that:
    * Offers a validating notary service
    * Will not have a webserver (since `webPort` is not defined)
    * Is running the `corda-finance` CorDapp


* `PartyA` and `PartyB` nodes that:
    * Are not offering any services
    * Will have a webserver (since `webPort` is defined)
    * Are running the `corda-finance` CorDapp
    * Have an RPC user, `user1`, that can be used to log into the node via RPC



Additionally, all three nodes will include any CorDapps defined in the project’s source folders, even though these
CorDapps are not listed in each node’s `cordapps` entry. This means that running the `deployNodes` task from the
template CorDapp, for example, would automatically build and add the template CorDapp to each node.

You can extend `deployNodes` to generate additional nodes.


{{< warning >}}
When adding nodes, make sure that there are no port clashes!

{{< /warning >}}


To extend node configuration beyond the properties defined in the `deployNodes` task use the `configFile` property with the path (relative or absolute) set to an additional configuration file.
This file should follow the standard [Node configuration](corda-configuration-file.md) format, as per node.conf. The properties from this file will be appended to the generated node configuration. Note, if you add a property already created by the ‘deployNodes’ task, both properties will be present in the file.
The path to the file can also be added while running the Gradle task via the `-PconfigFile` command line option. However, the same file will be applied to all nodes.
Following the previous example `PartyB` node will have additional configuration options added from a file `none-b.conf`:

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

Cordform parameter *drivers* of the *node* entry lists paths of the files to be copied to the *./drivers* subdirectory of the node.
To copy the same file to all nodes *ext.drivers* can be defined in the top level and reused for each node via *drivers=ext.drivers`*.

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    ext.drivers = ['lib/my_common_jar.jar']
    [...]
    node {
        name "O=PartyB,L=New York,C=US"
        [...]
        drivers = ext.drivers + ['lib/my_specific_jar.jar']
    }
}
```


### Signing Cordapp JARs

The default behaviour of Cordform is to deploy CorDapp JARs “as built”:



* prior to Corda 4 all CorDapp JARs were unsigned.
* as of Corda 4, CorDapp JARs created by the Gradle *cordapp* plugin are signed by a Corda development certificate by default.


The Cordform `signing` entry can be used to override and customise the signing of CorDapp JARs.
Signing the CorDapp enables its contract classes to use signature constraints instead of other types of the constraints [API: Contract Constraints](api-contract-constraints.md).

The sign task may use an external keystore, or create a new one.
The `signing` entry may contain the following parameters:


* `enabled` the control flag to enable signing process, by default is set to `false`, set to `true` to enable signing
* `all` if set to `true` (by default) all CorDapps inside *cordapp* subdirectory will be signed, otherwise if `false` then only the generated Cordapp will be signed
* `options` any relevant parameters of [SignJar ANT task](https://ant.apache.org/manual/Tasks/signjar.html) and [GenKey ANT task](https://ant.apache.org/manual/Tasks/genkey.html),
by default the JAR file is signed by Corda development key, the external keystore can be specified,
the minimal list of required options is shown below, for other options referer to [SignJar task](https://ant.apache.org/manual/Tasks/signjar.html):
    * `keystore` the path to the keystore file, by default *cordadevcakeys.jks* keystore is shipped with the plugin
    * `alias` the alias to sign under, the default value is *cordaintermediateca*
    * `storepass` the keystore password, the default value is *cordacadevpass*
    * `keypass` the private key password if it’s different than the password for the keystore, the default value is *cordacadevkeypass*
    * `storetype` the keystore type, the default value is *JKS*
    * `dname` the distinguished name for entity, the option is used when `generateKeystore true` only
    * `keyalg` the method to use when generating name-value pair, the value defaults to *RSA* as Corda doesn’t support *DSA*, the option is used when `generateKeystore true` only


* `generateKeystore` the flag to generate a keystore, it is set to `false` by default. If set to `true` then ad hock keystore is created and its key isused
instead of the default Corda development key or any external key.
The same `options` to specify an external keystore are used to define the newly created keystore. Additionally
`dname` and `keyalg` are required. Other options are described in [GenKey task](https://ant.apache.org/manual/Tasks/genkey.html).
If the existing keystore is already present the task will reuse it, however if the file is inside the *build* directory,
then it will be deleted when Gradle *clean* task is run.

The example below shows the minimal set of `options` needed to create a dummy keystore:

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

Contracts classes from signed CorDapp JARs will be checked by signature constraints by default.
You can force them to be checked by zone constraints by adding contract class names to `includeWhitelist` entry,
the list will generate *include_whitelist.txt* file used internally by [Network Bootstrapper](network-bootstrapper.md) tool.
Refer to [API: Contract Constraints](api-contract-constraints.md) to understand implication of different constraint types before adding `includeWhitelist` to `deployNodes` task.
The snippet below configures contracts classes from Finance CorDapp to be verified using zone constraints instead of signature constraints:

```groovy
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {
    includeWhitelist = [ "net.corda.finance.contracts.asset.Cash", "net.corda.finance.contracts.asset.CommercialPaper" ]
    //...
```


### Specifying a custom webserver

By default, any node listing a web port will use the default development webserver, which is not production-ready. You
can use your own webserver JAR instead by using the `webserverJar` argument in a `Cordform` `node` configuration
block:

```groovy
node {
    name "O=PartyA,L=New York,C=US"
    webPort 10005
    webserverJar "lib/my_webserver.jar"
}
```

The webserver JAR will be copied into the node’s `build` folder with the name `corda-webserver.jar`.


{{< warning >}}
This is an experimental feature. There is currently no support for reading the webserver’s port from the
node’s `node.conf` file.

{{< /warning >}}



## The Dockerform task

The `Dockerform` is a sister task of `Cordform` that provides an extra file allowing you to easily spin up
nodes using `docker-compose`. It supports the following configuration options for each node:


* `name`
* `notary`
* `cordapps`
* `rpcUsers`
* `useTestClock`

There is no need to specify the nodes’ ports, as every node has a separate container, so no ports conflict will occur.
Every node will expose port `10003` for RPC connections.

The nodes’ webservers will not be started. Instead, you should interact with each node via its shell over SSH
(see the [node configuration options](corda-configuration-file.md)). You have to enable the shell by adding the
following line to each node’s `node.conf` file:


`sshd { port = 2222 }`


Where `2222` is the port you want to open to SSH into the shell.

Below you can find the example task from the [IRS Demo](https://github.com/corda/corda/blob/release/os/4.1/samples/irs-demo/cordapp/build.gradle#L111) included in the samples directory of main Corda GitHub repository:

```groovy
def rpcUsersList = [
    ['username' : "user",
     'password' : "password",
     'permissions' : [
             "StartFlow.net.corda.irs.flows.AutoOfferFlow\$Requester",
             "StartFlow.net.corda.irs.flows.UpdateBusinessDayFlow\$Broadcast",
             "StartFlow.net.corda.irs.api.NodeInterestRates\$UploadFixesFlow",
             "InvokeRpc.vaultQueryBy",
             "InvokeRpc.networkMapSnapshot",
             "InvokeRpc.currentNodeTime",
             "InvokeRpc.wellKnownPartyFromX500Name"
     ]]
]

// (...)

task deployNodes(type: net.corda.plugins.Dockerform, dependsOn: ['jar']) {

    nodeDefaults {
            cordapps = [
            "net.corda:corda-finance-contracts:$corda_release_version",
            "net.corda:corda-finance-workflows:$corda_release_version",
            "net.corda:corda-confidential-identities:$corda_release_version"
            ]
    }

    node {
        name "O=Notary Service,L=Zurich,C=CH"
        notary = [validating : true]
        rpcUsers = rpcUsersList
        useTestClock true
    }
    node {
        name "O=Bank A,L=London,C=GB"
        rpcUsers = rpcUsersList
        useTestClock true
    }
    node {
        name "O=Bank B,L=New York,C=US"
        rpcUsers = rpcUsersList
        useTestClock true
    }
    node {
        name "O=Regulator,L=Moscow,C=RU"
        rpcUsers = rpcUsersList
        useTestClock true
    }
}
```


## Running the Cordform/Dockerform tasks

To create the nodes defined in our `deployNodes` task, run the following command in a terminal window from the root
of the project where the `deployNodes` task is defined:


* Linux/macOS: `./gradlew deployNodes`
* Windows: `gradlew.bat deployNodes`

This will create the nodes in the `build/nodes` folder. There will be a node folder generated for each node defined
in the `deployNodes` task, plus a `runnodes` shell script (or batch file on Windows) to run all the nodes at once
for testing and development purposes. If you make any changes to your CorDapp source or `deployNodes` task, you will
need to re-run the task to see the changes take effect.

If the task is a `Dockerform` task, running the task will also create an additional `Dockerfile` in each node
directory, and a `docker-compose.yml` file in the `build/nodes` directory.

You can now run the nodes by following the instructions in [Running a node](running-a-node.md).

