---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-toc-tree
tags:
- introduction
title: Introduction
weight: 100
---


# Introduction


## Corda Performance Test Suite

Use the Corda Enterprise performance test suite to stress/soak test a Corda installation, driving either a single
node or a small network of nodes including a notary.
It uses [Apache JMeter](https://jmeter.apache.org) to start flows on nodes via RPC calls, and
capture the start/return rates and thus throughput of the system under test.


{{< warning >}}
This guide assumes that you have a working Corda test network or
know how to set one up - the set-up and topology of the Corda network as well as the hardware used can have a sweeping
impact on performance, so there is not much point in performance testing before these points have been considered.

{{< /warning >}}



## Test Architecture

A typical test architecture consists of the following components:


* a Corda network to be tested. This should be a network of Corda nodes along with a notary that is self-contained
(i.e. does not depend on any external services). See e.g. ../corda-test-networks for information on
setting up a network.
* a CorDapp that is to be tested and needs to be installed on the cluster
* an app to drive the test - Apache JMeter is used here


### Apache JMeter

Apache JMeter runs tests that repeatedly trigger an action, wait for a response and record start/success/failure
timings and so on, and allow to view the result data interactively or rendered as reports in various formats. Run controls
like parallelising tasks, running tasks in a specific order and count and time based repetitions are already built in.

The interactions with the system under test are done via so called *samplers* (see [JMeter Samplers](jmeter-samplers.md)) that can be
triggered by JMeter and then
run an action. JMeter has a number of built-in samplers, mostly around web technology, e.g. for HTTP requests, database
queries, starting scripts and so on. It is also possible to provide custom samplers that can run Java code when invoked.

For the Corda performance tests, a custom sampler is used that invokes one or more specific flows via remote procedure
calls (RPC), where all the required parameters for the flow and RPC call are passed to the sampler as parameters from
the test definition.


#### Interactive Mode

By default, JMeter runs in interactive mode, i.e. it brings up a graphical user interface (GUI) that allows the user to
create, view, modify and run a test definition. Tests can either be in process (i.e. the sampler runs in the GUI
process) or can be fanned out to a set of JMeter server instances that will run under the control of a JMeter client
connected to them (see [Server Mode](#jmeter-server))


#### Non-Interactive Mode

Once a test definition is complete, it can be run in headless mode by providing the test definition and a report target
directory on the command line.



#### Server Mode

By adding the `-s` flag,  JMeter can run as a server process that runs samplers controlled by a client connected to it
via Java Remote Method Invocation (RMI).
This allows a single client to e.g. run load from various servers for one test run and collate all the results in the
client.


### jmeter-corda

Apache JMeter can be fairly tricky to run in a specific configuration - therefore the Corda Enterprise performance test
suite provides a wrapper around JMeter that comes in a fat JAR with all required dependencies and a default configuration,
and sets up the required directories and config files that JMeter needs to start. It is also bundled with a set of default
Corda performance test samplers. On top of that, it supports opening SSH tunnels to machines running remote JMeter server
instances.


### Performance Test CorDapps

The performance test suite contains two CorDapps that can be used for performance testing:
*  A performance test CorDapp called `perftest-cordapp.jar`, which is roughly modelled on the
finance CorDapp shipped with Corda Enterprise. It contains a number of flows that issue tokens and pay these to other
parties. For example, there are flows that issue and pay tokens with or without using coin selection, or others that create arbitrary
numbers of change output or coin input states to test the behaviour of the system when using various transaction sizes
and shapes.
* A performance test CorDapp called `settlement-perftest-cordapp`, which models a digital asset exchange, where assets can be issued to nodes, transferred bilaterally between them, and exchanged in batch via atomic swap transactions. This CorDapp can be used to exercise scenarios of flows running across multiple nodes.


### Basic Performance Test Set-Up

The typical set-up used for performance tests at R3 consists of a small Corda network of 2-4 nodes and a notary to
notarise transactions. These all run inside a datacenter or virtual network in the cloud with open connectivity (or at
least Corda P2P and RPC communication enabled between the nodes). On each of the node machines, an instance of JMeter
is running in server mode.

The driving app sits outside the network and connects to the JMeter servers through SSH tunnels. In the basic test
measuring the throughput of a node, the test definition instructs all JMeter servers to open RPC connections to one node,
thus saturating the RPC handler and driving the node as hard as possible. The test might invoke a flow that can be completed locally (for example, cash issuance) or it might require exchanging P2P messages with other nodes (for example, cash payment).

{{< figure alt="jmeter network overview" zoom="../resources/jmeter-network-overview.png" >}}

## Performance Tests

There are a number of different parts of the system that can be benchmarked with different performance tests, represented
by different test plans and/or samplers. In general, the closer a performance test is to real world load, the less it is
possible to isolate pinch points in the system under test. Hence a typical performance test run consists a of a number
of these tests that allow seeing where a performance drop off occurs.

If the reasons for a performance bottleneck cannot be figured out using a set of performance tests, it might be necessary
to attach a remote profile app to one of the nodes and profile a manual performance run using any of the suite of
existing JVM profiling tools available on the market.

The performance test suite contains test plans, CorDapp and sampler for the following tests:


### Performance of a Single Node

These tests stress components in a single node, without any dependencies on other nodes in the flow.


#### Empty Flow

The `EmptyFlow` test is part of the `perftest-cordapp` CorDapp. As its name suggests, this flow is empty and does not have any effect of its own - its purpose is to provide a timing for the overhead involved in starting a flow, such as RPC handling, deserialisation of the request, starting/winding down a flow, and sending the response. Note that a flow that requires inputs via RPC might have a larger overhead as these might need to be deserialised.


#### Issuance

The `CashIssueFlow` test is part of the `perftest-cordapp` CorDapp. It issues cash to the same node where the flow is invoked. In addition, it loads/starts the CorDapp, creates states in the vault, and thus uses persistence to the database.


### Inter-Node Performance

These are flows that are, to varying degrees, closer to modelling real-world loads.

#### Issue and Pay Flows

This is a set of flows (`CashIssueAndPaymentFlow` and `CashIssueAndPaymentNoSelection`) that are part of the `perftest-cordapp` CorDapp. They make the node under test issue some cash to itself, and then pay it to a second node. This involves initiating a transaction with the target node, and then having the transaction notarised by a network notary, thus creating a load that is similar to what a node would do under real-world conditions. These flows have a few variations that can be controlled through the test definition:

* Use of coin selection: the flows can either just pay the issued cash, or use coin selection to select the cash to pay. This
is used to isolate coin selection issues from general transaction performance.
* Anonymous identities: the flows can turn anonymous identities on. This means that a new private/public key pair will be
generated for each transaction, allowing you to measure the resulting overhead.

To test the throughput a single node can achieve, this flow is run against a single node from all JMeter servers. In order
to measure network throughput, it can also be run against all nodes from their respective JMeter server.

#### Advanced Flows

The `CashIssueFlow`, `CashIssueAndPaymentFlow`, and `CashIssueAndPaymentNoSelection` flows create a somewhat realistic load but still have a very uniform, artificial usage pattern of resources.
Therefore, more advanced test flows/test plans have been developed that allow to issue a large amount of cash once and
then start to break it up in smaller payments, allowing the following settings to be tweaked:


* Number of states to be transferred in one transaction
* Number of change states created per transaction (i.e. the number of output states of the transaction)
* Number of input states to a new transaction (i.e. pay a larger sums from change shards of the previous transaction).

Advanced tests also include testing - for example, connecting to the target node via float/firewall.

#### Atomic swap flows

This is a set of flows (`SwapStockForCashFlow` and `SwapSpecificStockForCashFlow`) that are part of the `settlement-perftest-cordapp` CorDapp. These flows can be used to swap assets between multiple nodes in a single atomic transaction. They can be used to exercise the performance of scenarios, where a node has to communicate with many other nodes in order to complete a transaction.
