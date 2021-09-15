---
aliases:
- /quick-start.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-quick-start
    parent: cenm-1-4-operations
    weight: 120
tags:
- quick
- start
- trial
title: CENM test environment quick start guide
---


# Quick start guide to manual deployment of a CENM test environment

## Introduction

This guide provides a set of simple steps for creating a permissioned Corda network
consisting of the following:

* Identity Manager service
* Network Map service
* [Notary Service](../../corda-enterprise/4.5/notary/running-a-notary.md)

{{% important %}}
The deployment outlined here is significantly simplified compared to a full production
deployment.
{{% /important %}}

For a full production environment you would need to modify this deployment to add:

* A [Signing Service](signing-service.md) deployment to replace the built-in (local) signing component of the Identity Manager and Network Map Services.
* A [Zone Service](zone-service.md) deployment to manage configuration deployment.
* [Angel Services](angel-service.md) around the [Identity Manager](identity-manager.md), [Network Map](network-map.md),
  and Signing Services to fetch configurations from the Zone Service.
* An [Auth Service](auth-service.md) deployment to handle user authentication and authorisation.
* A [Gateway Service](gateway-service.md) deployment to act as a gateway from the user interface (CLI) to the back-end services.

### Prerequisites

Ensure you have copies of the following files (provided by R3), before creating your network:

* Identity Manager distribution `.zip`
* Network Map distribution `.zip`
* PKI Tool distribution `.zip` *(for PKI generation)*
* A Corda `.jar` *(for the Notary node)*
* 3 Machines set up with Java 8 installed *(if not running locally).*

{{< note >}}
Due to known issues when executing transactions between nodes, using Java `8u252` subversion is not recommended.

In this guide, we use placeholder values for external endpoints (for example, `<IDENTITY_MANAGER_ADDRESS>`).
They depend on the machine in which the service is running and should be replaced with the correct values.

If you are running the network locally, this value will match the `address` parameter
within the Identity Manager configuration file but if you are deploying the network in a
cloud environment, this value should be the external address of your machine along
with any port defined in the `address` configuration parameter.

{{< /note >}}

## Process

To create your permissioned network takes several steps:

1. Generate the PKI
2. Start the Identity Manager Service
3. Register the Notary with the Identity Manager Service
4. Sign the notary's identity
5. Set initial network parameters
6. Start the Network Map service
7. Start the Notary

These are described in detail below:

### Generate the PKI

You need to generate the PKI (key pairs and certificates each service will use)
first before starting any services.

{{< note >}}
For more information on the certificate hierarchy, see [Certificate Hierarchy Guide](pki-guide.md).
{{< /note >}}

#### Example Configuration

In the example below, the configuration file (`pki-generation.conf`) uses a placeholder value for
`<IDENTITY_MANAGER_ADDRESS>` which you should replace with the external IP/hostname of the Identity Manager Service.

```guess
certificates = {
    "::CORDA_TLS_CRL_SIGNER" = {
        crl = {
            crlDistributionUrl = "http://<IDENTITY_MANAGER_ADDRESS>/certificate-revocation-list/tls"
            indirectIssuer = true
            issuer = "CN=Test TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US"
            file = "./crl-files/tls.crl"
        }
    },
    "::CORDA_ROOT" = {
        crl = {
            crlDistributionUrl = "http://<IDENTITY_MANAGER_ADDRESS>/certificate-revocation-list/root"
            file = "./crl-files/root.crl"
        }
    }
    "::CORDA_SUBORDINATE" = {
        crl = {
            crlDistributionUrl = "http://<IDENTITY_MANAGER_ADDRESS>/certificate-revocation-list/subordinate"
            file = "./crl-files/subordinate.crl"
        }
    },
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP"
}
```

This configuration is useful if you want to generate the certificates in the PKI
without CRL extensions, which is simpler however you cannot update them later or
use certificate revocation. If you do not need to use certificate revocation,
use the following configuration:

```guess
certificates = {
    "::CORDA_TLS_CRL_SIGNER",
    "::CORDA_ROOT",
    "::CORDA_SUBORDINATE",
    "::CORDA_IDENTITY_MANAGER",
    "::CORDA_NETWORK_MAP"
}
```

{{< note >}}
The passwords for the key stores are defaulted to “password” and the passwords for the trust stores are defaulted to “trustpass”. To change them in the configuration setting, see [Public Key Infrastructure (PKI) Tool](pki-tool.md)).
{{< /note >}}

#### Run the PKI Tool

This step generates the required certificate stores and key pairs using the
[Public Key Infrastructure (PKI) Tool](pki-tool.md). You will need to
extract the PKI tool distribution zip archive to a chosen location, and run it
using a command such as:

    ```bash
    java -jar pkitool.jar --config-file pki-generation.conf
    ```

This will produce the following set of files:
* `key-stores/corda-identity-manager-keys.jks` - Contains the key pairs for the Identity Manager Service which are used for signing Certificate Signing Requests (CSRs) and Certificate Revocation Requests (CRRs)
* `key-stores/corda-network-map-keys.jks` - Contains the key pairs for the Network Map Service which are used for signing the Network Map and Network Parameters
* `trust-stores/network-root-truststore.jks` - Contains the network root certificate and the TLS CRL signing certificate which are used by nodes to verify that responses from other participants on the network are valid

If you run the PKI tool with the alternative example configuration with CRL enabled, a
further set of CRL files will be created under the `crl-stores/` folder.
Although these files are not required to get a basic network up and running,
additional functionalities such as certificate revocation support, will be
available for you to use when required.

### Start the Identity Manager Service

Extract the Zip archive containing the Identity Manager, then copy the
`key-stores/corda-identity-manager-keys.jks` generated by the PKI tool
to the Identity Manager host (or directory location if running locally).

#### Example Configuration

This example provides a sample configuration (`identity-manager.conf`) for the Identity Manager Service, using automatic
approval and local signing for CSRs:

```guess
address = "localhost:10000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
}

shell {
    sshdPort = 10002
    user = "testuser"
    password = "password"
}

localSigner {
    keyStore {
        file = corda-identity-manager-keys.jks
        password = "password"
    }
    keyAlias = "cordaidentitymanagerca"
    signInterval = 10000
    # This CRL parameter is not strictly needed. However if it is omitted, then revocation cannot be used in the future so it makes sense to leave it in.
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

{{< note >}}
The example uses a local H2 database. You can modify this to point to a separate database instance by modifying the `database` section.
See the “Database properties” section of [Identity Manager Service](identity-manager.md) for more information.
{{< /note >}}

### Run The Service

Start the Identity Manager Service via:

```bash
java -jar identitymanager.jar --config-file identity-manager.conf
```

You will see the following message printed to the console if your start-up is successful:

```guess
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <IDENTITY_MANAGER_ADDRESS> with [RegistrationWebService, MonitoringWebService]
```

### Register your Notary with the Identity Manager

You need to register the Notary with the Identity Manager Service before the Network
Map Service can be initialised. This is because the list of trusted notaries is
stored within the Network Parameters, which have to be passed to the Network Map Service during initialisation.

Copy the `trust-stores/network-root-truststore.jks` generated by the PKI tool
to the Notary host (or directory location if running locally),
along with a valid Corda `.jar` (e.g. Corda OS 4.5).

#### Example Configuration

This is an example `node.conf` file, with dummy values for the endpoints. As these endpoints are dependent on the setup of the machines, replace them with their true values (e.g. external IP addresses for machines).

```guess
myLegalName="O=NotaryA,L=London,C=GB"
notary {
    validating=false
}

networkServices {
  doormanURL="http://<IDENTITY_MANAGER_ADDRESS>"
  networkMapURL="http://<NETWORK_MAP_ADDRESS>"
}

devMode = false

sshd {
  port = 2222
}

p2pAddress="<NOTARY_HOST>:30000"
rpcUsers=[
  {
    user=testuser
    password=password
    permissions=[
        ALL
    ]
  }
]

rpcSettings {
  address = "<NOTARY_HOST>:30001"
  adminAddress = "<NOTARY_HOST>:30002"
}
```

#### Node registration

On first run you need to run the Corda node with the `--initial-registration`
parameter, as shown below:

```bash
java -jar corda.jar --initial-registration --network-root-truststore-password trustpass --network-root-truststore network-root-truststore.jks
```

This will result in the node registering with the Identity Manager, creating a node info file in the
process. In a production environment we would typically use a separate Signing service
and manually sign CSRs, however for this quick start the Identity Manager is
configured to use a local signer.

Copy the node info generated file to the Network Map machine, as it is needed for
initialising the network parameters.

    {{< note >}}
    The `--initial-registration` flag was deprecated in the most recent Corda version in favour of `initial-registration` which may result in a warning being printed.
    {{< /note >}}

### Network Map Service first run

Copy the `corda-network-map-keys.jks` and `network-root-truststore.jks`
files over to the Network Map host, along with the Network Map zip
archive which you will need to unpack.

Before starting the Network Map Service, you will need to set initial
network parameters. The network parameters are a set of values that every
node participating in the zone needs to agree on and use to correctly
communicate with each other. Setting the parameters is covered below, after
configuration of the service.

#### Example service configuration

This is a sample configuration (`network-map.conf`) for the Network Map Service, using automatic approval and local signing for updates to the network map and parameters:

```guess
address = "localhost:20000"

database {
    driverClassName = org.h2.Driver
    url = "jdbc:h2:file:./network-map-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
    user = "example-db-user"
    password = "example-db-password"
}

shell {
    sshdPort = 20002
    user = "testuser"
    password = "password"
}

localSigner {
    keyStore {
        file = corda-network-map-keys.jks
        password = "password"
    }
    keyAlias = "cordanetworkmap"
    signInterval = 10000
}

pollingInterval = 10000
checkRevocation = false

```

{{< note >}}
This example uses a local H2 database. You can modify this to point to a separate database instance by modifying the `database` section. See the “Database properties” section of [Network Map Service](network-map.md) for more information.

{{< /note >}}

#### Example network parameters configuration

This is a sample configuration file (`network-parameters.conf`) that is passed to the service when you set the network parameters. The <NOTARY_NODE_INFO_FILENAME> should correspond to the node info file copied across while [registering the Notary with the Identity Manager](#register-your-notary-with-the-identity-manager).
The configured path should be relative to the Network Map working directory.

```guess
notaries : [
  {
    notaryNodeInfoFile: <NOTARY_NODE_INFO_FILENAME>
    validating: false
  }
]
minimumPlatformVersion = 3
maxMessageSize = 10485760
maxTransactionSize = 10485760
eventHorizonDays = 30
```

#### Setting the initial network parameters

To set the network parameters we pass additional arguments when starting the
Network Map Service, as below:

```bash
java -jar networkmap.jar --config-file network-map.conf --set-network-parameters network-parameters.conf --network-truststore network-root-truststore.jks --truststore-password trustpass --root-alias cordarootca
```

Upon successfully setting the initial parameters, you will see the following details displayed to the console:

```guess
Saved initial network parameters to be signed:
NetworkParameters {
  minimumPlatformVersion=3
  notaries=[NotaryInfo(identity=O=NotaryA, L=London, C=GB, validating=false)]
  maxMessageSize=10485760
  maxTransactionSize=10485760
  whitelistedContractImplementations {

  }
  eventHorizon=PT720H
  modifiedTime=<ACTUAL_MODIFIED_TIME>
  epoch=1
}
```

See [Updating the network parameters](updating-network-parameters.md) for more information on the process for setting and updating the parameters.

### Start the Network Map Service

You can start the Network Map Service via:

```bash
java -jar networkmap.jar --config-file network-map.conf
```

Upon successful start-up, you will see the following details printed to the console:

```guess
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <NETWORK_MAP_ADDRESS> with [NetworkMapWebService, MonitoringWebService]
```

### Start your Notary node

The two main components of your network should now be fully functional and hence the Notary node can be started:

```bash
java -jar corda.jar
```

## Further steps

Nodes will now be able to register and join the network. To do this they will need to have a node configuration file
similar to the example Notary configuration above (including the correct Network Map and Identity Manager endpoints) as
well as a copy of the `network-root-truststore.jks` file.

You can inspect each service via its interactive shell. For example, for the above configurations, the
Network Map shell can be accessed by connecting to the Network Map service via `ssh`, using the following:
* username
* password
* port
as shown in the example `network-map.conf`.

Use the following command if running a network locally:

```bash
ssh testuser@localhost -p 20002
```
Note: For the purpose of this exercise, the simplest settings have been used for all the services. However, you can configure them to run with more features, such as the following:

* Certificate revocation support (“Revocation workflow ” section within [Identity Manager Service](identity-manager.md))
* More advanced CSR approval workflows (“Certificate approval mechanism” section within [Identity Manager Service](identity-manager.md))
* External signing of CSRs/Network Map updates including HSM integration ([Signing Service](signing-service.md))

{{< note >}}For more information, see the configuration sections within [Identity Manager Service](identity-manager.md) and [Network Map Service](network-map.md). {{< /note >}}

## Bundled Service alternative

You can simplify the steps mentioned above by using a single service which bundles multiple services together.
* To do this, download Bundled Service distribution ".zip" file. The Service configuration files will remain unchanged.

The standard run command form is generalised for running multiple services:

```bash
java -jar bundled.jar -f <conf_1> ... -f <conf_n> -S <service_1> ... -S <service_n>
```

For example, you can run Identity Manager and Network Map in parallel:

```bash
java -jar bundled.jar -f identity-manager.conf -f network-map.conf -S IDENTITY_MANAGER -S NETWORK_MAP
```

Upon successful start-up, you will see the following details printed to the console:

```guess
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <IDENTITY_MANAGER_ADDRESS> with [RegistrationWebService, MonitoringWebService]
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <NETWORK_MAP_ADDRESS> with [NetworkMapWebService, MonitoringWebService]
```

### Backward compatibility

You could also run this service as a template for one of the services you want to run. The Bundled service deduces which service to run from the configuration file, making this feature backward compatible with CENM 1.1.

For example, you can implicitly run the Identity Manager Service:

```bash
java -jar bundled.jar -f identity-manager.conf
```

Upon successful start-up, you should see the following details printed to the console:

```guess
Deduced Identity Manager Service from provided configuration file...
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <IDENTITY_MANAGER_ADDRESS> with [RegistrationWebService, CertificateRevocationWebService, MonitoringWebService]
```
