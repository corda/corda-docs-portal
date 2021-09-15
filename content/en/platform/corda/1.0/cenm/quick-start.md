---
aliases:
- /releases/release-1.0/quick-start.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-quick-start
    parent: cenm-1-0-operations
    weight: 120
tags:
- quick
- start
title: Enterprise Network Manager Quick-Start Guide
---


# Enterprise Network Manager Quick-Start Guide



## Overview

The following is a simple step by step guide for creating a private network, consisting of a **Doorman service**,
**Network Map service** and **Notary node**.


## Pre-Requisites


* Machines setup with java 8 installed for each of the Doorman, Network Map and Notary services.
* The V0.4 Doorman jar *(for the Doorman and Network Map services)*
* The V0.4 Utilities jar *(for PKI generation)*
* A Corda jar *(for the Notary node)*

{{< note >}}
Throughout this guide placeholder values for endpoints are used (e.g. `<DOORMAN_HOST>`). These are dependent on
the machine in which the service is running and should be replaced with the correct values.

{{< /note >}}

## Steps


### Generate the PKI

Before starting any services, the PKI first needs to be generated. This involves creating the certificates and key pairs
for all ENM services, and determines what entities the nodes will trust. More information on the certificate hierarchy
is available in the certificate-hierarchy-generation doc.


#### Example Configuration

The following is an example configuration file (`pki-generation.conf`):

```kotlin
globalPassword = "example-password"
keyStore = {
    file = "./caKeyStore.jks"
}
certificatesStore = {
    file = "./certificateStore.jks"
}
networkTrustStore = {
    file = "./networkRootTrustStore.jks"
}
certificates = {
    "cordarootca" = {
        isSelfSigned = true
        subject = "CN=Corda Root Certificate, OU=Corda, O=Example HoldCo LLC, L=New York, C=US"
    },
    "cordatlscrlsigner" = {
        isSelfSigned = true
        issuesCertificates = false
        subject = "CN=Corda TLS Signer Certificate, OU=Corda, O=Example HoldCo LLC, L=New York, C=US"
    },
    "cordasubordinateca" = {
        signer = "cordarootca"
        subject = "CN=Corda Subordinate Certificate, OU=Corda, O=Example HoldCo LLC, L=New York, C=US"
    },
    "cordadoormanca" = {
        signer = "cordasubordinateca"
        role = DOORMAN_CA
        subject = "CN=Corda Doorman Certificate, OU=Corda, O=Example HoldCo LLC, L=New York, C=US"
    }
    "cordanetworkmap" = {
        signer = "cordasubordinateca"
        role = NETWORK_MAP
        issuesCertificates = false
        subject = "CN=Corda Network Map Certificate, OU=Corda, O=Example HoldCo LLC, L=New York, C=US"
    }
}
```

#### Running The Tool

The required certificate stores and key pairs can be generated using the tool-certificate-hierarchy-generator via
the utilities jar:

```bash
java -jar utilities.jar cert-hierarchy-generator --config-file pki-generation.conf
```

This will produce three things:


* `caKeyStore.jks` - Contains the key pairs for the Doorman and Network Map services *(used for signing Doorman and
Network Map related entities such as CSRs and Network Map changes)*
* `certificateStore.jks` - Contains all certificates for the relevant services. *(used by the Doorman and Network Map
services to validate certificate chains of other entities)*
* `networkRootTrustStore.jks` - Contains the root certificate *(used by the nodes to verify responses from other
participants on the network are valid, including responses from the Doorman and Network Map)*


### Start the Doorman service

Before running the service, the V0.3 Doorman jar along with the `certificateStore.jks` and `caKeyStore.jks` files
should be copied over to the Doorman machine.


#### Example Configuration

The following is an example configuration (`doorman.conf`) for the Doorman service, using automatic approval and local
signing for CSRs:

```kotlin
address = "<DOORMAN_HOST>:10000"

certificatesStoreFile = "certificateStore.jks"
certificatesStorePassword = "example-password"

dataSourceProperties {
  dataSourceClassName = org.h2.jdbcx.JdbcDataSource
  "dataSource.url" = "jdbc:h2:file:./doorman-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  "dataSource.user" = "example-user"
  "dataSource.password" = "example-password"
}

database {
  runMigration = true
}

doorman {
  updateInterval = 15000
  approveAll = true

  localSigner {
    keyStore {
      file = "caKeyStore.jks"
      password = "example-password"
    }
    keyPassword = "example-password"
    keyAlias = "cordadoormanca"
    signInterval = 15000
  }

  ezmListener {
    port = 10001
  }
}

# This section can be removed if the interactive shell is not required
shell {
  sshdPort = 10002
  user = "testuser"
  password = "example-password"
}

```

{{< note >}}
The example uses a local h2 database. You can modify this to point to an separate DB instance by modifying the
`dataSourceProperties` section. See the “Database properties” section of doorman for more information,
or see local-sqlserver-with-docker for information on how to run a local dockerized SQL server.

{{< /note >}}

#### Running The Service

The Doorman service can then be ran via:

```bash
java -jar doorman.jar --config-file doorman.conf --ignore-migration
```

Upon a successful startup the following should be printed to the console:

```guess
Binding Shell SSHD server on port 10002
Network management web services started on <DOORMAN_HOST>:10000 with [RegistrationWebService, MonitoringWebService]
```


### Register your Notary with the Doorman

Before the Network Map service can be initialised the Notary nodes first need to register with the Doorman. This is
because the list of trusted notaries is stored within the Network Parameters, which in turn need to be passed to the
Network Map service during initialisation.

The truststore containing the network root certificate (`networkRootTrustStore.jks`) should first be copied over to
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
  doormanURL="http://<DOORMAN_HOST>:10000"
  networkMapURL="http://<NETWORK_MAP_HOST>:20000"
}

devMode = false

sshd {
  port = 2222
}

p2pAddress="<NOTARY_HOST>:30000"
rpcUsers=[
  {
    user=testuser
    password=example-password
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
java -jar corda.jar --initial-registration --network-root-truststore-password example-password --network-root-truststore networkRootTrustStore.jks
```

This step should result in the node successfully registering with the Doorman, creating a node info file in the process.
This node info file is needed to initialise the network parameters, so should be copied over to the Network Map machine.

{{< note >}}
The `--initial-registration` flag was deprecated in the most recent Corda version in favour of
`initial-registration` which may result in a warning being printed.

{{< /note >}}

### Set the initial network parameters

Before initialising the parameters, the V0.3 Doorman jar along with the `certificateStore.jks` and `caKeyStore.jks`
files should be copied over to the Network Map machine. Note that both the Network Map and Doorman service’s are
currently bundled together within the single Doorman jar.

The network parameters are a set of values that every node participating in the zone needs to agree on and use to
correctly communicate with each other. Therefore they need to be set before the Network Map service can be started.
They are set via running the Doorman jar in a special “set network parameters” mode which requires a parameter
configuration file to be passed. Therefore this step requires both a Network Map service configuration and a network
parameters configuration. See [Updating the network parameters](updating-network-parameters.md) for more information around the processing of setting
and updating the parameters.


#### Example Configuration


##### Service

The following is an example configuration (`network-map.conf`) for the Network Map service, using automatic approval
and local signing for updates to the network map and parameters:

```kotlin
address = "<NETWORK_MAP_HOST>:20000"

certificatesStoreFile = "certificateStore.jks"
certificatesStorePassword = "example-password"

dataSourceProperties {
  dataSourceClassName = org.h2.jdbcx.JdbcDataSource
  "dataSource.url" = "jdbc:h2:file:./network-map-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  "dataSource.user" = "example-user"
  "dataSource.password" = "example-password"
}

database {
  runMigration = true
}

networkMap {
  cacheTimeout = 15000
  localSigner {
    keyStore {
      file = "caKeyStore.jks"
      password = "example-password"
    }
    keyPassword = "example-password"
    keyAlias = "cordanetworkmap"
    signInterval = 15000
  }

  ezmListener {
    port = 20001
  }

  checkRevocation = false
  privateNetworkAutoEnrolment = false
}

# This section can be removed if the interactive shell is not required
shell {
  sshdPort = 20002
  user = "testuser"
  password = "example-password"
}

```

{{< note >}}
The example uses a local h2 database. You can modify this to point to an separate DB instance by modifying the
`dataSourceProperties` section. See the “Database properties” section of [Network Map Service](network-map.md) for more information,
or see local-sqlserver-with-docker for information on how to run a local dockerized SQL server.

{{< /note >}}

##### Network Parameters

The following is an example configuration file (`network-parameters.conf`) that is passed to the service when setting
the network parameters. Note that the <NOTARY_NODE_INFO_FILENAME> should correspond to the node info file copied across
during the previous step ([Register your Notary with the Doorman](#register-your-notary-with-the-doorman)).

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
java -jar doorman.jar --config-file network-map.conf --set-network-parameters network-parameters.conf --network-truststore certificateStore.jks --truststore-password example-password --root-alias cordarootca --ignore-migration
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
java -jar doorman.jar --config-file network-map.conf
```

Upon a successful startup the following should be printed to the console:

```guess
Binding Shell SSHD server on port 20002
Network management web services started on <NETWORK_MAP_HOST>:20000 with [NetworkMapWebService, MonitoringWebService]
```

The service can also be validated


### Start your Notary service

The two main components of the Network should now be fully functional and hence the Notary node can be started:

```bash
java -jar corda.jar
```


## Further steps

Nodes should now be able to register and join the network. To do this they will need to have a node configuration file
similar to the example Notary configuration above (including the correct Network Map and Doorman endpoints) as well as
a copy of the `networkRootTrustStore.jks` file.

Each service can be inspected by utilising the interactive shell. For example, given the above configurations, the
Doorman shell can be accessed by connecting to then Doorman service via ssh, using the username, password and port
configured in the example `doorman.conf`:

```bash
ssh testuser@<DOORMAN_HOST> -p 10001
```

The above guide also assumes the simplest possible settings for all services. The services can be configured to run with
more features, in particular:


* Certificate revocation (revocation)
* CSR approval workflows (“Certificate approval mechanism” section within doorman)
* External signing of CSRs/Network Map updates including HSM integration ([Signing Service](signing-service.md))
* Private networks within the Network Map service ([Private Network Map](private-network-map.md))

See the configuration sections within the doorman and [Network Map Service](network-map.md) docs to learn more.
