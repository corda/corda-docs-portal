---
date: '2023-04-24'
version: 'Corda 5.0'
title: "Managing Roles and Permissions"
menu:
  corda5:
    parent: corda5-cluster-users
    identifier: corda5-cluster-managing-roles
    weight: 2000
section_menu: corda5
---
# Managing Roles and Permissions
By default, when a cluster starts, the "super admin" REST user is created, which has unrestricted access permissions.
While this account can be used to perform any action, there is room for error if not used carefully.
Role-based access control (RBAC) permission templates enable you to create fine-grained roles for specific actions such as:

* A dedicated role which can create users, roles, and permissions and drive all the associations between them.
* A dedicated role with a set of all the necessary permissions to create a virtual node (including CPI upload).
* A dedicated role which allows flows to run on this virtual node.

{{< note >}}
These roles and permissions enable certain common operations.
The creation of users and associating such users to these roles should be done manually by an admin user.
{{< /note >}}

| <div style="width:160px">Role</div> | Description                                                                                                                                                                                                                                                              |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `UserAdminRole`                     | Creates roles and permissions and controls all associations between the user roles, and permissions. This role is created at cluster bootstrap by the admin user. This role is created via a REST call enabling to have complete audit trail of the operation performed. |
| `VNodeCreatorRole`                  | Sets all the necessary permissions to create a virtual node, including CPI upload and CPI update. Create this role at cluster bootstrapping time.                                                                                                                        |
| `CordaDeveloperRole`                | Enables the use of virtual node reset and virtual node status update. This role should be provisioned at cluster boostrap time and should re-use previously created permissions for other roles.                                                                         |
| `FlowExecutorRole`                  | Permits the creation of a role for a given virtual node to start flows and enquire the status of the running flows once the virtual node is created.                                                                                                                     |

For information about creating these roles maually, see the [Manual Bootstrapping section]({{< relref "../deployment/deploying/manual-bootstrapping.md">}}).

## Querying Permissions via REST

To retrieve permissions matching certain query criteria, use the [get_permission](https://docs.r3.com/en/platform/corda/5.0-beta/rest-api/C5_OpenAPI.html#tag/RBAC-Permission-API/operation/get_permission) API call.

## Checking Permissions When Starting Flows

Currently, Corda checks if a user can execute `startFlow` REST operations. No checks are made to whether the user can start a particular flow. These checks should be performed against the RBAC sub-system before passing the start request to a FlowWorker.
