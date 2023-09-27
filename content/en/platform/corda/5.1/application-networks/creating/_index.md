---
date: '2023-08-10'
title: "Creating Application Networks"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-networks-create
    parent: corda51-networks
    weight: 3000
section_menu: corda51
---
# Creating Application Networks
This section describes how to set up a dynamic network. The network requires a running {{< tooltip >}}MGM{{< /tooltip >}} that all {{< tooltip >}}members{{< /tooltip >}} must register with before they can transact among the group. This section also describes how to onboard a new member as a {{< tooltip >}}notary{{< /tooltip >}} service representative. 

The main sections describe a standard configuration but you can learn more about using mutual {{< tooltip >}}TLS{{< /tooltip >}} or session certificates in the [Optional Configurations]({{< relref"./optional/_index.md">}}) section.

This section contains the following:
{{< childpages >}}