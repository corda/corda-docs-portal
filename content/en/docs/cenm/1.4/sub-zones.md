---
aliases:
- /sub-zones.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-sub-zones
    parent: cenm-1-4-concepts-and-overview
    weight: 40
tags:
- zones
title: Subzones
---


# Subzones

{{< note >}}
This is an internal feature. Running a network with multiple subzones is not a supported configuration.

{{< /note >}}

## Network from a Node’s Perspective

From the perspective of a node, a network is defined by the Identity Manager and Network Map services it is configured
to connect to. It has no comprehension of subzones. It simply connects to the services configured within its
configuration file and, once registered with both, interacts with other nodes and the apps deployed upon it via the
RPC clients. This is summarised below:

{{<
  figure
	 src="resources/node-zone-view.png"
	 zoom="resources/node-zone-view.png"
   width=90%
	 figcaption="Network from a Node's Perspective"
	 alt="node zone view"
>}}

The node is unaware of other subzones - it sees only those nodes registered with the Network Map service that it has also
registered with itself.


## Network from a Zone's Perspective

From the perspective of the operator of that zone however, things are a lot more interesting:

{{<
  figure
	 src="resources/simple-subzones.png"
	 zoom="resources/simple-subzones.png"
   width=110%
	 figcaption="Network from a Zone's Perspective"
	 alt="simple subzones"
>}}

In this example the zone operator is operating two public subzones, each with a different minimum platform version (the
other network parameters shared by the two zones are omitted for brevity). Each subzone has a single notary, operated
by the zone operator, whose node info is included in the whitelist of the network parameters representing that zone.

A zone always has only one instance of Signer. Multiple subzones can have different network maps but all share the same Signer and Identity Manager. Signer signs:
* Certificate signing requests from the Identity Manager,
* Changes to the network parameters,
* Updates to the network map.

Interesting features:

* All nodes are registered with the zone’s Identity Manager Service. *This includes the notaries.*
* Each subzone is represented by a network map, each with its own database and network parameters file.
* Node 1 is on the “older” subzone using a minimum platform version of 3. It is unaware that Nodes 2 and 3 even exist
(just as they are unaware of it) but can use Notary 1.
* Nodes 2 and 3 and Notary 2 can all intercommunicate as one would expect.


## Segregated Subzones

The fundamental difference between a public subzone and a segregated one is that the operation of the notaries is
deferred to a third party. The relationship between the zone operator and the notary operator is left to the discretion
of the zone operator.

{{< important >}}
The important part from the perspective of CENM is that the signed node info
is transferred from the notary operator to the zone operator.


{{< /important >}}

This is shown in the following diagram:

{{<
  figure
	 src="resources/simple-seg-zones.png"
	 zoom="resources/simple-seg-zones.png"
   width=110%
	 figcaption="Segregated Subzones"
	 alt="segregated subzones"
>}}
