---
aliases:
- /releases/release-V3.1/setting-up-a-corda-network.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-1:
    identifier: corda-os-3-1-setting-up-a-corda-network
    parent: corda-os-3-1-corda-networks-index
    weight: 1010
tags:
- setting
- corda
- network
title: Setting up a Corda network
---



# Setting up a Corda network

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


## Setting up your own network


### Certificates

Every node in a given Corda network must have an identity certificate signed by the network’s root CA. See
[Network permissioning](permissioning.md) for more information.


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
rpcSettings = {
    useSsl = false
    standAloneBroker = false
    address : "my-corda-node:10003"
    adminAddress : "my-corda-node:10004"
}
webAddress : "localhost:10004"
rpcUsers : [
    { username=user1, password=letmein, permissions=[ StartFlow.net.corda.protocols.CashProtocol ] }
]
devMode : true

```

[example-node.conf](https://github.com/corda/corda/blob/release/os/3.1/docs/source/example-code/src/main/resources/example-node.conf)

The most important fields regarding network configuration are:


* `p2pAddress`: This specifies a host and port to which Artemis will bind for messaging with other nodes. Note that the
address bound will **NOT** be `my-corda-node`, but rather `::` (all addresses on all network interfaces). The hostname specified
is the hostname *that must be externally resolvable by other nodes in the network*. In the above configuration this is the
resolvable name of a machine in a VPN.
* `rpcAddress`: The address to which Artemis will bind for RPC calls.
* `webAddress`: The address the webserver should bind. Note that the port must be distinct from that of `p2pAddress` and `rpcAddress` if they are on the same machine.


### Bootstrapping the network

The nodes see each other using the network map. This is a collection of statically signed node-info files, one for each
node in the network. Most production deployments will use a highly available, secure distribution of the network map via HTTP.

For test deployments where the nodes (at least initially) reside on the same filesystem, these node-info files can be
placed directly in the node’s `additional-node-infos` directory from where the node will pick them up and store them
in its local network map cache. The node generates its own node-info file on startup.

In addition to the network map, all the nodes on a network must use the same set of network parameters. These are a set
of constants which guarantee interoperability between nodes. The HTTP network map distributes the network parameters
which the node downloads automatically. In the absence of this the network parameters must be generated locally. This can
be done with the network bootstrapper. This is a tool that scans all the node configurations from a common directory to
generate the network parameters file which is copied to the nodes’ directories. It also copies each node’s node-info file
to every other node so that they can all transact with each other.

The bootstrapper tool can be downloaded from [http://downloads.corda.net/network-bootstrapper-corda-X.Y.jar](http://downloads.corda.net/network-bootstrapper-corda-X.Y.jar), where `X` is the major Corda version and `Y` is the minor Corda version.

To use it, create a directory containing a `node.conf` file for each node you want to create. Then run the following command:

`java -jar network-bootstrapper.jar <nodes-root-dir>`

For example running the command on a directory containing these files :

```none
.
├── notary.conf             // The notary's node.conf file
├── partya.conf             // Party A's node.conf file
└── partyb.conf             // Party B's node.conf file
```

Would generate directories containing three nodes: notary, partya and partyb.

This tool only bootstraps a network. It cannot dynamically update if a new node needs to join the network or if an existing
one has changed something in their node-info, e.g. their P2P address. For this the new node-info file will need to be placed
in the other nodes’ `additional-node-infos` directory. A simple way to do this is to use [rsync](https://en.wikipedia.org/wiki/Rsync).
However, if it’s known beforehand the set of nodes that will eventually the node folders can be pregenerated in the bootstrap
and only started when needed.


### Whitelisting Contracts

If you want to create a *Zone whitelist* (see [API: Contract Constraints](api-contract-constraints.md)), you can pass in a list of CorDapp jars:

`java -jar network-bootstrapper.jar <nodes-root-dir> <path-to-first-corDapp> <path-to-second-corDapp> ..`

The CorDapp jars will be hashed and scanned for `Contract` classes.
By default the tool would generate a file named `whitelist.txt` containing an entry for each contract with the hash of the jar.

For example:

```none
net.corda.finance.contracts.asset.Obligation:decd098666b9657314870e192ced0c3519c2c9d395507a238338f8d003929de8
net.corda.finance.contracts.asset.Cash:decd098666b9657314870e192ced0c3519c2c9d395507a238338f8d003929de9
```

These will be added to the `NetworkParameters.whitelistedContractImplementations`. See [Network Map](network-map.md).

This means that by default the Network bootstrapper tool will whitelist all contracts found in all passed CorDapps.

In case there is a `whitelist.txt` file in the root dir already, the tool will append the new jar hashes or contracts to it.

The zone operator will maintain this whitelist file, and, using the tool, will append new versions of CorDapps to it.


{{< warning >}}

* The zone operator must ensure that this file is *append only*.
* If the operator removes hashes from the list, all transactions pointing to that version will suddenly fail the constraint verification, and the entire chain is compromised.
* If a contract is removed from the whitelist, then all states created from that moment on will be constrained by the HashAttachmentConstraint.

Note: In future releases, we will provider a tamper-proof way of maintaining the contract whitelist.

{{< /warning >}}


For fine-grained control of constraints, in case multiple contracts live in the same jar, the tool reads from another file:
`exclude_whitelist.txt`, which contains a list of contracts that should not be whitelisted, and thus default to the very restrictive:
`HashAttachmentConstraint`

For example:

```none
net.corda.finance.contracts.asset.Cash
net.corda.finance.contracts.asset.CommercialPaper
```


### Starting the nodes

You may now start the nodes in any order. You should see a banner, some log lines and eventually `Node started up and registered`,
indicating that the node is fully started.


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

