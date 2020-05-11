---
aliases:
- /releases/4.4/network/azure-template-guide.html
- /docs/corda-enterprise/head/network/azure-template-guide.html
- /docs/corda-enterprise/network/azure-template-guide.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-networks-testnet
tags:
- azure
- template
- guide
title: Using Azure Resource Manager Templates to deploy a Corda Enterprise node
weight: 2
---


# Using Azure Resource Manager Templates to deploy a Corda Enterprise node

This document will explain how to deploy a Corda Enterprise node to the Azure cloud using the Azure Resource Manager templates via the Azure Marketplace.


## Prerequisites

You will need a Microsoft Azure account which can create new resource groups and resources within that group.


## Find Corda Enterprise on Azure Marketplace

Go to [https://azuremarketplace.microsoft.com/en-us/](https://azuremarketplace.microsoft.com/en-us/) and search for `corda enterprise` and select the `Corda Enterprise Single Node` option:

![azure template search](../resources/azure-template-search.png "azure template search")
Click on `GET IT NOW`:

![azure template marketplace](../resources/azure-template-marketplace.png "azure template marketplace")
Click on `Continue` to agree  to the terms:

![azure template agree](../resources/azure-template-agree.png "azure template agree")
This will take you to the Azure Cloud Portal. Log in to the Portal if you are not already. It should redirect to the Corda Enterprise template automatically:

![azure template portal](../resources/azure-template-portal.png "azure template portal")
Click on `Create` to enter the parameters for the deployment.

![azure template basics](../resources/azure-template-basics.png "azure template basics")
Enter the VM base name, an SSH public key or password to connect to the resources over SSH, an Azure region to host the deployment and create a new resource group to house the deployment. Click `OK`.

![azure template vm](../resources/azure-template-vm.png "azure template vm")
Next select the virtual machine specification. The default here is suitable for Corda Enterprise so its fine to click `OK`. Feel free to select a different specification of machine and storage if you have special requirements.

![azure template settings](../resources/azure-template-settings.png "azure template settings")
Next configure the Corda node settings. Currently the only version available with the template is the current release of Corda Enterprise. We may add more version options in the future.

Enter the city and country that you wish to be associated with your Corda node.

{{< note >}}
This doesn’t need to be the same as the Azure region you host your node in. It should represent the main location of your business operations.

{{< /note >}}
You will need to obtain a `one-time-download-key` in order to set up the template. This will allow the template scripts to connect to, and provision the node to the Corda Testnet.

You can register with Testnet and obtain the `ONE-TIME-DOWNLOAD-KEY` at [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet) or see the Testnet documentation: [Joining Corda Testnet](corda-testnet-intro.md).

Finally you can select your database sizing in the `Corda Data Tier Performance` (the default is fine for typical usage).

Click `OK`.

![azure template summary](../resources/azure-template-summary.png "azure template summary")
Wait for the validation checks to pass and check the settings. Click `OK`.

![azure template create](../resources/azure-template-create.png "azure template create")
Check the Terms of Use and if everything is OK click `Create`. Azure will now run the template and start to provision the node to your chosen region. This could take some time.

You will be redirected to your `Dashbord` where the deployment will appear if the deployment completes without errors.

You can now log in to your resource by selecting the virtual machine in the resource group and clicking on `Connect`. Log in with SSH.


## Testing the deployment

You can test the deployment by following the instructions in [Using the Node Explorer to test a Corda Enterprise node on Corda Testnet](testnet-explorer.md).
