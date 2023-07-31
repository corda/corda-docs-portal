---
title: Corda Community Edition 4.11 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-05-08'
menu:
  corda-community-4-11:
    identifier: corda-community-4-11-release-notes
    parent: about-corda-landing-4-11-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Community Edition 4.11 release notes

Corda Community Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.10 uses platform version 13.

For more information about platform versions, see [Versioning](versioning.md).

## New features and enhancements



## Fixed issues

This release includes the following fixes:

  
### Database schema changes

There are no database changes between 4.9 and 4.10.

### Third party component upgrades

The following table lists the dependency version changes between 4.9.5 and 4.10 Community Editions:

| Dependency           | Name           | Version 4.9.5 Community | Version 4.10 Community |
|----------------------|----------------|-------------------------|------------------------|
| com.squareup.okhttp3 | OKHttp         | 3.14.2                  | 3.14.9                 |
| org.bouncycastle	   | Bouncy Castle  | 1.68                    | 1.70                   |
| io.opentelemetry	   | Open Telemetry | -                       | 1.20.1                 |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.