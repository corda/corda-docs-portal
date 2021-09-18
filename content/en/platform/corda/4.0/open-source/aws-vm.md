---
aliases:
- /releases/release-V4.0/aws-vm.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-aws-vm
    parent: corda-os-4-0-operations
    weight: 200
tags:
- aws
- vm
title: AWS Marketplace
---


# AWS Marketplace

To help you design, build and test applications on Corda, called CorDapps, a Corda network AMI can be deployed from the [AWS Marketplace](https://aws.amazon.com/marketplace/pp/B077PG9SP5). Instructions on running Corda nodes can be found [here](https://docs.corda.net/deploying-a-node.html).

This Corda network offering builds a pre-configured network of Corda nodes as Ubuntu virtual machines (VM). The network consists of a Notary node and three Corda nodes using version 1 of Corda. The following guide will also show you how to load one of four [Corda Sample apps](https://www.corda.net/samples) which demonstrates the basic principles of Corda. When you are ready to go further with developing on Corda and start making contributions to the project head over to the [Corda.net](https://www.corda.net/).


## Pre-requisites


* Ensure you have a registered AWS account which can create virtual machines under your subscription(s) and you are logged on to the [AWS portal](https://console.aws.amazon.com)
* It is recommended you generate a private-public SSH key pair (see [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2/))


## Deploying a Corda Network

Browse to the [AWS Marketplace](https://aws.amazon.com/marketplace) and search for Corda.

Follow the instructions to deploy the AMI to an instance of EC2 which is in a region near to your location.


## Build and Run a Sample CorDapp

Once the instance is running ssh into the instance using your keypair

```shell
cd ~/dev
```

There are 4 sample apps available by default

```shell
ubuntu@ip-xxx-xxx-xxx-xxx:~/dev$ ls -la
total 24
drwxrwxr-x  6 ubuntu ubuntu 4096 Nov 13 21:48 .
drwxr-xr-x  8 ubuntu ubuntu 4096 Nov 21 16:34 ..
drwxrwxr-x 11 ubuntu ubuntu 4096 Oct 31 19:02 cordapp-example
drwxrwxr-x  9 ubuntu ubuntu 4096 Nov 13 21:48 obligation-cordapp
drwxrwxr-x 11 ubuntu ubuntu 4096 Nov 13 21:48 oracle-example
drwxrwxr-x  8 ubuntu ubuntu 4096 Nov 13 21:48 yo-cordapp
```

cd into the Corda sample you would like to run. For example:

```shell
cd cordapp-example/
```

Follow instructions for the specific sample at [https://www.corda.net/samples](https://www.corda.net/samples) to build and run the Corda sample
For example: with cordapp-example (IOU app) the following commands would be run:

```shell
./gradlew deployNodes
./kotlin-source/build/nodes/runnodes
```

Then start the Corda webserver

```shell
find ~/dev/cordapp-example/kotlin-source/ -name corda-webserver.jar -execdir sh -c 'java -jar {} &' \;
```

You can now interact with your running CorDapp. See the instructions [here](https://docs.corda.net/tutorial-cordapp.html#via-http).


## Next Steps

Now you have built a Corda network and used a basic Corda Cordapp do go and visit the [dedicated Corda website](https://www.corda.net)

Additional support is available on [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) and the [Corda Slack channel](http://cordaledger.slack.com/).

You can build and run any other [Corda samples](https://www.corda.net/samples) or your own custom CorDapp here.

Or to join the growing Corda community and get straight into the Corda open source codebase, head over to the [Github Corda repo](https://www.github.com/corda)
