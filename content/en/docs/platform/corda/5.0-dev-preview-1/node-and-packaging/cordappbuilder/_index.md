---
title: "CorDapp Builder CLI"
linkTitle: "CorDapp Builder CLI"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-node-packaging
    weight: 400
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Instructions on how to install and use CorDapp Builder CLI.
---

# CorDapp Builder CLI

## Installation

CorDapp Builder CLI is a command line interface utility used to assemble `.cpb` files from `.cpks`. Its functionality is going to be extended and it is going to be also integrated with Corda CLI.

### From source

1. Clone the Corda 5 repository using `git clone https://github.com/corda/corda5.git`
2. Run `./gradlew tools:cordapp-builder:installDist` in root directory of the corda5 repo.
3. Add `tools/cordapp-builder/build/install/cordapp-builder/bin` to your path.

### Manual installation

1. Download the latest package (either `.tar` or `.zip`) from [Artifactory](https://software.r3.com/artifactory/corda-os-maven-stable/net/corda/cordapp-builder/)
2. Extract it.
3. Add the `bin/` folder to the path.

### Automatic installation

1. Download the universal installer from [Artifactory](https://software.r3.com/artifactory/corda-os-maven-stable/net/corda/cordapp-builder/%5BRELEASE%5D/cordapp-builder-%5BRELEASE%5D-installer.jar)
2. Run the command:
    ```bash
    java -jar cordapp-builder-installer-*.jar
    ```
3. Start a new shell.
4. Test the program with:
    ```bash
    cordapp-builder --version
    ```

### To run the tool from the source directory

To run the tool from the source directory without installing it, run the following command:

```bash
./gradlew tools:cordapp-builder:installDist
./tools/cordapp-builder/build/install/cordapp-builder/bin/cordapp-builder
```

Add `./tools/cordapp-builder/build/install/cordapp-builder/bin` to your path or link `./build/install/cordapp-builder/bin/cordapp-builder` to somewhere in your path.
On Mac OS, for example, you can link the runner (on Windows this is a `.bat` file):

```bash
ln -s $(pwd)/build/install/cordapp-builder/bin/cordapp-builder /usr/local/bin/cordapp-builder
```

## Usage


### Assemble a `.cpb` file

To assemble a `.cpb` file from a set of `.cpk` files use:

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -o result.cpb
```

{{< note >}}

You can specify as many `.cpk` files as you want.

{{< /note >}}

If you have a `.cpk` file and all of its `.cpk` dependencies are located in a single folder `cpk-repository`, you can use:

```bash
cordapp-builder create --cpk cpk-repository/root.cpk -A cpk-repository -o result.cpb
```

This will fetch all the dependencies of `root.cpk` recursively from `cpk-repository` and bundle them in `result.cpb`.

You can also specify multiple repository folders:

```bash
cordapp-builder create --cpk root.cpk -A cpk-repository1 -A cpk-repository2 -o result.cpb
```

{{< attention >}}

Providing multiple `.cpk` files with the same identifier is an error. The identifier of a `.cpk` file is the tuple bundle symbolic name, bundle version, set of public keys that have signed the main `.jar`.

```bash
$ cordapp-builder create --cpk file.cpk --cpk file.cpk
net.corda.packaging.DependencyResolutionException: Detected two CPKs with the same identifier Identifier(symbolicName=contracts, version=1.0, signers=[]): './file.cpk' and './file.cpk'
```

{{< /attention >}}


### Sign the generated `.cpb` file

You can sign the generated `.cpb` file with:

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p KEYSTORE_PASSWORD -P KEY_PASSWORD -o file.cpb
```

For for enhanced security, you can also provide an environmental variable or a password file. Instead of typing `KEYSTORE_PASSWORD` and `KEY_PASSWORD` directly, to read secrets from environmental variables `STORE_PASS` and `KEY_PASS`use:

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:env STORE_PASS -P:env KEY_PASS -o file.cpb
```

To read secrets from files `keystore_password_file.txt` and `key_password_file.txt` (the whole file content will be used as a password, included any trailing newline/whitespace), use:

```bash
cordapp-builder create --cpk file1.cpk --cpk file2.cpk -k keystore.jks -a key-alias -p:file keystore_password_file.txt -P:file key_password_file.txt -o file.cpb
```
