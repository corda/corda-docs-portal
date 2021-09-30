---
aliases:
- /releases/4.3/running-a-notary-cluster/notary-sizing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-notary-sizing
    parent: corda-enterprise-4-3-ha-notary-service-overview
    weight: 1120
tags:
- notary
- sizing
title: Notary sizing considerations
---


# Notary sizing considerations


## Notary disk space requirements

The disk space required for a notary depends on how many transactions are notarised and how many states each of those
transactions contain. Disk space required increases linearly with the number of notarisation requests, notarised
transactions and notarised states. Note that even unsuccessfully notarised requests will consume disk space, while
configuring a notary in highly available mode does not cause the notary database to use more space.

Notaries store their data in two databases - the replicated database for storing notarisation results, as well as the
local notary worker database for storing the notary’s identity as well as data related to messaging. The largest amount
of required space will be for the notarisation results. Since these notarisation results will be replicated across
each of the database servers, this space is required per replicated database server.


### Maximum disk space formula

The following formula can be helpful in estimating the maximum disk space required for notarisation results:

```none
Bytes Required = (Number of transactions * 1952 bytes)
+ (Number of transactions * States per transaction * 276 bytes)
+ (Number of transactions * Percentage of transactions retried * 1823 bytes)
```


* “Number of transactions” indicates the total number of transactions required to be notarised.
* “States per transaction” indicates the average number of states per transaction. This will depend on the CorDapp.
* “Percentage of transactions retried” indicates the fraction of transactions for which more than one request will be received. As even unsuccessful requests consume space, this impacts the space required.

The following table contains some example scenarios that could be useful in determining disk space requirements. Note
that the disk space requirements given are always the maximum, meaning actual space required could be lower.


### Maximum disk space required for notary storage


{{< table >}}

|Notarised transations|States per transaction|Percentage of transations retried|Max space required (gigabytes)|
|-----------------------|--------------------------|-------------------------------------|---------------------------------|
|1 million|1|0%|1.98|
|10 million|2|1%|20.75|
|1 billion|4|2%|2332.46|

{{< /table >}}


## Notary performance considerations

Notary performance is defined by the ability of the notary to service incoming requests at a high enough rate that the latency
for such requests does not grow to unacceptable levels. Thus, the throughput of the notary in terms of states per second is
used as a proxy for the latency. For more details on notary performance measurement, see [Highly-available notary metrics](notary-metrics.md).

Note that notary performance degrades as the database fills up. This is an unavoidable consequence of the notary having more
states to examine when detecting double spend attempts. Some databases, notably CockroachDB, exhibit less degradation than
other databases, although the difference will only be apparent with databases containing more than a billion states.

Because of the performance degradation, we recommend sizing a notary and its database according to the expected minimum throughput
measured in states per second and the expected data volumes in terms of notarised states.

Notary performance is most affected by the hardware specifications of the database server, although the hardware specifications
of the notary worker are also important. It is recommend to have the database server and notary on separate machines.

The following tables show the relationship between minimum input states per second (IPS) and committed states. Note that the IPS
figure shown here refers to the notary in isolation, thus real world performance is likely to be lower.


### Performance table for low spec notary

The below table shows the performance of a notary cluster configured using the below minimum specifications:



* 3 * Microsoft Azure D8s v3 virtual machines
* 8 virtual CPUs, 32GB of memory, and a Premium SSD with a Max IOPS rating of 12800
* Ubuntu 18.04 LTS
* CockroachDB installed on each of the virtual machines
* One JPA notary worker running on each of the virtual machines


Note that the performance below is representative only.


{{< table >}}

|Committed states|States per second|
|---------------------|-------------------|
|10 million|1600|
|100 million|1500|
|1 billion|1350|
|6 billion|1300|
|9 billion|1300|

{{< /table >}}


### Performance table for high spec notary

The below table shows the performance of a notary configured using the below high specifications:



* 5 * physical machines
* Intel 2x Xeon E5-2687Wv4, 24 cores hyperthreaded, 256GB DDR4 ECC 2133 MHz, 2x 400GB NVME
* Ubuntu 18.04 LTS
* CockroachDB installed on each of the machines
* One JPA notary worker running on each of the machines


Note that the performance below is representative only.


{{< table >}}

|Committed states|States per second|
|---------------------|-------------------|
|2 billion|3500|
|20 billion|3500|
|40 billion|3500|
|100 billion|2200|
|200 billion|500|

{{< /table >}}
