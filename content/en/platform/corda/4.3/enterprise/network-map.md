---
aliases:
- /releases/4.3/network-map.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-network-map
    parent: corda-enterprise-4-3-corda-networks-index
    weight: 1030
tags:
- network
- map
title: The network map
---


# The network map


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
network parameters. A future version of Corda may provide a simple “stub” implementation for running test zones.
In the current version the right way to run a test network is through distribution of the relevant files via your own mechanisms.
We provide a tool to automate the bulk of this task (see below).

{{< /note >}}

## HTTP network map protocol

If the node is configured with the `compatibilityZoneURL` config then it first uploads its own signed `NodeInfo`
to the server at that URL (and each time it changes on startup) and then proceeds to download the entire network map from
the same server. The network map consists of a list of `NodeInfo` hashes. The node periodically polls for the network map
(based on the HTTP cache expiry header) and any new entries are downloaded and cached. Entries which no longer exist are deleted from the node’s cache.

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

{{< /table >}}

Network maps hosted by R3 or other parties using R3’s commercial network management tools typically also provide the following endpoints as a convenience to operators and other users

{{< note >}}
we include them here as they can aid debugging but, for the avoidance of doubt, they are not a formal part of the spec and the node will operate even in their absence.

{{< /note >}}

{{< table >}}

|Request method|Path|Description|
|----------------|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
|GET|/network-map/json|Retrieve the current public network map formatted as a JSON document.|
|GET|/network-map/json/{uuid}|Retrieve the current network map for a private network indicated by the uuid parameter formatted as a JSON document.|
|GET|/network-map/json/node-infos|Retrieve a human readable list of the currently registered `NodeInfo` files in the public network formatted as a JSON document.|
|GET|/network-map/json/node-infos/{uid}|Retrieve a human readable list of the currently registered `NodeInfo` files in the specified private network map.|
|GET|/network-map/json/node-info/{hash}|Retrieve a human readable version of a `NodeInfo` formatted as a JSON document.|

{{< /table >}}

HTTP is used for the network map service instead of Corda’s own AMQP based peer to peer messaging protocol to
enable the server to be placed behind caching content delivery networks like Cloudflare, Akamai, Amazon Cloudfront and so on.
By using industrial HTTP cache networks the map server can be shielded from DoS attacks more effectively. Additionally,
for the case of distributing small files that rarely change, HTTP is a well understood and optimised protocol. Corda’s
own protocol is designed for complex multi-way conversations between authenticated identities using signed binary
messages separated into parallel and nested flows, which isn’t necessary for network map distribution.

{{< note >}}

Note that only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are not supported.

{{< /note >}}

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

More information can be found in [Network Bootstrapper](network-bootstrapper.md).



## Network parameters

Network parameters are a set of values that every node participating in the zone needs to agree on and use to
correctly interoperate with each other. They can be thought of as an encapsulation of all aspects of a Corda deployment
on which reasonable people may disagree. Whilst other blockchain/DLT systems typically require a source code fork to
alter various constants (like the total number of coins in a cryptocurrency, port numbers to use etc), in Corda we
have refactored these sorts of decisions out into a separate file and allow “zone operators” to make decisions about
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
List of identity and validation type (either validating or non-validating) of the notaries which are permitted
in the compatibility zone.


* **maxMessageSize**:
Maximum allowed size in bytes of an individual message sent over the wire.


* **maxTransactionSize**:
Maximum allowed size in bytes of a transaction. This is the size of the transaction object and its attachments.


* **modifiedTime**:
The time when the network parameters were last modified by the compatibility zone operator.


* **epoch**:
Version number of the network parameters. Starting from 1, this will always increment whenever any of the
parameters change.


* **whitelistedContractImplementations**:
List of whitelisted versions of contract code.
For each contract class there is a list of SHA-256 hashes of the approved CorDapp jar versions containing that contract.
Read more about *Zone constraints* here [API: Contract Constraints](api-contract-constraints.md)


* **eventHorizon**:
Time after which nodes are considered to be unresponsive and removed from network map. Nodes republish their
`NodeInfo` on a regular interval. Network map treats that as a heartbeat from the node.


* **packageOwnership**:
List of the network-wide java packages that were successfully claimed by their owners.
Any CorDapp JAR that offers contracts and states in any of these packages must be signed by the owner.
This ensures that when a node encounters an owned contract it can uniquely identify it and knows that all other nodes can do the same.
Encountering an owned contract in a JAR that is not signed by the rightful owner is most likely a sign of malicious behaviour, and should be reported.
The transaction verification logic will throw an exception when this happens.
Read more about *Package ownership* here “[Package namespace ownership](network-bootstrapper.md#package-namespace-ownership)”.



{{< note >}}
To determine which *minimumPlatformVersion* a zone must mandate in order to permit all the features of Corda 4.3 see [Corda Features and Versions](features-versions.md)

{{< /note >}}
More parameters will be added in future releases to regulate things like allowed port numbers, whether or not IPv6
connectivity is required for zone members, required cryptographic algorithms and roll-out schedules (e.g. for moving to post quantum cryptography), parameters related to SGX and so on.


## Network parameters update process

Network parameters are controlled by the zone operator of the Corda network that you are a member of. Occasionally, they may need to change
these parameters. There are many reasons that can lead to this decision: adding a notary, setting new fields that were added to enable
smooth network interoperability, or a change of the existing compatibility constants is required, for example.

{{< note >}}
A future release may support the notion of phased roll-out of network parameter changes.

{{< /note >}}
Updating of the parameters by the zone operator is done in two phases:
1. Advertise the proposed network parameter update to the entire network.
2. Switching the network onto the new parameters - also known as a *flag day*.

The proposed parameter update will include, along with the new parameters, a human-readable description of the changes as well as the
deadline for accepting the update. The acceptance deadline marks the date and time that the zone operator intends to switch the entire
network onto the new parameters. This will be a reasonable amount of time in the future, giving the node operators time to inspect,
discuss and accept the parameters.

The fact a new set of parameters is being advertised shows up in the node logs with the message
“Downloaded new network parameters”, and programs connected via RPC can receive `ParametersUpdateInfo` by using
the `CordaRPCOps.networkParametersFeed` method. Typically a zone operator would also email node operators to let them
know about the details of the impending change, along with the justification, how to object, deadlines and so on.

```kotlin
/**
 * Data class containing information about the scheduled network parameters update. The info is emitted every time node
 * receives network map with [ParametersUpdate] which wasn't seen before. For more information see: [CordaRPCOps.networkParametersFeed]
 * and [CordaRPCOps.acceptNewNetworkParameters].
 * @property hash new [NetworkParameters] hash
 * @property parameters new [NetworkParameters] data structure
 * @property description description of the update
 * @property updateDeadline deadline for accepting this update using [CordaRPCOps.acceptNewNetworkParameters]
 */
@CordaSerializable
data class ParametersUpdateInfo(
        val hash: SecureHash,
        val parameters: NetworkParameters,
        val description: String,
        val updateDeadline: Instant
)

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)


### Auto Acceptance

If the only changes between the current and new parameters are for auto-acceptable parameters then, unless configured otherwise, the new
parameters will be accepted without user input. The following parameters with the `@AutoAcceptable` annotation are auto-acceptable:

```kotlin
/**
 * Network parameters are a set of values that every node participating in the zone needs to agree on and use to
 * correctly interoperate with each other.
 *
 * @property minimumPlatformVersion Minimum version of Corda platform that is required for nodes in the network.
 * @property notaries List of well known and trusted notary identities with information on validation type.
 * @property maxMessageSize This is currently ignored. However, it will be wired up in a future release.
 * @property maxTransactionSize Maximum permitted transaction size in bytes.
 * @property modifiedTime ([AutoAcceptable]) Last modification time of network parameters set.
 * @property epoch ([AutoAcceptable]) Version number of the network parameters. Starting from 1, this will always increment on each new set
 * of parameters.
 * @property whitelistedContractImplementations ([AutoAcceptable]) List of whitelisted jars containing contract code for each contract class.
 *  This will be used by [net.corda.core.contracts.WhitelistedByZoneAttachmentConstraint].
 *  [You can learn more about contract constraints here](https://docs.corda.net/api-contract-constraints.html).
 * @property packageOwnership ([AutoAcceptable]) List of the network-wide java packages that were successfully claimed by their owners.
 * Any CorDapp JAR that offers contracts and states in any of these packages must be signed by the owner.
 * @property eventHorizon Time after which nodes will be removed from the network map if they have not been seen
 * during this period
 */
@KeepForDJVM
@CordaSerializable
data class NetworkParameters(
        val minimumPlatformVersion: Int,
        val notaries: List<NotaryInfo>,
        val maxMessageSize: Int,
        val maxTransactionSize: Int,
        @AutoAcceptable val modifiedTime: Instant,
        @AutoAcceptable val epoch: Int,
        @AutoAcceptable val whitelistedContractImplementations: Map<String, List<AttachmentId>>,
        val eventHorizon: Duration,
        @AutoAcceptable val packageOwnership: Map<String, PublicKey>
) {

```

[NetworkParameters.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/node/NetworkParameters.kt)

This behaviour can be turned off by setting the optional node configuration property `networkParameterAcceptanceSettings.autoAcceptEnabled`
to `false`. For example:

```guess
...
networkParameterAcceptanceSettings {
    autoAcceptEnabled = false
}
...
```

It is also possible to switch off this behaviour at a more granular parameter level. This can be achieved by specifying the set of
`@AutoAcceptable` parameters that should not be auto-acceptable in the optional
`networkParameterAcceptanceSettings.excludedAutoAcceptableParameters` node configuration property.

For example, auto-acceptance can be switched off for any updates that change the `packageOwnership` map by adding the following to the
node configuration:

```guess
...
networkParameterAcceptanceSettings {
    excludedAutoAcceptableParameters: ["packageOwnership"]
}
...
```


### Manual Acceptance

If the auto-acceptance behaviour is turned off via the configuration or the network parameters change involves parameters that are
not auto-acceptable then manual approval is required.

In this case the node administrator can review the change and decide if they are going to accept it. The approval should be done
before the update Deadline. Nodes that don’t approve before the deadline will likely be removed from the network map by
the zone operator, but that is a decision that is left to the operator’s discretion. For example the operator might also
choose to change the deadline instead.

If the network operator starts advertising a different set of new parameters then that new set overrides the previous set.
Only the latest update can be accepted.

To send back parameters approval to the zone operator, the RPC method `fun acceptNewNetworkParameters(parametersHash: SecureHash)`
has to be called with `parametersHash` from the update. Note that approval cannot be undone. You can do this via the Corda
shell (see [Node shell](shell.md)):

`run acceptNewNetworkParameters parametersHash: "ba19fc1b9e9c1c7cbea712efda5f78b53ae4e5d123c89d02c9da44ec50e9c17d"`

If the administrator does not accept the update then next time the node polls network map after the deadline, the
advertised network parameters will be the updated ones. The previous set of parameters will no longer be valid.
At this point the node will automatically shutdown and will require the node operator to bring it back again.


## Private networks

To allow business network operators to onboard nodes in the early period of the Corda Network and not to reveal their membership
to other entities on the network, the concept of private network maps was introduced. This is a temporary solution which will only
be used in the early stages when it’s possible to deduce the members of a business network. Once sufficient number of entities have
joined the Network, this feature will be turned off and previously private nodes will be made visible in the public network map.

An additional REST `/network-map/{uuid}` endpoint serving private network maps was introduced. For nodes to be able to query
that information automatically you need to change `node.conf` to include private network UUIDs in `extraNetworkMapKeys` see [Node configuration](corda-configuration-file.md).

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
how to log into node’s shell see [Node shell](shell.md)). As we are testing and hardening the implementation this step shouldn’t be required.
After cleaning the cache, network map data is restored on the next poll from the server or filesystem.
