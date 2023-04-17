---
date: '2023-04-14'
title: "Permissions"
menu:
corda-5-beta:
identifier: corda-5-beta-permissions
parent: corda-5-beta-developing-and-operating
weight: 1000
section_menu: corda-5-beta
---

Corda 5 implements role-based access control (RBAC) permission system, also known as role-based security, as a mechanism to restrict system access.
It entails configuring permissions and privileges to grant authorized users access.

By default, when a cluster starts, a "super admin" REST user is created, which has unrestricted access permissions.
This user is created using a special utility that performs a one-time write to the RBAC permissions database.

The "super admin" user can create additional users and assign necessary permissions to them.
These permissions may include, but are not limited to, the ability to create even more users.

The governing principle is that even if a particular user ("minor admin") is assigned a permission to create other users,
it cannot assign more permissions to them than it currently has itself.
In other words, it is not possible to elevate access privileges by creating more user accounts.
