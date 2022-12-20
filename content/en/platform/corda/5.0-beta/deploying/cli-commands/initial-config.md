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
*************************************
Usage: corda initial-config create-db-config [-a] [-d=<description>]
       -e=<passphrase> -j=<jdbcUrl> [--jdbcPoolMaxSize=<jdbcPoolMaxSize>]
       [-l=<location>] -n=<connectionName> -p=<password> -s=<salt> -u=<username>


  -d, --description=<description>
                            Detailed info on the database connection
  -e, --passphrase=<passphrase>
                            Passphrase for the encrypting secrets service
  -j, --jdbcURL=<jdbcUrl>   The JDBC URL for the connection. Required.
      --jdbcPoolMaxSize=<jdbcPoolMaxSize>
                            The maximum size for the JDBC connection pool.
                              Defaults to 10
  -l, --location=<location> location to write the sql output to
  -n, --name=<connectionName>
                            Name of the database connection. Required.
  -p, --password=<password> Password name for the database connection. Required.
  -s, --salt=<salt>         Salt for the encrypting secrets service
  -u, --user=<username>     User name for the database connection. Required.


| Argument       | Description                                   |
| -------------- | --------------------------------------------- |
| -a, --isAdmin | Specifies if this is an admin (DDL) connection. The default value is false. |



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

   The `<SALT>` and `<PASSPHRASE>` are used to encrypt the credentials in the database. These must match the values specified in the Corda deployment configuration for the DB worker:

## create-crypto-config