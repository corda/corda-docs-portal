---
aliases:
- /releases/release-1.0/network-map.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-network-map
    parent: cenm-1-0-operations
    weight: 140
tags:
- network
- map
title: Network Map Service
---


# Network Map Service



## Purpose

The network map service acts as a directory for all participants on the network. It is responsible for recording
essential information of each participant such as connection address and available services. See
[Network Map Overview](network-map-overview.md) for an in-depth explanation.


## Running The Network Map Service

The network map service currently has to be initialised in two stages. First, the network parameters for the global
network have to be loaded into the database. Once complete, the service can be started.


### Setting the Network Parameters

The initial network parameters file can be loaded into the network map service database using the
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


* **[–ignore-migration]**: 
Required for fresh deployments (not an upgrade that involves migrating data across).



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

The network map service can now be started via:

```bash
java -jar network-map-<VERSION>.jar --config-file <CONFIG_FILE>
```


## Configuration

Similar to the Identity Manager the main elements that need to be configured for the network map service are:


* [Address](#address)
* [Database Properties](#database-properties)
* [Certificate Signing Mechanism](#certificate-signing-mechanism)
* [Cache Timeout](#cache-timeout)
* [Node Certificate Revocation Checking](#node-certificate-revocation-checking)
* [Embedded Shell (optional)](#embedded-shell-optional)
* [Restricting A Node’s Corda Version (optional)](#restricting-a-node-s-corda-version-optional)
* [Identity Manager & Revocation Communication](#identity-manager-revocation-communication)


### Address

The `address` parameter must be included in the top level of the configuration. This represents the host and port number that other nodes will use to connect to it.
For example:

```guess
address = "<SERVER_IP/SERVER_HOST>:<PORT_NUMBER>"
```


### Database Properties

The Network Map service is backed by a SQL database which it uses to store the network map along with node infos. The
connection settings must be included within the `dataSourceProperties` configuration in the config file.


#### Database Setup

The database can either be setup prior to running the Network Map service or, alternatively, it can be automatically
prepared on startup via the built-in migrations. To enable the running of database migrations on startup set the
`runMigration` parameter within the `database` configuration to true.

If the Network Map service is being run using the same DB instance as the Identity Manager service then the Network Map
schema name must be specified via the `schema` parameter within the `database` configuration block:

```guess
database {
    runMigration = true
    schema = networkmap
}
```

{{< note >}}
Due to the way the migrations are defined, the services *must* use separate DB schemas (either in the same DB
instance or in completely separate instances). For more information regarding the supported databases along
with the schema see [ENM Databases](database-set-up.md).

{{< /note >}}

#### Example

An example configuration for a Network Map service using a local h2 database, configured to run the migrations on
startup is:

```guess
dataSourceProperties {
  dataSourceClassName = org.h2.jdbcx.JdbcDataSource
  "dataSource.url" = "jdbc:h2:file:<LOCAL_DB_FILE>;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT="<H2_PORT>
  "dataSource.user" = <USERNAME>
  "dataSource.password" = <PASSWORD>
}

database {
    runMigration = true
}
```


### Certificate Signing Mechanism

Any changes to the network parameters and network map need to be signed by the network map service before they can be
downloaded by the participants on the network. Similarly to the Identity Manager , there are currently two mechanisms
for this:


* Local Signing Service
* External Signing Service


#### Local Signing Service

The Network Map service has the ability to use a local signing service to sign approved network map and parameter
changes. This is an integrated signer that is a cut-down version of the standalone [Signing Service](signing-service.md) and provides
no HSM integration or ability to manually verify changes. It should therefore only be used for testing and toy
environments. The local signing service will

In order for the local signer to function, it needs to be able to access Network Map’s certificate and keypair which
should have been previously generated (see certificate-hierarchy-generation for more information). Any
certificate issued by the Identity Manager will include a certificate chain that links the issued certificate back to
the network root certificate. Hence the local signer also needs access to a certificate store, defined by the
`certificatesStoreFile` and `certificatesStorePassword` configuration parameters. See
tool-certificate-hierarchy-generator for more information on generating this.

To enable the local signer, the following should be added to the config file:

```guess
..
certificatesStoreFile = <PATH_TO_CERT_STORE>
certificatesStorePassword = <CERT_STORE_PASSWORD>
..

networkMap {
    ...
    localSigner {
        keyStore {
            file = <PATH_TO_KEYSTORE>
            password = <KEYSTORE_PASSWORD>
        }
        keyAlias = <KEY_ALIAS>
        keyPassword = <KEY_PASSWORD>
        signInterval = <SIGN_INTERVAL>
    }
    ...
}
```

The key store defined within the local signer should contain the Network Map’s key pair used for signing network
parameters. The certificate store file should contain all certificates in the chain from Network Map back to the root of
the network.


#### External Signing Service

The production grade signing mechanism is the external [Signing Service](signing-service.md). This has all the functionality of the
integrated local signer as well as HSM integration and the ability for a user to interactively verify and sign network
map and parameter changes. It should be used in all production environments where maximum security and validation checks
are required.

In order to retrieve the network map and parameter data, the signing service will communicate with the Network Map
service via its [ENM internal server](#enm-internal-server). This is the only configuration option that is needed if signing is being done
via the external signing service.


### Cache Timeout

The network map service configuration contains a single required parameter `cacheTimeout`. This determines how often the server should poll the database for newly signed
network map changes. It also determines how often nodes should poll the network map service for a new network map (by including this value in the HTTP response header).

An example of how this should be added to the config file is:

```guess
networkMap {
    cacheTimeout = 600000
    ...
}
```


### Node Certificate Revocation Checking

In cases when the certificate revocation list infrastructure (See [Certificate Revocation List (CRL)](certificate-revocation.md) for more information)
is provided, the additional validation for the node’s certificates can be enabled in the Network Map service. This is
achieved via the `checkRevocation` flag set in the configuration file. This ensures that any node within the Network
Map has a valid, trusted certificate.

Setting this flag will result in the nodes legal identities certificate paths being validated against the certificate
revocation lists whenever the Network Map is updated. The certificates are checked when the node first submits its node
information to the Network Map service for publish, and also whenever the Network Map is rebuilt and signed.

When a new Network Map is built and signed, any node infos with revoked certificates need to be filtered out. As a
result, certificate revocation checking requires communication with the revocation service. This should be configured
within via `revocation` parameter within the `networkMap` configuration block.

An example of how this should be added to the config file is:

```guess
networkMap {
    checkRevocation = true
    revocation {
        host = <REVOCATION_HOST>
        port = <REVOCATION_LISTENER_PORT>
    }
    ...
}
```


### Embedded Shell (optional)

See [Shell Configuration](shell.md#shell-config) for more information on how to configure the shell.


### ENM Internal Server

To enable communication between the Network Map service and other network management services, such as Revocation and
Identity Manager servers, upon start up the Network Map service will create an internal long running listening server.
This can receive and respond to messages such as requests relating to private network administration (see
[Private Network Map](private-network-map.md)). The configuration block `enmListener` can be used to define the properties of this
listener, such as the port it listens on as well as the retrying and logging behaviour.

```guess
networkMap {
    ...
    enmListener {
        port = 10001
        reconnect = true
    }
    ...
}
```

If debugging or visibility of transport layer messaging is required, the listener can be configured in
a verbose mode that will dump packets to the logs.

```guess
networkMap {
    ...
    enmListener {
        port = 10001
        reconnect = true
        verbose = true
    }
    ...
}
```

{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the ENM services to use SSL](enm-with-ssl.md)

{{< /note >}}

### Identity Manager & Revocation Communication


{{< warning >}}
Private network functionality is an internal feature that is being deprecated. Running a network with one
or more private networks is not a supported configuration.

{{< /warning >}}


The Network Map service may need to speak to both the Identity Manager and Revocation services. For example, the Network
Map service may need to communicate with the Identity Manager service for private network functionality, and with the
Revocation service for CRL related information.

This is configured via the `identityManager` and `revocation` configuration options within the `networkMap`
configuration block:

```guess
networkMap {
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
}
```

The `host` should correspond to the host part of the `address` value in the Identity Manager configuration. The
`port` parameter for each service should correspond with the `port` value within the `enmListener` config block in
the service’s configuration. See [Network Map Configuration Parameters](config-network-map-parameters.md) for more information.

{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the ENM services to use SSL](enm-with-ssl.md)

{{< /note >}}

### Restricting A Node’s Corda Version (optional)

The optional configuration `versionInfoValidation` can be added to the `networkMap` configuration to restrict
publishing of node info to the network map. This configuration has two optional parameters `minimumPlatformVersion`
and `newPKIOnly`.

The new PKI (that involves arbitrary certificate chain lengths) is supported in OS V3.3+ and ENT V3.2+. Setting the
`newPKIOnly` parameter to true will ensure that any OS or ENT version older than this is rejected.

For example:

```guess
networkMap {
    ...
    versionInfoValidation {
        minimumPlatformVersion = 3
        newPKIOnly = true
    }
    ...
}
```

If a node is rejected by the Network Map Service during registration then it will not be present in the global network
map and will not be able to communicate with other nodes on the network. More information on these options can be found
in [Network Map Configuration Parameters](config-network-map-parameters.md).

{{< note >}}
The minimum version configuration options should, in general, be kept consistent between the Identity Manager
and Network Map service

{{< /note >}}

#### Disabling Auto-Enrolment

If this functionality is not needed then you can disable it by including the configuration parameter
`privateNetworkAutoEnrolment` and setting it to false. Disabling this functionality will prevent any nodes from
automatically joining a private network upon registering with the Network Map, although manual private network
functionality will still work (see [Private Network Map](private-network-map.md)).

The main benefit to disabling this functionality is that it removes the need to for a communication link between the
Network Map and Identity Manager. It also removes the need to specify the `identityManagerService` configuration
block:

```guess
networkMap {
    ...
    privateNetworkAutoEnrolment = false
    ...
}
```


### Example Configuration

```guess
address = "example-machine-url:10000"

database {
    runMigration = true
    initialiseSchema = true
    jdbcDriver = "/drivers/postgresql-42.2.5.jar"
    driverClassName = "org.postgresql.Driver"
    url = "jdbc:postgresql://<<DB HOST>>:<<DB PORT>>/<<DATABASE>?"
    user = <<USER>>
    password = <<PASSWORD>>
}

privateNetworkAutoEnrolment = true
checkRevocation = true
pollingInterval = 1000

identityManager {
    host = "example-identity-manager"
    port = 1111
}

revocation {
    host = "localhost"
    port = 2222
}

shell {
    sshdPort = 2222
    user = "testuser"
    password = "password"
}
```


## Network Parameters

Along with the above configuration, a *network-parameters* configuration file also needs to be created. This defines the
basic settings for communication across the network along with references to the notaries node info files. Therefore it
is advisable to register the notaries with the Identity Manager service and generate their node info files prior to
starting the network map.

The network parameters should contain reference to the notaries node info files. The notary node info files should be
copied over to the Network Map service.


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

The network map service provides an endpoint that can be used to determine the IP address of the querying host. This is
useful especially when dealing with node’s deployment in environments with IP address translation.


{{< table >}}

|GET|/network-map/my-hostname|Returns the IP address of the requestor.|

{{< /table >}}

