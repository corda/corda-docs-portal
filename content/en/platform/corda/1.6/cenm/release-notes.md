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

## Corda Enterprise Network Manager 1.6.3

### New features and enhancements

- CENM now supports JDK Azul 8uXXX and Oracle JDK 8uXXX (fill later).
- CENM now supports the following PostgreSQL versions: 12.22, 13.22, 14.19, 15.14, 16.10 (double check later). <!-- ENT 14086 --> 

### Fixed issues

- Fixed various issues related to CENM deployment using Docker, Kubernetes, and Helm charts. <!-- ENT-14010 -->
- Fixed an issue where an incorrect error message "No NETWORK_MAP type signing process set up" appeared when displaying unsigned network parameters data via the CENM tool. <!-- ENT 13944 -->
- The [shell Signing Service]({{< relref "shell.md#signing-service" >}}) `clientHealthCheck` health checks now work correctly across all service types.  <!-- ENT 13942 -->
- Fixed an issue where setting `certificates.key.type` to `AZURE_MSAL_KEY_VAULT_HSM` in the PKI tool configuration file was generating an error. <!--ENT-13898 -->

## Corda Enterprise Network Manager 1.6.2

### Fixed issues
* Signing Service now starts correctly when used with the MSAL (Microsoft Authentication Library) for Azure Cloud HSM integration.

## Corda Enterprise Network Manager 1.6.1

### New features and enhancements

* `sshdHost` can now be specified within the `shell {}` config block for the CENM services that support the interactive Shell.
* Added a new optional `host` parameter in the `enmListener` configuration.
* Added a new optional `host` parameter in the `adminListener` configuration.
* The Zone Service can now be started either with a configuration file or with the existing command-line options. Any current deployments using the original method remain unaffected.
* The Angel Service can now be started either with a configuration file or with the existing command-line options. Any current deployments using the original method remain unaffected.
* Added Azure cloud HSM integration with the MSAL (Microsoft Authentication Library) dependency. While users can continue to use integration through ADAL (Azure Active Directory Authentication Library), it is now marked as deprecated.
* Made the logging in CENM more consistent with Corda node logging. Errors appearing in CENM log files will be by default printed to the console now. This behaviour can be modified by providing a custom `log4j2.xml` file.

### Fixed issues

* The Angel Service can now correctly resolve argument paths when the absolute path of the Angel Service JAR file contains spaces.
* Users can now be reset in the Auth Service.
* Error messages when submitting CRRs through the CRR Submission Tool are now improved.
* Audit log messages are now correctly generated when users are added to a group.
* The CENM logger respects custom `log4j2.xml` files now. You can now provide custom `log4j2.xml` files and CENM will use the custom logging configuration.
* A warning emitted by Hibernate about equality of `SignedNodeInfo` has been eliminated.
* Authentication Service: HTTP metrics have been disabled by default to secure CENM from the [CVE-2023-34055](https://spring.io/security/cve-2023-34055) security vulnerability in Spring. The metrics can be enabled by setting the `corda.management.metrics.enable.http.server.requests` property to `true`.

### Upgraded dependencies

The following table lists the dependency version changes between CENM 1.6 and CENM 1.6.1:

| Dependency                                                | Name                       | CENM 1.6       | CENM 1.6.1    |
|-----------------------------------------------------------|----------------------------|----------------|---------------|
| org.bouncycastle                                          | Bouncy Castle              | 1.75           | 1.78.1        |
| org.springframework.security.oauth:spring-security-oauth2 | Spring Security            | 2.5.0.RELEASE  | 2.5.2.RELEASE |
| org.springframework:spring-*                              | Spring Framework           | 5.3.27         | 5.3.39        |
| org.springframework.security:*                            | Spring Framework Security  | 5.5.8          | 5.8.16        |
| com.nimbusds:nimbus-jose-jwt                              | Nimbus JOSE+JWT            | 8.19           | 9.48          |
| com.fasterxml.jackson.core:*                              | Jackson                    | 2.14.2         | 2.18.2        |
| io.projectreactor:reactor-core	                           | Project Reactor Core	      | 3.4.11	        | 3.4.41        |
| org.apache.tomcat.embed:tomcat-embed-*	                   | Apache Tomcat	             | 9.0.81	        | 9.0.98        |
| org.yaml:snakeyaml	                                       | Snake YAML	                | 1.33	          | 2.3           |
| commons-io:commons-io	                                    | Apache Commons IO	         | 2.11.0	        | 2.18.0        |
| info.picocli:picocli	                                     | PicoCLI	                   | 3.9.6	         | 4.1.4         |
| com.typesafe:config	                                      | Typesafe Config		          | 1.3.4	         | 1.4.0         |
| org.testcontainers:testcontainers	                        | TestContainers	            | 1.14.3	        | 1.15.2        |
| org.mockito.kotlin:mockito-kotlin		                       | Mockito Kotlin	            | 2.0.0-alpha01	 | 2.2.0         |
| org.junit.jupiter:junit-jupiter-api		                     | JUnit Jupiter API	         | 5.6.1	         | 5.6.2         |
| commons-codec:commons-codec		                             | Apache Commons Codec	      | 1.13           | 1.14          |

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
