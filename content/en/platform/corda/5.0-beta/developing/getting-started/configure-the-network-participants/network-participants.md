---
date: '2022-09-20'
title: "Configuring the Network Participants"
menu:
  corda-5-beta:
    parent: corda-5-beta-start
    identifier: corda-5-beta-csde-network
    weight: 7000
section_menu: corda-5-beta
---
The CSDE is pre-configured to create a Corda cluster with three virtual nodes: Alice, Bob, and Charlie.
This configuration can be changed by modifying the `config/dev-net.json` file.

{{< figure src="dev-net-file.png" figcaption="CSDE dev-net.json file in IntelliJ" >}}

For example, to add Dave to the network, modify the `dev-net.json` file as follows:

{{< figure src="modified-dev-net-file.png" figcaption="Modified CSDE dev-net.json file in IntelliJ" >}}

However, as CSDE is primarily for prototyping CorDapps, it uses a static version of a Corda network and so you cannot dynamically add or remove participants. To apply network changes, you must run: `stopCorda`, `startCorda`, and `deployCordapp`.
{{< note >}}
Applying an updated `dev-net.json` file changes the `ShortHashes` of all nodes.
{{< /note >}}
