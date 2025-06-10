---
title: "Corda Enterprise vs Corda Open Source"
date: '2021-07-02'
menu:
  corda-enterprise-4-13:
    parent: about-corda-landing-4-13-enterprise
    weight: 200
    name: "Enterprise vs Open Source"
tags:
- concepts
- enterprise
- community
- comparison

---

# Corda Enterprise vs Corda Open Source Edition

Details on Corda Enterprise features compared to Corda Open Source Edition features follow below.

## Corda functionality

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Corda ledger|&#10003;|&#10003;|
|Flow framework|&#10003;|&#10003;|
|Immutable states|&#10003;|&#10003;|
|Vault|&#10003;|&#10003;|
|Smart contracts|&#10003;|&#10003;|
|Atomic transactions (with input, output and reference states)|&#10003;|&#10003;|
|Multiple accounts|&#10003;|&#10003;|
|Supported development languages|Java, Kotlin|Java, Kotlin|
|Standard Corda APIs|&#10003;|&#10003;|
|Compatible with any Corda network |&#10003;|&#10003;|

{{< /table >}}

## Node

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Single node|&#10003;|&#10003;|
|Multiple nodes for high availability/disaster recovery|&#10007;|&#10003;|

{{< /table >}}

## Connectivity

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|In-process Artemis MQ|&#10003;|&#10003;|
|External Artemis MQ|&#10007;|&#10003;|
|Corda firewall|&#10007;|&#10003;|
|Multi-node use of a shared external Artemis MQ and a shared Corda firewall|&#10007;|&#10003;|

{{< /table >}}

## Key storage

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Java keystore file|&#10003;|&#10003;|
|HSM support|&#10007;|&#10003;|

{{< /table >}}

## Vault databases

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|H2 (development use only)|&#10003;|&#10003;|
|Postgres|&#10003; Please note that this has been harmonised with Corda Enterprise in Corda 4.5 to allow for in-place upgrades|&#10003;|
|SQL Server|Experimental only|&#10003;|
|Oracle|&#10007;|&#10003;|

{{< /table >}}

## Notaries

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Simple notary|&#10003;|&#10003;|
|Oracle RAC connectivity|&#10007;|&#10003;|
|CockroachDB connectivity|&#10007;|&#10003;|
|Clustered notary (for high availability)|&#10007;|&#10003;|

{{< /table >}}

## Performance

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Dynamic database caching and performance enhancements|&#10007;|&#10003;|
|Multi-threaded flow state machine|&#10007;|&#10003;|

{{< /table >}}

## Tooling

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Node health check tool|&#10007;|&#10003;|
|Configuration obfuscation tool|&#10007;|&#10003;|
|HA admin tool|&#10007;|&#10003;|

{{< /table >}}

## Support

{{< table >}}

|Feature|Corda Open Source Edition|Corda Enterprise|
|:------------------------------|:-----------------------------:|:-----------------------------:|
|Developer mailing lists (no SLA)|&#10003;|&#10003;|
|Cordaledger slack (no SLA)|&#10003;|&#10003;|
|Software maintenance|&#10007;|&#10003;|
|Support by R3 Support Engineering|&#10007;|&#10003;|
|Access to R3 Professional Services|Upgrading to Corda Enterprise only |&#10003;|

{{< /table >}}

