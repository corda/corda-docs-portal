---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-toc-tree
tags:
- performance
- tuning
title: Performance-tuning a node
weight: 800
---


# Performance-tuning a node

Great, so we have set up a test cluster, have all the CorDapps and JMeter installed, sorted out the firewall rules, we can get a request
go through via the JMeter GUI (see [View Results in Table](practical-considerations.md#view-results-in-table) for details how to verify that), we have sorted
out an initial test plan and have run a performance test, but these throughput numbers are not quite what we would like to see there.
Time to tune the node.


## Tweaking the node settings

The main parameters that can be tweaked for a Corda Enterprise node are


* The number of flow threads (the number of flows that can be live and active in the state machine at the same time). The default
value for this is twice the number of processor cores available on the machine, capped at 30.
* The number of RPC threads (the number of calls the RPC server can handle in parallel, enqueuing requests to the state machine). The default
for this is the number of processor cores available on the machine
* The amount of heap space the node process can allocate. The default for this is 512 megabytes.

For a machine with *n* cores, this will create up to *3*n* Corda threads. On top of that, the messaging system (Artemis and Netty) will
create their own messaging handling thread infrastructure.
On a server machine with many processor cores, this can lead to over a 100 threads sharing 512 megabyte of memory - this leaves the
threads fighting for resources, and memory contention and very poor performance will be the result.

In Corda Enterprise, these properties can be controlled via the node configuration.
It is recommended to keep a diary of changes during the tweaking of any parameters, or ideally have the node configuration under version
control so it is easy to go back and check settings for previous results.


### Tweaking the memory

The first tweak should be to give the node more memory - the instructions  how to deploy a node recommend at
least 2GB of memory. Performance tests at R3 typically use 8GB of memory for one node. This depends on the available memory and
how many nodes (and other processes) are run on the same machine. There are various ways to set the heap memory of the node documented at
[Setting JVM arguments](../node/deploy/running-a-node.md#setting-jvm-args). The recommended approach for performance optimisation work is to use the JVM argument section in the node
config file as this captures the memory setting along with any other settings.

Be careful with the total amount of memory allocated to processes - if the total memory allocated to all processes on one machine exceeds
the physical RAM available in the machine, memory will be swapped out to the file system (if this is enabled) or memory allocation will
fail. Corda node processes do not react kindly to either of those events. In case of a memory allocation failure, the node will
stop and needs to be restarted. If the memory of the node process gets swapped out, expected timings and guarantees within the process can
be broken. This can lead to severe performance degradation, and flows and apps that rely on timings might fail.

In general, more memory is better for the node, so it might be a good idea to start with as much memory as can be made available without
running into the issues mentioned above, and then proceed with tweaking other parameters. Once the node is tuned, it might be worthwhile
to run a few tests checking whether the amount of memory can be reduced without affecting performance.


### Tweaking the thread count

Especially on large server machines, the default number of flow threads might be on the upper limit of what is sensible. In order to find
the optimal number, it is necessary to tweak that number via the configuration, restart the node(s), and rerun a test plan to see how the
numbers have changed. In order to keep the tests reproducible, it might be a good idea to wipe the database between tests so index sizes
and query times do not skew the test results for later runs (see [Resetting a Node](practical-considerations.md#resetting-a-node)).

Flow and RPC threads can be set explicitly using the [tuning section](../node/setup/corda-configuration-file.md#enterprise-config-tuning) of the enterprise configuration. Add the following section to your
node configuration file:

```kotlin
enterpriseConfiguration = {
    tuning = {
        rpcThreadPoolSize = 4
        flowThreadPoolSize = 8
    }
}
```

The recommended approach is to start with a low number of flow threads (e.g. 1 per gigabyte of heap memory), and increase the number of
threads over a number of runs. In tests at R3, it seems that giving a node twice the number of flow threads than RPC threads seemed a
sensible number, but that might depend on the hardware and the use case, so it is worthwhile to experiment with this ratio.


### Disk access

The node needs to write log files to disk, and has an Artemis spool directory that is used for the durable queues on the hard disk, so disk
I/O for the node’s working directory has an impact on the node performance. For optimal performance, this should be on a fast, local disk.
For the Artemis spool directory, this leads to an inherent contradiction, a trade-off for which needs to be carefully considered and tested for
a production installation: the durable queue spool directory should be
as fast as possible in order not to become a bottleneck, on the other hand this data must not get lost or the durable promise of the queue
will be broken, so it should ideally be on a redundant storage medium.


### Fine-tuning the Artemis configuration

The following configuration options control some aspects of Artemis and can affect the throughput and latency of an application:
* `p2pConfirmationWindowSize`: the size of the in-memory buffer, used by the broker to buffer completed commands before acknowledging them to the client.
* `brokerConnectionTtlCheckIntervalMs`: the interval at which acknowledgements of completed commands are to be sent in case `p2pConfirmationWindowSize` is not exhausted in time.
* `journalBufferSize`: the size of the in-memory buffer used to store messages before they are flushed to disk.
* `journalBufferTimeout`: the interval at which Artemis messages that are buffered in-memory are to be flushed to disk if the `journalBufferSize` is not exhausted in time.

As a result, you can control how frequently Artemis persists messages to disk and how frequently acknowledgements are sent back to clients. These values can affect the latency of flows, since a flow is expected to wait less on Artemis if it flushes messages to disk and sends acknowledgements more frequently. However, such configuration tweaks can also affect the throughput of flows, since flushing to disk more frequently and sending acknowledgements more frequently can result in a reduced efficiency of the utilisation of the disk and network resources. It is important that you benchmark any changes to these values in order to make sure that you have achieved the desired balance between throughput and latency.

### Fine-tuning transaction resolution

In some cases, a node might have to resolve the provenance chain of a transaction from a counterparty. The configuration option `backchainFetchBatchSize` controls how many transactions the node will send at a time when performing this resolution. This defaults to a relatively large value, but you might need to increase it further if you have extremely large chains of transactions that nodes need to resolve. Increasing this value can reduce the latency of flows, since nodes will be able to resolve a transaction chain with fewer round trips. It might also have a positive impact on throughput because this way flows will last less and nodes will be able to complete more of them. However, this might also lead to an increase in the utilisation of network bandwidth and node resources in general. As a result, the actual results will depend on your environment.

## Database optimisation

The node has a high level of interaction with its database, so the performance of the database has a large impact on the node performance.


### Use an enterprise database

The H2 database that is used by Corda by default is very handy for development, but it cannot handle the throughput that a serious
performance test will generate on any sensible hardware. It has internal locks that will throttle the throughput of the node. To test
actual performance of a Corda system, it is required to use an enterprise level database.


### Database server

The database should be running on a separate server. Corda has some rather unusual requirements for the database: as the node writes its
checkpoints to the database, but only ever reads them when a flow needs to be restarted, the amount of data written to the database can
vastly exceed the amount of data read and index look-ups performed. Checkpoints are usually written once and removed once the flow finishes.
Therefore, a standard, read-optimised database as is e.g. on offer from cloud providers does not suit the performance requirements of Corda
very well. It is recommended to run a dedicated database on a server that has fast disks, so the writing of checkpoints does not slow
the processing down.

Depending on the write performance of the database, it might be useful to have a separate database server for each node rather than having
a schema per node in the same database server.


## Node interactions

For any flow that only works within one node (e.g. Cash Issuance), the above should allow to tweak the node to be performant. Any flows
that involve connections to other nodes (e.g. to the recipient of a payment or a notary) might also be bottlenecked on the performance
of their peers, so they might need to be tweaked as well.


### Peers

How much memory and how many threads are required on a peer node depends on the app being tested. When using the `CashIssueAndPayment`
flow from the performance CorDapp, the receiving node typically only needs half the number of threads/memory compared to the issuing
node to keep up with processing, but this might also depend on the hardware. Keeping one node configuration constant and modifying a peer
configuration is a valid test that needs to be undertaken.


### Notaries

Any flows that require notarisations might be limited by the throughput of the notary.


### TLS connections

Corda uses TLS to encrypt the peer to peer connections between nodes. It can be shown that the maximal throughput that is achievable with
the JVM TLS layer can limit the node throughput for flows that need to send sufficient amount of data between peers. This is e.g. the case
for the *CashIssueAndPayment* flow in the performance test CorDapp.

Corda nodes can optionally use *boringSsl* for TLS connections - this is an OpenSsl based native SSL/TLS library maintained by Google that
allows much higher peer to peer throughput. Its use can be enabled by adding the following to the node configuration file:

```kotlin
useOpenSsl=true
```


## Varying the load

The throughput of the system also varies with the load that is created from the client side - if the incoming request rate is too low, the
system will not reach maximum throughput, if it is too high, resource contention might actually lower the throughput as well. Varying the
load to identify the number of connections at which the node gets saturated and at which point throughput might start to suffer is not
only important to get optimal performance number, but this also needs to be considered when specifying a production system that needs
to be able to handle a certain load.

The *Number of Threads* setting on a *Thread Group* in the test plan controls how many threads JMeter will run in parallel, each starting
a run and then waiting for the result. If you look at the NightlyBenchmark example test plan, you’ll notice that the same test gets
repeated with different numbers of threads, thus creating a result that reports throughput as a function of number of clients.

Increasing the number of threads too high might lead to contention on the JMeter server (e.g. on the RPC client), therefore it is also
possible to run requests from several JMeter servers. In this case, it is important that the target *host* in the testplan is an actual
machine name or IP address, not *localhost*, as the JMeter servers might run on different machines. Each JMeter server will run the specified
number of threads, so five servers with 200 Threads each would lead to 1000 runs in parallel.


## Final considerations

After optimising the node using a specific test plan, do keep in mind that this might have optimised the node for this specific load that
gets generated by JMeter. While this is probably a good starting point to configure nodes for real world production uses, it is in no way
guaranteed that the configuration is suitable.

If monitoring a node reveals that it does not perform as expected, further tweaking might be required, or the creation of a test plan that
matches the usage pattern observed with real life use and with the CorDapps that get used.
