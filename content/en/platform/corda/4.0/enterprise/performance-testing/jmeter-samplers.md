---
aliases:
- /releases/4.0/performance-testing/jmeter-samplers.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-jmeter-samplers
    parent: corda-enterprise-4-0-performance-testing
    weight: 1040
tags:
- jmeter
- samplers
title: JMeter Samplers
---


# JMeter Samplers

JMeter uses samplers to interact with the system under test. It comes with a number of built-in
[samplers](https://jmeter.apache.org/usermanual/component_reference.html#samplers), mostly
around testing web sites and infrastructure.


## Corda Flow Sampling

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

When JMeter runs a test using such a sampler, the `setupTest` method is called once at the beginning of the test for each instance of the sampler. The actual test will be calling the `runTest` method one or more times and aggregating the sample results. Finally, the `teardownTest` method will be called once per instance. As thread groups in a JMeter test plan run all of their content in parallel, a new instance of the sampler will be created for each thread in the group, and `setupTest` and `teardownTest` get called once per thread. Note that `teardownTest` will only be called once all thread groups have run and the test plan is terminating.


## Provided Sampler Clients

JMeter Corda provides a number of sampler client implementations that can be used with the Java Request sampler. They all share some common base infrastructure that allows them to invoke flows on a Corda node via RPC. All of these samplers are built against a special performance test CorDapp called `perftestcordapp`. On each call to run the sampler, one RPC flow to the respective flow used by this sampler is made, and the run function will block until the flow result is returned.



## `EmptyFlowSampler`
This sampler client has the class name `com.r3.corda.jmeter.EmptyFlowSampler` and starts the flow `com.r3.corda.enterprise.perftestcordapp.flows.EmptyFlow`. As the name suggests, the `call()` method of this flow is empty - it does not run any logic of its own. Invoking this flow goes through the whole overhead of invoking a flow via RPC without adding any additional flow work, and can therefore be used to measure the pure overhead of invoking a flow in a given set-up.

![empty flow sampler](../resources/empty-flow-sampler.png "empty flow sampler")

This sampler client requires the following minimal set of properties:
 * `label`: A label for reporting results on this sampler - if in doubt what to put here, `${__samplername}` will fill in the sampler client classname.
* `host`: The host name on which the Corda node is running. The sampler client will connect to this host via RPC. This name needs to be resolvable from where the sampler client is running - if using remote JMeter calls, this means from the server, not the client machine.
* `port`: The RPC port of the Corda node.
* `username`: The RPC user name of the Corda node.
* `password`: The RPC password of the Corda node.

These properties are also required by all of the other Corda sampler clients documented on this page.

## `CashIssueSampler`
This sampler client has the classname `com.r3.corda.jmeter.CashIssueSampler` and starts the flow
`com.r3.corda.enterprise.perftestcordapp.flows.CashIssueFlow`. This flow will self-issue 1.1 billion cash tokens on the node it is running on and store it in the vault.

![cash issue sampler](../resources/cash-issue-sampler.png "cash issue sampler")

In addition to the common properties described above under `EmptyFlowSampler`, this sampler client also requires the following property:
* `notaryName`: The X500 name of the notary that will be acceptable to transfer cash tokens issued via this sampler. Issuing tokens does not need to be notarised, and therefore invoking this sampler does not create traffic to the notary. However, the notary is stored as part of the cash state and must be valid to do anything else with the cash state, therefore this sampler will check the notary identity against the network parameters of the node.

## `CashIssueAndPaySampler`
This sampler client has the classname `com.r3.corda.jmeter.CashIssueAndPaySampler` and can start either the flow `com.r3.corda.enterprise.perftestcordapp.flows.CashIssueAndPaymentFlow` or
`com.r3.corda.enterprise.perftestcordapp.flows.CashIssueAndpaymentNoSelection`, depending on its parameters. Either way, it issues 2 million dollars in tokens and then transfers the sum to a configurable other node, thus invoking the full vault access, peer-to-peer communication and notarisation cycle.

![cash issue and pay sampler](../resources/cash-issue-and-pay-sampler.png "cash issue and pay sampler")

In addition to the parameters required for the `CashIssueSampler`, this sampler client also requires the following properties:
* `otherPartyName`: The X500 name of the recipient node of the payment.
* `useCoinSelection`: Whether to use coin selection to select the tokens for paying or use the cash reference returned by the issuance call. The value of this flag switches between the two different flows mentioned above. Coin selection adds a set of additional problems to the processing, so it is of interest to measure its impact.
* `anonymousIdentities`: Switches the creation of anonymised per-transactions keys on and off.

## `CashPaySampler`
The classname of this sampler client is `com.r3.corda.jmeter.CashPaySampler`. The `CashPaySampler` client issues cash once per run in its `setupTest` method, and then generates a transaction to pay 1 dollar `numberOfStatesPerTx` times to a specified party per sample, thus invoking the notary and the payee via P2P. This allows us to test performance with different numbers of states per transaction, and to eliminate issuance from each sample (unlike `CashIssueAndPaySampler`).

![cash pay sampler](../resources/cash-pay-sampler.png "cash pay sampler")

In addition to the base requirements as in the `CashIssueSampler`, this sampler client requires the following properties:
* `otherPartyName`: The Corda X500 name of the party receiving the payments.
* `numberOfStatesPerTx`: The number of $1 payments that are batched up and transferred to the recipient in one transaction, thus allowing to observe the impact of transaction size on peer to peer throughput and notarisation.
* `anonymousIdentities`: Switches the creation of anonymised per-transactions keys on and off.

## Custom Sampler Clients

The sampler clients provided with JMeter Corda all target the performance test CorDapp developed along with the performance test tool kit. In order to drive performance tests using different CorDapps, custom samplers need to be used that can drive the respective CorDapp via RPC.

### Loading a Custom Sampler Client

The JAR file for the custom sampler needs to be added to the search path of JMeter in order for the Java sampler to be able to load it. The `-XadditionalSearchPaths` flag can be used to do this. It takes a list of semicolon-separated directories or JAR files that will all be scanned by JMeter and added to the classpath to run tests.

If the custom sampler uses flows or states from another CorDapp that is not packaged with the JMeter Corda package, this needs to be on the classpath for the JMeter instance running the sampler, as the RPC interface
requires instantiating classes to serialize them. The easiest way to achieve this is to add it to the list of additional search paths. A typical invocation would be similar to the following:

```kotlin
java -jar jmeter-corda.jar <other args...> -XaddditionalSearchPaths=/home/<user>/mySampler.jar;/home/<user>/myCorDapp.jar

or:

java -jar jmeter-corda.jar <other args...> -XaddditionalSearchPaths=/home/<user>/mySampler.jar;<node installation dir>/cordapps/myCordapp.jar
```

When using JMeter servers for remote invocation, the exact same version of the sampler JAR needs to be deployed on each
server, and must be added to the command line of the JMeter server process (with the same `-XadditionalSearchPaths` argument).
In this case, the node running the CorDapp and the JMeter server process both need to have the same version of the CorDapp - it needs to be installed as a CorDapp on the node, and needs to be on the class path of the JMeter server process. The JMeter process can either load its own copy of the CorDapp JAR or point to the CorDapp folder of the node installation.

In the case of JMeter remote invocation, the JMeter client might not actually need the CorDapp package on the classpath,
as the interaction with the CorDapp is happening on the server side - in this case, only the server process needs to have the CorDapp JAR
file on its search path.


### Writing a Custom Sampler Client

An SDK with examples on how to write samplers to drive different CorDapps is available at [https://github.com/corda/jmeter-sampler](https://github.com/corda/jmeter-sampler). The SDK and sampler code is freely available, but please note that it requires access to a licensed local Corda Enterprise installation to be used.

See the README and the annotated code examples in the SDK for instructions on how to build your own custom sampler.
