---
title: "Deploying Corda to Corda Testnet from an AWS Cloud Platform VM"
date: 2020-01-08T09:59:25Z
---


# Deploying Corda to Corda Testnet from an AWS Cloud Platform VM

{{< toc >}}
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

{{< img src="resources/aws-launch.png" alt="aws launch" >}}

In the quick start wizard scroll down and select the most recent Ubuntu machine image as the Amazon Machine Image (AMI).

{{< img src="resources/aws_select_ubuntu.png" alt="aws select ubuntu" >}}

Select the instance type (for example t2.xlarge).

{{< img src="resources/aws-instance-type.png" alt="aws instance type" >}}

Configure a couple of other settings before we review and launch

Under the storage tab (Step 4) increase the storage to 40GB:

{{< img src="resources/aws-storage.png" alt="aws storage" >}}

Configure the security group (Step 6) to open the firewall ports which Corda uses.

{{< img src="resources/aws-firewall.png" alt="aws firewall" >}}

Add a firewall rule for port range 10002-10003 and allow connection from Anywhere. Add another rule for the webserver on port 8080.

Click on the Review and Launch button then if everything looks ok click Launch.

You will be prompted to set up keys to securely access the VM remotely over ssh. Select “Create a new key pair” from the drop down and enter a name for the key file. Click download to get the keys and keep them safe on your local machine.


{{< note >}}
These keys are just for connecting to your VM and are separate from the keys Corda will use to sign transactions. These keys will be generated as part of the download bundle.


{{< /note >}}
{{< img src="resources/aws-keys.png" alt="aws keys" >}}

Click “Launch Instances”.

Click on the link to go to the Instances pages in the AWS console where after a few minutes you will be able to see your instance running.

{{< img src="resources/aws-instances.png" alt="aws instances" >}}

**STEP 2: Set up static IP address**

On AWS a permanent IP address is called an Elastic IP. Click on the
                “Elastic IP” link in the navigation panel on the left hand side of the console and then click on “Allocate new address”:

{{< img src="resources/aws-elastic.png" alt="aws elastic" >}}

Follow the form then once the address is allocated click on “Actions”
                then “Associate address”:

{{< img src="resources/aws-elastic-actions.png" alt="aws elastic actions" >}}

Then select the instance you created for your Corda node to attach the
                IP address to.

**STEP 3: Connect to your VM and set up the environment**

In the instances console click on “Connect” and follow the instructions to connect to your instance using ssh.

{{< img src="resources/aws-instances-connect.png" alt="aws instances connect" >}}

{{< img src="resources/aws-connect.png" alt="aws connect" >}}

**STEP 4: Download and set up your Corda node**

Now your AWS environment is configured you can switch back to the Testnet
                web application and click on the copy to clipboard button to get a one
                time installation script.


{{< note >}}
If you have not already set up your account on Testnet then please visit [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet) and sign up.


{{< /note >}}
{{< img src="resources/testnet-platform.png" alt="testnet platform" >}}

You can generate as many Testnet identites as you like by refreshing
                this page to generate a new one time link.

In the terminal of your cloud instance paste the command you just copied to install and run
                your unique Corda instance on that instance:

```bash
sudo ONE_TIME_DOWNLOAD_KEY=YOUR_UNIQUE_DOWNLOAD_KEY_HERE bash -c "$(curl -L https://onboarder.prod.ws.r3.com/api/user/node/TESTNET/install.sh)"
```

{{< warning >}}
This command will execute the install script as ROOT on your cloud instance. You may wish to examine the script prior to executing it on your machine.


{{< /warning >}}
You can follow the progress of the installation by typing the following command in your terminal:

```bash
tail -f /opt/corda/logs/node-<VM-NAME>.log
```

## Testing your deployment
To test your deployment is working correctly follow the instructions in [Using the Node Explorer to test a Corda node on Corda Testnet]({{< relref "testnet-explorer-corda" >}}) to set up the Finance CorDapp and issue cash to a counterparty.

This will also demonstrate how to install a custom CorDapp.


