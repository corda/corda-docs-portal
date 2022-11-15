---
date: '2022-11-15'
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-cordacli-installing
    weight: 1050
    parent: corda-5-alpha-deploy
section_menu: corda-5-alpha
title: Installing the Corda CLI
---
Corda CLI (command line interface) is a command line tool that supports various Corda related tasks, including [Corda Package Installer (CPI)](../introduction/key-concepts.html#corda-package-installer-cpi) creation and Corda cluster management.

## Downloading Corda CLI

To obtain the Corda CLI installer:
1. Download `platform-jars-Eagle.tar.gz` from the [R3 Customer Hub](https://r3.force.com/)
2. Extract `corda-cli-downloader-Eagle.zip` from `net\corda\cli\deployment\corda-cli-installer\5.0.0.0-Eagle`.

## Installing on Linux/macOS

1. Start a shell session (bash or zsh).
2. Change directory to where you saved `corda-cli-downloader-Eagle.zip`.
3. Extract the contents of the `zip` file:
   ```shell
   unzip ./corda-cli-downloader-Eagle.zip -d corda-cli-downloader-Eagle
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-downloader-Eagle
   ```
5. Run the install script:
   ```shell
   ./install.sh
   ```
   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. For example, on macOS, this is typically something like `/Users/charlie.smith` or on Linux, something like `/home/charlie.smith`.

## Installing on Windows

1. Start a Powershell session.
2. Change directory to where you saved `corda-cli-downloader-Eagle.zip`.
3. Extract the contents of the `zip` file:
   ```shell
   Expand-archive .\corda-cli-downloader-Eagle.zip
   ```
4. Change directory to the directory extracted from the `zip` file:
   ```shell
   cd corda-cli-downloader-Eagle
   ```
5. Run the install script:
   ```shell
   .\install.ps1
   ```
   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. On Windows, this is typically something like `C:\Users\Charlie.Smith`.

   {{< note >}}
   If your PowerShell execution policy does not allow you to run this script, copy the contents to your own PowerShell script and execute that instead.
   {{< /note >}}
