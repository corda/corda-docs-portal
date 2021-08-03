---
aliases:
- /releases/release-1.2/identity-manager.html
- /docs/cenm/head/identity-manager.html
- /docs/cenm/identity-manager.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-identity-manager
    parent: cenm-1-2-operations
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
* **Revocation**: *(Optional)* Responsible for handling certificate revocation requests as well as hosting the CRLendpoints that are used by participants to check a certificate’s revocation status.


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
certificates, config files etc. should be under the working directory.
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



{{< note >}}
See [Identity Manager Configuration Parameters](config-identity-manager-parameters.md) for a detailed explanation about each possible parameter.

{{< /note >}}

### Address

The `address` parameter must be included in the top level of the configuration and represents the host and port
number that the Identity Service will bind to upon startup. The host can either be the IP address or the hostname of
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

The Identity Manager service is backed by a SQL database which it uses to store information such as Certificate Signing
Requests (CSRs) and (optionally) Certificate Revocation Requests (CRRs). The connection settings must be included within
the `database` configuration block in the config file. The main options that should be included here are:


* `driverClassName` - the DB driver class name (e.g *com.microsoft.sqlserver.jdbc.SQLServerDriver* for Microsoft SQL Server, *org.postgresql.Driver* for postgres)
* `jdbcDriver` - the path to the appropriate JDBC driver jar (e.g *path/to/mssql-jdbc-7.2.2.jre8.jar*)
* `url` - the connection string for the DB
* `user` - the username for the DB
* `password` - the password for the DB


#### Database Setup

The database can either be setup prior to running the Identity Manager service or, alternatively, it can be
automatically prepared on startup via the built-in migrations. To enable the running of database migrations on startup
the optional `runMigration` parameter within the `database` configuration should be set to true. Additionally, if
the Identity Manager service is being run using the same DB instance as an accompanying Network Map service then the
Identity Manager schema name must be specified via the `schema` parameter within the `database` configuration block:

```guess
database {
    ...
    runMigration = true
    schema = identity_manager
}
```

{{< note >}}
Due to the way the migrations are defined, if the Identity Manager and Network Map services are using the same
DB instance then they *must* use separate DB schemas. For more information regarding the supported databases
along with the schema see [CENM Databases](database-set-up.md).

{{< /note >}}

#### Additional Properties

Additional database properties can be loaded by including an optional *additionalProperties* config block. In CENM 1.0
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

An example configuration for an Identity Manager service using a Microsoft SQL Server database, configured to run the
migrations on startup is:

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
within the Issuance workflow inside the Identity Manager’s config file. The CENM currently ships with two included
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


This mechanism can be enabled by referencing the auto approval workflow plugin within the config file:

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

The Identity Manager service can use JIRA to manage the certificate signing request approval work flow. This can be
enabled by referencing the JIRA CSR workflow plugin within the config file along with the associated configuration
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

To enable the local signer, the top level `localSigner` configuration block should be added to the config file:

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


#### Issuance Internal Server

Similarly to the other ENM services, the Identity Manager is designed to be able to communicate between other services
such as the Network Map and Signing services. Both the Issuance and, optionally, the Revocation workflows have their own
internal listening server that is created on startup which can receive and respond to messages from other ENM services.
For example, the Revocation workflow’s ENM listener can respond to messages from the Network Map regarding certificate
statuses of current participants which the Network Map service will then use when refreshing the latest Network Map.

To configure this internal server, the configuration block `enmListener` should be added within the Issuance
workflow’s config:

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
All inter-service communication can be configured with SSL support. See [Configuring the ENM services to use SSL](enm-with-ssl.md).

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
the Network Map service configuration. However, unlike the other two options, as it prevents an outdated node
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

The Revocation workflow is the second of the two main components in the Identity Manager service. It is an optional
component that is responsible for handling incoming Certificate Revocation Requests (CRRs) to revoke a node’s
certificate (acquired via a previously approved CSR) as well as hosting the Certificate Revocation Lists (CRLs) to
enable the participants on the network to verify the validity of other’s certificates.

Similarly to the Issuance workflow, the Revocation workflow determines how a CRR gets approved and signed.


#### CRR Approval Mechanism

In order to revoke a node’s certificate and therefore be evicted from the network, a CRR needs to be approved and signed
by the network operator. The method by which the CRR is approved is, similar to the Issuance workflow, configured by
specifying the plugin class responsible for the handling of the CRRs within the Revocation workflow inside the Identity
Manager’s config file. The CENM ships with two included plugins:


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


This mechanism can be enabled by referencing the auto approval workflow plugin within the config file:

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
CRR workflow plugin within the config file along with the associated configuration parameters:

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
block `enmListener` should be added within the Revocation workflow’s config:

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
All inter-service communication can be configured with SSL support. See [Configuring the ENM services to use SSL](enm-with-ssl.md).

{{< /note >}}

#### CRL Configuration

There are an additional two parameters that need to be specified with the revocation workflow config block:


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
a required element of the config that can be set to any invalid string should they wish to not provide it.


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

Below is an example of a more production-like configuration of the Identity Manager. It is configured with a Issuance
and Revocation workflow, using JIRA workflows for CSR/CRR approvals, no local signer and also using SSL for secure
communication between ENM services. In this scenario, all approved requests would be signed using an external signing
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
