---
title: Platform support matrix
date: '2021-07-02'
menu:
  corda-community-4-10:
    identifier: community-platform-support-matrix
    parent: corda-community-4-10-release-notes
    weight: 450
---


# Platform support matrix

Corda supports a subset of the platforms that are supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda: Community Edition 4.10 is only supported on Linux OS, see details below.

## Network management

The Community Edition of Corda does not come with network management support included. You can still consider joining the [Corda Network](https://corda.network).

If you require network management, you can consider using the [Network Map Service from Cordite](https://gitlab.com/cordite/network-map-service). Cordite Foundation is a third-party supplier, and not supported by R3.

## Notaries

Experimental notaries, such as **Crash fault-tolerant** and **Byzantine fault-tolerant** notaries, are not available for support in Corda: Community Edition.

## JDK support

Corda: Community Edition 4.10 has been tested and verified to work with **Oracle JDK 8 JVM 8u351** and **Azul Zulu Enterprise 8u352**, for Azure deployment downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise Edition 4.10.

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
|[Oracle JDK](https://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)|8u351|
|[Amazon Corretto 8](https://aws.amazon.com/corretto/)|8.252.09.1|
|[Red Hat's OpenJDK](https://developers.redhat.com/products/openjdk/overview/)|8u322|
|[Zulu's OpenJDK](https://www.azul.com/)|8u352|

{{< /table >}}

## Operating systems supported in production

{{< table >}}

|Platform|CPU architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|8.x, 7.x, 6.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.04, 16.10, 18.04, 20.04|
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
|PostgreSQL|x86-64|9.6, 10.10, 11.5, 13.8|PostgreSQL JDBC Driver 42.1.4 / 42.2.9|

{{< /table >}}
