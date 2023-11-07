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
* H2 has been upgraded from 1.4.197 to 2.1.214.
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final.
* Hibernate Validator has been upgraded to 6.2.5.Final.
* Liquibase has been upgraded from 3.6.3 to 4.20.0.
* Apache Tomcat has been upgraded from 9.0.80 to 9.0.81.
* Bouncy Castle has been upgraded from 1.68 to 1.75.
