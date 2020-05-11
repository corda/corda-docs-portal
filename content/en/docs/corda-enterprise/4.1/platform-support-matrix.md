---
aliases:
- /releases/4.1/platform-support-matrix.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-platform-support-matrix
    weight: 70
tags:
- platform
- support
- matrix
title: Platform support matrix
---


# Platform support matrix

Our supported Operating System platforms are a subset of those supported by [Java](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda Enterprise 4.1 is only supported on Linux OS, see details below.


## JDK support

Corda Enterprise 4.1 has been tested and verified to work with **Oracle JDK 8 JVM 8u171+** and **Azul Zulu Enterprise 8**, downloadable from
[Azul Systems](https://www.azul.com/downloads/azure-only/zulu/).

{{< note >}}
On previous versions of Corda only the **Oracle JDK 8 JVM 8u171+** is supported.

{{< /note >}}
Other distributions of the [OpenJDK](https://openjdk.java.net/) are not officially supported but should be compatible with Corda Enterprise 4.1.


{{< warning >}}
In accordance with the [Oracle Java SE Support Roadmap](https://www.oracle.com/technetwork/java/java-se-support-roadmap.html)
which outlines the end of public updates of Java SE 8 for commercial use, please ensure you have the correct Java support contract in place
for your deployment needs.

{{< /warning >}}



## Operating systems supported in production


{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|7.x,
6.x|
|Suse Linux Enterprise Server|x86-64|12.x,
11.x|
|Ubuntu Linux|x86-64|16.04,
18.04|
|Oracle Linux|x86-64|7.x,
6.x|

{{< /table >}}


## Operating systems supported in development


{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Microsoft Windows|x86-64|10,
8.x|
|Microsoft Windows Server|x86-64|2016,
2012 R2,
2012|
|Apple macOS|x86-64|10.9 and
above|

{{< /table >}}


## Databases


{{< table >}}

|Vendor|CPU Architecture|Versions|JDBC Driver|
|-------------------------------|------------------|------------------|--------------------|
|Microsoft|x86-64|Azure SQL,
SQL Server 2017|Microsoft JDBC
Driver 6.2|
|Oracle|x86-64|11gR2|Oracle JDBC 6|
|Oracle|x86-64|12cR2|Oracle JDBC 8|
|PostgreSQL|x86-64|9.6|PostgreSQL JDBC
Driver 42.1.4|

{{< /table >}}
