---
date: '2022-09-20'
version: 'Corda 5.0'
title: "Configuring the Network Participants"
menu:
  corda5:
    parent: corda5-develop-get-started
    identifier: corda5-csde-network
    weight: 7000
section_menu: corda5
---
The CSDE is pre-configured to create a Corda cluster with five virtual nodes: Alice, Bob, Charlie, Dave, and a notary.
This configuration can be changed by modifying the `config/static-network-config.json` file.

{{< figure src="static-network-config-file.png" figcaption="CSDE static-network-config.json file in IntelliJ" >}}

As CSDE is primarily for prototyping CorDapps, it uses a static version of a Corda network and so you cannot dynamically add or remove participants. To apply network changes, you must run: `stopCorda`, `startCorda`, and `5-vNodeSetup`.
{{< note >}}
Applying an updated `static-network-config.json` file changes the `ShortHashes` of all nodes.
{{< /note >}}
