---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-identity-manager
    parent: cenm-1-4-operations
    weight: 130
tags:
- identity
- manager
title: Identity Manager Service
---


# Identity Manager Service



## Purpose

The Identity Manager Service acts as the gatekeeper to the network. It is formed of two components:


* **Issuance**: Responsible for issuing certificates to new nodes wanting to join the network.
* **Revocation**: *(Optional)* Responsible for handling certificate revocation requests as well as hosting the CRL endpoints that are used by participants to check a certificate’s revocation status.

{{< warning >}}
**The Identity Manager Service cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.**
{{< /warning >}}

## Running The Identity Manager Service

Once the Identity Manager has been configured, it can be run via the command:

```bash
java -jar identity-manager-<VERSION>.jar --config-file <CONFIG_FILE>
```

Optional parameter:

```bash
--working-dir=<DIR>
```

This will set the working directory to the specified folder. The service will look for files in that folder. This means
certificates, configuration files etc. should be under the working directory.
If not specified it will default to the current working directory (the directory from which the service has been started).

On success you should see a message similar to:

```kotlin
Network management web services started on localhost:1300 with [RegistrationWebService, CertificateRevocationWebService, MonitoringWebServer]
```


## Configuration

The main elements that need to be configured for the Identity Manager are:


* [Address](#address)
* [Database](#database)
* [Embedded shell (optional)](#embedded-shell-optional)
* [Issuance workflow](#issuance-workflow)
    * [CSR Approval Mechanism](#csr-approval-mechanism)
    * [CSR Signing Mechanism](#csr-signing-mechanism)
    * [Issuance Internal Server](#issuance-internal-server)
    * [Restricting a node’s Corda version (optional)](#restricting-a-node-s-corda-version-optional)
* [Revocation workflow (optional)](#revocation-workflow-optional)
    * [CRR Approval Mechanism](#crr-approval-mechanism)
    * [CRR Signing Mechanism](#crr-signing-mechanism)
    * [Revocation Internal Server](#revocation-internal-server)
* [Admin RPC Interface](#admin-rpc-interface)
* [HA Endpoint (optional)](#ha-endpoint)
    * [Caching Proxy Setup](#caching-proxy-setup)
    * [Caching Proxy Limitations](#caching-proxy-limitations)
    * [Application Gateway Setup](#application-gateway-setup)
    * [System Configuration And Behavior](#system-configuration-and-behavior)


{{< note >}}
See [Identity Manager Configuration Parameters](config-identity-manager-parameters.md) for a detailed explanation about each possible parameter.
{{< /note >}}

### Address

The `address` parameter must be included in the top level of the configuration and represents the host and port
number that the Identity Service will bind to upon start-up. The host can either be the IP address or the hostname of
the machine that Identity Manager is running on. For example:

```guess
address = "<SERVER_IP/SERVER_HOST>:<PORT_NUMBER>"
```

{{< note >}}
Depending on the configuration of your deployment the host may be different to the external IP/DNS name
that other nodes will use to connect to the service. The service needs to be able to bind to this host and
port. For example, in a cloud environment with the machine inside a “virtual network”, the host in the
configuration may need to be the private IP address, whilst external nodes would use the machines external
IP/DNS name to connect to Identity Manager.

{{< /note >}}

### Database

The Identity Manager Service is backed by a SQL database which it uses to store information such as Certificate Signing
Requests (CSRs) and (optionally) Certificate Revocation Requests (CRRs). The connection settings must be included within
the `database` configuration block in the configuration file. The main options that should be included here are:


* `driverClassName` - the database driver class name (e.g *com.microsoft.sqlserver.jdbc.SQLServerDriver* for Microsoft SQL Server, *org.postgresql.Driver* for postgres)
* `jdbcDriver` - the path to the appropriate JDBC driver `.jar` (e.g *path/to/mssql-jdbc-7.2.2.jre8.jar*)
* `url` - the connection string for the database
* `user` - the username for the database
* `password` - the password for the database


#### Database Setup

The database can either be setup prior to running the Identity Manager Service or, alternatively, it can be
automatically prepared on start-up via the built-in migrations. To enable the running of database migrations on start-up
the optional `runMigration` parameter within the `database` configuration should be set to true. Additionally, if
the Identity Manager Service is being run using the same database instance as an accompanying Network Map Service then the
Identity Manager schema name must be specified via the `schema` parameter within the `database` configuration block:

```guess
database {
    ...
    runMigration = true
    schema = identity_manager
}
```

{{< note >}}
Due to the way the migrations are defined, if the Identity Manager and Network Map Services are using the same
database instance then they *must* use separate database schemas. For more information regarding the supported databases
along with the schema see [CENM Databases](database-set-up.md).

{{< /note >}}

#### Additional Properties

Additional database properties can be loaded by including an optional *additionalProperties* configuration block. Currently
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

An example configuration for an Identity Manager Service using a Microsoft SQL Server database, configured to run the
migrations on start-up is:

```guess
database {
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    jdbcDriver = "path/to/mssql-<EXAMPLE_JDBC_DRIVER>.jar"
    url = "jdbc:sqlserver://<EXAMPLE_CONNECTION_STRING>"
    user = "example-user"
    password = "example-password"
    schema = "identity_manager"
    runMigration = true
    additionalProperties {
        connectionTimeout = 60000
        maxLifetime = 3200000
        poolName = "myPool123"
    }
}
```


### Embedded shell (optional)

See [Shell Configuration](shell.md#shell-config) for more information on how to configure the shell.


### Issuance Workflow

The Issuance workflow is one of two components within the Identity Manager. In order for a new node to join the network,
it first needs a certificate that is signed by the Identity Manager. It acquires this by submitting a Certificate
Signing Request (CSR) to the Identity Manager which is handled by the Issuance workflow. The workflow determines how the
CSR gets approval as well as how the desired certificate is signed.


#### CSR Approval Mechanism

Before a certificate can be issued to a new node, its CSR first needs to be approved. The mechanism by which approval is
granted can vary from a basic automatic approval approach to a more manual, production grade approach like JIRA
integration. The approval mechanism is configured by specifying the plugin class responsible for handling CSR approvals
within the Issuance workflow inside the Identity Manager’s configuration file. The CENM currently ships with two included
plugins:


* Auto approval
* JIRA workflow

An approval mechanism *must* be specified.


{{< warning >}}
Auto Approval will approve every request without any oversight or checking. This setup should only ever be used for testing scenarios

{{< /warning >}}



##### Auto Approval

Auto approval results in the Issuance workflow blindly approving every request it receives. This is useful for testing
as it negates the need for an external approval process.


{{< warning >}}
This should only be enabled in a test environment

{{< /warning >}}


This mechanism can be enabled by referencing the auto approval workflow plugin within the configuration file:

```guess
workflows {
    "issuance" {
        type = ISSUANCE
        ...
        plugin {
            pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
        }
    }
}
```


##### JIRA Workflow

The Identity Manager Service can use JIRA to manage the certificate signing request approval work flow. This can be
enabled by referencing the JIRA CSR workflow plugin within the configuration file along with the associated configuration
parameters:

```guess
workflows {
    "issuance" {
        type = ISSUANCE
        ...
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCsrWorkflowPlugin"
            config {
                address = <IDENTITY_MANAGER_JIRA_HOST> # e.g. "https://identity-manager-jira-host.r3.com/"
                projectCode = <PROJECT_CODE>
                username = <USERNAME>
                password = <PASSWORD>
            }
        }
}
```

See [Workflow](workflow.md) for more information.


###### JIRA Project Configuration

See [JIRA Set-Up](jira-setup.md) for more information about how to configure a JIRA project for CSR approval.


#### CSR Signing Mechanism

Once a CSR signing request has been approved then a certificate can be signed and issued to the node. Similarly to the
approval mechanism above, this can be achieved via one of two mechanisms:


* Local Signing Service
* External Signing Service


##### Local Signing Service

The local signing service is recommended for testing and toy environments. Given a local key store containing the
relevant signing keys, it provides the functionality to automatically sign all approved CSRs on a configured schedule.
No human interaction is needed and the credentials for the key stores have to be provided upfront. The service is an
integrated signer that is a cut-down version of the standalone [Signing Services](signing-service.md) and provides no HSM integration or
ability to manually verify changes. It is strongly recommended against using this for production environments.

In order for the local signer to function, it needs to be able to access Identity Manager’s certificate and keypair
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

In this example, the key store defined within the local signer should contain the Identity Manager’s key pair used for
signing any CSR requests along with the full certificate chain back to the root of the network.


##### External Signing Service

The production grade signing mechanism is the external [Signing Services](signing-service.md). This has all the functionality of the
integrated local signer as well as HSM integration and the ability for a user to interactively verify and sign incoming
CSRs. It should be used in all production environments where maximum security and validation checks are required.

In order to retrieve the CSR information, the signing service will communicate with the Identity Manager via its
[Issuance internal server](#issuance-internal-server). This is the only configuration option that is needed if signing of CSRs is being done via the
external signing service.


#### Issuance Internal Interface

Similarly to the other Corda Enterprise Network Manager (CENM) services, the Identity Manager is designed to be able to communicate between other services
such as the Network Map and Signing services. Both the Issuance and, optionally, the Revocation workflows have their own
internal listening socket interface that is created on start-up which can receive and respond to messages from other CENM services.
For example, the Revocation workflow’s CENM listener can respond to messages from the Network Map regarding certificate
statuses of current participants which the Network Map Service will then use when refreshing the latest Network Map.

To configure this internal server, the configuration block `enmListener` should be added within the Issuance
workflow’s configuration:

```guess
workflows {
    "issuance" {
        type = ISSUANCE
        ...
        enmListener {
            port = 10001
            reconnect = true
        }
        ...
    }
    ...
}
```

{{< note >}}
This parameter can be omitted if desired, in which case it will default to port 5051 with `reconnect = true`.

{{< /note >}}
{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the CENM services to use SSL](enm-with-ssl.md).

{{< /note >}}

### Restricting A Node’s Corda Version (optional)

The optional configuration `versionInfoValidation` can be added to the Issuance workflow configuration block to
exclude nodes running an old version of Corda from successfully submitting a CSR. The configuration parameter
`minimumPlatformVersion` represents the minimum platform version that a node has to be running to be able to submit
a CSR. If this is set, then any node that attempts to submit a CSR and is running a version of Corda with a platform
version less than this will be automatically rejected. This can be used to ensure that all nodes that join the network
have access to certain features.

{{< note >}}
This serves a similar purpose to the *minimumPlatformVersion* within the network parameters and also within
the Network Map Service configuration. However, unlike the other two options, as it prevents an outdated node
from successfully submitting a CSR in the first place it prevents any version related issues at the earliest
possible step. Relying solely on the Network Parameters platform version gate can result in an outdated node
successfully receiving a certificate to join the network despite not being able to (and thus needing to
upgrade).

{{< /note >}}
```guess
workflows {
    "issuance" {
        type = ISSUANCE
        ...
        versionInfoValidation {
            minimumPlatformVersion = 4
        }
        ...
    }
    ...
}
```

{{< note >}}
Sending of version info during registration was added to Corda OS in release version 3.3. Using this approach
with a minimum version less than this will not work unless the nodes are running a modified code base.

{{< /note >}}

### Revocation Workflow (optional)

The Revocation workflow is the second of the two main components in the Identity Manager Service. It is an optional
component that is responsible for handling incoming Certificate Revocation Requests (CRRs) to revoke a node’s
certificate (acquired via a previously approved CSR) as well as hosting the Certificate Revocation Lists (CRLs) to
enable the participants on the network to verify the validity of other’s certificates.

Similarly to the Issuance workflow, the Revocation workflow determines how a CRR gets approved and signed.


#### CRR Approval Mechanism

In order to revoke a node’s certificate and therefore be evicted from the network, a CRR needs to be approved and signed
by the network operator. The method by which the CRR is approved is, similar to the Issuance workflow, configured by
specifying the plugin class responsible for the handling of the CRRs within the Revocation workflow inside the Identity
Manager’s configuration file. The CENM ships with two included plugins:


* Auto approval
* JIRA workflow

An approval mechanism *must* be specified.


{{< warning >}}
Auto Approval will approve every request without any oversight or checking. As such, this should only ever be used for testing scenarios

{{< /warning >}}



##### Auto Approval

Auto approval results in the Revocation workflow blindly approving every request it receives. This is useful for testing
as it negates the need for an external approval process.


{{< warning >}}
This should only be enabled in a test environment

{{< /warning >}}


This mechanism can be enabled by referencing the auto approval workflow plugin within the configuration file:

```guess
workflows {
    "revocation" {
        type = REVOCATION
        ...
        plugin {
            pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
        }
    }
}
```


##### JIRA Workflow

The Issuance workflow can alternatively use JIRA to manage CRR approval. This can be enabled by referencing the JIRA
CRR workflow plugin within the configuration file along with the associated configuration parameters:

```guess
workflows {
    "revocation" {
        type = REVOCATION
        ...
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCrrWorkflowPlugin"
            config {
                address = <REVOCATION_JIRA_HOST> # e.g. "https://revocation-jira-host.r3.com/"
                projectCode = <PROJECT_CODE>
                username = <USERNAME>
                password = <PASSWORD>
            }
        }
}
```

See [Workflow](workflow.md) for more information.


#### CRR Signing Mechanism

Once CRR have been approved they need to be signed by the Identity Manager. Similarly to the Issuance workflow, this
can be achieved via two mechanisms:


* Local Signing Service
* External Signing Service


##### Local Signing Service

As the local signer is a top-level configuration block, it is shared amongst all configured workflows within the
Identity Manager. That is, the same key used for signing approved CSRs will be used to sign approved CRRS. See the
“Local Signing Service” section within the above Issuance workflow documentation to see how to configured this.


##### External Signing Service

Also similarly to CSR signing, the production grade signing mechanism for CRRs is the external [Signing Services](signing-service.md).
This has all the functionality of the integrated local signer as well as HSM integration and the ability for a user to
interactively verify and sign incoming CRRs. It should be used in all production environments where maximum security and
validation checks are required.

In order to retrieve the CRR information, the signing service will communicate with the Revocation Service via its
[Revocation internal server](#revocation-internal-server). This is the only configuration option that is needed if signing of CSRs is being done via the
external signing service.


#### Revocation Internal Server

Similarly to the Issuance workflow, the Revocation workflow is configured with an internal listening server to enable
communication between other services such as the Network Map and Signing services.  To configure this, the configuration
block `enmListener` should be added within the Revocation workflow’s configuration:

```guess
workflows {
    "revocation" {
        type = REVOCATION
        ...
        enmListener {
            port = 10001
            reconnect = true
        }
        ...
    }
    ...
}
```

{{< note >}}
This parameter can be omitted if desired, in which case it will default to port 5052 with `reconnect = true`.

{{< /note >}}
{{< note >}}
All inter-service communication can be configured with SSL support. See [Configuring the CENM services to use SSL](enm-with-ssl.md).

{{< /note >}}


### Admin RPC Interface

To enable the CENM Command-Line Interface (CLI) tool to send commands to the Identity Manager Service,
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

### HA Endpoint

The crucial role that the Identity Manager Service plays in the communication between nodes, and in particular the
importance of the Certificate Revocation List (CRL) during flow execution, creates the need for high availability
even when the Identity Manager Service is unresponsive. The suggested approach is made of a load balancing gateway and as an entry point,
redirecting CRL requests to a pool of caching proxies, which ultimately redirect to the Identity Manager Service
or use their cached CRL values if it is down.

R3 have verified a solution using [Azure Application Gateway](https://docs.microsoft.com/en-us/azure/application-gateway/overview) and [Nginx](https://www.nginx.com), although the concepts applied should be similar for other solutions.

##### Caching Proxy Setup

Most of the reverse-proxy configuration provided in this document is straightforward, however the caching configuration requires
a few tweaks. Instead of operating as a normal cache that uses its stored values for purely performance benefits, this cache
needs to be updated frequently and to store the content for as long as the Identity Manager Service is not responsive.

For this reason, the validity period of the value is set to a very small amount (1 second). This forces all calls, which
are not within the same second, to attempt a redirection to the Identity Manager Service for a fresh response.
Simultaneously, Nginx is configured to use the stale content in case the server times out or fails with an error, ignoring
the aforementioned time window.

Moreover, Nginx by default deletes cached files that have not been accessed within the specified timeout,
forcing the use of the timeout variable when specifying the `proxy_cache_path` to make sure that the cache
is not cleared even if the CRL hasn't been requested for a while.

As a result of this implementation, you can choose to use an alternative method to
expire the cached responses and to return an error after some time - for example,
by making the proxy's health check to query its cached values for their updated
time, and to declare itself unavailable if needed.

A part of this configuration is shown below:

```guess
...

http {
    ...

    # enabling caching
    # timeout set to 10 days of stale value
    proxy_cache_path /var/cache/nginx keys_zone=mycache:10m max_size=1g loader_threshold=300 loader_files=200 inactive=240h;

    # server group for load balancing
    upstream idman {
	  ...
    }

    ...

    server {
	...

        location / {
            proxy_pass          http://idman;
            proxy_set_header    Host $host;
            proxy_buffering     on;

            proxy_cache mycache;
            proxy_cache_methods GET HEAD;
            # just one sec validity "forces" to hit backend
            proxy_cache_valid 200 1s;
            # use stale result in case of unreachable Identity Manager
            proxy_cache_use_stale error timeout;
        }
    }
}
```

See the [Nginx documentation](https://nginx.org/en/docs/) for additional information.

##### Caching Proxy Limitations

Based on the configuration mentioned above, if there is no expiry routine set in place, the call
will always return a value if it has managed to save one at any point in time. This effectively means that
the system can operate as normal without a running Identity Manager Service as long as the CRL is valid.

When multiple caching proxies are defined, in rare cases there could be inconsistencies among their cached values.
Some of the instances may contain outdated cached values because they were not hit after a CRL update,
or they may not contain a value at all due to a lack of hits after they were spawn. For this reason, we recommend that you use a shared mounted volume as
the cache directory in order to make sure that all the cached responses are the same, and that there are no CRL inconsistencies across proxy instances.
You can do that easily by, for example, using a Kubernetes cluster for managing the proxy containers.

The cache of each proxy instance (or all of them, if they are using a shared volume) is refreshed as soon as a request to this proxy is made.
A frequent polling interval should be set in order to avoid a scenario where an
Identity Manager Service is live long enough to receive a new signed CRL but
fails again before the proxies fetch and cache the updated CRL.

##### Application Gateway setup

The Application Gateway setup is very straightforward and for the most part follows the default configuration that Azure provides.
However, a custom health check probe may need to be added if we want proxies to declare themselves unavailable, for example
if the cached values are too old to use and the Identity Manager Service is not responding.

##### System configuration and behavior

After configuring the proxy and the Application Gateway, all the configuration files and certificates that would point to
the Identity Manager Service CRL endpoint must be pointing to the Gateway endpoint instead.

After you've made these changes and you have spun up a CENM ecosystem with an Identity Manager Service, a Network Map Service, a Signing Service, and Nodes,
you can observe a successful retrieval of revocation lists from the registered nodes even when the
Identity Manager Service is not operating (using the CRL endpoint health check tool provided by CENM). However, operations that require
additional calls, such as signing a new CRL from the Signing Service, may not be possible to perform.

Although we have observed errors during the tests where the Network Map Service would fail to validate
the registered Notary's certificate, we considered this to be an unrelated issue.

#### CRL configuration

There are two additional parameters that need to be specified with the revocation workflow configuration block:


* **crlCacheTimeout**:
The time (in milliseconds) for nodes to cache the CRL for


* **crlFiles**:
The list of CRLs for other participants within the certificate chain. This is necessary as when a node checks
for revoked certificates, it needs to check all certificates within the certificate chain. This parameter can
be used to include CRLs to remove the requirement for node operators to provide their own CRL
infrastructure (explained below).



For example:

```guess
workflows {
    "revocation" {
        type = REVOCATION
        ...
        crlCacheTimeout = 100000
        crlFiles = ["./crl-files/root.crl", "./crl-files/subordinate.crl", "./crl-files/identity-manager.crl"]
        ...
    }
    ...
}
```


##### TLS-level (empty) CRL

The downside of enabling certificate revocation is that all issuing authorities within the same chain
must provide the infrastructure by which connections can retrieve the revocation lists for their keys:

```kotlin
+------------------+
|       Root       | - Creates and signs a CRL to ensure we can revoke the Identity Manager certificate
+------------------+
         |
+------------------+
| Identity Manager | - *This* level is where the dynamic CRL list is provided for revoking node certificates
+------------------+   upon request
         |
+------------------+
|       Node       | - When issuing TLS certificates, node operators can opt to use the empty certificate
+------------------+   revocation list to avoid the need to provide their own CRL infrastructure.
         |
+------------------+
|        TLS       |
+------------------+
```

This has the effect that Node operators must also provide CRL infrastructure for the TLS certificates they
issue that is signed by their own key. Should Node operators wish to circumvent this requirement
they can take advantage of a convenience option whereby they can refer to a URL endpoint hosted by
the network operator within their certificates which is always empty.


{{< warning >}}
If node operators decide to go down this path then that Node will be unable to revoke any TLS certificates
it issues.

{{< /warning >}}


Given that the operator of a network is already committed to providing CRL infrastructure, they can
choose to make that empty list available to node operators as a convenience.


{{< attention >}}

There is of course no obligation of a zone to provide the empty list infrastructure. However it is still
a required element of the configuration that can be set to any invalid string should they wish to not provide it.


{{< /attention >}}


### Node Configuration

Running a Revocation service does not guarantee that revoked certificates will be checked before nodes communicate with
each other. Node configuration changes may be required to enable this behaviour. For more information see the
documentation for the specific release version of Corda of the node in question.

An example node configuration that enables revocation checking is:

```guess
tlsCertCrlDistPoint = "http://<IDENTITY_MANAGER_HOST>/certificate-revocation-list/empty"
tlsCertCrlIssuer = "C=US, L=New York, OU=Corda, O=R3 HoldCo LLC, CN=Corda Root CA" # the ordering of the X500 name parts is important
crlCheckSoftFail = false # strict CRL checking is enabled, meaning that the SSL connection will fail if the CRL cannot be obtained or is invalid
```

{{< note >}}
*tlsCertCrlDistPoint* needs to be an externally accessible URL.

{{< /note >}}

### Example Configuration


#### Test Configuration

Below is an example of a testing configuration of the Identity Manager. It is configured with a Issuance and Revocation
workflow, using a local signer and auto approval of CSRs and CRRs.

```docker
 address = "localhost:10000"

database {
  driverClassName = org.h2.Driver
  url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  user = "example-db-user"
  password = "example-db-password"
}

localSigner = {
  keyStore = {
   file = exampleKeyStore.jks
   password = "example-password"
  }
  keyAlias = "example-key-alias"
  signInterval = 15000
  crlDistributionUrl = "http://"${address}"/certificate-revocation-list/doorman"
}

workflows {
  "issuance" = {
    type = ISSUANCE
    updateInterval = 1000
    enmListener {
      port = 5050
      reconnect = true
    }
    plugin {
      pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
    }
  },
  "revocation" = {
    type = REVOCATION
    enmListener {
      port = 5051
      reconnect = true
    }
    plugin {
      pluginClass = "com.r3.enmplugins.approveall.ApproveAll"
    }
    crlCacheTimeout = 2000
    crlFiles = ["./crl-files/root.crl", "./crl-files/subordinate.crl", "./crl-files/tls.crl"]
  }
}

shell {
  sshdPort = 10002
  user = "testuser"
  password = "example-password"
}

```

#### Production Configuration

The example below shows a more production-like configuration of the Identity Manager. It is configured with an Issuance
and Revocation workflow, using JIRA workflows for CSR/CRR approvals, no local signer, and using SSL for secure communication between CENM services. In this scenario, all approved requests would be signed using an external signing
service (see [Signing Services](signing-service.md)).

```docker
address = "localhost:10000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
}

workflows {
    "issuance" = {
        type = ISSUANCE
        updateInterval = 1000
        enmListener {
            port = 5051
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
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCsrWorkflowPlugin"
            config {
                address = "https://doorman-jira-host.r3.com/"
                projectCode = "CSR"
                username = "example-jira-username"
                password = "example-jira-password"
            }
        }
    },
    "revocation" = {
        type = REVOCATION
        enmListener {
            port = 5052
            reconnect = true
            # note that this SSL configuration could use different keys to the above if desired
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
        plugin {
            pluginClass = "com.r3.enmplugins.jira.JiraCrrWorkflowPlugin"
            config {
                address = "https://doorman-jira-host.r3.com/"
                projectCode = "CRR"
                username = "example-jira-username"
                password = "example-jira-password"
            }
        }
        crlCacheTimeout = 2000
        crlFiles = ["./crl-files/root.crl", "./crl-files/subordinate.crl", "./crl-files/tls.crl"]
    }
}

shell {
    sshdPort = 10002
    user = "testuser"
    password = "example-password"
}

```
