---
aliases:
- /releases/3.2/platform-support-matrix.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-platform-support-matrix
    parent: corda-enterprise-3-2-corda-enterprise
    weight: 40
tags:
- platform
- support
- matrix
title: Platform support matrix
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Platform support matrix

Our supported Operating System platforms are a subset of those supported by Java [8u172](http://www.oracle.com/technetwork/java/javase/certconfig-2095354.html).

Production use of Corda Enterprise 3.2 is only supported on Linux OS, see details below.


## Operating systems supported in production


{{< table >}}

|Platform|CPU Architecture|Versions|
|-------------------------------|------------------|-----------|
|Red Hat Enterprise Linux|x86-64|7.x,
6.x|
|Suse Linux Enterprise Server|x86-64|12.x,
11.x|
|Ubuntu Linux|x86-64|16.10,
16.04|
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

