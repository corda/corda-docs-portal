---
date: '2020-09-08T12:00:00Z'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    weight: 9000
section_menu: corda-5-dev-preview
title: Deploying a CorDapp
expiryDate: '2022-09-28'
---

To deploy to a Corda 5 Developer Preview network, you must use a Corda package bundle file (`.cpb` file) which contains
both workflows and contracts packages.

{{< note >}}

Nodes in the Corda 5 Developer Preview can only support a single sandbox, running a single CorDapp at any one time.

{{< /note >}}

1. Apply the CorDapp CPK Gradle plugin to a Gradle project and generate the `.cpk` files. See [CorDapp CPK Gradle plugin](../../../../../en/platform/corda/5.0-dev-preview-1/packaging/gradle-plugin/overview.md).

2. Assemble your `.cpk` files into a single `.cpb` file using the CorDapp Builder CLI. See [CorDapp Builder CLI](../../../../../en/platform/corda/5.0-dev-preview-1/packaging/cordapp-builder.md).

3. To deploy your CorDapp, perform one of the following steps:

   * Deploy your CorDapp to all nodes in the running network using this command:

      `corda-cli pkg install -n <network-name> <cpb-file-location>`

      For example:

      `corda-cli pkg install -n network-example-name  */build/libs/*.cpb`

   * Deploy your CorDapp to only one of the nodes in the network using this command:

      `corda-cli pkg install -n <network-name> -m <node-name> <cpb-file-location>`

      For example:

      `corda-cli pkg install -n network-example-name -m bob */build/libs/*.cpb`


    **Step result:** The `pkg install` command copies the `.cpb` file to the node's CorDapps directory and restarts the node container.

   {{< note >}}

   You cannot install multiple `.cpb` files or use both `.cpb` and `.cpk` files simultaneously. This is because:

   * If there are both `.cpb` and `.cpk` files in the CorDapps directory, the node will pick only the `.cpb` and ignore the `.cpk` files.
   * If there are multiple `.cpb` files, the node will not start. You can only have a single `.cpb` in the CorDapps directory.
   * If there are only `.cpk` files in the CorDapps directory, the node will automatically assemble them into a single `.cpb` file.

   {{< /note >}}

4. Verify the status using the `corda-cli network status -n <network-name>` command.

   **Step result:** The **Deployed apps** section appears in the command's output.

   {{< note >}}
   Restarting the node retains the deployed CorDapps. To replace the CorDapps, run the `deploy` command with a new version of the `.cpb`. To remove a deployed CorDapp, remove the `.cpb` from the container and restart the node.

   Use the `corda-cli pgk remove` command to uninstall a previously installed `.cpb` or `.cpk`.

   {{< /note >}}
