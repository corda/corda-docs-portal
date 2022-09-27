---
date: '2020-09-08T12:00:00Z'
menu:
  corda-5-dev-preview2:
    identifier: corda-5-dev-preview-cordacli-csde-installing
    weight: 1050
    parent: corda-5-dev-preview-start
section_menu: corda-5-dev-preview2
title: Installing the Corda CLI
---
Corda CLI (command line interface) is a command line tool that supports various Corda related tasks, including CPI creation and Corda cluster management.
Direct use of Corda CLI by Developers is not supported in Developer Preview 2. However, the [CorDapp Standard Development Environment (CSDE)](../cordapp-standard-development-environment/csde.html) uses Corda CLI in the background.
As a result, you must install Corda CLI before using CSDE.

## Downloading Corda CLI
To install Corda-CLI, download the installation `zip` file from https://download.corda.net/packages/corda-cli-downloader/5.0.0.0-DevPreview-2/corda-cli-downloader-5.0.0.0-DevPreview-2.zip.

## Installing on Linux/MacOS

1. Start a shell session (bash or zsh).

2. Change directory to where you downloaded `corda-cli-downloader-5.0.0.0-DevPreview-2.zip`.

3. Extract the contents of the `zip` file:

   ```shell
unzip ./corda-cli-downloader-5.0.0.0-DevPreview-2.zip -d corda-cli-downloader-5.0.0.0-DevPreview-2
   ```

4. Change directory to the directory extracted from the `zip` file:

   ```shell
cd corda-cli-downloader-5.0.0.0-DevPreview-2
   ```

5. Run the install script:

   ```shell
./install.sh
   ```

   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. For example, on MacOS, this is typically something like `/Users/charlie.smith` or on Linux, something like `/home/charlie.smith`.

## Installing on Windows

1. Start a Powershell session.

2. Change directory to where you downloaded `corda-cli-downloader-5.0.0.0-DevPreview-2.zip`.

3. Extract the contents of the `zip` file:

   ```shell
 Expand-archive .\corda-cli-downloader-5.0.0.0-DevPreview-2.zip
   ```

4. Change directory to the directory extracted from the `zip` file:

   ```shell
cd corda-cli-downloader-5.0.0.0-DevPreview-2
   ```

5. Run the install script:

   ```shell
.\install.ps1
   ```

   The script installs Corda CLI to `<user-home>/.corda/cli`, where `<user-home>` refers to your user home directory. On Windows, this is typically something like `C:\Users\Charlie.Smith`.
<!-- For information about working directly with the Corda CLI, see [Corda CLI](../developing/corda-cli/overview.html).-->
