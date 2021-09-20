---
aliases:
- /corda-networks.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-corda-networks
    parent: cenm-1-4-concepts-and-overview
    weight: 20
tags:
- corda
- networks
title: Corda Networks
---


# Corda Networks

A Corda network is a collection of nodes with a vetted, unique identity that share a common “root of trust”
upon which all certificates and signatures are ultimately chained back to. The tooling that enables this infrastructure
is provided by the Enterprise Network Manager suite of tools, specifically the Identity Manager component.

As part of their boot-strapping process nodes submit their identity (public key and x500 name) to the Identity Manager
of the network they wish to join. From there a number of things happen:


* The request is recorded in the global store of identities
* A new request is created via the workflow engine of choice to facilitate the verification of the submitters legal
identity. The extent to which this is conducted is left to the discretion of the operator of the network but
should be consistent with their existing policies on such things.{{< note >}}
Alternatively, the service can be configured to automatically accept signature requests. However, this is
not the recommended deployment model outside of a testing setup.{{< /note >}}

* Once accepted the requests have a certificate signed by the PKI infrastructure that governs the network.Signing is performed by a separately deployed process called “The Signing Service”. It is important to realise how
this service should be deployed (for more details on this see the Signing Service documentation), in brief, it is the
intention that, unlike the Identity Manager, the signer is completely isolated from external communication. It only
addresses a data source it shares with the Identity Manager. This ensure no hostile entity can penetrate the system
and force the signing of a certificate. See [Signing Services](signing-service.md)
* The signed certificates are recognised by the Identity Manager and returned to the requesting node (Nodes poll the
Identity Manager periodically to see if their signature request has been fulfilled).

At the end of this process a node will have successfully registered the legal identity of the entity it is operating
on behalf of with the Zone. However, that node now needs to join one of the sub zones that make up the network as a
whole.


## Sub Zones

{{< note >}}
This is an internal feature. Running a network with multiple sub-zones is not a supported configuration.

{{< /note >}}
Where the zone as a whole is defined by the unique set of identities, a sub zone is a sub grouping of those entities
that agree to a common set of parameters that define the global consensus mechanisms for all members. This functionality
is offered by one or more Network Map Services.

Sub Zones are currently categorised in relation to the mechanism a zone operator has in place for the process of
setting the network parameters for it.


* *Public Sub Zones* where the entirety of the Network Parameters are under the sole control of the Zone Operator
* *Segregated Sub Zones* where one or more of the Network Parameters have been delegated to the authority of some
third party.

Note, in either circumstance the operation of the Network Map in question is still under the perview by the Zone
Operator, with a suitable out-of-band process established with the party to communicate the deferred parameter
entity.

{{< note >}}
Realistically, a segregated zone will operate to allow a third party to operate a notary on it’s own
terms rather than submit to the scrutiny of the global zone community or where the zone operator wishes to allow
stratification of the min platform version applied to a network

{{< /note >}}

{{< important >}}
Each sub zone requires it’s own notary pool as no node, including notaries, can exist in more than
one sub zone


{{< /important >}}

For more information, see [Sub Zones](sub-zones.md)


### Operating a Segregated Sub Zone

From the perspective of a mature CENM deployment, operating a sub zone post CENM 0.3 is the same as operating a single
network under the old paradigm where there was only the one zone.

Each Network Map that represents a segregated sub zone is configured separately from the others as a distinct entity
unaware of one another

Each Network Map Service requires:

* A configuration file.
* A starting set of network parameters.
* One or more notaries for inclusion in the whitelist.
* A signing service configured to sign the network map and network parameters.
