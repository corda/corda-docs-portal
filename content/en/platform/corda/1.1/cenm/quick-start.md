---
aliases:
- /releases/release-1.1/quick-start.html
- /quick-start.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-1:
    identifier: cenm-1-1-quick-start
    parent: cenm-1-1-operations
    weight: 120
tags:
- quick
- start
title: Enterprise Network Manager Quick-Start Guide
---


# Enterprise Network Manager Quick-Start Guide



## Overview

The following is a simple step by step guide for creating a subzone, consisting of an **Identity Manager service**,
**Network Map service** and **Notary node**.


## Pre-Requisites


* The Identity Manager distribution zip
* The Network Map distribution zip
* The PKI Tool distribution zip *(for PKI generation)*
* A Corda jar *(for the Notary node)*
* 3 Machines setup with java 8 installed *(if not running locally)*.

{{< note >}}
Throughout this guide placeholder values for external endpoints are used (e.g. `<IDENTITY_MANAGER_ADDRESS>`).
These are dependent on the machine in which the service is running and should be replaced with the correct values.
For example, if running the network locally then this value will be the exact value of the `address` parameter
within the Identity Manager config file. Alternatively, if deploying the network in a cloud environment then this
value should be the external address of the machine along with any port defined in the `address` config parameter.

{{< /note >}}

## Steps


### Generate the PKI

Before starting any services, the PKI first needs to be generated. This involves creating the certificates and key pairs
for all ENM services and determines what entities the nodes will trust. More information on the certificate hierarchy
is available in the [Certificate Hierarchy Guide](pki-guide.md) doc.


#### Example Configuration

The following is an example configuration file (`pki-generation.conf`) using the placeholder
`<IDENTITY_MANAGER_ADDRESS>` value. This should be replaced with the actual value.

```guess
certificates = {
    "::CORDA_TLS_CRL_SIGNER" = {
        crl = {
            crlDistributionUrl = "http://<IDENTITY_MANAGER_ADDRESS>/certificate-revocation-list/tls"
            indirectIssuer = true
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

The above configuration is useful as, currently, if the certificates within the PKI are generated without the CRL
extension then they cannot be updated a later date. This means that if the PKI is generated without CRL extensions then
certificate revocation cannot be used. If certificate revocation will not be needed then the following simplified config
can be used:

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
The passwords for the key stores are defaulted to “password” and the passwords for the trust stores are
defaulted to “trustpass”. These can be changed in the configuration (see [Public Key Infrastructure (PKI) Tool](pki-tool.md)).

{{< /note >}}

#### Running The Tool

The required certificate stores and key pairs can be generated using the [Public Key Infrastructure (PKI) Tool](pki-tool.md). The PKI tool distribution zip
archive should be extracted to a chosen location, after which it can be run via:

```bash
java -jar pkitool.jar --config-file pki-generation.conf
```

This will produce a set of files, including the following:


* `key-stores/corda-identity-manager-keys.jks` - Contains the key pairs for the Identity Manager service *(used for
signing CSRs and CRRs)*
* `key-stores/corda-network-map-keys.jks` - Contains the key pairs for the Network Map service *(used for signing the
Network Map and Network Parameters)*
* `trust-stores/network-root-truststore.jks` - Contains the network root certificate and the TLS CRL signer
certificate *(used by nodes to verify that responses from other participants on the network are valid)*

If the PKI tool was ran with the first example config then a further set of crl files will have been created. Although
not needed to get a basic network up and running, these extra parts of the PKI can be used at a later date to make use
of more advanced features such as as certificate revocation support.


### Start the Identity Manager service

Before running the service, the Identity Manager jar along with the `corda-identity-manager-keys.jks` file should be
copied over to the Identity Manager machine (or directory location if running locally).


#### Example Configuration

The following is an example configuration (`identity-manager.conf`) for the Identity Manager service, using automatic
approval and local signing for CSRs:

```docker
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

{{< note >}}
The example uses a local h2 database. You can modify this to point to an separate DB instance by modifying the
`dataSourceProperties` section. See the “Database properties” section of [Identity Manager Service](identity-manager.md) for more
information.

{{< /note >}}

#### Running The Service

The Identity Manager service can then be ran via:

```bash
java -jar identitymanager.jar --config-file identity-manager.conf
```

Upon a successful startup the following should be printed to the console:

```guess
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <IDENTITY_MANAGER_ADDRESS> with [RegistrationWebService, MonitoringWebService]
```


### Register your Notary with the Identity Manager

Before the Network Map service can be initialised the Notary nodes first need to register with the Identity Manager.
This is because the list of trusted notaries is stored within the Network Parameters, which in turn need to be passed to
the Network Map service during initialisation.

The truststore containing the network root certificate (`network-root-truststore.jks`) should first be copied over to
the Notary machine along with a valid Corda jar (e.g. Corda OS 4.0).


#### Example Configuration

The following is an example `node.conf` file, with dummy values for the end points. These endpoints are dependent on
the setup of the machines so should be replaced with their true values (e.g. IPs addresses for machines).

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


#### Running Registration

```bash
java -jar corda.jar --initial-registration --network-root-truststore-password trustpass --network-root-truststore network-root-truststore.jks
```

This step should result in the node successfully registering with the Identity Manager, creating a node info file in the
process. This node info file is needed to initialise the network parameters, so should be copied over to the Network Map
machine.

{{< note >}}
The `--initial-registration` flag was deprecated in the most recent Corda version in favour of
`initial-registration` which may result in a warning being printed.

{{< /note >}}

### Set the initial network parameters

Before initialising the parameters, the `corda-network-map-keys.jks` and `network-root-truststore.jks` files should
be copied over to the Network Map machine, along with the Network Map distribution zip which should also be unpacked.

The network parameters are a set of values that every node participating in the zone needs to agree on and use to
correctly communicate with each other. Therefore they need to be set before the Network Map service can be started.
They are set via running the Network Map jar in a special “set network parameters” mode which requires a parameter
configuration file to be passed. Therefore this step requires both a Network Map service configuration and a network
parameters configuration. See [Updating the network parameters](updating-network-parameters.md) for more information around the processing of setting
and updating the parameters.


#### Example Configuration


##### Service

The following is an example configuration (`network-map.conf`) for the Network Map service, using automatic approval
and local signing for updates to the network map and parameters:

```docker
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
The example uses a local h2 database. You can modify this to point to an separate DB instance by modifying the
`dataSourceProperties` section. See the “Database properties” section of [Network Map Service](network-map.md) for more information.

{{< /note >}}

##### Network Parameters

The following is an example configuration file (`network-parameters.conf`) that is passed to the service when setting
the network parameters. Note that the <NOTARY_NODE_INFO_FILENAME> should correspond to the node info file copied across
during the previous step ([Register your Notary with the Identity Manager](#register-your-notary-with-the-identity-manager)).

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

The following command should initialise the network parameters, including the Notary node that was registered in the
previous step:

```bash
java -jar networkmap.jar --config-file network-map.conf --set-network-parameters network-parameters.conf --network-truststore network-root-truststore.jks --truststore-password trustpass --root-alias cordarootca
```

Upon successfully setting the initial parameters the following should be displayed to the console:

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


### Start the Network Map service

The Network Map service can then be ran via:

```bash
java -jar networkmap.jar --config-file network-map.conf
```

Upon a successful startup the following should be printed to the console:

```guess
Binding Shell SSHD server on port <SHELL_PORT>
Network management web services started on <NETWORK_MAP_ADDRESS> with [NetworkMapWebService, MonitoringWebService]
```


### Start your Notary service

The two main components of the Network should now be fully functional and hence the Notary node can be started:

```bash
java -jar corda.jar
```


## Further steps

Nodes should now be able to register and join the network. To do this they will need to have a node configuration file
similar to the example Notary configuration above (including the correct Network Map and Identity Manager endpoints) as
well as a copy of the `network-root-truststore.jks` file.

Each service can be inspected by utilising the interactive shell. For example, given the above configurations, the
Network Map shell can be accessed by connecting to the Network Map service via ssh, using the username, password and
port configured in the example `network-map.conf`. For example, if running a network locally then the following can be
used:

```bash
ssh testuser@localhost -p 20002
```

The above guide also assumes the simplest possible settings for all services. The services can be configured to run with
more features, in particular:


* Certificate revocation support (“Revocation workflow ” section within [Identity Manager Service](identity-manager.md))
* More advanced CSR approval workflows (“Certificate approval mechanism” section within [Identity Manager Service](identity-manager.md))
* External signing of CSRs/Network Map updates including HSM integration ([Signing Service](signing-service.md))

See the configuration sections within the [Identity Manager Service](identity-manager.md) and [Network Map Service](network-map.md) docs to learn more.
