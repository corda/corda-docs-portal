---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-deploying
tags:
- env
- prod
- test
title: Deploying in a testing or production environment
weight: 1
---


# Deploying in a testing or production environment

These instructions will guide the user through the UAT or production configuration to deploy the following components. They are intended for firms deploying Corda Enterprise.


* Corda Node
* Corda Vault
* Corda Bridge and Float components of the Corda Firewall
* Load Balancer (presenting 1 public IP to CorDapp)
* Optional Zookeeper Cluster (manage Corda Firewall component availability)
* HTTPS Proxy Server (Node registration, Network Map download, includes CRL checking)
* SOCKS4/5 Proxy Server (AMPQ over TLS Messaging)

There are alternative approaches to how these components are deployed. For the purposes of this document, the following diagrams represent the topology used.


## Deployment scenarios for testing and production environments

When deploying Corda Enterprise in a testing environment the Node, Bridge, and Float components should be deployed in a non-HA configuration as shown in the following diagram.


{{< figure alt="nonha" zoom="../../resources/nonha.png" >}}

When deploying Corda Enterprise in a production environment, the Node, Bridge, and Float components should be deployed in a high-availability configuration.


{{< figure alt="ha" zoom="../../resources/ha.png" >}}


### Deployment details


* Corda Nodes run in a Hot/Cold Setup.
* The Corda Node communicates with the Doorman (authentication) and Network Map (peer addresses) over HTTPS typically through an HTTP Proxy Server.
* The Corda Node communicates with peers on the Corda network communicating with Corda Firewall which has 2 parts, the Bridge and the Float. The Float and Bridge components also check the certificate revocation list.
* The Float’s job is to act as an inbound socket listener, capturing messages from peers and send them to the Bridge. The Float prevents the Node and Artemis server from being exposed to Peer Nodes.
* The Bridge captures the inbound messages and sends them to the shared Artemis queue. The Bridge is typically configured to route through a SOCKS5 Proxy Server and also manages outgoing messages from the Node to Peers on the Network. The firewall between the Bridge and the DMZ is configured as an outbound only firewall. When communicating to the float, the bridge initiates the connection.
* In an HA configuration Node A and Node B use a shared Artemis queue configured on an NFS mountpoint shared between VM A and VM B.
* R3 have tested Zookeeper to provide an election mechanism to determine which Bridge is up and chooses a Bridge to send messages to the shared Artemis queue.
* The Bridge can select an Active and Alternative Artemis queue for incoming messages and an Active and Alternative Float for outgoing messages based on a configuration file setting.
* R3 customers have tested F5 Load Balancer presenting 1 Float IP to the external world for incoming Peer to Peer Traffic.
* R3 customers have also deployed Azure/F5 Load Balancers presenting 1 Node IP for RPC client connections.
* Customers could use a solution like VCS cluster for Node A to Node B failover, though this configuration has not been tested by R3.


## Installation steps


### Installing Java 8 on the VM

Java 8 JDK should be installed on your virtual machine. Refer to your internal processes for installation procedures.

These are the configuration files that will be created during the process:


* **Corda Node - node.conf**:
This configuration file contains settings for the following components and functions:
- Doorman
- Network Map
- Corda Bridge
- Vault Database
- RPC Port settings for client API
- P2P address for advertising Corda Node to Peers
- Crash shell port, user, and password


* **Corda Firewall Bridge - firewall.conf**:
This configuration file contains specifies the location of:
- Artemis broker IP address and port
- Corda Float listening address and port
- Location of local JKS PKI authentication keys


* **Corda Firewall Float - firewall.conf**:
This configuration file contains specifies the location of:
- Corda Float tunnel listening address and port (Bridge connecting address and port)
- Corda Float public endpoint
- Location of local JKS PKI authentication keys



You can find examples of configuration files [available here](../corda-firewall-configuration-file.html).


### Installing the Corda Node


* Upload the appropriate `corda-<version>.jar` file to the Node root directory.
* In the root of your Node directory, create a folder called `/certificates`.
* The network operator will provide you with a `network-root-truststore.jks` which will be used for authentication during initial registration.
* Upload the `network-root-truststore.jks` file to this directory.
* In the root of your Node directory, create a folder called `cordapps`.  Upload your CorDapps to this folder.

Once your Node has been started it will contain the following files and directories:

```shell
additional-node-infos/
artemis/
brokers/
certificates/
cordapps/
drivers/
logs/
plugins -> drivers/
corda-<version>.jar
network-parameters
node.conf
nodeInfo-XXXXXXXXX
```


This is a sample `node.conf` which details a configuration connecting to the Corda UAT Network.

```javascript
{
    "baseDirectory" : ".",
    "emailAddress" : "xxxxx@email.com",
    "jarDirs" : [
        "plugins",
        "cordapps"
    ],
    "keyStorePassword" : "MYPASSWORD",
    "myLegalName" : " MYLEGALNAME",
    "p2pAddress" : "banka.com:10005", // Host and port exposed by Internet facing firewall/load balancer in front of float servers in DMZ.
    "messagingServerAddress" : "0.0.0.0:11005", // Specifying endpoints of local Artemis instances
    "messagingServerExternal" : false, // Specifying that it is not an external instance
    "devMode" : false, // Turn off things like key autogeneration and require proper doorman registration.
    "detectPublicIp" : false, // Do not perform any public IP lookup on the host.


    "networkServices" : {
    "doormanURL" : "https://doorman.uat.corda.network/",
    "networkMapURL" : "https://netmap.uat.corda.network/"
},

//Azure SQL
//Microsoft SQL Server 2017

    "dataSourceProperties" : {
        "dataSource" : {
            "url" : "jdbc:sqlserver://SERVER:1433;database=DATABASENAME;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30;",
            "user" : "user",
            "password" : "password"
        },
        "dataSourceClassName" : "com.microsoft.sqlserver.jdbc.SQLServerDataSource"
    },
// postGres 9.6 RDBMS
    "dataSourceProperties" : {
        "dataSource" : {
           "url" : "jdbc:postgresql://SERVER:5432/DATABASENAME",
            "user" : "user",
            "password" : "password"
        },
        "dataSourceClassName" : "org.postgresql.ds.PGSimpleDataSource"
    },
// Oracle 11gR2/12cR2 RDBMS
    "dataSourceProperties" : {
        "dataSourceClassName" : "oracle.jdbc.pool.OracleDataSource",
        "dataSource" : {
   "url" : "jdbc:oracle:thin:@SERVERNAME:1521/DATABASENAME",
   "user" :  "user",
   "password" : "password"
        },
        },
    "database" : {
        "schema" : "dbo",
    },
    "rpcSettings" : {
        "address" : "0.0.0.0:10003",
        "adminAddress" : "0.0.0.0:10004"
    },
"rpcUsers" : [
	    {
        "password" : "test1",
	"user" : "user1",
        "permissions" : [ "ALL" ]
    }
    ],
    "trustStorePassword" : "PASSWORD",
    "sshd" : {
    "port" : "2222"

},
}

```

[nodefull.conf](../../resources/nodefull.conf)


### Implementing the Corda Firewall PKI

In a bank environment there will typically be several layers of security protecting the firms data.

{{< figure alt="cordarch" zoom="../../resources/cordarch.png" >}}
*Network Authentication*


* The Corda Node may be deployed behind the inner DMZ (no access to the Internet)
* The Bridge Server may reside on a VM in front of the inner DMZ  (not addressable from the Internet)
* The Corda Float may reside on a VM in the Outer DMZ (directly addressable from the Internet)

*PKI Authentication*


* Corda PKI Authentication issued by Corda Network can link the Node and Bridge i.e. the red keys indicated below truststore and sslkeystore
* Local PKI Authentication issued by separate CA will link the Bridge and Float i.e the purple keys indicated below trust and Bridge.

{{< figure alt="firewallpki" zoom="../../resources/firewallpki.png" >}}
The key thing is to look at this from the perspective of a bank implementing these Corda and Local PKI keys.


* Corda PKI Authentication will link the Node and Bridge and authenticate to Corda Network in the outside world. In other words, this permits mutual authentication between a Corda Node and its Peer Corda Nodes.
* Local PKI Authentication will link the Bridge and Float and allow a secure tunnel into the Float from the outside world. In other words, this permits mutual authentication between two software components, the Bridge and the Float.


### Explanation of PKI Keys

**Node Authentication**

`truststore.jks` - this is the same trust store that the Node is bootstrapped with during initial registration. It contains the `cordarootca` certificate - this is the public, root certificate of the entire network. It needs to be copied to the Bridge when it is set up. Note that the truststore is also dynamically copied from the Bridge to the Float at runtime (and is held in memory only on the Float). The truststore is used for authenticating Nodes that connect to the Bridge and Float.

**Node to Bridge Connection**

`sslkeystore.jks` is issued by the Node and contains just the Node’s TLS certificate. It needs to be installed on the Node and the Bridge. The Node-to-Bridge connection is mutually authenticated TLS, with sslkeystore used both sides to establish the secure tunnel and truststore.jks is required on each side to authenticate the connection.

**Bridge to Float Connection**

`bridge.jks` and `float.jks` contain TLS certificates and their associated private keys. By convention they should be referred to as keystores. These TLS certificates are unrelated to any of the certificates issued by the Node. In our example documentation the Bridge & Float keys are issued by a stand-alone root certificate. This root certificate is stored in trust.jks. This is required for the Bridge and Float to authenticate each other


### Generate Bridge and Float keystores

For Float and Bridge to communicate a tunnel keystore must be created. To create a tunnel keystore, run the following command:

`java -jar corda-tools-ha-utilities-4.1.jar generate-internal-tunnel-ssl-keystores -p tunnelStorePass -e tunnelPrivateKeyPassword -t tunnelTrustpass`


### Bridge Installation


* Upload the `corda-firewall-4.1.jar` to the /opt/cordabridge directory.
* In the /opt/cordabridge directory, create a softlink called `certificates` linked to /opt/corda/certificates
* In the /opt/cordabridge directory, make a directory called bridgecerts
* In the /opt/cordabridge directory, copy /opt/corda/network-parameters back to  /opt/cordabridge
* In the /opt/cordabridge directory, create a file called firewall.conf
* Copy the files /opt/corda/temp/bridge.jks and  /opt/corda/temp/trust.jks into the /opt/cordabridge/bridgecerts directory

This is a sample firewall.conf:

```javascript
firewallMode = BridgeInner

// Public SSL settings
keyStorePassword = "bridgeKeyStorePassword"
sslKeystore = "nodesCertificates/nodesUnitedSslKeystore.jks"
trustStorePassword = "trustpass"
trustStoreFile = "nodesCertificates/network-root-truststore.jks"

outboundConfig {
    artemisBrokerAddress = "<node-machine-address>:11005" // NB: for vmInfra2 swap artemisBrokerAddress and alternateArtemisBrokerAddresses.
    alternateArtemisBrokerAddresses = ["<node-machine-backup-address>:11005"]
    socksProxyConfig {
       version = SOCKS5
       proxyAddress = "<socks-server>:1080"
       username = "proxyuser"
       password = "password"
    }

}
bridgeInnerConfig {
    floatAddresses = ["<float-machine-address>:12005", "<float-machine-backup-address>:12005"] // NB: for vmInfra2 change the ordering.
    expectedCertificateSubject = "CN=float, O=Corda, L=London, C=GB" // This X.500 name should match to the name of the Float component which was used during Tunnel keystore generation above.
    tunnelSSLConfiguration {
        keyStorePassword = "tunnelStorePass"
        keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
        trustStorePassword = "tunnelTrustpass"
        sslKeystore = "./tunnel/bridge.jks"
        trustStoreFile = "./tunnel/tunnel-truststore.jks"
        crlCheckSoftFail = true
    }
}
haConfig {
    haConnectionString = "bully://localhost" // Magic URL enabling master via Artemis messaging, not Zookeeper
}
networkParametersPath = network-parameters // The network-parameters file is expected to be copied from the node registration phase and here is expected in the workspace folder.

```

[bridge.conf](../../resources/bridge.conf)


### Float Installation


* Create an /opt/cordafloat directory on your VM
* Upload the `corda-firewall-4.1.jar` to the /opt/cordafloat directory.
* In the /opt/cordafloat directory, make a directory called floatcerts.
* In the /opt/cordafloat directory, create a file called float.conf.
* The keys were created in the Node VM so sftp from the Node VM to the Float VM and copy the files NodeVM:/opt/corda/temp/float.jks and  /opt/corda/temp/trust.jks into the FloatVM:/opt/cordafloat/floatcerts directory.
* You now should have the correct non Corda PKI CA authentication in place between Bridge and Float.

This is a sample float.conf:

```javascript
firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "<float-external-facing-address>:10002"
}
floatOuterConfig {
    floatAddress = "<float-bridge-facing-address>:12005"
    expectedCertificateSubject = "CN=bridge, O=Corda, L=London, C=GB" // This X.500 name must align with name that Bridge received at the time of internal certificates generation.
    tunnelSSLConfiguration {
           keyStorePassword = "tunnelStorePass"
           keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
           trustStorePassword = "tunnelTrustpass"
           sslKeystore = "./tunnel/float.jks"
           trustStoreFile = "./tunnel/tunnel-truststore.jks"
           crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters // The network-parameters file is expected to be copied from the node registration phase and here is expected in the workspace folder.

```

[float.conf](../../resources/float.conf)

A full list of the parameters that can be utilized in these configuration files can be found in [Configuring the Corda Enterprise Firewall](../corda-firewall-configuration-file.md).


### Corda 3.x vs Corda 4.x Firewall Upgrade

In Corda 4.x it is possible to for multiple Nodes representing multiple identities to reside behind the same Corda Firewall. Details on setup can be found in [Firewall upgrade](../corda-firewall-upgrade.html).


### Port Policy and Network Configuration

Connections with the Corda Network Doorman and Network Map services (inbound and outbound traffic) will be over HTTP/HTTPS on ports 80 and 443.

Connections with peer Corda Nodes (including Notaries) will happen on a peer-to-peer connection using AMQP/TLS typically in a port range of 10000 - 10099, though port use is determined by the Node owner.

Connections with local applications connecting with the CorDapp via the Corda Node happen over RPC.

Administrative logins with the Corda Node happen via ssh whose port is configured in the node.conf file, typically port 2222.


### Suggested Work flow for Corda Node & Corda Firewall Installation


* Run ifconfig on Node VM.
* Run ifconfig on Bridge VM.
* Run ifconfig on Float VM.
* Ask your Infrastructure team to tell you public IP of load balancer/firewall.
* In node.conf p2pAddress put IP from question 4.
* In node.conf messagingServerAddress put local IP address of Node from question 1, or 0.0.0.0 for all interfaces.
* In Bridge.conf outboundconfig put IP address of Node from question 1.
* In Bridge.conf bridgeInnerConfig put IP address of 3, or ask infrastructure team what address is presented by firewall between Bridge and Float.
* In Float.conf floatOuterConfig put IP address from 3 which will be routed to from Node. If machine has one NIC use that address, if it has two then use the card that has permission for access from Bridge network.
* In Float.conf inboundConfig use IP address from 3 which faces the internet. If there is only one NIC use that value, if there are two check with Infrastructure which one is accessed from the load balancer.
* In Float.conf floatOuterConfig put IP address from 3 which will be routed to from Node. If machine has one NIC use that address, if it has two then use the card that has permission for access from Bridge network.

The following image may be helpful in ensuring alignment between the Node, Bridge and Float configuration files.

{{< figure alt="CordaFirewallConfigAlign" zoom="../../resources/CordaFirewallConfigAlign.png" >}}
{{< note >}}
**p2pAddress** reflects the **publicly accessible address**, which may or may not be the Float inboundConfig.listeningAddress. If there is an internet firewall configured in front of the Float then ask the Network Administrator for the public address that routes to the Float’s **listeningAddress**, and use that public address for your **p2pAddress**.

{{< /note >}}

### Proxy Configurations

You will likely need to establish proxy servers, one for HTTP connection to the Doorman and Network Map services, and Socks proxy to be used with the Corda Firewall for P2P communication Corda Nodes. Please note the examples below are for demonstration purposes only, it is assumed most financial institutions will already have Enterprise Proxy Server deployments in place and available for use by the Corda Firewall.







## Using HTTP Proxy with Corda

Many financial institutions will use an HTTP Proxy Server to monitor connections going out to the Internet. Corda facilitates the use of an HTTP Proxy to access the Doorman & Network map via HTTPS GET requests.

The following is an example of how to set up a Squid Proxy Server and start the Corda Node to point to it as a “tunnel” to connect to Doorman and Network Map.


* Prerequisite is a VM 2 CPU Core & 2 GB RAM running Ubuntu 18.x.
* ssh into the VM where you want to install the Proxy Server and run the following:


```shell
sudo apt update
sudo apt -y install squid
```




* Edit `/etc/squid/squid.conf` and add the following entries:


```javascript
acl SSL_ports port 443
acl Safe_ports port 8080
acl CONNECT method CONNECT
http_access allow all
http_port 8080
refresh_pattern ^ftp:           1440    20%     10080
refresh_pattern ^gopher:        1440    0%      1440
refresh_pattern -i (/cgi-bin/|\?) 0     0%      0
refresh_pattern (Release|Packages(.gz)*)$      0       20%     2880
refresh_pattern .               0       20%     4320
debug_options ALL,3
```
[squidconfig.conf](../../resources/squidconfig.conf)


* Once Squid is successfully installed run:


```shell
sudo systemctl start squid
sudo systemctl enable squid
sudo systemctl status squid
```




* If Squid starts successfully you will see an output similar to this:

```javascript
cordaadmin@corda-firewall-proxies:~$ sudo systemctl status squid
● squid.service - LSB: Squid HTTP Proxy version 3.x
   Loaded: loaded (/etc/init.d/squid; generated)
   Active: active (running) since Wed 2019-03-13 18:44:10 UTC; 14min ago
     Docs: man:systemd-sysv-generator(8)
  Process: 14135 ExecStop=/etc/init.d/squid stop (code=exited, status=0/SUCCESS)
  Process: 14197 ExecStart=/etc/init.d/squid start (code=exited, status=0/SUCCESS)
    Tasks: 4 (limit: 4915)
   CGroup: /system.slice/squid.service
           ├─14261 /usr/sbin/squid -YC -f /etc/squid/squid.conf
           ├─14263 (squid-1) -YC -f /etc/squid/squid.conf
           ├─14265 (logfile-daemon) /var/log/squid/access.log
           └─14267 (pinger)

Mar 13 18:44:10 corda-firewall-proxies systemd[1]: Starting LSB: Squid HTTP Proxy version 3.
Mar 13 18:44:10 corda-firewall-proxies squid[14197]:  * Starting Squid HTTP Proxy squid
Mar 13 18:44:10 corda-firewall-proxies squid[14261]: Squid Parent: will start 1 kids
Mar 13 18:44:10 corda-firewall-proxies squid[14197]:    ...done.
Mar 13 18:44:10 corda-firewall-proxies systemd[1]: Started LSB: Squid HTTP Proxy version 3.x
Mar 13 18:44:10 corda-firewall-proxies squid[14261]: Squid Parent: (squid-1) process 14263

```

[squidstatus.conf](../../resources/squidstatus.conf)


* At this point you can ssh to the VM where the Corda Node is installed and run the following command:


`java -Dhttps.proxyHost=your-firewall-proxy -Dhttps.proxyPort=8080 -jar corda.jar`



* If the Corda Node starts up successfully you can then check `/var/log/squid/access.log` and you should see output as follows:


```javascript
1552502594.525  70615 10.1.0.30 TCP_TUNNEL/200 30087 CONNECT netmap.uat.corda.network:443 - HIER_DIRECT/51.140.164.141 -

```

[access.conf](../../resources/access.conf)


## Using Socks Proxy with Corda Bridge

R3 strongly recommend the use of a SOCKS Proxy in conjunction with the Corda Firewall to access peers on the network for P2P communication.

SOCKS is a general purpose proxy server that establishes a TCP connection to another server on behalf of a client, then routes all the traffic back and forth between the client and the server. It works for any kind of network protocol on any port. SOCKS Version 5 adds additional support for security and UDP. By contrast an HTTP Proxy only understands HTTP traffic.

SOCKS works by establishing a TCP/IP connection with another server on the behalf of your client machine. Through this connection, traffic is routed between the client and the server, essentially anonymizing and encrypting your data and your information along the way.

SOCKS proxies provide an improvement over HTTP proxy in terms of speed of data delivery & by preventing data packets being mis-routed or mislabeled. This provides an overall improvement in terms of stability and avoiding data transfer errors that could otherwise happen.

The additional benefit of utilizing a SOCKS server is that it facilitates organizations enforce security policy and allow applications to reach legitimate external hosts through simple, centrally controlled rule-based settings.

```javascript
 socksProxyConfig {
        version = SOCKS5
        proxyAddress = "PROXYSERVER:1080"
        userName = "user"
        password = "password"
}

```

[socks.conf](../../resources/socks.conf)
