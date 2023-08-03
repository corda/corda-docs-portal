---
title: Corda Enterprise Edition 4.11 release notes
date: '2023-05-08'

menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-release-notes
    parent: about-corda-landing-4-11-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.11 release notes

Corda Enterprise Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## New features and enhancements

* This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

* Updated documentation for both `.startNodes()` and `.stopNodes()` of `MockNetwork` to indicate that restarting nodes is not supported.

## Fixed issues

This release includes the following fixes:



### Database schema changes

There are no database changes between 4.10 and 4.11.

### Third party component upgrades

The following table lists the dependency version changes between 4.10.2 and 4.11 Enterprise Editions:

| Dependency                         | Name                | Version 4.1.2 Enterprise | Version 4.11 Enterprise|
|------------------------------------|---------------------|--------------------------|------------------------|
| com.squareup.okhttp3               | OKHttp              | 3.14.2                   | 3.14.9                 |
| org.bouncycastle                   | Bouncy Castle       | 1.68                     | 1.70                   |
| io.opentelemetry                   | Open Telemetry      | -                        | 1.20.1                 |
| org.apache.commons:commons-text    | Apache Commons-Text | 1.9                      | 1.10.0                 |
| org.apache.shiro                   | Apache Shiro        | 1.9.1                    | 1.10.0                 |

## Log4j patches

Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.