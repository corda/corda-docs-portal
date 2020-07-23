---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-upgrading-and-tools
tags:
- platform
- support
- matrix
title: Platform support matrix
weight: 3
---


# Platform support matrix

Our supported Operating System platforms are a subset of those supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda Enterprise 4.5 is only supported on Linux OS, see details below.

## JDK support

Corda Enterprise 4.5 has been tested and verified to work with **Oracle JDK 8 JVM 8u251+** and **Azul Zulu Enterprise 8u252**, downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise 4.5.

{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html),
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

## MySQL notary databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|--------------------|
|Percona Server for MySQL *(deprecated)*|x86-64|5.7|MySQL JDBC Driver 8.0.16|

{{< /table >}}

## JPA notary databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|--------------------|
|CockroachDB|x86-64|19.1.2|PostgreSQL JDBCDriver 42.1.4|
|Oracle RAC|x86-64|12cR2|Oracle JDBC 8|

{{< /table >}}

## Hardware Security Modules (HSM)

{{< table >}}

|Device|Legal Identity & CA keys|TLS keys|Confidential Identity keys|Notary service keys|
|-------------------------------|----------------------------|----------------------------|----------------------------|-----------------------------|
| Utimaco SecurityServer Se Gen2| * Firmware version 4.21.1  | * Firmware version 4.21.1  | Not supported              | * Firmware version 4.21.1   |
|                               | * Driver version 4.21.1    | * Driver version 4.21.1    |                            | * Driver version 4.21.1     |
| Gemalto Luna                  | * Firmware version 7.0.3   | * Firmware version 7.0.3   | Not supported              | * Firmware version 7.0.3    |
|                               | * Driver version 7.3       | * Driver version 7.3       |                            | * Driver version 7.3        |
| FutureX Vectera Plus          | * Firmware version 6.1.5.8 | * Firmware version 6.1.5.8 | Not supported              | * Firmware version 6.1.5.8  |
|                               | * PKCS#11 version 3.1      | * PKCS#11 version 3.1      |                            | * PKCS#11 version 3.1       |
|                               | * FXJCA version 1.17       | * FXJCA version 1.17       |                            | * FXJCA version 1.17        |
| Azure Key Vault               | * Driver version 1.2.1     | * Driver version 1.2.1     | Not supported              | * Driver version 1.2.1      |
| Securosys PrimusX             | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4    |
|                               | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2      |
| nCipher nShield Connect       | * Firmware version 12.50.11| * Firmware version 12.50.11| Not supported              | * Firmware version 12.50.11 |
|                               | * Driver version 12.60.2   | * Driver version 12.60.2   |                            | * Driver version 12.60.2    |
| AWS CloudHSM                  | * Driver version 3.0.0     | * Driver version 3.0.0     | * Driver version 3.0.0     | * Driver version 3.0.0      |

{{< /table >}}
