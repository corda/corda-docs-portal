---
date: '2022-09-22'
title: "Resetting the CSDE"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-flow
    weight: 8000
section_menu: corda-5-dev-preview
---
The CSDE creates temporary files, which it uses to store data required to generate and upload CPI files and to manage the Corda cluster.
If these files are modified, deleted, or otherwise get out of sync with the actual state of the Corda cluster, the CSDE Gradle tasks may not function correctly.   
For example:
* A Corda cluster is started without using the `startCorda` task or by running `startCorda` from a different CSDE repository.
* A CPI file is uploaded without using the CSDE Gradle task.

To handle these situations or if the CSDE tasks are just not working as expected, follow the “CSDE Reset Procedure” given below***
This process does the following:
* Stops any processes related to the Corda cluster.
* Removes the existing Corda cluster software (but not Corda CLI).
* Deletes all of the temporary files that the CSDE creates and uses.
* Runs the Gradle `clean` task to remove any CPI build artifacts.





Definition Of Terms
“<project-root-dir>” means the project directory of the Intellij project contained in the repo. For example if I have git-cloned the corda/CSDE-cordapp-template-kotlin to /Users/chris.barratt/DevWork/DevExWork then <project-root-dir> is /Users/chris.barratt/DevWork/DevExWork/CSDE-cordapp-template-kotlin.

“<user-home>” means the user home directory.

On Windows this is typically something like C:\Users\Chris.Barratt .

On MacOS this is typically something like /Users/chris.barratt.

On Linux this typically something like /home/chris.barratt.

CSDE Reset Procedure
Stop any running combined-worker processes

On Linux / MacOS

Find the process ID (pid) run:


ps | grep corda-combined-worker
To stop the process run:


kill <pid-for-corda-combined-worker>
On windows

To stop the combined worker process run in powershell:


invoke-CimMethod -Query "SELECT * from Win32_Process WHERE name LIKE 'java.exe' and Commandline like '%corda-combined-worker%'" -MethodName "Terminate"
You can check whether these commands were successful -

on Linux / MacOS run:


ps | grep corda-combined-worker
on Window run:


Get-CimInstance -Query "SELECT * from Win32_Process WHERE name LIKE 'java.exe' and Commandline like '%corda-combined-worker%'"
Stop any CSDEpostgresql containers run:


docker stop CSDEpostgresql
You check what containers are running with


docker ps
run the gradle clean task from a terminal:


<project-root-dir>/gradlew clean
delete the <user-home>/.corda/corda5 directory and its contents

delete <project-root-dir>/workspace directory and its contents



After the procedure is carried out you should be able to run all CSDE gradle tasks again.  These will download the Corda cluster software and recreate all the temporary files as required.
