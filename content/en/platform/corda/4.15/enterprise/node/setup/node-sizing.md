---
date: '2026-10-15T12:00:00Z'
menu:
  corda-enterprise-4-15:
    parent: corda-enterprise-4-15-corda-nodes-configuring
tags:
- sizing
- memory
- node
title: Node sizing and memory requirements
weight: 25
---

# Node sizing and memory requirements

This page describes how much memory and CPU a Corda Enterprise node needs, which configuration
settings determine that, what the smallest practical configuration looks like and what it can do,
how to estimate the requirements of other workloads, and how to verify how much memory a running
node actually uses.

The figures on this page were measured on Corda Enterprise 4.15 nodes running in production mode
(`devMode = false`) against a PostgreSQL database on a separate host, on Ubuntu Linux with OpenJDK 17.
The measurement method is described [at the end of this page](#how-these-figures-were-measured).
Treat the numbers as a guide: your CorDapps, flows, database and network determine the actual
requirements, and the [verification commands](#verifying-how-much-memory-your-node-uses) show what
your node needs.

{{< note >}}
The benchmark figures and the Small to X-Large sizing table in
[Performance benchmarking results]({{< relref "../../performance-testing/performance-results.md" >}})
come from Corda Enterprise 4.0-era tests on different hardware and are kept for reference only.
Use this page for sizing.
{{</ note >}}

## Terms used on this page

* **Live heap**: the part of the Java heap still in use after a full garbage collection, that is,
  the data the node actually holds. **Committed heap** is the memory the JVM has reserved from the
  operating system for the heap, whether or not it holds live data; it grows toward `-Xmx` under
  load.
* **Resident memory**: the physical memory a process occupies, as reported by `ps` (RSS). It
  includes the heap and everything outside it. **Peak** means the highest resident value observed
  during a test (the process's high-water mark); **idle** means the node after startup with no
  flows running.
* **Cores**: the number of logical processors the JVM reports. This counts hyper-threads and
  honours container CPU limits, and it is what every CPU-derived default on this page is computed
  from.
* **Suspended flow**: a flow that has checkpointed and is waiting for a message, a timer or an
  external operation. Such flows are also called in flight.
* **Flow with little state**: a flow that carries no data of its own beyond what the flow
  framework stores, so its checkpoint is about 2 KB. The test flow is one; a flow holding a
  transaction, a document or a large collection is not.
* **Launcher**: `corda.jar` is a Capsule launcher, a small JVM that unpacks the node and starts the
  node JVM as a child process, then stays alive. It is counted separately from the node.
* **Serial GC** and **G1 GC**: the two JDK garbage collectors referred to on this page. Serial GC
  (`-XX:+UseSerialGC`) is the single-threaded collector; G1 GC (`-XX:+UseG1GC`, Garbage-First) is
  the JDK's default on hosts with two or more cores and about 1.8 GB or more of memory.
* **Clients** and **flows per second**: in the measurements, a client is one thread of the load
  generator that starts the next test flow as soon as the previous one has completed; all clients
  share one RPC connection, so the figures do not include the per-connection cost of several RPC
  clients (see [How these figures were measured](#how-these-figures-were-measured)). Flows per second
  is the rate at which those flows complete. The test flow is described in
  [How these figures were measured](#how-these-figures-were-measured).

## Summary

* The node process itself needs about **100 MB of live heap** when idle. The memory outside the
  heap (class metadata, compiled code, thread stacks, buffers) depends on the configuration and the
  number of cores: about **300 MB** for the minimal configuration on two cores, 450 MB for the same
  configuration on 48 cores, and 770 MB for the default configuration on 48 cores. Everything above
  that is heap headroom, caches that grow with the heap size, and suspended flows.
* With the [minimal configuration](#the-minimal-configuration) a node runs in **0.43 to 0.6 GB
  of resident memory on two cores** (0.6 to 0.8 GB on a 48-core host) plus about 0.1 GB for the
  launcher, completes **70 test flows per second from one client and up to 200 from two or
  more** on two cores, and fits comfortably on a **2 vCPU / 2 GB** host.
* With the **default configuration** the node starts a 4 GB heap and sizes its thread pools from the
  number of cores. On a 48-core host it used **1.1 GB of resident memory idle and 2.1 GB at peak
  under load**, and scaled to about 570 test flows per second with eight concurrent clients.
* Each **suspended flow** keeps its live state plus a compressed serialized copy of it in the heap,
  plus about 12 KB of bookkeeping: measured at **14 KB for a flow with little state** and about
  **150 KB for a flow holding 64 KB of incompressible state**. 5,000 suspended flows with little
  state add about 90 MB.
* The database, the Corda Firewall and notaries are separate processes with their own requirements
  and are not included in any figure on this page.

## Where a node's memory goes

A Corda node is a JVM, and its resident memory is more than its heap. The table lists the parts,
typical sizes for a 4.15 node, and the settings that control them.

{{< table >}}

| Part | Typical size | Controlled by |
|---|---|---|
| Live heap, idle node | 75 to 100 MB | Fixed cost: node services, the embedded message broker (Apache ActiveMQ Artemis), Hibernate metadata, Kotlin reflection, logging buffers |
| Committed heap | grows toward `-Xmx` under load | `-Xmx`, `-Xms`; with Serial GC also `-XX:MaxHeapFreeRatio` / `-XX:MinHeapFreeRatio` |
| Suspended flows | per flow: its live object graph, plus the Snappy-compressed serialized copy that is also written to `node_checkpoint_blobs`, plus about 12 KB | your flows; [pausing](#suspended-flows-and-restarts) releases it |
| Caches scaled from the heap | `transactionCacheSizeMegaBytes` is 8 MB + 5% of the heap above 300 MB (about 200 MB at 4 GB); the attachment content cache is 10 MB + the same increment; about 25 other caches get `transactionCacheSizeBytes / 8 KB` entries each | `transactionCacheSizeMegaBytes`, `attachmentContentCacheSizeMegaBytes` |
| Class metadata (metaspace) | 110 to 125 MB for the node; more per CorDapp | `-XX:MaxMetaspaceSize` as a cap; the CorDapps you install |
| Compiled code (code cache) | 40 to 90 MB | `-XX:ReservedCodeCacheSize`; the just-in-time (JIT) compiler compiles more, and uses more threads, on hosts with more cores |
| Thread stacks | about 70 threads idle with the minimal configuration, 120 with the defaults on a 48-core host; 1 MB reserved each (only the touched part is resident) | the pools below; `-Xss` |
| Thread pools | flow threads: 2 × cores, capped at 30; RPC threads: cores; external operation threads: cores, capped at 10; message broker acceptor threads: 3 × cores, created as connections arrive; broker client threads: up to 8 × cores; bridge threads: 2 × cores; JIT compiler and garbage collector worker threads | `enterpriseConfiguration.tuning`, `flowExternalOperationThreadPoolSize`, system properties, `-XX:ActiveProcessorCount` |
| Direct memory (off-heap buffers) | Netty buffer pools, called arenas (2 × cores by default, each holding at least one 4 MB chunk once used), plus messages up to `maxMessageSize` in transit | `io.netty.allocator.numDirectArenas`, `-XX:MaxDirectMemorySize` |
| Native memory of the message broker's journal | two buffers of about `maxMessageSize` each, allocated by the native asynchronous I/O library on Linux and not counted against `-XX:MaxDirectMemorySize` | network parameter `maxMessageSize` |
| Memory freed by the JVM but kept by the C library (glibc) | 40 MB to several hundred MB on Linux; a trim returned about 320 MB on an unconfigured 48-core node, 85 to 136 MB with `MALLOC_ARENA_MAX=2` on 48 cores, and about 40 MB with the cap on two CPUs | `MALLOC_ARENA_MAX` in the environment |
| Launcher | 60 to 90 MB, a second JVM that stays alive | unavoidable when starting through `corda.jar` |
| External verifier | a third JVM, started only when transactions with legacy (pre-4.12) contracts are verified; it takes a quarter of the host's RAM as heap unless configured | `custom.externalVerifierJvmArgs` |

{{< /table >}}

Two consequences follow. First, lowering `-Xmx` alone does not shrink a node much: the idle node
needs only about 100 MB of live heap, so the parts outside the heap dominate, and those are
governed by the number of cores and by the settings listed under
[The minimal configuration](#the-minimal-configuration). Second, raising `-Xmx`
costs more than heap: the cache bounds, the Netty heap buffer pools and the message broker's
memory limit all scale with it.

## The minimal configuration

### Host

{{< table >}}

| Resource | Minimum | Notes |
|---|---|---|
| CPU | 2 vCPU | The node starts in about 20 s on two cores and its two flow threads can each use a core. Fewer cores were not tested; startup and JIT warm-up would be slower, and the flow and RPC threads would compete with the messaging threads. |
| Memory | 2 GB | Node 0.6 to 0.8 GB resident, launcher 0.1 GB, the rest for the operating system, page cache for the Artemis journal and logs, and headroom for suspended flows. |
| Disk | several GB, local and fast | Artemis journal, logs, heap dumps on failure. |
| Database | separate | See [Host prerequisites and database requirements]({{< relref "host-prereq.md" >}}). H2 is for development only. |

{{< /table >}}

### `node.conf`

Add the following to your node configuration. Every setting is explained below the block; settings
marked optional have a small effect and can be omitted.

```kotlin
// Caches. The transaction cache size also sets the bounds of about 25 other caches
// and the embedded Artemis broker's memory limit (which has a floor of 10 x maxMessageSize).
transactionCacheSizeMegaBytes = 8
attachmentContentCacheSizeMegaBytes = 8
flowExternalOperationThreadPoolSize = 1

enterpriseConfiguration {
    tuning {
        flowThreadPoolSize = 2            // default: 2 x cores, capped at 30
        rpcThreadPoolSize = 2             // default: number of cores
        maximumMessagingBatchSize = 64    // optional, default 256
        p2pConfirmationWindowSize = 262144 // optional, default 1048576
    }
}

// Must be greater than the sum of all flow thread pools + rpcThreadPoolSize + 2.
dataSourceProperties.maximumPoolSize = 7

systemProperties {
    "io.netty.allocator.numDirectArenas" = 1
    "io.netty.allocator.numHeapArenas" = 1
    "activemq.artemis.client.global.thread.pool.max.size" = 8
    "activemq.artemis.client.global.scheduled.thread.pool.core.size" = 2
    "net.corda.nodeapi.amqpbridgemanager.NumBridgeThreads" = 1
    "net.corda.nodeapi.amqpclient.NumClientThread" = 1
}

custom {
    // Replaces the launcher's default JVM arguments (-Xmx4G in production mode).
    jvmArgs = [
        "-Xmx512m", "-Xms128m",
        "-XX:+UseSerialGC",
        "-XX:MaxHeapFreeRatio=40", "-XX:MinHeapFreeRatio=10", "-XX:-ShrinkHeapInSteps",
        "-Xss512k",
        "-XX:ReservedCodeCacheSize=96m",
        "-XX:MaxDirectMemorySize=96m",
        "-XX:MaxMetaspaceSize=256m",
        "-Djava.util.concurrent.ForkJoinPool.common.parallelism=2",
        "-XX:NativeMemoryTracking=summary",
        "-XX:+HeapDumpOnOutOfMemoryError", "-XX:+CrashOnOutOfMemoryError"
    ]
    // The external verifier would otherwise take a quarter of the host's RAM.
    externalVerifierJvmArgs = ["-Xmx256m", "-XX:+UseSerialGC"]
}
```

And in the environment of the node process, for example in the `[Service]` section of its systemd
unit or with `-e` on `docker run`:

```none
MALLOC_ARENA_MAX=2
```

On hosts with many cores, also add `-XX:ActiveProcessorCount=2` to `jvmArgs`; see
[Thread pools and the number of cores](#thread-pools-and-the-number-of-cores).

The settings were measured together as one profile, with a workload that uses no peer-to-peer
messaging. The effect of the bridge and client thread properties, `maximumMessagingBatchSize` and
`p2pConfirmationWindowSize` on a node that talks to real peers is therefore unmeasured; they
reduce buffering and thread counts by construction, but test them with your own traffic before
relying on them.

### Why each setting

* **`transactionCacheSizeMegaBytes` and `attachmentContentCacheSizeMegaBytes`**: both default to
  a base value plus 5% of the heap above 300 MB, about 19 MB each on a 512 MB heap and about
  200 MB each on a 4 GB heap, and the transaction cache size also sizes about 25 other caches and
  the embedded Artemis broker's memory limit. 8 MB keeps the caches useful while leaving the heap
  to flows. It also bounds those other caches at about 1,000 entries each, including the identity
  and network map caches, so a node on a network with well over a thousand parties, or one using
  many confidential identities, will read from the database more often; raise it in that case. See
  [transactionCacheSizeMegaBytes]({{< relref "corda-configuration-fields.md#transactioncachesizemegabytes" >}}).
* **`flowThreadPoolSize`, `rpcThreadPoolSize`, `flowExternalOperationThreadPoolSize`**: the node
  derives these from the number of cores at startup unless you set them, so on a large host a small node
  would still start 30 flow threads and as many RPC threads as cores, and open a database
  connection for each. Two flow threads sustain 150 to 200 simple flows per second; more
  concurrent requests queue rather than fail. Raise them together with `maximumPoolSize` when you
  need more concurrency. See [tuning]({{< relref "corda-configuration-fields.md#tuning" >}}).
* **`dataSourceProperties.maximumPoolSize`**: the node refuses to start unless the connection pool
  is larger than all flow threads (the default pool plus any `additionalFlowThreadPools`) and the
  RPC threads plus two. Each connection holds driver buffers.
* **`maximumMessagingBatchSize` and `p2pConfirmationWindowSize`** (optional): bound the outbound
  message queue and the broker's acknowledgement buffer; the defaults are sized for throughput.
* **Netty buffer pools** (`io.netty.allocator.*`): Netty, the network library under the message
  broker and the RPC server, pools its buffers in arenas, on the heap and off it. The node sizes
  the heap arenas from the heap, but the off-heap (direct) arenas default to two per core, and each
  arena that has been used holds at least one 4 MB chunk. One arena of each kind is enough for a
  small node. In a development-mode test on a 10-core machine this, together with the other
  settings of the profile, cut off-heap buffers from 125 MB to 47 MB; on the Linux node the
  measured off-heap use was 140 to 190 MB with the defaults and 16 to 42 MB with this profile.
* **Message broker and bridge thread properties**: the embedded broker's client thread pool
  defaults to 8 × cores and the bridge (the component that delivers peer-to-peer messages) to
  2 × cores. These properties cap them; the node only creates the threads when they are needed,
  so the saving appears under load.
* **`-Xmx512m -Xms128m`**: a 512 MB heap leaves about 400 MB for suspended flows and caches
  above the idle live set. `-Xms128m` makes the heap grow on demand instead of committing the
  maximum at startup.
* **`-XX:+UseSerialGC` with the heap-free ratios**: Serial GC runs no concurrent worker threads
  and keeps far less bookkeeping memory than G1 GC; measured against G1 GC at the same heap size
  it saved 40 to 70 MB of resident memory and 44 threads on a 48-core host, with the same
  throughput at this size. That comparison was made at 512 MB only; the free-ratio flags let the
  heap shrink again after a burst. Use G1 GC for heaps of 1 GB and more or when pause times
  matter.
* **`-Xss512k`**: halves the stack reservation of the node's own threads, including the flow
  worker threads. Flow code runs on those threads' native stacks (only the frames saved at a
  checkpoint live on the heap), so deeply recursive flow code or very deep object graphs during
  checkpoint serialization can hit a `StackOverflowError` sooner; remove the flag if one appears.
* **`-XX:ReservedCodeCacheSize=96m`**: the minimal node used 60 to 70 MB of compiled code under
  the test load; the default configuration, without the cap, used about 85 MB on 48 cores. Real
  CorDapps and the peer-to-peer and TLS paths compile more, and a full code cache stops further
  compilation with only a log line. Raise it if the node logs that the code cache is full.
* **`-XX:MaxDirectMemorySize=96m`**: caps Netty's off-heap buffers; the measured use was under
  50 MB. Messages are buffered off-heap up to the network's `maxMessageSize` (10 MB by default),
  so raise the cap together with a larger `maxMessageSize`. The message broker's journal buffers
  are native allocations that this flag does not cover.
* **`-XX:MaxMetaspaceSize=256m`**: a cap, not a reservation. The node used 112 to 125 MB; every
  installed CorDapp adds its classes, and so does every contract version verified from
  attachments, so raise the cap if you install many CorDapps or verify many versions. Reaching the
  cap stops the node, because of `-XX:+CrashOnOutOfMemoryError`.
* **`ForkJoinPool.common.parallelism=2`**: the JDK's common pool otherwise creates up to one thread
  per core on demand; 32 of them were idle in one reading of a 48-core host running the
  performance-test configuration.
* **`externalVerifierJvmArgs`**: the external verifier is a separate JVM the node starts to verify
  transactions that use contracts built before Corda 4.12. It inherits no heap setting and takes a
  quarter of the host's RAM by default. See
  [custom]({{< relref "corda-configuration-fields.md#custom" >}}).
* **`MALLOC_ARENA_MAX=2`**: the GNU C library (glibc), which the JVM uses for native memory
  allocation, gives a multi-threaded process up to eight allocation arenas per core and keeps
  freed memory in each. No JVM tool reports it. On the 48-core host a trim returned about 320 MB
  from a node with the default configuration and no arena cap, 85 to 136 MB from nodes with the
  cap (different configurations, so not a controlled comparison), and about 40 MB from the node
  confined to two CPUs with the cap; a trim command described
  [below](#verifying-how-much-memory-your-node-uses) shows how much your node holds. The cap
  applies to glibc only; `-XX:ActiveProcessorCount` does not change the arena count. This
  applies to glibc-based systems and images; Alpine-based images use musl, which does not keep
  per-thread arenas.

The measured profile also lowered `enterpriseConfiguration.attachmentClassLoaderCacheSize`. That
setting had no measurable effect in these tests and is not part of this recommendation; change it
only on advice from R3 support. Every measured profile also had `-XX:NativeMemoryTracking=summary`
on, which costs about 12 MB; it is kept in the recommendation because it is what the verification
commands below rely on.

### What the minimal configuration can do

The figures below come from a 4.15 node with the configuration above on a host confined to two
CPUs and 2 GB, running the test flow described in
[How these figures were measured](#how-these-figures-were-measured): it checkpoints three times,
queries the vault and records a one-output transaction per run, with no counterparties or notary
involved. Startup time is measured from the service start to the node's "started up and
registered" log line.

{{< table >}}

| Scenario | Result |
|---|---|
| Idle after startup | 430 MB resident (node only), 73 MB live heap, 73 threads; 20 s startup |
| Load from 1, 2 and 4 concurrent clients, 2 minutes each | 72, 204 and 203 flows per second; average latency 14, 10 and 20 ms; 600 MB peak resident |
| Two hours of continuous load from 2 clients | 160 to 217 flows per second (192 in the last run); resident memory 600 to 607 MB after the first 20 minutes; live heap 98 MB at the end |
| 1,200 suspended flows, 200 of them holding 64 KB of incompressible state | 556 MB resident; 28 KB of heap per flow for the first 500 (one-off costs included), 14 KB per further flow with little state, 147 KB per flow with 64 KB of state |
| Restart with 5,000 suspended flows | startup 25 s instead of 20 s; 554 MB peak resident during the restore, below the 657 MB before the restart; all 5,000 flows restored |

{{< /table >}}

Each scenario was run once; the five runs of the same configuration on the 48-core host peaked
between 727 and 788 MB, which gives an idea of the run-to-run spread. The same configuration on
that host reached 175 flows per second at 4 clients with 787 MB resident; the confined node was
faster, which is not explained by the data (candidates are the larger thread pools and JIT
activity on 48 cores, and CPU pinning). The limits of this configuration are concurrency, not
memory: with two flow threads, requests beyond two concurrent flows queue, and latency grows with
the queue.

## Sizing for other workloads

### Estimating memory

Estimate the heap first, then add the parts outside the heap:

1. **Live heap** = 100 MB + suspended flows × (live state + stored checkpoint + 12 KB) + the
   caches you configure. A suspended flow holds its state twice: as live objects and as the
   serialized checkpoint, which the node compresses with Snappy before keeping it in memory and
   writing it to the `flow_state` column of `node_checkpoint_blobs`. The stored size is therefore a
   lower bound for the live state. For incompressible state (hashes, signatures, encrypted or
   random data) the two are equal and the cost is about 2 × stored size + 12 KB; for compressible
   state (text, repeated structures) the live objects can be several times the stored size.
   Measured points: a flow with little state and a 2 KB checkpoint (1.4 KB of `flow_state` plus
   0.7 KB of `checkpoint_value`) costs about 14 KB; a flow holding 64 KB of incompressible state
   has a 68 KB checkpoint and costs about 150 KB.

   The reliable method for your own flows is to measure: with the node otherwise idle, start N
   instances of the flow in a state where they stay suspended, force a garbage collection, and
   divide the increase in live heap by N, using the [commands below](#verifying-how-much-memory-your-node-uses).
2. **Heap size (`-Xmx`)** = live heap × 1.5 for Serial GC, × 2 for G1 GC, so the collector has
   room to work without running continuously.
3. **Memory outside the heap** = 250 MB + 1 MB per expected thread + off-heap buffers + class
   metadata for your CorDapps. On hosts with many cores budget for 3 × cores message broker
   acceptor threads if RPC clients reconnect often, or cap the number of cores the JVM reports as
   described below.
4. **Host memory** = heap + memory outside the heap + 0.1 GB launcher + 25% headroom, plus the
   operating system and page cache. Count the external verifier separately if you have legacy
   contracts.

For example, a node that must hold 5,000 suspended flows with little state and 2 KB checkpoints
needs about 100 + 5,000 × 16 KB ≈ 180 MB of live heap, so a 512 MB heap with Serial GC (or a
1 GB heap with G1 GC), about 400 MB outside the heap, and a 2 GB host still suffices; this is
close to the measured 5,000-flow restart scenario. A node holding 2,000 flows with 64 KB of
incompressible state each would need about 400 MB of live heap and therefore a 1 GB heap and a
3 GB host; that case is extrapolated from the per-flow measurements, not measured.

### Measured tiers

{{< table >}}

| Tier | Configuration | Host | Resident memory idle / at peak | Throughput |
|---|---|---|---|---|
| Minimal | as above: 512 MB heap with Serial GC, 2 flow and 2 RPC threads | 2 vCPU, 2 GB | 0.43 GB / 0.6 GB | up to 200 flows per second |
| Minimal on a large host | as above, 48 cores available | 48 cores | 0.6 GB / 0.8 GB | 175 flows per second at 4 clients |
| Default | launcher defaults: 4 GB heap with G1 GC, 30 flow threads and 48 RPC threads on this host | 48 cores | 1.1 GB / 2.1 GB (at 8 clients) | 570 flows per second at 8 clients |

{{< /table >}}

The default configuration is not wrong for a large host, but it is wasteful for a small one: most
of its 2.1 GB is heap headroom, heap-scaled caches and threads that a light workload never uses.
Between the two tiers, raise the flow and RPC thread counts with the concurrency you need, raise
`maximumPoolSize` with them, and raise the heap by the rule above; switch to G1 GC once the heap
exceeds 1 GB (the collectors were compared at 512 MB only, so this threshold is a judgement, not
a measurement).

### Thread pools and the number of cores

Several pools are sized from the number of cores the JVM reports: the flow, RPC and external
operation pools, the message broker's acceptor and client pools, the bridge's network threads, the
JDK's common pool, and the JIT compiler and G1 GC worker threads. On a host with many cores a small
node therefore carries a large thread population it never uses. Two ways to prevent that:

* Set the Corda pools explicitly, as in the minimal configuration, and cap the broker and bridge
  pools through the system properties shown there.
* Add `-XX:ActiveProcessorCount=N` to `jvmArgs`. The JVM then reports N cores to everything
  inside it, so all of the pools above size themselves as on an N-core machine; it does not affect
  the C library's allocation arenas, so `MALLOC_ARENA_MAX` is still needed. In containers, a CPU
  limit (not merely a request) has the same effect because the JVM is container-aware.

The broker's acceptor creates one thread per RPC or peer connection until it reaches 3 × cores;
on a 48-core host that is 144 threads if clients reconnect frequently, against 6 on two cores.
Each open RPC connection also holds a broker session pair, a reply queue and network buffers on
the node; the measurements used a single connection, so allow a few MB for each additional RPC
client your deployment keeps connected.

### Garbage collector

Serial GC is the right choice for small heaps: in a comparison at 512 MB with two flow threads
it matched G1 GC's throughput and used 40 to 70 MB less resident memory and 44 fewer threads on a
48-core host. Pause times were not measured, and larger heaps were not compared, so the 1 GB
boundary used on this page is a judgement. G1 GC is the JDK default and the better choice for
larger heaps and when pause times matter. Note that the node's
launcher sets only `-Xmx`; the collector is chosen by the JDK unless you set it, and the JDK picks
Serial GC on its own when it sees fewer than two cores or less than about 1.8 GB of memory.

### Containers

The launcher adds `-Xmx512m`, or `-Xmx4G` when `node.conf` contains `devMode = false`
explicitly, regardless of the container's memory limit. A node without a `devMode` line runs in
production mode on Linux but keeps the 512 MB heap, because the launcher only looks at the
configuration file. Always set the heap yourself in a container, by either of these means:

* `custom.jvmArgs` in `node.conf`, which replaces the launcher's list entirely. This is the only
  way to use `-XX:MaxRAMPercentage`, because the launcher's `-Xmx` would otherwise take precedence.
* `-Dcapsule.jvm.args="-Xmx…"` on the launcher command line (the `JVM_ARGS` variable of the
  official image). A flag given this way overrides the same flag from `custom.jvmArgs` and leaves
  the others in place.

Size the container limit at the expected resident memory of the node plus the launcher plus
headroom, not at the heap size. The minimal configuration peaked at 0.6 to 0.8 GB plus a 0.1 GB
launcher, but the container limit also has to cover the page cache of the message broker's journal
and the logs, which cgroups charge to the container, the external verifier if it ever starts, and
disk for a heap dump on failure, so start at 1.5 GB for a 512 MB heap; the tests ran with a 2 GB
limit and lower limits were not tried. Pass `MALLOC_ARENA_MAX=2` as an environment variable on
the Ubuntu- and Amazon Linux-based images, which use glibc; the Alpine image uses musl, which
manages its memory differently and was not measured. The image's start script warns that `-Xmx`
is not recommended in containers; with an explicit limit sized as described here the warning can
be ignored. See
[Docker deployments]({{< relref "../../node-docker-deployments.md" >}}).

### Suspended flows and restarts

A flow that is waiting for a counterparty, a notary or a timer keeps both its live state and a
compressed serialized copy of it in memory until it completes. Long-waiting flows are therefore the
main reason a node's memory grows beyond the figures above. Pausing a flow releases both copies;
a paused flow is loaded from the database again only when it is retried, and with the default
`smmStartMode` it stays paused across a restart. See
[Pause and resume flows]({{< relref "../../flow-pause-and-resume.md" >}}).

Restarting a node with many suspended flows costs time while the checkpoints are restored, not
extra memory: 5,000 flows with little state added five seconds to startup, and the resident peak
during the restore (554 MB) stayed below the node's footprint with the same flows suspended before
the restart (657 MB). Starting with the `--pause-all-flows` option described on the same page
keeps the flows out of memory until retried, but note that it also enables flow draining, which
has to be switched off again by hand.

## Verifying how much memory your node uses

Measure the node JVM, not the launcher. On a host where the node runs as a service:

```bash
jps -l
```

The node is the process whose main class is `net.corda.node.Corda`; `corda.jar` is the launcher,
and `net.corda.verifier.Main` is the external verifier if it is running.

```bash
ps -o pid=,rss=,vsz=,nlwp= -p <node-pid>
```

`rss` is the resident memory in kB and includes the heap, metaspace, thread stacks and buffers.
It is the number to compare with the figures on this page and with a container limit. On Linux,
`grep -E 'VmRSS|VmHWM|Threads' /proc/<node-pid>/status` also shows the high-water mark since
startup, which captures peaks that a single reading misses.

```bash
jcmd <node-pid> GC.run && jcmd <node-pid> GC.heap_info
```

`used` after the forced collection is the live data, the floor of what the node needs; `total` is
what the JVM has committed and grows toward `-Xmx` under load even when live data stays flat.
`GC.run` forces a full, stop-the-world collection, which pauses a node with a multi-gigabyte heap
for seconds; run it outside busy periods. All `jcmd` commands must run as the node's operating
system user, or as root.

```bash
jcmd <node-pid> VM.native_memory summary
```

Native Memory Tracking breaks the JVM's own memory down by category (Java heap, class metadata,
threads, compiled code, garbage collector, off-heap buffers under `Other`). It requires
`-XX:NativeMemoryTracking=summary` in `jvmArgs`; the overhead is a few MB, so it is reasonable to
keep on. The category totals are committed sizes, so they do not add up exactly to `rss`:
untouched committed pages are not resident, while memory allocated by native libraries and kept by
the C library is resident but not tracked.

```bash
jcmd <node-pid> System.trim_native_heap
```

Asks the C library to return freed memory to the kernel and prints the resident size before and
after. The difference is memory the node is not using; a large value points at the allocation
arena behaviour described above. The command needs JDK 17.0.9 or later and a glibc-based system.

```bash
jcmd <node-pid> Thread.print | grep -c '^"'
```

The number of threads. Compare it with the pool settings; a count that keeps growing on a host
with many cores usually means the message broker's acceptor is still creating threads for new
connections.

The same information is available continuously through JMX: the `java.lang:type=Memory` and
`java.lang:type=Threading` beans and the node's own cache and flow metrics, see
[Node metrics]({{< relref "../operating/monitoring-and-logging/node-metrics.md" >}}) and
[Monitoring scenarios]({{< relref "../operating/monitoring-and-logging/monitoring-scenarios.md" >}}).

## How these figures were measured

The measurements were taken on Corda Enterprise 4.15 nodes in production mode with a PostgreSQL
database on a separate host, on Ubuntu Linux (kernel 6.8) with OpenJDK 17.0.16 on a 48-core,
96 GB host. The node was a member of a real network with a network map, had the performance-test
CorDapps installed, and ran with `useOpenSsl = true` and a Jolokia JMX port open, so the class
and metaspace figures include those CorDapps and the native TLS library's own allocations are
outside what Native Memory Tracking sees. The small-host figures confine the node service to two
CPUs and a 2 GB memory limit with Linux control groups (cgroups) and `-XX:ActiveProcessorCount=2`;
they do not emulate slower disks or network, and the two CPUs were pinned on a 48-processor host,
which may give more than a cloud VM's two hyper-threads. Each scenario was run once. The load
generator ran on the same host over the loopback interface, outside the cgroup, and each client
count ran for 120 seconds including JIT warm-up. All clients shared one RPC connection. That did
not limit throughput (the same single connection carried the default configuration to 566 flows
per second, and the minimal configuration's ceiling is its two flow threads), but it means the
memory figures contain one connection's broker session, reply queue, buffers and acceptor thread
rather than one set per RPC client. Heap figures were read after two forced garbage
collections, so they are live data;
resident figures are the process's `VmRSS` and its high-water mark; startup time runs from the
service start to the node's "started up and registered" log line.

The workload was a synthetic test flow started over RPC from one to eight concurrent clients, each
client starting the next flow as soon as the previous one completed over a shared RPC
connection. Each flow runs three suspend-and-resume cycles, each with an indexed vault lookup
for a state reference that does not exist (so no state is deserialized) and a checkpoint carrying
4 KB of random bytes, followed by signing, verifying and recording a one-output transaction. It exercises the
state machine, checkpoint serialization, the database, the vault, transaction verification and the
RPC and internal messaging paths. It does not exercise peer-to-peer messaging, TLS or notarisation,
so the throughput figures describe one node's own capacity rather than an end-to-end business
flow. For end-to-end performance testing with the Corda performance test suite, see
[Performance testing]({{< relref "../../performance-testing/introduction.md" >}}).
