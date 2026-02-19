---
descriptions: "Learn how to create your own TVU class."
date: '2023-12-15'
section_menu: corda-enterprise-4-13
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-testing-tvu
    parent: corda-enterprise-4-13-tvu
tags:
- pluggable tvu
- tvu
- transaction validator utility
title: Creating TVU classes
weight: 600
---

# Creating TVU classes

Apart from verification and deserialization, you may also want to perform other tasks on your transactions using the Transaction Validator Utility (TVU). To do that, you can provide your own class and run its logic on every transaction.
The following is an example of a pluggable project that logs transactions. You can use this project to test the utility and as a starting point for any project that needs to be pluggable in the TVU.

To run the project from the command-line:

1. Navigate to the enterprise base directory.
2. Create a JAR file under `samples/log-transaction/build/libs`:
    * If you are using Unix, run `./gradlew tools:transaction-validator:samples:logtransaction:build`.
    * If you are using Windows, run `gradlew tools:transaction-validator:samples:logtransaction:build`.
3. Place the JAR in the node's drivers directory (`<node-base>/drivers`).
4. Run the TVU using the `-c` CLI option specifying full class name, for example, `-c net.corda.tvu.LogTransaction`.
