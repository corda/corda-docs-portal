---
date: '2022-12-20'
version: 'Corda 5.1'
menu:
  corda5:
    identifier: corda51-cordacli-database
    weight: 1000
    parent: corda51-cli-reference
section_menu: corda5
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

|Argument| Description                                                                        |
| --------------------------------------- | ---------------------------------------------------------------------------------- |
| spec                                    | Generates the database schema from Liquibase.                                      |
| -c, \-\-clear-change-log                | Deletes the changelogCSV in the PWD to force generation of the SQL files.          |
| -l, \-\-location                        | The path to write the generated DML files to.                                      |
| -s, \-\-schemas                         | The file of schema files to generate. If not specified, all schemas are generated. |

For example, the following command generates the files in the directory `/tmp/db`:

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