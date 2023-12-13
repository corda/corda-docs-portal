---
date: '2022-12-20'
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-cordacli-database
    weight: 1000
    parent: corda51-cli-reference
section_menu: corda51
title: "database"
---
# database
This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `database` arguments. You can use these commands to manually perform setup actions in the database, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deployment/deploying/manual-bootstrapping.md" >}}) section.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| spec                         | Generates the database schema from Liquibase.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -c, \-\-clear-change-log     | Deletes the changelog CSV in the PWD to force generation of the SQL files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -g, \-\--generate-schema-sql | The list of schemas to create. Specify schemas in the form `schema-type:schema-name`, where `schema-type` is one of the following: `config`, `messagebus`, `rbac`, or `crypto`. For example, use `config:my-config-schema,crypto:my-crypto-schema` to create config tables in a schema called `my-config-schema` and crypto tables in a schema called `my-crypto-schema`. Any schemas not specified take the default name, which is the same as schema-type. To create schemas using all default names, pass `""` as the value. If not specified, the generated SQL files do not create schemas and it is the responsibility of the database administrator to apply these files to the correct schema. |
| -l, \-\-location             | The path to write the generated DML files to.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| \-\-jdbc-url                 | The JDBC URL of the database. If not specified, the generation runs in offline mode.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -p, \-\-password             | The database password.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -s, \-\-schemas              | The list of SQL files to generate. If not specified, files for all schemas are generated.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -u, \-\-user                 | The database user.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

For example, the following command generates the files for all schemas in the directory `/tmp/db`:

   {{< tabs name="database">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -c -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -c -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}
