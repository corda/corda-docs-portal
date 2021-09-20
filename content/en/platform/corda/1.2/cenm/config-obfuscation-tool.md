---
aliases:
- /releases/release-1.2/config-obfuscation-tool.html
- /docs/cenm/head/config-obfuscation-tool.html
- /docs/cenm/config-obfuscation-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-config-obfuscation-tool
    parent: cenm-1-2-tools-index
    weight: 1050
tags:
- config
- obfuscation
- tool
title: Config Obfuscation Tool
---


# Config Obfuscation Tool



## Overview

The Config Obfuscation Tool allows users to obfuscate sensitive information in configuration files, such that the
data is protected at rest. The tool is an altered version of the config obfuscator used by Corda. There are two steps
a user shall take in order to make use of this tool:



* An obfuscated config file should be produced using the config obfuscation tool.
* The obfuscated config file should be passed as a command line argument when starting one of the services where the
obfuscation flag *needs* to be set.


The following subsections will explain in detail how each of these two steps should be performed.


## Using the Config Obfuscation Tool

The config obfuscation tool resides in the `configobfuscationtool.jar`. Fields in the config are obfuscated by
encapsulating the values to be obfuscated in a `<encrypt{...}>` block.

Using the identity manager configuration file as found in the **Enterprise Network Manager Quick Start Guide**, an
example of a plain text pre-obfuscation configuration file would be:

```docker
address = "localhost:10000"

database {
    driverClassName = org.h2.jdbcx.JdbcDataSource
    url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "<encrypt{example-db-password}>"
}

shell {
    sshdPort = 10002
    user = "testuser"
    password = "<encrypt{password}>"
}

localSigner {
    keyStore {
        file = corda-identity-manager-keys.jks
        password = "<encrypt{password}>"
    }
    keyAlias = "cordaidentitymanagerca"
    signInterval = 10000
    # This CRL parameter is not strictly needed. However if it is omitted then
    # revocation cannot be used in the future so it makes sense to leave it in.
    crlDistributionUrl = "http://"${address}"/certificate-revocation-list/doorman"
}

workflows {
    "issuance" {
        type = ISSUANCE
        updateInterval = 10000
        plugin {
            pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
        }
    }
}
```

A file can be obfuscated by running the following command:

```bash
java -jar configobfuscationtool.jar <config-file>
```

The config obfuscation tool does not overwrite the existing config file, but produces a new file with an “obfuscated”
label unless a new file name is explicitly specified. A user may specify the name of the newly generated obfuscated
file by setting the `-n` or `--new-file-name` flags followed by the new name.
For example, passing the plain text file `im-config.conf` into the config obfuscation tool absent any naming flag
would result in a newly generated obfuscated file named `im-config-obfuscated.conf`.


{{< warning >}}
The newly generated file will **overwrite** any existing file of the same name in the respective directory in which
the obfuscation tool is being run. Please use the naming flags in order to avoid any unwanted data loss.

{{< /warning >}}


Adding to the previous config example, the corresponding newly generated obfuscated config file would be:

```docker
address = "localhost:10000"

database {
    driverClassName = org.h2.jdbcx.JdbcDataSource
    url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "<{4W5WiK849jeRmtU6SQ4cwQ==:HnvFhgG29t3DohAI0VYhqwwxjeDJMIS2I5SeWr8VLaY/b8Q=}>"
}

shell {
    sshdPort = 10002
    user = "testuser"
    password = "<{I0cWBh/gyRYje6aBOJoOOA==:xQWs9bYVJ2A3sDtENaCdIbpeAMqaHzsE}>"
}

localSigner {
    keyStore {
        file = corda-identity-manager-keys.jks
        password = "<{/uLFgdlJYbGp4MDXUc8Odg==:x+OftT8pulIRWm4tGle1NY3AJpjOBaZB}>"
    }
    keyAlias = "cordaidentitymanagerca"
    signInterval = 10000
    # This CRL parameter is not strictly needed. However if it is omitted then
    # revocation cannot be used in the future so it makes sense to leave it in.
    crlDistributionUrl = "http://"${address}"/certificate-revocation-list/doorman"
}

workflows {
    "issuance" {
        type = ISSUANCE
        updateInterval = 10000
        plugin {
            pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
        }
    }
}
```

The config obfuscation tool should merely be used for obfuscating configs. The tool uses a hardware address
and a seed for deriving the key used for AES encryption. For the key derivation function PBKDF2 (with HMAC-SHA256)
is used. By default the hardware address corresponds to the MAC address of the machine on which the config obfuscation
tool is run. A machine-independent seed value is used at default. However, a user may pass in a custom hardware address
and/or seed value by running the following command:

```bash
java -jar configobfuscationtool.jar <config-file> --hardware-address <hardware-address> --seed <some-random-seed>
```

If one would like to print the obfuscated config file to console once it has been generated, the `-p` flag can be set when running the
tool.


## Running services with obfuscated configs

When using obfuscated config files for the Identity Manager, Network Map or Signing service, upon starting the
respective service one has to explicitly set the `-o` command line flag to indicate that the config has been
obfuscated.

An example of running a service with an obfuscated config file would be:

```bash
java -jar identitymanager.jar --config-file <im-config-obfuscated.conf> -o
```

Note that the above example only works for a config, which has been obfuscated using the default hardware address and
seed. If a config has been obfuscated using a custom seed, the respective value would have to be specified as a command
line argument.

For example, in the case of a custom seed, the following command would have to be run:

```bash
java -jar identitymanager.jar --config-file <im-config-obfuscated.conf> -o --seed <obfuscation-seed>
```

{{< note >}}
Each time an obfuscated config is passed as a command line argument to one of the services, the required
seed **needs** to be supplied if it was explicitly set for obfuscation.

{{< /note >}}
service in a cloud), the following example command shows how a custom MAC address can be specified:

```bash
java -jar identitymanager.jar --config-file <im-config-obfuscated.conf> -o --hardware-address 44:1C:8F:36:C2:A8
```
