---
date: '2023-09-12'
menu:
  cenm-1-6:
    identifier: cenm-1-6-release-notes
    parent: cenm-1-6-cenm-releases
    weight: 80
tags:
- cenm
- release
- notes
title: Release notes
---

# Corda Enterprise Network Manager release notes

## Corda Enterprise Network Manager 1.6

### New features and enhancements

* CENM 1.6 has been upgraded to use Corda 4.11, the latest Corda 4 release.
* Two network parameters for ledger recovery with Corda 4.11 have been added:
  * `recoveryMaximumBackupInterval`
  * `confidentialIdentityMinimumBackupInterval`

### Upgraded dependencies

This release includes the following dependency version changes between CENM 1.5.9 and 1.6:
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final
* Hibernate Validator has been upgraded to 6.2.5.Final
* Apache Tomcat has been upgraded from 9.0.80 to 9.0.81
* Bouncy Castle has been upgraded from 1.68 to 1.75
* H2 has been upgraded from 1.4.197 to 2.2.214

  H2 database has been upgraded to version 2.2.224 primarily to address vulnerabilities reported in earlier versions of H2.
  H2 is not a supported production database and should only be utilized for development and test purposes. For detailed information
  regarding the differences between H2 version 1.4.197 used in CENM 1.5.9 and below, and the new H2 version 2.2.224 implemented in CENM 1.6,
  see the [H2 documentation](https://www.h2database.com/html/main.html). Although, a few noteworthy points are outlined below:

  * Entity naming

    In this version of H2, there are stricter rules regarding the naming of tables and columns within the database.
    The use of SQL keywords is no longer permitted.

  * Backwards compatibility

    H2 version 2.x is not backwards-compatible with older versions. Limited backwards compatibility can be achieved by adding
    `MODE=LEGACY` to the H2 database URL. For more information, go to the LEGACY Compatibility Mode section
    of the [H2 Features](https://www.h2database.com/html/features.html) page.

    H2 2.x is unable to read database files created by older H2 versions. The recommended approach for upgrading an older database
    involves exporting the data and subsequently re-importing it into a new version 2.x database. Further details on this
    process are outlined on the [H2 Migration to 2.0](https://www.h2database.com/html/migration-to-v2.html) page.

* Liquibase has been upgraded from 3.6.3 to 4.20.0

  * Logging

    In this version of Liquibase, all informational logging is directed to stderr, while stdout is used for logging SQL queries.
    Utilities that have implemented their own database migration code that uses Liquibase can establish their custom logger
    to capture Liquibase's informational logging. The Liquibase API provides classes that can be used to integrate custom loggers.
