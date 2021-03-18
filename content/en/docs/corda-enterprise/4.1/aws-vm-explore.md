---
aliases:
- /releases/4.1/aws-vm-explore.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-aws-vm-explore
    parent: corda-enterprise-4-1-corda-networks-testnet-decommission
    weight: 1020
tags:
- aws
- vm
- explore
title: Deploying Corda to Corda Testnet from an AWS Cloud Platform VM
---


# Deploying Corda to Corda Testnet from an AWS Cloud Platform VM


This document explains how to deploy a Corda node to AWS that can connect directly to the Corda Testnet.
A self service download link can be obtained from [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet). This
document will describe how to set up a virtual machine on the AWS
Cloud Platform to deploy your pre-configured Corda node and automatically connnect
to Testnet.


## Pre-requisites


* Ensure you have a registered Amazon AWS account which can create virtual machines and you are logged on to the AWS console: [https://console.aws.amazon.com](https://console.aws.amazon.com).


## Deploy Corda node

Browse to [https://console.aws.amazon.com](https://console.aws.amazon.com) and log in with your AWS account.

**STEP 1: Launch a new virtual machine**

Click on Launch a virtual machine with EC2.

![aws launch](/en/images/aws-launch.png "aws launch")
In the quick start wizard scroll down and select the most recent Ubuntu machine image as the Amazon Machine Image (AMI).

![aws select ubuntu](/en/images/aws_select_ubuntu.png "aws select ubuntu")
Select the instance type (for example t2.xlarge).

![aws instance type](/en/images/aws-instance-type.png "aws instance type")
Configure a couple of other settings before we review and launch

Under the storage tab (Step 4) increase the storage to 40GB:

![aws storage](/en/images/aws-storage.png "aws storage")
Configure the security group (Step 6) to open the firewall ports which Corda uses.

![aws firewall](/en/images/aws-firewall.png "aws firewall")
Add a firewall rule for port range 10002-10003 and allow connection from Anywhere. Add another rule for the webserver on port 8080.

Click on the Review and Launch button then if everything looks ok click Launch.

You will be prompted to set up keys to securely access the VM remotely over ssh. Select “Create a new key pair” from the drop down and enter a name for the key file. Click download to get the keys and keep them safe on your local machine.

{{< note >}}
These keys are just for connecting to your VM and are separate from the keys Corda will use to sign transactions. These keys will be generated as part of the download bundle.

{{< /note >}}
![aws keys](/en/images/aws-keys.png "aws keys")
Click “Launch Instances”.

Click on the link to go to the Instances pages in the AWS console where after a few minutes you will be able to see your instance running.

![aws instances](/en/images/aws-instances.png "aws instances")
**STEP 2: Set up static IP address**

On AWS a permanent IP address is called an Elastic IP. Click on the
“Elastic IP” link in the navigation panel on the left hand side of the console and then click on “Allocate new address”:

![aws elastic](/en/images/aws-elastic.png "aws elastic")
Follow the form then once the address is allocated click on “Actions”
then “Associate address”:

![aws elastic actions](/en/images/aws-elastic-actions.png "aws elastic actions")
Then select the instance you created for your Corda node to attach the
IP address to.

**STEP 3: Connect to your VM and set up the environment**

In the instances console click on “Connect” and follow the instructions to connect to your instance using ssh.

![aws instances connect](/en/images/aws-instances-connect.png "aws instances connect")
![aws connect](/en/images/aws-connect.png "aws connect")
**STEP 4: Download and set up your Corda node**

Now your AWS environment is configured you can switch back to the Testnet
web application and click on the copy to clipboard button to get a one
time installation script.

{{< note >}}
If you have not already set up your account on Testnet then please visit [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet) and sign up.

{{< /note >}}
![testnet platform](/en/images/testnet-platform.png "testnet platform")
You can generate as many Testnet identites as you like by refreshing
this page to generate a new one time link.

In the terminal of your cloud instance paste the command you just copied to install and run
your unique Corda instance on that instance:

```bash
sudo ONE_TIME_DOWNLOAD_KEY=YOUR_UNIQUE_DOWNLOAD_KEY_HERE bash -c "$(curl -L https://marketplace.r3.com/network/testnet/api/user/node/install.sh)"
```


{{< warning >}}
This command will execute the install script as ROOT on your cloud instance. You may wish to examine the script prior to executing it on your machine.

{{< /warning >}}


You can follow the progress of the installation by typing the following command in your terminal:

```bash
tail -f /opt/corda/logs/node-<VM-NAME>.log
```

Once the node has booted up you can navigate to the external web address of the instance on port 8080. If everything is working you should see the following:

![installed cordapps](/en/images/installed-cordapps.png "installed cordapps")

## Testing your deployment

To test your deployment is working correctly follow the instructions in [Using the Node Explorer to test a Corda node on Corda Testnet](testnet-explorer-corda.md) to set up the Finance CorDapp and issue cash to a counterparty.

This will also demonstrate how to install a custom CorDapp.
