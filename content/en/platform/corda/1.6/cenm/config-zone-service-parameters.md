---
aliases:
- /config-zone-service-parameters.html
date: '2024-09-24'
menu:
  cenm-1-6:
    identifier: cenm-1-6-config-zone-service-parameters
    parent: cenm-1-6-configuration
    weight: 256
tags:
- config
- zone service
title: Zone Service configuration parameters
---

# Zone Service configuration parameters

The configuration references for the Zone Service are given below:

* **database**:
See [CENM database configuration]({{< relref "config-database.md" >}})

* **enmListener**:
Information about the way the service communicates with the rest of the CENM deployment.

  * **host**:
  *(Optional)* The host or IP of the service.

  * **port**:
  The port that the service binds to, and other CENM components it connects to.

  * **reconnect**:
  Determines if a client should attempt to reconnect if the connection is dropped.

  {{< note >}}
  The `ssl` configuration is not present in the `enmListener`, as the Zone Service uses the same TLS configuration for both CENM and admin listening sockets.

  {{< /note >}}

* **adminListener**:
  A configuration property you must define in order to use the RPC API in the Zone Service.
  You can add `port`, `reconnect`, and `verbose`. Also, this property has an SSL field - for more information, see [SSL settings]({{< relref "config-ssl.md" >}}).

  * **host**:
    *(Optional)* The host or IP of the Admin RPC service.

  * **port**:
    Port number to listen to for Admin RPC connections.

  * **verbose**:
    *(Optional)* Enables verbose logging for the socket layer. Defaults to `false`.

  * **reconnect**:
    *(Optional)* Determines if a client should attempt to reconnect if the connection is dropped. Defaults to `true`.

  * **ssl**:
    See [SSL settings]({{< relref "config-ssl.md" >}}) for details.

* **authServiceConfig**:
  The admin RPC interface requires an Auth Service to verify requests, which must be configured below in an `authServiceConfig` block. Typically, this is provided automatically by the [Zone Service]({{< relref "zone-service.md" >}}) (via an [Angel Service]({{< relref "angel-service.md" >}})). However, the parameters are detailed below for reference:

  * **host**:
    The hostname of the Auth Service. Required unless authentication is disabled.

  * **port**:
    The port number of the Auth Service. Required unless authentication is disabled.

  * **trustStore**:
  Trust store configuration for the SSL PKI root of trust.

    * **location**:
    The location in the file system of the keystore containing the Auth Service root of trust.

    * **password**:
    The password for the trust root keystore.

  * **issuer**:
    The \"iss\" claim in the JWT - you must set the same value as in the Auth Service's configuration. Required unless authentication is disabled.

  * **leeway**:
    Defines the amount of time, in seconds, allowed when checking JSON Web Token (JWT) issuance and expiration times. Required unless authentication is disabled. R3 recommends a default time of **10 seconds**.

## Obfuscated configuration files

To view the latest changes to the obfuscated configuration files,
see [Obfuscation configuration file changes]({{< relref "obfuscated-config-file-changes.md" >}}).
