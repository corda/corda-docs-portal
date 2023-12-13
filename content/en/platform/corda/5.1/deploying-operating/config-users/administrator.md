---
date: '2023-04-07'
version: 'Corda 5.1'
title: "Administrator"
menu:
  corda51:
    parent: corda51-cluster-users
    identifier: corda51-cluster-administrator
    weight: 1000
section_menu: corda51
---
# Administrator

By default, when a {{< tooltip >}}cluster{{< /tooltip >}} starts, a "super admin" {{< tooltip >}}REST user identity{{< /tooltip >}} is created, which has unrestricted access permissions.
This user is created using a special utility that performs a one-time write to the {{< tooltip >}}RBAC{{< /tooltip >}} permissions database.

The "super admin" user can create additional users and assign necessary permissions to them.
These permissions may include, but are not limited to, the ability to create even more users.

The governing principle is that even if a particular user ("minor admin") is assigned a permission to create other users,
it cannot assign more permissions to them than it currently has itself.
In other words, it is not possible to elevate access privileges by creating more user accounts.
