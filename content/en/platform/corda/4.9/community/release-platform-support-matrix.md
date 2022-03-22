---
title: Platform support matrix
date: '2021-07-02'
menu:
  corda-community-4-9:
    identifier: community-platform-support-matrix
    parent: corda-community-4-9-release-notes
    weight: 450
---


# Platform support matrix

Corda supports a subset of the platforms that are supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda: Community Edition 4.9 is only supported on Linux OS, see details below.

## Network management

The Community Edition of Corda does not come with network management support included. You can still consider joining the [Corda Network](https://corda.network).

If you require network management, you can consider using the [Network Map Service from Cordite](https://gitlab.com/cordite/network-map-service). Cordite Foundation is a third-party supplier, and not supported by R3.

## JDK support

Corda: Community Edition 4.9 has been tested and verified to work with **Oracle JDK 8 JVM 8u251** and **Azul Zulu Enterprise 8u312**, for Azure deployment downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise 4.9.

{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html),
which outlines the end of public updates of Java SE 8 for commercial use, please ensure you have the correct Java support contract in place
for your deployment needs.
{{< /warning >}}

## JDKs supported in development

Install the **Java 8 JDK**. Corda does not currently support Java 9 or higher.

{{< table >}}

|Supported JDKs|Latest supported version|
|-----------------------------------|-----------|
|[Oracle JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)|8u321|
|[Amazon Corretto 8](https://aws.amazon.com/corretto/)|8.252.09.1|
|[Red Hat's OpenJDK](https://developers.redhat.com/products/openjdk/overview/)|8u322|
|[Zulu's OpenJDK](https://www.azul.com/)|8u322b06|

{{< /table >}}

## Operating systems supported in production

{{< table >}}

|Platform|CPU architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|8.x, 7.x, 6.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.04, 18.04|
|Oracle Linux|x86-64|7.x, 6.x|

{{< /table >}}

## Operating systems supported in development

{{< table >}}

|Platform|CPU architecture|Versions|
|-------------------------------|------------------|-----------|
|Microsoft Windows|x86-64|10, 8.x|
|Microsoft Windows Server|x86-64|2016, 2012 R2, 2012|
|Apple macOS|x86-64|10.9 and above|

{{< /table >}}

## Node databases

{{< table >}}

|Vendor|CPU architecture|Versions|JDBC driver|
|-------------------------------|------------------|------------------|------------------------|
|PostgreSQL|x86-64|9.6, 10.10, 11.5, 13.3|PostgreSQL JDBC Driver 42.1.4 / 42.2.9|

{{< /table >}}

## MySQL notary databases

{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC driver|
|-------------------------------|------------------|------------------|--------------------|
|Percona Server for MySQL *(deprecated)*|x86-64|5.7|MySQL JDBC Driver 8.0.16|

{{< /table >}}

## JPA notary databases

{{< table >}}

|Vendor|CPU architecture|Versions|JDBC driver|
|-------------------------------|------------------|------------------|--------------------|
|CockroachDB|x86-64|20.2.x|PostgreSQL JDBCDriver 42.2.9|
|Oracle RAC|x86-64|19c|Oracle JDBC 8|

{{< /table >}}

## Hardware Security Modules (HSM)

{{< table >}}

|Device|Legal identity & CA keys|TLS keys|Confidential identity keys|Notary service keys|
|-------------------------------|----------------------------|----------------------------|----------------------------|-----------------------------|
| Utimaco SecurityServer Se Gen2| Firmware version 4.21.1  | Firmware version 4.21.1  | Firmware version 4.21.1 | Firmware version 4.21.1   |
|                               | Driver version 4.21.1    | Driver version 4.21.1    | Driver version 4.21.1   | Driver version 4.21.1     |
| Gemalto Luna                  | Firmware version 7.0.3   | Firmware version 7.0.3   | Firmware version 7.0.3  | Firmware version 7.0.3    |
|                               | Driver version 7.3       | Driver version 7.3       | Driver version 7.3      | Driver version 7.3        |
| FutureX Vectera Plus          | Firmware version 6.1.5.8 | Firmware version 6.1.5.8 | Firmware version 6.1.5.8 | Firmware version 6.1.5.8  |
|                               | PKCS#11 version 3.1      | PKCS#11 version 3.1      | PKCS#11 version 3.1      | PKCS#11 version 3.1       |
|                               | FXJCA version 1.17       | FXJCA version 1.17       | FXJCA version 1.17       | FXJCA version 1.17        |
| Azure Key Vault               | Driver version           | Driver version           | Driver version (SOFTWARE mode only)| Driver version  |
|                               | azure-identity 1.2.0     | azure-identity 1.2.0     | azure-identity 1.2.0     | azure-identity 1.2.0      |
|                               | azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3| azure-security-keyvault-keys 4.2.3|
| Securosys PrimusX             | Firmware version 2.7.4   | Firmware version 2.7.4   | Firmware version 2.7.4   | Firmware version 2.7.4    |
|                               | Driver version 1.8.2     | Driver version 1.8.2     | Driver version 1.8.2     | Driver version 1.8.2      |
| nCipher nShield Connect       | Firmware version 12.50.11| Firmware version 12.50.11| Firmware version 12.50.11| Firmware version 12.50.11 |
|                               | Driver version 12.60.2   | Driver version 12.60.2   | Driver version 12.60.2   | Driver version 12.60.2    |
| AWS CloudHSM                  | Driver version 3.2.1     | Driver version 3.2.1     | Driver version 3.2.1     | Driver version 3.2.1      |

{{< /table >}}
