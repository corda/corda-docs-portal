---
date: '2023-11-07'
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cordacli-vnode
    weight: 6000
    parent: corda51-cli-reference
section_menu: corda51
title: "vnode"
---
# vnode
This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `vnode` sub-commands. You can use these commands to reset or upgrade virtual nodes. For more information see, [Upgrading from 5.0]({{< relref "../../deploying-operating/deployment/upgrading/_index.md" >}}).

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument           | Description                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| reset              | Uploads and overwrites a previous CPI; see [reset](#reset).                                                                                                                        |
| platform-migration | Generates the required SQL commands to migrate the database schema of virtual nodes from one version of Corda Platform to the next; see [platform-migration](#platform-migration). |

## reset

The following table lists the `reset` sub-commands and arguments:

| Argument         | Description                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| -c, \-\-cpi      | The path to the CPI file used to overwrite the virtual node.                                                |
| -k, \-\-insecure | Allows insecure server connections with SSL. The default value is false.                                    |
| -p, \-\-password | The REST API password.                                                                                      |
| -r, \-\-resync   | The short hash holding IDs of the virtual nodes to reset.                                           |
| -t, \-\-target   | The URL of the REST API.                                                                                    |
| -u, \-\-user     | The REST API user.                                                                                          |
| -w, \-\-wait     | Polls for the result.                                                                                       |
| -y, \-\-yield    | Duration in seconds to wait for the REST connection to become available. Defaults to 10 seconds if missing. |

## platform-migration

The following table lists the `platform-migration` sub-commands and arguments:

| Argument                | Description                                                                                                                                                                        |
| ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -i, \-\-input-filename  | The path to a file containing the list of short hash holding IDs of the virtual nodes to migrate. The file must only contain one ID per line. The default value is `./holdingIds`. |
| \-\-jdbc-url            | The JDBC URL for the connection. Read access is required for Liquibase tracking tables to determine the current version of the platform schemas of each virtual node.              |
| -o, \-\-output-filename | The path to the generated SQL file. The default value is `./vnodes.sql`.                                                                                                          |
| -p, \-\-password        | The database password.                                                                                                                                                             |
| -u, \-\-user            | The database user.                                                                                                                                                                 |

{{< tabs name="">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh vnode platform-migration --jdbc-url=jdbc:postgresql://host.docker.internal:5432/cordacluster -u postgres -i /sql_updates/holdingIds -o /sql_updates/vnodes.sql
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd vnode platform-migration --jdbc-url=jdbc:postgresql://host.docker.internal:5432/cordacluster -u postgres -i /sql_updates/holdingIds -o /sql_updates/vnodes.sql
```
{{% /tab %}}
{{< /tabs >}}

For more information about upgrading from Corda 5.0 to Corda 5.1, see [Upgrading from 5.0]({{< relref "../../deploying-operating/deployment/upgrading/_index.md" >}}).
