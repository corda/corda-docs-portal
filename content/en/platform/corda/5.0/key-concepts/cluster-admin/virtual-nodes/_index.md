---
title: "Virtual Nodes"
date: 2023-07-24
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-admin-vnodes
    parent: corda5-key-concepts-cluster-admin
    weight: 3000
section_menu: corda5
---

# Virtual Nodes

From Corda 5 onwards, a single Corda deployment can host multiple virtual node identities. Previous to this, the identity and the compute process/JVM were tied. Hence in this version of Corda, we refer to virtual nodes, rather than nodes. They are now a context in which a distributed application runs under rather than the process itself.

We now also refer to application networks, as networks of virtual nodes that all run the same, or compatible, CorDapps and where membership of the network is managed by the Membership Group Manager (MGM). In other words, a virtual node represents an identity on a network of application users that is managed by the MGM.

A virtual node is abstracted from the Corda runtime, and so a Corda cluster can support many virtual nodes members of different networks. However, a given virtual node can only belong to a single application network, and only deployed to a single Corda cluster at one time, and of course, an application network can span multiple Corda clusters.

{{< 
  figure
	 src="virtual-nodes.png"
   width="50%"
	 figcaption="Virtual Nodes"
>}}

Virtual nodes are identified by their X.500 name and the ID of the network they belong to. This means that the same X.500 name (for example, the same legal entity), can exist on multiple networks at the same time. 
Future versions of Corda will support interoperability between these types of virtual nodes and networks. 

For information about managing virtual nodes using the REST API, see [Managing Virtual Nodes]({{< relref "../../../deploying-operating/vnodes/_index.md" >}}).