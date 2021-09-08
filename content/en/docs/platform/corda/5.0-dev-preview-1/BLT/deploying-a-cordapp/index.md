---
date: '2021-09-06'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-network
    weight: 100
project: corda-5
section_menu: corda-5-dev-preview
title: Deploying a CorDapp
---

To deploy anything to a Corda 5 Developer Preview network, you must use a Corda package bundle file (a `.cpb` file) which contains both workflows and contracts packages.

1. Apply the CorDapp CPK Gradle plugin to a Gradle project and generate the `.cpk` files. See [CorDapp CPK Gradle plugin](XXX).

2. Assemble your `.cpk` files into a single `.cpb` file using the CorDapp Builder CLI. See [CorDapp Builder CLI](XXX).

3. To deploy your CorDapp, perform one of the following steps:

   * To deploy your CorDapp to all nodes in the running network, use the following command:

      `corda-cli pkg install -n <network-name> <cpb-file-location>`

      For example:

      `corda-cli pkg install -n network-example-name  */build/libs/*.cpb`

   * To deploy your CorDapp to only one of the nodes in the network, use:

      `corda-cli pkg install -n <network-name> -m <node-name> <cpb-file-location>`

      For example:

      `corda-cli pkg install -n network-example-name -m bob */build/libs/*.cpb`


    **Step result:** The `pkg install` command copies the `.cpb` file to the node's CorDapps directory and restarts the node container.

   {{< note >}}

   You cannot install multiple `.cpb` files or use both `.cpb` and `.cpk` files simultaneously:

   * If there are both `.cpb` and `.cpk` files in the CorDapps directory, the node will pick only the `.cpb` and ignore the `.cpk` files.
   * If there are multiple `.cpb` files, the node will not start. You can only have a single `.cpb` in the CorDapps directory.
   * If there are only `.cpk` files in the CorDapps directory, the node will automatically assemble them into a single `.cpb` file.

   {{< /note >}}


4. Verify the status using the `corda-cli network status -n <network-name>` command.

   **Step result:** The **Deployed apps** section appears in the command's output.

   {{< note >}}
   Restarting the node retains the deployed apps. To replace the apps, run the deploy with a new version of the `.cpb`. To remove a deployed app, remove the `.cpb` from the container and restart the node.

   Use the `corda-cli pgk remove` command to uninstall a previously installed `.cpb` or `.cpk`.

   {{< /note >}}
