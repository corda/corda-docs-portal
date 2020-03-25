---
aliases:
- /releases/release-V3.0/out-of-process-verification.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-0:
    identifier: corda-os-3-0-out-of-process-verification
    parent: corda-os-3-0-corda-nodes-index
    weight: 1090
tags:
- out
- of
- process
- verification
title: Out-of-process verification
---


# Out-of-process verification

A Corda node does transaction verification through `ServiceHub.transactionVerifierService`. This is by default an
`InMemoryTransactionVerifierService` which just verifies transactions in-process.

Corda may be configured to use out of process verification. Any number of verifiers may be started connecting to a node
through the node’s exposed artemis SSL port. The messaging layer takes care of load balancing.

{{< note >}}
We plan to introduce kernel level sandboxing around the out of process verifiers as an additional line of
defence in case of inner sandbox escapes.

{{< /note >}}
To configure a node to use out of process verification specify the `verifierType` option in your node.conf:

```cfg
myLegalName : "O=Bank A,L=London,C=GB"
p2pAddress : "my-corda-node:10002"
webAddress : "localhost:10003"
verifierType: "OutOfProcess"

```

[example-out-of-process-verifier-node.conf](https://github.com/corda/corda/blob/release/os/3.0/docs/source/example-code/src/main/resources/example-out-of-process-verifier-node.conf)

You can build a verifier jar using `./gradlew verifier:standaloneJar`.

And run it with `java -jar verifier/build/libs/corda-verifier.jar <PATH_TO_VERIFIER_BASE_DIR>`.

`PATH_TO_VERIFIER_BASE_DIR` should contain a `certificates` folder akin to the one in a node directory, and a
`verifier.conf` containing the following:

```cfg
nodeHostAndPort: "my-corda-node:10002"
keyStorePassword : "cordacadevpass"
trustStorePassword : "trustpass"
```

[example-verifier.conf](https://github.com/corda/corda/blob/release/os/3.0/docs/source/example-code/src/main/resources/example-verifier.conf)

