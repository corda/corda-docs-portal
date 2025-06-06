---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-corda-nodes-notary-operate
tags:
- handling
- flag
- days
title: Handling flag days
weight: 7
---


# Handling flag days


## Consequences of flag days for the notary

A *flag day* signifies the point in time where the network stops using one set of network parameters and begins using the new, previously
proposed set of network parameters. This is discussed in [Network parameters update process]({{< relref "../network/network-map.md#network-parameters-update-process" >}}).

Once a flag day is issued, the next time a node polls the Network Map service, it will receive the updated network parameters, in turn
causing the node to shut down due to a parameter mismatch. As a Notary node (whether a basic Notary or a worker within a HA cluster) is built
upon the same foundation as a standard node, it will behave in the same way and also shut down when it next polls.

{{< note >}}
This shutdown occurs because, with one exception, it is not possible to hot swap the old set of Network Parameters with the new set, and the only
option to refresh the parameters is a node restart. A consequence of this is that there is no way to restart the Notary in a preemptive
manner prior to the flag day.

The exception is if the parameter changes _only_ update the list of notaries. In those circumstances, the node does not need to restart. See [Hotloading]({{< relref "../network/network-map.md#hotloading" >}}) for more information.

{{< /note >}}
Outlined below are some basic suggestions to best deal with flag days. Note that to avoid any issues restarting the Notary nodes, a Notary
operator should ensure that all nodes have accepted the parameter update. See [Network parameters update process]({{< relref "../network/network-map.md#network-parameters-update-process" >}}) for more information.


## Single notary

With a simple non-HA Notary service, a zero-downtime parameter update is not possible. After the flag day, the service must be restarted,
either manually and immediately after the flag day (if the network operator in control of the flag day is also in control of the Notary) or
automatically when the Notary next polls the Network Map service (e.g. using a daemon to restart the service after any shutdowns).

Although immediately restarting manually after a flag day should be preferred, there is a chance that a notarisation request is sent during
the downtime from a node who is not yet aware of the flag day. If network participants cannot handle Notary downtime then a HA notary
cluster should be run instead.


## HA notary cluster

With a HA cluster of Notary worker nodes, a zero-downtime update is possible but is dependent on the Network Map service polling schedules.
The schedule of each Notary worker’s polling will be determined by both the polling interval (specified by the Network Map service) along
with the Notary service start time. As the node will shutdown when it next polls the Network Map service, having all polling schedules be in
sync across worker nodes will mean that without manual intervention the entire HA notary cluster will shutdown after a flag day. To avoid
this situation a Notary operator should ensure that the worker nodes are started in a staggered manner and the polling intervals are not in
sync.

{{< note >}}
During the flag day roll over process the cluster can temporarily be in a state where some workers are using the old set of Network
Parameters and some are using the new set. As the Notary does not check the Network Parameters used for notarisation requests this is
not an issue.

{{< /note >}}
The best approach to achieve a zero-downtime update is to manually restart a single worker node immediately after the flag day. Where
possible, to achieve maximum worker node uptime nodes that have most recently polled the Network Map service should be prioritised *last*
for restarting.

If a daemon or some automated process is being used to resurrect dead worker nodes then the Notary operator can rely on this to
automatically handle the flag day roll-over. If the polling intervals are properly staggered then this should also result in a zero-downtime
Notary cluster however it is inherently more risky.

{{< note >}}
Each node must be restarted during a flag day. Although the HA cluster as a whole can remain active there is still the risk that a
worker node is restarted whilst processing a notarisation request. If this happens before the notarisation request is completed then
the request will fail. The current version of Corda will automatically retry notarisation requests after a predefined timeout period
which negates any issues that may arise from this scenario.

{{< /note >}}
