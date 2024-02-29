---
date: '2023-11-01'
title: "Resetting the Corda Runtime Gradle Plugin"
description: Learn to stop and clean the Corda runtime Gradle plugin.
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-reset
    weight: 8000

---
# Resetting the Corda Runtime Gradle Plugin

The CorDapp template creates temporary files to store data required to generate and upload {{< tooltip >}}CPI{{< /tooltip >}} files and manage the Corda cluster.
If these files are modified, deleted, or otherwise get out of sync with the actual state of the Corda cluster, the CorDapp template Gradle tasks may not function correctly.
For example:

* A Corda cluster is started without using the `startCorda` task or by running `startCorda` from a different CorDapp Template repository.
* A CPI file is uploaded without using the CorDapp template Gradle task.

This section describes how to reset the CorDapp template to handle these situations or other occasions when the CorDapp template tasks are not working as expected.
This process does the following:

* Stops any processes related to the Corda cluster.
* Removes the existing Corda cluster software (but not the {{< tooltip >}}Corda CLI{{< /tooltip >}}).
* Deletes all of the temporary files that the CorDapp template creates and uses.
* Runs the Gradle `clean` task to remove any CPI build artifacts.

The instructions in this section use the following terms:

* `project-root-dir` — the project directory of the IntelliJ project contained in the repo.
   For example, if you git-cloned the `corda/cordapp-template-kotlin` repo to `/Users/charlie.smith/DevWork/DevExWork`, `<project-root-dir>` is `/Users/charlie.smith/DevWork/DevExWork/cordapp-template-kotlin`.
* `user-home` — the user home directory.
  * On Windows, this is typically something like `C:\Users\Charlie.Smith`.
  * On macOS, this is typically something like `/Users/charlie.smith`.
  * On Linux, this is typically something like `/home/charlie.smith`.

To reset the Corda runtime Gradle plugin:

1. Run the following command, to stop and remove Docker containers and network used by the Corda cluster, where:
   * `config/combined-worker-compose.yaml` is the path to the compose file. This should match the value of the `composeFilePath` property in the `cordaRuntimeGradlePlugin` section of the `build.gradle` file.
   * `corda-cluster` should match the `composeNetworkName` property. `corda-cluster` is the default value and is not set in the template code.

   ```shell
   docker compose -f config/combined-worker-compose.yaml -p corda-cluster down
   ```
   
1. Run the Gradle clean task:
   ```shell
   <project-root-dir>/gradlew clean
   ```
1. Delete the `<user-home>/.corda/corda5` directory and its contents.

1. Delete the `<project-root-dir>/workspace` directory and its contents.

   You should now be able to run all CorDapp template Gradle tasks again. These tasks download the Corda cluster software and recreate all of the temporary files, as required.
