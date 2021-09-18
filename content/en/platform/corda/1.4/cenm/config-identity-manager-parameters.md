---
aliases:
- /config-identity-manager-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-config-identity-manager-parameters
    parent: cenm-1-4-configuration
    weight: 220
tags:
- config
- identity
- manager
- parameters
title: Identity Manager Configuration Parameters
---


# Identity Manager Configuration Parameters

The Configuration references for the Identity Manager Service are given below:


* **address**:
The host and port on which the service runs


* **database**:
See [CENM Database Configuration](config-database.md)


* **shell**:
  *(Optional)* See [Shell Configuration Parameters](config-shell.md) for more information. Note that
               we are planning to deprecate the shell and the recommended path for interacting with CENM services
               is the admin RPC interface detailed below.


* **localSigner**:
*(Optional)* Configuration of the local signer for the Identity Manager Service. Useful for debugging, testing or when Hardware Security Module (HSM) support is not available.


  * **keyStore**:
  Configuration for the key store containing the Identity Manager Service key pair.
    * **file**:
    Path to the key store file containing the signing keys for the Identity Manager Service.
    * **password**:
    Key store password.
    * **keyAlias**:
    Key alias under which the key can be found in the key store.
    * **keyPassword**:
    Password for the ‘keyAlias’ key entry within the key store.
  * **signInterval**:
  The frequency for triggering the signing process (defined in milliseconds).
  * **timeout**:
  *(Optional)* The maximum time allowed for executing the signing process (in milliseconds). Defaults
  to 30 seconds. If the timeout threshold is reached, then the signing process will abort and wait
  before retrying. The wait time after each failure is determined by an exponential backoff strategy.


* **crlDistributionUrl**:
*(Optional)* REST endpoint under which the certificate revocation list issued by the Identity Manager can be obtained.
It is needed as this URL is encoded in certificates issued by the Identity Manager.
* **workflows**:

  * **workflow-id**:

  * **type**:
 Either `ISSUANCE` or `REVOCATION` - see below for details.

  * **enmListener**:
  Information about the way the service will communicate with the rest of the CENM deployment.

    * **port**:
    The port that the service will bind to, and other CENM components it will connect to.

    * **verbose**:
    *(Optional)* Enables verbose logging for the socket layer.

    * **reconnect**:
    Determines if a client should attempt to reconnect if the connection is dropped.

    * **ssl**:
    See [SSL Settings](config-ssl.md).


* **plugin**:

  * **pluginClass**:
  The main class of the plugin being loaded.

  {{< note >}}
  For automatic acceptance of requests, set this to the `ApproveAll` plugin (“com.r3.enmplugins.approveall.ApproveAll”).

  {{< /note >}}

  * **pluginJar**:
  *(Optional)* The absolute path to the `.jar` file of the workflow plugin.

  * **config**:
  *(Optional)* A free-form map that allows options to be passed to the plugin class.






* **“issuance workflow”**:
  * **updateInterval**:
  Determines how often the Issuance Workflow Processor should synchronise Certificate Signing Request (CSR) statuses.
  * **versionInfoValidation**:
  *(Optional)* Configuration for the validation of node version info during CSR submission.
  * **minimumPlatformVersion**:
  *(Optional - defaults to `-1`)* The minimum platform version of Corda that a node needs to run on, in order to successfully submit Certificate Signing Requests. The platform
  version is an integer value that increments with each release where any of the public APIs of the entire Corda platform are changed. Setting this to a value lower than 1
  disables this behaviour - in that case, the Identity Manager Service does not check whether that platform version is passed from the node.

  {{< important >}}
  Whilst this value is optional, picking the correct value is essential for a zone operator as it forms the basis upon which compatibility and consensus are formed on the Network. It also commits potential members to specific versions of the Corda API. The value must be higher or equal to any other value specified in the Network Map and the corresponding Network Parameter configurations.
  {{< /important >}}

  * **newPKIOnly**:
  *(Optional - defaults to `false`)* A boolean parameter that determines whether Certificate Signing Request (CSR) should be rejected for all nodes running an outdated version of Corda that does not support the new PKI structure (arbitrary length certificate chains).
* **“revocation workflow”**:
  * **crlCacheTimeout**:
  The interval after which the Revocation Workflow Processor needs to synchronise Certificate Revocation Requests (CRR) statuses, as well as the duration after the CRL cache in Revocation Web Service is cleared.
  * **crlFiles**:
A list of CRLs hosted by the Identity Manager Service, in addition to the CRLs hosted by node operators. This allows the Identity Manager Service to host the CRLs for node operators that will not host their own CRL infrastructure, at the cost of not being able to revoke TLS certificates issued by the node.
* **adminListener**:
  A configuration property you must define in order to use the RPC API in the Identity Manager Service.
  You can add `port`, `reconnect`, and `verbose`. Also, this property has an SSL field - for more information, see [SSL Settings](config-ssl.md).
  * **port**:
    Port number to listen to for Admin RPC connections.
  * **verbose**:
    *(Optional)* Enables verbose logging for the socket layer. Defaults to `false`.
  * **reconnect**:
    *(Optional)* Determines if a client should attempt to reconnect if the connection is dropped. Defaults to `true`.
  * **ssl**:
    See [SSL Settings](config-ssl.md) for details.

{{% important %}}
If the `adminListener` property is present in the configuration, this means that the service must only be used via Admin RPC. In this case, the `shell` configuration property will be disabled. The `shell` and `adminListener` properties cannot be used in the configuration at the same time.
{{% /important %}}

* **authServiceConfig**:
  The admin RPC interface requires an Auth Service to verify
  requests, which must be configured below in a `authServiceConfig` block. Typically
  this is provided automatically by the [Zone Service](zone-service.md) (via an Angel Service),
  however the parameters are detailed below for reference:
  * **host**: The hostname of the Auth Service. Required unless authentication is disabled.
  * **port**: The port number of the Auth Service. Required unless authentication is disabled.
  * **trustStore**:
  Trust store configuration for the SSL PKI root of trust.
    * **location**:
    The location in the file system of the keystore containing the Auth Service root of trust.
    * **password**:
    The password for the trust root keystore.
  * **issuer**: The \"iss\" claim in the JWT - you must set the same value as in the Auth Service's configuration. Required unless authentication is disabled.
  * **leeway**: Defines the amount of time, in seconds, allowed when checking JSON Web Token (JWT) issuance and expiration times. Required unless authentication is disabled. We recommend a default time of **10 seconds**.

## Obfuscated configuration files

To view the latest changes to the obfuscated configuration files,
see [Obfuscation configuration file changes](obfuscated-config-file-changes.md).

## Redirection forbidden

The Identity Manager cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.
