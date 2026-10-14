package net.corda.client.rpc.proxy

import net.corda.client.rpc.internal.security.READ_ONLY
import net.corda.client.rpc.internal.security.RpcPermissionGroup
import net.corda.core.messaging.RPCOps
import net.corda.nodeapi.flow.hospital.FlowInfo
import net.corda.nodeapi.flow.hospital.FlowStatusQuery

/**
 * An RPC extension which provides access to the FlowHospital
 *
 * This interface is designed to allow external applications to query and view the status
 * of the flows which are currently under monitoring by the FlowHospital
 *
 * example use:
 *
```
val rpcAddress = NetworkHostAndPort("nodeAddress", 1000)
val client = MultiRPCClient(rpcAddress, NodeFlowStatusRpcOps::class.java, rpcUser.username, rpcUser.password)
val connFuture = client.start()
val conn = connFuture.get()
val flowStatusRPCOPs = conn.proxy

val matchingFlows: List<String>  = flowStatusRPCOPs.getFlowsMatching(FlowStatusQuery(
    flowClass = "IssueToken",
    flowState = FlowState.RUNNABLE,
    progressStep = "SIGNING",
    cordapp = "tokens-workflows",
    compatibleWithCurrentCordaRuntime = true,
    suspensionDuration = Duration.ofMinutes(10),
    flowStart = FlowTimeWindow.between(Instant.now().minus(30, ChronoUnit.MINUTES), Instant.now())
    )
)
matchingFlows.forEach { flowId ->
    println(flowStatusRPCOPs.getFlowStatus(flowId))
}
```
 *
 *
 */
interface NodeFlowStatusRpcOps : RPCOps {

    /**
     * @param flowId the flowId to return information for
     * @return FlowInfo object describing the suspended flow
     */

    @RpcPermissionGroup(READ_ONLY)
    fun getFlowStatus(flowId: String): FlowInfo?

    /**
     * @param query the query that should be applied for filtering the contents of the flow hospital
     * it is possible to query by:
     * @return a list of flow IDs which match the query
     * @see net.corda.nodeapi.internal.flow.hospital.FlowStatusQuery
     *
     * flowClass: String - a fragment of the class name of the flow the .* regex operator is applied to the start and end of the fragment
     * flowState: Enum ( RUNNABLE, FAILED, COMPLETED, HOSPITALIZED, KILLED, PAUSED ) - the state of the flow
     * progressStep: String - a fragment of a user defined step within the flow. The .* regex operator is applied to the start and end of the fragment
     * cordapp: String a fragment of the jar name the flow was loaded from the .* regex operator is applied to the start and end of the fragment
     * compatibleWithCurrentCordaRuntime: Boolean - whether the suspended flow is compatible (and loadable) on the current corda runtime.
     * suspensionDuration: java.time.Duration - the amount of wall-clock time that a flow has been suspended for (not execution time)
     * flowStart: net.corda.core.contracts.TimeWindow - an open or closed time window for when the flow was first started.
     *                                                  A start-open window will return all flows started before the Unix 0 Instant
     *                                                  An end-open window will return all flows started after a given time and before the current Instant
     */
    @RpcPermissionGroup(READ_ONLY)
    fun getFlowsMatching(query: FlowStatusQuery): List<String>
}
