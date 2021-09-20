---
date: '2021-09-01'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordacli
    weight: 300
project: corda-5
section_menu: corda-5-dev-preview
title: Deleting Corda CLI
---

To delete the Corda CLI tool, perform the following steps:

1. Delete the application's folder at its location.

   {{< note >}}

   If you performed automated installation, the installation directory is platform specific.

   {{< /note >}}

2. Remove the application's folder from the PATH.

   {{< note >}}

   How you remove the entry from the PATH depends on which shell you are using. For `bash`, manually edit the `$HOME/.bashrc` file and for `zsh`, the `$HOME/.zshrc` file.

   {{< /note >}}

3. **Optional for Unix and Mac OS only**: Remove the symbolic link to the application launcher created in `$HOME/.local/bin/cordapp-builder`.
