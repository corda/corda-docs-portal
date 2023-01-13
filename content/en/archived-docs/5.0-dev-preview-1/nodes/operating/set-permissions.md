---
title: "Managing user permissions"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-permissions
    weight: 4600
section_menu: corda-5-dev-preview
description: >
  How to configure permissions for HTTP-RPC operations.
expiryDate: '2022-09-28'  
---

Use this guide to configure permissions for HTTP-RPC operations.

The Corda 5 Developer Preview uses [Apache Shiro](https://shiro.apache.org/) libraries and databases to hold permissions data at runtime,
as described in Corda 4's guide on [managing RPC security](../../../../../../en/platform/corda/4.8/open-source/clientrpc.html#managing-rpc-security).

When expressing grants for users, you can still use extended syntax for individual users, as described in Corda 4's guide on
[defining RPC users and permissions](../../../../../../en/platform/corda/4.8/enterprise/node/operating/clientrpc.html#defining-rpc-users-and-permissions-1).


## Configure user permissions: flow initiation

For a user to start a flow via HTTP-RPC you need to:
1. Set the permissions for the target flow.
2. Grant HTTP-RPC specific permission for `FlowStarterRPCOps`: `InvokeRpc:net.corda.client.rpc.flow.FlowStarterRPCOps#startFlow`
or `InvokeRpc:net.corda.client.rpc.flow.FlowStarterRPCOps#ALL`.

Here's an example of how to configure permissions in the `node.conf` file:

For user `user1` with password `password1` to start the flow
`net.corda.sample.datapersistence.flows.RecordFlow$Initiator` (where `Initiator` is an inner class of `RecordFlow`), the `node.conf` section must include:

```shell
security {
    authService {
        dataSource {
            type=INMEMORY
            users=[
                {
                    username=user1
                    password=password1
                    permissions=[
                        "InvokeRpc:net.corda.client.rpc.flow.FlowStarterRPCOps#startFlow",
                        "StartFlow.net.corda.sample.datapersistence.flows.RecordFlow$$Initiator"
                    ]
                }
            ]
        }
    }
}
```

{{< note >}}
Double dollar signs (`$$`) are necessary as `$` is a special character in the [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md)
format, which is used in Corda's configuration files.
{{< /note >}}
