---
descriptions: "TVU output to the console and the options for controlling logging."
date: '2024-04-03'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu-output
    parent: corda-enterprise-4-12-tvu
tags:
- tvu output
- tvu
- transaction validator utility
title: TVU output and logging
weight: 350
---

# TVU output and logging

The following section describes what the Transaction Validator Utility (TVU) outputs to the console, and the options for controlling logging.

## Console output

By default, the TVU outputs to the console a short summary of what it is doing. If the TVU is run with valid parameters, the output is the following:

```
Starting
Total Transactions: 8649
Waiting for all transactions to be processed...
```

The output is then suspended whilst the transactions are processed, until finally you see:

```
Success, All transactions processed.
Total time taken: 2001778ms
```

If a parameter is specified with an incorrect value, the TVU indicates what the problem is, for example:

```
-t,--load-tx-time: invalid date/time specified. Format should be yyyy-MM-ddThh:mm:ss.nnZ
-e,--error-directory: directory does not exist.
-e,--error-directory: directory is not writeable.
```

## Logging

The TVU generates a log file in the current working directory. As with all Corda CLI tools, the level of logging is controlled by the `--logging-level` parameter. The available levels, in order of increasing detail, are:
* `ERROR`
* `WARN`
* `INFO` (default logging level)
* `DEBUG`
* `TRACE`

For example:

```
java -jar transaction-validator.jar --logging-level DEBUG
```

## Verbose logging

The `--verbose` (short version `-v`) parameter enables verbose logging. This feature takes the messages written to the TVU log file and additionally echoes them to the console.
