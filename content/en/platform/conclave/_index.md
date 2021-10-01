---
date: '2021-04-24T00:00:00Z'
section_menu: conclave
menu:
  projects:
    name: Conclave
    identifier: homepage-conclave
    weight: 90000
project: conclave
version: 'conclave'
title: Conclave
---

# Welcome to the Conclave Platform

Conclave is a toolkit for building enclaves, small pieces of software that are protected from attack by the owner of the computer on which they run. It is the ideal solution for solving multi-party collaboration and privacy problems; however, you can also use it to secure your infrastructure against attack.

## Why Conclave?

* High-level, simple API that is much easier to use than other enclave APIs.
* Write your host app in any language that can run on a Java Virtual Machine, such as Java, Kotlin, or even JavaScript.
* Write your enclave using the GraalVM native image technology for incredibly tight memory usage, support for any GraalVM language and instant startup time. Eliminate all memory management errors that would undermine the security of your enclave, thanks to the built-in compacting generational garbage collector.
* Develop gracefully on all operating systems, not just Linux. Windows and macOS are fully supported as well.
* Full support for auditing enclaves over the internet, including remote attestation. A user can verify what the source code of the remotely running enclave is, to ensure it will behave as they expect.
* A message-oriented communication and storage system that eliminates size-based side channel attacks and integrates with the Intel SGX secure upgrade mechanisms. Roll forward through security upgrades without disrupting clients' work.
* A Gradle plugin to automate compiling, signing, and calculating the code hash of your enclave. No need to use the Intel SDK - everything needed is included.
* API designs that guide you towards SGX best practices and help you avoid security pitfalls.
* Easily deploy to Microsoft Azure by uploading your Java host app and running it as normal—no setup required.
* A powerful unit testing framework to verify the operation of your enclave and remote attestation functionality using JUnit.
* Integrate and benefit from Corda, an open source peer-to-peer network for business uses with enterprise support.
* Tutorials, guides, design assistance, and commercial support from the SGX experts at R3. Talk to developers on a dedicated Slack channel, even if you don't have a support contract.

Conclave is free for individuals and early-stage startups.

## Next steps

The Conclave product and developer documentation is still hosted on a [separate website](https://docs.conclave.net/), however the R3 Technical Writing Team and the Conclave squad are working to bring this content over to the [R3 documentation portal](https://docs.r3.com/) (this site) in the near future - keep your eyes peeled!

To familiarize yourself with the Conclave platform and start using it:

* Read the [Conclave documentation](https://docs.conclave.net/).
* Visit the [Conclave website](https://www.conclave.net/).
