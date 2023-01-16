---
date: '2021-09-06'
title: "Setting up a local Corda 5 development network"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-gettingstarted
    weight: 500
section_menu: corda-5-dev-preview
expiryDate: '2022-09-28'
---

In this document, you will learn how to set up a local Corda 5 development network using Docker. You can then use this network to perform manual and/or automated testing.

Use this procedure if you are developing a CorDapp but not deploying it to a production environment.

{{< note >}}

In the Corda 5 Developer Preview release, the notaries support non-validating mode only. Validating mode is not supported.

{{< /note >}}


## Before you start

Before you begin, make sure you [install the Corda 5 Developer Preview](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/overview.md).


## Configure your network

To configure your network, run the following Corda CLI command:

```console
corda-cli network config <network-type> <network-name>
```

Where:
* `network-type` is the type of the network. Currently only `docker-compose` is supported.
* `network-name` is the name of the network.

For example, to configure the `smoke-tests-network`, use:

```console
corda-cli network config docker-compose smoke-tests-network
```

This command configures the `smoke-tests-network` for Docker Compose, ready for deployment.


## Create network definitions file

1. Create a network definition `<network-name>.yaml` file in the root of your project.

   The network definition `.yaml` file is a template for the network you want to deploy. This template allows you to configure how the nodes will be set up.

2. Add parameters to your newly-created `<network-name>.yaml` file.

   This is an example of a `.yaml` file with its parameters:

   ```yaml
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

1. Deploy your network by running one of the following commands:

   * If you are in the same directory as your `<network-name>.yaml` file, run:

      ```console
      corda-cli network deploy -n <network-name> | docker-compose -f - up -d
      ```

   * If you are not in the directory of your `<network-name>.yaml` file, run:

      ```console
      corda-cli network deploy -n <network-name> -f <network-name.yaml file location> | docker-compose -f - up -d
      ```

   The `corda-cli network deploy` command looks for the type of network and a network definition file (by default in the local directory) with the name `<network-name>.yaml`. It  outputs a `.yaml` file to stdout that Docker Compose can use to create your local test network.

   {{< note >}}

   When using the docker-compose `up` command, it's recommended to use it in detached mode (`-d`).

   {{< /note >}}

2. Wait for the nodes to run. You can monitor nodes starting up by running this command:

   ```console
   corda-cli network wait -n <network-name>
   ```

   This command inspects the logs every few seconds until all the nodes are ready.

   {{< note >}}

   During network deployment, the nodes' keys, key stores, and certificates are generated automatically.

   {{< /note >}}


3. To monitor logs, run this Corda CLI command:

   ```
   corda-cli network deploy -n <network-name> | docker-compose -f - logs -f
   ```

    The terminal displays the standard output of all the nodes in the network. Once a network is running, it shows a message similar to: `Running P2PMessaging loop`. You must wait for all the nodes to run. When all nodes have run, an output similar to the output shown below will appear.

    ```console
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


## Troubleshooting

If you encounter any issues while deploying your local Corda 5 network, see [Corda 5 local network troubleshooting](../../../../../en/platform/corda/5.0-dev-preview-1/getting-started/troubleshooting/network-troubleshooting.md).
