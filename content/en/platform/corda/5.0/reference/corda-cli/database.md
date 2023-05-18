---
date: '2022-12-20'
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cordacli-database
    weight: 1000
    parent: corda5-cli-reference
section_menu: corda5
title: "database"
---

This section lists the Corda CLI `database` arguments. You can use these commands to manually perform setup actions in the database, as described in the [Manual Bootstrapping]({{< relref "../../deploying-operating/deploying/bootstrapping.md" >}}) section.

| <div style="width:160px">Argument</div> | Description                                                                        |
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