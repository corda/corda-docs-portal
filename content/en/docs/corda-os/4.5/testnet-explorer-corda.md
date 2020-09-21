---
date: '2020-09-20T09:59:25Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-testnet-explorer-corda
    parent: corda-os-4-5-deploy-to-testnet-index
    weight: 1080
tags:
- testnet
- explorer
- corda
title: Using the Node Explorer to test a Corda node on Corda Testnet
---


# Using the Node Explorer to test a Corda node on Corda Testnet

This document will explain how to test the installation of a Corda node on Testnet.


## Prerequisites

This guide assumes you have deployed a Corda node to the Corda Testnet.

{{< note >}}
If you need to set up a node on Testnet first please follow the instructions: [Joining Corda Testnet](corda-testnet-intro.md).

{{< /note >}}

## Get the testing tools

To run the tests and make sure your node is connecting correctly to the network you will need to download and install a
couple of resources.


* Log into your Cloud VM via SSH.
* Stop the Corda node(s) running on your cloud instance.

```bash
ps aux | grep corda.jar | awk '{ print $2 }' | xargs sudo kill
```


* Download the finance CorDappIn the terminal on your cloud instance run:

```bash
wget https://software.r3.com/artifactory/corda-releases/net/corda/corda-finance-contracts/4.5/corda-finance-contracts-4.5.jar
wget https://software.r3.com/artifactory/corda-releases/net/corda/corda-finance-workflows/4.5/corda-finance-workflows-4.5.jar
```

This is required to run some flows to check your connections, and to issue/transfer cash to counterparties. Copy it to
the Corda installation location:

```bash
sudo cp /home/<USER>/corda-finance-4.5-corda.jar /opt/corda/cordapps/
```


* Run the following to create a config file for the finance CorDapp:

```bash
echo "issuableCurrencies = [ USD ]" > /opt/corda/cordapps/config/corda-finance-4.5-corda.conf
```


* Restart the Corda node:

```bash
cd /opt/corda
sudo ./run-corda.sh
```

Your node is now running the finance Cordapp.{{< note >}}
You can double-check that the CorDapp is loaded in the log file `/opt/corda/logs/node-<VM-NAME>.log`. This
file will list installed apps at startup. Search for `Loaded CorDapps` in the logs.{{< /note >}}

* Now download the Node Explorer to your **LOCAL** machine:{{< note >}}
Node Explorer is a JavaFX GUI which connects to the node over the RPC interface and allows you to send transactions.{{< /note >}}
Download the Node Explorer from here:

```bash
https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-explorer/4.5-corda/corda-tools-explorer-4.5-corda.jar
```


{{< warning >}}
This Node Explorer is incompatible with the Corda Enterprise distribution and vice versa as they currently
use different serialisation schemes (Kryo vs AMQP).{{< /warning >}}



* Run the Node Explorer tool on your **LOCAL** machine.

```bash
java -jar corda-tools-explorer-4.5-corda.jar
```

![explorer login](/en/images/explorer-login.png "explorer login")



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

![explorer network](/en/images/explorer-network.png "explorer network")
If your Corda node is correctly configured and connected to the Testnet then you should be able to see the identities of
your node, the Testnet notary and the network map listing all the counterparties currently on the network.


## Test issuance transaction

Now we are going to try and issue some cash to a ‘bank’. Click on the `Cash` tab.

![explorer cash issue1](/en/images/explorer-cash-issue1.png "explorer cash issue1")
Now click on `New Transaction` and create an issuance to a known counterparty on the network by filling in the form:

![explorer cash issue2](/en/images/explorer-cash-issue2.png "explorer cash issue2")
Click `Execute` and the transaction will start.

![explorer cash issue3](/en/images/explorer-cash-issue3.png "explorer cash issue3")
Click on the red X to close the notification window and click on `Transactions` tab to see the transaction in progress,
or wait for a success message to be displayed:

![explorer transactions](/en/images/explorer-transactions.png "explorer transactions")
Congratulations! You have now successfully installed a CorDapp and executed a transaction on the Corda Testnet.
