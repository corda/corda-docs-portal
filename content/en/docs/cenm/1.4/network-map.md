---
aliases:
- /network-map.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-network-map
    parent: cenm-1-4-operations
    weight: 140
tags:
- network
- map
title: Network Map Service
---


# Network Map Service



## Purpose

The Network Map Service acts as a directory for all participants on the network. It is responsible for recording
essential information of each participant such as connection address and available services. See
[Network Map Overview](network-map-overview.md) for an in-depth explanation.


## Running The Network Map Service

The Network Map Service currently has to be initialised in two stages. First, the network parameters for the global
network have to be loaded into the database. Once complete, the service can be started.
As of CENM 1.3, the initial bootstrap is managed via the Zone Service for the
network, along with the Angel Service of the Network Map Services. Service
restarts are handled automatically.

{{< warning >}}
**The Network Map Service cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.**
{{< /warning >}}


### Setting the Network Parameters

{{< warning >}}
The options below have been replaced with the Admin RPC commands.
They are listed here for reference only and will be removed in a future release of CENM.
{{< /warning >}}

The initial network parameters file can be loaded into the Network Map Service database using the
`--set-network-parameters` flag. The complete list of flags required to set the network parameters is as follows:


* **[–set-network-parameters] or [-s]**:
This flag specifies that you wish to set or update the network parameters, and
should be followed by the new network parameters configuration file.
* **[–network-truststore] or [-t]**:
This is used to define the network trustStore, which should contain the root
certificate (similar to the *network-root-truststore.jks* file for Corda nodes). This is needed to validate that the
notaries that have been set in the network parameters have a valid certificate issued by the Identity Manager.
* **[–truststore-password] or [-p]**:
The password for the above trustStore.
* **[–root-alias] or [-a]**:
The alias for the root certificate within the above trustStore.

An example of setting the network parameters is:

```bash
java -jar network-map-<VERSION>.jar --config-file <CONFIG_FILE> \
--set-network-parameters <NETWORK_PARAMS_CONFIG_FILE> \
--network-truststore <NETWORK_ROOT_TRUSTSTORE_FILE> \
--truststore-password <TRUSTSTORE_PASSWORD> \
--root-alias <ROOT_ALIAS>
```

The server will terminate once this process is complete. Upon completion the following message should be displayed:

```kotlin
Saved initial network parameters to be signed:
...
```

### Starting The Network Map Service

Once you have set the network parameters, you can start the Network Map Service
manually by running the following command:

```bash
java -jar network-map-<VERSION>.jar --config-file <CONFIG_FILE>
```

Optional parameter:

```bash
--working-dir=<DIR>
```

This will set the working directory to the specified folder. The service will look for files in that folder. This means
certificates, configuration files etc. should be under the working directory.
If not specified it will default to the current working directory (the directory from which the service has been started).


## Configuration

Similar to the Identity Manager the main elements that need to be configured for the Network Map Service are:


* [Address](#address)
* [Database](#database)
* [Embedded shell (optional)](#embedded-shell-optional)
* [Network Data Signing Mechanism](#network-data-signing-mechanism)
* [Cache Timeout](#cache-timeout)
* [Node Certificate Revocation Checking](#node-certificate-revocation-checking)
* [CENM Internal Server](#cenm-internal-server)
* [Identity Manager & Revocation Communication](#identity-manager-revocation-communication)
* [Restricting A Node’s Corda Version (optional)](#restricting-a-node-s-corda-version-optional)
* [Admin RPC Interface](#admin-rpc-interface)

{{< note >}}
See [Network Map Configuration Parameters](config-network-map-parameters.md) for a detailed explanation about each possible parameter.
{{< /note >}}

### Address

The `address` parameter must be included in the top level of the configuration and represents the host and port
number that the Network Map Service will bind to upon start-up. The host can either be the IP address or the hostname of
the machine that Network Map Service is running on. For example:

```guess
address = "<SERVER_IP/SERVER_HOST>:<PORT_NUMBER>"
```

{{< note >}}
Depending on the configuration of your deployment the host may be different to the external IP/DNS name that
other nodes will use to connect to the service. The service needs to be able to bind to this host and port.
For example, in a cloud environment with the machine inside a “virtual network”, the host in the configuration
may need to be the private IP address, whilst external nodes would use the machines external IP/DNS name to
connect to Network Map.

{{< /note >}}

### Database

The Network Map Service is backed by a SQL database which it uses to store the network map along with node infos. The
connection settings must be included within the `database` configuration block in the configuration file. The main options
that should be included here are:


* `driverClassName` - the database driver class name (e.g *com.microsoft.sqlserver.jdbc.SQLServerDriver* for Microsoft SQL Server, *org.postgresql.Driver* for postgres)
* `jdbcDriver` - the path to the appropriate JDBC driver `.jar` (e.g *path/to/mssql-jdbc-7.2.2.jre8.jar*)
* `url` - the connection string for the database
* `user` - the username for the database
* `password` - the password for the database


#### Database Setup

The database can either be setup prior to running the Network Map Service or, alternatively, it can be automatically
prepared on start-up via the built-in migrations. To enable the running of database migrations on start-up set the
`runMigration` parameter within the `database` configuration to true.

If the Network Map Service is being run using the same database instance as the Identity Manager Service then the Network Map
schema name must be specified via the `schema` parameter within the `database` configuration block:

```guess
database {
    ...
    runMigration = true
    schema = networkmap
}
```

{{< note >}}
Due to the way the migrations are defined, if the Identity Manager and Network Map Services are using the same
database instance then they *must* use separate database schemas. For more information regarding the supported databases
along with the schema see [CENM Databases](database-set-up.md).

{{< /note >}}

#### Additional Properties

Additional database properties can be loaded by including an optional *additionalProperties* configuration block. In CENM 1.0
these are restricted to HikariCP configuration settings.

```guess
database {
    ...
    additionalProperties {
        connectionTimeout = 60000
        maxLifetime = 3200000
        poolName = "myPool123"
    }
}
```


#### Example

An example configuration for a Network Map Service using a Microsoft SQL Service database, configured to run the
migrations on start-up is:

```guess
database {
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    jdbcDriver = "path/to/mssql-<EXAMPLE_JDBC_DRIVER>.jar"
    url = "jdbc:sqlserver://<EXAMPLE_CONNECTION_STRING>"
    user = "example-user"
    password = "example-password"
    schema = "network-map"
    runMigration = true
    database {
        additionalProperties {
            connectionTimeout = 60000
            maxLifetime = 3200000
            poolName = "myPool123"
        }
    }
}
```


### Embedded shell (optional)

See [Shell Configuration](shell.md#shell-config) for more information on how to configure the shell.


### Network Data Signing Mechanism

Before any changes to the network data (e.g. Network Map or Network Parameter updates) can be broadcast to the
participants on the network, they first need to be signed. Similarly to the Identity Manager, there are currently two
mechanisms for this:


* Local Signing Service
* External Signing Service


#### Local Signing Service

The local signing service is recommended for testing and toy environments. Given a local key store containing the
relevant signing keys, it provides the functionality to automatically sign all approved Network Map and Parameter
updates on a configured schedule. No human interaction is needed and the credentials for the key stores have to be
provided upfront. The service is an integrated signer that is a cut-down version of the standalone
[Signing Services](signing-service.md) and provides no HSM integration or ability to manually verify changes. It is strongly recommended
against using this for production environments.

In order for the local signer to function, it needs to be able to access Network Map’s certificate and keypair
which should have been previously generated (see [Certificate Hierarchy Guide](pki-guide.md) for more information). The local signer uses local
key stores which should include the necessary signing keys along with their full certificate chains.

To enable the local signer, the top level `localSigner` configuration block should be added to the configuration file:

```guess
localSigner {
    keyStore {
        file = exampleKeyStore.jks
        password = "example-keystore-password"
    }
    keyAlias = "example-key-alias"
    keyPassword = "example-key-password" # optional - defaults to key store password
    signInterval = 15000 # signing interval in millis
}
```

In this example, the key store defined within the local signer should contain the Network Map’s key pair used for
signing any network map or parameter changes along with the full certificate chain back to the root of the network.


#### External Signing Service

The production grade signing mechanism is the external [Signing Services](signing-service.md). This has all the functionality of the
integrated local signer as well as HSM integration and the ability for a user to interactively verify and sign incoming
network map or parameter changes. It should be used in all production environments where maximum security and validation
checks are required.

In order to retrieve the network map and parameter data, the signing service will communicate with the Network Map
service via its [CENM internal server](#cenm-internal-server). This is the only configuration option that is needed if signing is being done
via the external signing service.


### Cache Timeout

The Network Map Service configuration contains a single required top-level parameter `pollingInterval`. This
determines how often the server should poll the database for newly signed network map and parameter changes. It also
determines how often nodes should poll the Network Map Service for a new network map (by including this value in the
HTTP response header).

It takes a numerical value and represents the number of milliseconds between each refresh. An example of how this should
be added to the configuration file is:

```guess
...
pollingInterval = 600000
...
```


### Node Certificate Revocation Checking

In cases when the certificate revocation list infrastructure (See [Certificate Revocation List](certificate-revocation.md) for more information)
is provided, the additional validation for the node’s certificates can be enabled in the Network Map Service. This is
achieved via the top-level `checkRevocation` flag set in the configuration file. This ensures that any node within the
Network Map has a valid, trusted certificate.

Setting this flag will result in the nodes legal identities certificate paths being validated against the certificate
revocation lists whenever the Network Map is updated. Any node that has a revoked certificate will be removed from the
Network Map. The certificates are also checked when the node submits its information to the Network Map Service to
publish for the first time.

An example of how this should be added to the configuration file is:

```guess
...
checkRevocation = true
...
```

{{< note >}}
Enabling this option requires communication with the Revocation service to be configured (See
[Identity Manager & Revocation Communication](#identity-manager-revocation-communication) below)

{{< /note >}}

### CENM Internal Server

To enable communication between the Network Map Service and other network management services, such as Revocation and
Identity Manager servers, upon start up the Network Map Service will create an internal long running listening server.
The configuration block `enmListener` can be used to define the properties of this
listener, such as the port it listens on as well as the retrying and logging behaviour.

```guess
...
enmListener {
    port = 5050
    reconnect = true
}
...
```

{{< note >}}
The `reconnect` parameter is optional - it will default to `reconnect = true` if not set.
{{< /note >}}

{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the CENM services to use SSL](enm-with-ssl.md).
{{< /note >}}


### Admin RPC Interface

To enable the CENM Command-Line Interface (CLI) tool to send commands to the Network Map Service,
you must enable the RPC API by defining a configuration block called `adminListener`.
The configuration block `adminListener` is used to define the properties of this
listener, such as the port it listens on as well as the retrying and logging behaviour.
For example, add the following to the service configuration:

```guess
...
adminListener {
    port = 5050
    reconnect = true
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}
...
```

{{< note >}}
The `reconnect` parameter is optional - it will default to `reconnect = true` if not set.
{{< /note >}}

{{% important %}}
If the `adminListener` property is present in the configuration, this means that the service must only be used via Admin RPC. In this case, the `shell` configuration property will be disabled. The `shell` and `adminListener` properties cannot be used in the configuration at the same time.
{{% /important %}}

The admin RPC interface requires an Auth Service to verify
requests, which must be configured below in a `authServiceConfig` block. Typically
this is provided automatically by the Zone Service (via an Angel Service),
however an example is provided below for reference:

```guess
authServiceConfig {
    host = <auth service host>
    port = <auth service port>
    trustStore = {
        location = /path/to/trustroot.jks
        password = <key store password>
    }
    issuer = <issuer>
    leeway = <leeway duration>
}
```

### Identity Manager & Revocation Communication


{{< warning >}}
Private network functionality was an internal feature that has been disabled from CENM 1.2 and above.
Running a network with one or more private networks is not a supported configuration.

{{< /warning >}}


The Network Map Service may need to speak to both the Identity Manager and Revocation services. For example, the Network
Map service may need to communicate with the Revocation service for CRL related information.
This is configured via the `identityManager` and `revocation` configuration options within the `networkMap`
configuration block:

```guess
...
identityManager {
    host = <IDENTITY_MANAGER_HOST> # e.g. identity-manager-url.com
    port = <IDENTITY_MANAGER_LISTENER_PORT>
}
revocation {
    host = <REVOCATION_HOST> # e.g. identity-manager-url.com
    port = <REVOCATION_LISTENER_PORT>
}
...
```

The `host` should correspond to the host part of the `address` value in the Identity Manager configuration. The
`port` parameter for each service should correspond with the `port` value within the `enmListener` configuration block in
the service’s configuration. See [Network Map Configuration Parameters](config-network-map-parameters.md) for more information.

You can also use the optional `timeout` parameter that enables you to set specific Network Map Service timeouts for communication to the Identity Manager and Revocation services. This allows for high node count network maps to operate at reliable performance levels. The `timeout` value is set in milliseconds and the default value is 10000 milliseconds. For example:

```guess
...
identityManager {
    host = <IDENTITY_MANAGER_HOST> # e.g. identity-manager-url.com
    port = <IDENTITY_MANAGER_LISTENER_PORT>
    timeout = 12000
}
revocation {
    host = <REVOCATION_HOST> # e.g. identity-manager-url.com
    port = <REVOCATION_LISTENER_PORT>
    timeout = 10000
}
...
```

{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the CENM services to use SSL](enm-with-ssl.md)

{{< /note >}}

### Restricting A Node’s Corda Version (optional)

The optional tpo-level configuration `versionInfoValidation` can be added to the configuration to exclude nodes
running an old version of Corda from successfully publishing their node info to the network map. The configuration
parameter `minimumPlatformVersion` represents the minimum platform version that a node has to be running to be able to
successfully publish. If this is set, then any node that attempts to publish its node info whilst running a version of
Corda with a platform version less than this will be automatically rejected. This can be used to ensure that all nodes
that join the network have access to certain features.

{{< note >}}
This serves a similar purpose to the *minimumPlatformVersion* within the network parameters and also within
the Identity Manager Service configuration. Publishing of the node info is the second step to joining the
network, after obtaining a certificate from the Identity Manager, so this option provides another gate of
security and peace of mind to the network operator.

{{< /note >}}
```guess
...
versionInfoValidation {
    minimumPlatformVersion = 4
}
...
```

{{< note >}}
Sending of version info during registration was added to Corda OS in release version 3.3. Using this approach
with a minimum version less than this will not work unless the nodes are running a modified code base.

{{< /note >}}
{{< note >}}
The minimum version configuration options should, in general, be kept consistent between the Identity Manager
and Network Map Service

{{< /note >}}

### Admin RPC
To use the RPC API in the Network Map Service, you must define a configuration property called `adminListener`.
Example:
```docker
adminListener = {
    port = 10000
    reconnect = true
    ssl {
        keyStore {
            location = exampleSslKeyStore.jks
            password = "password"
        }
        trustStore {
            location = exampleSslTrustStore.jks
            password = "trustpass"
        }
    }
}
```

{{% important %}}
If the `adminListener` property is present in the configuration, this means that the service must only be used via Admin RPC. In this case, the `shell` configuration property will be disabled. The `shell` and `adminListener` properties cannot be used in the configuration at the same time.
{{% /important %}}

### Example Configuration

```docker
address = "localhost:20000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./network-map-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
    runMigration = true
}

pollingInterval = 10000


localSigner {
    keyStore {
        file = exampleKeyStore.jks
        password = "example-password"
    }
    keyAlias = "example-key-alias"
    signInterval = 15000
}

enmListener {
    port = 20001
}

checkRevocation = false

shell {
  sshdPort = 20002
  user = "testuser"
  password = "example-password"
}

```


## Network Parameters

Along with the above configuration, a *network-parameters* configuration file also needs to be created. This defines the
basic settings for communication across the network along with references to the notaries node info files. Therefore it
is advisable to register the notaries with the Identity Manager Service and generate their node info files prior to
starting the network map.

The network parameters should contain reference to the notaries node info files. The notary node info files should be
copied over to the Network Map Service.


### Example Network Parameters File

```guess
notaries : [
    {
        notaryNodeInfoFile: "/Path/To/NodeInfo/File1"
        validating: true
    },
    {
        notaryNodeInfoFile: "/Path/To/NodeInfo/File2"
        validating: false
    }
]
minimumPlatformVersion = 1
maxMessageSize = 10485760
maxTransactionSize = 10485760
whitelistContracts = {
    cordappsJars = [
        "/Path/To/CorDapp/JarFile1",
    ],
    exclude = [
        "com.cordapp.contracts.ContractToExclude1",
    ]
}
eventHorizonDays = 30 # Duration in days
packageOwnership = [
    {
        packageName = "com.megacorp.example.claimed.package",
        publicKeyPath = "/example/path/to/public_key_rsa.pem",
        algorithm = "RSA"
    },
    {
        packageName = "com.anothercorp.example",
        publicKeyPath = "/example/path/to/public_key_ec.pem",
        algorithm = "EC"
    }
]
```


## Node’s host IP address

The Network Map Service provides an endpoint that can be used to determine the IP address of the querying host. This is
useful especially when dealing with node’s deployment in environments with IP address translation.


{{< table >}}

|GET|/network-map/my-hostname|Returns the IP address of the requestor.|

{{< /table >}}


## Obfuscated configuration files

To view the latest changes to the obfuscated configuration files, see [Obfuscation configuration file changes](obfuscated-config-file-changes.md).

{{< note >}}
You should not obfuscate the Network Parameters configuration file as it is not yet supported.
{{< /note >}}
