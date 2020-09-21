---
aliases:
- /releases/release-1.2/network-map-overview.html
- /docs/cenm/head/network-map-overview.html
- /docs/cenm/network-map-overview.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-network-map-overview
    parent: cenm-1-2-concepts-and-overview
    weight: 50
tags:
- network
- map
- overview
title: Network Map Overview
---


# Network Map Overview

The network map is a collection of signed `NodeInfo` objects. Each NodeInfo is signed by the node it represents and
thus cannot be tampered with. It forms the set of reachable nodes in a network. A node can receive these objects from
two sources:


* A network map server that speaks a simple HTTP based protocol.
* The `additional-node-infos` directory within the node’s directory.

The network map server also distributes the parameters file that define values for various settings that all nodes need
to agree on to remain in sync.

{{< note >}}
In Corda 3 no implementation of the HTTP network map server is provided. This is because the details of how
a network manages its membership (the databases, ticketing workflows, HSM hardware etc) is expected to vary
between operators, so we provide a simple REST based protocol for uploading/downloading NodeInfos and managing
network parameters. A future version of Corda may provide a simple “stub” implementation for running test zones.
In Corda 3 the right way to run a test network is through distribution of the relevant files via your own mechanisms.
We provide a tool to automate the bulk of this task (see below).

{{< /note >}}

## HTTP network map protocol

If the node is configured to connect with a network using the `networkServices` section of the config, then it first uploads its own signed `NodeInfo`
to the server at the `networkMapUrl` (and each time it changes on startup) and then proceeds to download the entire network map from
the same server. The network map consists of a list of `NodeInfo` hashes. The node periodically polls for the network map
(based on the HTTP cache expiry header) and any new entries are downloaded and cached. Entries which no longer exist are deleted from the node’s cache.

The set of REST end-points for the network map service are as follows. This defines the first commited version of the Corda Network Map protocol.


{{< table >}}

|Request method|Path|Description|
|----------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|POST|/network-map/publish|For the node to upload its signed `NodeInfo` object to the network map.|
|POST|/network-map/ack-parameters|For the node operator to acknowledge network map that new parameters were accepted for future update.|
|GET|/network-map|Retrieve the current signed public network map object. The entire object is signed with the network map certificate which is also attached.|
|GET|/network-map/node-info/{hash}|Retrieve a signed `NodeInfo` as specified in the network map object.|
|GET|/network-map/network-parameters/{hash}|Retrieve the signed network parameters (see below). The entire object is signed with the network map certificate which is also attached.|

{{< /table >}}

In addition to the above the Corda Enterprise Network Manager provides a number of additional features available via a REST interface. These are not used by the node itself, but
either zone or node operators for information and debugging.


{{< table >}}

|Request method|Path|Description|
|----------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|GET|/network-map-user/network-map|Retrieve the current public network map formatted as a JSON document.|
|GET|/network-map-user/node-infos|Retrieve a human readable list of the currently registered `NodeInfo` files in the public network formatted as a JSON document.|
|GET|/network-map-user/node-info/{hash}|Retrieve a human readable version of a `NodeInfo` formatted as a JSON document.|
|GET|/network-map-user/network-parameters|Retrieve a human readable version of the current `NetworkParameters` formatted as a JSON document.|
|GET|/network-map-user/network-parameters/{hash}|Retrieve a human readable version of a `NetworkParameters` formatted as a JSON document.|

{{< /table >}}

HTTP is used for the network map service instead of Corda’s own AMQP based peer to peer messaging protocol to
enable the server to be placed behind caching content delivery networks like Cloudflare, Akamai, Amazon Cloudfront and so on.
By using industrial HTTP cache networks the map server can be shielded from DoS attacks more effectively. Additionally,
for the case of distributing small files that rarely change, HTTP is a well understood and optimised protocol. Corda’s
own protocol is designed for complex multi-way conversations between authenticated identities using signed binary
messages separated into parallel and nested flows, which isn’t necessary for network map distribution.


## Node Info

The node info consists the following data:



* **addresses**:
List of network addresses (including port numbers) under which the node is accessible.


* **legalIdentitiesAndCerts**:
List of legal identities (with their certificates) registered at the node.


* **platformVersion**:
Platform version of the node.


* **serial**:
Serial number of this node info file.





## The `additional-node-infos` directory

Alongside the HTTP network map service, or as a replacement if the node isn’t connected to one, the node polls the
contents of the `additional-node-infos` directory located in its base directory. Each file is expected to be the same
signed `NodeInfo` object that the network map service vends. These are automatically added to the node’s cache and can
be used to supplement or replace the HTTP network map. If the same node is advertised through both mechanisms then the
latest one is taken.

On startup the node generates its own signed node info file, filename of the format `nodeInfo-${hash}`. It can also be
generated using the `--just-generate-node-info` command line flag without starting the node. To create a simple network
without the HTTP network map service simply place this file in the `additional-node-infos` directory of every node that’s
part of this network. For example, a simple way to do this is to use rsync.

Usually, test networks have a structure that is known ahead of time. For the creation of such networks we provide a
`network-bootstrapper` tool. This tool pre-generates node configuration directories if given the IP addresses/domain
names of each machine in the network. The generated node directories contain the NodeInfos for every other node on
the network, along with the network parameters file and identity certificates. Generated nodes do not need to all be
online at once - an offline node that isn’t being interacted with doesn’t impact the network in any way. So a test
cluster generated like this can be sized for the maximum size you may need, and then scaled up and down as necessary.


## Network parameters

Network parameters are a set of values that every node participating in the network needs to agree on and use to
correctly interoperate with each other. They can be thought of as an encapsulation of all aspects of a Corda deployment
on which reasonable people may disagree. Whilst other blockchain/DLT systems typically require a source code fork to
alter various constants (like the total number of coins in a cryptocurrency, port numbers to use etc), in Corda we
have refactored these sorts of decisions out into a separate file and allow “network operators” to make decisions about
them. The operator signs a data structure that contains the values and they are distributed along with the network map.
Tools are provided to gain user opt-in consent to a new version of the parameters and ensure everyone switches to them
at the same time.

If the node is using the HTTP network map service then on first startup it will download the signed network parameters,
cache it in a `network-parameters` file and apply them on the node.


{{< warning >}}
If the `network-parameters` file is changed and no longer matches what the network map service is advertising
then the node will automatically shutdown. Resolution to this is to delete the incorrect file and restart the node so
that the parameters can be downloaded again.

{{< /warning >}}


If the node isn’t using a HTTP network map service then it’s expected the signed file is provided by some other means.
For such a scenario there is the network bootstrapper tool which in addition to generating the network parameters file
also distributes the node info files to the node directories.

The current set of network parameters:


* **minimumPlatformVersion**:
The minimum platform version that the nodes must be running. Any node which is below this will
not start.


* **notaries**:
List of identity and validation type (either validating or non-validating) of the notaries which are
permitted in the network.


* **maxMessageSize**:
Maximum allowed size in bytes of an individual message sent over the wire.


* **maxTransactionSize**:
Maximum allowed size in bytes of a transaction. This is the size of the transaction object and its
attachments.


* **modifiedTime**:
The time when the network parameters were last modified by the network operator.


* **epoch**:
Version number of the network parameters. Starting from 1, this will always increment whenever any of the
parameters change.


* **whitelistedContractImplementations**:
List of whitelisted versions of contract code. For each contract class there is a
list of hashes of the approved CorDapp jar versions containing that contract. Read
more about *contract constraints* in the [contract constraints doc](https://docs.corda.net/api-contract-constraints.html). See
[Contract Whitelist Generation](contract-whitelisting.md) for how to configure this in the network parameters
configuration file.


* **eventHorizon**:
Time after which nodes are considered to be unresponsive and removed from network map. Nodes republish
their `NodeInfo` on a regular interval. Network map treats that as a heartbeat from the node.




More parameters may be added in future releases to regulate things like allowed port numbers, how long a node can be
offline before it is evicted from the network, whether or not IPv6 connectivity is required for members, required
cryptographic algorithms and rollout schedules (e.g. for moving to post quantum cryptography), parameters related to
SGX and so on.


## Network parameters update process

In case of the need to change network parameters Corda network operator will start the update process. There are many
reasons that may lead to this decision: adding a notary, setting new fields that were added to enable smooth network
interoperability, or a change of the existing compatibility constants is required, for example.

To synchronize all nodes in the network to use the new set of the network parameters two RPC methods are provided. The
process requires human interaction and approval of the change, so node operators can review the differences before
agreeing to them.

When the update is about to happen the network map service starts to advertise the additional information with the usual network map
data. It includes new network parameters hash, description of the change and the update deadline. Nodes query the network map server
for the new set of parameters.

The fact a new set of parameters is being advertised shows up in the node logs with the message
“Downloaded new network parameters”, and programs connected via RPC can receive `ParametersUpdateInfo` by using
the `CordaRPCOps.networkParametersFeed` method. Typically a network operator would also email node operators to let
them know about the details of the impending change, along with the justification, how to object, deadlines and so on.

The node administrator can review the change and decide if they are going to accept it. The approval should be do
before the update Deadline. Nodes that don’t approve before the deadline will likely be removed from the network map by
the network operator, but that is a decision that is left to the operator’s discretion. For example the operator might
also choose to change the deadline instead.

If the network operator starts advertising a different set of new parameters then that new set overrides the previous set.
Only the latest update can be accepted.

To send back parameters approval to the network operator, the RPC method
`fun acceptNewNetworkParameters(parametersHash: SecureHash)` has to be called with `parametersHash` from the update.
Note that approval cannot be undone. You can do this via the Corda shell:

`run acceptNewNetworkParameters parametersHash: "ba19fc1b9e9c1c7cbea712efda5f78b53ae4e5d123c89d02c9da44ec50e9c17d"`

If the administrator does not accept the update then next time the node polls network map after the deadline, the
advertised network parameters will be the updated ones. The previous set of parameters will no longer be valid.
At this point the node will automatically shutdown and will require the node operator to bring it back again.

{{< note >}}
It is not recommended to advertise new parameters or cancel the update during the period between flag day
issuance and the next network map signing, especially if the scheduled network map signing task is configured.
This can result in inconsistent parameters update record in the database and implicit cancellation of the
issued flag day.

{{< /note >}}

## Node’s host IP address

The network map service provides an endpoint that can be used to determine the IP address of the querying host. This is
useful especially when dealing with node’s deployment in environments with IP address translation.


{{< table >}}

|GET|/network-map/my-hostname|Returns the IP address of the requestor.|

{{< /table >}}
