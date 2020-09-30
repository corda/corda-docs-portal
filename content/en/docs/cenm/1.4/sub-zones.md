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
title: Sub Zones
---


# Sub Zones

{{< note >}}
This is an internal feature. Running a network with multiple sub-zones is not a supported configuration.

{{< /note >}}

## From a Node’s Perspective

From the perspective of a node a network is defined by the Identity Manager and Network Map Services it is configured
to connect to. It has no comprehension of sub zones. It simply connects to the services configured within its
configuration file and, once registered with both, interacts with other nodes and the apps deployed upon it via the
RPC clients. This is summarised below:

![node zone view](/en/images/node-zone-view.png "node zone view")
The node is unaware of other sub zones, seeing only those nodes registered with the Network Map Service it itself has
registered with.


## From the Perspective of the Zone

From the perspective of the operator of that zone however, things are a lot more interesting:

![simple sub zones](/en/images/simple-sub-zones.png "simple sub zones")
{{< note >}}
Signing infrastructure is omitted for brevity

{{< /note >}}
In this example the zone operator is operating two public sub zones, each with a different min platform version (the
other network parameters shared by the two zones are omitted for brevity). Each sub zone has a single notary, operated
by the zone operator, whose node info is included in the whitelist of the network parameters representing that zone.

Interesting features


* All nodes are registered with the zone’s Identity Manager Service. *(This includes the notaries.)*
* Each sub zone is represented by a network map, each with its own database and network parameters file
* Node 1 is on the “older” sub zone using a minimum platform version of 3, it is unaware Nodes 2 and 3 even exist
(just as they are unaware of it) but can use Notary 1.
* Nodes 2 and 3 and Notary 2 can all intercommunicate as one would expect


## Segregated Sub Zones

The fundamental difference between a public sub zone and a segregated one is the operation of the notaries is
deferred to a third party.


{{< important >}}
The relationship between the zone operator and the notary operator is left to the discretion
of the zone operator. The important part from the perspective of the CENM is that the signed Node Info
is transferred from the notary operator to the zone operator.


{{< /important >}}

This is shown in the following diagram:

![simple seg zones](/en/images/simple-seg-zones.png "simple seg zones")
