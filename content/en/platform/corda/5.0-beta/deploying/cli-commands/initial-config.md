---
date: '2022-12-20'
menu:
  corda-5-beta:
    identifier: corda-5-beta-cordacli-initial-config
    weight: 3000
    parent: corda-5-beta-cordacli-deploy-commands
section_menu: corda-5-beta
title: "initial-config"
---

This section lists the Corda CLI `initial-config` arguments. You can use these commands to manually perform various setup actions, as described in the [Manual Bootstrapping Tutorial](deployment-tutorials/manual.html).

## create-user-config 

The `create-user-config` command creates the SQL script to add the RBAC configuration for an initial admin user. 

| Argument       | Description                                   |
| -------------- | --------------------------------------------- |
| -l, --location | The path to write the generated SQL files to. |
| -p, --password | The password of the initial admin user.       |
| -u, --user     | The user name of the initial admin user.      |

{{< tabs name="DDL-user">}}
{{% tab name="Linux" %}}
```sh
corda-cli.sh initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
```
{{% /tab %}}
{{% tab name="macOS" %}}
```sh
corda-cli.sh initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
```
{{% /tab %}}
{{% tab name="Windows" %}}
```shell
corda-cli.cmd initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
```
{{% /tab %}}
{{< /tabs >}}

## create-db-config

The `create-db-config` command creates the SQL statements to insert the connection manager configuration for the database.

| <div style="width:290px">Argument</div>           | Description                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| -a, --isAdmin     | Specifies if this is an admin (DDL) connection. The default value is false.                                                                      |
| -d, --description | Detailed informoation about the database connection.                                                                                             |
| -e, --passphrase  | The passphrase for the encrypting secrets service.  This must match the value specified in the Corda deployment configuration for the DB worker. |
| -j, --jdbcURL     | The JDBC URL for the connection. This value is required.                                                                                         |
| --jdbcPoolMaxSize | The maximum size of the JDBC connection pool. The default value is 10.                                                                           |
| -l, --location    | The path to write the generated SQL files to.                                                                                                    |
| -n, --name        | The name of the database connection. Required.                                                                                                   |
| -p, --password    | The password name for the database connection. Required.                                                                                         |
| -s, --salt        | Salt for the encrypting secrets service. This must match the value specified in the Corda deployment configuration for the DB worker.            |
| -u, --user        | The user name for the database connection. Required.                                                                                             |

{{< tabs name="RBAC">}}
{{% tab name="Linux" %}}
```sh
corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
  --name corda-rbac --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \
  --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{% tab name="macOS" %}}
```sh
corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
  --name corda-rbac --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \
  --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{% tab name="Windows" %}}
```shell
corda-cli.cmd initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> `
  --name corda-rbac --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> `
  --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{< /tabs >}}

## create-crypto-config

The `create-crypto-config` command creates the SQL statements to insert the initial crypto configuration for the database. This operation must be performed after the cluster database is initialised but before the cluster is started.

| Argument         | Description                                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| -l, --location   | The path to write the generated SQL files to.                                                                                                    |
| -p, --passphrase | The passphrase for the encrypting secrets service.  This must match the value specified in the Corda deployment configuration for the DB worker. |
| -s, --salt       | Salt for the encrypting secrets service. This must match the value specified in the Corda deployment configuration for the DB worker.            |
| -wp, --wrapping-passphrase   | The passphrase for the SOFT HSM root wrapping key.                                                                                                   |
| -ws, --wrapping-salt   | Salt for the SOFT HSM root wrapping key.                                                                                                  |

{{< tabs name="DDL-crypto-config">}}
{{% tab name="Linux" %}}
```sh
corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{% tab name="macOS" %}}
```sh
corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{% tab name="Windows" %}}
```shell
corda-cli.cmd initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{< /tabs >}}