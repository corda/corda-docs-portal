---
aliases:
- /releases/4.1/azure-vm-explore.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-azure-vm-explore
    parent: corda-enterprise-4-1-corda-networks-testnet-decommission
    weight: 1010
tags:
- azure
- vm
- explore
title: Deploying Corda to Corda Testnet from an Azure Cloud Platform VM
---


# Deploying Corda to Corda Testnet from an Azure Cloud Platform VM


This document will describe how to set up a virtual machine on the Azure Cloud Platform to deploy your pre-configured
Corda node and automatically connnect to Testnet. A self-service download link can be obtained from
[https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet).


## Pre-requisites


* Ensure you have a registered Microsoft Azure account which can create virtual machines.


## Deploy Corda node

Browse to [https://portal.azure.com](https://portal.azure.com) and log in with your Microsoft account.


### STEP 1: Create a Resource Group

Click on the “Resource groups” link in the side nav in the Azure Portal and then click “Add”:

![azure rg](/en/images/azure-rg.png "azure rg")
Fill in the form and click “Create”:

![azure rg 2](/en/images/azure-rg-2.png "azure rg 2")

### STEP 2: Launch the VM

At the top of the left sidenav click on the button with the green cross “Create a resource”.

In this example we are going to use an Ubuntu server so select the latest Ubuntu Server option:

![azure select ubuntu](/en/images/azure-select-ubuntu.png "azure select ubuntu")
Fill in the form:


* Add a username (to log into the VM) and choose and enter a password
* Choose the resource group we created earlier from the “Use existing” dropdown
* Select a cloud region geographically near to your location to host your VM

Click on “OK”:

![azure vm form](/en/images/azure-vm-form.png "azure vm form")
Choose a size (“D4S_V3 Standard” is recommended if available) and click “Select”:

![azure instance type](/en/images/azure-instance-type.png "azure instance type")
Click on “Public IP address” to open the “Settings” panel

![azure vm settings](/en/images/azure-vm-settings.png "azure vm settings")
Set the IP address to “Static” under “Assignment” and click “OK”:

{{< note >}}
This is so the IP address for your node does not change frequently in the global network map.

{{< /note >}}
![azure set static ip](/en/images/azure-set-static-ip.png "azure set static ip")
Next toggle “Network Security Group” to advanced and click on “Network security group (firewall)”:

![azure nsg](/en/images/azure-nsg.png "azure nsg")
Add the following inbound rules for ports 8080 (webserver), and 10002-10003 for the P2P and RPC ports used by the Corda
node respectively:

```bash
Destination port ranges: 10002, Priority: 1041  Name: Port_10002
Destination port ranges: 10003, Priority: 1042  Name: Port_10003
Destination port ranges: 8080, Priority: 1043  Name: Port_8080
Destination port ranges: 22, Priority: 1044  Name: Port_22
```

{{< note >}}
The priority has to be unique number in the range 900 (highest) and 4096 (lowest) priority. Make sure each
rule has a unique priority or there will be a validation failure and error message.

{{< /note >}}
![azure nsg 2](/en/images/azure-nsg-2.png "azure nsg 2")
Click “OK” and “OK” again on the “Settings” panel:

![azure settings ok](/en/images/azure-settings-ok.png "azure settings ok")
Click “Create” and wait a few minutes for your instance to be provisioned and start running:

![azure create vm](/en/images/azure-create-vm.png "azure create vm")

### STEP 3: Connect to your VM and set up the environment

Once your instance is running click on the “Connect” button and copy the ssh command:

![azure ssh](/en/images/azure-ssh.png "azure ssh")
Enter the ssh command into your terminal. At the prompt, type “yes” to continue connecting and then enter the password
you configured earlier to log into the remote VM:

![azure shell](/en/images/azure-shell.png "azure shell")

### STEP 4: Download and set up your Corda node

Now that your Azure environment is configured you can switch to the
[Testnet web application](https://marketplace.r3.com/network/testnet/platform) and click “Copy” to get a one-time installation
script.

{{< note >}}
If you have not already set up your account on Testnet, please visit [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet) and sign
up.

{{< /note >}}
{{< note >}}
You can generate as many Testnet identites as you like by refreshing this page to generate a new one-time
link.

{{< /note >}}
![testnet platform](/en/images/testnet-platform.png "testnet platform")
In the terminal of your cloud instance, paste the command you just copied to install and run your Corda node:

```bash
sudo ONE_TIME_DOWNLOAD_KEY=YOUR_UNIQUE_DOWNLOAD_KEY_HERE bash -c "$(curl -L https://marketplace.r3.com/network/testnet/api/user/node/install.sh)"
```


{{< warning >}}
This command will execute the install script as ROOT on your cloud instance. You may wish to examine the
script prior to executing it on your machine.

{{< /warning >}}


You can follow the progress of the installation by typing the following command in your terminal:

```bash
tail -f /opt/corda/logs/node-<VM-NAME>.log
```

Once the node has booted up, you can navigate to the external web address of the instance on port 8080:

```bash
http://<PUBLIC-IP-ADDRESS>:8080/
```

If everything is working, you should see the following:

![installed cordapps](/en/images/installed-cordapps.png "installed cordapps")

## Testing your deployment

To test that your deployment is working correctly, follow the instructions in [Using the Node Explorer to test a Corda node on Corda Testnet](testnet-explorer-corda.md) to set up
the Finance CorDapp and issue cash to a counterparty.

This will also demonstrate how to install a custom CorDapp.
