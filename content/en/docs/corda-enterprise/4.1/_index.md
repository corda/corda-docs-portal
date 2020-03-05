+++
date = "2020-01-08T09:59:25Z"
title = "Corda Enterprise 4.1"
aliases = [ "/releases/4.1/index.html",]
section_menu = "corda-enterprise-4-1"
version = "4.1"
project = "corda-enterprise"

[menu.versions]
weight = 159

[menu.corda-enterprise-4-1]
+++


# Welcome to Corda !

[Corda](https://www.corda.net/) is an open-source blockchain platform. If you’d like a quick introduction to blockchains and how Corda is different, then watch this short video:

<embed>
<iframe src="https://player.vimeo.com/video/205410473" width="640" height="360" frameborder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen="true"></iframe>


</embed>

Want to see Corda running? Download our demonstration application [DemoBench](https://www.corda.net/downloads/) or
            follow our [quickstart guide](quickstart-index.md).

If you want to start coding on Corda, then familiarise yourself with the [key concepts](key-concepts.md), then read
            our [Hello, World! tutorial](hello-world-introduction.md). For the background behind Corda, read the non-technical
            [platform white paper](_static/corda-platform-whitepaper.pdf) or for more detail, the [technical white paper](_static/corda-technical-whitepaper.pdf).

If you have questions or comments, then get in touch on [Slack](https://slack.corda.net/) or ask a question on
            [Stack Overflow](https://stackoverflow.com/questions/tagged/corda) .

We look forward to seeing what you can do with Corda!


{{< note >}}
You can read this site offline. Either [download the PDF](_static/corda-developer-site.pdf) or download the Corda source code, run `gradle buildDocs` and you will have
                a copy of this site in the `docs/build/html` directory.

{{< /note >}}

* [Release notes for Corda 4.1](release-notes.md)

* [Release notes for Corda 4](release-notes.md#release-notes-for-corda-4)

* [Upgrading apps to Corda 4](app-upgrade-notes.md)

* [Upgrading your node to Corda 4](node-upgrade-notes.md)

* [Corda API](corda-api.md)

* [Cheat sheet](cheat-sheet.md)



Development
* [Quickstart](quickstart-index.md)

* [Key concepts](key-concepts.md)

* [CorDapps](building-a-cordapp-index.md)

* [Tutorials](tutorials-index.md)

* [Tools](tools-index.md)

* [Node internals](node-internals-index.md)

* [Component library](component-library-index.md)

* [Serialization](serialization-index.md)

* [JSON](json.md)

* [Troubleshooting](troubleshooting.md)



Operations
* [Nodes](corda-nodes-index.md)
    * [Node folder structure](node-structure.md)

    * [Node identity](node-naming.md)

    * [Node configuration](corda-configuration-file.md)

    * [Node command-line options](node-commandline.md)

    * [Node administration](node-administration.md)

    * [Deploying a node to a server](deploying-a-node.md)

    * [Node database](node-database.md)

    * [Database access when running H2](node-database-access-h2.md)

    * [Node shell](shell.md)

    * [Interacting with a node](clientrpc.md)

    * [Creating nodes locally](generating-a-node.md)

    * [Running nodes locally](running-a-node.md)


* [Networks](corda-networks-index.md)
    * [What is a compatibility zone?](compatibility-zones.md)

    * [Network certificates](permissioning.md)

    * [The network map](network-map.md)

    * [Cipher suites supported by Corda](cipher-suites.md)

    * [Joining an existing compatibility zone](joining-a-compatibility-zone.md)

    * [Joining Corda Testnet](corda-testnet-intro.md)

    * [Deploying Corda to Testnet](deploy-to-testnet-index.md)

    * [Using the Node Explorer to test a Corda node on Corda Testnet](testnet-explorer-corda.md)

    * [Setting up a dynamic compatibility zone](setting-up-a-dynamic-compatibility-zone.md)

    * [Setting up a notary service](running-a-notary.md)


* [Official Corda Docker Image](docker-image.md)
    * [Running a node connected to a Compatibility Zone in Docker](docker-image.md#running-a-node-connected-to-a-compatibility-zone-in-docker)

    * [Running a node connected to a Bootstrapped Network](docker-image.md#running-a-node-connected-to-a-bootstrapped-network)

    * [Generating configs and certificates](docker-image.md#generating-configs-and-certificates)

    * [Joining TestNet](docker-image.md#joining-testnet)

    * [Joining an existing Compatibility Zone](docker-image.md#joining-an-existing-compatibility-zone)


* [Azure Marketplace](azure-vm.md)
    * [Pre-requisites](azure-vm.md#pre-requisites)

    * [Deploying the Corda Network](azure-vm.md#deploying-the-corda-network)

    * [Using the Yo! CorDapp](azure-vm.md#using-the-yo-cordapp)

    * [Viewing logs](azure-vm.md#viewing-logs)

    * [Next Steps](azure-vm.md#next-steps)


* [AWS Marketplace](aws-vm.md)
    * [Pre-requisites](aws-vm.md#pre-requisites)

    * [Deploying a Corda Network](aws-vm.md#deploying-a-corda-network)

    * [Build and Run a Sample CorDapp](aws-vm.md#build-and-run-a-sample-cordapp)

    * [Next Steps](aws-vm.md#next-steps)


* [Load testing](loadtesting.md)
    * [Configuration of the load testing cluster](loadtesting.md#configuration-of-the-load-testing-cluster)

    * [Running the load tests](loadtesting.md#running-the-load-tests)

    * [Configuration of individual load tests](loadtesting.md#configuration-of-individual-load-tests)

    * [How to write a load test](loadtesting.md#how-to-write-a-load-test)

    * [Stability Test](loadtesting.md#stability-test)


* [Shell extensions for CLI Applications](cli-application-shell-extensions.md)
    * [Installing shell extensions](cli-application-shell-extensions.md#installing-shell-extensions)

    * [Upgrading shell extensions](cli-application-shell-extensions.md#upgrading-shell-extensions)

    * [List of existing CLI applications](cli-application-shell-extensions.md#list-of-existing-cli-applications)




