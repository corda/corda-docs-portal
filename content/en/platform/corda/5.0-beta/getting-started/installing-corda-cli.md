---
date: '2022-11-23'
menu:
  corda-5-beta:
    identifier: corda-5-beta-cordacli-csde-installing
    weight: 1050
    parent: corda-5-beta-start
section_menu: corda-5-beta
title: Installing the Corda CLI
---

Corda CLI (command line interface) is a command line tool that supports various Corda-related tasks, including [Corda Package Installer (CPI)](../introduction/key-concepts.html#corda-package-installer-cpi) creation and Corda cluster management.
The CorDapp Standard Development Environment (CSDE) uses Corda CLI in the background. As a result, you must install Corda CLI before using CSDE.

{{< note >}}
Performing command line instructions directly is described in the relevant sections throughout the documentation. 
{{< /note >}}

## Third-Party Prerequisites

Software | Version
---------|------------
Java     | Azul JDK 11

## Downloading Corda CLI

To obtain the Corda CLI installer:
1. Download `platform-jars-Eagle.tar.gz` from the [R3 Customer Hub](https://r3.force.com/).
2. Extract `corda-cli-installer-5.0.0.0-Eagle.zip` from `net\corda\cli\deployment\corda-cli-installer\5.0.0.0-Eagle`.

## Installing on Linux/macOS

1. Start a shell session (bash or zsh).
2. Change directory to where you saved `corda-cli-installer-5.0.0.0-Eagle.zip`.
3. Extract the contents of the `zip` file:
   ```shell
   unzip ./corda-cli-installer-5.0.0.0-Eagle.zip -d corda-cli-installer-5.0.0.0-Eagle
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-installer-5.0.0.0-Eagle
   ```
5. Run the install script:
   ```shell
   ./install.sh
   ```
   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. For example, on macOS, this is typically something like `/Users/charlie.smith` or on Linux, something like `/home/charlie.smith`.

6. Run the following command to verify your installation:
   ```shell
   ./corda-cli.sh -h
   ```
   If successful, this outputs details of the Corda CLI commands.

## Installing on Windows

1. Start a Powershell session.
2. Change directory to where you saved `corda-cli-installer-5.0.0.0-Eagle`.
3. Extract the contents of the `zip` file:
   ```shell
   Expand-Archive .\corda-cli-installer-5.0.0.0-Eagle.zip
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-installer-5.0.0.0-Eagle
   ```
5. Run the install script:
   ```shell
   .\install.ps1
   ```
   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. On Windows, this is typically something like `C:\Users\Charlie.Smith`.

   {{< note >}}
   If your PowerShell execution policy does not allow you to run this script, copy the contents to your own PowerShell script and execute that instead.
   {{< /note >}}

6. Run the following command to verify your installation:
     ```shell
     corda-cli.cmd -h
     ```
    If successful, this outputs details of the Corda CLI commands.   
