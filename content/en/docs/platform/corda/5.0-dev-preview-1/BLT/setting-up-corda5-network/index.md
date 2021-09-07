---
date: '2021-09-06'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-network
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
title: Setting up a local Corda 5 development network
---

Use this procedure if you are developing a CorDapp but not deploying it to a production environment. In this document, you will learn how to:

* Set up a local Corda 5 development network using Docker.
* Deploy nodes to your network.

You can then use this network to perform manual and/or automated testing.

{{< note >}}

In the Corda 5 Developer Preview release, the notaries support the non-validating mode only. The validating mode is not supported.

{{< /note >}}


## Before you start

Before you begin, make sure you [set up your development environment first](XXX).


## Configure your network

Configure your network by running the following Corda CLI command:

`corda-cli network config <network-type> <network-name>`

Where:
* `network-type` is the type of the network - currently only docker-compose is supported.
* `network-name` is the name of the network.

For example, to run the iou-sample network, use:

`corda-cli network config docker-compose iou-sample`

**Step result:** An entry is added to `~/.corda/network.yaml` with the name and the type of the network.


## Create network definitions file

1. Create a network definition `<network-name>.yaml` file in the root of your project.

   A network definition file is a `.yaml` file that has an entry for each node. The network is created based on defaults, unless otherwise specified.

2. Add parameters to your newly created `<network-name>.yaml` file.

   This is an example of a `.yaml` file with its parameters:

```
# Nodes in network
nodes:
  # Name of the node
  alice:
    # (Optional) Specify the X500 name of the node
    x500: "O=Borrower, C=GB, L=LONDON, CN=blah-Inc"
    # (Optional) Specify the database type: "postgres:13" or "H2" (default)
    database: "postgres:13"
    # (Optional) Enable remote debugging of the Corda node
    debug: true
    # (Optional) Specify users and permissions
    users:
      fred:
        password: mySecretPassword
        permissions: ["ALL"]
      alfred:
        password: alfredPassword
  bob:
  caroline:
    # (Optional) Indicate if the node is a notary
    notary: true
```


## Deploy your network

1. Deploy your network by running the following command:

   `corda-cli network deploy -n <network-name> | docker-compose -f - up -d`

   The `corda-cli network deploy` command will look for the type of network and a network definition file (by default in the local directory) with the name `<network-name>.yaml`. Also, it will create a `.yaml` file that the Docker Compose can use to create a collections of containers and a network.

   {{< note >}}

   When using docker-compose, it's recommended to use the detached mode (`-d`).

   {{< /note >}}

2. Wait for the nodes to run. You can monitor nodes starting by using the following command:

   `corda-cli network deploy -n <network-name> | docker-compose -f - logs -f`

   The terminal displays the standard output of all the nodes in the network. Once a network is running, it shows a message similar to: `Running P2PMessaging loop`. You must wait for all the nodes to run. When all nodes have run, an output similar to the output shown below will appear.

   ```
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
   ```

3. **Optional:** To monitor logs, you can also use the following Corda CLI command:

   `corda-cli network wait -n <network-name>`

   This command inspects the logs every few seconds until all the nodes are ready.
