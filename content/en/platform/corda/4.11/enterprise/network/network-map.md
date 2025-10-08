---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-corda-networks
tags:
- network
- map
title: Network map
weight: 30
---


# Network map

The network map is a collection of signed `NodeInfo` objects. Each NodeInfo is signed by the node it represents and
thus cannot be tampered with. It forms the set of reachable nodes in a compatibility zone. A node can receive these
objects from two sources:


* A network map server that speaks a simple HTTP based protocol.
* The `additional-node-infos` directory within the node’s directory.

The network map server also distributes the parameters file that define values for various settings that all nodes need
to agree on to remain in sync.

{{< note >}}
In Corda Enterprise no implementation of the HTTP network map server is provided. This is because the details of how
a compatibility zone manages its membership (the databases, ticketing workflows, HSM hardware etc) is expected to vary
between operators, so we provide a simple REST based protocol for uploading/downloading NodeInfos and managing
[network parameters]({{< relref "network-parameters.md" >}}). A future version of Corda may provide a simple “stub” implementation for running test zones.
In the current version the right way to run a test network is through distribution of the relevant files via your own mechanisms.
We provide a tool to automate the bulk of this task (see below).

{{< /note >}}

## HTTP network map protocol

If the node is configured with the `compatibilityZoneURL` config then it first uploads its own signed `NodeInfo`
to the server at that URL (and each time it changes on startup) and then proceeds to download the entire network map from
the same server. The network map consists of a list of `NodeInfo` hashes. The node periodically polls for the network map
(based on the HTTP cache expiry header) and any new entries are downloaded and cached. Entries which no longer exist are deleted from the node’s cache.

{{< note >}}
**New Headers**

CENM 1.4 introduced a header in all Network Map API responses (except for internal error responses with code 5xx), which indicates the version of the Network Map and the available calls. This header is called `X-Corda-Server-Version` and has a default value of `2`.

In addition, CENM 1.4 and above support two new headers, which replace existing headers as follows:
* `X-Corda-Platform-Version` replaces `Platform-version`.
* `X-Corda-Client-Version` replaces `Client-version`.

**The old header names are still fully supported.**
{{< /note >}}

The set of REST end-points for the network map service are as follows.


{{< table >}}

|Request method|Path|Description|
|----------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|POST|/network-map/publish|For the node to upload its signed `NodeInfo` object to the network map.|
|POST|/network-map/ack-parameters|For the node operator to acknowledge network map that new parameters were accepted for future update.|
|GET|/network-map|Retrieve the current signed public network map object. The entire object is signed with the network map certificate which is also attached.|
|GET|/network-map/{uuid}|Retrieve the current signed private network map object with given uuid. Format is the same as for `/network-map` endpoint.|
|GET|/network-map/node-info/{hash}|Retrieve a signed `NodeInfo` as specified in the network map object.|
|GET|/network-map/network-parameters/{hash}|Retrieve the signed network parameters (see below). The entire object is signed with the network map certificate which is also attached.|
|GET|/network-map/my-hostname|Retrieve the IP address of the caller (and **not** of the network map).|
|GET|/network-map/node-infos|Retrieve a list of all signed `NodeInfo` objects for _all_ the nodes in the network at once, included in the second item in the returned pair `Pair<SignedDataWithCert<NetworkMap>, List<SignedNodeInfo>>` in a binary format. (The first item in the returned pair is the same as the response expected from the `GET network-map` endpoint mentioned above).|

{{< /table >}}

{{< warning >}}
**The Network Map Service cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.**
{{< /warning >}}


### Additional endpoints from R3

Network maps hosted by R3 or other parties using R3’s commercial network management tools typically provide some
additional endpoints for users. These additional endpoints can be found {{< cenmlatestrelref "cenm/network-map-overview.md" "here" >}}.

HTTP is used for the network map service instead of Corda’s own AMQP based peer to peer messaging protocol to
enable the server to be placed behind caching content delivery networks like Cloudflare, Akamai, Amazon Cloudfront and so on.
By using industrial HTTP cache networks the map server can be shielded from DoS attacks more effectively. Additionally,
for the case of distributing small files that rarely change, HTTP is a well understood and optimised protocol. Corda’s
own protocol is designed for complex multi-way conversations between authenticated identities using signed binary
messages separated into parallel and nested flows, which isn’t necessary for network map distribution.


## The `additional-node-infos` directory

Alongside the HTTP network map service, or as a replacement if the node isn’t connected to one, the node polls the
contents of the `additional-node-infos` directory located in its base directory. Each file is expected to be the same
signed `NodeInfo` object that the network map service vends. These are automatically added to the node’s cache and can
be used to supplement or replace the HTTP network map. If the same node is advertised through both mechanisms then the
latest one is taken.

On startup the node generates its own signed node info file, filename of the format `nodeInfo-${hash}`. It can also be
generated using the `generate-node-info` sub-command without starting the node. To create a simple network
without the HTTP network map service simply place this file in the `additional-node-infos` directory of every node that’s
part of this network. For example, a simple way to do this is to use rsync.

Usually, test networks have a structure that is known ahead of time. For the creation of such networks we provide a
`network-bootstrapper` tool. This tool pre-generates node configuration directories if given the IP addresses/domain
names of each machine in the network. The generated node directories contain the NodeInfos for every other node on
the network, along with the network parameters file and identity certificates. Generated nodes do not need to all be
online at once - an offline node that isn’t being interacted with doesn’t impact the network in any way. So a test
cluster generated like this can be sized for the maximum size you may need, and then scaled up and down as necessary.

More information can be found in [Network Bootstrapper]({{< relref "../network-bootstrapper.md" >}}).


## Private network maps

To allow business network operators to onboard nodes in the early period of the Corda Network and not to reveal their membership
to other entities on the network, the concept of private network maps was introduced. This is a temporary solution which will only
be used in the early stages when it’s possible to deduce the members of a business network. Once sufficient number of entities have
joined the Network, this feature will be turned off and previously private nodes will be made visible in the public network map.

An additional REST `/network-map/{uuid}` endpoint serving private network maps was introduced. For nodes to be able to query
that information automatically you need to change `node.conf` to include private network UUIDs in `extraNetworkMapKeys` see [Node configuration]( {{< relref "../node/setup/corda-configuration-file.md" >}}).

From the node operator’s perspective the process is simple. During the initial registration the Compatibility Zone operator will
mark the node as belonging to the private network map and will provide the node operator with UUID that should be put in the node’s config file.
Then node can be started as usual. At some point in time, nodes will gradually join public network without leaking confidential
information on business relations with operators. Private networks are not separate networks, nodes are still part of bigger
compatibility zone, only hidden. We reuse all the infrastructure of the compatibility zone like notaries, permissioning service,
so the interoperability between nodes is kept.


## Cleaning the network map cache

Sometimes it may happen that the node ends up with an inconsistent view of the network. This can occur due to changes in deployment
leading to stale data in the database, different data distribution time and mistakes in configuration. For these unlikely
events both RPC method and command line option for clearing local network map cache database exist. To use them
you either need to run from the command line:

```shell
java -jar corda.jar clear-network-cache
```

or call RPC method *clearNetworkMapCache* (it can be invoked through the node’s shell as *run clearNetworkMapCache*, for more information on
how to log into node’s shell see shell). As we are testing and hardening the implementation this step shouldn’t be required.
After cleaning the cache, network map data is restored on the next poll from the server or filesystem.
