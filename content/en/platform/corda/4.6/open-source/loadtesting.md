---
aliases:
- /head/loadtesting.html
- /HEAD/loadtesting.html
- /loadtesting.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-loadtesting
    parent: corda-os-4-6-operations
    weight: 380
tags:
- loadtesting
title: Load testing
---


# Load testing

This section explains how to apply random load to nodes to stress test them. It also allows the specification of disruptions that strain different resources, allowing us to inspect the nodes’ behaviour under extreme conditions.

The load-testing framework is incomplete and is not part of CI currently, but the basic pieces are there.


## Configuration of the load testing cluster

The load-testing framework currently assumes the following about the node cluster:


* The nodes are managed as a systemd service
* The node directories are the same across the cluster
* The messaging ports are the same across the cluster
* The executing identity of the load-test has SSH access to all machines
* There is a single network map service node
* There is a single notary node
* Some disruptions also assume other tools (like openssl) to be present

Note that these points could and should be relaxed as needed.

The load test Main expects a single command line argument that points to a configuration file specifying the cluster hosts and optional overrides for the default configuration:

```none
# nodeHosts = ["host1", "host2"]
# sshUser = "someusername", by default it uses the System property "user.name"
# executionFrequency = <number of execution per second> , optional, defaulted to 20 flow execution per second.
# generateCount = <number of generated command> , optional, defaulted to 10000.
# parallelism = <unmber of thread used to execte the commands>, optional, defaulted to [ForkJoinPool] default parallelism.
localCertificatesBaseDirectory = "build/load-test/certificates"
localTunnelStartingPort = 10000
remoteNodeDirectory = "/opt/corda"
rpcPort = 10003
remoteSystemdServiceName = "corda"
rpcUser = {username = corda, password = not_blockchain, permissions = ["ALL"]}

```

[loadtest-reference.conf](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/resources/loadtest-reference.conf)


## Running the load tests

In order to run the loadtests you need to have an active SSH-agent running with a single identity added that has SSH access to the loadtest cluster.

You can use either IntelliJ or the gradle command line to start the tests.

To use gradle with configuration file: `./gradlew tools:loadtest:run -Ploadtest-config=PATH_TO_LOADTEST_CONF`

To use gradle with system properties: `./gradlew tools:loadtest:run -Dloadtest.mode=LOAD_TEST -Dloadtest.nodeHosts.0=node0.myhost.com`

{{< note >}}
You can provide or override any configuration using the system properties, all properties will need to be prefixed with `loadtest.`.

{{< /note >}}
To use IntelliJ simply run Main.kt with the config path supplied as an argument or system properties as vm options.


## Configuration of individual load tests

The load testing configurations are not set-in-stone and are meant to be played with to see how the nodes react.

There are a couple of top-level knobs to tweak test behaviour:

```kotlin
    /**
     * @param parallelism Number of concurrent threads to use to run commands. Note that the actual parallelism may be
     *     further limited by the batches that [generate] returns.
     * @param generateCount Number of total commands to generate. Note that the actual number of generated commands may
     *     exceed this, it is used just for cutoff.
     * @param clearDatabaseBeforeRun Indicates whether the node databases should be cleared before running the test. May
     *     significantly slow down testing as this requires bringing the nodes down and up again.
     * @param gatherFrequency Indicates after how many commands we should gather the remote states.
     * @param disruptionPatterns A list of disruption-lists. The test will be run for each such list, and the test will
     *     be interleaved with the specified disruptions.
     */
    data class RunParameters(
            val parallelism: Int,
            val generateCount: Int,
            val clearDatabaseBeforeRun: Boolean,
            val executionFrequency: Int?,
            val gatherFrequency: Int,
            val disruptionPatterns: List<List<DisruptionSpec>>
    )

```

[LoadTest.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/LoadTest.kt)

The one thing of note is `disruptionPatterns`, which may be used to specify ways of disrupting the normal running of the load tests.

```kotlin
data class Disruption(
        val name: String,
        val disrupt: (NodeConnection, SplittableRandom) -> Unit
)

data class DisruptionSpec(
        val nodeFilter: (NodeConnection) -> Boolean,
        val disruption: Disruption,
        val noDisruptionWindowMs: LongRange
)

```

[Disruption.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/Disruption.kt)

Disruptions run concurrently in loops on randomly chosen nodes filtered by `nodeFilter` at somewhat random intervals.

As an example take `strainCpu` which overutilises the processor:

```kotlin
fun strainCpu(parallelism: Int, durationSeconds: Int) = Disruption("Put strain on cpu") { connection, _ ->
    val shell = "for c in {1..$parallelism} ; do openssl enc -aes-128-cbc -in /dev/urandom -pass pass: -e > /dev/null & done && JOBS=\$(jobs -p) && (sleep $durationSeconds && kill \$JOBS) & wait"
    connection.runShellCommandGetOutput(shell).getResultOrThrow()
}

```

[Disruption.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/Disruption.kt)

We can use this by specifying a `DisruptionSpec` in the load test’s `RunParameters`:

```kotlin
      DisruptionSpec(
              disruption = strainCpu(parallelism = 4, durationSeconds = 10),
              nodeFilter = { true },
              noDisruptionWindowMs = 5000L..10000L
      )

```

[Main.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/Main.kt)

This means every 5-10 seconds at least one randomly chosen nodes’ cores will be spinning 100% for 10 seconds.


## How to write a load test

A load test is basically defined by a random datastructure generator that specifies a unit of work a node should perform, a function that performs this work, and a function that predicts what state the node should end up in by doing so:

```kotlin
data class LoadTest<T, S>(
        val testName: String,
        val generate: Nodes.(S, Int) -> Generator<List<T>>,
        val interpret: (S, T) -> S,
        val execute: Nodes.(T) -> Unit,
        val gatherRemoteState: Nodes.(S?) -> S,
        val isConsistent: (S) -> Boolean = { true }
) {

```

[LoadTest.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/LoadTest.kt)

`LoadTest` is parameterised over `T`, the unit of work, and `S`, the state type that aims to track remote node states. As an example let’s look at the Self Issue test. This test simply creates Cash Issues from nodes to themselves, and then checks the vault to see if the numbers add up:

```kotlin
data class SelfIssueCommand(
        val request: IssueAndPaymentRequest,
        val node: NodeConnection
)

data class SelfIssueState(
        val vaultsSelfIssued: Map<AbstractParty, Long>
) {
    fun copyVaults(): HashMap<AbstractParty, Long> {
        return HashMap(vaultsSelfIssued)
    }
}

val selfIssueTest = LoadTest<SelfIssueCommand, SelfIssueState>(

```

[SelfIssueTest.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/tests/SelfIssueTest.kt)

The unit of work `SelfIssueCommand` simply holds an Issue and a handle to a node where the issue should be submitted. The `generate` method should provide a generator for these.

The state `SelfIssueState` then holds a map from node identities to a Long that describes the sum quantity of the generated issues (we fixed the currency to be USD).

The invariant we want to hold then simply is: The sum of submitted Issues should be the sum of the quantities in the vaults.

The `interpret` function should take a `SelfIssueCommand` and update `SelfIssueState` to reflect the change we’re expecting in the remote nodes. In our case this will simply be adding the issued amount to the corresponding node’s Long.

The `execute` function should perform the action on the cluster. In our case it will simply take the node handle and submit an RPC request for the Issue.

The `gatherRemoteState` function should check the actual remote nodes’ states and see whether they conflict with our local predictions (and should throw if they do). This function deserves its own paragraph.

```kotlin
        val gatherRemoteState: Nodes.(S?) -> S,

```

[LoadTest.kt](https://github.com/corda/corda/blob/release/os/4.6/tools/loadtest/src/main/kotlin/net/corda/loadtest/LoadTest.kt)

`gatherRemoteState` gets as input handles to all the nodes, and the current predicted state, or null if this is the initial gathering.

The reason it gets the previous state boils down to allowing non-deterministic predictions about the nodes’ remote states. Say some piece of work triggers an asynchronous notification of a node. We need to account both for the case when the node hasn’t received the notification and for the case when it has. In these cases `S` should somehow represent a collection of possible states, and `gatherRemoteState` should “collapse” the collection based on the observations it makes. Of course we don’t need this for the simple case of the Self Issue test.

The last parameter `isConsistent` is used to poll for eventual consistency at the end of a load test. This is not needed for self-issuance.


## Stability Test

Stability test is one variation of the load test, instead of flooding the nodes with request, the stability test uses execution frequency limit to achieve a constant execution rate.

To run the stability test, set the load test mode to STABILITY_TEST (`mode=STABILITY_TEST` in config file or `-Dloadtest.mode=STABILITY_TEST` in system properties).

The stability test will first self issue cash using `StabilityTest.selfIssueTest` and after that it will randomly pay and exit cash using `StabilityTest.crossCashTest` for P2P testing, unlike the load test, the stability test will run without any disruption.

