---
title: "Application Networks"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-fundamentals-app-networks
    parent: corda5-fundamentals
    weight: 2000
section_menu: corda5
---

# Application Networks

Corda, as previously described, is a private, permissioned, DLT platform. 
An application network is a discrete instance of a permissioned collective associated with one or more applications.

Unlike public DLT platforms, such as Ethereum, where the ability to use the system is open to all, access to a Corda system is gated by the entity/entities (known as the Network Operators) choosing to operate the network. 
This network is associated with a CorDapp, where the members of the network are allowed to utilize the system for some purpose. The specific rules specifying how an identity is allowed to join are left to the operator to determine. 
However, once permitted to join, each member understands that each other member has had their identity challenged to the same extent. 

The severity and extent of that attestation are, as previously mentioned, left to the Network Operator, but should reflect the needs of the CorDapp being operated by the network and can range from allowing anyone to join unchallenged to performing a full KYC process on each request.

{{< 
  figure
	 src="application-network.png"
   width=50%
	 figcaption="Application Network"
>}}

## Identity Attestation

The Membership Group Manager (MGM) permits identities into an application network. 
Identities wishing to join present a request containing various metadata describing them but, most importantly, their unique name and their location as an IP address.

Whilst not strictly required, it is encouraged that alongside their name, identities submit a PKI (Public Key Infrastructure) certificate issued by a trusted authority, alongside the public key whose signature represents the identity's affirmation of acceptance. 

The process of attestation is simple: identities submit their request, additionally request an escalated role, and the Network Operator either [approves or declines the request]({{< relref "../../../application-networks/managing/registration-requests/_index.md" >}}).

### Identity Uniqueness

It is important within an application network that each identity is uniquely addressable and so each identity must present to the network a unique name.
Corda does not allow duplicate names to join a single application network.
However, the same name may exist in multiple different networks, especially if representing the same entity. 
This is enforced at the platform level.

## Peer-to-Peer Communication

Corda is different from other distributed ledger systems in that all communication between nodes is peer-to-peer, and only shared on a need-to-know basis. It is also encrypted using TLS (Transport Layer Security). 
There are no global broadcasts to all nodes on a network, but all nodes in a network can send messages directly to each other. 
If the recipient is offline, the message waits in an outbound queue until they are online again, just like an e-mail.

{{< 
  figure
	 src="point-to-point-communication.png"
   width=50%
	 figcaption="Peer-to-Peer Communication"
>}}

Identities not regsitered as members of the application network cannot communicate with those that are, even if they obtain a copy of the CorDapp code:
* The identities may not be externally visible outside of the application network.
* The reverse connection attestation undertaken by the Corda networking layer ensures that only attested identities can communicate. 
