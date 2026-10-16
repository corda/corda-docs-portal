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

## Summary

* The node process itself needs about **100 MB of live heap** when idle and about **300 MB of
  non-heap memory** (class metadata, compiled code, thread stacks, buffers). Everything above
  that is heap headroom, caches that grow with the heap size, and in-flight flows.
* With the [minimal configuration](#the-minimal-configuration) a node runs in **0.5 to 0.8 GB
  of resident memory** plus about 0.1 GB for the launcher process, sustains **150 to 200 simple
  flows per second** on two cores, and fits comfortably on a **2 vCPU / 2 GB** host.
* With the **default configuration** the node starts a 4 GB heap and sizes its thread pools from the
  CPU count. On a 48-core host it used **1.1 GB idle and 2.1 GB under load**, and scaled to about
  570 flows per second with eight concurrent clients in the same test.
* Each **suspended flow** keeps its live state plus a compressed serialized copy of it in heap
  while it is in flight, plus about 12 KB of bookkeeping: measured at **14 KB for a trivial flow**
  and about **150 KB for a flow holding 64 KB of incompressible state**. 5,000 suspended small
  flows add about 90 MB.
* The database, the Corda Firewall and notaries are separate processes with their own requirements
  and are not included in any figure on this page.

## Where a node's memory goes

A Corda node is a JVM, and its resident memory is more than its heap. The table lists the parts,
typical sizes for a 4.15 node, and the settings that control them.

{{< table >}}

| Part | Typical size | Controlled by |
|---|---|---|
| Live heap, idle node | 75 to 100 MB | Fixed cost: node services, Artemis broker, Hibernate metadata, Kotlin reflection, logging buffers |
| Heap committed | grows toward `-Xmx` under load | `-Xmx`, `-Xms`; with Serial GC also `-XX:MaxHeapFreeRatio` / `-XX:MinHeapFreeRatio` |
| In-flight flows | per suspended flow: its live object graph, plus the Snappy-compressed serialized copy that is also written to `node_checkpoint_blobs`, plus about 12 KB | your flows; [pausing](#suspended-flows-and-restarts) releases it |
| Caches scaled from the heap | `transactionCacheSizeMegaBytes` is 8 MB + 5% of the heap above 300 MB (about 200 MB at 4 GB); the attachment content cache is 10 MB + the same increment; about 25 other caches get `transactionCacheSizeBytes / 8 KB` entries each | `transactionCacheSizeMegaBytes`, `attachmentContentCacheSizeMegaBytes` |
| Class metadata (metaspace) | 110 to 125 MB for the node; more per CorDapp | `-XX:MaxMetaspaceSize` as a cap; the CorDapps you install |
| Compiled code (code cache) | 40 to 90 MB | `-XX:ReservedCodeCacheSize`; JIT activity, which grows with the number of cores |
| Thread stacks | about 70 threads idle, 1 MB reserved each (only the touched part is resident) | the pools below; `-Xss` |
| Thread pools | flow threads: 2 × cores, capped at 30; RPC threads: cores; external operation threads: cores, capped at 10; Artemis acceptor threads: 3 × cores, created as connections arrive; Artemis client threads: up to 8 × cores; bridge threads: 2 × cores; JIT and GC worker threads | `enterpriseConfiguration.tuning`, `flowExternalOperationThreadPoolSize`, system properties, `-XX:ActiveProcessorCount` |
| Direct memory | Netty buffer arenas (2 × cores by default, 4 MB per chunk) plus two Artemis journal buffers of about `maxMessageSize` each | `io.netty.allocator.numDirectArenas`, `-XX:MaxDirectMemorySize` |
| Memory freed by the JVM but kept by glibc | 100 MB to several hundred MB on Linux | `MALLOC_ARENA_MAX` in the environment |
| Capsule launcher | 60 to 90 MB, a second JVM that stays alive | unavoidable when starting through `corda.jar` |
| External verifier | a third JVM, started only when transactions with legacy (pre-4.12) contracts are verified; it takes a quarter of the host's RAM as heap unless configured | `custom.externalVerifierJvmArgs` |

{{< /table >}}

Two consequences follow. First, lowering `-Xmx` alone does not shrink a node much: the idle node
needs only about 100 MB of live heap, so the non-heap parts dominate and those are governed by the
CPU count and by the settings in the next section. Second, raising `-Xmx` costs more than heap:
the cache bounds, the Netty heap arenas and the Artemis broker's memory limit all scale with it.

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

// Must be greater than flowThreadPoolSize + rpcThreadPoolSize + 2.
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
[Thread pools and the CPU count](#thread-pools-and-the-cpu-count).

### Why each setting

* **`transactionCacheSizeMegaBytes` and `attachmentContentCacheSizeMegaBytes`**: both default to
  a base value plus 5% of the heap above 300 MB, about 19 MB each on a 512 MB heap and about
  200 MB each on a 4 GB heap, and the transaction cache size also sizes about 25 other caches and
  the embedded Artemis broker's memory limit. 8 MB keeps the caches useful while leaving the heap
  to flows. See
  [transactionCacheSizeMegaBytes]({{< relref "corda-configuration-fields.md#transactioncachesizemegabytes" >}}).
* **`flowThreadPoolSize`, `rpcThreadPoolSize`, `flowExternalOperationThreadPoolSize`**: the node
  derives these from the CPU count at startup unless you set them, so on a large host a small node
  would still start 30 flow threads and as many RPC threads as cores, and open a database
  connection for each. Two flow threads sustain 150 to 200 simple flows per second; more
  concurrent requests queue rather than fail. Raise them together with `maximumPoolSize` when you
  need more concurrency. See [tuning]({{< relref "corda-configuration-fields.md#tuning" >}}).
* **`dataSourceProperties.maximumPoolSize`**: the node refuses to start unless the connection pool
  is larger than the flow and RPC threads plus two. Each connection holds driver buffers.
* **`maximumMessagingBatchSize` and `p2pConfirmationWindowSize`** (optional): bound the outbound
  message queue and the broker's acknowledgement buffer; the defaults are sized for throughput.
* **Netty arenas**: the node sizes its heap arenas from the heap, but the direct arenas default to
  two per core, and each arena that has been used holds at least one 4 MB chunk. One arena of each
  kind is enough for a small node; this alone saved about 80 MB on a 10-core host.
* **Artemis and bridge thread properties**: the embedded broker's client thread pool defaults to
  8 × cores and the bridge to 2 × cores. These properties cap them; the node only creates the
  threads when they are needed, so the saving appears under load.
* **`-Xmx512m -Xms128m`**: a 512 MB heap leaves about 400 MB for suspended flows and caches
  above the idle live set. `-Xms128m` makes the heap grow on demand instead of committing the
  maximum at startup.
* **`-XX:+UseSerialGC` with the heap-free ratios**: Serial GC has no concurrent worker threads and
  no card-table and remembered-set structures; measured against G1 at the same heap it saved 40
  to 70 MB of resident memory and 44 threads on a 48-core host, with the same throughput at this
  size. The free-ratio flags let the heap shrink again after a burst. Use G1 for heaps of 1 GB and
  more or when pause times matter.
* **`-Xss512k`**: halves the stack reservation of the node's own threads. Flows run on Quasar
  fibers whose stacks live on the heap, so this does not limit flow depth.
* **`-XX:ReservedCodeCacheSize=96m`**: the minimal node used 60 to 70 MB of compiled code under
  load. Raise it if the node logs that the code cache is full.
* **`-XX:MaxDirectMemorySize=96m`**: covers the Netty arena and the Artemis journal buffers; the
  measured use was under 50 MB.
* **`-XX:MaxMetaspaceSize=256m`**: a cap, not a reservation. The node used 112 to 125 MB; every
  installed CorDapp adds its classes, so raise the cap if you install many.
* **`ForkJoinPool.common.parallelism=2`**: the JDK's common pool otherwise creates one thread per
  core on demand; 32 of them were idle on a 48-core host.
* **`externalVerifierJvmArgs`**: the external verifier is a separate JVM the node starts to verify
  transactions that use contracts built before Corda 4.12. It inherits no heap setting and takes a
  quarter of the host's RAM by default. See
  [custom]({{< relref "corda-configuration-fields.md#custom" >}}).
* **`MALLOC_ARENA_MAX=2`**: glibc gives a multi-threaded process up to eight memory arenas per core
  and keeps freed memory in each. On a 48-core host this added several hundred MB of resident
  memory, about 800 MB in one measurement, that no JVM tool reports. Two arenas remove most of it;
  a trim command described [below](#verifying-how-much-memory-your-node-uses) shows how much
  remains. This applies to glibc-based systems and images; Alpine-based images use musl, which
  does not keep per-thread arenas.

The measured profile also lowered `enterpriseConfiguration.attachmentClassLoaderCacheSize`. That
setting has no effect on an idle or lightly loaded node and is not part of this recommendation;
change it only on advice from R3 support.

### What the minimal configuration can do

The figures below come from a 4.15 node with the configuration above on a host confined to two
CPUs and 2 GB, running a synthetic flow that checkpoints three times, queries the vault and records
a one-output transaction per run, with no counterparties or notary involved. See
[How these figures were measured](#how-these-figures-were-measured).

{{< table >}}

| Scenario | Result |
|---|---|
| Idle after startup | 430 MB resident (node), 73 MB live heap, 73 threads; 20 s startup |
| Load from 1, 2 and 4 concurrent clients, 2 minutes each | 72, 204 and 203 flows per second; average latency 14, 10 and 20 ms; 600 MB resident peak |
| Two-hour soak at 2 clients | 160 to 192 flows per second throughout; resident memory flat at 607 MB after the first 20 minutes; live heap 98 MB at the end |
| 1,200 suspended flows, 200 of them holding 64 KB of incompressible state | 556 MB resident; 14 KB of heap per small flow, 147 KB per flow with 64 KB of state |
| Restart with 5,000 suspended flows | 25 s instead of 20 s; 554 MB resident peak during the restore; all flows resumed |

{{< /table >}}

The same configuration on the unconfined 48-core host reached 175 flows per second at 4 clients
with 787 MB resident, the difference being the larger thread pools of the messaging layer and more
JIT activity. The limits of this configuration are concurrency, not memory: with two flow threads,
requests beyond two concurrent flows queue, and latency grows with the queue.

## Sizing for other workloads

### Estimating memory

Estimate the heap first, then add the non-heap parts:

1. **Live heap** = 100 MB + suspended flows × (live state + stored checkpoint + 12 KB) + the
   caches you configure. A suspended flow holds its state twice: as live objects and as the
   serialized checkpoint, which the node compresses with Snappy before keeping it in memory and
   writing it to the `flow_state` column of `node_checkpoint_blobs`. The stored size is therefore a
   lower bound for the live state. For incompressible state (hashes, signatures, encrypted or
   random data) the two are equal and the cost is about 2 × stored size + 12 KB; for compressible
   state (text, repeated structures) the live objects can be several times the stored size.
   Measured points: a trivial flow with a 2 KB checkpoint costs about 14 KB; a flow holding 64 KB
   of incompressible state has a 68 KB checkpoint and costs about 150 KB.

   The reliable method for your own flows is to measure: with the node otherwise idle, start N
   instances of the flow in a state where they stay suspended, force a garbage collection, and
   divide the increase in live heap by N, using the [commands below](#verifying-how-much-memory-your-node-uses).
2. **Heap size (`-Xmx`)** = live heap × 1.5 for Serial GC, × 2 for G1, so the collector has room
   to work without running continuously.
3. **Non-heap** = 250 MB + 1 MB per expected thread + direct memory + metaspace for your CorDapps.
   On hosts with many cores budget for 3 × cores Artemis acceptor threads if RPC clients reconnect
   often, or cap the processor count as described below.
4. **Host memory** = heap + non-heap + 0.1 GB launcher + 25% headroom, plus the operating system
   and page cache. Count the external verifier separately if you have legacy contracts.

For example, a node that must hold 5,000 suspended flows with small state and 2 KB checkpoints
needs about 100 + 5,000 × 16 KB ≈ 180 MB of live heap, so a 512 MB heap with Serial GC (or a
1 GB heap with G1), about 400 MB of non-heap, and a 2 GB host still suffices. A node holding 2,000 flows with
64 KB of incompressible state each needs about 400 MB of live heap and therefore a 1 GB heap and
a 3 GB host.

### Measured tiers

{{< table >}}

| Tier | Configuration | Host | Measured |
|---|---|---|---|
| Minimal | as above: 512 MB heap with Serial GC, 2 flow and 2 RPC threads | 2 vCPU, 2 GB | 0.43 GB idle, 0.6 GB peak, up to 200 flows/s |
| Minimal on a large host | as above, 48 cores available | 48 cores | 0.6 GB idle, 0.8 GB peak, 175 flows/s at 4 clients |
| Default | capsule defaults: 4 GB heap with G1 GC, 30 flow threads and 48 RPC threads on this host | 48 cores | 1.1 GB idle, 2.1 GB peak at 8 clients, 570 flows/s at 8 clients |

{{< /table >}}

The default configuration is not wrong for a large host, but it is wasteful for a small one: most
of its 2.1 GB is heap headroom, heap-scaled caches and threads that a light workload never uses.
Between the two tiers, raise the flow and RPC thread counts with the concurrency you need, raise
`maximumPoolSize` with them, and raise the heap by the rule above; switch to G1 once the heap
exceeds 1 GB.

### Thread pools and the CPU count

Several pools are sized from the number of processors the JVM reports: the flow, RPC and external
operation pools, the Artemis acceptor and client pools, the bridge's Netty threads, the JDK's common
pool, and the JIT compiler and G1 worker threads. On a host with many cores a small node therefore
carries a large thread population it never uses. Two ways to prevent that:

* Set the Corda pools explicitly, as in the minimal configuration, and cap the Artemis and bridge
  pools through the system properties shown there.
* Add `-XX:ActiveProcessorCount=N` to `jvmArgs`. The JVM then reports N processors to everything,
  so all of the pools above size themselves as on an N-core machine. In containers, a CPU limit
  has the same effect because the JVM is container-aware.

The Artemis acceptor creates one thread per RPC or peer connection until it reaches 3 × cores;
on a 48-core host that is 144 threads if clients reconnect frequently, against 6 on two cores.

### Garbage collector

Serial GC is the right choice up to a 1 GB heap: in the tests it matched G1's throughput and used
40 to 70 MB less resident memory and 44 fewer threads on a 48-core host. G1 is the JDK default
and the better choice for larger heaps and when pause times matter. Note that the node's launcher
sets only `-Xmx`; the collector is chosen by the JDK unless you set it, and the JDK picks Serial on
its own when it sees fewer than two processors or less than about 1.8 GB of memory.

### Containers

The capsule launcher adds `-Xmx512m` in development mode and `-Xmx4G` when `devMode` is
explicitly `false`, regardless of the container's memory limit. Always set the heap yourself in a
container, by either of these means:

* `custom.jvmArgs` in `node.conf`, which replaces the launcher's list entirely. This is the only
  way to use `-XX:MaxRAMPercentage`, because the launcher's `-Xmx` would otherwise take precedence.
* `-Dcapsule.jvm.args="-Xmx…"` on the launcher command line (the `JVM_ARGS` variable of the
  official image). A flag given this way overrides the same flag from `custom.jvmArgs` and leaves
  the others in place.

Size the container limit at the expected resident memory of the node plus the launcher plus 25%,
not at the heap size: the minimal configuration on this page peaked at 0.6 to 0.8 GB plus a 0.1 GB
launcher, so a limit of 1 to 1.2 GB suits its 512 MB heap. Pass `MALLOC_ARENA_MAX=2` as an
environment variable on the Ubuntu- and Amazon Linux-based images, which use glibc; the Alpine
image uses musl and does not need it. See
[Docker deployments]({{< relref "../../node-docker-deployments.md" >}}).

### Suspended flows and restarts

A flow that is waiting for a counterparty, a notary or a timer keeps both its live state and a
compressed serialized copy of it in memory until it completes. Long-waiting flows are therefore the
main reason a node's memory grows beyond the figures above. Pausing a flow releases both copies;
paused flows are restored from the database when they are retried or when the node restarts. See
[Pause and resume flows]({{< relref "../../flow-pause-and-resume.md" >}}).

Restarting a node with many suspended flows costs time and memory while the checkpoints are
restored: 5,000 small flows added five seconds to startup and a resident peak of about 550 MB on
the minimal configuration. Allow for that peak when you size the heap of a node that routinely
holds many in-flight flows, or start it with the `--pause-all-flows` option described on the same
page.

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

```bash
jcmd <node-pid> VM.native_memory summary
```

Breaks the JVM's own memory down by category (Java heap, class metadata, threads, code, GC,
direct buffers under `Other`). It requires `-XX:NativeMemoryTracking=summary` in `jvmArgs`; the
overhead is a few MB, so it is reasonable to keep on. The category totals are committed sizes, so
they do not add up exactly to `rss`: untouched committed pages are not resident, while memory
allocated by native libraries and kept by glibc is resident but not tracked.

```bash
jcmd <node-pid> System.trim_native_heap
```

Asks glibc to return freed memory to the kernel and prints the resident size before and after. The
difference is memory the node is not using; a large value points at the arena behaviour described
above.

```bash
jcmd <node-pid> Thread.print | grep -c '^"'
```

The number of threads. Compare it with the pool settings; a count that keeps growing on a host
with many cores usually means the Artemis acceptor is still creating threads for new connections.

The same information is available continuously through JMX: the `java.lang:type=Memory` and
`java.lang:type=Threading` beans and the node's own cache and flow metrics, see
[Node metrics]({{< relref "../operating/monitoring-and-logging/node-metrics.md" >}}) and
[Monitoring scenarios]({{< relref "../operating/monitoring-and-logging/monitoring-scenarios.md" >}}).

## How these figures were measured

The measurements were taken on Corda Enterprise 4.15 nodes in production mode with a PostgreSQL
database on a separate host, on Ubuntu Linux (kernel 6.8) with OpenJDK 17.0.16 on a 48-core,
96 GB host. The small-host figures confine the node service to two CPUs and a 2 GB memory limit with
cgroups and `-XX:ActiveProcessorCount=2`; they do not emulate slower disks or network. Memory was
read after two forced garbage collections, so heap figures are live data; resident figures are the
process's `VmRSS` and its high-water mark.

The workload was a synthetic flow started over RPC from one to eight concurrent clients: three
suspend-and-resume cycles, each with an indexed vault lookup and a checkpoint carrying 4 KB of
state, followed by signing, verifying and recording a one-output transaction. It exercises the
state machine, checkpoint serialization, the database, the vault, transaction verification and the
RPC and internal messaging paths. It does not exercise peer-to-peer messaging, TLS or notarisation,
so the throughput figures describe one node's own capacity rather than an end-to-end business
flow. For end-to-end performance testing with the Corda performance test suite, see
[Performance testing]({{< relref "../../performance-testing/introduction.md" >}}).
