---
aliases:
- /head/comm-upgrade-guide.html
- /HEAD/comm-upgrade-guide.html
- /comm-upgrade-guide.html
date: '2024-06-05'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-comm-upgrade-guide
    parent: corda-community-4-12-upgrading
    weight: 15
tags:
- upgrade
- guide
title: Corda Open Source Edition 4.11 to 4.12 upgrade guide
---

# Corda Open Source Edition 4.11 to 4.12 upgrade guide

This upgrade guide outlines the steps for migrating your Corda 4.11 node to version 4.12 while maintaining backwards compatibility with earlier Corda 4.x versions.

{{< note >}}
The steps from this guide only work for direct upgrades from Corda 4.11 to 4.12. If you have any nodes on versions 4.10 and below, you must upgrade them to 4.11 first. To do that, consult the relevant release upgrade documentation.
{{< /note >}}

### Background

Corda 4.12 has been upgraded to use Kotlin 1.9.20 and Java 17. When designing Corda 4.12, we had to take into consideration the issue of having a backchain of transactions that had been verified using Kotlin 1.2 and Java 8 by earlier versions of Corda.

If a Corda 4.12 node were to be part of a network of mixed Corda 4.x versions, a Corda 4.12 node would not be able to verify a contract compiled using Kotlin 1.2. Similarly, a Corda node running an earlier version of Kotlin would not be able to verify a new Corda 4.12 contract compiled using Kotlin 1.9.20.

### The solution

To address verification issues, both earlier versions of Corda 4.x and Corda 4.12 had to have a way of verifying the correct contract attachment, depending on the Corda version. This is where the external verifier, a component of Corda 4.12, comes in.

The external verifier is a process started by Corda 4.12, running Kotlin 1.2 (with Java 17). This enables Corda 4.12 to run independently of Java 8. Whenever Corda 4.12 detects an old contract version, it externally verifies this contract within the external verifier process.

When upgrading to Corda 4.12, the old contract CorDapp JAR is preserved and relocated to a new directory named `legacy-contracts`. This directory is essential in a mixed network (4.12 nodes and pre-4.12 nodes) as it provides legacy contracts for Corda 4.12 nodes to maintain backward compatibility, as required by the transaction builder.

#### Corda 4.11 vs Corda 4.12

The following diagram outlines the core differences between Corda 4.11 and Corda 4.12, providing a high-level overview of how the external verifier works with the legacy contract code to verify both Corda 4.11 and Corda 4.12 transactions.

The different colors in the diagram indicate the elements used in each version. While Corda 4.11 remains unchanged, some elements from Corda 4.11 are carried over to Corda 4.12. When the 4.12 node starts, it loads the 4.11 Contract CorDapp, enabling the Corda 4.12 node to send transactions to the Corda 4.11 node. Both the 4.11 contract code (pink) and the 4.12 contract code (green) are included in the transactions. The 4.11 node then discards the new 4.12 contract code.

The Corda 4.11 transaction verifier has also been preserved in an external process to allow Corda 4.11 transactions to be verified by Corda 4.12.

{{< figure alt="Corda 4.12 vs Corda 4.11" width=75% height=75% src="resources/corda412vs411.png" figcaption="Corda 4.12 vs Corda 4.11">}}

## Upgrade scenarios

This section describes three possible upgrade paths to a network operating on Corda 4.12. In these scenarios a network is a collection of Corda nodes that are all running the same CorDapp.

All scenarios involving the upgrade of existing node versions from a previous version of Corda 4.x to Corda 4.12 assume the existence of 4.11 (or earlier) transactions in the node’s backchain.

### Upgrading selected network nodes to 4.12

In this scenario, you have a mixed network where only selected nodes are upgraded to Corda 4.12, while others remain on previous versions of Corda 4.x. This scenario requires you to perform the following actions:
1. Upgrade any existing CorDapps to run on Java 17 and Kotlin 1.9.20.
2. Keep a copy of the old CorDapp contract JAR file in the new `legacy-contracts` folder placed inside all upgraded 4.12 nodes.
3. If your contracts depend on third-party dependencies or JARs from the `drivers` folder, then you must place these in the new `legacy-jars` folder located inside all upgraded 4.12 nodes.

Any future Corda 4.12 nodes added to the network will also require the `legacy-contracts` folder, unless all nodes have been updated by that time. In the latter case, you are adding new Corda 4.12 nodes to a non-mixed network and this requirement is no longer necessary.

Additionally, if contracts depend on third-party dependencies or JARs in the `drivers` folder, then the populated `legacy-jars` folder must exist on all 4.12 nodes.


### Upgrading all network nodes to 4.12

In this scenario, you are creating a non-mixed network composed solely of nodes operating on Corda 4.12. Transactions occurring within this newly-upgraded network only have the 4.12 contract component group and therefore, you do not need the `legacy-contracts` folder. However, it is still important that you keep a copy of the old contract JAR for reference.

If any new Corda 4.12 nodes are added to this network in the future, a problem arises wherein new nodes won’t trust old contract attachments. For example, this happens if a new transaction contains a backchain of old Corda 4.x transactions. For this reason, you must upload the old contract JAR via RPC to the new node, ensuring it trusts the old contract version.

The `legacy-jars` folder is also required if contracts use third-party libraries or depend on JARs in the `drivers` directory.

### Adding 4.12 nodes to a new network

This scenario is the simplest, as it does not require any complex update procedures. In this scenario, all CorDapps are developed for Java 17 and Kotlin 1.9.20, and the process for adding new nodes is the same as setting up a new network of any previous Corda version.

## Upgrade prerequisites

This guide assumes that you have a working Corda network with one or more Corda 4.11 nodes running. If you have custom CorDapps running on your nodes, this guide also describes the required upgrade steps for CorDapps from version 4.11 to 4.12.

To complete the upgrade from Corda 4.11 to Corda 4.12, you need the following components:
* A Corda 4.12 JAR (obtained from R3).
* Access to, and the ability to edit the source code for any existing custom CorDapps running in the nodes to be upgraded from 4.11 to 4.12.

## Upgrade outline

To upgrade your Corda node from version 4.11 to 4.12, you must perform the following steps:

1. Upgrade any custom CorDapps running on the Corda 4.11 node to work with Java 17 and Kotlin 1.9.20. See [Upgrade 4.11 CorDapps]({{< relref "#upgrade-411-cordapps" >}}).
2. Validate all existing transactions (per node) to ensure that their backchain works with 4.12.
3. Preserve old CorDapp contracts in a new folder called `legacy-contracts`. See [Add the legacy contracts folder to mixed networks]({{< relref "#add-the-legacy-contracts-folder-to-mixed-networks" >}}).
   {{< note >}}
   This step is for mixed networks only. It is not required if you plan on upgrading all nodes on your network to 4.12.
   {{< /note >}}
4. If your contracts use third-party dependencies or rely on JARs in the `drivers` directory, then create a new folder `legacy-jars` and insert the third-party dependencies and required JARs from the `drivers` folder into the `legacy-jars` folder.

### Upgrade 4.11 CorDapps

You must update all custom CorDapps being upgraded that are running on Corda 4.11 nodes so they use Java 17 and Kotlin 1.9.20. For steps on updating Cordapps, see [Upgrading CorDapps to newer platform versions]({{< relref "app-upgrade-notes.md" >}}).

#### Flow versioning
You must annotate any flow that initiates other flows with the `@InitiatingFlow` annotation, which is defined as:

```
annotation class InitiatingFlow(val version: Int = 1)
```

The version property, which defaults to 1, specifies the flow’s version. You must increment this integer value whenever a flow release includes changes that are not backwards compatible. However, in this case, the flow version must stay the same to ensure backward compatibility with the flows running on previous Corda versions. However, even though in this case you are not incrementing the flow version, you must always increment the new 4.12 contract version; see [Contract versioning]({{< relref "#contract-versioning" >}}).

#### Contract versioning

When Corda 4.12 starts, it loads the CorDapp contract JAR. For version 4.12, the contract version must be higher than the contract version in the `legacy-contracts` JAR file. Therefore, you must increment the contract version by at least one.

#### CorDapp minimum platform version

The new CorDapp should inherit the same minimum platform version as Corda 4.12, which is 140. This is not 14, to account for minor updates to Corda 4.11.

#### CorDapp signing

Upon startup, a node verifies the signing key for the CorDapps it uses, preventing unwanted code from being executed. In Corda 4.12, nodes having both new and legacy versions of a contract CorDapp must have the same signing keys, otherwise the node will fail to start.

### Add the legacy contracts folder to mixed networks

When operating a network with nodes running different versions of Corda, you must store the old CorDapp contract JAR files in the Corda 4.12 node directory (see [Legacy contracts]({{< relref "#legacy-contracts" >}})). This step is not required if all nodes in your network are being upgraded to Corda 4.12.

However, in both scenarios, you must keep a copy of the old CorDapp contracts JAR file. This file may be required if new Corda 4.12 nodes are introduced into a network containing nodes that have previously been upgraded. For steps describing adding a new node to an existing network of Corda 4.12 containing previously upgraded nodes, see [Adding new 4.12 nodes]({{< relref "#adding-new-412-nodes" >}}).

#### Legacy contracts

Corda 4.12 introduces the concept of *legacy contracts*. A new `legacy-contracts` folder is required when operating a network where not all nodes are running Corda 4.12.

{{< note >}}
If you are not using a mixed network, you do not need the `legacy-contracts` folder.
{{< /note >}}

This folder contains old CorDapp contract JAR files required by the external verifier process to verify old contract attachments in new transactions. The following is an example folder structure of how to set up the node folder to include the `legacy-contracts` folder.

Before upgrade:
```
.
├── certificates
├── corda-4.11.jar
├── cordapps
│   ├── config
│   ├── corda-finance-contracts-4.11.jar
│   └── corda-finance-workflows-4.11.jar
├── drivers
└── node.conf
After upgrade
```

After upgrade:
```
.
├── certificates
├── corda-4.12.jar
├── cordapps
│   ├── config
│   ├── corda-finance-contracts-4.12.jar
│   └── corda-finance-workflows-4.12.jar
├── drivers
├── legacy-contracts
│   └── corda-finance-contracts-4.11.jar
├── legacy-jars
│   └── third-party-dependency.jar
└── node.conf
```

To ensure compatibility, you must keep the legacy contracts. When a node operating on a prior version of Corda 4.x wants to transact with a Corda 4.12 node, the 4.12 node identifies an old contract version attached to the transaction. To verify this old contract, Corda 4.12 initiates the external verifier process, which starts a new external process running Kotlin 1.2. Making use of the external verifier process is the way in which a 4.12 node can verify transactions from 4.11 or earlier nodes.

Similarly, when a 4.12 node creates a transaction, it adds a 4.12 contract into a new component group of the transaction, reserving the existing component group for the 4.11 contract. Consequently, when a 4.11 contract gets attached to the transaction, it ends up with two sets of contract attachments (JARs): the legacy one and the new 4.12 contract. If this transaction is received by a node not running Corda 4.12, the node lacks awareness of the new component group. It disregards the 4.12 contract and proceeds to verify the legacy contract instead, which is then stored in the database.

When creating a transaction, it is the responsibility of the transaction builder to make sure the transaction has all required JARs attached to it. For example, if a contract JAR depends on a class in `xyz.jar` then that JAR should also be attached to the transaction for verification.

If the above is not the case, then Corda tries to assist here. For example, if a class is not found when verifying a transaction, Corda will search the `cordapps` folder for other JARs containing the required class, and then attach the relevant JAR. This would be the case for a 4.12 contract JAR. When attaching the legacy contract to the transaction, Corda will look for a suitable class from the `legacy-contracts` folder.  That is to say, it would look for `xyz.jar` (the JDK8 version) from the `legacy-contracts` folder. Therefore, you must ensure the JDK8 version of `xyz.jar` is in the `legacy-contracts` directory.

### Add the `legacy-jars` folder, if required

Pre-4.12 transactions are verified in an external verifier process when encountered. By default, this process does not include all third-party libraries shipped with Corda 4.11 or earlier, nor does it have the contents of the `drivers` directory on its classpath. If your contracts in ledger attachments depend on such third-party libraries or items previously in the `drivers` directory of Corda 4.11 or earlier, you can place the required JAR files in a directory named `legacy-jars` within the node directory. Any JARs in this directory will be added to the classpath of the external verifier. The TVU will help you discover and verify resolution of such issues.

## Starting 4.12 nodes

1. Run the database migration scripts. See [Use run-migration-scripts]({{< relref "deploying-a-node.md#use-run-migration-scripts" >}}).
2. Start your node in the usual way:

   ```
   java -jar corda-4.12.jar -f node.conf
   ```

## Adding new 4.12 nodes

If you want to add another Corda 4.12 node into your network post-upgrade, the specific steps vary depending on the state of your network.

### Adding new 4.12 nodes to a mixed network

If you are operating a mixed network, then the process for adding a new Corda 4.12 node is relatively straightforward.

1. Set up the node folder structure same as other Corda 4.12 nodes.
2. Add the `legacy-contracts` folder and associated files to the node folder.
3. Add the `legacy-jars` folder if required.

   ```
   .
   ├── certificates
   ├── corda-4.12.jar
   ├── cordapps
   │   ├── config
   │   ├── corda-finance-contracts-4.12.jar
   │   └── corda-finance-workflows-4.12.jar
   ├── drivers
   ├── legacy-contracts
   │   └── corda-finance-contracts-4.11.jar
   ├── legacy-jars
   │   └── third-party-dependency.jar
   └── node.conf
   ```

3. Register the node to the network and proceed to operate it as normal.

### Adding new 4.12 nodes to a non-mixed network

Perform the following steps if you are adding a new Corda 4.12 node to a network that is only running Corda 4.12 nodes, but also contains older Corda 4.x transactions.

{{< note >}}
In this scenario, you still require a copy of the old CorDapp contract JAR file.
{{< /note >}}

1. Set up the node folder structure without the `legacy-contracts` folder.
2. Add the `legacy-jars` folder if required.

   ```
   .
   ├── certificates
   ├── corda-4.12.jar
   ├── cordapps
   │   ├── config
   │   ├── corda-finance-contracts-4.12.jar
   │   └── corda-finance-workflows-4.12.jar
   ├── legacy-jars
   │   └── third-party-dependency.jar
   ├── drivers
   └── node.conf
   ```

3. Register and then start the node.

4. Access the Corda node either via RPC client or the standalone shell and upload the old CorDapp contract JAR as an attachment to the node.
   For more information on uploading attachments, see [Working with attachments]({{< relref "get-started/tutorials/supplementary-tutorials/tutorial-attachments.md" >}}).

## Additional release information

In Corda 4.12, the Corda node explorer is no longer included in the release pack. Should you require it, the Corda 4.11 node explorer remains compatible with Corda 4.12 and should be used for Corda 4.12 nodes.

Corda 4.11 versions of the node and flow management plugins are also compatible with Corda 4.12 and you should use them for Corda 4.12 nodes.

## Troubleshooting

### Add-opens

After upgrading Corda to Java 17, CorDapps no longer have access to internal Java classes due to the strong encapsulation module system introduced in Java 11. If your CorDapp still requires access to any internal Java classes, you can open the package by either:

* Starting the JAR with a command line option:
   ```
   java -jar corda.jar -f node.conf --add-opens $MODULE/$PACKAGE=$REFLECTING_MODULE
   ```

* Or by declaring it in the CorDapp manifest file:
   ```
   Add-Opens: <module>/<package>
   ```
