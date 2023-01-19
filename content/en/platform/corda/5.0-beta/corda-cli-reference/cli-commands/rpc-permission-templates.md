---
date: '2023-01-10'
menu:
  corda-5-beta:
    identifier: corda-5-beta-rpc-permissions-templates
    weight: 6000
    parent: corda-5-cli-reference
section_menu: corda-5-beta
title: "RPC Permission Templates"
---


By default, when a cluster starts there is a single "admin" account auto-created which can do everything. While this account can be used to perform any action, there is room for error if not used carefully. RPC permission templates enable you to create fine-grained roles for specific actions such as:

* A dedicated role which can create users, roles, and permissions and drive all the associations between them.
* A dedicated role with a set of all the necessary permissions to create a virtual node (including CPI upload).
* A dedicated role which allows flows to run on this virtual node.

{{< note >}}
These roles and permissions enable certain common operations. The creation of users and associating such users to these roles should be done manually by an admin user.
{{< /note >}}

| Role   | Description |
| ----------- | ----------- |
| `UserAdminRole` | Creates roles and permissions and controls all associations between the user roles, and permissions. This role is created at cluster bootstrap by the admin user. This role is created via a REST call enabling to have complete audit trail of the operation performed.       |
| `VNodeCreatorRole` | Sets all the necessary permissions to create a virtual node, including CPI upload and CPI update. Create this role at cluster bootstrapping time.|
| `CordaDeveloperRole` | Enables the use of virtual node reset and virtual node status update. This role should be provisioned at cluster boostrap time and should re-use previously created permissions for other roles.|
| `FlowExecutorRole`|  Permits the creation of a role for a given virtual node to start flows and enquire the status of the running flows once the virtual node is created.|

## Querying Permissions via HTTP RPC

At the moment, it is only possible to retrieve a permission if its identifier is known to the caller.
However, there might be cases when a new role is being set up and existing permissions need to be included.

## Checking Permissions When Starting Flows

Currently, Corda checks if a user can execute startFlow RPC operations. No checks are made to whether the user can start a particular flow.

These checks should be performed against the RBAC sub-system before passing the start request to a FlowWorker.
