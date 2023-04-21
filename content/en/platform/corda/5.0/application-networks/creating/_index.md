---
date: '2023-04-18'
title: "Creating Application Networks"
project: corda
version: 'Corda 5.0'
menu:
  corda-5:
    identifier: corda-5-app-networks-create
    parent: corda-5-app-networks
    weight: 3000
section_menu: corda-5
---
This section describes how to create a dynamic network. The network requires a running {{< tooltip >}}MGM{{< definition term="MGM" >}}{{< /tooltip >}} that all members must register with before they can transact among the group. This section also describes how to onboard a new member as a {{< tooltip >}}notary{{< definition term="Notary" >}}{{< /tooltip >}} service representative. 

The main sections describe a standard configuration but you can learn more about using mutual TLS or session certificates in the [Optional Configurations]({{< relref"./optional/_index.md">}}) section.