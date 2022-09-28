---
date: '2022-09-22'
title: "Resetting the CSDE"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-reset
    weight: 8000
section_menu: corda-5-dev-preview2
---
The CSDE creates temporary files, which it uses to store data required to generate and upload CPI files and to manage the Corda cluster.
If these files are modified, deleted, or otherwise get out of sync with the actual state of the Corda cluster, the CSDE Gradle tasks may not function correctly.   
For example:
* A Corda cluster is started without using the `startCorda` task or by running `startCorda` from a different CSDE repository.
* A CPI file is uploaded without using the CSDE Gradle task.

This section describes how to reset the CSDE to handle these situations or other occasions when the CSDE tasks are just not working as expected. This process does the following:
* Stops any processes related to the Corda cluster.
* Removes the existing Corda cluster software (but not Corda CLI).
* Deletes all of the temporary files that the CSDE creates and uses.
* Runs the Gradle `clean` task to remove any CPI build artifacts.

The instructions in this section use the following terms:
* `project-root-dir` — the project directory of the Intellij project contained in the repo.
   For example, if you git-cloned the `corda/CSDE-cordapp-template-kotlin` to `/Users/charlie.smith/DevWork/DevExWork` then `<project-root-dir>` is `/Users/charlie.smith/DevWork/DevExWork/CSDE-cordapp-template-kotlin`.
* `user-home` — the user home directory.
   * On Windows, this is typically something like `C:\Users\Charlie.Smith`.
   * On MacOS, this is typically something like `/Users/charlie.smith`.
   * On Linux, this typically something like `/home/charlie.smith`.

To rest the CSDE:
1. Stop any running combined worker processes:
   * On Linux/MacOS:
      1. To find the process ID (pid), run:
         ```shell
         ps | grep corda-combined-worker
         ```
      2. To stop the process, run:
         ```shell
         kill <pid-for-corda-combined-worker>
         ```
   * On Windows, run in PowerShell:
         ```shell
         invoke-CimMethod -Query "SELECT * from Win32_Process WHERE name LIKE 'java.exe' and Commandline like '%corda-combined-worker%'" -MethodName "Terminate"
         ```
2. Check if the above commands were successful:
   * On Linux/MacOS, run:
      ```shell
      ps | grep corda-combined-worker
      ```
   * On Windows, run:
      ```shell
      Get-CimInstance -Query "SELECT * from Win32_Process WHERE name LIKE 'java.exe' and Commandline like '%corda-combined-worker%'"
      ```
3. To stop any `CSDEpostgresql` containers, run:
   ```shell
   docker stop CSDEpostgresql
   ```
   You can check which containers are running using:
   ```shell
   docker ps
   ```
4. Run the Gradle clean task:
   ```shell
   <project-root-dir>/gradlew clean
   ```
5. Delete the `<user-home>/.corda/corda5` directory and its contents.

6. Delete the `<project-root-dir>/workspace` directory and its contents.

   You should now be able to run all CSDE Gradle tasks again. These will download the Corda cluster software and recreate all the temporary files, as required.
