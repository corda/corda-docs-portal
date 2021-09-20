---
title: "CorDapp Builder CLI"
linkTitle: "CorDapp Builder CLI"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-packaging
    weight: 400
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Instructions on how to install and use CorDapp Builder CLI.
---

# CorDapp Builder CLI

CorDapp Builder CLI is a command-line utility that assembles Corda Package Bundles (`.cpb` files) from Corda Packages (`.cpk` files).

{{% note %}}
In future releases, it will be integrated into the `corda-cli` utility.
{{% /note %}}

## Installation

CorDapp Builder CLI can be installed manually, or installed automatically.

### Manual installation

1. Download the latest package (either `.tar` or `.zip`) from [Artifactory](https://software.r3.com/artifactory/corda-os-maven-stable/net/corda/cordapp-builder/).
2. Extract it.
3. Add its `bin/` folder to your path.

### Automatic installation

1. Download the universal installer from [Artifactory](https://software.r3.com/artifactory/corda-os-maven-stable/net/corda/cordapp-builder/%5BRELEASE%5D/cordapp-builder-%5BRELEASE%5D-installer.jar).
2. Run the following command.
    ```bash
    java -jar cordapp-builder-installer-*.jar
    ```
3. Start a new shell.
4. Test the program with the following command.
    ```bash
    cordapp-builder --version
    ```

## Usage

### Assemble a Corda Package Bundle (`.cpb` file)

To assemble a `.cpb` file from a set of `.cpk` files use the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -o result.cpb
```

Where:
* `-o` specifies the output file.
* `-cpk` specifies a `.cpk` file to include in the bundle. You can use this option as many times as you want in order to specify as many `.cpk` files as you want

If you have a `.cpk` file and all of its `.cpk` dependencies are located in a single folder `cpk-repository`, you can use the following command.

```bash
cordapp-builder create --cpk cpk-repository/root.cpk -A cpk-repository -o result.cpb
```

This will fetch all the dependencies of `root.cpk` recursively from `cpk-repository` and bundle them in `result.cpb`.

You can also specify multiple repository folders:

```bash
cordapp-builder create --cpk root.cpk -A cpk-repository1 -A cpk-repository2 -o result.cpb
```

{{< attention >}}

Providing multiple `.cpk` files with the same identifier is an error. The identifier of a `.cpk` file is the tuple of bundle symbolic name, bundle version, and set of public keys that have signed the main `.jar`.

```bash
$ cordapp-builder create --cpk file.cpk --cpk file.cpk
net.corda.packaging.DependencyResolutionException: Detected two CPKs with the same identifier Identifier(symbolicName=contracts, version=1.0, signers=[]): './file.cpk' and './file.cpk'
```

{{< /attention >}}


### Sign the generated `.cpb` file

You can sign the generated `.cpb` file with the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p KEYSTORE_PASSWORD -P KEY_PASSWORD -o file.cpb
```

For for enhanced security, you can also use either environment variables or a password file. Instead of typing `KEYSTORE_PASSWORD` and `KEY_PASSWORD` directly, to read secrets from environment variables `STORE_PASS` and `KEY_PASS` use, the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:env STORE_PASS -P:env KEY_PASS -o file.cpb
```

To read secrets from files `keystore_password_file.txt` and `key_password_file.txt` use the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:file keystore_password_file.txt -P:file key_password_file.txt -o file.cpb
```

{{% note %}}
The entire contents of the file will be used as a password, including any trailing newlines or whitespace.
{{% /note %}}

{{% note %}}
In this release, although you can sign a `.cpb` file, Corda does not check the validity of the signature.
{{% /note %}}

## Uninstalling CorDapp Builder CLI

To uninstall CorDapp Builder CLI tool, perform the following steps:

1. Delete the application's folder.

   {{< note >}}

   If you performed [automatic installation](#automatic-installation), the installation directory is platform specific.

   {{< /note >}}

2. Remove the application's folder from the `PATH`.

   {{< note >}}

   How you remove the entry from the `PATH` depends on which shell you are using. For example:

* For `fish`, delete `$HOME/.config/fish/conf.d/cordapp-builder.fish`.
* For `bash`, edit`$HOME/.bashrc`.
* For `zsh`, edit `$HOME/.zshrc`.

   {{< /note >}}

3. **Optional for Unix and Mac OS only**: Remove the symbolic link to the application launcher created in `$HOME/.local/bin/cordapp-builder`.
