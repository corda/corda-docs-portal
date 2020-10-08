---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-firewall
    name: "Corda Enterprise Firewall"
    parent: corda-enterprise-4-6-corda-nodes
tags:
- corda
- firewall
- component
title: Firewall component overview
weight: 64
---


# Firewall component overview

The Corda Firewall (bridge/float) component is designed for enterprise deployments and acts as an application-level
firewall and protocol break on all internet-facing endpoints. The `corda-firewall.jar` encapsulates the peer
network functionality of the basic Corda Enterprise node, so that it can be operated separately from the security sensitive
JVM runtime of the node. This gives separation of functionality and ensures that the legal identity keys are not
used in the same process as the internet TLS connections. Only the bridge component is initiating connections to the
float further increasing the isolation of the node’s internet access point. Also, it adds support for enterprise deployment
requirements, such as High Availability (HA) and SOCKS proxy support. The firewall can also serve two or more nodes, thus reducing
the deployment complexity of multiple nodes in the same network.

This document is intended to provide an overview of the architecture and options available.


## Terminology

The component referred to here as the *bridge* is the library of code responsible for managing outgoing links to peer
nodes and implements the AMQP 1.0 protocol over TLS 1.2 between peers to provide reliable flow message delivery. This
component can be run as a simple integrated feature of the node. However, for enhanced security and features in Corda
Enterprise, the in-node version should be turned off and a standalone and HA version can be run from the
`corda-firewall.jar`, possibly integrating with a SOCKS proxy.

The *float* component refers to the inbound socket listener, packet filtering and DMZ compatible component. In the
simple all-in-one node, all inbound peer connections terminate directly onto an embedded Artemis broker component
hosted within the node. The connection authentication and packet filtering is managed directly via Artemis
permission controls managed directly inside the node JVM. For Corda Enterprise deployments, we provide a more
secure and configurable isolation component that is available using code inside `corda-firewall.jar`. This
component is designed to provide a clear protocol break and thus prevents the node and Artemis server ever being
directly exposed to peers. For simpler deployments with no DMZ, the float and bridge logic can also be run as a
single application behind the firewall, but still protecting the node and hosted Artemis. It is also possible to host
the Artemis server out of process and shared across nodes, but this will be transparent to peers as the interchange
protocol will continue to be AMQP 1.0 over TLS.

{{< note >}}
All deployment modes of the bridge, float, or all-in-one node are transparently interoperable, if correctly configured.

{{< /note >}}

## Message path between peer nodes

When a flow within a node needs to send a message to a peer, there is a carefully orchestrated sequence of steps to ensure
correct secure routing based upon the network map information and to ensure safe, restartable delivery to the remote flow.
Adding the bridge and float to this process adds some extra steps and security checking of the messages.
The complete sequence is therefore:


* The flow calls `send`, or `sendAndReceive` to propagate a message to a peer. This leads to checkpointing
of the flow fiber within the `StateMachine` and posting the message to the internal `MessagingService`. This ensures that
the send activity will be retried if there are any errors before further durable transmission of the message.
* The `MessagingService` checks if this is a new destination node and if an existing out queue and bridge exists in Artemis.
If the durable out queue does not exist, then this will need to be created in Artemis:
* First, the durable queue needs to be created in the peer-to-peer Artemis. Each queue is uniquely named based upon the hash of the
legal identity `PublicKey` of the target node.
* Once the queue creation is complete, a bridge creation request is also published to the Artemis bus via the bridge control protocol.
This message uses information from the network map to link the out queue to the target host and port and TLS credentials.
The flow does not need to wait for any response at this point and can carry on to send messages to the Artemis out queue.
* The bridge process monitors all the queues and as soon as the message is published to one of the queues, the bridge opens a TLS connection
to the remote peer (optionally, this connection can be made via a SOCKS4/5 proxy).
Upon connection, the two ends of the TLS link exchange certificate details
and confirm that the certificate path is anchored at the network root certificate and that the X500 subject matches
the expected target as specified in the create bridge message using details contained in the network map.
The links are long lived so as to reduce the setup cost of the P2P messaging.
* If the outgoing TLS 1.2 link is created successfully, then the bridge opens a consumer on the Artemis out queue.
The pending messages will then be transferred to the remote destination using AMQP 1.0, with final removal from the
out queue only occurring when the remote end fully acknowledges safe message receipt. This ensures at least once
delivery semantics.
* Note that at startup of either the node or the bridge, the bridge control protocol resynchronises the bridging state,
so that all out queues have an active bridge.
* Assuming an out queue exists, the message can be posted to Artemis and the bridge should eventually deliver this
message to the remote system.
* On receipt of a message acknowledge from Artemis, the `StateMachine` can continue flow if it is not awaiting a response
(that is, a `send` operation). Otherwise it remains suspended waiting for the reply.
* The receiving end of the bridge TLS 1.2 /AMQP 1.0 link might be the Artemis broker of a remote node,
but for now we assume it is an enterprise deployment that is using a float process running behind a firewall.
The receiver will already have confirmed the validity of the TLS originator when it accepted the TLS handshake.
However, the float does some further basic checking of received messages and their associated headers.
For instance, the message must be targeted at an inbox address and must be below the network parameters defined `maxMessageSize`.
* Having passed initial checks on the message, the float bundles up the message and originator as a payload to be
sent across the DMZ internal firewall. This inbound message path uses a separate AMQP 1.0/TLS 1.2 control tunnel.
(Note that this link is initiated from the local master bridge in the trusted zone to the float in the DMZ. This allows a
simple firewall rule to be configured which blocks any attempts to probe the internal network from the DMZ.)
Once the message is forwarded, the float keeps track of the delivery acknowledgements,
so that the original sender will consume the message in the source queue, only on final delivery to the peer inbox.
Any disconnections, or problems will send a reject status leading to redelivery from source.
* The bridge process, having now received custody of the message, does further checks that the message is good.
The checks validate the structure of the message and that the source and the destination are valid.
If validation for the message fails, it is acknowledged to prevent further redelivery, a validation error is logged for audit purposes
and the message is discarded.
* Assuming this is a normal message, it is passed on to the Artemis inbox and on acknowledgment of delivery,
is cascaded back. Thus, Artemis acknowledgement leads to acknowledgement of the tunnel AMQP packet,
which acknowledges the AMQP back to the sending bridge and that finally marks the Artemis out queue item as consumed.
To prevent this leading to very slow, one-after-the-other message delivery, the AMQP channels use sliding window flow control.
(Currently, a practical default is set internally and the window size is not user configurable.)
* The `MessagingService` on the peer node will pick up the message from the inbox on Artemis, carry out any necessary
deduplication. This deduplication is needed as the distributed restartable logic of the Corda wire protocol only
offers 'at least once' delivery guarantees.
The resulting unique messages are then passed to the `StateMachine` so that the remote flow can be woken up.
* The reply messages use the authenticated originator flag attached by the float to route the replies back to the
correct originator.{{< note >}}
The message reply path is not via the inbound path, but instead is via a separately validated route
from the local bridge to the original node’s float and then on to the original node via Artemis.{{< /note >}}



## Operating modes of the Bridge and Float with a single node


### Embedded Developer Node (node + artemis + internal bridge, no float, no DMZ)


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md/))
* Corda Enterprise JAR

The simplest development deployment of the node is without firewall and thus just use the embedded bridge and Peer-to-Peer
Artemis with the node as TLS endpoint and to have the outgoing packets use the internal bridge functionality.
Typically this should only be used for easy development, or for organisations evaluating on Open Source Corda,
where this is the only available option:

{{< figure alt="node embedded bridge" zoom="/en/images/node_embedded_bridge.png" >}}

### Node + Combined Bridge/Float (no DMZ)


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md))
* Corda Enterprise JAR
* Corda Firewall JAR

The next simplest deployment is when combined Bridge/Float component is segregated away from Corda Node.

To enable this mode `node.conf` specifies `externalBridge = true`.
In this configuration Artemis Broker will still be embedded inside the Corda Node and the combined Bridge/Float process needs to connect
to that broker.

In this mode it is possible to host both of the processes on the same machine. This might be suitable for a test environment, to conserve VMs.


{{< note >}}
Note that to run the firewall and the node on the same machine there could be a port conflict with a naive `node.conf` setup,
but by using the `messagingServerAddress` property to specify the bind address and port plus setting
`messagingServerExternal = false` (Artemis Broker still within Corda Node)
the embedded Artemis P2P broker can be set to listen on a different port rather than the advertised `p2paddress` port.
Then configure an all-in-one bridge to point at this node’s `messagingServerAddress`:

{{< /note >}}

{{< figure alt="simple bridge" zoom="/en/images/simple_bridge.png" >}}

#### node.conf

```javascript
myLegalName = "O=Bank A, L=New York, C=US"

# This is the address advertised into the network map. As such it must be the publicly resolved IP,
# or DNS name that will allow peers to connect to the float.
p2pAddress = "banka.com:10005"

messagingServerAddress = "nodeserver:11005"
messagingServerExternal = false

enterpriseConfiguration {
  externalBridge = true
}

rpcSettings = {
    address: "nodeserver:10006"
    adminAddress="nodeserver:10007"
}

```

[node.conf](../resources/bridge/node_bridge/node.conf)


#### bridge.conf

```javascript
firewallMode = SenderReceiver
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
inboundConfig {
    listeningAddress = "bridgeexternal:10005"
}
networkParametersPath = network-parameters

```

[bridge.conf](../resources/bridge/node_bridge/bridge.conf)


### DMZ ready (node + bridge + float)


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md))
* Corda Enterprise JAR
* Corda Firewall JAR

This is a more complete deployment which includes a DMZ and separate processes for outbound and inbound connectivity. The process deployed into DMZ is
called `Float`, also known as `BridgeOuter`. The process that sits along with Corda Node in the Green Zone is called `Bridge`,
also known as `BridgeInner`. These mode names were chosen to remind users that the `Bridge` should run in the trusted
*inner* network zone and the `Float` should run in the less trusted *outer* zone.
The diagram below shows such a non-HA deployment. This would not be recommended for production, unless used as part of a cold
disaster recovery (DR) type standby.

{{< note >}}
Note that whilst the bridge needs access to the official TLS private
key, the tunnel link should use a private set of link specific keys and certificates. The float will be provisioned
dynamically with the official TLS key when activated via the tunnel and this key will never be stored in the DMZ:

{{< /note >}}
{{< figure alt="node bridge float" zoom="/en/images/node_bridge_float.png" >}}

#### node.conf

```javascript
myLegalName = "O=Bank A, L=New York, C=US"

# This is the address advertised into the network map. As such it must be the publicly resolved IP,
# or DNS name that will allow peers to connect to the float.
p2pAddress = "banka.com:10005"

messagingServerAddress = "nodeserver:11005"
messagingServerExternal = false

rpcSettings {
    address = "nodeserver:10006"
    adminAddress = "nodeserver:10007"
}

enterpriseConfiguration = {
    externalBridge = true
}

```

[node.conf](../resources/bridge/node_bridge_float/node.conf)


#### bridge.conf

```javascript
firewallMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
}
bridgeInnerConfig {
    floatAddresses = [ "dmzinternal:12005" ]
    expectedCertificateSubject = "CN=float,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"
    }
}
networkParametersPath = network-parameters
```

[bridge.conf](../resources/bridge/node_bridge_float/bridge.conf)


#### float.conf

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal:10005"
}
floatOuterConfig {
    floatAddress = "dmzinternal:12005"
    expectedCertificateSubject = "CN=bridge,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
    }
}
```

[float.conf](../resources/bridge/node_bridge_float/float.conf)


### DMZ ready with outbound SOCKS


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md))
* Corda Enterprise JAR
* Corda Firewall JAR
* SOCKS Proxy

Some organisations require dynamic outgoing connections to operate via a SOCKS proxy. The code supports this option
by adding extra information to the `outboundConfig` section of the bridge process. A simplified example deployment is shown here
to highlight the option:

{{< figure alt="socks proxy" zoom="/en/images/socks_proxy.png" >}}

#### node.conf

```javascript
myLegalName = "O=Bank A, L=New York, C=US"

# This is the address advertised into the network map. As such it must be the publicly resolved IP,
# or DNS name that will allow peers to connect to the float.
p2pAddress = "banka.com:10005"

messagingServerAddress = "nodeserver:11005"
messagingServerExternal = false

rpcSettings {
    address = "nodeserver:10006"
    adminAddress = "nodeserver:10007"
}

enterpriseConfiguration = {
    externalBridge = true
}

```

[node.conf](../resources/bridge/socks_proxy/node.conf)


#### bridge.conf

```javascript
firewallMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "nodeserver:11005"
    proxyConfig {
       version = SOCKS5
       proxyAddress = "proxyserver:12345"
       userName = "proxyuser"
       password = "password"
    }
}
bridgeInnerConfig {
    floatAddresses = ["dmzinternal:12005" ]
    expectedCertificateSubject = "CN=float,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"
    }
}
networkParametersPath = network-parameters

```

[bridge.conf](../resources/bridge/socks_proxy/bridge.conf)


#### float.conf

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal:10005"
}
floatOuterConfig {
    floatAddress = "dmzinternal:12005"
    expectedCertificateSubject = "CN=bridge,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
    }
}
```

[float.conf](../resources/bridge/socks_proxy/float.conf)


### Full production HA DMZ ready mode (hot/cold node, hot/warm bridge)


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md))
* Corda Enterprise JAR
* Corda Firewall JAR
* Zookeeper v3.6.1
* Optional: SOCKS Proxy

Finally, we show a full HA solution as recommended for production. This does require adding an external ZooKeeper
cluster to provide `Bridge` leader election. Also there will be extra instances of the `Bridge` and `Float` processes. This allows
hot-warm operation of all the `Bridge` and `Float` instances. The Corda Enterprise node must be run as hot-cold HA too.

Highlighted in the diagram is the addition of the `haConfig` section to point at `zookeeper` and also the use of secondary
addresses in the `alternateArtemisAddresses` to allow node failover and in the `floatAddresses` to point at a
pool of DMZ float processes.

{{< figure alt="ha nodes" zoom="/en/images/ha_nodes.png" >}}

#### node.conf

```javascript
myLegalName = "O=Bank A, L=New York, C=US"

# This is the address advertised into the network map. As such it must be the publicly resolved IP,
# or DNS name that will allow peers to connect to the float.
p2pAddress = "banka.com:10005"

messagingServerAddress = "artemiserver:11005"
messagingServerExternal = true

rpcSettings {
    address = "nodeserver1:10006"
    adminAddress = "nodeserver1:10007"
}

enterpriseConfiguration = {
    externalBridge = true
    messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
    messagingServerSslConfiguration = {
        sslKeystore = artemis/artemis.jks
        keyStorePassword = artemisStorePass
        trustStoreFile = artemis/artemis-truststore.jks
        trustStorePassword = artemisTrustpass
    }
    mutualExclusionConfiguration = {
        on = true
        machineName = "nodeserver1"
        updateInterval = 20000
        waitInterval = 40000
    }
}

```

[node.conf](../resources/bridge/ha_nodes/node.conf)


#### bridge.conf

```javascript
firewallMode = BridgeInner
outboundConfig {
    artemisBrokerAddress = "artemiserver:11005"
}
bridgeInnerConfig {
    floatAddresses = ["dmzinternal1:12005", "dmzinternal2:12005"]
    expectedCertificateSubject = "CN=float,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "bridgepass"
        trustStorePassword = "trustpass"
        sslKeystore = "./bridgecerts/bridge.jks"
        trustStoreFile = "./bridgecerts/trust.jks"
    }
}
haConfig {
    haConnectionString = "zk://zookeep1:11105,zk://zookeep2:11105,zk://zookeep3:11105"
}
networkParametersPath = network-parameters

```

[bridge.conf](../resources/bridge/ha_nodes/bridge.conf)


#### float.conf

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "dmzexternal1:10005"
}
floatOuterConfig {
    floatAddress = "dmzinternal1:12005"
    expectedCertificateSubject = "CN=bridge,O=Tunnel,L=London,C=GB"
    tunnelSSLConfiguration {
        keyStorePassword = "floatpass"
        trustStorePassword = "trustpass"
        sslKeystore = "./floatcerts/float.jks"
        trustStoreFile = "./floatcerts/trust.jks"
    }
}
```

[float.conf](../resources/bridge/ha_nodes/float.conf)


#### Notes on physical deployment of services

In this mode of operation there will be a large amount of network traffic exchanged between: Float, Bridge, Artemis Broker and Corda Node.

In order to ensure optimal performance of this sort of deployment, it is required to have stable connectivity and to minimise latency
between aforementioned services. Failing that, communication may lead to frequent timeouts/re-tries or even un-necessary HA cluster switchover
therefore greatly reducing net useful uptime.

{{< note >}}
Requirements below only relate to “in-house” set of services hosted by a node operator. Connection from Bridge to Foreign node
and from Foreign Node to Float are done over WAN over which the node operator does not have direct control. Therefore, connectivity from Bridge to Foreign node and from Foreign Node to Float are out of scope for the requirements below.

{{< /note >}}
More specifically, in order to ensure optimal performance it is required:


* To deploy Float, Bridge, Artemis Broker and Corda Node in the same data center;
* Network bandwidth between any two hosts where services deployed should be no less than 100 MBit (1 GBit preferred);
* TCP packets loss ratio should be 0.1% or less;
* Round-trip time (RTT) should be 10 milliseconds or less.


## Operating modes of shared Bridge and Float


### Multiple nodes + Bridge (no float, no DMZ)


#### Prerequisites


* A supported Java distribution (see [Getting set up for CorDapp development](../cordapps/getting-set-up.md))
* Corda Enterprise JAR
* Corda Firewall JAR
* Apache Artemis v2.6.2 or RedHat amq broker v7.2.2
* Optional: Zookeeper v3.6.1 if using Bridge cluster

It is possible to allow two or more Corda nodes (HA and/or non-HA) handle outgoing and incoming P2P communication through a shared bridge. This is possible by configuring the nodes to use
an external Artemis messaging broker which can be easily configured using the ha-tool. For more information, please see HA Utilities. While this example is the simplest deployment
possible with a shared bridge, any other configuration previously presented can be created.

{{< figure alt="multiple nodes no ha" zoom="/en/images/multiple_nodes_no_ha.png" >}}

#### bank-a-node.conf

```javascript
myLegalName = "O=Bank A, L=New York, C=US"

keyStorePassword = "entityAStorePass"
trustStorePassword = "nodeTrustpass"

p2pAddress="bank.com:10005"

messagingServerAddress = "artemisServer:11005"
messagingServerExternal = true

enterpriseConfiguration {
  externalBridge = true
  messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
  messagingServerSslConfiguration = {
    sslKeystore = artemis/artemis.jks
    keyStorePassword = artemisStorePass
    trustStoreFile = artemis/artemis-truststore.jks
    trustStorePassword = artemisTrustpass
  }
}

rpcSettings = {
        address: "nodeserver:10006"
        adminAddress="nodeserver:10007"
}

```

[bank-a-node.conf](../resources/bridge/multiple_non_ha_nodes/bank-a-node.conf)


#### bank-b-node.conf

```javascript
myLegalName = "O=Bank B, L=New York, C=US"

keyStorePassword = "entityBStorePass"
trustStorePassword = "nodeTrustpass"

p2pAddress="bank.com:10005"

messagingServerAddress = "artemisServer:11005"
messagingServerExternal = true

enterpriseConfiguration {
  externalBridge = true
  messagingServerConnectionConfiguration = "CONTINUOUS_RETRY"
  messagingServerSslConfiguration = {
    sslKeystore = artemis/artemis.jks
    keyStorePassword = artemisStorePass
    trustStoreFile = artemis/artemis-truststore.jks
    trustStorePassword = artemisTrustpass
  }
}

rpcSettings = {
        address: "nodeserver:10016"
        adminAddress="nodeserver:10017"
}

```

[bank-b-node.conf](../resources/bridge/multiple_non_ha_nodes/bank-b-node.conf)


#### bridge.conf

```javascript
firewallMode = SenderReceiver

outboundConfig {
    artemisBrokerAddress = "artemisServer:11005"
    artemisSSLConfiguration = {
        sslKeystore = artemis/artemis.jks
        keyStorePassword = artemisStorePass
        trustStoreFile = artemis/artemis-truststore.jks
        trustStorePassword = artemisTrustpass
    }
}

inboundConfig {
    listeningAddress = "bridgeexternal:10005"
}

networkParametersPath = network-parameters

sslKeystore = nodesCertificates/nodesUnitedSslKeystore.jks
keyStorePassword = bridgeKeyStorePassword

trustStorePassword = nodeTrustpass
trustStoreFile = nodesCertificates/truststore.jks
```

[bridge.conf](../resources/bridge/multiple_non_ha_nodes/bridge.conf)


### Adding new nodes to existing shared Bridge

Most of the HA components are agnostic to the node, with exception of the bridge which needs to have access to the node’s SSL key in order to establish TLS connection to the counterparty nodes.

The bridge’s SSL keystore will need to be updated when adding new node to the shared HA infrastructure. This can be done by using any keytool or by using HA Utilities,
the *SSL key copier* is tailored to import multiple node’s SSL keys into the bridge’s keystore.

A simple procedure for adding a new node might look like the following:



* Back up and shut down all Corda components - Nodes, Bridges, Artemis broker and Float.
* Register your new entities with the network operator. See joining-a-compatibility-zone.
* Locate the SSL keystore file in node’s certificate folder. e.g. `<node base directory>/certificates/sslkeystore.jks`
* Copy the SSL keystores generated from the registration process to Bridge if they are on a different host.
* Using the HA Utilities, copy the newly acquired legal entity’s SSL key to the bridge’s SSL keystore.
`ha-utilities import-ssl-key --node-keystores <<Node keystore path>> --node-keystore-passwords=<<Node keystore password>> --bridge-keystore=<<Bridge keystore path>> --bridge-keystore-password=<<Bridge keystore password>>`
* Start the Bridge and other nodes.



## Standalone Artemis server

The Corda node can be configured to use a external Artemis broker instead of embedded broker to provide messaging layer HA capability in enterprise environment.

Detailed setup instructions for Apache Artemis can be found in [Apache Artemis documentation](https://activemq.apache.org/artemis/docs/latest/index.html). Also see
HA Utilities for Artemis server configuration tool, which you can use to build a local, configured for Corda, Apache Artemis directory.

{{< note >}}
To run Apache Artemis you can use: `cd artemis && bin/artemis run`

{{< /note >}}
We have tested Corda against Apache Artemis v2.6.2 and RedHat amq broker v7.2.2. It is recommended to use these Artemis versions with Corda.


## Apache ZooKeeper

Apache ZooKeeper is used in Corda firewall to manage the hot/warm bridge clusters. Because hot/hot is not supported,ZooKeeper is used to ensure only 1 instance of the bridge is active at all time.
The ZooKeeper instance is also used for signals failover when the active bridge is disconnected. ZooKeeper does not process or store any data regarding transactions or P2P communication.


### Setting up ZooKeeper cluster

ZooKeeper can be deployed in single-server or multi-server setup. A clustered (multi-Server) setup is recommended for production use, for added fault tolerance and reliability.

Detailed setup instructions can be found in [Apache ZooKeeper documentation](https://zookeeper.apache.org/doc/r3.6.1/zookeeperAdmin.html#sc_zkMulitServerSetup).


### Sharing ZooKeeper

A single ZooKeeper cluster instance can be shared between multiple bridge clusters to reduce infrastructure cost. The `haConfig.haTopic` can be configured to allow each bridge cluster to access a different ZooKeeper path.


## ZooKeeper alternative

It is possible to have the hot-warm capability of the bridge and float clusters without the added deployment complexity of a ZooKeeper cluster. The firewall provides a `Bully Algorithm` implementation for master election which can be enabled
by simply changing the `haConnectionString` configuration property from `zk://<host>:<port>` to the pseudo-url `bully://localhost` (the host is a dummy string). This feature uses Publish/Subscribe messages on the P2P Artemis messaging broker for coordination. Please be aware that
this approach does not protect against network partitioning problems, therefore it is strongly recommended to use ZooKeeper in production environments.



## Use of HSM in Corda Firewall

There are several private keys necessary for Corda Firewall to function:



* Private key to enable TLS signing when external party connects into Float using P2P protocol. Also this key is used when Bridge performs an outgoing communication to external party.
* Private key to enable TLS signing when Bridge connecting into Artemis.
* A pair of distinct private keys to enable TLS signing when two way communication is performed between Bridge and Float, also known as tunnel communication.


Historically, those private keys were stored in keystore files on local disk. Depending on the firm’s IT security policy, applications may be required to store private keys in HSM.

To address this requirement, Corda Firewall has a facility to enable TLS signing using HSM. The key principle here is that private key is generated on HSM and never leaves HSM to avoid being compromised.
When it comes to use of private key for signing - this operation is performed on HSM device itself.

This mode of operation is very similar to what is happening on the Corda Node for identity private key, please see: Crypto service configuration.

HA Utilities tool been extended such that during initial generation of TLS keys they are created on HSM.

{{< note >}}
Even though Corda Firewall has a facility to store Artemis private key in HSM, out-of-process Artemis and Corda Node do not yet have facility to store their private keys on HSM.

{{< /note >}}
{{< note >}}
Since tunnel is an internal communication channel between Bridge and Float secured by self-signed certificate using custom trust root,
there is little benefit in protecting private keys for this particular communication channel using HSM. Also this would require to have `Float` (a DMZ side component) to be connecting to HSM, which might
be undesired given that `Float` is an externally-facing component and will be at the forefront should an adversary decides to attack Corda Firewall.

{{< /note >}}

## Memory requirements for Corda Firewall

By default, Corda Firewall components (both `Bridge` and `Float`) start with 1,600 MB of memory. This is necessary to accommodate all the
messages that might be in flight at any particular moment in time.
Corda Firewall been tested to support 100 concurrent connections which are intensively exchanging messages of 10 MB in size, which means that at any particular
moment, there were around 1 GB of data in flight.

If necessary, memory allocated to Corda Firewall can be changed using the `custom.jvmArgs` configuration file option.
