---
aliases:
- /zone-service.html
date: '2020-06-04T13:44:00Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-zone-service
    parent: cenm-1-4-operations
    weight: 155
tags:
- zone
- configuration
title: Zone Service
---

# Zone Service

## Overview

The Zone Service is a central store of configuration for other CENM services
for one or more zones, and optionally for their subzones. These CENM services
can fetch their configuration from the Zone Service and therefore simplify change
management. They also provide functionality for managing
lifecycle events of subzones, such as updating network parameters via
flag days.

The Zone Service stores relevant configurations for the following services:

* Identity Manager Service
* Network Map Service
* Signing Services

It uses the associated [Angel Service]({{< relref "angel-service.md" >}}) to deploy those configurations as needed.
Each Angel Service identifies itself to the Zone Service via an authentication
token, referred to as the "zone token". The Zone Service also coordinates actions
needed on subzones (for example, new network parameters), which are executed
by the Angel Service for the appropriate Network Map Service.

## Running the Zone service

The Zone Service does not have a configuration file, and is configured entirely
from the command-line. To run the Zone Service, use a command like the one shown in the example below:

```bash
java -jar zone.jar --enm-listener-port=5061 --url=\"jdbc:h2:file:/opt/zone/zone-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0\" --user=testuser --password=password --admin-listener-port=5063 --driver-class-name=org.h2.jdbcx.JdbcDataSource --auth-host=auth-service --auth-port=8081 --auth-trust-store-location=certificates/corda-ssl-trust-store.jks --auth-trust-store-password=trustpass --auth-issuer=http://test --auth-leeway=10 --run-migration=true
```

The full list of configuration options follows below:

- `--enm-listener-port`: The port where the Zone Service listens for Angel Services to connect.
- `--enm-reconnect`: Allows you to reconnect. Defaults to `true` if no value is provided.
- `--tls`: Defines whether TLS is used on listening sockets (CENM and admin). Defaults to `false` if no value is provided.
- `--tls-keystore`: The path for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-keystore-password`: The password for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-truststore`: The path for the TLS truststore. Required if `--tls` is set to `true`.
- `--tls-truststore-password`: The password for the TLS truststore. Required if `--tls` is set to `true`.
- `--run-migration`:  Defines whether schema migration is enabled on the database. Defaults to `false` if no value is provided. **Important:** if you are upgrading to CENM 1.4 from CENM 1.3, you **must** set this option to `true` due to a change in the Zone Service database schema - see the [CENM upgrade guide]({{< relref "upgrade-notes.md" >}}) for more information.
- `--jdbc-driver`:  The path for the JAR file containing the JDBC driver for the database.
- `--driver-class-name`: The name of the JDBC driver class within the JAR file specified by `--jdbc-driver`.
- `--url`: The URL for the Zone Service's database.
- `--user`: The user for the Zone Service's database.
- `--password`: The password for the Zone Service's database.
- `--current-schema`: Allows you to alter the session's current schema for the database. Use this configuration option when the schema name differs from the user name. Only valid for Oracle databases.
- `--admin-listener-port`: The port where Angel Services connect to the Zone Service.
- `--disable-authentication`: Allows you to disable authentication and authorisation via the [Auth Service]({{< relref "auth-service.md" >}}). Only use this option in development environments. Defaults to `false` if no value is provided.
- `--auth-host`: The hostname of the Auth Service. Required unless authentication and authorisation are disabled.
- `--auth-port`: The port number of the Auth Service. Required unless authentication and authorisation are disabled.
- `--auth-trust-store-location`: The location of the Auth Service trust root keystore. Required unless authentication and authorisation are disabled.
- `--auth-trust-store-password`: The password for the Auth Service trust root keystore. Required unless authentication and authorisation are disabled.
- `--auth-issuer`: The \"iss\" claim in the JWT - you must set the same value as in the Auth Service's configuration. Required unless authentication and authorisation are disabled.
- `--auth-leeway`: Defines the amount of time, in seconds, allowed when checking JSON Web Token (JWT) issuance and expiration times. Required unless authentication and authorisation are disabled. R3 recommends a default time of **10 seconds**.
- `--working-dir`: Defines the working directory to the specified directory. The service will look for files in that directory. This means certificates, configuration files etc. should be under the working directory. If not specified it will default to the current working directory (the directory from which the service has been started).

## Configurations for other CENM services

To ensure consistency and correctness of the configurations it sends to other CENM services, the Zone Service edits them before sending. The following sections describe these changes for each affected service.

### Identity Manager service configuration

The Zone Service sets the Auth Service configuration for the Identity Manager Service based on the Auth Service configuration options provided when running the Zone Service (see the previous section).

The Auth Service trust store location and password must match on the hosts of the Zone Service and the Identity Manager Service. R3 recommends that the trust store location is set as a relative path to the working directory on each host (for example, `certificates/auth-trust-store.jks`) rather than as an absolute path.

{{< note >}}
The shell UI used in CENM 1.2 (and below) is not supported in combination with the RPC API functionality in CENM 1.3 and above, so configurations *must not* specify a shell configuration or they will be rejected by the respected services.
{{< /note >}}

### Network Map service configuration

The Zone Service sets the authentication configuration for the Network Map Service based on the Auth Service configuration options provided when running the Zone Service. The same guidance on sharing values applies as described for the Identity Manager Service above.

The Zone Service also sets the Sub Zone ID (`authObjectId`) for the Network Map Service. The Sub Zone ID is used to support permissioning per subzone for users. It is set automatically so no user action is required.

### Signing services configuration

The service locations for the Signing Services are set by the Zone Service using the external addresses and the CENM ports configured for the Identity Manager Service and Network Map Service. Any service locations provided in Signing Services configurations, sent to the Zone Service, are overwritten.

The SSL client settings used when connecting to these services are set uniformly
across all service locations, and are taken from the first of any service location
in the Signing Service location set on the Zone Service.

As the service locations are generated programmatically, the service location aliases
(referred to by the signing task configurations) are in a specific format, which
must be matched exactly, as follows:

* Identity Manager CSR: `issuance`
* Identity Manager CRR/CRL: `revocation`
* Network Map: `network-map-<subzone-id>`

An example configuration section generated by the Zone Service is provided below:

```guess
serviceLocations = {
    "issuance" = {
        host = "identity-manager"
        port = 5051
        reconnect = true
        ssl = {
            keyStore = {
                location = ./certificates/corda-ssl-signer-keys.jks
                password = password
                keyPassword = password
            }
            trustStore = {
                location = ./certificates/corda-ssl-trust-store.jks
                password = trustpass
            }
            validate = true
        }
        verbose = false
    }
    "network-map-1" = {
        host = "networkmap"
        port = 5070
        reconnect = true
        ssl = {
            keyStore = {
                location = ./certificates/corda-ssl-signer-keys.jks
                password = password
                keyPassword = password
            }
            trustStore = {
                location = ./certificates/corda-ssl-trust-store.jks
                password = trustpass
            }
            validate = true
        }
        verbose = false
    }
    "revocation" = {
        host = "identity-manager"
        port = 5052
        reconnect = true
        ssl = {
            keyStore = {
                keyPassword = password
                location = ./certificates/corda-ssl-signer-keys.jks
                password = password
            }
            trustStore = {
                location = ./certificates/corda-ssl-trust-store.jks
                password = trustpass
            }
            validate = true
        }
        verbose = false
    }
    timeout = 12000
}
```

{{< note >}}
The `timeout` parameter used in the example above is optional. It allows to set a Signing Service timeout for communication to each of the services used within the signing processes defined in the [signers map]({{< relref "signing-service.md#signers-map-entry-example" >}}), in a way that allows high node count network maps to get signed and to operate at reliable performance levels. The `timeout` value is set in milliseconds and the default value is 10000 milliseconds. The `timeout` parameter's value is stored in a column in the [Zone Service]({{< relref "zone-service.md" >}})'s database tables `socket_config` and `signer_config` called `timeout`. This value can remain `null` (for example, if `timeout` is not defined in `serviceLocations`), in which case the default 10000 milliseconds value (`timeout = 10000`) will be used wherever applicable. Please note that currently, due to a known issue with `serviceLocations`, when the `timeout` parameter is passed to the Zone Service via the Signing Service's `serviceLocations` configuration block, only the `timeout` value of the first `serviceLocations` location will be taken into account and used for all other service locations.
{{< /note >}}

## Interaction with Angel Services

Angel Services regularly poll the network's Zone Service for jobs.

The Zone Service maintains its database and decides if a configuration update or a lifecycle event is needed for the underlying Angel Service. If needed, it sends the relevant response.

If a flag day is triggered, the Zone Service sends the required step (initiate, start, or cancel Flag Day) to the Angel Service that manages the Network Map. The Angel Service always reports the status of the current action back to the Zone Service.
