---
aliases:
- /head/key-concepts-ecosystem.html
- /HEAD/key-concepts-ecosystem.html
- /key-concepts-ecosystem.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-ecosystem
    parent: corda-os-4-8-key-concepts
    weight: 1010
tags:
- concepts
- ecosystem
- network
- identity
- discovery
title: Networks, identity, and discovery
---


# Networks

## Summary

* *People and businesses using Corda can communicate over a peer-to-peer network.*
* *A Corda network is made up of nodes, which represent real-world legal identities. Each node runs an instance of Corda and one or more CorDapps.*
* *Nodes communicate point-to-point—not by global broadcast.*
* *Each node has a certificate that maps its network identity to a real-world legal identity.*
* *Corda networks are semi-private—you need a certificate from the network operator to join.*

## What is a network?
On Corda, people and business interact by communicating over a peer-to-peer network of [Corda nodes](key-concepts-node.md). Each node represents a legal entity running Corda and one or more Corda distributed applications, known as [CorDapps](cordapp-overview.md).

{{< figure alt="network" width=80% zoom="/en/images/network.png" >}}
Corda is different from other distributed ledgers because all communication between nodes is point-to-point, and only shared on a need-to-know basis. It's also encrypted using transport-layer security. There are *no global broadcasts* to all parties on a network, but all of the nodes in a network can send messages directly to other nodes. If the recipient is offline, the message waits in an outbound queue until they are online again—just like an email.

## Join a network

Unlike traditional blockchain, Corda networks are semi-private. To join a network, you must obtain a certificate from the network operator. This
certificate maps the node's identity on Corda to a real-world legal identity and a [public key](https://www.investopedia.com/terms/p/public-key.asp).

The network operator enforces rules that stipulate what information nodes must provide and the know-your-customer (KYC) processes they must undergo before being granted this certificate.

## Node identities
The *network map service* matches each node identity to an IP address. Nodes use these IP addresses to send messages to each other.

Nodes can also generate confidential identities for individual transactions. The certificate chain linking a
confidential identity to a node identity or real-world legal identity is only distributed on a need-to-know
basis. Nodes can use confidential identities to protect themselves in the event that an attacker gets access to an unencrypted transaction. The attackers cannot identify the participants without additional information.

## Find other nodes on a network
Corda nodes discover each other via a *network map service*. You can think of this service as a phone book, which publishes a list of peer nodes that includes metadata about who they are and what services they can offer.
