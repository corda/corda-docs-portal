---
description: "Learn how to use RBAC permission templates to create fine-grained roles for specific actions."
date: '2023-04-07'
title: "Managing Roles and Permissions"
menu:
  corda53:
    parent: corda53-cluster-users
    identifier: corda53-cluster-managing-roles
    weight: 2000
---
# Managing Roles and Permissions

By default, when a cluster starts, the "super admin" REST user identity is created, which has unrestricted access permissions.
This user is created using a special utility that performs a one-time write to the RBAC permissions database.
This "super admin" user can create additional users and assign necessary permissions to them.
These permissions may include, but are not limited to, the ability to create even more users.
A user with permission to create other users cannot assign more permissions other users than it currently has itself.

RBAC permission templates enable you to create fine-grained roles for specific actions such as:

* A dedicated role which can create users, roles, and permissions and drive all the associations between them.
* A dedicated role with a set of all the necessary permissions to create and onboard a {{< tooltip >}}virtual node{{< /tooltip >}}, perform [Bring Your Own Database]({{< relref "../vnodes/bring-your-own-db.md" >}}) operations and {{< tooltip >}}CPI{{< /tooltip >}} upgrade.
* A dedicated role which allows flows to run on this virtual node.

{{< note >}}
These roles and permissions enable certain common operations.
The creation of users and associating such users to these roles should be performed manually by an admin user.
{{< /note >}}

## Default Roles

The following table lists the roles created by default by [RBAC bootstrapping as part of deploying Corda]({{< relref "../deployment/deploying/_index.md#rbac" >}}). For information about creating roles manually, see the [Manual Bootstrapping section]({{< relref "../deployment/deploying/manual-bootstrapping.md">}}).

| <div style="width:160px">Role</div> | Description                                                                                                                                                                                       |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UserAdminRole`                     | Permits the following:<li>Create and delete users<li>Create and delete permissions<li>Create and delete roles<li>Change the password of other users<li>Assign and un-assign roles to users<li>Assign and un-assign permissions to roles |
| `VNodeCreatorRole`                  | Permits the following:<li>Uploading CPIs<li>Upgrading CPIs<li>Creating virtual nodes<li>Updating virtual nodes<li>Bring Your Own Database operations<li>Uploading certificates<li>Assign soft HSM<li>Member registration<li>Generate key pair<li>Check flow status<li>Setup network  |
| `FlowExecutorRole`                  | Permits the following for a specified virtual node:<li>Start any flow<li>Enquire about the status of running flows      |
