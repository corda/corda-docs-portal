---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-toc-tree
tags:
- jmeter
- samplers
title: JMeter samplers
weight: 400
---

{{< note >}}
All mentions of `jmeter-corda.jar` on this page refer to the `jmeter-corda-<version>-capsule.jar` - see [Obtaining and Installing the Performance Test Suite](installation.html) for more information.
{{< /note >}}

# JMeter samplers

JMeter uses samplers to interact with the system under test. It comes with a number of built-in
[samplers](https://jmeter.apache.org/usermanual/component_reference.html#samplers),  mostly
around testing web sites and infrastructure.


## Corda flow sampling

For performance testing Corda, the [Java Request sampler](https://jmeter.apache.org/usermanual/component_reference.html#Java_Request) is used. This sampler works by calling
a Java class implementing the `org.apache.jmeter.protocol.java.sampler.JavaSamplerClient` interface and passing
a set of parameters:

```kotlin
public interface JavaSamplerClient {
    void setupTest(JavaSamplerContext context);

    SampleResult runTest(JavaSamplerContext context);

    void teardownTest(JavaSamplerContext context);

    Arguments getDefaultParameters();
}
```

When JMeter runs a test using such a sampler, the `setupTest` method is called once at the beginning of the test for
each instance of the sampler. The actual test will be calling the``runTest`` method one ore more times and aggregating
the sample results. Finally, the `teardownTest` method will be called once per instance. As thread groups in a JMeter
test plan run all of their content in parallel, a new instance of the sampler will be created for each thread in the
group, and `setupTest` and `teardownTest` get called once per thread. Note that `teardownTest` will only be called
once all thread groups have run and the test plan is terminating.


## Provided sampler clients

[JMeter Corda](running-jmeter-corda.md) provides a number of sampler implementations that can be used with the Java Request sampler. They all
share some common base infrastructure that allows them to invoke flows on a Corda node via RPC. All of these samplers
are built against the included performance testing CorDapps (`perftestcordapp` and `settlement-perftest-cordapp`). On each call to run the sampler, one RPC flow to the respective flow used by this sampler is made, and the run function will block until the flow result is returned.

* `EmptyFlowSampler`: this sampler has the class name `com.r3.corda.jmeter.EmptyFlowSampler` and starts the flow
`com.r3.corda.enterprise.perftestcordapp.flows.EmptyFlow`. As the name suggests, the `call()` method of this flow
is empty, it does not run any logic of its own. Invoking this flow goes through the whole overhead of invoking a flow
via RPC without adding any additional flow work, and can therefore be used to measure the pure overhead of invoking
a flow in a given set-up. This sampler client requires the minimal set of properties to be required that it shares with all Corda samplers documented here:
   * `label`: a label for reporting results on this sampler - if in doubt what to put here, `${__samplername}` will fill in the sampler class name.
   * `host`: the host name on which the Corda node is running. The sampler client will connect to this host via RPC. This name needs
to be resolvable from where the sampler client is running - for example, if using remote JMeter calls, this means from the
server, not the client machine.
   * `port`: the RPC port of the Corda node.
   * `minimumNodePlatformVersion`: the minimum platform version that the JMeter client will require from the Corda nodes. It defaults to 4, which can be used to test with Corda 4.0 nodes or later.
   * `username`: the RPC user name of the Corda node.
   * `password`: the RPC password of the Corda node.
{{< figure alt="empty flow sampler" zoom="../resources/empty-flow-sampler.png" >}}
* `CashIssueSampler`: this sampler client has the class name `com.r3.corda.jmeter.CashIssueSampler` and starts the flow `com.r3.corda.enterprise.perftestcordapp.flows.CashIssueFlow`. This flow self-issues 1.1 billion cash tokens on the node it is running on, and stores it in the vault. In addition to the common properties described for `EmptyFlowSampler` above, this sampler client also requires:
   * `notaryName`: the X500 name of the notary that is acceptable to transfer cash tokens issued via this sampler. Issuing tokens does not need to be notarised, and therefore invoking this sampler does not create traffic to the notary. However, the notary is stored as part of the cash state and must be valid to do anything else with the cash state, therefore this sampler checks the notary identity against the network parameters of the node.
* `CashIssueAndPaySampler`: this sampler client has the classname `com.r3.corda.jmeter.CashIssueAndPaySampler` and, depending on its parameters, it can start either of these flows -  `com.r3.corda.enterprise.perftestcordapp.flows.CashIssueAndPaymentFlow` or `com.r3.corda.enterprise.perftestcordapp.flows.CashIssueAndpaymentNoSelection`. Either way it issues 2 million dollars in tokens and then transfers the sum to a configurable other node, thus invoking the full vault access, peer-to-peer communication and notarisation cycle. In addition to the parameters required for `CashIssueSampler`, this sampler also requires:
   * `otherPartyName`: the X500 name of the recipient node of the payment.
   * `useCoinSelection`: whether to use coin selection to select the tokens for paying, or use the cash reference returned by the issuance call. The value of this flag switches between the two different flows mentioned above. Coin selection adds a set
of additional problems to the processing, so it is of interest to measure its impact.
   * `anonymousIdentities`: switches the creation of anonymised per-transactions keys on and off.
* `CashPaySampler`: a sampler that issues cash once per run in its `setupTest` method, and then generates a transaction to pay one dollar `numberOfStatesPerTx` times to a specified party per sample, thus invoking the notary and the payee via P2P. This allows to test performance with different numbers of states per transaction, and to eliminate issuance from each sample (unlike `CashIssueAndPaySampler`). The classname of this sampler client is `com.r3.corda.jmeter.CashPaySampler`. In addition to the base requirements defined for `CashIssueSampler` above, this sampler client requires the following parameters:
    * `otherPartyName`: the Corda X500 name of the party receiving the payments.
    * `numberOfStatesPerTx`: The number of $1 payments that are batched up and transferred to the recipient in one transaction, thus allowing to observe the impact of transaction size on peer-to-peer throughput and notarisation.
    * `anonymousIdentities`: switches the creation of anonymised per-transactions keys on and off.
* `SettlementFlowSampler`: a sampler that issues some tokens to every node per run in its `setupTest` method and then generates transactions to swap these tokens between the nodes, thus involving signature collection and communication of the finalised transaction across multiple nodes. This allows to test the performance of a flow that involves multiple nodes. In addition to the common properties defined for `EmptyFlowSampler` above, this sampler client also requires:
    * `notaryName`: the X500 name of the notary that will be used to finalise the transactions.
    * `otherPartiesNames`: the X500 names of the parties that will be involved in the transactions. The provided list will be split into two sublists. The nodes in the first list will be issued assets of one class (for example, cash), while the nodes in the second list will be issued assets of a different class (for example, stocks).
    * `withVaultStateSelection`: a boolean value indicating whether the states, which are to be swapped, will be selected by the nodes by querying the vault, or the client will specify them explicitly. If the value is set to `true`, the JMeter client will request that the Corda node performs a swap of specific amounts of assets, and the nodes will be responsible for querying the vault and specifying the states that sum up to the amount and that are to be exchanged. If the value is set to `false`, the JMeter client will keep track of the issued states and will re-use them in the subsequent swaps, thus not requiring from the other nodes to query the vault. The vault state selection, combined with the soft locking, can become a bottleneck, so it might be beneficial to disable in when testing under high throughput.
* `BackchainSettlementFlowSampler`: a sampler that issues some tokens to every node and creates bilateral payments with other nodes of these assets to generate backchains of the specified size for every run in its `setupTest` method. It then generates transactions to swap these tokens between the nodes, thus forcing nodes to resolve the backchains of the states they do not "know" about. This allows to test the performance of a flow that involves multiple nodes, where many of them need to perform transaction resolution. In addition to the common properties defined for `EmptyFlowSampler` above, this sampler client also requires:
	* `notaryName`: the X500 name of the notary that will be used to finalise the transactions.
	* `otherPartiesName`: the X500 names of the parties that will be involved in the transactions. The provided list will be split into two sublists. The nodes in the first list will be issued assets of one class (for example, cash), while the nodes in the second list will be issued assets of a different class (for example, stocks). The nodes from the first group will then form pairs with the nodes from the second group. Bilateral payments will be performed during the setup between these pairs in order to generate backchains unknown to the other pairs. During the test, transactions will contain asset swaps between all these pairs.
	* `backchainSize`: the size of the backchain that will be generated during the test setup via bilateral payments.


## Custom sampler clients

The sampler clients provided with [JMeter Corda](running-jmeter-corda.md) all target the performance testing CorDapps developed along with the
performance test tool kit. In order to drive performance tests using different CorApps, custom samplers need to be
used that can drive the respective CorDapp via RPC.


### Loading a custom sampler client

The JAR file for the custom sampler needs to be added to the search path of JMeter in order for the Java sampler to
be able to load it. The `-XadditionalSearchPaths` flag can be used to do this. It takes a list of semicolon separated
directories or JAR files that all will be scanned by JMeter and added to the classpath to run tests.

If the custom sampler uses flows or states from another CorDapp that is not packaged with the
JMeter Corda package, this needs to be on the classpath for the JMeter instance running the sampler as the RPC interface
requires instantiating classes to serialize them. The easiest way to achieve this is to add it to the list of additional
search paths. A typical invocation would look like:

```kotlin
java -jar jmeter-corda.jar <other args...> -XaddditionalSearchPaths=/home/<user>/mySampler.jar;/home/<user>/myCorDapp.jar

or:

java -jar jmeter-corda.jar <other args...> -XaddditionalSearchPaths=/home/<user>/mySampler.jar;<node installation dir>/cordapps/myCordapp.jar
```

When using JMeter servers for remote invocation, the exact same version of the sampler JAR needs to be deployed on each
server, and be added to the command line of the JMeter server process (with the same `-XadditionalSearchPaths` argument).
In this case, the node running the CorDapp and the JMeter server process both need to have the same version of the CorDapp - it needs to be
installed as a CorDapp on the node, and needs to be on the class path of the JMeter server process. The JMeter process can either load its own
copy of the CorDapp JAR or point to the CorDapp folder of the node installation.

In the case of JMeter remote invocation, the JMeter client might not actually  need the CorDapp package on the classpath,
as the interaction with the CorDapp is happening server side - in this case, only the server process needs to have the CorDapp JAR
file on its search path.


### Writing a custom sampler client

An SDK with examples on how to write samplers to drive different CorDapps is availabe at [https://github.com/corda/jmeter-sampler](https://github.com/corda/jmeter-sampler)
The SDK and sampler code is freely available, but please note that it requires access to a licensed local Corda Enterprise installation
to be used.

See the README and the annotated code examples in the SDK for instructions how to build your own custom sampler.
