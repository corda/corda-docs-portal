---
date: '2021-09-01'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordacli
    weight: 200
section_menu: corda-5-dev-preview
title: Installing Corda CLI
---

You can install Corda CLI manually or through automated installation. Before installing via either of these methods, ensure that you have [Docker](https://www.docker.com/) version 18.06.0 or higher installed.

## Automated installation

Use the bash installation script to automate the manual steps. This script downloads Corda CLI, adds it to the path, and sets the
auto-completion for Corda CLI to your bash/zsh profile. On Windows the script can run on a git-bash terminal.

1. Run the bash script:

   ```Bash
   curl "https://download.corda.net/corda-cli/1.0.0-DevPreview/get-corda-cli.sh" | bash
   ```

2. Verify installation by opening a new terminal session and running `corda-cli -v`.

   If successful, this will output details of the installed Corda CLI version.

## Manual installation

### Before you start

If a previous installation of Corda CLI exists, remove it. See [Deleting Corda CLI](../../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/deleting-corda-cli.md).

### Steps

1. Download either the <a href="https://download.corda.net/corda-cli/1.0.0-DevPreview/corda-cli.tar">`.tar`</a> or <a href="https://download.corda.net/corda-cli/1.0.0-DevPreview/corda-cli.zip">`.zip`</a> file.

2. Create a new `bin/corda-cli` directory under the current users home directory.

3. Extract the previously-downloaded archive into this new directory.

   Once extracted, your folder structure should be:

     ```text
     bin/corda-cli
      ├───bin
      │   └───complete
      └───lib
      ```
4. **Windows:** Add Corda CLI to PATH:

   a. Go to the **Edit the system environment variables** Control Panel setting.

   b. Edit the **Path** user variable and add the Corda CLI bin directory extracted in the previous step as a new entry. For example, `C:\Users\username\bin\corda-cli\bin`.

   c. If you are using Git Bash, update your home directory `username/.bashrc` file with the code:

   ```shell
      # Corda-CLI default path
      export PATH="$HOME/bin/corda-cli/bin:$PATH"
      if [[ -f $HOME/bin/corda-cli/bin/complete/corda-cli_completion.sh ]]; then
      source $HOME/bin/corda-cli/bin/complete/corda-cli_completion.sh
      fi
   ```

5. **Linux or macOS**: Add Corda CLI to PATH by adding this code to the `~/.bashrc` (Linux) or `~/.zshrc` file (macOS):

    ```shell
      # Corda-CLI default path
      export PATH="$HOME/bin/corda-cli/bin:$PATH"
      if [[ -f $HOME/bin/corda-cli/bin/complete/corda-cli_completion.sh ]]; then
      source $HOME/bin/corda-cli/bin/complete/corda-cli_completion.sh
      fi
    ```

6. Verify installation by opening a new terminal session and running `corda-cli -v`.

   If successful, this will output details of the installed Corda CLI version.
