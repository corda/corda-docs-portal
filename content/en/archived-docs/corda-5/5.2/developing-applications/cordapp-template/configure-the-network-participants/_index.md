---
date: '2023-11-01'
description: Learn how to configure the network participants using the CorDapp template.
title: "Configuring the Network Participants"
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-runtime-plugin-network
    weight: 7000

---
# Configuring the Network Participants

The CorDapp template is pre-configured to create a Corda cluster with five virtual nodes: Alice, Bob, Charlie, Dave, and a {{< tooltip >}}notary{{< /tooltip >}}.
This configuration can be changed by modifying the `config/static-network-config.json` file.

{{< figure src="static-network-config-file.png" figcaption="static-network-config.json file in IntelliJ" >}}

As the CorDapp template is primarily for prototyping {{< tooltip >}}CorDapps{{< /tooltip >}}, it uses a static version of a Corda network and so you cannot dynamically add or remove participants. To apply network changes, you must run: `stopCorda`, `startCorda`, and `vNodesSetup`.

{{< note >}}
Applying an updated `static-network-config.json` file changes the `ShortHashes` of all nodes.
{{< /note >}}
