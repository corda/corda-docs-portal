---
date: '2020-09-10'
title: "Debugging CorDapps"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    weight: 9100
section_menu: corda-5-dev-preview
---

To debug your CorDapp in a local network using IntelliJ:

1. Ensure the node you want to debug has the `debug: true` property set in the network definition `.yaml` file.

2. Run the `corda-cli network status` command:

   `corda-cli network status -n <network name>`

3. In the command's output, find and copy the debug port number of the node that you want to test.

4. At the top of the IntelliJ window, click the **Select/Run Debug Configuration** drop-down menu. Click **Edit Configurations...**.

5. In the **Run/Debug Configurations** window, click the plus (+) symbol and select **Remote JVM Debug**.

6. Provide a name for your **Remote JVM Debug** and paste the port number in the **Port** window. Click **OK**.

7. Attach the debug to the node and specify the flow's break points.
