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
The Corda CLI is a command line tool which provides tooling for working with Corda clusters.
The CSDE handles calls to the Corda CLI and so the Corda CLI must be installed before using the CSDE.
A bash installation script is available to automate the installation of Corda CLI.
This script downloads Corda CLI, adds it to the path, and sets the auto-completion for Corda CLI to your bash/zsh profile.
On Windows, the script can run on a git-bash terminal.

To install Corda CLI:
1. Run the bash script:

   ```Bash
   curl "https://xxxxxxxxxx/corda-cli-downloader-5.0.0.0-DevPreview-2.sh" | sudo bash
   ```

2. Verify installation by opening a new terminal session and running `./corda-cli.sh`.

   If successful, this command lists the Corda CLI commands.

For information about working directly with the Corda CLI, see [Corda CLI](../developing/corda-cli/overview.html).
