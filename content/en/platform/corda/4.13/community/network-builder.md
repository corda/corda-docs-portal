---
aliases:
- /head/network-builder.html
- /HEAD/network-builder.html
- /network-builder.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-13:
    identifier: corda-community-4-13-network-builder
    parent: corda-community-4-13-tools-index
    weight: 1010
tags:
- network
- builder
title: Corda Network Builder
---


# Corda Network Builder

The Corda Network Builder is a tool for building Corda networks for testing purposes. It leverages Docker and
containers to abstract the complexity of managing a distributed network away from the user.

{{< figure alt="network builder v4" width=80% zoom="/en/images/network-builder-v4.png" >}}
The network you build will either be made up of local `Docker` nodes *or* of nodes spread across Azure
containers.
For each node, a separate Docker image is built based on [corda/corda-zulu-java1.8-4.4](https://hub.docker.com/r/corda/corda-zulu-java1.8-4.4).
Unlike the official image, a *node.conf* file and CorDapps are embedded into the image
(they are not externally provided to the running container via volumes/mount points).
More backends may be added in future. The tool is open source, so contributions to add more
destinations for the containers are welcome!

Download the Corda Network Builder from `https://download.corda.net/maven/corda-releases/net/corda/corda-tools-network-builder/|corda_version|/corda-tools-network-builder-|corda_version|-all.jar`.

## Prerequisites

- **Docker:** Docker version greater than v17.12.0-ce
- **Azure:** An authenticated Azure CLI greater than or equal to v2.0; see: [How to install the Azure CLI on Windows
](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)

## Creating the base nodes

The network builder uses a set of nodes as the base for all other operations. A node is anything that satisfies
the following layout:

```shell
-
 -- node.conf
 -- corda.jar
 -- cordapps/
```

An easy way to build a valid set of nodes is by running `deployNodes`. In this document, we will be using the output of running `deployNodes` for the [Java samples repository](https://github.com/corda/samples-java/tree/release/4.13).

Run the following commands:

1 `git clone https://github.com/corda/samples-java/tree/release/4.13`
2 `cd samples-java/Basic/cordapp-example`
3 `./gradlew clean workflows-java:deployNodes`


## Building a network via the command line

### Starting the nodes

#### Quickstart local Docker

Run the following commands:

1. `cd workflows-java/build/nodes`
2. `java -jar <path/to/corda-tools-network-builder.jar> -d .`

If you run `docker ps` to see the running containers, the following output should be displayed:

```shell
CONTAINER ID        IMAGE                       COMMAND         CREATED             STATUS              PORTS                                                                                                    NAMES
406868b4ba69        node-partyc:corda-network   "run-corda"     17 seconds ago      Up 16 seconds       0.0.0.0:32902->10003/tcp, 0.0.0.0:32895->10005/tcp, 0.0.0.0:32898->10020/tcp, 0.0.0.0:32900->12222/tcp   partyc0
4546a2fa8de7        node-partyb:corda-network   "run-corda"     17 seconds ago      Up 17 seconds       0.0.0.0:32896->10003/tcp, 0.0.0.0:32899->10005/tcp, 0.0.0.0:32901->10020/tcp, 0.0.0.0:32903->12222/tcp   partyb0
c8c44c515bdb        node-partya:corda-network   "run-corda"     17 seconds ago      Up 17 seconds       0.0.0.0:32894->10003/tcp, 0.0.0.0:32897->10005/tcp, 0.0.0.0:32892->10020/tcp, 0.0.0.0:32893->12222/tcp   partya0
cf7ab689f493        node-notary:corda-network   "run-corda"     30 seconds ago      Up 31 seconds       0.0.0.0:32888->10003/tcp, 0.0.0.0:32889->10005/tcp, 0.0.0.0:32890->10020/tcp, 0.0.0.0:32891->12222/tcp   notary0
```

Depending on you machine performance, even after all containers are reported as running,
the underlying Corda nodes may be still starting and SSHing to a node may be not available immediately.

#### Quickstart Remote Azure

{{< important >}}
Before starting the deployment, ensure that you set the `AZURE_SUBSCRIPTION_ID` environment variable to your default subscription; for example, `export AZURE_SUBSCRIPTION_ID=<default_subscription_id>`. This prevents Azure API errors when calling `getDefaultSubscription()`, which will fail if multiple subscriptions exist in your tenant.
{{</ important >}}

Run the following commands:

1. `cd kotlin-source/build/nodes`
2. `java -jar <path/to/corda-tools-network-builder.jar> -b AZURE -d .`

{{< note >}}
The Azure configuration is handled by the Azure CLI utility; see [Prerequisites](#prerequisites).

{{< /note >}}

### Interacting with the nodes

You can interact with the nodes by SSHing into them on the port that is mapped to 12222. For example, to SSH into the
`partya0` node, you would run:

```shell
ssh user1@localhost -p 32893
Password authentication
Password:


Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

>>> run networkMapSnapshot
[
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 6, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 6, "serial" : 1532701330118 }
]

>>>
```

You can also run a flow from `cordapp-example`: 

- `flow start net.corda.samples.example.flows.ExampleFlow$Initiator iouValue: 20, otherParty: "PartyB"`

To verify it:

1. Connect to the `partyb0` node.
2. Execute:

   `run vaultQuery contractStateType: "net.corda.samples.example.states.IOUState".`

The `partyb0` vault should contain `IOUState`.

### Adding additional nodes

It is possible to add additional nodes to the network by reusing the nodes you built earlier. For example, to add a
node by reusing the existing `PartyA` node, you would run:

`java -jar <path/to/corda-tools-network-builder.jar> --add "PartyA=O=PartyZ,L=London,C=GB"`

To confirm the node has been started correctly, run the following in the previously connected SSH session:

```shell
Tue Jul 17 15:47:14 GMT 2018>>> run networkMapSnapshot
[
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 6, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 6, "serial" : 1532701330118 },
  { "addresses" : [ "partya1:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyZ, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701630861 }
]
```

## Building a network in Graphical User Mode

The Corda Network Builder also provides a GUI for when automated interactions are not required. To launch it, run
`java -jar <path/to/corda-tools-network-builder.jar> -g`.

### Starting the nodes

1. Click **Open nodes ...**.
2. Select the folder where you built your nodes in [Creating the base nodes](#creating-the-base-nodes).
3. Click **Open**.
4. Select **Local Docker** or **Azure**.
5. Click `Build`.

{{< note >}}
The Azure configuration is handled by the Azure CLI utility; see [Prerequisites](#prerequisites).

{{< /note >}}
All the nodes should eventually move to a `Status` of `INSTANTIATED`. If you run `docker ps` from the terminal to
see the running containers, the following output should be displayed:

```shell
CONTAINER ID        IMAGE                       COMMAND         CREATED             STATUS              PORTS                                                                                                    NAMES
406868b4ba69        node-partyc:corda-network   "run-corda"     17 seconds ago      Up 16 seconds       0.0.0.0:32902->10003/tcp, 0.0.0.0:32895->10005/tcp, 0.0.0.0:32898->10020/tcp, 0.0.0.0:32900->12222/tcp   partyc0
4546a2fa8de7        node-partyb:corda-network   "run-corda"     17 seconds ago      Up 17 seconds       0.0.0.0:32896->10003/tcp, 0.0.0.0:32899->10005/tcp, 0.0.0.0:32901->10020/tcp, 0.0.0.0:32903->12222/tcp   partyb0
c8c44c515bdb        node-partya:corda-network   "run-corda"     17 seconds ago      Up 17 seconds       0.0.0.0:32894->10003/tcp, 0.0.0.0:32897->10005/tcp, 0.0.0.0:32892->10020/tcp, 0.0.0.0:32893->12222/tcp   partya0
cf7ab689f493        node-notary:corda-network   "run-corda"     30 seconds ago      Up 31 seconds       0.0.0.0:32888->10003/tcp, 0.0.0.0:32889->10005/tcp, 0.0.0.0:32890->10020/tcp, 0.0.0.0:32891->12222/tcp   notary0
```


### Adding additional nodes

It is possible to add additional nodes to the network by reusing the nodes you built earlier. For example, to add a
node by reusing the existing `PartyA` node, you would:

1. Select **partya** in the dropdown.
2. Click **Add Instance**.
3. Specify the new node’s X500 name and click **OK**.

If you click on `partya` in the pane, you should see an additional instance listed in the sidebar. To confirm the
node has been started correctly, run the following in the previously connected SSH session:

```shell
Tue Jul 17 15:47:14 GMT 2018>>> run networkMapSnapshot
[
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 6, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 6, "serial" : 1532701330118 },
  { "addresses" : [ "partya1:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyZ, L=London, C=GB" ], "platformVersion" : 6, "serial" : 1532701630861 }
]
```

## Shutting down the nodes

Run `docker kill $(docker ps -q)` to kill all running Docker processes.
