---
date: '2023-04-12'
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-networks-cli
    weight: 1050
    parent: corda5-networks-tooling
section_menu: corda5
title: Installing the Corda CLI
---
# Installing the Corda CLI
Corda CLI (command line interface) is a command line tool that supports various Corda-related tasks. For information about the commands available, see the [Corda CLI reference content]({{< relref "../../reference/corda-cli/_index.md">}}).

## Third-Party Prerequisites

Software | Version
---------|------------
Java     | Azul JDK 11

## Downloading Corda CLI

To obtain the Corda CLI installer, download `platform-jars-Iguana1.0.tar.gz` from the [R3 Developer Portal](https://developer.r3.com/next-gen-corda/#get-corda) and extract `corda-cli-downloader-5.0.0.0-Iguana1.0.zip` from `net\corda\cli\deployment\corda-cli-installer\5.0.0.0-Iguana1.0`.

## Installing on Linux/macOS

1. Ensure that you remove any existing installations of Corda CLI by deleting the `<user-home>/.corda/cli` folder.
2. Start a shell session (bash or zsh).
2. Change directory to where you saved `corda-cli-downloader-5.0.0.0-Iguana1.0.zip`.
3. Extract the contents of the `zip` file:
   ```shell
   unzip ./corda-cli-downloader-5.0.0.0-Iguana1.0.zip -d corda-cli-downloader-5.0.0.0-Iguana1.0
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-downloader-5.0.0.0-Iguana1.0
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

1. Ensure that you remove any existing installations of Corda CLI by deleting the `<user-home>/.corda/cli` folder.
2. Start a Powershell session.
2. Change directory to where you saved `corda-cli-downloader-5.0.0.0-Iguana1.0.zip`.
3. Extract the contents of the `zip` file:
   ```shell
   Expand-Archive .\corda-cli-downloader-5.0.0.0-Iguana1.0.zip
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-downloader-5.0.0.0-Iguana1.0
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
