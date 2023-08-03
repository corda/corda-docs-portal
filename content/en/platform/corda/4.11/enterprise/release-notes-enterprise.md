---
title: Corda Enterprise Edition 4.11 release notes
date: '2023-05-08'

menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-release-notes
    parent: about-corda-landing-4-11-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.11 release notes

Corda Enterprise Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## New features and enhancements

* This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

## Fixed issues

This release includes the following fixes:

* Updated documentation for both `.startNodes()` and `.stopNodes()` of `MockNetwork` to indicate that restarting nodes is not supported.

* A fix for cache eviction has been applied where an issue resulted in an incorrect contract verification status while a database transaction was in progress during contract verification.

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* Previously, when configured to use confidential identities and the Securosys PrimusX HSM, it was possible for Corda to fail to generate a wrapped key-pair for a new confidential identity. This would cause a temporary key-pair to be leaked, consuming resource in the HSM. This issue occurred when:

  * the Securosys HSM was configured in a master-clone cluster

  * the master HSM had failed and Corda had failed-over to use the clone HSM

  * there was an attempt to create a transaction using confidential identities

  The issue is now resolved. When generating a wrapped key-pair the temporary key-pair is not persisted in the HSM and thus cannot be leaked.

  On applying this update the PrimusX JCE should be upgraded to version 2.3.4 or later.

  There is no need to upgrade the HSM firmware version for this update but it is recommended to keep the firmware up to date as a matter of course. Currently the latest firmware version if 2.8.50.

* Previously, where nodes had invoked a very large number of flows, the cache of client IDs that had not been removed were taking up significant heap space. A solution has been implemented where the space taken up has been reduced by 170 bytes per entry. For example, 1 million unremoved client IDs now take up 170,000,000 bytes less heap space than before.

* A new or restarted peer node coming online and connecting to a node for the first time can significantly slow message processing from other peers on the node to which it connects.  With this improvement, new peers coming online get a dedicated thread on the node they connect to and do not delay message processing for existing peer-to-peer connections on the receiving node.

* Improved compatibility when using the performance test suite from Apple silicon Macs.

* Previously, when loading checkpoints, the only log messages recorded were at the end of the process, recording the total number of checkpoints loaded.

  Now, the following additional logging has been added:

  * Checkpoints: Logging has been added for the two types of checkpoints - runnable and paused flows - being loaded; log messages show the number of checkpoints loaded every 30 seconds until all checkpoints have been loaded.

  * Finished flows: Log messages now show the number of finished flows.

  For example:

  ```
  [INFO ] 2023-02-03T17:00:12,767Z [main] statemachine.MultiThreadedStateMachineManager. - Loading checkPoints flows {}
  [INFO ] 2023-02-03T17:00:12,903Z [main] statemachine.MultiThreadedStateMachineManager. - Number of runnable flows: 0. Number of paused flows: 0 {}
  [INFO ] 2023-02-03T17:00:12,911Z [main] statemachine.MultiThreadedStateMachineManager. - Started loading finished flows {}
  [INFO ] 2023-02-03T17:00:28,437Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 9001 finished flows {}
  [INFO ] 2023-02-03T17:00:43,606Z [main] statemachine.MultiThreadedStateMachineManager. - Loaded 24001 finished flows {}
  [INFO ] 2023-02-03T17:00:46,650Z [main] statemachine.MultiThreadedStateMachineManager. - Number of finished flows : 27485 {}
  ```
  
* Previously, if a node was configured to use two different slots on the Luna HSM (for example using one slot for node identities and a separate slot for the confidential identities), this failed. This issue has now been resolved. 

  {{< warning >}}
  However as a result of this fix, you need to make sure the Luna client your are using is version 10.4.0 or later.
  {{</ warning >}}
  
* The default value for the node configuration value `cryptoServiceTimeout` has been increased from 1 second to 10 seconds.

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.

### Database schema changes

There are no database changes between 4.10 and 4.11.

### Third party component upgrades

The following table lists the dependency version changes between 4.10.2 and 4.11 Enterprise Editions:

| Dependency                         | Name                | Version 4.1.2 Enterprise | Version 4.11 Enterprise|
|------------------------------------|---------------------|--------------------------|------------------------|
| com.squareup.okhttp3               | OKHttp              | 3.14.2                   | 3.14.9                 |
| org.bouncycastle                   | Bouncy Castle       | 1.68                     | 1.70                   |
| io.opentelemetry                   | Open Telemetry      | -                        | 1.20.1                 |
| org.apache.commons:commons-text    | Apache Commons-Text | 1.9                      | 1.10.0                 |
| org.apache.shiro                   | Apache Shiro        | 1.9.1                    | 1.10.0                 |

## Log4j patches

Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.