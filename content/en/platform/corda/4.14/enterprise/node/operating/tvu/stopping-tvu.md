---
description: "Learn how to stop TVU in a correct way."
date: '2023-12-15'
section_menu: corda-enterprise-4-13
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-stopping-tvu
    parent: corda-enterprise-4-13-tvu
tags:
- stopping tvu
- tvu
- transaction validator utility
title: Stopping TVU
weight: 400
---

# Stopping TVU

The Transaction Validator Utility (TVU) writes its runtime progress and registers transaction processing errors to the underlying resources. Once the TVU has processed all the transactions, it terminates automatically. However, if needed, you can terminate it mid-flow by sending either `SIGINT` or `SIGTERM` to the TVU's Java process. `SIGINT` can be sent using `Ctrl+C` in the shell that is running the process.

Otherwise, signals can be sent using the Linux `kill` command, specifying the signal and the process ID (`pid`):

* `kill -s SIGINT -p <pid>`
* `kill -s SIGTERM -p <pid>`

The use of the `SIGKILL` signal is discouraged as it terminates the utility immediately, and the progress and errors will not be reliably captured in the TVU's output files.

