---
title: "Extending RPC functionality"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing
    identifier: corda-5-dev-preview-1-nodes-developing-extending-rpc
    weight: 1600
section_menu: corda-5-dev-preview
description: >
  How to extend RPC functionality using `RPCOps`.
---

A Corda node can contain many RPC functions, which facilitate a range of operations. For example, you can:
* Get a list of all the CorDapps installed.
* Manage flows: start a flow, enquire about a flow's progress/state, or receive flow execution results.

Use this guide to extend a set of available RPC operations.

## Extend the `RPCOps` interface

You can extend the `RPCOps` interface by including additional classes that represent a set of RPC functions.
First, include the methods that you expect an RPC client to invoke.

This example shows a trivial interface which extends `RPCOps` to provide some additional abstract methods:

````kotlin
@HttpRpcResource(
        name = "NodeIdentityRPCOps",
        description = "Various operations related to the identity of the Corda node in the network",
        path = "nodeidentity"
)
interface NodeIdentityRPCOps : RPCOps {

    @HttpRpcGET(
            title = "Obtains this node's MemberInfo")
    fun getMyMemberInfo(): RpcMemberInfo

    @HttpRpcGET(
            title = "Obtains node's network readiness status")
    fun getNetworkReadinessStatus(): RpcNetworkReadinessStatus

    /**
     * Returns a list of candidate matches for a given string, with optional fuzzy(ish) matching. Fuzzy matching may
     * get smarter with time, for example by correcting spelling errors, so you should not hard-code indexes into the results.
     * Instead, show them via a user interface and let the user pick the one they want.
     *
     * @param query The string to check against the X.500 name components.
     * @param exactMatch If true, a case-sensitive match is done against each component of each X.500 name.
     */
    @HttpRpcGET(
            title = "Retrieves set of party given matching criteria")
    fun partiesFromName(
            @HttpRpcQueryParameter(
                    description = "Query string to perform match upon",
                    required = true
            )
            query: String,
            @HttpRpcQueryParameter(
                    description = "Whether to do exact match or allow fuzzy matches",
                    required = false,
                    default = "false"
            )
            exactMatch: Boolean): Set<CordaX500Name>
}
````
{{< note >}}
For details about `@Http...` annotations, see <a href="expose-rpc/annotation.md">`RPCOps` annotations</a>.
{{< /note >}}

{{< note >}}
When selecting input parameters and return results of RPC methods, keep in mind that with HTTP-RPC transport in place, the payload will ultimately be represented as JSON.
{{< /note >}}

After you define the interface, create a server (node side) implementation of it.

## Implement the extended `RPCOps` interface

If you implemented a simplified version of the example, it might include the class
`NodeIdentityRPCOpsImpl` implementing `NodeIdentityRPCOps` interface. This would implement the abstract
methods:

```kotlin
@ServiceProvider(NodeRpcOps::class)
internal class NodeIdentityRPCOpsImpl : NodeIdentityRPCOps, NodeRpcOps<NodeIdentityRPCOps> {

    override val protocolVersion: Int = PLATFORM_VERSION
    override val priority: Int = LifecycleObserver.RPC_PRIORITY_NORMAL
    override fun getVersion(nodeServicesContext: InitialContext): Int = 1

    override val targetInterface: Class<NodeIdentityRPCOps> = NodeIdentityRPCOps::class.java

    private lateinit var myInfo: MemberInfo

    private lateinit var identityService: IdentityService

    private lateinit var diagnosticsService: DiagnosticsService

    private lateinit var nodeAdmin: NodeAdmin

    private lateinit var memberLookupService: MemberLookupServiceInternal

    override fun update(nodeLifecycleEvent: LifecycleEvent): Try<String> {
        return when (nodeLifecycleEvent) {
            is LifecycleEvent.AfterNodeStart<*> -> Try.on {
                val nodeServicesContext = nodeLifecycleEvent.servicesContext as ExtendedNodeServicesContext
                myInfo = nodeServicesContext.myInfo
                identityService = nodeServicesContext.identityService
                diagnosticsService = nodeServicesContext.diagnosticsService
                nodeAdmin = nodeServicesContext.nodeAdmin
                memberLookupService = nodeServicesContext.memberLookupService as MemberLookupServiceInternal
                reportSuccess(nodeLifecycleEvent)
            }
            else -> super.update(nodeLifecycleEvent)
        }
    }

    override fun getMyMemberInfo(): RpcMemberInfo {
        return convertToRpcMemberInfo(myInfo)
    }

    override fun partiesFromName(query: String, exactMatch: Boolean): Set<CordaX500Name> {
        return memberLookupService.lookupNames(query, exactMatch)
    }

    override fun getNetworkReadinessStatus(): RpcNetworkReadinessStatus {
        return RpcNetworkReadinessStatus(memberLookupService.nodeReady.isDone, memberLookupService.isGroupManager,
                memberLookupService.groupManagerInfo.party.name)
    }
}
```

In this code example, you can see how `memberLookupService` (and a few others) are discovered.
`memberLookupService` is key for this implementation.

The rest of the code indicates:
* The `RPCOps` interface being exposed.
* The version of the functionality being exposed. There may be multiple implementations of the same
  interface installed at the same time.
* The platform version that was used at compile time of the `RPCOps` implementation.
* Where this implementation sits in the node's lifecycle events distribution list in comparison to its siblings. This is presented in priority order.

{{< note >}}
No HTTP-RPC annotations are necessary for the `RPCOps` implementation. You only need to provide them at the interface level.
{{< /note >}}

Every pluggable `RPCOps` implementation has a facility to listen to the node's lifecycle events. Whenever a `RPCOps`
implementation is notified about a lifecycle event, it's also an opportunity to wire the node's internal
services essential for the functioning of `RPCOps`.

The annotation `@ServiceProvider(NodeRpcOps::class)` is an instruction to wire the `RPCOps`
implementation as an OSGi service via
[Service Loader Mediator Specification](https://docs.osgi.org/specification/osgi.cmpn/7.0.0/service.loader). This annotation
needs to appear at the beginning of your `RPCOps` implementation.

[Service Loader](https://docs.oracle.com/javase/9/docs/api/java/util/ServiceLoader.html) is responsible for discovering `RPCOps` implementations, so you must include its class name in the `META-INF/services/net.corda.ext.api.NodeRpcOps` file.

## Test `RPCOps` implementation

Use the integration test `net.corda.extensions.node.rpc.CordaRPCOpsImplFactoryTest` to make sure that
your `RPCOps` implementations are correctly registered and will be discovered during node start-up.
