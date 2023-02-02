---
date: '2020-06-01T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- db
- monitoring
- notary
- agent
title: Monitoring the Corda Notary database
weight: 10
---

# Monitoring the Corda Notary database

A notary database contains tables and records of notarised transactions. In rare instances, notaries can be vulnerable
to 'silent failures' that may not be detected. These failures can be caused by accidental deletion of notary records,
or by errors within the notary database.

In the case of a non-validating notary, if a transaction is notarised, and the record of that transaction is later damaged or lost,
there may be a risk of double-spend transactions being undetected. To prevent double-spends, it is important to monitor the notary database
for damaged or deleted entries.

{{< note >}}
The database monitoring agent is only supported by a high-availability JPA notary implementation.
{{< /note >}}

## Database monitoring agent

You can use the database monitoring agent to check that previously notarised transactions are still present in the notary
database. The database monitoring agent allows you to check that previously notarised transactions are still present in
the notary database so that you can be notified of database errors, such as accidental entry deletion, invalid database
entries, or silent write failures caused by bugs in the JDBC driver.

If you have configured the database monitoring agent, a check will be run against the transaction record after the
transaction has been committed. If the check returns a failure, it indicates that some expected transaction data is
missing from the database.

When a check fails, an error is logged to the notary log file, and a metric counter is incremented. Notary logs are stored in
the notary's working directory at `logs/node-<hostname>.log`.

Notary operators should set alerts based on the metric counter and log file.

### Creating and configuring the database monitoring agent

The database monitoring agent configuration block should be in the `notary` block inside the `node.conf` file of each notary worker in the cluster.

If the `notary.jpa.dbMonitoringAgent` is empty, the database monitoring agent will be created using the default values. If the `notary.jpa.dbMonitoringAgent` block is not added, the database monitoring agent will not be created.

You can configure the database monitoring agent using the following parameters:

{{< table >}}

|Configuration parameter|Description|Format|Default|
|-----------------------|-----------|------|-------|
|`dataCheckDelay`|Time until the database monitoring agent checks that a committed transaction exists in the notary database.|Duration: `10seconds`, `1minute`. If no unit is specified, the default unit is milliseconds.|3 minutes.|
|`sampleRate`|The decimal percentage in the range 0.0 to 1.0 representing the portion of notarised transactions for the agent to check.|Double|0.1|
|`readBatchSize`|The maximum number of committed transactions to be checked in a single batch.|Int|200|
|`batchTimeoutMs`| Length of time to wait for a full batch before a batch is processed.|Time in milliseconds.|200ms|

{{< /table >}}

#### Example configuration

```
dbMonitoringAgent {
    dataCheckDelay = 5minutes
    sampleRate = 0.5
    readBatchSize = 150
    batchTimeoutMs = 250ms
}
```

### Metrics

The database monitoring agent produces a small number of metrics:
- `processedBatchSize`: The size of each batch of transactions that have been checked by the monitoring agent.
- `batchTimer`: The time taken for each batch to be processed.
- `missingTransactionDataCount`: The total count of missing transaction data. If this metric is greater than zero, it
indicates that notarised transactions are missing data in the notary database.

### Performance impact

Using the database monitoring agent will increase the number of database read operations. For flexibility, the database monitoring agent
can be configured to check only a portion of all notarised transactions.

Checking a smaller number of transactions may be useful to detect incorrect database configuration - for example, the incorrect clearing of a database table.
