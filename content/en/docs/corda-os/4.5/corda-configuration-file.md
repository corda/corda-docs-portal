---
aliases:
- /head/corda-configuration-file.html
- /HEAD/corda-configuration-file.html
- /corda-configuration-file.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-corda-configuration-file
    parent: corda-os-4-5-corda-nodes-index
    weight: 1030
tags:
- corda
- configuration
- file
title: Node configuration
---

# Node configuration

{{< warning >}}
If not specified in the node configuration file, `devMode` defaults to `True`. `devMode` must be disabled on all
production nodes.
{{< /warning >}}

## Configuration file location

When starting a node, the `corda.jar` file defaults to reading the node’s configuration from a `node.conf` file in the directory from which the command to launch Corda is executed.
There are two command-line options to override this behaviour:

* The `--config-file` command line option allows you to specify a configuration file with a different name, or in a different file location.
Paths are relative to the current working directory
* The `--base-directory` command line option allows you to specify the node’s workspace location.
A `node.conf` configuration file is then expected in the root of this workspace.

If you specify both command line arguments at the same time, the node will fail to start.

## Configuration file format

The Corda configuration file uses the HOCON format which is a superset of JSON. Please visit
[HOCON (Human-Optimized Config Object Notation)](https://github.com/typesafehub/config/blob/master/HOCON.md) on GitHub for further details.

Please do NOT use double quotes (`"`) in configuration keys.

Node setup will log `Config files should not contain " in property names. Please fix: [key]` as an error when it finds double quotes around keys.
This prevents configuration errors when mixing keys containing `.` wrapped with double quotes and without them e.g.: The property
`"dataSourceProperties.dataSourceClassName" = "val"` in [Reference.conf](#reference-conf) would be not overwritten by the property
`dataSourceProperties.dataSourceClassName = "val2"` in *node.conf*.

{{< warning >}}
If a property is defined twice the last one will take precedence. The library currently used for parsing HOCON
currently does not provide a way to catch duplicates when parsing files and will silently override values for the same key.
For example having `key=initialValue` defined first in node.conf and later on down the
lines `key=overridingValue` will result into the value being `overridingValue`.

{{< /warning >}}

By default the node will fail to start in presence of unknown property keys.
To alter this behaviour, the `on-unknown-config-keys` command-line argument can be set to `IGNORE` (default is `FAIL`).

{{< note >}}
As noted in the HOCON documentation, the default behaviour for resources referenced within a config file is to silently
ignore them if missing. Therefore it is strongly recommended to utilise the `required` syntax for includes. See HOCON documentation
for more information.

{{< /note >}}

## Overriding configuration values

### Placeholder Overrides

It is possible to add placeholders to the `node.conf` file to override particular settings via environment variables. In this case the
`rpcSettings.address` property will be overridden by the `RPC_ADDRESS` environment variable, and the node will fail to load if this
environment variable isn’t present (see: [Hiding sensitive data](node-administration.md#hiding-sensitive-data) for more information).

```groovy
rpcSettings {
  address=${RPC_ADDRESS}
  adminAddress="localhost:10015"
}
```

### Direct Overrides

It is also possible to directly override Corda configuration (regardless of whether the setting is already in the `node.conf`), by using
environment variables or JVM options. Simply prefix the field with `corda.` or `corda_`, using periods (`.`) or
underscores (`_`) to signify nested options. For example, to override the `rpcSettings.address` setting, you can override it via environment variables:

```shell
# For *nix systems:
export corda_rpcSettings_address=localhost:10015

# On Windows systems:
SET corda_rpcSettings_address=localhost:10015
SET corda.rpcSettings.address=localhost:10015
```

Or via JVM arguments:

```shell
java -Dcorda_rpcSettings_address=localhost:10015 -jar corda.jar
java -Dcorda.rpcSettings.address=localhost:10015 -jar corda.jar
```

Items in lists can be overridden by appending the list index to the configuration key. For example, the `jarDirs` setting can be
overridden via:

```shell
# via JVM arguments:
java -Dcorda.jarDirs.0=./libs -Dcorda.jarDirs.1=./morelibs -jar corda.jar
java -Dcorda_jarDirs_0=./libs -Dcorda_jarDirs_1=./morelibs -jar corda.jar

# or via environment variables

# for *nix systems:
export corda_jarDirs_0=./libs
export corda_jarDirs_1=./morelibs

# for Windows systems:
SET corda.jarDirs.0=./libs
SET corda.jarDirs.1=./morelibs
# or
SET corda_jarDirs_0=./libs
SET corda_jarDirs_1=./morelibs
```

#### Limitations

* If the same key is overridden by both an environment variable and system property, the system property takes precedence.
* Variables and properties are case sensitive. Corda will warn you if a variable
prefixed with `CORDA` cannot be mapped to a valid property. Shadowing occurs when two properties
of the same type with the same key are defined. For example having `corda.p2Aaddress=host:port` and `corda_p2Aaddress=host1:port1`
will raise an exception on startup. This is to prevent hard to spot mistakes.
* If an item in a list is overridden via an environment variable/system property, the whole list will be overridden. E.g., with a `node.conf`
containing:

```groovy
jarDirs=["./dir1", "./dir2", "./dir3"]
```

When Corda is started via:

```shell
java -Dcorda.jarDirs_0=./newdir1
```

The resulting value of `jarDirs` will be `["./newdir1"]`.

* You can’t override a populated list with an empty list. For example, when `devMode=false`, `cordappSignerKeyFingerprintBlacklist` is
pre-populated with Corda development keys. It isn’t possible to set this to an empty list via the commandline. You can however override
the list with an all zero hash which will remove the keys:

```shell
java -Dcorda.cordappSignerKeyFingerprintBlacklist.0="0000000000000000000000000000000000000000000000000000000000000000"
```

* Objects in lists cannot currently be overridden. For example the `rpcUsers` configuration key is a list of user objects, overriding these
via environment variables or system properties will not work.

## Configuration file fields

See [Configuration file fields](corda-configuration-fields.md).

## Reference.conf

A set of default configuration options are loaded from the built-in resource file `/node/src/main/resources/reference.conf`.
This file can be found in the `:node` gradle module of the [Corda repository](https://github.com/corda/corda).
Any options you do not specify in your own `node.conf` file will use these defaults.

Here are the contents of the `reference.conf` file:

```none
additionalP2PAddresses = []
crlCheckSoftFail = true
database = {
    transactionIsolationLevel = "REPEATABLE_READ"
    exportHibernateJMXStatistics = "false"
}
dataSourceProperties = {
    dataSourceClassName = org.h2.jdbcx.JdbcDataSource
    dataSource.url = "jdbc:h2:file:"${baseDirectory}"/persistence;DB_CLOSE_ON_EXIT=FALSE;WRITE_DELAY=0;LOCK_TIMEOUT=10000"
    dataSource.user = sa
    dataSource.password = ""
}
emailAddress = "admin@company.com"
flowTimeout {
    timeout = 30 seconds
    maxRestartCount = 6
    backoffBase = 1.8
}
jmxReporterType = JOLOKIA
keyStorePassword = "cordacadevpass"
lazyBridgeStart = true
rpcSettings = {
    useSsl = false
    standAloneBroker = false
}
trustStorePassword = "trustpass"
useTestClock = false
verifierType = InMemory

```

[reference.conf](https://github.com/corda/corda/blob/release/os/4.5/node/src/main/resources/reference.conf)

## Configuration examples

General node configuration file for hosting the IRSDemo services

```none
myLegalName = "O=Bank A,L=London,C=GB"
keyStorePassword = "cordacadevpass"
trustStorePassword = "trustpass"
crlCheckSoftFail = true
dataSourceProperties {
    dataSourceClassName = org.h2.jdbcx.JdbcDataSource
    dataSource.url = "jdbc:h2:file:"${baseDirectory}"/persistence"
    dataSource.user = sa
    dataSource.password = ""
}
p2pAddress = "my-corda-node:10002"
rpcSettings {
    useSsl = false
    standAloneBroker = false
    address = "my-corda-node:10003"
    adminAddress = "my-corda-node:10004"
}
rpcUsers = [
    { username=user1, password=letmein, permissions=[ StartFlow.net.corda.protocols.CashProtocol ] }
]
devMode = true

```

```none
myLegalName = "O=Notary Service,OU=corda,L=London,C=GB"
keyStorePassword = "cordacadevpass"
trustStorePassword = "trustpass"
p2pAddress = "localhost:12345"
rpcSettings {
    useSsl = false
    standAloneBroker = false
    address = "my-corda-node:10003"
    adminAddress = "my-corda-node:10004"
}
notary {
    validating = false
}
devMode = false
networkServices {
    doormanURL = "https://cz.example.com"
    networkMapURL = "https://cz.example.com"
}
```

Configuring a node where the Corda Compatibility Zone’s registration and Network Map services exist on different URLs

```none
myLegalName = "O=Bank A,L=London,C=GB"
keyStorePassword = "cordacadevpass"
trustStorePassword = "trustpass"
crlCheckSoftFail = true
dataSourceProperties {
    dataSourceClassName = org.h2.jdbcx.JdbcDataSource
    dataSource.url = "jdbc:h2:file:"${baseDirectory}"/persistence"
    dataSource.user = sa
    dataSource.password = ""
}
p2pAddress = "my-corda-node:10002"
rpcSettings {
    useSsl = false
    standAloneBroker = false
    address = "my-corda-node:10003"
    adminAddress = "my-corda-node:10004"
}
rpcUsers = [
    { username=user1, password=letmein, permissions=[ StartFlow.net.corda.protocols.CashProtocol ] }
]
devMode = false
networkServices {
    doormanURL = "https://registration.example.com"
    networkMapURL = "https://cz.example.com"
}

```

## Generating a public key hash

This section details how a public key hash can be extracted and generated from a signed CorDapp. This is required for a select number of
configuration properties.

Below are the steps to generate a hash for a CorDapp signed with a RSA certificate. A similar process should work for other certificate types.

* Extract the contents of the signed CorDapp jar.
* Run the following command (replacing the < > variables):

```none
openssl pkcs7 -in <extract_signed_jar_directory>/META-INF/<signature_to_hash>.RSA -print_certs -inform DER -outform DER \
| openssl x509 -pubkey -noout \
| openssl rsa -pubin -outform der | openssl dgst -sha256
```

* Copy the public key hash that is generated and place it into the required location (e.g. in `node.conf`).
