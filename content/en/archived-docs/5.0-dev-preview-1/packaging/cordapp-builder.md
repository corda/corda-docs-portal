---
date: '2021-09-2012:00:00Z'
title: "CorDapp Builder CLI"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-packaging
    identifier: corda-5-dev-preview-1-packaging-cordapp-builder
    weight: 200
section_menu: corda-5-dev-preview
expiryDate: '2022-09-28'
---

CorDapp Builder CLI is a command-line utility that assembles Corda package bundles (`.cpb` files) from Corda package files (`.cpk` files).


## Installation

CorDapp Builder CLI can be installed automatically or manually.

### Automatic installation

1. Download the [universal installer](https://download.corda.net/cordapp-builder/5.0.0-DevPreview-1.0.1/cordapp-builder-installer.jar).
2. Run the following command.
    ```console
    java -jar cordapp-builder-installer.jar
    ```
3. Start a new shell.
4. Test the program with the following command.
    ```console
    cordapp-builder --version
    ```

### Manual installation

#### Before you start

If a previous installation of CorDapp Builder CLI exists, remove it. See [deleting the CorDapp Builder CLI](#delete-the-cordapp-builder-cli).

#### Steps

1. Download the latest stable <a href="https://download.corda.net/cordapp-builder/5.0.0-DevPreview-1.0.1/cordapp-builder.tar">`.tar`</a> or <a href="https://download.corda.net/cordapp-builder/5.0.0-DevPreview-1.0.1/cordapp-builder.zip">`.zip`</a> file.

2. Create a new `bin/cordapp-builder` directory under the current users home directory.

3. Extract the previously-downloaded archive into this new directory.

   Once extracted, your folder structure should be as follows:

     ```text
     bin/cordapp-builder
      ├───bin
      └───lib
      ```
4. **Windows:** Add CorDapp Builder CLI to PATH:

   1. Go to the **Edit the system environment variables** Control Panel setting.

   2. Edit the **Path** user variable and add the cordapp-builder bin directory extracted in the previous step as a new entry. For example, `C:\Users\username\bin\cordapp-builder\bin`.

   3. If you are using Git Bash on Windows, update your home directory `username/.bashrc` file with the following code:

   ```shell
      # cordapp-builder default path
      export PATH="$HOME/bin/cordapp-builder/bin:$PATH"
   ```

5. **Linux or macOS**: Add CorDapp Builder CLI to PATH by adding the following code to the `~/.bashrc` (Linux) or `~/.zshrc` file (macOS):

    ```shell
      # cordapp-builder default path
      export PATH="$HOME/bin/cordapp-builder/bin:$PATH"
    ```

6. Verify installation by opening a new terminal session and running `cordapp-builder --version`.

   If successful, this outputs details of the installed CorDapp Builder CLI version.

## Usage

### Assemble a Corda package bundle

To assemble a `.cpb` file from a set of `.cpk` files use the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -o result.cpb
```

Where:
* `-o` specifies the output file.
* `--cpk` specifies a `.cpk` file to include in the bundle. You can use this option as many times as you want to specify as many `.cpk` files as you want.

If you have a `.cpk` file and all of its `.cpk` dependencies are located in a single folder `cpk-repository`, you can use the following command.

```bash
cordapp-builder create --cpk cpk-repository/root.cpk -A cpk-repository -o result.cpb
```

This fetches all the dependencies of `root.cpk` recursively from `cpk-repository` and bundle them in `result.cpb`.

You can also specify multiple repository folders:

```bash
cordapp-builder create --cpk root.cpk -A cpk-repository1 -A cpk-repository2 -o result.cpb
```

{{< note >}}

Providing multiple `.cpk` files with the same identifier is an error. The identifier of a `.cpk` file is the tuple of bundle symbolic name, bundle version, and set of public keys that have signed the main `.jar`.

```bash
$ cordapp-builder create --cpk file.cpk --cpk file.cpk
net.corda.packaging.DependencyResolutionException: Detected two CPKs with the same identifier Identifier(symbolicName=contracts, version=1.0, signers=[]): './file.cpk' and './file.cpk'
```

{{< /note >}}


### Sign the generated `.cpb` file

You can sign the generated `.cpb` file with the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p KEYSTORE_PASSWORD -P KEY_PASSWORD -o file.cpb
```

For enhanced security, you can also use either environment variables or a password file. Instead of typing `KEYSTORE_PASSWORD` and `KEY_PASSWORD` directly, to read secrets from environment variables `STORE_PASS` and `KEY_PASS` use, the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:env STORE_PASS -P:env KEY_PASS -o file.cpb
```

To read secrets from files `keystore_password_file.txt` and `key_password_file.txt` use the following command.

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:file keystore_password_file.txt -P:file key_password_file.txt -o file.cpb
```

{{< note >}}
The entire contents of the file will be used as a password, including any trailing new lines or white spaces.
{{< /note >}}

{{< note >}}
In the Corda 5 Developer Preview, although you can sign a `.cpb` file, Corda does not check the validity of the signature.
{{< /note >}}

## Delete the CorDapp Builder CLI

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

3. **Optional for Unix and macOS only**: Remove the symbolic link to the application launcher created in `$HOME/.local/bin/cordapp-builder`.
