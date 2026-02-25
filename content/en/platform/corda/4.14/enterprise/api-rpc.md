---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-nodes-operating-interacting
tags:
- api
- rpc
title: 'RPC operations'
weight: 2
---


# RPC operations

The node’s owner interacts with the node solely via remote procedure calls (RPC). The node’s owner does not have
access to the node’s `ServiceHub`.

The key RPC operations exposed by the node are:

- `CordaRPCOps.currentNodeTime`: Returns the current time according to the node’s clock. It is a 'quick RPC'. It bypasses the thread pool and other regular RPCs waiting in it, allowing the node to reply relatively quickly.
- `CordaRPCOps.isReadOnlyNode`: Allows you to check the [read-only status]({{< relref "node/setup/read-only-nodes.md" >}}) of a node. It returns true if the node is configured as read-only, otherwise false
- `CordaRPCOps.killFlow()`: Attempts to kill a flow. This is not a clean termination and should be reserved for exceptional cases such as stuck fibers. Returns whether the flow existed and was killed.
- `CordaRPCOps.networkMapFeed`: Returns a list of network nodes and observable changes to the network map
- `CordaRPCOps.nodeDiagnosticInfo`: Returns diagnostic information about the node, including the version and CorDapp details
- `CordaRPCOps.nodeInfo`: Returns the network map entry of the node, including its address and identity details as well as the platform version information
- `CordaRPCOps.partyFromKey/CordaRPCOps.wellKnownPartyFromX500Name`: Retrieves a party on the network based on a public key or X.500 name
- `CordaRPCOps.registeredFlows`: Returns a list of registered flows on the node
- `CordaRPCOps.startFlowDynamic`: Start one of the node’s registered flows
- `CordaRPCOps.startTrackedFlowDynamic`: The same as `startFlowDynamic` above, but also returns a progress handle for the flow
- `CordaRPCOps.uploadAttachment`/`CordaRPCOps.openAttachment`/`CordaRPCOps.attachmentExists`: Uploads, opens and checks for the existence of attachments
- `CordaRPCOps.vaultQueryBy`: Extract states from the node’s vault based on a query criteria
- `CordaRPCOps.vaultTrackBy`: The same as `vaultQueryBy` above, but also returns an observable of future states matching the query

## RPC Authentication Rate Limiting

To protect the RPC listener from brute-force login attempts and abusive authentication activity, Corda supports
configurable rate limiting of RPC login attempts. When enabled, repeated failed authentication attempts from
the same IP address will trigger a temporary suspension period during which further failed attempts
are rejected. This helps mitigate credential-stuffing and denial-of-service scenarios while allowing
legitimate clients to retry after a backoff period.

See [rateLimit]({{< relref "node/setup/corda-configuration-fields.md#rateLimit" >}}) for details on how to configure this feature.
