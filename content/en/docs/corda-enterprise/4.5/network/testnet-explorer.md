---
date: '2020-09-20T09:59:25Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-networks-testnet
tags:
- testnet
- explorer
title: Using the Node Explorer to test a Corda Enterprise node on Corda Testnet
weight: 3
---


# Using the Node Explorer to test a Corda Enterprise node on Corda Testnet

This document will explain how to test the installation of a Corda Enterprise node on Corda Testnet.


## Prerequisites

This guide assumes you have deployed a Corda Enterprise node to either Azure or AWS using one of:


* Azure Resource Manager Templates (ARM Templates) on the [Azure Marketplace](https://portal.azure.com/#blade/Microsoft_Azure_Marketplace/GalleryFeaturedMenuItemBlade/selectedMenuItemId/Blockchain_MP/resetMenuId/)
* [AWS Quick Start Template](https://aws.amazon.com/quickstart/)



It also assumes your node is provisioned and connected to the Corda Testnet although the instructions below should work
for any Corda Enterprise node connected to any Corda network.

{{< note >}}
If you need to set up a Corda Enterprise node using the Cloud templates, see: [Using Azure Resource Manager Templates to deploy a Corda Enterprise node](azure-template-guide.md).

{{< /note >}}

## Get the testing tools

To run the tests and make sure your node is connecting correctly to the network you will need to download and install a
couple of resources.


* Log into your Cloud VM via SSH.
* Stop the Corda node(s) running on your cloud instance.

```bash
sudo systemctl stop corda

{{< warning >}}
If this is an HA node, make sure to stop both the hot and cold nodes before proceeding. Any database migration should be performed whilst both nodes are offline.
{{< /warning >}}

* Download the Resources:Download the finance CorDapp and database manager to your VM instance:
    * corda-finance-contracts-4.5.jar
    * corda-finance-workflows-4.5.jar
    * corda-tools-database-manager-4.5.jar

This is required to run some flows to check your connections, and to issue/transfer cash to counterparties. Copy it to
the Corda installation location:

```bash
sudo cp /home/<USER>/corda-finance-*-4.5.jar /opt/corda/cordapps/
```

* Create a symbolic link to the shared database driver folder

```bash
sudo ln -s /opt/corda/drivers /opt/corda/plugins
```


* Execute the database migration. This is required so that the node database has the right schema for finance transactions defined in the installed CorDapp.

```bash
cd /opt/corda
sudo java -jar /home/<USER>/corda-tools-database-manager-4.5.jar --base-directory /opt/corda --execute-migration
```


* Run the following to create a config file for the finance CorDapp:

```bash
echo "issuableCurrencies = [ USD ]" > /opt/corda/cordapps/config/corda-finance-4.5.conf
```


* Restart the Corda node:

```bash
sudo systemctl start corda
```

Your node is now running the Finance Cordapp.

{{< note >}}
You can double-check that the CorDapp is loaded in the log file `/opt/corda/logs/node-<VM-NAME>.log`. This
file will list installed apps at startup. Search for `Loaded CorDapps` in the logs.
{{< /note >}}

* Now download the Node Explorer to your **LOCAL** machine:

```bash
https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-explorer/4.5/corda-tools-explorer-4.5.jar
```

{{< warning >}}
The Enterprise Node Explorer is incompatible with open source versions of Corda and vice versa as they currently
use different serialisation schemes (Kryo vs AMQP).
{{< /warning >}}

* Run the Node Explorer tool on your **LOCAL** machine.

```bash
java -jar corda-tools-explorer-4.5.jar
```

![explorer login](../resources/explorer-login.png "explorer login")



## Connect to the node

To connect to the node you will need:


* The IP address of your node (the public IP of your cloud instance). You can find this in the instance page of your cloud console.
* The port number of the RPC interface to the node, specified in `/opt/corda/node.conf` in the `rpcSettings` section,
(by default this is 10003 on Testnet).
* The username and password of the RPC interface of the node, also in the `node.conf` in the `rpcUsers` section,
(by default the username is `cordazoneservice` on Testnet).

Click on `Connect` to log into the node.


## Check your network identity and counterparties

Once Explorer has logged in to your node over RPC click on the `Network` tab in the side navigation of the Explorer UI:

![explorer network](../resources/explorer-network.png "explorer network")
If your Enterprise node is correctly configured and connected to the Testnet then you should be able to see the identities of
your node, the Testnet notary and the network map listing all the counterparties currently on the network.


## Test issuance transaction

Now we are going to try and issue some cash to a ‘bank’. Click on the `Cash` tab.

![explorer cash issue1](../resources/explorer-cash-issue1.png "explorer cash issue1")
Now click on `New Transaction` and create an issuance to a known counterparty on the network by filling in the form:

![explorer cash issue2](../resources/explorer-cash-issue2.png "explorer cash issue2")
Click `Execute` and the transaction will start.

![explorer cash issue3](../resources/explorer-cash-issue3.png "explorer cash issue3")
Click on the red X to close the notification window and click on `Transactions` tab to see the transaction in progress,
or wait for a success message to be displayed:

![explorer transactions](../resources/explorer-transactions.png "explorer transactions")
Congratulations! You have now successfully installed a CorDapp and executed a transaction on the Corda Testnet.
