---
aliases:
- /releases/3.2/corda-test-networks.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-corda-test-networks
    parent: corda-enterprise-3-2-corda-networks-index
    weight: 1010
tags:
- corda
- test
- networks
title: Corda networks
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}



# Corda networks

A Corda network consists of a number of machines running nodes. These nodes communicate using persistent protocols in
order to create and validate transactions.

There are three broader categories of functionality one such node may have. These pieces of functionality are provided
as services, and one node may run several of them.


* Notary: Nodes running a notary service witness state spends and have the final say in whether a transaction is a
double-spend or not
* Oracle: Network services that link the ledger to the outside world by providing facts that affect the validity of
transactions
* Regular node: All nodes have a vault and may start protocols communicating with other nodes, notaries and oracles and
evolve their private ledger


## Bootstrap your own test network


### Certificates

Every node in a given Corda network must have an identity certificate signed by the network’s root CA. See
[Network permissioning](permissioning.md) for more information.


### Configuration

A node can be configured by adding/editing `node.conf` in the node’s directory. For details see [Node configuration](corda-configuration-file.md).

An example configuration:

```kotlin
myLegalName : "O=Bank A,L=London,C=GB"
keyStorePassword : "cordacadevpass"
trustStorePassword : "trustpass"
crlCheckSoftFail: true
dataSourceProperties : {
    dataSourceClassName : org.h2.jdbcx.JdbcDataSource
    dataSource.url : "jdbc:h2:file:"${baseDirectory}"/persistence"
    dataSource.user : sa
    dataSource.password : ""
}
p2pAddress : "my-corda-node:10002"
rpcSettings = {
    useSsl = false
    standAloneBroker = false
    address : "my-corda-node:10003"
    adminAddress : "my-corda-node:10004"
}
rpcUsers : [
    { username=user1, password=letmein, permissions=[ StartFlow.net.corda.protocols.CashProtocol ] }
]
devMode : true

```


* **language**:
cfg


The most important fields regarding network configuration are:


* `p2pAddress`: This specifies a host and port to which Artemis will bind for messaging with other nodes. Note that the


address bound will **NOT** be `my-corda-node`, but rather `::` (all addresses on all network interfaces). The hostname specified
is the hostname *that must be externally resolvable by other nodes in the network*. In the above configuration this is the
resolvable name of a machine in a VPN.




* `rpcAddress`: The address to which Artemis will bind for RPC calls.
* `webAddress`: The address the webserver should bind. Note that the port must be distinct from that of `p2pAddress` and `rpcAddress` if they are on the same machine.


### Starting the nodes

You will first need to create the local network by bootstrapping it with the bootstrapper. Details of how to do that
can be found in [Network Bootstrapper](network-bootstrapper.md).

Once that’s done you may now start the nodes in any order. You should see a banner, some log lines and eventually
`Node started up and registered`, indicating that the node is fully started.


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
