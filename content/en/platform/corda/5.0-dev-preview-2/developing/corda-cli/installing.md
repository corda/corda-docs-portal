---
date: '2020-09-08T12:00:00Z'
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-cordacli-installing
    weight: 1000
    parent: corda-5-dev-preview-cordacli
section_menu: corda-5-dev-preview
title: Installing Corda CLI
---
A bash installation script is available to automate the installation of Corda CLI. This script downloads Corda CLI, adds it to the path, and sets the
auto-completion for Corda CLI to your bash/zsh profile. On Windows, the script can run on a git-bash terminal.

1. Run the bash script:

   ```Bash
   curl "https://xxxxxxxxxx/get-corda-cli.sh" | bash
   ```

2. Verify installation by opening a new terminal session and running `corda-cli -v`.

   If successful, this will output details of the installed Corda CLI version.
