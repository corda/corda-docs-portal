---
title: "Application Networks"
date: 2023-06-07
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-fundamentals-app-networks
    parent: corda5-fundamentals
    weight: 2000
section_menu: corda5
---

# Application Networks

Corda, as previously described, is a private, permissioned, {{< tooltip >}}DLT{{< /tooltip >}} platform.
An application network is a discrete instance of a permissioned collective associated with one or more applications.

Unlike public DLT platforms such as Ethereum, where the ability to use the system is open to all, access to a Corda system is gated by the entity/entities (known as the Network Operators) operating the network.
This network is associated with a {{< tooltip >}}CorDapp{{< /tooltip >}}, where the members of the network are allowed to utilize the system for some purpose. The specific rules specifying how an identity is allowed to join are left to the operator to determine.
However, once permitted to join, each member understands that each other member has had their identity challenged to the same extent.

The severity and extent of that attestation are, as previously mentioned, left to the Network Operator, but should reflect the needs of the CorDapp being operated by the network and can range from allowing anyone to join unchallenged to performing a full KYC process on each request.

The following diagram shows the application network architecture:

{{< 
  figure
	 src="application-network.png"
   width=40%
	 figcaption="Application Network"
>}}

## Identity Attestation

The Membership Group Manager ({{< tooltip >}}MGM{{< /tooltip >}}) permits identities into an application network. 
Identities wishing to join present a request containing various metadata describing them but, most importantly, their unique name and their location as an IP address.

Whilst not strictly required, it is encouraged that alongside their name, identities submit a {{< tooltip >}}PKI{{< /tooltip >}} certificate issued by a trusted authority, alongside the public key whose signature represents the identity's affirmation of acceptance. 

The process of attestation is simple: identities submit their request, additionally request an escalated role, and the Network Operator either [approves or declines the request]({{< relref "../../../application-networks/managing/registration-requests/_index.md" >}}).

### Identity Uniqueness

It is important within an application network that each identity is uniquely addressable and so each identity must present to the network a unique name.
Corda does not allow duplicate names to join a single application network.
However, the same name may exist in multiple different networks, especially if representing the same {{< tooltip >}}entity{{< /tooltip >}}. 
This is enforced at the platform level.

## Peer-to-Peer Communication

As shown below, Corda is different from other {{< tooltip >}}distributed ledger{{< /tooltip >}} systems in that all communication between nodes is peer-to-peer, and only shared on a need-to-know basis. It is also encrypted using {{< tooltip >}}TLS{{< /tooltip >}}.
There are no global broadcasts to all nodes on a network, but all nodes in a network can send messages directly to each other.
If the recipient is offline, the message waits in an outbound queue until they are online again, just like an e-mail.

{{< 
  figure
	 src="point-to-point-communication.png"
   width=25%
	 figcaption="Peer-to-Peer Communication"
>}}

Identities not registered as members of the application network cannot communicate with those that are, even if they obtain a copy of the CorDapp code:
* The identities may not be externally visible outside of the application network.
* The reverse connection attestation undertaken by the Corda networking layer ensures that only attested identities can communicate. 

## Privacy

### Communication

Through its attested identity model, Corda allows for direct [peer-to-peer messaging]({{< relref "../application-networks/_index.md/#peer-to-peer-communication" >}}) between identities. 
A proposal to mutate the global state can be undertaken without the knowledge of those not a party to that mutation; there is no need to globally broadcast updates and thus avoid leaking sensitive information.
At any single point in time, an identity can be involved in any number of distinct transactions:

{{< 
  figure
	 src="private-communication.png"
   width="25%"
	 figcaption="Private Communication"
>}}

### Global State

In Corda, as in all {{< tooltip >}}DLT{{< /tooltip >}} systems, there exists a global state. 
However, in Corda, that global state is not globally visible. 
Each participant's identity only has visibility over those portions of the global data that are relevant to it:

{{< 
  figure
	 src="global-state.png"
   width="50%"
	 figcaption="Global State"
>}}

As shown in the following diagram, there is no single storage point or distribution of data globally. 
Each identity locally stores the slices of the global state it needs to, either because:
* it is a direct participant in a mutation of the global state.
* it was added as an interested party by a participant.

{{< 
  figure
	 src="global-state-facts.png"
   width="50%"
	 figcaption="Historic and Current Facts in the Global State"
>}}

Therefore, multiple copies of data are distributed and replicated where needed:

{{< 
  figure
	 src="multiple-copies-data.png"
   width="40%"
	 figcaption="Distributed and Replicated Copies of Data"
>}}

Ultimately, the fundamental promise of Corda and all DLTs is that, once committed to the global state and accepted as valid, there can be no disagreement that an event has occurred:

{{< 
  figure
	 src="trust.png"
   width="40%"
	 figcaption="You See What I See"
>}}

Reconciliation is not needed as there is a single accepted version of valid that has been attested by all parties and that those with visibility trust.