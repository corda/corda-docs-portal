---
date: '2021-08-25'
corda-enterprise-4-10:
parent: corda-enterprise-4-10-cordapps-debugging
tags:
- network
- bootstrapper
title: Network Bootstrapper
weight: 40
---


# Network Bootstrapper
Corda's Network Bootstrapper tool lets you quickly create a group of nodes that can see and communicate with each other. You can use these simple networks for development and testing.

Each node on the network must:
* Operate using the same set of constants, called **network parameters**. This guarantees that the nodes can interoperate.
* Have a copy of the `node-info` file for every other node on the network. This is what makes them visible to each other.

The Network Bootstrapper automates the processes of creating and distributing the network parameters and `node-info` files.


## Glossary

| Term                          | Definition                                                                                               |
|-------------------------------|----------------------------------------------------------------------------------------------------------|
| network parameters            | A set of constants shared between a group of nodes to guarantee interoperability.                        |
| `node-info` file              | A file containing information about the node.                                                            |
| compatibility zone constraint | The compatibility zone operator lists the hashes of CorDapp versions that a contract class name can use. |
| signature constraint           | A contract class can use any version of a CorDapp that is signed by a given `CompositeKey`.              |
| hash constraint               | Only one version of a CorDapp can be used with a specific state.                                         |


## Test deployments

Nodes within a network see each other using the [network map](network/network-map.md). This is a collection of statically-signed `node-info` files, one for each node. Most production deployments use a highly-available, secure distribution of the network map via HTTP.

If you are creating a test deployment that stores the nodes on the same filesystem, place the `node-info` files into the node’s `additional-node-infos` directory. The node picks them up and stores them in its local network map cache, then generates its own `node-info` file on startup.

All the nodes must use the same set of network parameters. These are a set of constants
that guarantee interoperability between the nodes. Typically, the HTTP network map distributes the network parameters to the nodes, which download them automatically. You can also generate network parameters locally.

You can use the Network Bootstrapper to scan all the node configurations in a common directory to generate the network parameters file. The bootstrapper then copies the network parameters file to all the nodes' directories. It also copies each node's `node-info` file to all the other nodes, which makes them visible to each other.


## Bootstrap a test network

To bootstrap a test network:

1. Download the [Corda Network Boostrapper](https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-network-bootstrapper) for the version of Corda you want the nodes to run.
2. Create a directory containing a node config file (ending in “_node.conf”) for each node you want to create.
3. Set “devMode” to `true`.
4. Run the command `java -jar network-bootstrapper-4.9.jar --dir <nodes-root-dir>`.

If you were to run this command on a directory containing these files:

```none
.
├── notary_node.conf             // The notary's node.conf file
├── partya_node.conf             // Party A's node.conf file
└── partyb_node.conf             // Party B's node.conf file
```

Then the bootstrapper will generate directories containing three nodes: `notary`, `partya`, and `partyb`. Each node will use the `corda.jar`
provided by the Network Bootstrapper you chose. If you need to change the version, put the relevant `corda.jar` file with the configuration files in the directory.

Alternatively, you can structure the node directories like this:

```none
.
├── notary
│   └── node.conf
├── partya
│   └── node.conf
└── partyb
    └── node.conf
```

It's possible for each node directory to contain its own `corda.jar`. In this case, the bootstrapper uses the `corda.jar` file in the node directory.


## Include CorDapps in a generated node

If you would like the bootstrapper to include your CorDapps in each generated node, place them in the directory
alongside the configuration files. For example, for a directory with this structure:

```none
.
├── notary_node.conf            // The notary's node.conf file
├── partya_node.conf            // Party A's node.conf file
├── partyb_node.conf            // Party B's node.conf file
├── cordapp-a.jar               // A cordapp to be installed on all nodes
└── cordapp-b.jar               // Another cordapp to be installed on all nodes
```

The `cordapp-a.jar` and `cordapp-b.jar` will be installed in each node directory, and any contracts within them will be
added to the [contract whitelist](###whitelist-contracts).



### Create a contracts whitelist
If you provide a CorDapp, the boostrapper will hash it, then scan it for instances of the `contacts` class. If it finds contracts, it will use them to create a [compatibility zone whitelist](https://docs.corda.net/docs/4.10/enterprise/cordapps/api-contract-constraints.html) for the network.

{{< note >}}
If you want to whitelist the CorDapps without copying them to each node, run them using the `--copy-cordapps=No` option.

{{< /note >}}

The bootstrapper hashes the CorDapp `.jar`s and scans them for `contract` classes. These contract class implementations become part
of the whitelisted contracts in the network parameters. For each contract class, there is a list of SHA-256 hashes of the approved CorDapp `.jar` versions containing that contract.

By default, the bootstrapper whitelists all the contracts it finds in the unsigned CorDapp `.jar`s (`.jar` files not signed by `jarSigner` tool).
It checks whitelisted contracts using compatibility zone constraints, and contract classes from signed `.jar`s using signature constraints.

If you want to prevent specific contracts from unsigned `.jar`s from being whitelisted, add their fully-qualified class name in the `exclude_whitelist.txt` file. Contracts in this file will use the more restrictive `HashAttachmentConstraint`, which only allows one version of a CorDapp to be used with a specific state.

To add specific contracts from signed `.jar`s to the whitelist, add their fully-qualified class name to the `include_whitelist.txt` file.

For example:

```none
net.corda.finance.contracts.asset.Cash
net.corda.finance.contracts.asset.CommercialPaper
```

Before you add `exclude_whitelist.txt` or `include_whitelist.txt` files, refer to [contract constraints](https://docs.corda.net/docs/4.10/enterprise/cordapps/api-contract-constraints.html) to understand different constraint types.




## Modify a bootstrapped network

The Network Bootstrapper is a tool for setting up Corda networks for development and testing. Functionality for making changes is limited. You can:
* Add a new node to the network.
* Update the contract whitelist for bootstrapped networks.

If you need to make more complicated changes, use a [Network Map server](network/network-map.md).

Make sure all `node-info` files are in one directory when running the Network Bootstrapper. If you are running
the nodes on different machines:

1. Copy the node directories from each machine into one directory, on one machine.
2. Add any new files required to the root directory.
3. Run the Network Bootstrapper from the root directory.
4. Copy each individual node’s directory back to the original machines.

The Network Bootstrapper cannot dynamically update the network if an existing node has changed something in their `node-info`,
such as their P2P address. You will need to place the updated `node-info` in the other nodes’ `additional-node-infos` directory.
If the nodes are located on different machines, you can use a utility such as [rsync](https://en.wikipedia.org/wiki/Rsync)
so the nodes can share `node-info`.


### Adding a new node to the network

You can add a new node and distribute its `node-info` to the existing nodes on the network by running the Network Bootstrapper twice.

In this example, you have an existing bootstrapped network. It consists of a notary and Party A, and you'd like to add Party B.

First, run the Network Bootstrapper as usual. Your network structure will look like this:

```none
.
├── notary                      // existing node directories
│   ├── node.conf
│   ├── network-parameters
│   ├── node-info-notary
│   └── additional-node-infos
│       ├── node-info-notary
│       └── node-info-partya
├── partya
│   ├── node.conf
│   ├── network-parameters
│   ├── node-info-partya
│   └── additional-node-infos
│       ├── node-info-notary
│       └── node-info-partya
└── partyb_node.conf            // the node.conf for the node to be added
```

Then, run the Network Bootstrapper again from the root directory:

`java -jar network-bootstrapper-4.9.jar --dir <nodes-root-dir>`

You will produce this result:

```none
.
├── notary                      // the contents of the existing nodes (keys, db's etc...) are unchanged
│   ├── node.conf
│   ├── network-parameters
│   ├── node-info-notary
│   └── additional-node-infos
│       ├── node-info-notary
│       ├── node-info-partya
│       └── node-info-partyb
├── partya
│   ├── node.conf
│   ├── network-parameters
│   ├── node-info-partya
│   └── additional-node-infos
│       ├── node-info-notary
│       ├── node-info-partya
│       └── node-info-partyb
└── partyb                      // a new node directory is created for PartyB
    ├── node.conf
    ├── network-parameters
    ├── node-info-partyb
    └── additional-node-infos
        ├── node-info-notary
        ├── node-info-partya
        └── node-info-partyb
```

The bootstrapper generates a directory and the `node-info` file for Party B. It also places a copy of each
nodes’ `node-info` file in the `additional-node-info` directory of every node. Any other files in the existing nodes,
such a generated keys, will be unaffected.

{{< note >}}
The Network Bootstrapper is intended for test deployments, and can only generate information for nodes collected on
the same machine. If you need to update a network using the bootstrapper after you deploy it, you will need to collect the nodes on one machine again.

{{< /note >}}


### Updating the contract whitelist for bootstrapped networks

If the network already has a set of network parameters defined (the node directories all contain the same `network-parameters`
file) then you can use the Network Bootstrapper to append contracts from new CorDapps to the current whitelist.

For example, you could take this pre-generated network:

```none
.
├── notary
│   ├── node.conf
│   ├── network-parameters
│   └── cordapps
│       └── cordapp-a.jar
├── partya
│   ├── node.conf
│   ├── network-parameters
│   └── cordapps
│       └── cordapp-a.jar
├── partyb
│   ├── node.conf
│   ├── network-parameters
│   └── cordapps
│       └── cordapp-a.jar
└── cordapp-b.jar               // The new cordapp to add to the existing nodes
```

Then run the Network Bootstrapper again from the root directory:

`java -jar network-bootstrapper-4.9.jar --dir <nodes-root-dir>`

To produce:

```none
.
├── notary
│   ├── node.conf
│   ├── network-parameters      // The contracts from cordapp-b are appended to the whitelist in network-parameters
│   └── cordapps
│       ├── cordapp-a.jar
│       └── cordapp-b.jar       // The updated CorDapp is placed in the node's CorDapp directory
├── partya
│   ├── node.conf
│   ├── network-parameters      // The contracts from cordapp-b are appended to the whitelist in network-parameters
│   └── cordapps
│       ├── cordapp-a.jar
│       └── cordapp-b.jar       // The updated CorDapp is placed in the node's cordapp directory
└── partyb
    ├── node.conf
    ├── network-parameters      // The contracts from cordapp-b are appended to the whitelist in network-parameters
    └── cordapps
        ├── cordapp-a.jar
        └── cordapp-b.jar       // The updated CorDapp is placed in the node's cordapp directory
```

{{< note >}}
You can only add to the whitelist. Once added, you can't remove a contract implementation.

{{< /note >}}

## Modify the network parameters

The Network Bootstrapper creates a default `network-parameters` file. However, if you require specific parameters for testing, you can modify the default:
* Using a command line argument.
* By supplying a configuration file.

If the same parameter is overridden both by a command line argument and in the configuration file, the command line value
will take precedence.


### Override network parameters via command line

You can use the `--minimum-platform-version`, `--max-message-size`, `--max-transaction-size`, and `--event-horizon` command line parameters to override the default network parameters. See [Command line options](#command-line-options) for more information.


### Overriding network parameters via a file

You can provide a file to override the network parameters using:

`java -jar network-bootstrapper-4.9.jar --network-parameter-overrides=<path_to_file>`

Or the short form version:

`java -jar network-bootstrapper-4.9.jar -n=<path_to_file>`

The network parameter overrides file is a HOCON file with several configuration fields, all of which are optional. If you don't provide a field, it will be ignored. If a field is not provided and you are bootstrapping a new network, a sensible default value will be used. If a field is not provided
when you are updating an existing network, the value in the existing network parameters file will be used.

{{< note >}}
All fields can contain placeholders for environment variables. For example: `${KEY_STORE_PASSWORD}` would be replaced by the contents of environment
variable `KEY_STORE_PASSWORD`. See: [Hiding sensitive data](node/operating/node-administration.md#hiding-sensitive-data).

{{< /note >}}
The available configuration fields are:


* **minimumPlatformVersion**:
  The minimum supported version of the Corda platform that is required for nodes in the network.


* **maxMessageSize**:
  The maximum permitted message size, in bytes.


* **maxTransactionSize**:
  The maximum permitted transaction size, in bytes.


* **eventHorizon**:
  The time after which nodes will be removed from the network map if they have not been seen during this period. This parameter uses
  the `parse` function on the `java.time.Duration` class to interpret the data. See [Oracle's documentation](https://docs.oracle.com/javase/8/docs/api/java/time/Duration.html#parse-java.lang.CharSequence-)
  for information on valid inputs.


* **packageOwnership**:
  A list of package owners. See [Package namespace ownership](#id1). For each package owner, these fields
  are required:


* **packageName**:
  Java package name (for example, *com.my_company*).


* **keystore**:
  The path of the keystore file containing the signed certificate.


* **keystorePassword**:
  The password for the given keystore (not to be confused with the key password).


* **keystoreAlias**:
  The alias for the name associated with the certificate to be associated with the package namespace.





An example configuration file:

```kotlin
minimumPlatformVersion=4
maxMessageSize=10485760
maxTransactionSize=524288000
eventHorizon="30 days"
packageOwnership=[
    {
        packageName="com.example"
        keystore="myteststore"
        keystorePassword="MyStorePassword"
        keystoreAlias="MyKeyAlias"
    }
]
```



## Package namespace ownership

Package namespace ownership is a Corda security feature. It allows a compatibility zone to grant ownership of parts of the Java package
namespace to registered users (for example, a CorDapp development organisation). The exact mechanism used to claim a namespace is up to the zone
operator. A typical approach would be to accept an SSL certificate with the domain in it as proof of domain ownership, or to accept an email from that domain.

A Java package namespace is case-insensitive and cannot be a sub-package of an existing registered namespace.
See Oracle's guidelines for [naming a package](https://docs.oracle.com/javase/tutorial/java/package/namingpkgs.html) and [naming conventions](https://www.oracle.com/technetwork/java/javase/documentation/codeconventions-135099.html#28840forguidelinesandconventions).

To register a Java package namespace, you need a signed certificate generated by the
[Java keytool](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/keytool.html).

You can register the package by supplying a network parameters override configuration file via the command line, using the `--network-parameter-overrides` command.

To register a package, you need to provide the:


* **packageName**:
  Java package name (for example, *com.my_company*).


* **keystore**:
  The path of the keystore file containing the signed certificate. If a relative path is provided, it is assumed to be relative to the
  location of the configuration file.


* **keystorePassword**:
  The password for the given keystore (not to be confused with the key password).


* **keystoreAlias**:
  The alias for the name associated with the certificate to be associated with the package namespace.

### Register a namespace with a sample CorDapp

We've created a sample CorDapp (available in [Java](https://github.com/corda/samples-java/tree/master/Basic/cordapp-example) and [Kotlin](https://github.com/corda/samples-kotlin/tree/master/Basic/cordapp-example)) you can use to practice initializing a simple network and registering and unregistering a package namespace.

1. Check the sample CorDapp out, then follow the [instructions to build it](../../../../../en/platform/corda/4.10/open-source/tutorial-cordapp.html#building-the-example-cordapp).

{{< note >}}
You can point to any existing bootstrapped network on Corda. This will update the associated network parameters file for that network).

{{< /note >}}

2. Create a new public key. You will use this to sign the Java package namespace you want to register:
```shell
$JAVA_HOME/bin/keytool -genkeypair -keystore _teststore -storepass MyStorePassword -keyalg RSA -alias MyKeyAlias -keypass MyKeyPassword -dname "O=Alice Corp, L=Madrid, C=ES"
```


This generates a keystore file called `_teststore` in the current directory.

3. Create a `network-parameters.conf` file in the same directory. Include this information:
```kotlin
packageOwnership=[
    {
        packageName="com.example"
        keystore="_teststore"
        keystorePassword="MyStorePassword"
        keystoreAlias="MyKeyAlias"
    }
]
```




4. Register the package namespace to be claimed by the public key generated earlier:
```shell
# Register the Java package namespace using the Network Bootstrapper
java -jar network-bootstrapper.jar --dir build/nodes --network-parameter-overrides=network-parameters.conf
```




5. To unregister the package namespace, edit the `network-parameters.conf` file to remove the package:
```kotlin
packageOwnership=[]
```




6. Unregister the package namespace:
```shell
# Unregister the Java package namespace using the Network Bootstrapper
java -jar network-bootstrapper.jar --dir build/nodes --network-parameter-overrides=network-parameters.conf
```






## Command line options

You can start the Network Bootstrapper with these command line options:

```shell
bootstrapper [-hvV] [--copy-cordapps=<copyCordapps>] [--dir=<dir>]
         [--event-horizon=<eventHorizon>] [--logging-level=<loggingLevel>]
         [--max-message-size=<maxMessageSize>]
         [--max-transaction-size=<maxTransactionSize>]
         [--minimum-platform-version=<minimumPlatformVersion>]
         [-n=<networkParametersFile>] [COMMAND]
```


* `--dir=<dir>`: Root directory containing the node configuration files and CorDapp `.jar`s that will form the test network.
  It may also contain existing node directories. It defaults to the current directory.
* `--copy-cordapps=<copyCordapps>`: This determines whether to copy the CorDapp `.jar`s into the node's ‘cordapps’ directory. Possible values:
  `FirstRunOnly`, `Yes`, `No`. Default: `FirstRunOnly`.
* `--verbose`, `--log-to-console`, `-v`: If set, this prints logging to the console and to a file.
* `--logging-level=<loggingLevel>`: Enables logging at this level and higher. Possible values: `ERROR`, `WARN`, `INFO`, `DEBUG`, and `TRACE`. Default: `INFO`.
* `--help`, `-h`: Shows the list of available commands, and the exit option.
* `--version`, `-V`: Prints version information and exit.
* `--minimum-platform-version`: The minimum platform version to use in the `network-parameters`.
* `--max-message-size`: The maximum message size to use in the `network-parameters`, in bytes.
* `--max-transaction-size`: The maximum transaction size to use in the `network-parameters`, in bytes.
* `--event-horizon`: The event horizon to use in the `network-parameters`.
* `--network-parameter-overrides=<networkParametersFile>`, `-n=<networkParametersFile>`: Overrides the default network parameters with the parameters
  in the file provided. See [Overriding network parameters via a file](#overriding-network-parameters-via-a-file).


### Sub-commands

`install-shell-extensions`: Installs the `bootstrapper` alias and auto-completion for bash and zsh. See [Shell extentions for CLI applications](../../../../../en/platform/corda/4.10/open-source/cli-application-shell-extensions.html#shell-extensions-for-cli-applications).
