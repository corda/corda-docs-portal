---
aliases:
- /releases/4.4/tools-config-obfuscator.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-ent-4-4-tool-index
tags:
- tools
- config
- obfuscator
title: Configuration Obfuscator
---


# Configuration Obfuscator

The purpose of this tool is to obfuscate sensitive information in configuration files. The Obfuscator tool takes
a seed and a passphrase as input to obfuscate a given config file. Processes that accept obfuscated config
must be provided the same seed and passphrase to deobfuscate the configuration.

{{< note >}}
The tool makes node installation less vulnerable to someone trawling plain text files searching for passwords and
credentials of resources that they should not have access to in the first place.
{{< /note >}}

{{< warning >}}
This feature will not make password protection completely secure. However, it will protect the node
against trawling attacks.

It is also recommended to use the most up to date version of this tool for improved security.
{{< /warning >}}



## Using the command-line tool

The command-line tool is included as a JAR file, named `corda-tools-config-obfuscator-<version>.jar`.
This tool takes as input the configuration file that is to be obfuscated, denoted `CONFIG_FILE` in
the usage screen. The tool also takes a seed and a passphrase as inputs, and uses them to derive a 256bit AES encryption
key.


{{< warning >}}
For backwards compatibility reasons, the seed and passphrase have default values and can be omitted.
However, to gain the benefits of obfuscated configuration files, the seed and passphrase must be set.
{{< /warning >}}


```bash
config-obfuscator [-hiV] [--config-obfuscation-passphrase[=<cliPassphrase>]]
                  [--config-obfuscation-seed[=<cliSeed>]] [-w[=<writeToFile>]]
                  [--logging-level=<loggingLevel>] CONFIG_FILE
                  [HARDWARE_ADDRESS]
```


* `CONFIG_FILE` is the configuration file to obfuscate.
- `--config-obfuscation-passphrase[=<cliPassphrase>]` The passphrase used in the key derivation function when generating an AES key. Leave blank to provide input interactively.
- `--config-obfuscation-seed[=<cliSeed>]` The seed used in the key derivation function to create a salt. Leave blank to provide input interactively.
* `-w=[<writeToFile>]` is a flag to indicate that the tool should write the obfuscated output to
disk, using the same file name as the input (if left blank and provided at the end of the command line),
or the provided file name.
* `-i` is a flag, which if set, says to provide input to obfuscated fields interactively.
* `-h`, `--help` is a flag used to show this help message and exit.
* `-V`, `--version` is a flag used to print version information and exit.

The following options provide backwards compatibility, but should not be used in cases where backwards compatibility is not required.
* `HARDWARE_ADDRESS` is the primary hardware address of the machine on which the configuration file resides. By default, the MAC address of the
running machine will be used. Supplying `DEFAULT` will explicitly use the default value.

Note that, by default, the tool only prints out the transformed configuration to the terminal for
verification. To persist the changes, we need to use the `-w` flag, which ensures that the obfuscated
content gets written back into the provided configuration file.

The `-w` flag also takes an optional file name for cases where we want to write the result back to
a different file. If the optional file name is not provided, the flag needs to be provided at the end
of the command:

```bash
# Explicit output file provided
$ java -jar corda-tools-config-obfuscator-<version>.jar -w node.conf node_template.conf

# No output file provided
$ java -jar corda-tools-config-obfuscator-<version>.jar node_template.conf -w
```

Note also that `HARDWARE_ADDRESS` is optional.

{{< note >}}
The tool works on both HOCON and JSON files. Include directives (i.e. `include "other.conf"`) are not followed by the
tool. If you wish to obfuscate fields in multiple files, you will need to run the tool against each file individually.
The node will de-obfuscate the included files automatically.
{{< /note >}}

{{< warning >}}
The Corda Enterprise Network Manager (see the CENM section on [https://docs.corda.net/](https://docs.corda.net/)) does not currently support obfuscated configurations.
{{< /warning >}}



## Configuration directives

To indicate parts of the configuration that should be obfuscated, we can place text markers on the form
`<encrypt{...}>`, like so:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "<encrypt{testpassword}>",
  // (...)
}
```

Which, after having been run through the obfuscation tool, would result in something like:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "<{8I1E8FKrBxVkRpZGZKAxKg==:oQqmyYO+SZJhRkPB7laNyQ==}>",
  // (...)
}
```

When run by a Corda node on a machine with the matching hardware address, the configuration would be
deobfuscated on the fly and interpreted like:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "testpassword",
  // (...)
}
```

These directives can be placed arbitrarily within string properties in the configuration file, with a maximum of one per line.
For instance:

```json
{
  // (...)
  "dataSourceProperties" : {
    "dataSource" : {
      "url" : "jdbc:h2:file:persistence;<encrypt{sensitive-options-go-here}>",
      "user" : "<encrypt{your-database-username}>",
      "password" : "<encrypt{your-secret-database-password}>"
    },
    "dataSourceClassName" : "org.h2.jdbcx.JdbcDataSource"
  },
  // (...)
}
```

## Limitations

The `<encrypt{}>` blocks can only appear inside string properties. They cannot be used to obfuscate entire
configuration blocks. Otherwise, the node will not be able to decipher the obfuscated content. More explicitly,
this means that the blocks can only appear on the right hand-side of the colon, and for string properties only.
