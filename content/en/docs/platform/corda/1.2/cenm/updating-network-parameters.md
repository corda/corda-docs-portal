---
aliases:
- /releases/release-1.2/updating-network-parameters.html
- /docs/cenm/head/updating-network-parameters.html
- /docs/cenm/updating-network-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-updating-network-parameters
    parent: cenm-1-2-operations
    weight: 160
tags:
- updating
- network
- parameters
title: Updating the network parameters
---


# Updating the network parameters

The initial network parameters can be subsequently changed through an update process. However, these changes must first
be advertised to the entire network to allow nodes time to agree to the changes. Every time the server needs to be shutdown
and run with one of the following flags: `--set-network-parameters`, `--flag-day` or `--cancel-update`. For change to be
advertised to the nodes new network map has to be signed (either by HSM or by local signer).

Typical update process is as follows:


* Start network map with initial network parameters.
* To advertise an update:>

* Stop the Network Map service.
* Run it with `--set-network-parameters` flag, along with the network truststore related flags. See the ‘Setting
the Network Parameters’ section within the [Network Map Service](network-map.md) doc for more information. The network parameters
file must have `parametersUpdate` config block:

```guess
parametersUpdate {
    description = "Important update"
    updateDeadline = "2017-08-31T05:10:36.297Z" # ISO-8601 time, substitute it with update deadline
}
```


Where *description* is a short description of the update that will be communicated to the nodes and `updateDeadline` is
the time (in ISO-8601 format) by which all nodes in the network must decide that they have accepted the new parameters.{{< note >}}
Currently only backwards compatible changes to the network parameters can be made, i.e. notaries can’t be
removed (eg. they will be always added to the existing list), max transaction size can only increase, etc.{{< /note >}}
Upon success the process will exit. Not that as the Network Map service is up and running again, nothing will be
sent to the nodes yet.
* Start the Network Map service as normal without any flags. When the nodes on the network next poll the service for
the latest Network Map they will be notified of the proposed parameter update.



* Before the `updateDeadline` time, nodes will have to run the `acceptNewNetworkParameters()` RPC command to accept
new parameters. This will not
activate the new network parameters on the nodes, only inform the Network Map service that the node has agreed to the
update. See [https://docs.corda.net/tutorial-clientrpc-api.html](https://docs.corda.net/tutorial-clientrpc-api.html) for further details.
The Network Map’s shell contains a command to list network participants that have or haven’t accepted the new
network parameters:>
```bash
view nodesAcceptedParametersUpdate accepted: <true/false>, parametersHash: <parameters update hash value>,
pageNumber: <which page to show, every page contains 100 records>
```



It is also possible to poll the network map database to check how many network participants have accepted the new
network parameters - the information is stored in the `node-info.accepted_parameters_hash` column.
* Once the `updateDeadline` has passed, a flag day can be issued. This is the act of changing the active network
parameters to be the parameters advertised in step 2. To achieve this, restart the Network Map service with the
`--flag-day` flag. This will cause all nodes in the network to shutdown when they next poll the service due to a
parameter hash mismatch. The nodes that didn’t accept the parameter update will be removed from the network map and
unable to restart until they accept. The nodes that accepted, can be restarted and continue as normal.{{< note >}}
All nodes will currently shutdown regardless of acceptance as there is currently no hotswapping of Network
Parameters within a node.{{< /note >}}
{{< note >}}
A flag day cannot be issued *before* the `updateDeadline` has passed. Therefore this should be chosen carefully.{{< /note >}}


It is possible to cancel the previously scheduled update. To do so simply run:

```bash
java -jar networkmap.jar --cancel-update
```

The Network Map service will continue to advertise the cancelled update until the new network map is signed.

{{< note >}}
It is not recommended to advertise new parameters or cancel the update during the period between flag day
issuance and the next network map signing, especially if the scheduled network map signing task is configured.
This can result in inconsistent parameters update record in the database and implicit cancellation of the
issued flag day.

{{< /note >}}

## Updating the network paramaters via service’s shell

Network parameters updates can be done via shell commands, eliminating the need to bring the Network Map service
offline during this time. The three commands for managing this process are:


* Advertising an update with `--set-network-parameters` flag can be replaced via
`run networkParametersRegistration` shell command. For instance:>
```bash
run networkParametersRegistration networkParametersFile: params.conf, \
networkTrustStore: ./certificates/network-root-truststore.jks, \
trustStorePassword: trustpass, \
rootAlias: cordarootca
```




* Flag day can be initiated via `run flagDay` command.
* Cancellation of the previously scheduled update can be done by running `run cancelUpdate` command.

{{< note >}}
Bear in mind initial network parameters setting cannot be done via shell since Network Map service cannot run
without Network Parameters.

{{< /note >}}

## Bootstrapping the network parameters

When the Network Map service is running it will serve the current network map including the network parameters.

The first time it is started it will need to know the initial value for those parameters, these
can be specified with a file, like this:

```guess
notaries : [
    {
        notaryNodeInfoFile: "/Path/To/NodeInfo/File1"
        validating: true
    },
    {
        notaryNodeInfoFile: "/Path/To/NodeInfo/File2"
        validating: false
    }
]
minimumPlatformVersion = 1
maxMessageSize = 10485760
maxTransactionSize = 10485760
eventHorizonDays = 30 # Duration in days

whitelistContracts = {
    cordappsJars = [
        "/Path/To/CorDapp/JarFile1",
    ],
    exclude = [
        "com.cordapp.contracts.ContractToExclude1",
    ]
}

packageOwnership = [
    {
        packageName = "com.megacorp.example.claimed.package",
        publicKeyPath = "/example/path/to/public_key_rsa.pem",
        algorithm = "RSA"
    },
    {
        packageName = "com.anothercorp.example",
        publicKeyPath = "/example/path/to/public_key_ec.pem",
        algorithm = "EC"
    }
]
```

And the location of that file can be specified with: `--set-network-parameters`.

Note that when reading from file:


* `epoch` will be initialised to 1, unless a different value is specified within the config file
* `modifiedTime` will be the network map startup time

`epoch` will increase by one every time the network parameters are updated, however larger jumps can be achieved by
manually setting the next epoch value within the config file..
