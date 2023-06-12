---
date: '2022-09-22'
version: 'Corda 5.0'
title: "Resetting the CSDE"
menu:
  corda5:
    parent: corda5-develop-get-started
    identifier: corda5-reset
    weight: 8000
section_menu: corda5
---
# Resetting the CSDE
The CSDE creates temporary files to store data required to generate and upload Corda Package Installer (CPI) files and manage the Corda cluster.
If these files are modified, deleted, or otherwise get out of sync with the actual state of the Corda cluster, the CSDE Gradle tasks may not function correctly.
For example:
* A Corda cluster is started without using the `startCorda` task or by running `startCorda` from a different CSDE repository.
* A CPI file is uploaded without using the CSDE Gradle task.

This section describes how to reset the CSDE to handle these situations or other occasions when the CSDE tasks are not working as expected.
This process does the following:
* Stops any processes related to the Corda cluster.
* Removes the existing Corda cluster software (but not [Corda CLI](installing-corda-cli.html)).
* Deletes all of the temporary files that the CSDE creates and uses.
* Runs the Gradle `clean` task to remove any CPI build artifacts.

The instructions in this section use the following terms:
* `project-root-dir` — the project directory of the IntelliJ project contained in the repo.
   For example, if you git-cloned the `corda/CSDE-cordapp-template-kotlin` repo to `/Users/charlie.smith/DevWork/DevExWork`, `<project-root-dir>` is `/Users/charlie.smith/DevWork/DevExWork/CSDE-cordapp-template-kotlin`.
* `user-home` — the user home directory.
   * On Windows, this is typically something like `C:\Users\Charlie.Smith`.
   * On macOS, this is typically something like `/Users/charlie.smith`.
   * On Linux, this is typically something like `/home/charlie.smith`.

To reset the CSDE:
1. Stop any running combined worker processes:
   * On Linux/macOS:

      a. To find the process ID (pid), run:

      ```shell
      ps -ef | grep corda-combined-worker
      ```

       The combined worker process is the second ID returned. For example, 63892 in the following response:

      ```shell
      503 63892 52310   0  1:05PM ??         2:36.96 /Library/Java/JavaVirtualMachines/zulu-11.jdk/Contents/Home/bin/java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005 -Dco.paralleluniverse.fibers.verifyInstrumentation=true -jar /Users/.gradle/caches/modules-2/files-2.1/net.corda/corda-combined-worker/5.0.0.0-Hawk1.0/1b7c6fdecd5e54e09ec080905f2b6e14fad1a4d5/corda-combined-worker-5.0.0.0-Hawk1.0.jar --instance-id=0 -mbus.busType=DATABASE -spassphrase=password -ssalt=salt -spassphrase=password -ssalt=salt -ddatabase.user=user -ddatabase.pass=password -ddatabase.jdbc.url=jdbc:postgresql://localhost:5432/cordacluster -ddatabase.jdbc.directory=/Users/.corda/corda5/jdbcDrivers
      ```

      Alternatively, you can use the jps command to list java processes running:

      ```shell
      jps
     ```
     Which returns:
     ```
     23666 GradleDaemon
     25400 GradleDaemon
     18986
     1114
     41770 Jps
     25419 KotlinCompileDaemon
     63892 corda-combined-worker-5.0.0.0-Hawk.jar

     ```

      b. To stop the process, run:

      ```shell
      kill <pid-for-corda-combined-worker>
      ```

   * On Windows, run in PowerShell:
     ```shell
     Invoke-CimMethod -Query "SELECT * from Win32_Process WHERE name LIKE 'java.exe' and Commandline like '%corda-combined-worker%'" -MethodName "Terminate"
     ```
2. Check if the above commands were successful:
   * On Linux/macOS, run:
      ```shell
      ps -ef | grep corda-combined-worker
      ```
      or
      ```shell
      jps
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

   You should now be able to run all CSDE Gradle tasks again. These tasks download the Corda cluster software and recreate all of the temporary files, as required.
