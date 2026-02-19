---
date: '2023-09-25'
menu:
  corda-enterprise-4.14:
    parent: corda-enterprise-4.14-corda-networks
    identifier: corda-enterprise-4.14-corda-networks-parameters
tags:
- network
- map
title: Network parameters
weight: 35
---


Network parameters are a set of values that every node participating in the zone needs to agree on and use to
correctly interoperate with each other. They can be thought of as an encapsulation of all aspects of a Corda deployment
on which reasonable people may disagree.

While other blockchain/DLT systems typically require a source code fork to
alter various constants (such as the total number of coins in a cryptocurrency or the port numbers to use), in Corda we
have refactored these sorts of decisions out into a separate file and allow *zone operators* to make decisions about
them. The zone operator signs a data structure that contains the values and they are distributed along with the network map.
Tools are provided to gain user opt-in consent to a new version of the parameters and ensure everyone switches to them
at the same time.

If the node is using the HTTP network map service, then on first startup it will:

* Download the signed network parameters
* Cache them to a `network-parameters` file
* Apply them to the node


{{< warning >}}
If the `network-parameters` file is changed and no longer matches what the network map service is advertising,
then the node will automatically shutdown. To resolve this, delete the incorrect file and restart the node so
that the parameters can be downloaded again.

{{< /warning >}}


If the node is not using a HTTP network map service, then it is expected that the signed file is provided by another means.
For such a scenario there is the [Network Bootstrapper]({{< relref "../network-bootstrapper.md" >}}) tool, which in addition to generating the network parameters file,
also distributes the node info files to the node directories.

More parameters will be added in future releases to regulate attributes such as:

- Allowed port numbers
- Whether or not IPv6 connectivity is required for zone members
- Required cryptographic algorithms
- roll-out schedules (for example, for moving to post-quantum cryptography)
- Parameters related to SGX, and so on

For the list of available network parameters, see [Available network parameters]({{< relref "available-network-parameters.md" >}}).

## Updating network parameters

Network parameters are controlled by the zone operator of the Corda network that you are a member of. Occasionally, they may need to change
these parameters. There are many reasons that can lead to this decision; for example:

- Adding a notary
- Setting new fields that were added to enable smooth network interoperability
- Changing the existing compatibility constants is required.

Updating of the parameters by the zone operator is done in two phases:

1. Advertise the proposed network parameter update to the entire network.
2. Switching the network onto the new parameters - also known as a *flag day*.

{{< note >}}
When a flag day is run, all nodes (regardless of whether they have accepted or not) shut down. The nodes that previously accepted the update can be restarted. The nodes that did not accept must manually purge their network parameters file before restarting.
{{< /note >}}

The proposed parameter update will include, along with the new parameters, a human-readable description of the changes as well as the
deadline for accepting the update. The acceptance deadline marks the date and time that the zone operator intends to switch the entire
network onto the new parameters. This will be a reasonable amount of time in the future, giving the node operators time to inspect,
discuss and accept the parameters.

The fact a new set of parameters is being advertised shows up in the node logs with the message
*Downloaded new network parameters*, and programs connected via RPC can receive `ParametersUpdateInfo` by using
the `CordaRPCOps.networkParametersFeed` method. Typically, a zone operator would also email node operators to let them
know about the details of the impending change, along with the justification, how to object, deadlines and so on.

{{< note >}} You can add notary entries to your network parameters, but they cannot be deleted. Even after an existing notary identity is revoked
and a replacement is registered to the network, the original notary will continue to appear in the list of available
notaries. Use explicit notary selection in your CordApp to avoid issues when adding a new notary to the network parameters. {{< /note >}}

### Automatic acceptance

If the only changes between the current and new parameters are for auto-acceptable parameters then, unless configured otherwise, the new
parameters will be accepted without user input. The following parameters with the `@AutoAcceptable` annotation are auto-acceptable:

This behaviour can be turned off by setting the optional node configuration property `networkParameterAcceptanceSettings.autoAcceptEnabled`
to `false`. For example:

```guess
...
networkParameterAcceptanceSettings {
    autoAcceptEnabled = false
}
...
```

It is also possible to switch off this behaviour at a more granular parameter level. This can be achieved by specifying the set of
`@AutoAcceptable` parameters that should not be auto-acceptable in the optional
`networkParameterAcceptanceSettings.excludedAutoAcceptableParameters` node configuration property.

For example, auto-acceptance can be switched off for any updates that change the `packageOwnership` map by adding the following to the
node configuration:

```guess
...
networkParameterAcceptanceSettings {
    excludedAutoAcceptableParameters: ["packageOwnership"]
}
...
```


### Manual acceptance

If the auto-acceptance behaviour is turned off via the configuration or the network parameters change involves parameters that are
not auto-acceptable then manual approval is required.

In this case the node administrator can review the change and decide if they are going to accept it. The approval should be done
before the update Deadline. Nodes that don’t approve before the deadline will likely be removed from the network map by
the zone operator, but that is a decision that is left to the operator’s discretion. For example the operator might also
choose to change the deadline instead.

If the network operator starts advertising a different set of new parameters then that new set overrides the previous set.
Only the latest update can be accepted.

To send back parameters approval to the zone operator, the RPC method `fun acceptNewNetworkParameters(parametersHash: SecureHash)`
has to be called with `parametersHash` from the update. Note that approval cannot be undone. You can do this via the [Corda shell]({{< relref "../node/operating/shell.md" >}}):

`run acceptNewNetworkParameters parametersHash: "ba19fc1b9e9c1c7cbea712efda5f78b53ae4e5d123c89d02c9da44ec50e9c17d"`

If the administrator does not accept the update, then the next time the node polls the network map after the deadline, the
advertised network parameters will be the updated ones. The previous set of parameters will no longer be valid.
At this point, the node will automatically shut down and will require the node operator to restart the node.

### Hotloading

Most network parameter changes require that a node is stopped and restarted before the changes are accepted. The exception to this is when the network parameter changes only update notaries. Updates that have only changes to notaries can be accepted without a restart. In other words, they can be *hotloaded*.
