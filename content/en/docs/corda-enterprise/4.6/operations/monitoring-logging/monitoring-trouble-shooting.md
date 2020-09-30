---
date: '2020-06-18T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-ops-monitoring-logging
tags:
- operations
- deployment
- planning
title: Troubleshooting and recovering your node
weight: 20
---
# Troubleshooting, health-checking, and recovering your node

If you are a Corda Enterprise Network Manager (CENM) services user in your Corda Enterprise environment, you can make use of the CENM node troubleshooting guide.

Here you can find [troubleshooting solutions](../../../../cenm/1.4/troubleshooting-common-issues) to issues such as:

* **Verifying a service is running and responsive** - As well as the service logs, the CENM services provideendpoints which can be used to determine the current status of the service, whether it is executing and if it is reachable.
* **Nodes are not appearing in the Network Map** - The Network Map Service and node is up and running, but the node cannot be seen from any other nodes on the network. There are a few different reasons why this could be:
    * The publishing of the node info was successfully, but the updated network map has not been signed yet.
    * There was an issue with the node info publishing such as the node’s certificate was not valid.
    * The publishing of a node info is still in progress, and the Network Map Service is awaiting a response from the
    Identity Manager Service.


## Corda Health Survey tool

[The Health Survey Tool](../../health-survey) is a command line utility that can be used to collect information about a node, which can be used by the R3 support team as an aid to diagnose support issues. It works by scanning a provided node base directory and archiving some of the important files. Furthermore, it does a deployment status check by connecting to the node and probing it and the firewall (if deployed externally) for information on configuration, service status, connection map and more.

## Ledger sync

Part of [Collaborative Recovery](../../node/collaborative-recovery/introduction-cr), LedgerSync is a CorDapp used to discover any differences between the common ledger data held by two nodes that exist on the same Business Network. This is called the **Reconciliation** stage of collaborative recovery. It uses an efficient set reconciliation algorithm to minimise the amount of network communication required. Reconciliations can be configured to run both on-demand, and at a given time (through the use of scheduled states).

All reconciliations are added to a bounded execution pool, which is configurable, for eventual execution by the internal job scheduler. Results of reconciliations are stored in the database of the node that requested the reconciliation, and work only in one direction.

This means the node that requested the reconciliation will be notified if the responding node has transactions that the requesting node does not. The responding node will not be notified if the requesting node has transactions that the responding node does not.
