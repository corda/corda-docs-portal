---
aliases:
- /releases/3.3/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 45
project: corda-enterprise
section_menu: corda-enterprise-3-3
title: Corda Enterprise 3.3
version: '3.3'
---


# Corda Enterprise 3.3

Welcome to the documentation website for Corda Enterprise 3.3, based on the Corda 3.x open source release. Corda Enterprise adds:


* High performance, thanks to multi-threaded flow execution and extensive tuning.
* Support for more database backends:

    * SQL Server 2017
    * Azure SQL
    * Oracle 11g RC2
    * Oracle 12c
    * PostgreSQL 9.6



* The Corda Firewall, for termination of TLS connections within your network’s DMZ.
* High availability features to support node-to-node failover.
* Support for advanced database migrations.

You can learn more in the [Release notes](release-notes.md).

Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
application development please continue to refer to [the main project documentation website](https://docs.corda.net/).

{{< note >}}
Corda Enterprise provides platform API version 3, which matches the API available in open source Corda 3.x releases.
Although the shipped JARs may contain new classes and methods that do not appear in API level 3, these should be considered
preliminary and not for use by application developers at this time.
{{< /note >}}
