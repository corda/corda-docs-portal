---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-firewall
tags:
- corda
- firewall
- upgrade
title: Firewall upgrade
weight: 2
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


{{< table >}}

|node.conf 3.x|node.conf 4.x|
|:------------------------------------------------|:------------------------------------------------|
|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf 3.x|firewall.conf 4.x|
|:---------------------------------------------------|:--------------------------------------------------|
|<pre>bridgeMode = SenderReceiver<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver:11005"<br>}<br>inboundConfig {<br>    listeningAddress = "bridgeexternal:10005"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|<pre>firewallMode = SenderReceiver<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver:11005"<br>}<br>inboundConfig {<br>    listeningAddress = "bridgeexternal:10005"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


### DMZ ready (node + bridge + float)


{{< table >}}

|node.conf 3.x|node.conf 4.x|
|:------------------------------------------------|:------------------------------------------------|
|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf - Bridge configuration 3.x|firewall.conf - Bridge configuration 4.x|
|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
|<pre>bridgeMode = BridgeInner<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver:11005"<br>}<br>bridgeInnerConfig {<br>    floatAddress = [ "dmzinternal:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    customSSLConfiguration {<br>        keyStorePassword = "bridgepass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./bridgecerts/bridge.jks"<br>        trustStoreFile = "./bridgecerts/trust.jks"<br>        crlCheckSoftFail = true<br>    }<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|<pre>firewallMode = BridgeInner<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver:11005"<br>}<br>bridgeInnerConfig {<br>    floatAddress = [ "dmzinternal:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    tunnelSSLConfiguration {<br>        keyStorePassword = "bridgepass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./bridgecerts/bridge.jks"<br>        trustStoreFile = "./bridgecerts/trust.jks"<br><br>    }<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf - Float configuration 3.x|firewall.conf - Float configuration 4.x|
|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
|<pre>bridgeMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    customSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br>        crlCheckSoftFail = true<br>    }<br>}<br>networkParametersPath = network-parameters<br></pre>|<pre>firewallMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    tunnelSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br><br>    }<br>}<br></pre>|

{{< /table >}}


### DMZ ready with outbound SOCKS

The changes for this deployment are the same as for **DMZ ready (node + bridge + float)** with the additional renaming of the
SOCKS configuration property from **socksProxyConfig** to **proxyConfig**.


### Full production HA DMZ ready (hot/cold node, hot/warm bridge)


{{< table >}}

|node.conf 3.x - Hot instance|node.conf 4.x - Hot instance|
|:------------------------------------------------|:------------------------------------------------|
|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver1:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver1:10006"<br>    adminAddress="nodeserver1:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>    mutualExclusionConfiguration = {<br>        on = true<br>        updateInterval = 20000<br>        waitInterval = 40000<br>    }<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver1:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver1:10006"<br>    adminAddress="nodeserver1:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>    mutualExclusionConfiguration = {<br>        on = true<br>        updateInterval = 20000<br>        waitInterval = 40000<br>    }<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|node.conf 3.x - Cold instance|node.conf 4.x - Cold instance|
|:------------------------------------------------|:------------------------------------------------|
|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver2:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver2:10006"<br>    adminAddress="nodeserver2:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>    mutualExclusionConfiguration = {<br>        on = true<br>        updateInterval = 20000<br>        waitInterval = 40000<br>    }<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver2:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver2:10006"<br>    adminAddress="nodeserver2:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>    mutualExclusionConfiguration = {<br>        on = true<br>        updateInterval = 20000<br>        waitInterval = 40000<br>    }<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf - Bridge configuration 3.x (same for every instance)|firewall.conf - Bridge configuration 4.x (same for every instance)|
|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
|<pre>bridgeMode = BridgeInner<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver1:11005"<br>    alternateArtemisBrokerAddresses = ["nodeserver2:11005"]<br>}<br>bridgeInnerConfig {<br>    floatAddress = [ "dmzinternal1:12005", "dmzinternal2:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    customSSLConfiguration {<br>        keyStorePassword = "bridgepass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./bridgecerts/bridge.jks"<br>        trustStoreFile = "./bridgecerts/trust.jks"<br>        crlCheckSoftFail = true<br>    }<br>}<br>haConfig {<br>   haConnectionString = "zk://zookeep1:11105,zk://zookeep2:11105,<br>                         zk://zookeep3:11105"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|<pre>firewallMode = BridgeInner<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver1:11005"<br>    alternateArtemisBrokerAddresses = ["nodeserver2:11005"]<br>}<br>bridgeInnerConfig {<br>    floatAddress = [ "dmzinternal1:12005", "dmzinternal2:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    tunnelSSLConfiguration {<br>        keyStorePassword = "bridgepass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./bridgecerts/bridge.jks"<br>        trustStoreFile = "./bridgecerts/trust.jks"<br><br>    }<br>}<br>haConfig {<br>   haConnectionString = "zk://zookeep1:11105,zk://zookeep2:11105,<br>                         zk://zookeep3:11105"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf - Float configuration 3.x hot instance|firewall.conf - Float configuration 4.x hot instance|
|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
|<pre>bridgeMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal1:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal1:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    customSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br>        crlCheckSoftFail = true<br>    }<br>}<br>networkParametersPath = network-parameters<br></pre>|<pre>firewallMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal1:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal1:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    tunnelSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br><br>    }<br>}<br></pre>|

{{< /table >}}


{{< table >}}

|bridge.conf - Float configuration 3.x warm instance|firewall.conf - Float configuration 4.x warm instance|
|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|
|<pre>bridgeMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal2:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal2:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    customSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br>        crlCheckSoftFail = true<br>    }<br>}<br>networkParametersPath = network-parameters<br></pre>|<pre>firewallMode = FloatOuter<br>inboundConfig {<br>    listeningAddress = "dmzexternal2:10005"<br>}<br>floatOuterConfig {<br>    floatAddress = [ "dmzinternal2:12005" ]<br>    expectedCertificateSubject = "CN=Float Local,O=Local Only,L=London,C=GB"<br>    tunnelSSLConfiguration {<br>        keyStorePassword = "floatpass"<br>        trustStorePassword = "trustpass"<br>        sslKeystore = "./floatcerts/float.jks"<br>        trustStoreFile = "./floatcerts/trust.jks"<br><br>    }<br>}<br></pre>|

{{< /table >}}


## Reconfiguring to the shared Corda Firewall Architecture

In 4.x, it is possible to for multiple nodes representing multiple identities to reside behind the same Corda Firewall.
To achieve this, the nodes can be configured to use an external Artemis server. Furthermore, the Artemis server can be run
in HA mode with replication and failback. Reconfiguring a node and bridge to use external artemis does not affect the float configuration,
therefore it will not be discussed.

Client connections to external Artemis require separate SSL key and trust stores. These can be created using the *ha-utilities* tool
For more information please see HA Utilities. There is also an example of keystore generation in
Firewall configuration under the *Artemis keystore generation* section.

For the purpose of this guide, the Artemis connection key and trust stores will be named *artemis.jks* and *artemis-truststore.jks*.
The machines hosting the Artemis instances are *artemisserver1* and *artemisserver2*.


### Node + Bridge to Node + Artemis + Bridge


{{< table >}}

|node.conf - Internal Artemis|node.conf - External Artemis (HA mode)|
|:------------------------------------------------|:----------------------------------------------------------------------|
|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="nodeserver:11005"<br>messagingServerExternal = false<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|<pre>myLegalName="O=Bank A,L=London,C=GB"<br>p2pAddress="banka.com:10005"<br>messagingServerAddress="artemisserver1:11005"<br>messagingServerExternal = true<br>rpcSettings {<br>    address="nodeserver:10006"<br>    adminAddress="nodeserver:10007"<br>}<br>enterpriseConfiguration = {<br>    messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"<br>    messagingServerBackupAddresses = ["artemisserver2:11005"]<br>    messagingServerSslConfiguration = {<br>                sslKeystore = artemis/artemis.jks<br>                keyStorePassword = artemisStorePass<br>                trustStoreFile = artemis/artemis-truststore.jks<br>                trustStorePassword = artemisTrustpass<br>    }<br>    externalBridge = true<br>}<br>keyStorePassword = "keyPass"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


{{< table >}}

|firewall.conf - Bridge Internal Artemis|firewall.conf - Bridge External Artemis|
|:---------------------------------------------------|:----------------------------------------------------------------------|
|<pre>firewallMode = SenderReceiver<br>outboundConfig {<br>    artemisBrokerAddress = "nodeserver:11005"<br>}<br>inboundConfig {<br>    listeningAddress = "bridgeexternal:10005"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/sslkeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|<pre>firewallMode = SenderReceiver<br>outboundConfig {<br>    artemisBrokerAddress = "artemisserver1:11005"<br>    alternateArtemisBrokerAddresses = [ "artemisserver2:11005" ]<br>    artemisSSLConfiguration {<br>        keyStorePassword = "artemisStorePass"<br>        trustStorePassword = "artemisTrustpass"<br>        sslKeystore = "artemis/artemis.jks"<br>        trustStoreFile = "artemis/artemis-truststore.jks"<br>    }<br>}<br>inboundConfig {<br>    listeningAddress = "bridgeexternal:10005"<br>}<br>networkParametersPath = network-parameters<br>sslKeystore = "./nodeCerts/unitedSslKeystore.jks"<br>keyStorePassword = "keyPass"<br>trustStoreFile = "./nodeCerts/truststore.jks"<br>trustStorePassword = "trustPass"<br></pre>|

{{< /table >}}


### Multiple nodes behind the Bridge

To add additional nodes behind the same Corda firewall (either all-in-one bridge or bridge and float), it’s sufficient
to configure the new nodes to connect to Artemis as shown in the previous section. The same applies for the bridge. The additional
nodes need to set their P2P address as the shared float’s address. Furthermore, all previous floats except the shared one need to be shut down.
