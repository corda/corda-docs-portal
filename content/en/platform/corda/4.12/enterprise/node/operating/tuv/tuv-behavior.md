---
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tuv-behavior
    parent: corda-enterprise-4-12-tuv
tags:
- tuv
- transaction validator utility
title: Transaction Validator Utility behavior
weight: 100
---

# Transaction Validator Utility behavior

This section describes the steps that the TUV goes through when processing transactions present in a specified database.

1. Upon startup, the utility connects to the specified database.
2. If it is not able to connect to the database, it exits with an error message.
3. It loads the following:
  * If `-l` or `--load-tx-time` CLI option is given, it loads last known processed transaction.
  * If `-i` CLI option is given, it loads transaction ID(s) for reverification.
4. It loads transaction processing class to process transactions.
5. It starts reading transactions from the database.
6. It submits transactions to an executor which processes them in separate threads using the loaded process class.
7. It registers progress as per given CLI parameters.
8. It registers any processing-related errors.
9. It waits for all transaction processing to complete.
10. It disconnects cleanly from the database, shuts down the executor when all transactions are verified and writes progress and errors to underlying resources.
11. It exits upon completion or can be stopped.
