---
date: '2021-04-24T00:00:00Z'
description: "Documentation for the Corda Business Network membership extension; this allows you to create and manage business networks"
section_menu: tools
menu:
  tools:
    name: Business Network membership extension
    weight: 300
    identifier: tools-bne
title: Business Network Membership extension
---

# The Corda Business Network membership extension

The Business Network membership extension allows you to create and manage business networks - as a node operator, this means you can define and create a logical network based on a set of common CorDapps as well as a shared business context.

Corda nodes outside of your business network are not aware of its members. The network can be split into subgroups or membership lists which allows for further privacy (members of a group only know about those in their group).

In a business network, there is at least one authorized member. This member has sufficient permissions to execute management operations over the network and its members.

Read the full documentation about the [extension](../../platform/corda/{{< latest-c4-version >}}/community/business-network-membership.md).
