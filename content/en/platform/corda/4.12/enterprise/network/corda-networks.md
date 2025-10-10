---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-12:
    parent: corda-enterprise-4-12-corda-networks
tags:
- corda
- networks
title: Understanding Corda networks
weight: 10
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

* Once accepted, the requests have a certificate signed by the PKI infrastructure that governs the network. Signing is performed by a separately deployed process called the *Signing Service*. It is important to realise how
this service should be deployed. For more information, see {{< cenmlatestrelref "cenm/signing-service.md" "Signing Service" >}}. In brief, it is the
intention that, unlike the Identity Manager, the signer is completely isolated from external communication. It only
addresses a data source it shares with the Identity Manager. This ensure no hostile entity can penetrate the system
and force the signing of a certificate.
* The signed certificates are recognised by the Identity Manager and returned to the requesting node (Nodes poll the
Identity Manager periodically to see if their signature request has been fulfilled).

At the end of this process a node will have successfully registered the legal identity of the entity it is operating
on behalf of with the Zone. However, that node now needs to join one of the subzones that make up the network as a
whole.


## Subzones

{{< note >}}
This is an internal feature. Running a network with multiple subzones is not a supported configuration.

{{< /note >}}
Where the zone as a whole is defined by the unique set of identities, a subzone is a sub grouping of those entities
that agree to a common set of parameters that define the global consensus mechanisms for all members. This functionality
is offered by one or more Network Map services.

Subzones are currently categorised in relation to the mechanism a zone operator has in place for the process of
setting the network parameters for it.


* *Public subzones* where the entirety of the Network Parameters are under the sole control of the Zone Operator
* *Segregated subzones* where one or more of the Network Parameters have been delegated to the authority of some
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
Each subzone requires it’s own notary pool as no node, including notaries, can exist in more than
one subzone


{{< /important >}}

For more information, see {{< cenmlatestrelref "cenm/sub-zones.md" "Subzones" >}}.

### Operating a segregated subzone

From the perspective of a mature CENM deployment, operating a subzone post ENM 0.3 is the same as operating a single
network under the old paradigm where there was only the one zone.

Each Network Map that represents a segregated subzone is configured separately from the others as a distinct entity
unaware of one another

Each Network Map requires:

* A configuration file
* A starting set of network parameters
* One or more notaries for inclusion in the whitelist
* A signing service configured to sign the network map and network parameters


## More in this section

* [What is a compatibility zone?]({{< relref "compatibility-zones.md" >}})
    * [How do I become part of a compatibility zone?]({{< relref "compatibility-zones.md#how-do-i-become-part-of-a-compatibility-zone" >}})
        * [Bootstrapping a compatibility zone]({{< relref "compatibility-zones.md#bootstrapping-a-compatibility-zone" >}})
        * [Joining an existing compatibility zone]({{< relref "compatibility-zones.md#joining-compatibility-zones" >}})
        * [Setting up a dynamic compatibility zone]({{< relref "setting-up-a-dynamic-compatibility-zone.md" >}}) (in detail)
            * [Do you need to create your own dynamic compatibility zone?]({{< relref "setting-up-a-dynamic-compatibility-zone.md#do-you-need-to-create-your-own-dynamic-compatibility-zone" >}})
            * [Why create your own zone?]({{< relref "setting-up-a-dynamic-compatibility-zone.md#why-create-your-own-zone" >}})
            * [How to create your own compatibility zone]({{< relref "setting-up-a-dynamic-compatibility-zone.md#how-to-create-your-own-compatibility-zone" >}})
                * [Using an existing network map implementation]({{< relref "setting-up-a-dynamic-compatibility-zone.md#using-an-existing-network-map-implementation" >}})
                * [Creating your own network map implementation]({{< relref "setting-up-a-dynamic-compatibility-zone.md#creating-your-own-network-map-implementation" >}})
                    * [Writing a network map server]({{< relref "setting-up-a-dynamic-compatibility-zone.md#writing-a-network-map-server" >}})
                    * [Writing a doorman server]({{< relref "setting-up-a-dynamic-compatibility-zone.md#writing-a-doorman-server" >}})
                    * [Setting zone parameters]({{< relref "setting-up-a-dynamic-compatibility-zone.md#setting-zone-parameters" >}})
                * [Selecting parameter values]({{< relref "setting-up-a-dynamic-compatibility-zone.md#selecting-parameter-values" >}})
* [Network certificates]({{< relref "permissioning.md" >}})
    * [Certificate hierarchy]({{< relref "permissioning.md#certificate-hierarchy" >}})
    * [Key pair and certificate formats]({{< relref "permissioning.md#key-pair-and-certificate-formats" >}})
    * [Certificate role extension]({{< relref "permissioning.md#certificate-role-extension" >}})
* [The network map]({{< relref "network-map.md" >}})
    * [HTTP network map protocol]({{< relref "network-map.md#http-network-map-protocol" >}})
        * [Additional endpoints from R3]({{< relref "network-map.md#additional-endpoints-from-r3" >}})
    * [The `additional-node-infos` directory]({{< relref "network-map.md#the-additional-node-infos-directory" >}})
    * [Network parameters]({{< relref "network-map.md#network-parameters" >}})
    * [Network parameters update process]({{< relref "network-map.md#network-parameters-update-process" >}})
        * [Automatic acceptance]({{< relref "network-map.md#automatic-acceptance" >}})
        * [Manual acceptance]({{< relref "network-map.md#manual-acceptance" >}})
    * [Private networks]({{< relref "network-map.md#private-networks" >}})
    * [Cleaning the network map cache]({{< relref "network-map.md#cleaning-the-network-map-cache" >}})
* [Cipher suites supported by Corda]({{< relref "cipher-suites.md" >}})
    * [Certificate hierarchy]({{< relref "cipher-suites.md#certificate-hierarchy" >}})
    * [Supported cipher suites]({{< relref "cipher-suites.md#supported-cipher-suites" >}})
