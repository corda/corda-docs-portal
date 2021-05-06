---
aliases:
- /releases/release-V2.0/setting-up-a-corda-network.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-setting-up-a-corda-network
    parent: corda-os-2-0-corda-networks-index
    weight: 1010
tags:
- setting
- corda
- network
title: Creating a Corda network
---



# Creating a Corda network

A Corda network consists of a number of machines running nodes, including a single node operating as the network map
service. These nodes communicate using persistent protocols in order to create and validate transactions.

There are four broader categories of functionality one such node may have. These pieces of functionality are provided as
services, and one node may run several of them.


* Network map: The node running the network map provides a way to resolve identities to physical node addresses and associated public keys.
* Notary: Nodes running a notary service witness state spends and have the final say in whether a transaction is a double-spend or not.
* Oracle: Network services that link the ledger to the outside world by providing facts that affect the validity of transactions.
* Regular node: All nodes have a vault and may start protocols communicating with other nodes, notaries and oracles and evolve their private ledger.


## Setting up your own network


### Certificates

All nodes belonging to the same Corda network must have the same root CA. For testing purposes you can
use `certSigningRequestUtility.jar` to generate a node certificate with a fixed test root:

```bash
# Build the jars
./gradlew buildCordaJAR
# Generate certificate
java -jar build/libs/certSigningRequestUtility.jar --base-dir NODE_DIRECTORY/
```


### Configuration

A node can be configured by adding/editing `node.conf` in the node’s directory. For details see [Node configuration](corda-configuration-file.md).

An example configuration:

```cfg
myLegalName : "O=Bank A,L=London,C=GB"
keyStorePassword : "cordacadevpass"
trustStorePassword : "trustpass"
dataSourceProperties : {
    dataSourceClassName : org.h2.jdbcx.JdbcDataSource
    "dataSource.url" : "jdbc:h2:file:"${baseDirectory}"/persistence"
    "dataSource.user" : sa
    "dataSource.password" : ""
}
p2pAddress : "my-corda-node:10002"
rpcAddress : "my-corda-node:10003"
webAddress : "localhost:10004"
extraAdvertisedServiceIds : [ "corda.interest_rates" ]
networkMapService : {
    address : "my-network-map:10000"
    legalName : "O=Network Map Service,OU=corda,L=London,C=GB"
}
useHTTPS : false
rpcUsers : [
    { username=user1, password=letmein, permissions=[ StartProtocol.net.corda.protocols.CashProtocol ] }
]
devMode : true
// Certificate signing service will be hosted by R3 in the near future.
//certificateSigningService : "https://testnet.certificate.corda.net"

```

[example-node.conf](https://github.com/corda/corda/blob/release/os/2.0/docs/source/example-code/src/main/resources/example-node.conf)

The most important fields regarding network configuration are:


* `p2pAddress`: This specifies a host and port to which Artemis will bind for messaging with other nodes. Note that the
address bound will **NOT** be `my-corda-node`, but rather `::` (all addresses on all network interfaces). The hostname specified
is the hostname *that must be externally resolvable by other nodes in the network*. In the above configuration this is the
resolvable name of a machine in a VPN.
* `rpcAddress`: The address to which Artemis will bind for RPC calls.
* `webAddress`: The address the webserver should bind. Note that the port must be distinct from that of `p2pAddress` and `rpcAddress` if they are on the same machine.
* `networkMapService`: Details of the node running the network map service. If it’s this node that’s running the service
then this field must not be specified.


### Starting the nodes

You may now start the nodes in any order. Note that the node is not fully started until it has successfully registered with the network map!

You should see a banner, some log lines and eventually `Node started up and registered`, indicating that the node is fully started.


In terms of process management there is no prescribed method. You may start the jars by hand or perhaps use systemd and friends.


### Logging

Only a handful of important lines are printed to the console. For
details/diagnosing problems check the logs.

Logging is standard [log4j2](http://logging.apache.org/log4j/2.x/) and may be configured accordingly. Logs
are by default redirected to files in `NODE_DIRECTORY/logs/`.


### Connecting to the nodes

Once a node has started up successfully you may connect to it as a client to initiate protocols/query state etc.
Depending on your network setup you may need to tunnel to do this remotely.

See the [Using the client RPC API](tutorial-clientrpc-api.md) on how to establish an RPC link.

Sidenote: A client is always associated with a single node with a single identity, which only sees their part of the ledger.

