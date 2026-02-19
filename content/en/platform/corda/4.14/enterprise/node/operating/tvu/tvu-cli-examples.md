---
descriptions: "TVU CLI command examples."
date: '2023-12-20'
section_menu: corda-enterprise-4-14
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-tvu-cli-examples
    parent: corda-enterprise-4-14-tvu
tags:
- tvu cli
- tvu
- transaction validator utility
title: TVU CLI command examples
weight: 300
---

# TVU CLI command examples

The following section provides examples of how to use the Transaction Validator Utility (TVU) CLI commands. You can modify and use the provided TVU CLI command examples to work in your project.

{{< note >}}
Unless explicitly stated, all examples assume the TVU JAR is present in the node's root directory, and that is also the current working directory.
{{< /note >}}

## Transaction validation

Validate all transactions in the database specified in the `node.conf` file of the node base directory `/cordallp/corda/nodeA/`.

```
java -jar transaction-validator.jar -b /cordallp/corda/nodeA
```

To validate all the node's transactions present at `/cordallp/corda/nodeA` without using the `-b` CLI option, paste the `transaction-validator.jar` file in the node’s base directory `/cordall/coda/nodeA` and run the command without any option. This treats the node’s base directory as the current working directory (which is the default behavior for the `-b` option) and validates all transactions using the `node.conf` file present in the current working directory. Go to `/cordallp/corda/nodeA` using `cd /cordallp/corda/nodeA` and run the command:

```
cd /cordallp/corda/nodeA; java -jar transaction-validator.jar
```

## Progress registration

You can register progress in a `.txt` file and reload it from this file using the `-l` option. If the file doesn’t exist, specifying a file path as this option’s value creates the file at this path and writes the progress into it. If the file is present, the utility loads the most recent progress from it and updates the file with the new progress.

```
java -jar transaction-validator.jar -l register.txt
```

## Progress reloading

You can register progress in a `.txt` file and reload it from this file using the `-l` option. Specifying a file path as this option’s value directs the utility to load the most recent progress from it and update the file with the new progress.

{{< note >}}
Even if all transactions from the `.txt` file have been processed, when reloading progress, the `-l` option always returns a count of one transaction for verification. This behavior is expected because, at startup, the TVU reads the last processed transaction from the progress file and then looks for any transactions in the database with a timestamp greater than or equal to the one retrieved from the file. Naturally, this will always match the last transaction previously processed.
{{< /note >}}

```
java -jar transaction-validator.jar -l register.txt
```

## Transaction time loading

You can load transactions from or after a certain transaction time.

```
java -jar transaction-validator.jar -t 2007-12-03T10:15:30.00Z
```

## Reverification using transaction ID

Reverify transactions by specifying path to a newline-separated `Ids.txt` file containing transaction IDs.

```
java -jar transaction-validator.jar -i Ids.txt
```

## Error registration

If you specify `/cordallp/corda/nodeA/errors` using the `-e` option, the errors are registered in a `.zip` file generated in this directory.

```
java -jar transaction-validator.jar -e /cordallp/corda/nodeA/errors
```

## Erroneous transaction reverification

Reverify erroneous transactions specified in the `.zip` file created using the `-e` option. Use the `-i` option with a file path to the error `.zip` file to invoke this functionality.

```
java -jar transaction-validator.jar -i /cordallp/corda/nodeA/errors/2024-01-25-18-24-25.zip
```

## Transaction processor

Process transactions as specified in the `net.corda.tvu.LogTransaction` class. Put the JAR file containing the `net.corda.tvu.LogTransaction` class in the `/cordallp/corda/nodeA/drivers` directory.

```
java -jar transaction-validator.jar -c net.corda.tvu.LogTransaction
```
