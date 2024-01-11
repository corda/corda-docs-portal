---
description: "Learn how to create an application network, that includes a a running MGM that all members must register with before they can transact among the group."
date: '2023-04-07'
title: "Creating Application Networks"
project: corda
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-networks-create
    parent: corda52-networks
    weight: 3000
section_menu: corda52
---
# Creating Application Networks

This section describes how to set up a dynamic network. The network requires a running {{< tooltip >}}MGM{{< /tooltip >}} that all {{< tooltip >}}members{{< /tooltip >}} must register with before they can transact among the group. This section also describes how to onboard a new member as a {{< tooltip >}}notary{{< /tooltip >}} service representative.

The main sections describe a standard configuration but you can learn more about using mutual {{< tooltip >}}TLS{{< /tooltip >}} or session certificates in the [Optional Configurations]({{< relref"./optional/_index.md">}}) section.

This section contains the following:
{{< childpages >}}
