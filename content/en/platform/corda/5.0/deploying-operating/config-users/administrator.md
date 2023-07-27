---
date: '2023-04-24'
version: 'Corda 5.0'
title: "Administrator"
menu:
  corda5:
    parent: corda5-cluster-users
    identifier: corda5-cluster-administrator
    weight: 1000
section_menu: corda5
---
# Administrator
By default, when a cluster starts, a "super admin" REST user is created, which has unrestricted access permissions.
This user is created using a special utility that performs a one-time write to the RBAC permissions database.

The "super admin" user can create additional users and assign necessary permissions to them.
These permissions may include, but are not limited to, the ability to create even more users.

The governing principle is that even if a particular user ("minor admin") is assigned a permission to create other users,
it cannot assign more permissions to them than it currently has itself.
In other words, it is not possible to elevate access privileges by creating more user accounts.
