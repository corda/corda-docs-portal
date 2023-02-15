---
date: '2023-02-13'
menu:
  corda-enterprise-4-7:
    parent: about-corda-landing
    name: Platform support
tags:
- platform
- support
- matrix
title: Corda Enterprise 4.7 platform support
weight: 250
---

# Platform support

This topic lists the JDKs, operating systems and database types that support Corda Enterprise Edition 4.7, both for production and for development.

## JDK support

Corda Enterprise Edition supports a subset of the platforms that are supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

### JDK support in production

Corda Enterprise Edition 4.7 has been tested and verified to work with **Oracle JDK 8 JVM 8u251** and **Azul Zulu Enterprise 8u252**, for Azure deployment downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise Edition 4.7.

{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html),
which outlines the end of public updates of Java SE 8 for commercial use, please ensure you have the correct Java support contract in place
for your deployment needs.
{{< /warning >}}

## Operating systems support

### Operating systems support in production

Production use of Corda Enterprise Edition 4.7 is only supported on Linux OS; see details below.

{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|7.x, 6.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.04, 18.04|
|Oracle Linux|x86-64|7.x, 6.x|

{{< /table >}}

### Operating systems support in development

The following operating systems can be used with Corda for development purposes.

{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Microsoft Windows|x86-64|10, 8.x|
|Microsoft Windows Server|x86-64|2016, 2012 R2, 2012|
|Apple macOS|x86-64|10.9 and above|

{{< /table >}}

## Database support

The following database types are supported both in production and for development purposes.                                                                                           
### Node databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|------------------------|
|Microsoft|x86-64|Azure SQL,SQL Server 2017|Microsoft JDBC Driver 6.4|
|Oracle|x86-64|11gR2|Oracle JDBC 6|
|Oracle|x86-64|12cR2|Oracle JDBC 8|
|PostgreSQL|x86-64|9.6, 10.10, 11.5|PostgreSQL JDBC Driver 42.1.4 / 42.2.8|

{{< /table >}}

### MySQL notary databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|--------------------|
|Percona Server for MySQL *(deprecated)*|x86-64|5.7|MySQL JDBC Driver 8.0.16|

{{< /table >}}

### JPA notary databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|--------------------|
|CockroachDB|x86-64|20.1.x|PostgreSQL JDBCDriver 42.1.4|
|Oracle RAC|x86-64|12cR2|Oracle JDBC 8|

{{< /table >}}

## Docker images

The Docker images used for the Kubernetes deployment are listed below for reference:

{{< table >}}
| Service           | Image name                                                  |
|-------------------|-------------------------------------------------------------|
| Identity Manager  | `corda/enterprise-identitymanager:1.5.4-zulu-openjdk8u242`  |
| Network Map       | `corda/enterprise-networkmap:1.5.4-zulu-openjdk8u242`       |
| Signing           | `corda/enterprise-signer:1.5.4-zulu-openjdk8u242`           |
| Zone              | `corda/enterprise-zone:1.5.4-zulu-openjdk8u242`             |
| Auth              | `corda/enterprise-auth:1.5.4-zulu-openjdk8u242`             |
| Gateway           | `corda/enterprise-gateway:1.5.4-zulu-openjdk8u242`          |
| PKI Tool          | `corda/enterprise-pkitool:1.5.4-zulu-openjdk8u242`          |
| Notary            | `corda/enterprise-notary:4.5.9-zulu-openjdk8u242`           |
{{< /table >}}

## Hardware Security Modules (HSM)

{{< table >}}

|Device|Legal Identity & CA keys|TLS keys|Confidential Identity keys|Notary service keys|
|-------------------------------|----------------------------|----------------------------|----------------------------|-----------------------------|
| Utimaco SecurityServer Se Gen2| * Firmware version 4.21.1  | * Firmware version 4.21.1  | Not supported              | * Firmware version 4.21.1   |
|                               | * Driver version 4.21.1    | * Driver version 4.21.1    |                            | * Driver version 4.21.1     |
| Gemalto Luna                  | * Firmware version 7.0.3   | * Firmware version 7.0.3   | Not supported              | * Firmware version 7.0.3    |
|                               | * Driver version 7.3       | * Driver version 7.3       |                            | * Driver version 7.3        |
| FutureX Vectera Plus          | * Firmware version 6.1.5.8 | * Firmware version 6.1.5.8 | * Firmware version 6.1.5.8 | * Firmware version 6.1.5.8  |
|                               | * PKCS#11 version 3.1      | * PKCS#11 version 3.1      | * PKCS#11 version 3.1      | * PKCS#11 version 3.1       |
|                               | * FXJCA version 1.17       | * FXJCA version 1.17       | * FXJCA version 1.17       | * FXJCA version 1.17        |
| Azure Key Vault               | * Driver version 1.2.1     | * Driver version 1.2.1     | * Driver version 1.2.1 (SOFTWARE mode only)| * Driver version 1.2.1      |
| Securosys PrimusX             | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4   | * Firmware version 2.7.4    |
|                               | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2     | * Driver version 1.8.2      |
| nCipher nShield Connect       | * Firmware version 12.50.11| * Firmware version 12.50.11| * Firmware version 12.50.11| * Firmware version 12.50.11 |
|                               | * Driver version 12.60.2   | * Driver version 12.60.2   | * Driver version 12.60.2   | * Driver version 12.60.2    |
| AWS CloudHSM                  | * Driver version 3.2.1     | * Driver version 3.2.1     | * Driver version 3.2.1     | * Driver version 3.2.1      |

{{< /table >}}
