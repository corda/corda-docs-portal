---
aliases:
- /releases/release-1.0/private-network-map.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-private-network-map
    parent: cenm-1-0-tools-index
    weight: 1090
tags:
- private
- network
- map
title: Private Network Map
---


# Private Network Map


{{< warning >}}
This is an internal feature that is being deprecated. Running a network with one or more private networks
is not a supported configuration.

{{< /warning >}}


The private network is a tactical solution to provide temporary privacy to the initial network map.

Private network maps can be created in one of two modes, one where auto enrolment is allowed, and one
where it isn’t. Auto enrolment is a feature whereby a node can be configured with the UUID of the private
network and communicate that information to the Identity Manager at the point it registers with the network.

That node would then be automatically added to that private network. The alternative is for the operator of
compatibility zone to have to manually move nodes into a private network after registration has occurred as a
part of their identity onboarding workflow.

Since auto enrolment removes human oversight from the process, it must be consciously chosen by the sponsor as
the default.

{{< note >}}
A private network with automatic enrolment enabled can still have nodes manually added to it.

{{< /note >}}

## Managing a private network

Managing a private network should be done via the integrated shell within the Network Map. To access the private manager
and view the tools available, log into the shell and execute the `run privateNetworkManager` command. See the
“Embedded Shell” section within the [Network Map Service](network-map.md) doc for more information on how to configure shell access.

{{< note >}}
To ensure full functionality of private networks you should ensure that Identity Manager communication is
correctly configured for the Network Map service and that `privateNetworkAutoEnrolment` is set to true.

{{< /note >}}

### Available Commands

The private network manager provides the following functionality:



* **Create A New Private Network** - Creates a persists a new private network, automatically generating a unique UUID.
* **List Existing Private Networks** - Lists all currently persisted private networks.
* **Add a Node to a Private Network** - Move a node from the public network (if previously published its node info)into the provided private network. Note that in order for this command to
succeed, the node must have registered with the Identity Manager.
* **Move a Node back to the Public Network** - Move a node from a private network back into the public network.



## [DEPRECATED] Manually managing a private network


{{< warning >}}
Since the Network Map and Identity Manager DB schema separation introduced in V0.3, creation of a new
private network requires it to be persisted in **both** the Network Map database and the Identity Manager
database. This is due to backwards compatibility constraints. Using the provided interactive shell command
described above for private network creation will handle this for you and is *strongly* recommended.

{{< /warning >}}


Although strongly discouraged, you can execute some SQL commands to manage you private network:


### Creating a private network

To create a new private network, an entry has to be created in the `private_network` table manually.

Run the following SQL script to create a new private network that doesn’t allow for auto enrolment:

```sql
insert into private_network values (NEWID(), 'Private Network Name', 0)
```

Or this to allow for auto enrolment

```sql
insert into private_network values (NEWID(), 'Private Network Name', 1)
```

Private networks auto enrolment choice can be altered at will by simply changing the value of the `allow_auto_enrolment`
to either 1 or 0 for enable and disable respectively.


### Querying private networks

Then use the following SQL to retrieve the private network ID for the private network owner:

```sql
select id from private_network where name = 'Private Network Name'
```


### Add nodes to the private network

To add a node to the private network map run the following SQL

```sql
update cert_signing_request
set private_network = '<<private_network_id>>'
where request_id in ('<<certificate_request_id>>', ...)
```

If all existing entries in the map need adding to the private map, this SQL script can be used to add all approved nodes.

```sql
update cert_signing_request
set private_network = '<<private_network_id>>'
where status = 'APPROVED'
```


{{< important >}}
If notary is to be used by private network participants add private network UUIDs to notary’s `node.conf`
using `extraNetworkMapKeys` list.

If this isn’t done, and a node from private network contacts the notary, the notary node won’t be able to send
any messages back as it doesn’t see the hidden node. This situation will result in flow hanging on waiting for
a notary response.


{{< /important >}}


### Move a node from its private network and into the global network map

```sql
update cert_signing_request
    set private_network = null
    where request_id = '<<certificate_request_id>>'
```


## Configure a node for auto enrolment

The UUID of the private network should be communicated out of band first to the sponsor of the private network
and then, through them, to the nodes operator whose node will be joining that private network. Those nodes should
then have their `networkServices` configuration set as follows.

```guess
networkServices = {
    doormanURL = "http://<some host>:<some port>"
    networkMapURL = "http://<some other host>:<some port>"
    pnm = "5E2E6F26-6736-457D-BEE6-39A3C5161FB3"
}
```

The Identity Manager will return any error to the node and reject the CSR if there are any issues with the configured
private network.

