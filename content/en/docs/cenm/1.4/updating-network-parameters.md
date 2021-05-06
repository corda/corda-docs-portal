---
aliases:
- /updating-network-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-updating-network-parameters
    parent: cenm-1-4-operations
    weight: 160
tags:
- updating
- network
- parameters
title: Updating the network parameters
---


# Updating the network parameters

The initial network parameters can be subsequently changed through an update process. However, these changes must first
be advertised to the entire network to allow nodes time to agree to the changes.

{{< note >}}
This process changed extensively in CENM 1.3. The legacy process is still
supported for services which use the shell interface instead of the admin RPC
interface - for example, in the CENM Command-Line Interface (CLI) tool. However, this document presumes  that you
use admin RPC. For information about the legacy process, see the [CENM 1.2 documentation](../1.2/updating-network-parameters.md).
{{< /note >}}

At a high level, the process is as follows:

1. Edit the network parameters configuration. This includes setting an update deadline by which
   nodes are expected to have accepted the new parameters.
2. Set the network parameters configuration in the Zone Service.
3. Advertise the new network parameters from the Network Map Service.
4. Sign the new network parameters from the Signing Service.
5. Wait for the update deadline to pass.
6. Execute the network parameter update.
7. Sign the new network map containing the new network parameters, via the Signing Service.

## Editing network parameters configuration

See [Setting the Network Parameters](network-map.md#network-parameters)
for information on the network parameters configuration file format and options.

When updating the network parameters, ensure that the network parameters file has the
`parametersUpdate` configuration block configured, as shown in the example below:

```guess
parametersUpdate {
    description = "Important update"
    updateDeadline = "2017-08-31T05:10:36.297Z" # ISO-8601 time, substitute it with update deadline
}
```

In this example, `description` is a short description of the update that will be communicated to the nodes, and `updateDeadline` is
the time (in ISO-8601 format) by which all nodes in the network must decide that they have accepted the new parameters.
A Flag Day cannot be issued *before* the `updateDeadline` has passed, so make sure to set the right `updateDeadline` time.

{{< note >}}
Currently you can only make backward-compatible changes to the network parameters. For example, you cannot remove notaries
(they will be always added to the existing list), you can only increase the max transaction size, and so on.
{{< /note >}}

## Set network parameter update

Push the new network parameters to the Zone Service, using a command like the one below:

```bash
cenm netmap netparams update submit -p config/parameters.conf
```

The Angel Service of the Network Map Service will pick up the new network parameters
from the Zone service automatically.

## Advertise network parameter update

The next step is to tell the Network Map Service to advertise the update to
nodes, using the following command:

```bash
cenm netmap netparams update advertise
```

When the nodes on the network next poll the service for
the latest Network Map, they will be notified of the proposed parameter update.

## Sign new network parameters

You must execute the commands listed below on the Signing Service - this means that
you must run the commands from within the same secure network as the service.
The recommended deployment includes a Gateway Service dedicated to these high
security actions:

* Fetch the unsigned network parameters - command: `cenm signer netmap netparams unsigned`.
* Sign the updated network parameters - command: `cenm signer netmap netparams sign -h <hash>`.

## Node operators accept the update

Before the `updateDeadline` time, nodes will have to run the `acceptNewNetworkParameters()` RPC command to accept
new parameters. This will not
activate the new network parameters on the nodes - it will only inform the Network Map Service that the node has agreed to the
update. See [the Corda node RPC API](../../corda-os/4.6/tutorial-clientrpc-api.md) for further details.

To list network participants that have or have not accepted the new network parameters,
run the following command:

```bash
cenm signer netmap netparams update status --network-params-hash <parameters update hash value>
```

## Execute network parameters update

Once the `updateDeadline` has passed, you can issue a Flag Day. This is the act of changing the active network
parameters to be the parameters advertised in step 2. To do so, use the following
command:

```bash
cenm netmap netparams update execute
```

As a result, all nodes on the network will shut down when they next poll the service, due to a
parameter hash mismatch. The nodes that did not accept the parameter update will be removed from the network map and
will be unable to restart until they accept. The nodes that accepted can be restarted and continue as normal.

{{< note >}}
Corda 4.6 does not support hotswapping of Network Parameters within a node. As a result, all nodes will shut down in this situation, regardless of whether they have accepted the parameter update or not.
{{< /note >}}

## Sign the network map

As with signing the network parameters, you should run the high security commands listed below
from within the same network as the Signing Service:

* Fetch the unsigned Network Map - command: `cenm signer netmap unsigned`.
* Sign the Network Map - command: `cenm signer netmap sign -h <hash>`.

# Cancelling an update

It is possible to cancel a previously scheduled update. To do so, run the following command:

```bash
cenm signer netmap netparams update cancel
```

The Network Map Service will continue to advertise the cancelled update until a new network map is signed.

{{< note >}}
You should avoid advertising new parameters or cancelling the update during the period between Flag Day
issuance and the next network map signing, especially if the scheduled network map signing task is configured.
Otherwise you can cause an inconsistent parameters update record in the database and the implicit cancellation of the
issued Flag Day.
{{< /note >}}
