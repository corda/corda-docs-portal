---
aliases:
- /head/compatibility-zones.html
- /HEAD/compatibility-zones.html
- /compatibility-zones.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-compatibility-zones
    parent: corda-community-4-12-corda-networks-index
    weight: 1010
tags:
- compatibility
- zones
title: What is a compatibility zone?
---




# What is a compatibility zone?

Every Corda node is part of a “zone” (also sometimes called a Corda network) that is *permissioned*. Production
deployments require a secure certificate authority. We use the term “zone” to refer to a set of technically compatible
nodes reachable over a TCP/IP network like the internet. The word “network” is used in Corda but can be ambiguous with
the concept of a “business network”, which is usually more like a membership list or subset of nodes in a zone that
have agreed to trade with each other.


## How do I become part of a compatibility zone?


### Bootstrapping a compatibility zone

You can easily bootstrap a compatibility zone for testing or pre-production use with either the
[Network Bootstrapper]({{< relref "network-bootstrapper.md" >}}) or the [Corda Network Builder]({{< relref "network-builder.md" >}}) tools.


### Joining an existing compatibility zone

After the testing and pre-production phases, users are encouraged to join an existing compatibility zone such as Corda
Network (the main compatibility zone). See [Joining an existing compatibility zone]({{< relref "joining-a-compatibility-zone.md" >}}).


### Setting up a dynamic compatibility zone

Some users may also be interested in setting up their own dynamic compatibility zone. For instructions and a discussion
of whether this approach is suitable for you, see [Setting up a dynamic compatibility zone]({{< relref "setting-up-a-dynamic-compatibility-zone.md" >}}).
