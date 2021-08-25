---
date: '2021-08-24'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-network
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
title: Create a membership group
---

In the Corda 5 Developer Preview, you can experiment with the new membership group functionality by bootstrapping nodes into a private network (membership group).

You can use the bootstrapped membership group to:
*Do
*Do
*do

## Prerequisites

Before you can create a bootstrapped membership group, you must:
1.  [Install the Corda CLI (command line interface) tool](link to CLI docs).
2.  [Create multiple nodes](link to node docs).

## Changes from Corda 4

If you're familiar with Corda 4, you'll notice that:
* `NodeInfo` files have been replaced with `MemberInfo` files.
* References to `NodeInfo` have been replaced with references to `MemberInfo` in flow service, RPC, and Corda Docker files, the network bootstrapper, and the network map.
* `Nodeinfo` definitions have been replaced with a `MemberInfoConstants` file.
* The membership group service has been updated to contain references to `MemberInfo`.

