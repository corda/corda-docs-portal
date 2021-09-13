---
aliases:
- /releases/4.1/network-builder.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-network-builder
    parent: corda-enterprise-4-1-tools-index
    weight: 1010
tags:
- network
- builder
title: Corda Network Builder
---


# Corda Network Builder


The Corda Network Builder is a tool for building Corda networks for testing purposes. It leverages Docker and
containers to abstract the complexity of managing a distributed network away from the user.

![network builder v4](/en/images/network-builder-v4.png "network builder v4")
The network you build will either be made up of local `docker` nodes *or* of nodes spread across Azure
containers. More backends may be added in future. The tool is open source, so contributions to add more
destinations for the containers are welcome!

[Download the Corda Network Builder](https://software.r3.com/artifactory/corda-releases/net/corda/corda-network-builder/4.0-corda/corda-network-builder-4.0-corda-executable.jar).



## Prerequisites


* **Docker:** docker > 17.12.0-ce
* **Azure:** authenticated az-cli >= 2.0 (see: [https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest))



## Creating the base nodes

The network builder uses a set of nodes as the base for all other operations. A node is anything that satisfies
the following layout:

```shell
-
 -- node.conf
 -- corda.jar
 -- cordapps/
```

An easy way to build a valid set of nodes is by running `deployNodes`. In this document, we will be using
the output of running `deployNodes` for the [Example CorDapp](https://github.com/corda/cordapp-example):


* `git clone https://github.com/corda/cordapp-example`
* `cd cordapp-example`
* `./gradlew clean deployNodes`


## Building a network via the command line


### Starting the nodes


#### Quickstart Local Docker


* `cd kotlin-source/build/nodes`
* `java -jar <path/to/network-builder-jar> -d .`

If you run `docker ps` to see the running containers, the following output should be displayed:

```shell
CONTAINER ID        IMAGE                       COMMAND             CREATED             STATUS              PORTS                                                                                                    NAMES
406868b4ba69        node-partyc:corda-network   "/run-corda.sh"     17 seconds ago      Up 16 seconds       0.0.0.0:32902->10003/tcp, 0.0.0.0:32895->10005/tcp, 0.0.0.0:32898->10020/tcp, 0.0.0.0:32900->12222/tcp   partyc0
4546a2fa8de7        node-partyb:corda-network   "/run-corda.sh"     17 seconds ago      Up 17 seconds       0.0.0.0:32896->10003/tcp, 0.0.0.0:32899->10005/tcp, 0.0.0.0:32901->10020/tcp, 0.0.0.0:32903->12222/tcp   partyb0
c8c44c515bdb        node-partya:corda-network   "/run-corda.sh"     17 seconds ago      Up 17 seconds       0.0.0.0:32894->10003/tcp, 0.0.0.0:32897->10005/tcp, 0.0.0.0:32892->10020/tcp, 0.0.0.0:32893->12222/tcp   partya0
cf7ab689f493        node-notary:corda-network   "/run-corda.sh"     30 seconds ago      Up 31 seconds       0.0.0.0:32888->10003/tcp, 0.0.0.0:32889->10005/tcp, 0.0.0.0:32890->10020/tcp, 0.0.0.0:32891->12222/tcp   notary0
```


#### Quickstart Remote Azure


* `cd kotlin-source/build/nodes`
* `java -jar <path/to/network-builder-jar> -b AZURE -d .`

{{< note >}}
The Azure configuration is handled by the az-cli utility. See the [Prerequisites](#pre-requisites).

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
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 3, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 3, "serial" : 1532701330118 }
]

>>>
```


### Adding additional nodes

It is possible to add additional nodes to the network by reusing the nodes you built earlier. For example, to add a
node by reusing the existing `PartyA` node, you would run:

`java -jar <network-builder-jar> --add "PartyA=O=PartyZ,L=London,C=GB"`

To confirm the node has been started correctly, run the following in the previously connected SSH session:

```shell
Tue Jul 17 15:47:14 GMT 2018>>> run networkMapSnapshot
[
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 3, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 3, "serial" : 1532701330118 },
  { "addresses" : [ "partya1:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyZ, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701630861 }
]
```


## Building a network in Graphical User Mode

The Corda Network Builder also provides a GUI for when automated interactions are not required. To launch it, run
`java -jar <path/to/network-builder-jar> -g`.


### Starting the nodes


* Click `Open nodes ...` and select the folder where you built your nodes in [Creating the base nodes](#creating-the-base-nodes) and
click `Open`
* Select `Local Docker` or `Azure`
* Click `Build`

{{< note >}}
The Azure configuration is handled by the az-cli utility. See the [Prerequisites](#pre-requisites).

{{< /note >}}
All the nodes should eventually move to a `Status` of `INSTANTIATED`. If you run `docker ps` from the terminal to
see the running containers, the following output should be displayed:

```shell
CONTAINER ID        IMAGE                       COMMAND             CREATED             STATUS              PORTS                                                                                                    NAMES
406868b4ba69        node-partyc:corda-network   "/run-corda.sh"     17 seconds ago      Up 16 seconds       0.0.0.0:32902->10003/tcp, 0.0.0.0:32895->10005/tcp, 0.0.0.0:32898->10020/tcp, 0.0.0.0:32900->12222/tcp   partyc0
4546a2fa8de7        node-partyb:corda-network   "/run-corda.sh"     17 seconds ago      Up 17 seconds       0.0.0.0:32896->10003/tcp, 0.0.0.0:32899->10005/tcp, 0.0.0.0:32901->10020/tcp, 0.0.0.0:32903->12222/tcp   partyb0
c8c44c515bdb        node-partya:corda-network   "/run-corda.sh"     17 seconds ago      Up 17 seconds       0.0.0.0:32894->10003/tcp, 0.0.0.0:32897->10005/tcp, 0.0.0.0:32892->10020/tcp, 0.0.0.0:32893->12222/tcp   partya0
cf7ab689f493        node-notary:corda-network   "/run-corda.sh"     30 seconds ago      Up 31 seconds       0.0.0.0:32888->10003/tcp, 0.0.0.0:32889->10005/tcp, 0.0.0.0:32890->10020/tcp, 0.0.0.0:32891->12222/tcp   notary0
```


### Interacting with the nodes

See [Interacting with the nodes](#interacting-with-the-nodes).


### Adding additional nodes

It is possible to add additional nodes to the network by reusing the nodes you built earlier. For example, to add a
node by reusing the existing `PartyA` node, you would:


* Select `partya` in the dropdown
* Click `Add Instance`
* Specify the new node’s X500 name and click `OK`

If you click on `partya` in the pane, you should see an additional instance listed in the sidebar. To confirm the
node has been started correctly, run the following in the previously connected SSH session:

```shell
Tue Jul 17 15:47:14 GMT 2018>>> run networkMapSnapshot
[
  { "addresses" : [ "partya0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyA, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701330613 },
  { "addresses" : [ "notary0:10020" ], "legalIdentitiesAndCerts" : [ "O=Notary, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701305115 },
  { "addresses" : [ "partyc0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyC, L=Paris, C=FR" ], "platformVersion" : 3, "serial" : 1532701331608 },
  { "addresses" : [ "partyb0:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyB, L=New York, C=US" ], "platformVersion" : 3, "serial" : 1532701330118 },
  { "addresses" : [ "partya1:10020" ], "legalIdentitiesAndCerts" : [ "O=PartyZ, L=London, C=GB" ], "platformVersion" : 3, "serial" : 1532701630861 }
]
```


## Shutting down the nodes

Run `docker kill $(docker ps -q)` to kill all running Docker processes.

