---
date: '2022-12-20'
menu:
  corda-5-beta:
    identifier: corda-5-beta-cordacli-database
    weight: 2000
    parent: corda-5-beta-cordacli-deploy-commands
section_menu: corda-5-beta
title: "database"
---

This section lists the Corda CLI `database` arguments. You can use these commands to manually perform setup actions in the database, as described in the [Manual Bootstrapping Tutorial](deployment-tutorials/manual.html).

Usage: corda database spec [-c] [-l=<outputDir>] [-s=<schemasToGenerate>[,
                           <schemasToGenerate>...]]...
Does database schema generation from liquibase
  -c, --clearChangeLog   Automatically delete the changelogCSV in the PWD to
                           force generation of the sql files
  -l, --location=<outputDir>
                         Directory to write all files to
  -s, --schemas=<schemasToGenerate>[,<schemasToGenerate>...]
                         File of schema files to generate. Default is all
                           schemas

| Argument             | Description                                                                        |
| -------------------- | ---------------------------------------------------------------------------------- |
| spec                 | Generates the database schema from liquibase.                                      |
| -c, --clearChangeLog | Deletes the changelogCSV in the PWD to force generation of the SQL files.          |
| -l, --location       | The path to write the generated DML files to.                                          |
| -s, --schemas        | The file of schema files to generate. If not specified, all schemas are generated. |

For example, the following command generates the files in the directory `/tmp/db`:

   {{< tabs name="database">}}
   {{% tab name="Linux" %}}
   ```sh
   corda-cli.sh database spec -c -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="macOS" %}}
   ```sh
   corda-cli.sh database spec -c -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="Windows" %}}
   ```shell
   corda-cli.cmd database spec -c -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}