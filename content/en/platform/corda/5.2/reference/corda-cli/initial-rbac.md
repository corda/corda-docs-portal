---
description: "List of initial-rbac commands for the Corda 5.1 CLI. You can use these commands to manually create RBAC roles."  
date: '2023-10-06'
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-cordacli-initial-rbac
    weight: 2500
    parent: corda52-cli-reference
section_menu: corda52
title: "initial-rbac"
---

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

# initial-rbac
This section lists the Corda CLI `initial-rbac` arguments. You can use these commands to manually create {{< tooltip >}}RBAC{{< /tooltip >}} roles, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#rbac-roles" >}}) section.

## user-admin

The `user-admin` command creates a `UserAdminRole` role, which permits the following:

* Create and delete users
* Create and delete permissions
* Create and delete roles
* Assign and un-assign roles to users
* Assign and un-assign permissions to roles

{{< snippet initial-rbac.md >}}

{{< tabs >}}
 {{% tab name="Bash" %}}
 ```sh
corda-cli.sh initial-rbac user-admin --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd initial-rbac user-admin --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{< /tabs >}}

## vnode-creator

The `vnode-creator` command creates a `VNodeCreatorRole` role, which permits the following:
* Uploading CPIs
* Creating virtual nodes
* Updating virtual nodes

{{< snippet initial-rbac.md >}}

{{< tabs >}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh initial-rbac vnode-creator --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd initial-rbac vnode-creator --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{< /tabs >}}

## corda-developer

The `corda-developer` command creates a `CordaDeveloperRole` role, which permits the following:

* Reset virtual nodes
* Sync virtual node vaults
* Change the state of virtual nodes

{{< snippet initial-rbac.md >}}

{{< tabs >}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh initial-rbac corda-developer --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd initial-rbac corda-developer --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{< /tabs >}}

## flow-executor

The `flow-executor` command creates a `FlowExecutorRole` role, which permits the following for a specified virtual node:

* Start any flow
* Enquire about the status of running flows

| Argument                  | Description                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------- |
| -k, \-\-insecure          | Specifies if insecure server connections with SSL are permitted. The default value is `false`.      |
| -p, \-\-password          | The password for the user.                                                                          |
| -pv, \-\-protocol-version | The minimum protocol version. The default value is 1.                                               |
| -t, \-\-target            | The target address of the REST API Endpoint. For example, `https://host:port`.                      |
| -u, \-\-user              | The username.                                                                                       |
| -v, \-\-v-node-id         | The short hash identifier of the virtual node that the permissions apply to.                        |
| -y, \-\-yield             | The duration in seconds to wait for a REST connection to become available. The default value is 10. |

{{< tabs >}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh initial-rbac flow-executor --v-node-id 253501665E9D --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd initial-rbac flow-executor --v-node-id 253501665E9D --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{< /tabs >}}

## all-cluster-roles

The `all-cluster-roles` command creates all of the cluster-scoped roles: [CordaDeveloperRole](#corda-developer), [UserAdminRole](#user-admin), [VNodeCreatorRole](#vnode-creator).

{{< snippet initial-rbac.md >}}

{{< tabs >}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh initial-rbac all-cluster-roles --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd initial-rbac all-cluster-roles --yield 300 --user <INITIAL-USERNAME> --password <INITIAL-PASSWORD> --target <API-ENDPOINT>
```
{{% /tab %}}
{{< /tabs >}}