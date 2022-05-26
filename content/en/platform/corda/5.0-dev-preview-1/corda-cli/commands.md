---
date: '2021-09-01'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordacli
    weight: 400
section_menu: corda-5-dev-preview
title: "Corda CLI commands"
description: >
  Corda CLI commands used for managing Corda network and Corda package files.
---

## Get help in the Corda CLI

To access help and get the Corda CLI version number, use the following command structure:

`corda-cli [-hv] [--stacktrace] [COMMAND]`

### Options

`-h, --help`
See a list of available commands and descriptions.

`--stacktrace`
Print out the stacktrace for all exceptions.

`-v, --version`
See the current version of the Corda CLI you are using.


### Overview of available commands

The main Corda CLI commands are:

`network`
Manage a network.

`package, pkg`
Commands to handle Corda package files (`.cpk`, `.cpb`, `.cpi`) and `.jar`s.


## Manage a network

You can use the `network` command in the Corda CLI to deploy and configure a network, list available networks, get the network's status, wait for a network to start or terminate and to remove containers from a running network. Also, you can use it to configure or restart nodes present in a network.

### Syntax

`corda-cli network [-h] [--stacktrace] [COMMAND]`

### Options

`-h, --help`
See a list of available `network` subcommands and descriptions.

`--stacktrace`
Print out the stacktrace for all exceptions.


### Subcommands

#### **`configure, config, conf`**

Use this command to configure a node or a network.

##### Syntax

````console
corda-cli network configure [-h] [--stacktrace] <deploymentType> <networkName>
````

##### Options

`-h, --help`
See a list of available options and arguments with descriptions.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Arguments

`<deploymentType>`
The type of the deployment values: k8s, docker-compose.

`<networkName>`
The name of the network.

##### Example

````console
corda-cli network config docker-compose test-network
Network test-network configured to be docker-compose
````

#### **`list, ls`**

List available networks.

##### Syntax

````console
corda-cli network list [-h] [--stacktrace]
````

##### Options

`-h, --help`
See a list of available options with descriptions.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Example

````console
corda-cli network list
Available networks:
docker-compose
 - test-network
````

#### **`deploy`**

Deploy a network.

##### Syntax

````console
corda-cli network deploy [-h] [--stacktrace] [-f=<file>] -n=<networkName> [-p=<firstPort>] [-r=<containerRegistry>] [-t=<containerImageTag>]
````

##### Options

`-f, --file=<file>`
The file location. Defaults to `./<name>.yaml`

`-h, --help`
See a list of available options.

`-n, --network, --networkName=<networkName>`
The name of the network.

`-p, --port=<firstPort>`
The first port to use. If not specified, it will start looking for free ports from port 12111.

`-r, --container-registry=<containerRegistry>`
The default container registry to use for the test container.

`--stacktrace`
Print out the stacktrace for all exceptions.

`-t, --container-tag=<containerImageTag>`
The default image tag to use for the test container. If not specified, it will use the latest one.

##### Example

````console
corda-cli network deploy -n smoke-tests-network -f "C:\Users\<user-name>\Desktop\smoke-tests-network.yaml" | docker-compose -f - up
...output was trimmed...
smoke-tests-network-notary | Loaded 0 CorDapp(s)                     :
smoke-tests-network-notary | Node for "notary" started up and registered in 17.31 sec
smoke-tests-network-notary | SSH server listening on port            : 22222
smoke-tests-network-notary | Running P2PMessaging loop
smoke-tests-network-alice | Loaded 0 CorDapp(s)                     :
smoke-tests-network-alice | Node for "alice" started up and registered in 17.08 sec
smoke-tests-network-alice | SSH server listening on port            : 22222
smoke-tests-network-alice | Running P2PMessaging loop
smoke-tests-network-bob | Loaded 0 CorDapp(s)                     :
smoke-tests-network-bob | Node for "bob" started up and registered in 16.79 sec
smoke-tests-network-bob | SSH server listening on port            : 22222
smoke-tests-network-bob | Running P2PMessaging loop
smoke-tests-network-caroline | Loaded 0 CorDapp(s)                     :
smoke-tests-network-caroline | Node for "caroline" started up and registered in 19.33 sec
smoke-tests-network-caroline | SSH server listening on port            : 22222
smoke-tests-network-caroline | Running P2PMessaging loop
````


#### **`status`**

Get network status.

##### Syntax

````console
corda-cli network status [-h] [--stacktrace] [-f=<format>] -n=<networkName>
````

##### Options

`-f, --format=<format>`
Set the output format to either json, pretty-json, yaml, or text. Defaults to text.

`-h, --help`
See a list of available options.

`-n, --network, --networkName=<networkName>`
The name of the network.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Example

````console
corda-cli network status -n test-network
Network test-network status:
         with type: docker-compose
         has started and has nodes:
                 service caroline: Starting
                         test-network-caroline (22db63258903)
                         x500 name: O=caroline, L=London, C=GB
                         Node Role: Notary
                         Ports:
                                HTTP RPC port: 12119
                                Node agent port: 12120
                                Debug Disabled
                         Startup stage: Running corda.jar
                 service alice-db: Ready
                         test-network-alice-db (3f85082904e9)
                         postgres database with public port: 12121
                 service bootstrapper: Ready
                         test-network-bootstrapper (6f1c06349f24)
                 service bob: Starting
                         test-network-bob (b911ecddd18e)
                         x500 name: O=bob, L=London, C=GB
                         Node Role: Corda Node
                         Ports:
                                HTTP RPC port: 12116
                                Node agent port: 12117
                                Debug Disabled
                         Startup stage: corda.jar failed
                 service alice: Starting
                         test-network-alice (e5db8f9d85da)
                         x500 name: O=Borrower, C=GB, L=LONDON, CN=blah-Inc
                         Node Role: Corda Node
                         Ports:
                                HTTP RPC port: 12112
                                Node agent port: 12113
                                Debug port: 12114
                         Startup stage: Running corda.jar
````


#### **`wait`**

Wait for a network to start (by default) or terminate (use `--terminate`).

##### Syntax

````console
corda-cli network wait [-h] [--stacktrace] [--terminate] -n=<networkName> [-t=<timeout>]
````

##### Options

`-h, --help`
See a list of available options.

`-n, --network, --networkName=<networkName>`
The name of the network.

`--stacktrace`
Print out the stacktrace for all exceptions.

`-t, --timeout=<timeout>`
How many minutes to wait. Defaults to `7`.

`--terminate`
Wait for the network to terminate.

##### Example

````console
corda-cli --stacktrace network wait -n smoke-tests-network -t 20
waiting for smoke-tests-network...
Getting status...
Node alice is not ready
Getting status...
...output was trimmed...
Getting status...
Node alice is ready
Node alice is ready
Node alice-db is ready
Node bob is ready
Node bob is ready
Node bob-db is ready
Node bootstrapper is ready
Node caroline is ready
Node notary is ready
Network smoke-tests-network is ready
````


#### **`terminate`**

Terminate and remove containers from a running network.

##### Syntax

````console
corda-cli network terminate [-fhry] [--stacktrace] -n=<networkName>
````

##### Options

`-f, --forget`
Forget the network after stopping it.

`-h, --help`
See a list of available options.

`-n, --network, --networkName=<networkName>`
The name of the network.

`-r, --reset`
Reset the network after stopping it.

`--stacktrace`
Print out the stacktrace for all exceptions.

`-y, --assume-yes`
Assume `Yes` to all queries and do not prompt.

##### Example

````console
corda-cli network terminate -fry -n test-network
Terminating test-network...
Network test-network terminated.
Deleting local files for test-network...
Deleting test-network configuration
````


#### **`restart`**

Restart a node.

##### Syntax

````console
corda-cli network restart [-hr] [--stacktrace] [-m=<nodeName>] -n=<networkName>
````

##### Options

`-h, --help`
See a list of available options.

`-m, --node, --nodeName=<nodeName>`
The name of the node to restart. Omit to restart all the nodes.

`-n, --network, --networkName=<networkName>`
The name of the network.

`-r, --run-migration`
Run migration script.

`--stacktrace`
Print out the stacktrace for all exceptions.


##### Example

````console
corda-cli network restart -n test-network
caroline: Restarting caroline...
bob: Restarting bob...
alice: Restarting alice...
caroline: caroline restarted
bob: bob restarted
alice: alice restarted
````

## CPK tool

You can use the Corda CLI `package` command to install CorDapps on nodes as well as inspect the contents of Corda package files. Corda package file names can end with `.cpi`, `.cpk` and `.cpb`. This command can also be used to inspect `.jar` files.

### Syntax

`corda-cli package [-hv] [--stacktrace] [COMMAND]`

### Options

`-h, --help`
See a list of available package subcommands and descriptions.

`--stacktrace`
Print out the stacktrace for all exceptions.

`-v, --version`
Display version info.


### Subcommands

#### **`list, ls`**

This command recursively lists the content of any Corda package file (`.cpk`, `.cpi`, `.cpb`), which can contain other Corda package files, and so on.

##### Syntax

````console
corda-cli package list [-hl] [--stacktrace] <path>
````

##### Options

`-h, --help`
See a list of available options.

`-l`
Use long listing format.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Arguments

`<path>`
Path to a Corda package.

##### Example

````console
corda-cli pkg ls httprpc-demo.cpb
httprpc-demo.cpb:install.json
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/CORDAPP.SF
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/CORDAPP.EC
...
````

#### **`cat`**

Concatenate the contents of a `.cpk` or a `.cpi` file, or a file in a nested `.jar`.

{{< note >}}

Paths to the nested files can be found by using the `list` command.

{{< /note >}}

##### Syntax

````console
corda-cli package cat [-h] [--stacktrace] <nested:path>
````

##### Options

`-h, --help`
See a list of available options.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Arguments

`<nested:path>`
The the root file system path, and nested paths with in the archive concatenated by `:`.

##### Example

````console
corda-cli pkg ls httprpc-demo.cpb
httprpc-demo.cpb:install.json
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF

$ corda-cli pkg cat httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF
Manifest-Version: 1.0
Corda-CPK-Format: 1.0
Corda-CPK-Cordapp-Name: net.corda.httprpc-demo-workflows
Corda-CPK-Cordapp-Version: 1.0.0.SNAPSHOT
Corda-CPK-Cordapp-Licence: Open Source (Apache 2)
Corda-CPK-Cordapp-Vendor: R3
Corda-CPK-Built-Platform-Version: 999

Name: httprpc-demo-workflows-1.0.0-SNAPSHOT.jar
SHA-256-Digest: Kz8WY20GJMypiomOlhMLHb6TlgXn8sKVVBr6/Pt/ny8=
...
````

#### **`depends, deps`**

This is a convenience subcommand that recursively lists all `CPKDependency` and `DependencyConstraints` files in the specified file.

##### Syntax

````console
corda-cli package depends [-h] [--stacktrace] <path>
````

##### Options

`-h, --help`
See a list of available options.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Arguments

`<path>`
Path to a Corda package.

##### Example

````console
corda-cli pkg deps httprpc-demo.cpb

httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-contracts-1.0.0-SNAPSHOT.jar:META-INF/CPKDependencies:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cpkDependencies xmlns="urn:corda-cpk"/>

httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-contracts-1.0.0-SNAPSHOT.jar:META-INF/DependencyConstraints:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dependencyConstraints xmlns="urn:corda-cpk"/>

httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-workflows-1.0.0-SNAPSHOT.jar:META-INF/CPKDependencies:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cpkDependencies xmlns="urn:corda-cpk">
    <cpkDependency>
        <name>net.corda.flows</name>
        <version>1.0.0.SNAPSHOT</version>
        <signers>
            <signer algorithm="SHA-256">qlnYKfLKj931q+pA2BX5N+PlTlcrZbk7XCFq5llOfWs=</signer>
        </signers>
    </cpkDependency>
    <cpkDependency>
        <name>net.corda.httprpc-demo-contracts</name>
        <version>1.0.0.SNAPSHOT</version>
        <signers>
            <signer algorithm="SHA-256">qlnYKfLKj931q+pA2BX5N+PlTlcrZbk7XCFq5llOfWs=</signer>
        </signers>
    </cpkDependency>
</cpkDependencies>

httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-workflows-1.0.0-SNAPSHOT.jar:META-INF/DependencyConstraints:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dependencyConstraints xmlns="urn:corda-cpk"/>
````

#### **`install`**

This command installs a CorDapp to one or all nodes in the network.

##### Syntax

````console
corda-cli package install [-hs] [--stacktrace] [-m=<nodeName>] -n=<networkName> <cordapps>…​
````

##### Options

`-h, --help`
See a list of available options.

`-m, --node, --nodeName=<nodeName>`
The name of the node to apply the command to. You can omit the `-m` to apply the command to all the nodes.

`-n, --network, --networkName=<networkName>`
The name of the network.

`-s, --skip-notaries`
Skip deploying app(s) to the notary node.

`--stacktrace`
Print out the stacktrace for all exceptions.

##### Arguments

`<cordapps>…​`
Path to the `.cpk`/`.cpb` file(s) with the CorDapp to deploy.

##### Example

````console
corda-cli pkg install -n smoke-tests-network solar-system.cpb
Deploying apps to nodes: [notary, bob, alice]
bob: bob will have apps deployed to it
alice: alice will have apps deployed to it
notary: notary will have apps deployed to it
alice: Copying files to alice...
bob: Copying files to bob...
alice: solar-system.cpb (/home/ben/projects/Corda5-SolarSystem/solar-system.cpb)...
notary: Copying files to notary...
bob: solar-system.cpb (/home/ben/projects/Corda5-SolarSystem/solar-system.cpb)...
notary: solar-system.cpb (/home/ben/projects/Corda5-SolarSystem/solar-system.cpb)...
alice: Restarting alice
notary: Restarting notary
bob: Restarting bob
notary: Node smoke-tests-network/notary was deployed with [solar-system.cpb]
alice: Node smoke-tests-network/alice was deployed with [solar-system.cpb]
bob: Node smoke-tests-network/bob was deployed with [solar-system.cpb]
Network smoke-tests-network was deployed with [solar-system.cpb]
````

### Removing a CorDapp

{{< note >}}
It is not currently possible to remove a CorDapp from the network. Instead, you can terminate the network and reset it.
{{< /note >}}

To remove a CorDapp in the Corda 5 Developer Preview:

1. Terminate the local network: run `terminate -rn <name of network>`.
2. Deploy a new network using the guide for [deploying a new network](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/setup-network.md).
