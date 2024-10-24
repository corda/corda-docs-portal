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

## Corda Enterprise Network Manager 1.6.1

### New features and enhancements

* `sshdHost` can now be specified within the `shell {}` config block for the CENM services that support the interactive Shell.
* Added a new optional `host` parameter in the `enmListener` configuration.
* Added a new optional `host` parameter in the `adminListener` configuration.
* The Zone Service can now be started either with a configuration file or with the existing command-line options. Any current deployments using the original method remain unaffected.
* The Angel Service can now be started either with a configuration file or with the existing command-line options. Any current deployments using the original method remain unaffected.

### Fixed issues

* The Angel Service can now correctly resolve argument paths when the absolute path of the Angel Service JAR file contains spaces.
* Users can now be reset in the Auth Service.

### Upgraded dependencies

* Bouncy Castle has been upgraded from 1.75 to 1.78.1.
* CENM now supports JDK Azul 8u422 and Oracle JDK 8u421.
* CENM now supports version 9.x of the Red Hat Enterprise Linux production operating system.
* CENM now supports Ubuntu Linux production operating system versions 20.04, 22.04, 24.04.
* CENM now supports the following databases:
  * Microsoft version: SQL Server 2022.
  * Oracle version: 23.4.
  * PostgreSQL versions: 12.19, 13.3, 13.15, 14.12, 15.7, 16.3.
* CENM now supports the following node databases:
  * Microsoft version: SQL Server 2022.
  * PostgreSQL versions: 12.19, 13.3, 13.15, 14.12, 15.7, 16.3.

For more information about CENM dependencies, see [CENM support matrix]({{< relref "cenm-support-matrix.md" >}}).

## Corda Enterprise Network Manager 1.6

### New features and enhancements

* CENM 1.6 has been upgraded to use Corda 4.11, the latest Corda 4 release.
* Two network parameters for ledger recovery with Corda 4.11 have been added:
  * `recoveryMaximumBackupInterval`
  * `confidentialIdentityMinimumBackupInterval`
* CENM now supports JDK Azul 8u382 and Oracle JDK 8u381.

### Fixed issues

* Updated Typesafe Config version from 1.3.1 to 1.4.0 for the CENM CLI tool.

### Upgraded dependencies

This release includes the following dependency version changes between CENM 1.5.9 and 1.6:
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final.
* Hibernate Validator has been upgraded to 6.2.5.Final.
* Apache Tomcat has been upgraded from 9.0.80 to 9.0.81.
* Bouncy Castle has been upgraded from 1.68 to 1.75.
* H2 has been upgraded from 1.4.197 to 2.2.214.

  H2 database has been upgraded to version 2.2.224 primarily to address vulnerabilities reported in earlier versions of H2.
  H2 is not a supported production database and should only be used for development and test purposes. For detailed information
  regarding the differences between H2 version 1.4.197 used in previous versions of CENM, and the new H2 version 2.2.224 implemented in CENM 1.6,
  see the [H2 documentation](https://www.h2database.com/html/main.html). The most important differences are the following:
  * Entity naming

    H2 version 2.2.224 implements stricter rules regarding the naming of tables and columns within the database.
    The use of SQL keywords is no longer permitted.
  * Backwards compatibility

    H2 version 2.x is not backwards-compatible with older versions. Limited backwards compatibility can be achieved by adding
    `MODE=LEGACY` to the H2 database URL. For more information, go to the LEGACY Compatibility Mode section
    of the [H2 Features](https://www.h2database.com/html/features.html) page.

    H2 2.x is unable to read database files created by older H2 versions. The recommended approach for upgrading an older database
    involves exporting the data and subsequently re-importing it into a new version 2.x database. Further details on this
    process are outlined on the [H2 Migration to 2.0](https://www.h2database.com/html/migration-to-v2.html) page.

* Liquibase has been upgraded from 3.6.3 to 4.20.0.
  * Logging

    In this version of Liquibase, all INFO-level logging is directed to STDERR, while STDOUT is used for logging SQL queries.
    Utilities that have implemented their own database migration code that uses Liquibase can establish their custom logger
    to capture Liquibase's informational logging. The Liquibase API provides classes that can be used to integrate custom loggers.
