---
aliases:
- /releases/4.3/corda-firewall-configuration-file.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-corda-firewall-configuration-file
    parent: corda-enterprise-4-3-corda-firewall
    weight: 1020
tags:
- corda
- firewall
- configuration
- file
title: Firewall Configuration
---


# Firewall Configuration



## File location

When starting a standalone firewall (in bridge, or float mode), the `corda-firewall.jar` file defaults to reading the firewall’s configuration from a `firewall.conf` file in
the directory from which the command to launch the process is executed. The syntax is:

```bash
corda-firewall [-hvV] [--install-shell-extensions]
               [--logging-level=<loggingLevel>] [-b=<baseDirectory>]
               [-f=<_configFile>]
```

Where:


* `--config-file`, `-f`: Allows you to specify a configuration file with a different name, or at
a different file location. Paths are relative to the current working directory
* `--base-directory`, `-b`: Allows you to specify the firewall’s workspace location. A `firewall.conf`
configuration file is then expected in the root of this workspace
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--install-shell-extensions`: Install `corda-firewall` alias and auto completion for bash and zsh. See [Shell extensions for CLI Applications](cli-application-shell-extensions.md) for more info.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


## Format

The firewall configuration file uses the HOCON format which is superset of JSON. Please visit
[https://github.com/typesafehub/config/blob/master/HOCON.md](https://github.com/typesafehub/config/blob/master/HOCON.md) for further details.


{{< warning >}}
Please do NOT use double quotes (`"`) in configuration keys.

Bridge setup will log *Config files should not contain ” in property names. Please fix: [key]* as error
when it founds double quotes around keys.
This prevents configuration errors when mixing keys containing `.` wrapped with double quotes and without them

{{< /warning >}}



## Defaults

A set of default configuration options are loaded from the built-in resource file. Any options you do not specify in
your own `firewall.conf` file will use these defaults:

```javascript
healthCheck = true
keyStorePassword = "cordacadevpass"
trustStorePassword = "trustpass"
enableAMQPPacketTrace = false
artemisReconnectionIntervalMin = 5000
artemisReconnectionIntervalMax = 60000
politeShutdownPeriod = 1000
p2pConfirmationWindowSize = 1048576
auditServiceConfiguration : {
  loggingIntervalSec = 60
}
silencedIPs = []
useProxyForCrls = true
```

[firewalldefault_latest.conf](resources/bridge/firewalldefault_latest.conf)


## Firewall operating modes

{{< note >}}
By default, the Corda node assumes that it will carry out the peer-to-peer functions of the `bridge` internally!
Before running a dedicated firewall process, it is essential to turn off the dev mode component by setting the
`enterpriseConfiguration.externalBridge` property of the `node.conf` file to `true`.
If the `externalBridge` flag is not `true`, there will be unexpected behaviour as the node will try to send peer-to-peer messages directly!

{{< /note >}}
Assuming that an external firewall is to be used, the `corda-firewall.jar` operates in one of three basic operating modes.
The particular mode is selected via the required `firewallMode` configuration property inside `firewall.conf`:


* **SenderReceiver**:
selects a single process firewall solution to isolate the node and Artemis broker from direct Internet contact.
It is still assumed that the firewall process is behind a firewall, but both the message sending and receiving paths will pass via the `bridge`.
In this mode the `outboundConfig` and `inboundConfig` configuration sections of `firewall.conf` must be provided,
the `bridgeInnerConfig` and `floatOuterConfig` sections should not be present.


* **BridgeInner**:
mode runs this instance of the `corda-firewall.jar` as the trusted portion of the peer-to-peer firewall float.
Specifically, this process runs the complete outbound message processing. For the inbound path it operates only the filtering and durable storing portions of the message processing.
The process expects to connect through a firewall to a matched `FloatOuter` instance running in the DMZ as the actual `TLS 1.2/AMQP 1.0` termination point.


* **FloatOuter**:
causes this instance of the `corda-firewall.jar` to run as a protocol break proxy for inbound message path. The process
will initialise a `TLS` control port and await connection from the `BridgeInner`. Once the control connection is successful the `BridgeInner` will securely provision
the `TLS` socket server key and certificates into the `FloatOuter`. The process will then start listening for inbound connection from peer nodes.




## Fields

The configuration fields are listed in [Corda Enterprise Firewall configuration fields](corda-firewall-configuration-fields.md).


## Complete example

As an example to show all features, the following is a walk-through of the configuration steps to set-up a pair of HA hot-cold nodes for two separate legal identities,
connected to by a HA hot-warm set of `BridgeInner` and `FloatOuter` that use some simple certificates to secure the
control tunnel and a SOCKS5 proxy for outgoing connectivity (see diagram).
This is also the recommended full enterprise deployment pattern, although there are plenty of alternative deployment options.

Conceptually deployment will be done as follows:

![deployment concept](/en/images/deployment_concept.png "deployment concept")
In this example it is assumed that a large organisation is running two nodes that represent two distinct legal entities. Each node/entity has its own set of CorDapps installed
and its own transaction storage (vault). These two nodes are running within a Green/Trusted Zone and can be interacted with via RPC calls from clients (either standalone or embedded in other applications).
In order to be able to communicate outside of the organisation, special provisions are made in the form of Bridge, Float and SOCKS Proxy.

The following diagram illustrates physical deployment of the example setup discussed above:

![physical deployment](/en/images/physical_deployment.png "physical deployment")
{{< note >}}
The arrows on the diagram show in which direction connection is initiated. The actual data exchange may then be happening in both directions.

{{< /note >}}
In this example it is assumed that the Corda nodes are deployed on `vmNodesPrimary` and `vmNodesSecondary` using Azure SQL Server as clustered storage.

The Float instances run on `vmFloat1` and `vmFloat2` which are located in the DMZ.

The SOCKS5 proxy is running on `vmSocks` which also resides in the DMZ.

Each of the `vmInfra1` and `vmInfra2` computers host: ZooKeeper cluster participant, Bridge instance and Artemis cluster participant:

![Infra](/en/images/Infra.png "Infra")
To facilitate High Availability requirement deployment is split onto two data centers.

{{< note >}}
This document does not describe how to perform SOCKS5 setup. It is assumed that this type of proxy is correctly configured as part
of organisation’s IT infrastructure according to best practices/policies for outbound Internet connectivity. Other types of proxies are also supported
as well as no proxy at all. For more information please see [proxyConfig](#proxyconfig) parameter above.

{{< /note >}}


### Keystores generation

A special tool was created to simplify generation of the keystores. For more information please see [HA Utilities](ha-utilities.md).
This section explains how to generate a number of internally used keystores. Commands below can be executed on any machine as long as it will
be easy enough to copy results to the other machines including DMZ hosts.

It is also advisable to create an application user account (say `corda`) and use it instead of using own personal user.


{{< note >}}
All the `java -jar ...` commands below run so-called Fat Capsule Jar. This process involves up-packing content of the Fat Jar into temporary location.
By default it is set to `~/.capsule/apps/<APPLICATION_NAME>`. Application user setup may prevent creating directories and files at this location. To provide an
alternative, environment variable `CAPSULE_CACHE_DIR` can be used.

Capsule unpacks content of the Fat Jar only once and subsequent runs perform faster than initial one. However, in order to perform a clean run, it is advised to delete Capsule cache directory.

{{< /note >}}

#### Tunnel keystore generation

For Float and Bridge to communicate a tunnel keystore has to be created as follows:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar generate-internal-tunnel-ssl-keystores -p tunnelStorePass -e tunnelPrivateKeyPassword -t tunnelTrustpass
```

This should produce files: `tunnel/float.jks`, `tunnel/tunnel-truststore.jks` and `tunnel/bridge.jks` which will be used later on.


#### Artemis keystore generation

Bridge communicates to Artemis which requires a separate keystore.

Due to Artemis limitations the password for the keystore should be the same as the password for the private keys in the store. The tool below caters for these
arrangements. Artemis trust password can and should be different.

The tool should be used as follows:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar generate-internal-artemis-ssl-keystores -p artemisStorePass -t artemisTrustpass
```

This should produce files: `artemis/artemis-truststore.jks`, `artemis/artemis.jks` which will be used later on.


### Node VMs setup

As shown on the Physical deployment diagram above there will be two separate machines in two distinct data centres hosting Corda Nodes for Legal Entity A and Legal Entity B.
For this setup, each machine is powerful enough to host nodes for both entities with all the CorDapps and two datacentres are used for High Availability purposes.


#### Prerequisites


##### Corda Network connectivity

Before nodes can be configured, Corda Network administrator will need to provide:


* Network root trust store file: `network-root-truststore.jks` and password for it in this example assumed to be `trustpass`;
* Corda Network URL for Doorman e.g.: `http://r3-doorman:10001`;
* Corda Network URL for NetworkMap e.g.: `http://r3-netman:10001`


##### Nodes inbound connectivity provisions

In order for the nodes for both legal entities `Entity A` and `Entity B` to be reached from the outside of the organisation by other nodes, a **single** TCP endpoint
address is being exposed.

{{< note >}}
This is not a HTTP address! This endpoint address is what is known to be peer-to-peer (P2P) connectivity address for binary, non-human readable inbound data communication.
Therefore, there is little point pasting this address into any web-browser.

{{< /note >}}
In this example this address will be `banka.com:10005`.

From infrastructure point of view this can be address of a load balancer which will be routing network traffic to `vmFloat1` and `vmFloat2` hosts in the DMZ.

Out of `vmFloat1` and `vmFloat2` there will be at most one active host which will be accepting incoming communication. Therefore, load balancer will route inbound traffic to `vmFloat1` or `vmFloat2`.


##### Databases setup

Each legal entity is supposed to have it is own database(DB) schema in order to store Corda transaction data. Therefore `Entity A` and `Entity B`
should have different DB connectivity URLs.

For nodes’ High Availability(HA) functionality to work properly, databases the nodes connect to should be remote databases with transactional guarantees.
Please see [Hot-cold high availability deployment](hot-cold-deployment.md). I.e. HA nodes cannot be using local H2 database.

In the example below we will be using Azure SQL DB, however it can be any database Corda Enterprise supports.

Two empty schemas should be created for `Entity A` and `Entity B` and upon first startup of the node the necessary tables will be created automatically.


##### Base directory setup

Initially, the nodes configuration is performed on `vmNodesPrimary` host and then there is a special paragraph that details `vmNodesSecondary` setup.

Files `artemis/artemis.jks` and `artemis/artemis-truststore.jks` should be copied from [Artemis keystore generation](#artemis-keystore-generation) stage.

Corda FAT Jar `corda.jar` from Corda Enterprise distribution should also be copied into base directory.

Any CorDapps the node is meant to be working with should be installed into `cordapps` directory.


#### Creating node configuration files

Since there will be two distinct nodes serving two different legal entities they are meant to have two difference X.500 names, please see
`myLegalName` field in the config files below.

Also these two separate node may have different passwords to protected their keystore (`keyStorePassword`) and their trust store (`trustStorePassword`).

Suggested configuration for node serving `Entity A` on `vmNodesPrimary` would be a `entityA/node.conf` files containing:

```javascript
myLegalName = "O=Entity A,L=London,C=GB"
p2pAddress = "banka.com:10005" // Host and port exposed by Internet facing firewall/load balancer in front of float servers in DMZ.
messagingServerAddress = "vmInfra1:11005" // Specifying endpoints of remote Artemis instances, Note: SWAP1
messagingServerExternal = true // Specifying that it is an external instance
// Public keystore settings
keyStorePassword = "entityAStorePass"
trustStorePassword = "entityATrustPass"
// RPC settings
rpcSettings {
    address = "0.0.0.0:10006"
    adminAddress = "0.0.0.0:10026"
}
dataSourceProperties { // Point at clustered Azure SQL Server
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://entityAdb.database.windows.net:1433;databaseName=corda;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    dataSource.user = Corda
    dataSource.password = password
}
database {
    transactionIsolationLevel = READ_COMMITTED
    runMigration = false
    schema = dbo
}
security {
    authService {
        dataSource {
            type = INMEMORY
            users = [
                {
                    password = password
                    permissions = [
                        ALL
                    ]
                    username=user
                }
            ]
        }
    }
}
useTestClock = false
enterpriseConfiguration = {
    externalBridge = true // Ensure node doesn't run P2P AMQP bridge, instead delegate to the BridgeInner.
    messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
    messagingServerBackupAddresses = ["vmInfra2:11005"] // See "messagingServerAddress" above, Note: SWAP1
    mutualExclusionConfiguration = { // Enable the protective heartbeat logic so that only one node instance is ever running.
        on = true
        updateInterval = 20000
        waitInterval = 40000
    }
    messagingServerSslConfiguration = {
                sslKeystore = artemis/artemis.jks
                keyStorePassword = artemisStorePass
                trustStoreFile = artemis/artemis-truststore.jks
                trustStorePassword = artemisTrustpass
    }
}
networkServices {
    doormanURL = "http://r3-doorman:10001"
    networkMapURL = "http://r3-netman:10001"
}
devMode = false // Turn off things like key autogeneration and require proper doorman registration.
detectPublicIp = false // Do not perform any public IP lookup on the host.
sshd {
    port = 2222
}
```

For “sibling” node serving `Entity B` on `vmNodesPrimary` would be a `entityB/node.conf` file containing:

```javascript
myLegalName = "O=Entity B,L=London,C=GB"
p2pAddress = "banka.com:10005" // Host and port exposed by Internet facing firewall/load balancer in front of float servers in DMZ.
messagingServerAddress = "vmInfra1:11005" // Specifying endpoints of remote Artemis instances, Note: SWAP1
messagingServerExternal = true // Specifying that it is an external instance
// Public keystore settings
keyStorePassword = "entityBStorePass"
trustStorePassword = "entityBTrustPass"
// RPC settings
rpcSettings {
    address = "0.0.0.0:10106"
    adminAddress = "0.0.0.0:10126"
}
dataSourceProperties { // Point at clustered Azure SQL Server
    dataSourceClassName = "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    dataSource.url = "jdbc:sqlserver://entityAdb.database.windows.net:1433;databaseName=corda;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
    dataSource.user = Corda
    dataSource.password = password
}
database {
    transactionIsolationLevel = READ_COMMITTED
    runMigration = false
    schema = dbo
}
security {
    authService {
        dataSource {
            type = INMEMORY
            users = [
                {
                    password = password
                    permissions = [
                        ALL
                    ]
                    username=user
                }
            ]
        }
    }
}
useTestClock = false
enterpriseConfiguration = {
    externalBridge = true // Ensure node doesn't run P2P AMQP bridge, instead delegate to the BridgeInner.
    messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
    messagingServerBackupAddresses = ["vmInfra2:11005"] // See "messagingServerAddress" above, Note: SWAP1
    mutualExclusionConfiguration = { // Enable the protective heartbeat logic so that only one node instance is ever running.
        on = true
        updateInterval = 20000
        waitInterval = 40000
    }
    messagingServerSslConfiguration = {
                sslKeystore = artemis/artemis.jks
                keyStorePassword = artemisStorePass
                trustStoreFile = artemis/artemis-truststore.jks
                trustStorePassword = artemisTrustpass
    }
}
networkServices {
    doormanURL = "http://r3-doorman:10001"
    networkMapURL = "http://r3-netman:10001"
}
devMode = false // Turn off things like key autogeneration and require proper doorman registration.
detectPublicIp = false // Do not perform any public IP lookup on the host.
sshd {
    port = 2223
}
```


#### Nodes keystores generation

Given two configuration files above, in order to produce node keystores the following command should be used:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar node-registration --config-files=./entityA/node.conf --config-files=./entityB/node.conf --network-root-truststore=network-root-truststore.jks --network-root-truststore-password=trustpass
```

This call will process `node.conf` files and for each legal name performs Doorman registration. Depending on Corda Network configuration this process may require manual approval
and the program will poll for for Certification Signing Request(CSR) completion. For more information see [Joining an existing compatibility zone](joining-a-compatibility-zone.md).

After successful execution this will produce two directories `entityA/certificates` and `entityB/certificates` containing the following files:


* `truststore.jks`, the network/zone operator’s root certificate in keystore with a locally configurable password as protection against certain attacks;
* `nodekeystore.jks`, which stores the node’s identity key pairs and certificates;
* `sslkeystore.jks`, which stores the node’s TLS key pair and its certificate.

These are the keystores that will be used by each of the nodes.

Also, file called `network-parameters` will be produced which represents global parameters for this Corda Network.


{{< note >}}
Whenever communication needs to happen to NetworkMap or Doorman the process established *direct* HTTP (or HTTPS) connection with `doormanURL` or  `networkMapURL`.
Due to network firewall policy in place it might be necessary to specify proxy’s host and port for this connection to be successful.
Therefore when running Java command to start Capsule Jar it is necessary to add the following `-D` parameters.

```kotlin
-Dcapsule.jvm.args="-Dhttp.proxyHost=10.0.0.100 -Dhttp.proxyPort=8800 -Dhttps.proxyHost=10.0.0.100 -Dhttps.proxyPort=8800"
```

{{< /note >}}
Copy the `network-parameters` file and the artemis certificates into the `entityA` and `entityB` sub-directories which will then look as follows:

```kotlin
.
├── artemis
│   ├── artemis.jks
│   └── artemis-truststore.jks
├── certificates
│   ├── nodekeystore.jks
│   ├── sslkeystore.jks
│   └── truststore.jks
├── corda.jar
├── network-parameters
└── node.conf
```


#### CorDapps installation

In the node’s base directory create `cordapps` sub-directory and install all the required CorDapps you intend to work with.
In this example we are going to use Finance CorDapp which is supplied as part of Corda Enterprise distribution.


#### DB drivers installation

As discussed above each of the nodes will be using database to store node’s data. Corda Enterprise supports a number of databases, however in order
for a Corda Node to store its data in the DB, a JDBC driver needs to be installed into `drivers` sub-directory.

In this example we are using MSSql Server DB, therefore `mssql-jdbc-6.4.0.jre8.jar` will be installed.


#### Keystore aggregation for the Bridge

Since there is a single Bridge instance representing multiple nodes, it will need to have an aggregated SSL keystore representing all the nodes.
In order to produce such aggregated keystore, the following command should be used:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar import-ssl-key --bridge-keystore-password=bridgeKeyStorePassword --bridge-keystore=./nodesCertificates/nodesUnitedSslKeystore.jks --node-keystores=./entityA/certificates/sslkeystore.jks --node-keystore-passwords=entityAStorePass --node-keystores=./entityB/certificates/sslkeystore.jks --node-keystore-passwords=entityBStorePass
```

As a result `./nodesCertificates/nodesUnitedSslKeystore.jks` file will be produced containing 2 entries.


#### `vmNodeSecondary` setup

`vmNodeSecondary` is supposed to be an almost exact replica of `vmNodesPrimary` host. The only difference between those two machines that they are
residing in two different data centres for BCP purposes.

Since all the keystores been already created on `vmNodesPrimary` and nodes X.500 names been registered with Doorman, all it takes to clone `vmNodesPrimary` setup
onto `vmNodesSecondary` is to copy base directories with all the files recursively for `Entity A` and `Entity B`.

The only thing in node configuration files that ought to be changed is configuration of Artemis connectivity. This is needed to ensure DataCentre locality whenever possible.

See `SWAP1` note in the `node.conf` files.
For both nodes (`Entity A` and `Entity B`) configured on `vmNodeSecondary`:


* `messagingServerAddress` should be set to `vmInfra2:11005` ;
* `enterpriseConfiguration.messagingServerBackupAddresses` should be set to `["vmInfra1:11005"]`.


### Float VMs setup

It is advisable for each of the hosts `vmFloat1` and `vmFloat2` to be dual homed machines with two network interfaces. However, this is not mandated.
Addresses `vmFloat1-int` and `vmFloat2-int` are exposed to the internal trusted zone only.
The externally accessible addresses of the DMZ servers are `vmFloat1-ext` and `vmFloat2-ext`, which the Internet facing firewall/load balancer maps to `banka.com`.

Each of the `vmFloat1` and `vmFloat2` should have a base directory where Corda Firewall will be installed.

Configuration file: `firewall.conf` for `vmFloat1` should look as follows:

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "vmFloat1-ext:10005" // NB: Replace with "vmFloat2-ext:10005" on vmFloat2 host
}
floatOuterConfig {
    floatAddress = "vmFloat1-int:12005" // NB: Replace with "vmFloat2-int:12005" on vmFloat2 host
    expectedCertificateSubject = "CN=bridge, O=Corda, L=London, C=GB" // This X.500 name must align with name that Bridge received at the time of internal certificates generation.
    tunnelSSLConfiguration {
        keyStorePassword = "tunnelStorePass"
        keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
        trustStorePassword = "tunnelTrustpass"
        sslKeystore = "./tunnel/float.jks"
        trustStoreFile = "./tunnel/tunnel-truststore.jks"
    }
}
healthCheckPhrase = "HelloCorda"
```

Files `tunnel/float.jks` and `tunnel/tunnel-truststore.jks` should be copied from [Tunnel keystore generation](#tunnel-keystore-generation) stage.
`network-parameters` file should be copied from one of the node hosts, which has already been produced from [Nodes keystores generation](#nodes-keystores-generation) stage.

`corda-firewall.jar` is included into Corda Enterprise distribution and should be copied into base directory on `vmFloat1` and `vmFloat2` hosts.

For reference, base directory for `vmFloat1` and `vmFloat2` should look as follows:

```kotlin
.
├── corda-firewall.jar
├── firewall.conf
├── network-parameters
└── tunnel
    ├── float.jks
    └── tunnel-truststore.jks
```


### Infra VMs setup

`vmInfra1` and `vmInfra2` are hosting infrastructural processes which enable nodes to perform in/out communication with the rest of Corda Network.

The following process will be hosted by each of the VMs:


* Apache ZooKeeper cluster participant;
* Bridge instance;
* Artemis cluster participant.


#### Apache ZooKeeper setup

Apache ZooKeeper(ZK) is needed to facilitate leader election among two hot-warm Bridge Instances.
We require using version [3.5.4-beta](https://apache.org/dist/zookeeper/zookeeper-3.5.4-beta/zookeeper-3.5.4-beta.tar.gz) and have 3 cluster participants which will be hosted on `vmInfra1`, `vmInfra2` and `vmZkWitness`.

Assuming `/opt/corda` is the base directory for ZK instance on `vmInfra1` the following files needs to be created:


* `config/zoo1/zoo.cfg` containing:

```javascript
dataDir=/opt/corda/config/zoo1/
syncLimit=2
initLimit=5
tickTime=2000
dynamicConfigFile=/opt/corda/config/zoo1/zoo.cfg.dynamic
```

On `vmInfra2` `zoo1` should be replaced with `zoo2`.
On `vmZkWitness` `zoo1` should be replaced with `zoo3`


* `config/zoo1/zoo.cfg.dynamic` containing:

```javascript
server.1=vmInfra1:4000:4001:participant;10.155.0.5:11105
server.2=vmInfra2:4000:4001:participant;10.155.0.6:11105
server.3=vmZkWitness:4000:4001:participant;10.155.0.7:11105
```

`10.155.0.x` are assumed to be trusted zone corresponding IP addresses of each of the VMs.
The content of this file is identical across all 3 hosts: `vmInfra1`, `vmInfra2` and `vmZkWitness`.


* `config/zoo1/myid` containing:

```javascript
1
```

On `vmInfra2` it should contain `2`.

On `vmZkWitness` it should contain `3`.


#### Bridge instances setup

Base directory for Bridge instance should be created on each of the `vmInfra1` and `vmInfra2` hosts.

File copy from previous stages:


* Files `tunnel/bridge.jks` and `tunnel/tunnel-truststore.jks` should be copied from [Tunnel keystore generation](#tunnel-keystore-generation) stage.
* Files `artemis/artemis.jks` and `artemis/artemis-truststore.jks` should be copied from [Artemis keystore generation](#artemis-keystore-generation) stage.
* File `nodesCertificates/nodesUnitedSslKeystore.jks` should be copied from [Keystore aggregation for the Bridge](#keystore-aggregation-for-the-bridge) stage.
* File `network-root-truststore.jks`  along with the password to read this keystore provided by the CN owner.
* File `network-parameters` should be copied from [Nodes keystores generation](#nodes-keystores-generation) stage.

`corda-firewall.jar` is included into Corda Enterprise distribution and should be copied into Bridge base directory on `vmInfra1` and `vmInfra2` hosts.

Configuration file: `firewall.conf` for `vmInfra1` should look as follows:

```javascript
firewallMode = BridgeInner

// Public SSL settings
keyStorePassword = "bridgeKeyStorePassword"
sslKeystore = "nodesCertificates/nodesUnitedSslKeystore.jks"
trustStorePassword = "trustpass"
trustStoreFile = "nodesCertificates/network-root-truststore.jks"

outboundConfig {
    artemisBrokerAddress = "vmInfra1:11005" // NB: for vmInfra2 swap artemisBrokerAddress and alternateArtemisBrokerAddresses. Note: SWAP2
    alternateArtemisBrokerAddresses = ["vmInfra2:11005"] // Note: SWAP2
    proxyConfig {
       version = SOCKS5
       proxyAddress = "vmSocks:1080"
       userName = "proxyuser"
       password = "password"
    }

    artemisSSLConfiguration {
        keyStorePassword = "artemisStorePass"
        trustStorePassword = "artemisTrustpass"
        sslKeystore = "artemis/artemis.jks"
        trustStoreFile = "artemis/artemis-truststore.jks"
    }
}
bridgeInnerConfig {
    floatAddresses = ["vmFloat1:12005", "vmFloat2:12005"] // NB: for vmInfra2 change the ordering. Note: SWAP3
    expectedCertificateSubject = "CN=float, O=Corda, L=London, C=GB" // This X.500 name should match to the name of the Float component which was used during Tunnel keystore generation above.
    tunnelSSLConfiguration {
        keyStorePassword = "tunnelStorePass"
        keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
        trustStorePassword = "tunnelTrustpass"
        sslKeystore = "./tunnel/bridge.jks"
        trustStoreFile = "./tunnel/tunnel-truststore.jks"
    }
}
haConfig {
    haConnectionString = "zk://vmInfra1:11105,zk://vmInfra2:11105,zk://vmZkWitness:11105" // NB: for vmInfra2 change the ordering. Note: SWAP4
}
networkParametersPath = network-parameters // The network-parameters file is expected to be copied from the node registration phase and here is expected in the workspace folder.
```

For reference, base directory for the Bridge instance should look as follows:

```kotlin
.
├── artemis
│   ├── artemis.jks
│   └── artemis-truststore.jks
├── corda-firewall.jar
├── firewall.conf
├── network-parameters
├── nodesCertificates
│   ├── nodesUnitedSslKeystore.jks
│   └── network-root-truststore.jks
└── tunnel
    ├── bridge.jks
    └── tunnel-truststore.jks
```


#### Artemis cluster participant

Artemis will be deployed as a standalone process cluster and will be used as a communication bus for multiple applications(nodes and bridges). The required configuration files can be easily generated using
the `ha-utilities` command line tool. The tool can also install a configured Artemis instance provided that a distribution already exists. For the purpose of this example, commands are provided
to use the `ha-utilities` to install and configure 2 Artemis instances in HA mode.

`ha-utilities` with `configure-artemis` option will create two configurations for two processes known as `master` and `slave`. For more information please see:
[Artemis HA Documentation](https://activemq.apache.org/artemis/docs/latest/ha.html)

Apache Artemis distribution can be downloaded from [here](https://activemq.apache.org/artemis/download.html).

File copy from previous stages:


* Files `artemis/artemis.jks` and `artemis/artemis-truststore.jks` should be copied from [Artemis keystore generation](#artemis-keystore-generation) stage.

`vmInfra1` box will host Artemis `master` instance. To generate application distribution with the config files, please run:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar configure-artemis --install --distribution ${ARTEMIS_DISTRIBUTION_DIR} --path ${WORKING_DIR}/artemis-master --user "CN=artemis, O=Corda, L=London, C=GB" --ha MASTER --acceptor-address vmInfra1:11005 --keystore ./artemis/artemis.jks --keystore-password artemisStorePass --truststore ./artemis/artemis-truststore.jks --truststore-password artemisTrustpass --connectors vmInfra1:11005,vmInfra2:11005
```

Where `ARTEMIS_DISTRIBUTION_DIR` - is the path to the directory where Artemis was downloaded and extracted. Example: `/home/apache-artemis-2.6.3`

Files `artemis/artemis.jks` and `artemis/artemis-truststore.jks` from [Artemis keystore generation](#artemis-keystore-generation) stage need to be copied into `${WORKING_DIR}/artemis-master/etc/artemis`.

{{< note >}}
Due to the way Artemis handles connections in HA mode, the `.jks` files are configured with relative paths. This means that they will have to be installed in the same path relative to the bridge’s and node’s working directory.

{{< /note >}}

#### `vmInfra2` setup


##### `vmInfra2` Artemis cluster participant setup

Repeat steps from [Artemis cluster participant](#artemis-cluster-participant) section for `WORKING_DIR` creation as well as keystores copy and Apache Artemis distribution download.

`vmInfra2` box will host Artemis `slave` instance. To generate application distribution with the config files, please run:

```kotlin
java -jar corda-tools-ha-utilities-4.3.jar configure-artemis --install --distribution ${ARTEMIS_DISTRIBUTION_DIR} --path ${WORKING_DIR}/artemis-slave --user "CN=artemis, O=Corda, L=London, C=GB" --ha SLAVE --acceptor-address vmInfra2:11005 --keystore ./artemis/artemis.jks --keystore-password artemisStorePass --truststore ./artemis/artemis-truststore.jks --truststore-password artemisTrustpass --connectors vmInfra2:11005,vmInfra1:11005
```

Where `ARTEMIS_DISTRIBUTION_DIR` - is the path to the directory where Artemis was downloaded and extracted. Example: `/home/apache-artemis-2.6.3`

Files `artemis/artemis.jks` and `artemis/artemis-truststore.jks` from [Artemis keystore generation](#artemis-keystore-generation) stage need to be copied into `${WORKING_DIR}/artemis-slave/etc/artemis`.


##### `vmInfra2` Bridge instance setup

`vmInfra1` setup been done in the section above [Bridge instances setup](#bridge-instances-setup).

For `vmInfra2` the whole of base directory can be copied across to `vmInfra2` and then `firewall.conf` ought to be modified.

Please see `SWAP2`, `SWAP3` and `SWAP4` comments in the configuration file. The key principle here is to ensure DataCentre locality whenever possible,
making same DataCentre connection a priority. This applies to Artemis connection, Float connection and Zookeeper connection.


### Starting all up

Please see [Http Proxy Setup](#http-proxy-setup) note above on connectivity through the proxy.

Please see [Capsule Cache Directory](#capsule-cache-directory) note above explaining details of running Capsule Fat Jars.


#### Starting Float processes

In order to run each of the Float processes on `vmFloat1` and `vmFloat2`, in the base directory chosen during [Float VMs setup](#float-vms-setup), the following command should be executed:

```bash
nohup java –jar corda-firewall.jar &
```

{{< note >}}
When Float is started, since there is no Bridge connected to it yet, the Java process will be running but the Float will not be active yet and therefore
will not be accepting inbound connections.

{{< /note >}}
When Float instance is successfully started for the first time, the `logs` directory will be created in the base directory and the following line will show up in the log file:

```kotlin
[main] internal.FirewallStartup.startFirewall - Firewall started up and registered in 2.86 sec
```

In addition, traffic stats are logged every minute, like so:

```kotlin
Load average: 5%
Memory:
        Free: 75 MB
        Total: 200 MB
        Max: 200 MB
Traffic totals:
        Successful connection count: 1(inbound), 0(outgoing)
        Failed connection count: 1(inbound), 0(outgoing)
        Packets accepted count: 0(inbound), 0(outgoing)
        Bytes transmitted: 0(inbound), 0(outgoing)
        Packets dropped count: 0(inbound), 0(outgoing)
Traffic breakdown:
        Successful connections in:
                /13.80.124.64:57196 -> 1
        Failed connections in:
                /81.148.212.130:6546 -> 1
```


#### Starting Apache ZooKeeper processes

With configuration completed during [Apache ZooKeeper setup](#apache-zookeeper-setup) stage, start ZK instance using the following command in the base directory:

On `vmInfra1` host:

```bash
./zookeeper/bin/zkServer.sh --config /opt/corda/config/zoo1 start
```

On `vmInfra2` host:

```bash
./zookeeper/bin/zkServer.sh --config /opt/corda/config/zoo2 start
```

On `vmZkWitness` host:

```bash
./zookeeper/bin/zkServer.sh --config /opt/corda/config/zoo3 start
```

Every `zkServer.sh` start should report back to console with:

```kotlin
Starting zookeeper ... STARTED
```

After all ZooKeeper clusters have been successfully started on every host, execute:

```kotlin
./zookeeper/bin/zkServer.sh --config /opt/corda/config/zooX status
```

Where `zooX` is `zoo1` on `vmInfra1`, `zoo2` on `vmInfra2` and `zoo3` on `vmZkWitness`

Messages similar to the ones below should appear on two of the hosts indicating the `follower` status:

```kotlin
Using config: ./config/zoo3/zoo.cfg
Client port not found in static config file. Looking in dynamic config file.
Client port found: 11105. Client address: 10.155.0.8.
Mode: follower
```

Whereas on the remaining host, the `leader` status is indicated by:

```kotlin
Using config: ./config/zoo2/zoo.cfg
Client port not found in static config file. Looking in dynamic config file.
Client port found: 11105. Client address: 10.155.0.4.
Mode: leader
```


#### Starting Artemis cluster

In order to start Artemis, the following command should be issued for `master` on `vmInfra1`:

```kotlin
nohup ${WORKING_DIR}/artemis-master/bin/artemis run &
```

To confirm `master` has been successfully started, `nohup.out` file should contain:

```kotlin
AMQ221007: Server is now live
AMQ221001: Apache ActiveMQ Artemis Message Broker version 2.6.3 [0.0.0.0, nodeID=5df84d6f-0ea4-11e9-bdbf-000d3aba482b]
```

In order to start Artemis, the following command should be issued for `slave` on `vmInfra2`:

```kotlin
nohup ${WORKING_DIR}/artemis-slave/bin/artemis run &
```

To confirm `slave` has been successfully started, `nohup.out` file should contain:

```kotlin
AMQ221024: Backup server ActiveMQServerImpl::serverUUID=5df84d6f-0ea4-11e9-bdbf-000d3aba482b is synchronized with live-server.
AMQ221031: backup announced
```

In this example, `5df84d6f-0ea4-11e9-bdbf-000d3aba482b` is the cluster ID of the Artemis `master` instance.


#### Starting Bridge processes

There will be two Bridge instances running on `vmInfra1` and `vmInfra2`. They will be running in Hot-Warm mode whereby one on the processes
is active(leader) and the other one is running, but it a passive mode(follower).

Should primary process goes down or otherwise becomes unavailable, the stand-by process will take over. Apache Zookeper cluster will be used to ensure this leader transition process happens smoothly.

In order to run each of the Bridge processes the following command should be executed on `vmInfra1` and `vmInfra2`:

```bash
nohup java –jar corda-firewall.jar &
```

Checking any file in the logs folder should ideally reveal no `ERROR` nor `WARN` messages.
If bridge start-up sequence has been successful the following `INFO` level log messages should be observed for both Bridge instances:

```kotlin
artemis.BridgeArtemisConnectionServiceImpl.artemisReconnectionLoop - Session created
```

One of the Bridges will become a leader and should have the following in its log:

```kotlin
setting leadership to true; old value was false
...
Waiting for activation by at least one bridge control inbox registration
```


#### Domino effect

There is a concept of chained activation of the services which is often internally called the Domino effect.
When services are not activated they run as Java operating system processes, however they are dormant from data processing point of view.
E.g. Float service when not activated does not even have the port for inbound communication open. This makes perfect sense as underlying backend infrastructure
may not be running at all and if a message was received from the outside, it will not be able to route it correctly for processing.

Given ZK, Artemis, Bridge and Float running, but without any nodes started, the environment is largely in the dormant state.

When node starts the following happens:


* Node creates queues on the Artemis side;
* Using Artemis communication mechanism, the node sends a special activation message to the Bridge. In response to this message, the Bridge activates;
* Bridge then sends a special activation message to a Float via the tunnel communication channel;
* Float starts to listen for inbound communication (port 10005 in the example above) and this will make it available for processing traffic from the Internet facing loadbalancer.


#### Starting node processes

Each of the boxes `vmNodesPrimary` and `vmNodesSecondary` is capable of hosting both nodes for `Entity A` and `Entity B` at the same time.

`vmNodesPrimary` and `vmNodesSecondary` are meant to be located in different datacentres and in case when one of the datacentres is unavailable, the whole application plant will be running
on the other datacentre’s hardware.

In this setup Corda Nodes for each of the entities work in Hot-Cold mode. Which means that if the node is running on `vmNodesPrimary`, the node for the same identity on `vmNodesSecondary` cannot even be started.
For more information, please see [Hot-cold high availability deployment](hot-cold-deployment.md).

This implies that when starting nodes they should be running in re-start loop.

In order to start Corda Node normally on any of the hosts (`vmNodesPrimary` or `vmNodesSecondary`) for either of the entities (`Entity A` or `Entity B`) the following command should
be used from the base directory:

```bash
nohup bash -c 'while true; do java -jar corda.jar; done' &
```

Upon successful startup of primary nodes there should be no `ERROR` level lines in node logs. Once node’s startup sequence completes, the following line will be
printed in the logs:

```kotlin
Node for "Entity A" started up and registered in 35.58 sec
```

If the primary node is already running, secondary nodes will gracefully shutdown with the following lines in the logs:

```kotlin
[ERROR] PID: 7256 failed to become the master node. Check if /opt/corda/entityA/vmNodesPrimary, PID: 7593 is still running. Try again in PT40S
[INFO ] Will sleep for MutualExclusionConfiguration(on=true, machineName=vmNodesSecondary, updateInterval=20000, waitInterval=40000).waitInterval seconds till lease expires then shutting down this process.
```


### Performing basic health checks


#### Checking Float port is open

If the Domino effect happened successfully and all the services activated, one of the the Floats should be listening on port `10005`.
To check this is indeed the case, logon to `vmFloat1` or `vmFloat2` host and check that the port is bound:

```kotlin
lsof | grep 10005
```

This should produce a non-empty list of processes that are listening to this port.


#### Checking Float is reachable from the outside

Using a computer that is capable to perform external communication to the environment, run:

```kotlin
telnet banka.com 10005
```

Type `healthCheckPhrase` which is in our example - `HelloCorda`. Initially, no characters will be echoed back, however once you finish the phrase, it will be
echoed back in full to the terminal as well as any subsequent symbols that you type.

This will ensure that the Float can be contacted from the outside and is performing normally.


#### Running some flows

The ultimate test is of course running some flows.
it would make sense to check that `EntityA` can successfully talk to `Entity B`, as well as have some external node sending flows to `EntityA` and `Entity B`.

Desired effect is dependent on the CorDapps installed, however the Bridge and the Float will log some stats every minute detailing the number of messages relayed in every direction.
