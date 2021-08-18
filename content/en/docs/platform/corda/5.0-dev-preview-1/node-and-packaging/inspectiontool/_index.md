---
title: "CPK inspection tool"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-node-packaging
    weight: 300
project: corda-5
section_menu: corda-5-dev-preview
description: >
  The `corda-cli` command for inspecting CPK packages.
---
# CPK inspection tool


You can use the `package` command in the `corda-cli` command-line utility to inspect the contents of Corda package files. Corda package file names can end with `.cpi`, `.cpk` and `.cpb`. This command can also be used on `.jar` files.

## Syntax

````bash
$ corda-cli package --help

Commands to inspect Corda Package files (cpk, cpi, cpb) and jars
Usage: corda-cli package [COMMAND]
Commands:
  list, ls       List the contents of a Corda package file or jar
  depends, deps  List Corda package dependencies
  cat            Cat the contents of a cpk/cpi file or a file in a nested jar
````

Alias: `pkg`.

## Subcommands

### `list`

This command recursively lists the content of any Corda package file (`.cpk`, `.cpi`, `.cpb`), which can contain other Corda package files, and so on.

Alias: `ls`

#### Syntax

````bash
corda-cli pkg list <file>
````

Where `<file>` is the Corda package file.

#### Example

````bash
$ corda-cli pkg ls httprpc-demo.cpb
httprpc-demo.cpb:install.json
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/CORDAPP.SF
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/CORDAPP.EC
...
````

### `cat`

This command prints to stdout the content of the supplied file. Note that this is a 'nested path' returned by the `corda-cli package ls <file>` command.

#### Syntax

````bash
corda-cli package cat <nested:path>
````

Where `<nested:path>` is the root file system path, and nested paths with in the archive concatenated by `:`.


#### Example

````bash
$ corda-cli pkg ls httprpc-demo.cpb
httprpc-demo.cpb:install.json
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk
httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF

$ corda-cli pkg cat httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:META-INF/MANIFEST.MF
Manifest-Version: 1.0
Corda-CPK-Format: 1.0
Corda-CPK-Cordapp-Name: net.corda.httprpc-demo-workflows
Corda-CPK-Cordapp-Version: 1.0.0.SNAPSHOT
Corda-CPK-Cordapp-Licence: Open Source (Apache 2)
Corda-CPK-Cordapp-Vendor: R3
Corda-CPK-Built-Platform-Version: 999

Name: httprpc-demo-workflows-1.0.0-SNAPSHOT.jar
SHA-256-Digest: Kz8WY20GJMypiomOlhMLHb6TlgXn8sKVVBr6/Pt/ny8=
...
````

### `depends`

This is a convenience subcommand that recursively lists all `CPKDependency` and `DependencyConstraints` files in the specified file.

Alias: `deps`

#### Syntax

````bash
corda-cli pkg depends <file>
````

Where `<file>` is the Corda package file.

#### Example

````bash
$ corda-cli pkg deps httprpc-demo.cpb

httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-contracts-1.0.0-SNAPSHOT.jar:META-INF/CPKDependencies:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cpkDependencies xmlns="urn:corda-cpk"/>

httprpc-demo.cpb:httprpc-demo-contracts-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-contracts-1.0.0-SNAPSHOT.jar:META-INF/DependencyConstraints:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dependencyConstraints xmlns="urn:corda-cpk"/>

httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-workflows-1.0.0-SNAPSHOT.jar:META-INF/CPKDependencies:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cpkDependencies xmlns="urn:corda-cpk">
    <cpkDependency>
        <name>net.corda.flows</name>
        <version>1.0.0.SNAPSHOT</version>
        <signers>
            <signer algorithm="SHA-256">qlnYKfLKj931q+pA2BX5N+PlTlcrZbk7XCFq5llOfWs=</signer>
        </signers>
    </cpkDependency>
    <cpkDependency>
        <name>net.corda.httprpc-demo-contracts</name>
        <version>1.0.0.SNAPSHOT</version>
        <signers>
            <signer algorithm="SHA-256">qlnYKfLKj931q+pA2BX5N+PlTlcrZbk7XCFq5llOfWs=</signer>
        </signers>
    </cpkDependency>
</cpkDependencies>

httprpc-demo.cpb:httprpc-demo-workflows-1.0.0-SNAPSHOT-cordapp.cpk:httprpc-demo-workflows-1.0.0-SNAPSHOT.jar:META-INF/DependencyConstraints:
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<dependencyConstraints xmlns="urn:corda-cpk"/>
````

## Further reading
* [The Proposed Packaging Model](/engineering-central/teams/architecture/cordapp-packaging-and-isolation/#the-proposed-packaging-model)
* [Cordapp CPK Gradle Plugin Readme](https://github.com/corda/corda-gradle-plugins/tree/master/cordapp-cpk)
* [Corda CPK Metadata Format](https://github.com/corda/platform-eng-design/blob/996d0e31a9991b509b41db29f528fac208b91ba8/core/corda-5/corda-5.0/cpk/cpk-metadata-format.md)
