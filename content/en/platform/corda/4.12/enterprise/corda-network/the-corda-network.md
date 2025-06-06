---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-corda-network
    name: "Corda Network"
title: Corda Network
weight: 500
---


# Corda Network


[Corda Network](https://corda.network/) is a publicly-available internet of Corda nodes operated by network participants. Each
node is identified by a certificate issued by the network’s identity service, and is also discoverable on a network map.

Corda Network went live in December 2018.

## Benefits of Corda Network

Corda Network enables interoperability – the exchange of data or assets via a secure, efficient internet layer – in a way
that isn’t possible with separate, isolated Corda networks. A common trust root surrounds all transactions, and a consistent set of network parameters ensures all participants may transact with each other.

The network will support many sub-groups of participants running particular CorDapps (sometimes referred to as ‘business networks’), and these groups will often have a co-ordinating party (the ‘business network operator’) who manages the distribution of the app and rules, including membership, for its use. There is a clear separation between areas of control for the network as a whole and for individual business networks. Like the internet, Corda Network intends to exist as a background utility.

The main benefit of Corda Network for participants is being able to move cash, digital assets, and identity data from one application or line of business to another. Business network operators also benefit by being able to access network-wide services, and reuse the [trust root](https://trust.corda.network/) and network services, instead of building and managing their own.

The [Corda Network](https://corda.network/) website provides a [high-level overview](https://corda.network/joining-corda-network/onboarding-workflow) of the joining process.


# Key services

The roles of the individual services on Corda Network are described below.


## Identity Service

The Identity Service controls admissions of participants into Corda Network. The service receives certificate
signing requests (CSRs) from prospective network participants (sometimes via a business network operator) and reviews the
information submitted. A digitally signed participation certificate is returned if:


* The participant meets the requirements specified in the [Corda Network Rulebook](https://corda.network/corda-network-rulebook/introduction).
* The participant agrees to Corda Network participant terms of use.

The Corda Network node can then use the participation certificate to register itself with the Network Map Service.


## Network Map service

The Network Map Service accepts digitally signed documents describing network routing and identifying information from
nodes, based on the participation certificates signed by the Identity Service, and makes this information available to all
Corda Network nodes.


## Notary Service

The Corda design separates correctness consensus from uniqueness consensus, and the latter is provided by one or more Notary
Services. The Notary will digitally sign a transaction presented to it, provided no transaction referring to
any of the same inputs has been previously signed by the Notary, and the transaction timestamp is within bounds.

Business network operators and network participants may choose to enter into legal agreements which rely on the presence
of such digital signatures when determining whether a transaction to which they are party, or upon the details of which they
otherwise rely, is to be treated as ‘confirmed’ in accordance with the terms of the underlying agreement.


## Support Service

The Support Service is provided to participants and business network operators to manage and resolve inquiries and incidents
relating to the Identity Service, Network Map Service and Notary Service.
