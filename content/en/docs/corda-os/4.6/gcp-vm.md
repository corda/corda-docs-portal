---
aliases:
- /head/gcp-vm.html
- /HEAD/gcp-vm.html
- /gcp-vm.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-gcp-vm
    parent: corda-os-4-6-deploy-to-testnet-index
    weight: 1030
tags:
- gcp
- vm
title: Deploying Corda to Corda Testnet from a Google Cloud Platform VM
---


# Deploying Corda to Corda Testnet from a Google Cloud Platform VM


This document explains how to deploy a Corda node to Google Cloud Platform that can connect directly to the Corda Testnet. A self service download link can be obtained from [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet). This document will describe how to set up a virtual machine on the Google Cloud Platform (GCP) to deploy your pre-configured Corda node and automatically connnect to Testnet.


## Pre-requisites


* Ensure you have a registered Google Cloud Platform account with
billing enabled ([https://cloud.google.com/billing/docs/how-to/manage-billing-account](https://cloud.google.com/billing/docs/how-to/manage-billing-account)) which can create virtual machines under your subscription(s) and you are logged on to the GCP console: [https://console.cloud.google.com](https://console.cloud.google.com).


## Deploy Corda node

Browse to [https://console.cloud.google.com](https://console.cloud.google.com) and log in with your
Google credentials.

**STEP 1: Create a GCP Project**

In the project drop down click on the plus icon to create a new
project to house your Corda resources.

{{< figure alt="consolegcp" zoom="/en/images/consolegcp.png" >}}
{{< figure alt="console2" zoom="/en/images/console2.png" >}}
{{< figure alt="newprojectgcp" zoom="/en/images/newprojectgcp.png" >}}
Enter a project name and click Create.

**STEP 2: Launch the VM**

In the left hand side nav click on Compute Engine.

{{< figure alt="gcpcompute" zoom="/en/images/gcpcompute.png" >}}
Click on Create Instance.

{{< figure alt="consolegcpcreatevm" zoom="/en/images/consolegcpcreatevm.png" >}}
Fill in the form with the desired VM specs:

Recommended minimum 4vCPU with 15GB memory and 40GB Persistent disk.
Ubuntu 16.04 LTS.

Allow full API access.

Dont worry about firewall settings as you will configure those later.

{{< figure alt="gcpconsolevmsettings" zoom="/en/images/gcpconsolevmsettings.png" >}}
Click Create and wait a few sections for your instance to provision
and start running.

**STEP 3: Connect to your VM and set up the environment**

Once your instance is running click on the SSH button to launch a
cloud SSH terminal in a new window.

{{< figure alt="gcpconsolelaunchssh" zoom="/en/images/gcpconsolelaunchssh.png" >}}
{{< figure alt="gcpshell" zoom="/en/images/gcpshell.png" >}}
Run the following to configure the firewall to allow Corda traffic

```bash
gcloud compute firewall-rules create nodetonode --allow tcp:10002
gcloud compute firewall-rules create nodetorpc --allow tcp:10003
gcloud compute firewall-rules create webserver --allow tcp:8080
```

Promote the ephemeral IP address associated with this
instance to a static IP address.

First check the region and select the one you are using from the list:

```bash
gcloud compute regions list
```

Find your external IP:

```bash
gcloud compute addresses list
```

Run this command with the ephemeral IP address as the argument to
the –addresses flag and the region:

```bash
gcloud compute addresses create corda-node --addresses 35.204.53.61 --region europe-west4
```

**STEP 4: Download and set up your Corda node**

Now your GCP environment is configured you can switch to the Testnet
web application and click on the copy to clipboard button to get a one
time installation script.

{{< note >}}
If you have not already set up your account on Testnet then please visit [https://marketplace.r3.com/network/testnet](https://marketplace.r3.com/network/testnet) and sign up.

{{< /note >}}
{{< figure alt="testnet platform" zoom="/en/images/testnet-platform.png" >}}
You can generate as many Testnet identites as you like by refreshing
this page to generate a new one time link.

In the terminal of your cloud instance paste the command you just copied to install and run
your unique Corda instance:

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

To test your deployment is working correctly follow the instructions in [Using the Node Explorer to test a Corda node on Corda Testnet](testnet-explorer-corda.md) to set up the Finance CorDapp and issue cash to a counterparty.

This will also demonstrate how to install a custom CorDapp.

