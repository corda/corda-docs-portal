---
date: '2023-08-10'
version: 'Corda 5.1'
title: "Configuring the Network Participants"
menu:
  corda51:
    parent: corda51-develop-get-started
    identifier: corda51-csde-network
    weight: 7000
section_menu: corda51
---
# Configuring the Network Participants
The CSDE is pre-configured to create a Corda cluster with five virtual nodes: Alice, Bob, Charlie, Dave, and a {{< tooltip >}}notary{{< /tooltip >}}.
This configuration can be changed by modifying the `config/static-network-config.json` file.

{{< figure src="static-network-config-file.png" figcaption="CSDE static-network-config.json file in IntelliJ" >}}

As CSDE is primarily for prototyping {{< tooltip >}}CorDapps{{< /tooltip >}}, it uses a static version of a Corda network and so you cannot dynamically add or remove participants. To apply network changes, you must run: `stopCorda`, `startCorda`, and `5-vNodeSetup`.
{{< note >}}
Applying an updated `static-network-config.json` file changes the `ShortHashes` of all nodes.
{{< /note >}}
