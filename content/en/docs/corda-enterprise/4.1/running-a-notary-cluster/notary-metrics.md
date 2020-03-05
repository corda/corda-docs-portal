+++
date = "2020-01-08T09:59:25Z"
title = "HA Notary Metrics"
menu = [ "corda-enterprise-4-1",]
tags = [ "notary", "metrics",]
+++


# HA Notary Metrics

Corda nodes export various performance and health metrics for monitoring, as
            described in [Node administration](../node-administration.md). The HA notary provides additional
            notary-related metrics as listed below.


## net.corda.MySQLUniquenessProvider

The MySQLUniquenessProvider collects and exposes the following metrics.


{{< table >}}

|Metric Name|Description|
|-----------------------------|------------------------------------------------------------------------------|
|Commit|Transaction commit duration and transactions per seconds|
|IPS|Input states per second|
|BatchCommit|Transaction batch commit duration and rate meter|
|Rollback|When writing to multiple masters with Galera, transaction rollbacks may
                                    happen due to high write contention|
|ConnectionException|Incremented when we can not obtain a DB connection|
|Conflicts|Double spend attempts, including notarisation retries|
|NumberOfInputStates|Distribution of number of input states per transaction|
|requestQueue.queuedStates|Number of requests in the queue at insert|

{{< /table >}}
Below is a screenshot of the metrics displayed in the Hawtio console.

![metrics](running-a-notary-cluster/resources/metrics.png "metrics")
