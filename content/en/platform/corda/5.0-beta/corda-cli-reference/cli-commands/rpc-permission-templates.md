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

* A dedicated role which can create users, roles, permissions and drive all the associations between them.
* A dedicated role with a set of all the necessary permissions to create a virtual node (including CPI upload).
* A dedicated role which allows flows to run on this vNode.

{{< note >}}
These roles and permissions enable certain common operations. The creation of users and associating such users to these roles should be done manually by an admin user.
{{< /note >}}

`UserAdminRole` - Creates roles, permissions, and controls all associations between the user, roles, and permissions. This role is created at cluster bootstrap by the admin user. This role is created via REST call enabling to have complete audit trail of the operation performed.

`VNodeCreatorRole` - Set all the necessary permissions to create a virtual node, including CPI upload and CPI update. Create this role at cluster bootstrapping time.

`CordaDeveloperRole` - Users can do the following:

1. VNode reset
2. Vnode status update

This role should be provisioned at cluster boostrap time and should re-use previously created permissions for other roles.

`FlowExecutorRole` - Once the vNode is created, a new CLI command will permit creation of such role for a given vNode to start new flows and enquire about the status of the running flows.

## Querying Permissions via HTTP RPC

At the moment it is only possible to retrieve a permission if its identifier is known to the caller.
However, there might be cases when a new role is being setup and existing permissions need to be included. It would be helpful to do a search of the permissions available.

{{< note >}}
Being unable to do this creates potentially duplicated permissions.
{{< /note >}}

## Check Permissions When Starting Flows

Currently, Corda checks if a user can execute startFlow RPC operations. No checks are made to whether the user can start a particular flow.

These checks should be performed against the RBAC sub-system even before passing start request to FlowWorker.

## RPC Permission Templates

The draft of a test plan may look like the following:

1. Make sure UserAdminRole, VNodeCreatorRole and CordaDeveloperRole are either available at cluster bootstap time:
"GET <https://localhost:8888/api/v1/role>" or if not (e.g. in case of Combined Worker), they can be created used CLI tools:

`> java -jar corda-cli.jar initial-rbac user-admin -t <https://localhost:8888> -u admin -p admin`
`> java -jar corda-cli.jar initial-rbac vnode-creator -t <https://localhost:8888> -u admin -p admin`
`> java -jar corda-cli.jar initial-rbac corda-developer -t <https://localhost:8888> -u admin -p admin`

2. Use Swagger UI to create user "UserAdmin" and assign "UserAdminRole" to it.

3. Logout as "admin" and login as user "UserAdmin".
4. Use Swagger UI, as "UserAdmin" to create user "vNodeCreator" and assign the "VNodeCreatorRole" to it.
5. Use Swagger UI, as "UserAdmin" to create user" CordaDeveloper" and assign the "CordaDeveloperRole" to it.
6. Build a CPI with some usable flows.
7. Log on as "vNodeCreator" and upload CPI and create a vNode.
8. Create a 'FlowExecutorRole" role for running flows for a vNode using the CLI tool:

`>java -jar corda-cli.jar initial-rbac flow-executor -t <https://localhost:8888> -u UserAdmin -p UserAdmin -v 9B02C806787D`

{{< note >}}
This is done using "UserAdmin" and not as all mighty "admin".
After creation role name should be: "FlowExecutorRole-9B02C806787D"
{{< /note >}}

9. Use Swagger UI, as "UserAdmin" to create user "FlowExecutor" and assign "FlowExecutorRole-9B02C806787D" to it.
10. Using Swagger UI, log on as "FlowExecutor" and run a flow ensuring that it successfully completes with expected result returned. When checking results of the flow make sure that vNode ID: 9B02C806787D is used, the calls will be forbidden for any other vNodes.
11. Execute some negative testing scenarios, e.g.:
• Ensure that "UserAdmin" cannot upload CPIs, create vNodes or run flows.
Ensure that "FlowExecutor" and "vNodeCreator" cannot perform any RBAC operations.
