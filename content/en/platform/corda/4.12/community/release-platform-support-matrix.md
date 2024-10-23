---
title: Platform support matrix
date: '2021-07-02'
menu:
  corda-community-4-12:
    identifier: community-platform-support-matrix
    parent: about-corda-landing-4-12-community
    weight: 450
---


# Platform support matrix

Corda supports a subset of the platforms that are supported by [Java](https://www.oracle.com/java/technologies/javase/products-doc-jdk17certconfig.html).

Production use of Corda Open Source 4.12 is only supported on Linux OS, see details below.

## Network management

The Open Source Edition of Corda does not come with network management support included. You can still consider joining the [Corda Network](https://corda.network).

If you require network management, you can consider using the [Network Map Service from Cordite](https://gitlab.com/cordite/network-map-service). Cordite Foundation is a third-party supplier, and not supported by R3.

## Notaries

Experimental notaries, such as **Crash fault-tolerant** and **Byzantine fault-tolerant** notaries, are not available for support in Corda: Open Source Edition.

## JDK support

Corda Open Source Edition 4.12 has been tested and verified to work with **Azul Zulu Enterprise 17.0.9**, for Azure deployment downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise Edition 4.11.

## JDKs supported in development

The following JDKs support Corda for development purposes. Corda does not currently support Java 18 or higher.

{{< table >}}

|Supported JDKs|Latest supported version|
|-----------------------------------|-----------|
|[Zulu OpenJDK](https://www.azul.com/)|17.0.9|
|[Oracle JDK](https://www.oracle.com/ie/java/technologies/downloads/)|17.0.11|

{{< /table >}}

## Operating systems supported in production

Production use of Corda Open Source 4.12 is only supported on Linux OS; see details below.

{{< table >}}

|Platform|CPU architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|8.x, 7.x, 6.x, 9.x|
|Suse Linux Enterprise Server|x86-64|12.x, 11.x|
|Ubuntu Linux|x86-64|16.10, 20.04, 22.04, 24.04|
|Oracle Linux|x86-64|7.x, 6.x|

{{< /table >}}

## Operating systems support in development

The following operating systems can be used with Corda for development purposes.

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
|PostgreSQL|x86-64|12.19, 13.12, 13.15, 13.3, 14.12, 15.3, 15.7, 16.3|PostgreSQL JDBC Driver 42.1.4 / 42.5.2|

{{< /table >}}
