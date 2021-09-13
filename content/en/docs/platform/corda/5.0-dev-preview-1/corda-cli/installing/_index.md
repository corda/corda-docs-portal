---
date: '2021-09-01'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordacli
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
title: Installing Corda CLI
---

Instructions on how to install the Corda CLI tool.

## Automated installation

Use the bash installation script to automate the manual steps. This script downloads Corda CLI, adds it to the path, and sets the auto completion for Corda CLI to your bash/zsh profile. On Windows the script can run on a git-bash terminal.

Run the bash script:

```
curl "https://staging.download.corda.net/corda-cli/1.0.0-DevPreview-RC05-807ddcda51ce4f1a933bb0489a7953a7/get-corda-cli.sh" | bash
```

{{< note >}}

The URL in the script is specific to a given release and will be updated once the GA release is ready.

{{< /note >}}

## Manual installation

1. Download either the [`.tar`](https://staging.download.corda.net/corda-cli/1.0.0-DevPreview-RC03-6f6261d84aa64a8b91eb9c92327e1e46/corda-cli.tar) or the [`.zip`](https://staging.download.corda.net/corda-cli/1.0.0-DevPreview-RC03-6f6261d84aa64a8b91eb9c92327e1e46/corda-cli.zip) file.
2. Extract it.
3. Add the `bin/` directory to your path.
