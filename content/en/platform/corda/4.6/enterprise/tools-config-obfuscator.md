---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-configuring
tags:
- tools
- config
- obfuscator
title: Configuration Obfuscator
weight: 70
---

# Configuration Obfuscator

The purpose of the Configuraton Obfuscator tool is to obfuscate sensitive information in configuration files.

The Configuration Obfuscator makes node installation less vulnerable to someone trawling plain text files, searching for passwords and credentials of resources that they should not have access to in the first place.

{{< warning >}}
Although the Configuration Obfuscator does protect the node against trawling attacks, it does not ensure that password protection is completely secure. For improved security, always use the [latest released version](https://docs.corda.net/docs/corda-enterprise/tools-config-obfuscator.html) of the tool.
{{< /warning >}}

{{< note >}}
The Configuraton Obfuscator tool can only be used with configuration files for Corda Enterprise 4.4 (and above) nodes, Corda Firewall, and Corda Network Enterprise Manager (CENM) 1.3 (and above) services. Corda configuration files obfuscated with older versions of Corda Enterprise can still be deobfuscated by Corda Enterprise 4.4 and above. Configuration files obfuscated with CENM 1.1 and 1.2 can be deobfuscated with CENM 1.3 (and above), but further obfuscation must be done using the new version of the Configuration Obfuscator tool.
{{< /note >}}

## How obfuscation works

You obfuscate a configuration file using the Configuration Obfuscation tool. In the example below, the `user` and `password` properties are encrypted by placing them in this format: `"<encrypt{your-secret-database-password}>"`.


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

The tool takes a seed and a passphrase as input to obfuscate a given configuration file.

{{< note >}}
To deobfuscate that configuration file, you must provide the same seed and passphrase to any process that accepts obfuscated configurations. For example, when starting a node.
{{< /note >}}

## How deobfuscation works

You deobfuscate an obfuscated configuration file by starting the respective node, Firewall component, or service (for example, a [Corda Enterprise Network Manager service](https://docs.corda.net/docs/cenm/index.html)).

You cannot use the Configuration Obfuscator tool to deobfuscate an obfuscated file directly. This is intentional in order to prevent a potential security risk where plain text passwords could be revealed by just running the tool again.

The node or service itself deobfuscates the configuration object internally on startup, taking the same seed and passphrase as the Configuration Obfuscator tool. The 'Deobfuscate an obfuscated configuration file' section further below describes how to do that.

## Obfuscate using the command-line tool

The command-line tool is included in Corda Enterprise as a `.jar` file with a name `corda-tools-config-obfuscator-<version>.jar`, where `<version>` stands for the Corda Enterprise version (for example, `corda-tools-config-obfuscator-4.6.jar` or `corda-tools-config-obfuscator-4.6.jar`).

### Usage

The paramaters, options, and commands that you can use when running the command-line tool, are shown below.

```bash
config-obfuscator [-hiV] [--config-obfuscation-passphrase[=<cliPassphrase>]]
                  [--config-obfuscation-seed[=<cliSeed>]] [-w[=<writeToFile>]]
                  [--logging-level=<loggingLevel>] CONFIG_FILE
                  [HARDWARE_ADDRESS]
```

### Input parameters

The command-line tool takes following parameters as input:

* `CONFIG_FILE` is the name of the configuration file to obfuscate. This is a mandatory parameter.
* `--config-obfuscation-passphrase[=<cliPassphrase>]` is the passphrase used in the key derivation function when generating an AES key. Leave blank to provide input interactively.
* `--config-obfuscation-seed[=<cliSeed>]` is the seed used in the key derivation function to create a salt. Leave blank to provide input interactively.
* `[HARDWARE_ADDRESS]` is the primary hardware address of the machine on which the configuration file resides. By default, the MAC address of the running machine is used - to explicitly use that, set the value to `DEFAULT`. Note that this parameter provides backwards compatibility but should not be used in cases where backwards compatibility is not required. This is an optional parameter.

### Input options

The following options are available when running the command-line tool:

* `-v, --verbose, --log-to-console` is an option to print logging to the console as well as to a file.
* `--logging-level=<loggingLevel>` is an option to enable logging at this level or higher. The possible values for `<loggingLevel>` are `ERROR` (default), `WARN`, `INFO`, `DEBUG`, and `TRACE`.
* `-w=[<writeToFile>]` is a flag to indicate that the tool should write the obfuscated output to disk, using the same file name as the input (if left blank and provided at the end of the command line), or the provided file name.
* `-i` is a flag, which if set, says to provide input to obfuscated fields interactively.
* `-h`, `--help` is a flag used to show this help message and exit.
* `-V`, `--version` is a flag used to print version information and exit.


{{< note >}}
By default, the command-line tool only prints out the transformed configuration to the terminal for verification. To persist the changes, you must use the `-w` flag, which ensures that the obfuscated content gets written back into the provided configuration file.

The `-w` flag also takes an optional file name for cases where you need to write the result back to a different file. If you are not providing the optional file name, you must put the `-w` flag at the end of the command.

An example of these two cases follows below:

```bash
# Explicit output file provided
$ java -jar corda-tools-config-obfuscator-4.6.jar -w node.conf node_template.conf

# No output file provided
$ java -jar corda-tools-config-obfuscator-4.6.jar node_template.conf -w
```
{{< /note >}}


### Input commands

You can use the following command to install 'alias' and 'autocompletion' for `bash` and `zsh`:

`install-shell-extensions`

For example:

```bash
$ java -jar corda-tools-config-obfuscator-4.6.jar install-shell-extensions
```

### How to pass the seed and passphrase to the Obfuscation Tool using the command-line tool options

As described above, the command-line tool takes a seed and a passphrase as input parameters, and uses them to derive a 256bit AES encryption key.

* The option (flag) for the seed is `--config-obfuscation-seed[=<cliSeed>]`.
* The option (flag) of the passphrase is `--config-obfuscation-passphrase[=<cliPassphrase>]`.

If you provide a value in your command, that value is treated as the seed/passphrase. Otherwise, you are prompted to provide the seed/passphrase in the command prompt.

{{< warning >}}
For backwards compatibility reasons, it is possible to run the tool without passing the seed and passphrase - in that case, the tool uses default seed and passphrase values.
However, we strongly recommend that you always set the seed and passphrase in order to obfuscate configuration files in the most secure way.
{{< /warning >}}

The following example shows a run of the command-line tool with a seed and a passphrase passed explicitly:

```bash
$ java -jar tools/config-obfuscator/build/libs/corda-tools-config-obfuscator-4.6.jar --config-obfuscation-seed my-seed --config-obfuscation-passphrase my-passphrase -w node.conf /p/tmp/node-non-obfuscated.conf
```

The following example shows a run of the command-line tool with the seed and passphrase values left blank - the user is prompted to provide these interactively:

```bash
$ java -jar tools/config-obfuscator/build/libs/corda-tools-config-obfuscator-4.6.jar --config-obfuscation-seed --config-obfuscation-passphrase -w node.conf /p/tmp/node-non-obfuscated.conf
$ Enter value for --config-obfuscation-seed (The seed used in the key derivation function to create a salt):
$ Enter value for --config-obfuscation-passphrase (The passphrase used in the key derivation function when creating an AES key):
```

### Example of an obfuscated node configuration file

```json
p2pAddress="localhost:10005"
rpcSettings {
  address="localhost:10006"
  adminAddress="localhost:10015"
}
security {
  authService {
    dataSource {
      type=INMEMORY
      users=[
        {
          password="<encrypt{my-pass}>"
          permissions=[
            ALL
          ]
          user=bankUser
        }
      ]
    }
  }
}
```

## Obfuscate using environment variables

Another way to provide the seed and passphrase to obfuscate a configuration file is to set the following environment variables:

* `CONFIG_OBFUSCATION_SEED`
* `CONFIG_OBFUSCATION_PASSPHRASE`

{{< note >}}
If you use both command-line options and environment variables to pass the seed and passphrase, the command-line options take precedence.
{{< /note >}}

{{< note >}}
The same environment variables are used by all components that use the Configuration Obfuscator tool.
{{< /note >}}

### How to pass the seed and passphrase to the Obfuscation Tool using environment variables

```bash
$ export CONFIG_OBFUSCATION_SEED=my-seed; export CONFIG_OBFUSCATION_PASSPHRASE=my-passphrase; java -jar tools/config-obfuscator/build/libs/corda-tools-config-obfuscator-4.6.jar -w node.conf /p/tmp/node-non-obfuscated.conf
```

## Deobfuscate an obfuscated configuration file

You deobfuscate an obfuscated configuration file by starting the respective node, Firewall component, or service (for example, a [Corda Enterprise Network Manager service](https://docs.corda.net/docs/cenm/index.html)).

When you need your node, Firewall component, or service, to deobfuscate an obfuscated configuration file, you must pass them the same seed and passhprase used when that configuration file was deobfuscated. There are two ways you can do that, as described below.

### How to pass the seed and passphrase to a node, Firewall component, or service, using the command-line tool options

To pass the obfuscation seed and passphrase to a node or Firewall component using the command-line tool, use the `--config-obfuscation-seed` and `--config-obfuscation-passphrase` flags, respectively, in your node, Firewall, or service run command.

These flags are the same for all components that use the Configuration Obfuscator tool.

The following example shows how to pass a seed and a passphrase explicitly to a node component using the command-line tool:

```bash
$ java -jar corda.jar --config-obfuscation-seed my-seed --config-obfuscation-passphrase my-passphrase

```
The following example shows how to pass a seed and a passphrase to a node component using the command-line tool by leaving the flag values blank to invoke a prompt:

```bash
$ java -jar corda.jar --config-obfuscation-seed --config-obfuscation-passphrase
$ Enter value for --config-obfuscation-seed (The seed used in the key derivation function to create a salt):
$ Enter value for --config-obfuscation-passphrase (The passphrase used in the key derivation function when creating an AES key):
```

### Pass the seed and passphrase to a node, Firewall component, or service, using environment variables

```bash
$ export CONFIG_OBFUSCATION_SEED=my-seed; export CONFIG_OBFUSCATION_PASSPHRASE=my-passphrase; java -jar corda.jar
```

## Configuration directives

The configuration directives described below can be placed arbitrarily within 'string' properties in the target configuration file, with a maximum of one per line.

{{< note >}}
Obfuscated passwords are unique to the configuration field they came from. You cannot use the same obfuscation of a password for multiple fields, even if they use the same password. In other words, once a password has been obfuscated, you cannot copy and paste the obfuscated version into different fields - the password will not be accepted.
{{< /note >}}

For example:

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

### Directive to indicate obfuscation areas

To indicate parts of the configuration that should be obfuscated, you can place text markers in the form `<encrypt{...}>`. For example:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "<encrypt{testpassword}>",
  // (...)
}
```

{{< note >}}
If your configuration file uses `include` directives, as shown below, then the referenced file is automatically imported and obfuscated with the main file. The result will contain both the main file and the `include` file in the output:

`include "path/to/file.conf"`
`include required("path/to/file.conf")`

Each `include` statement must be on a single line and follow the format shown above.

{{< /note >}}

The example below shows how this area of the configuration file will look like after it is run through the obfuscation tool:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "<{8I1E8FKrBxVkRpZGZKAxKg==:oQqmyYO+SZJhRkPB7laNyQ==}>",
  // (...)
}
```

### Deobfuscation based on configuration directives

When the Corda node, Firewall component, or service is run with the correct seed/passphrase provided, the configuration is deobfuscated on the fly and interpreted as shown in the example below:

```json
{
  // (...)
  "p2pAddress": "somehost.com:10001",
  "keyStorePassword": "testpassword",
  // (...)
}
```

### Limitations

The `<encrypt{}>` blocks can only appear inside 'string' properties - they cannot be used to obfuscate entire configuration blocks.

Otherwise, the Corda node or service will not be able to decipher the obfuscated content.

More explicitly, this means that the blocks can only appear on the right-hand side of the colon, and for 'string' properties only.
