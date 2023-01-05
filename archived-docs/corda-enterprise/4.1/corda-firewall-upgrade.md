---
aliases:
- /releases/4.1/corda-firewall-upgrade.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-corda-firewall-upgrade
    parent: corda-enterprise-4-1-corda-firewall
    weight: 1030
tags:
- corda
- firewall
- upgrade
title: Firewall upgrade
---


# Firewall upgrade



## Introduction

Corda Firewall 4.x brings with it an few changes, some related to deployment and configuration. The first part of the guide
covers the upgrade of existing firewall deployments, from the simplest operating mode to the full HA DMZ ready mode. For
more information on supported operating modes please see [Operating modes of the Bridge and Float](corda-firewall-component.md).
The **Embedded Developer Node** is left out as it is not impacted. The second part explains the steps to evolve the upgraded
environments to use the new 4.x features such as standalone Artemis with HA and shared bridge. For consistency, this guide uses the same
hostname and port values as main firewall guide.


## Upgrade

When upgrading, it’s important to note that one of the main configuration differences is the renaming of all terms containing *bridge*
to use *firewall*. This applies to the configuration files for the bridge and float which are now called *firewall.conf*.
There are properties which have been renamed or reworked, such as *customSSLConfiguration* which was previously
used to override SSL configuration for bridge-to-artemis or bridge-to-float connections. For more information on the new properties, please see
Firewall configuration.
One other major change is the binary file name has changed from  **corda-bridgeserver.jar** to **corda-firewall.jar**. Any existing deployment
scripts will require updating as well.


### Node + Bridge (no float, no DMZ)

For this type of deployment, version 3.x would have the following configuration:

#### Node configuration

Corda 3.x

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {
    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

Corda 4.x

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {
    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

#### Bridge configuration

Corda 3.x

```javascript
bridgeMode = SenderReceiver
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
inboundConfig {
    listeningAddress = "bridgeexternal:10005"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

Corda 4.x

```javascript
firewallMode = SenderReceiver
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
inboundConfig {
    listeningAddress = "bridgeexternal:10005"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

### DMZ ready (node + bridge + float)

#### Node configuration

Corda 3.x

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {
    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

Corda 4.x

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {
    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```
#### Bridge configuration

Corda 3.x

```javascript
bridgeMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
bridgeInnerConfig {
    floatAddress = [ "dmzinternal:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    customSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

Corda 4.x

```javascript
firewallMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
bridgeInnerConfig {
    floatAddress = [ "dmzinternal:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"

    }
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

#### Float configuration

Corda 3.x

```javascript
bridgeMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    customSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
```

Corda 4.x

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"

    }
}
```

## DMZ ready with outbound SOCKS

The changes for this deployment are the same as for **DMZ ready (node + bridge + float)** with the additional renaming of the
SOCKS configuration property from **socksProxyConfig** to **proxyConfig**.

### Full production HA DMZ ready (hot/cold node, hot/warm bridge)

#### node.conf 3.x - Hot instance


```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver1:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver1:10006"
    adminAddress="nodeserver1:10007"
}
enterpriseConfiguration = {
	  externalBridge = true
    mutualExclusionConfiguration = {
        on = true
        updateInterval = 20000
        waitInterval = 40000
    }
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

#### node.conf 4.x - Hot instance

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver1:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver1:10006"
    adminAddress="nodeserver1:10007"
}
enterpriseConfiguration = {
    externalBridge = true
    mutualExclusionConfiguration = {
        on = true
        updateInterval = 20000
        waitInterval = 40000
    }
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```


#### node.conf 3.x - Cold instance

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver2:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver2:10006"
    adminAddress="nodeserver2:10007"
}
enterpriseConfiguration = {
	  externalBridge = true
    mutualExclusionConfiguration = {
        on = true
        updateInterval = 20000
        waitInterval = 40000
    }
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

#### node.conf 4.x - Cold instance

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver2:11005"
messagingServerExternal = false
rpcSettings {
   address="nodeserver2:10006"
   adminAddress="nodeserver2:10007"
}
enterpriseConfiguration = {
   externalBridge = true
   mutualExclusionConfiguration = {
       on = true
       updateInterval = 20000
       waitInterval = 40000
   }
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```



#### bridge.conf - Bridge configuration 3.x (same for every instance)

```javascript
bridgeMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver1:11005"
    alternateArtemisBrokerAddresses = ["nodeserver2:11005"]
}
bridgeInnerConfig {
    floatAddress = [ "dmzinternal1:12005", "dmzinternal2:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    customSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"
        crlCheckSoftFail = true
    }
}
haConfig {
   haConnectionString = "zk://zookeep1:11105,zk://zookeep2:11105,
                         zk://zookeep3:11105"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

#### firewall.conf - Bridge configuration 4.x (same for every instance)

```javascript
firewallMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver1:11005"
    alternateArtemisBrokerAddresses = ["nodeserver2:11005"]
}
bridgeInnerConfig {
    floatAddress = [ "dmzinternal1:12005", "dmzinternal2:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"        crlCheckSoftFail = true
    }
}
haConfig {
   haConnectionString = "zk://zookeep1:11105,zk://zookeep2:11105,
                         zk://zookeep3:11105"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

#### bridge.conf - Float configuration 3.x hot instance

```javascript
bridgeMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal1:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal1:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    customSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
```

#### firewall.conf - Float configuration 4.x hot instance

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal1:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal1:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
```


#### bridge.conf - Float configuration 3.x warm instance

```javascript
bridgeMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal2:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal2:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    customSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
```

#### firewall.conf - Float configuration 4.x warm instance

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal2:10005"
}
floatOuterConfig {
    floatAddress = [ "dmzinternal2:12005" ]
    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
        crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters
```


## Reconfiguring to the shared Corda Firewall Architecture

In 4.x, it is possible to for multiple nodes representing multiple identities to reside behind the same Corda Firewall.
To achieve this, the nodes can be configured to use an external Artemis server. Furthermore, the Artemis server can be run
in HA mode with replication and failback. Reconfiguring a node and bridge to use external artemis does not affect the float configuration,
therefore it will not be discussed.

Client connections to external Artemis require separate SSL key and trust stores. These can be created using the *ha-utilities* tool
For more information please see [HA Utilities](ha-utilities.md). There is also an example of keystore generation in
Firewall configuration under the *Artemis keystore generation* section.

For the purpose of this guide, the Artemis connection key and trust stores will be named *artemis.jks* and *artemis-truststore.jks*.
The machines hosting the Artemis instances are *artemisserver1* and *artemisserver2*.

### Node + Bridge to Node + Artemis + Bridge


#### node.conf - Internal Artemis

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="nodeserver:11005"
messagingServerExternal = false
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {








    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```

#### node.conf - External Artemis (HA mode)

```javascript
myLegalName="O=Bank A,L=London,C=GB"
p2pAddress="banka.com:10005"
messagingServerAddress="artemisserver1:11005"
messagingServerExternal = true
rpcSettings {
    address="nodeserver:10006"
    adminAddress="nodeserver:10007"
}
enterpriseConfiguration = {
    messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
    messagingServerBackupAddresses = ["artemisserver2:11005"]
    messagingServerSslConfiguration = {
                sslKeystore = artemis/artemis.jks
                keyStorePassword = artemisStorePass
                trustStoreFile = artemis/artemis-truststore.jks
                trustStorePassword = artemisTrustpass
    }
    externalBridge = true
}
keyStorePassword = "keyPass"
trustStorePassword = "trustPass"
```



#### firewall.conf - Bridge Internal Artemis

```javascript
firewallMode = SenderReceiver
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"








}
inboundConfig {
    listeningAddress = "bridgeexternal:10005"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/sslkeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

#### firewall.conf - Bridge External Artemis

```javascript
firewallMode = SenderReceiver
outboundConfig {
 artemisBrokerAddress = "artemisserver1:11005"
 alternateArtemisBrokerAddresses = [ "artemisserver2:11005" ]
 artemisSSLConfiguration {
     keyStorePassword = "artemisStorePass"
     trustStorePassword = "artemisTrustpass"
     sslKeystore = "artemis/artemis.jks"
     trustStoreFile = "artemis/artemis-truststore.jks"
     crlCheckSoftFail = true
 }
}
inboundConfig {
 listeningAddress = "bridgeexternal:10005"
}
networkParametersPath = network-parameters
sslKeystore = "./nodeCerts/unitedSslKeystore.jks"
keyStorePassword = "keyPass"
trustStoreFile = "./nodeCerts/truststore.jks"
trustStorePassword = "trustPass"
```

### Multiple nodes behind the Bridge


To add additional nodes behind the same Corda firewall (either all-in-one bridge or bridge and float), it's sufficient
to configure the new nodes to connect to Artemis as shown in the previous section. The same applies for the bridge. The additional
nodes need to set their P2P address as the shared float's address. Furthermore, all previous floats except the shared one need to be shut down.
