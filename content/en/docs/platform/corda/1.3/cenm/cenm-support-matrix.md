---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-cenm-support-matrix
    parent: cenm-1-3-operations
    weight: 200
tags:
- cenm
- support
- matrix
title: CENM support matrix
---


# CENM support matrix

The Operating System platforms supported in Corda Enterprise Network Manager 1.3 are a subset of those supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda Enterprise Network Manager 1.3+ is only supported on Linux OS, see details below.

For information about supported Operating Systems for Corda Enterprise, see the Corda Enterprise 4.5 [platform support matrix](../../corda-enterprise/4.5/platform-support-matrix.md) section or check the relevant [support documentation](https://docs.corda.net/docs/corda-enterprise/index.html) for previous versions of Corda Enterprise.

## Hardware Security Modules (HSMs)

Both the Signing Service and the PKI Tool support a variety of HSMs.


{{< table >}}

|Device|Firmware Version|Driver Version|High Availability (HA)|
|--------------------------------|----------------------------------|------------------|------|
|Utimaco SecurityServer Se Gen2|4.21.1|4.21.1|No|
|Gemalto Luna|7.0.3|7.3|Yes (Tested and officially supported)|
|Securosys PrimusX|2.7.4|1.8.2|No|
|Azure Key Vault|N/A|1.1.1|No|
|AWS CloudHSM|N/A|3.0.0|No|

{{< /table >}}

## CENM databases

CENM currently supports the following databases:

* PostgreSQL 9.6 (JDBC 42.2.8)
* PostgreSQL 10.10 (JDBC 42.2.8)
* PostgreSQL 12.2 (JDBC 42.2.8)
* SQL Server 2017 (Microsoft JDBC Driver 6.4)
* Oracle 11gR2 (Oracle JDBC 6)
* Oracle 12cR2 (Oracle JDBC 8)


## JDK support

Corda Enterprise 4.4+ and Corda Enterprise Network Manager 1.3+ have been tested and verified to work with **Oracle JDK 8 JVM 8u251** and **Azul Zulu Enterprise 8u252**, for Azure deployment downloadable from [Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise 4.4.

{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html)
which outlines the end of public updates of Java SE 8 for commercial use, please ensure you have the correct Java support contract in place
for your deployment needs.

{{< /warning >}}

## Operating systems supported in production

{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|7.x, 6.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.04, 18.04|
|Oracle Linux|x86-64|7.x, 6.x|

{{< /table >}}


## Operating systems supported in development


{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Microsoft Windows|x86-64|10, 8.x|
|Microsoft Windows Server|x86-64|2016, 2012 R2, 2012|
|Apple macOS|x86-64|10.9 and above|

{{< /table >}}


## Node databases


{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|------------------------|
|Microsoft|x86-64|Azure SQL,SQL Server 2017|Microsoft JDBC Driver 6.4|
|Oracle|x86-64|11gR2|Oracle JDBC 6|
|Oracle|x86-64|12cR2|Oracle JDBC 8|
|PostgreSQL|x86-64|9.6, 10.10, 11.5|PostgreSQL JDBC Driver 42.1.4 / 42.2.8|

{{< /table >}}
