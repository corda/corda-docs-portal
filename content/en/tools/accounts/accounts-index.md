---
date: '2021-04-24T00:00:00Z'
description: "Documentation for the Corda Accounts Library"
section_menu: tools
menu:
  tools:
    name: Corda Accounts Library
    weight: 200
    identifier: tools-accounts
title: Corda Accounts Library
---

# Corda Accounts Library

In the context of Corda, the Corda Accounts Library allows a Corda node to partition the vault — a collection of state objects — into a number of subsets, where each subset represents an account. In other words, the Corda Accounts Library allows a Corda node operator to split the vault into multiple "logical" sub-vaults. This is advantageous for a couple of reasons:

1. Node operators can reduce costs by hosting multiple entities, as accounts, on one node.
2. Node operators can partition the vault on a per-entity basis.

Accounts are created by host nodes, which are just regular Corda nodes. Hosts can create accounts for a range of purposes, such as customer accounts, balance sheets or P&L accounts, employee accounts, and so on.

The Corda Accounts Library takes the form of a JAR file, which can be dropped into the CorDapps directory. It is optional to use - some nodes will support accounts but others will not. This functionality is intentional, as not all nodes will need to support accounts and the optional nature of accounts reduces the learning curve for new CorDapp developers.

You can access the Corda Accounts Library from the [public repository](https://github.com/corda/accounts).

To learn how to install and use the Corda Accounts Library, check out the [readme](https://github.com/corda/accounts/blob/master/README.md) and [docs](https://github.com/corda/accounts/blob/master/docs.md) repo pages.
