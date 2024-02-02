---
description: "List of initial-rbac commands for the Corda 5.2 CLI. You can use these commands to manually create RBAC roles."  
date: '2023-10-06'
menu:
  corda52:
    identifier: corda52-cordacli-initial-rbac
    weight: 2500
    parent: corda52-cli-reference
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

This section lists the Corda CLI `initial-rbac` arguments. You can use these commands to manually create {{< tooltip >}}RBAC{{< /tooltip >}} roles, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md#rbac-roles" >}}) section. For more information about these default roles, see [Managing Roles and Permissions]({{< relref "../../deploying-operating/config-users/managing-roles.md">}}).

## user-admin

The `user-admin` command creates the `UserAdminRole` role.

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

The `vnode-creator` command creates the `VNodeCreatorRole` role.
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

## flow-executor

The `flow-executor` command creates the `FlowExecutorRole` role.

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

The `all-cluster-roles` command creates the `UserAdminRole` and `VNodeCreatorRole` roles.

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