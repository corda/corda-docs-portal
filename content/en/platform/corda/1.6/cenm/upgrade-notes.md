---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-6:
    identifier: cenm-1-6-upgrade-notes
    parent: cenm-1-6-operations
    weight: 170
tags:
- upgrade
- notes
title: Upgrading Corda Enterprise Network Manager
---


# Upgrading Corda Enterprise Network Manager

This document provides instructions for upgrading your network management suite - Identity Manager Service (formerly Doorman), Network Map Service, Signing Service, Zone Service, Auth Service, Angel Service - from previous versions to the newest version. Please consult the relevant [release notes](release-notes.md) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the [CENM Release Notes](release-notes.md) to confirm all changes between releases.
{{< /warning >}}

## 1.5.x to 1.6

### Database migration

The Identity Manager Service, the Network Map Service, the Zone Service, and the Auth Service all require database migration. To enable database migration, set `runMigration = true` in the database configuration. If a service is connecting to a database with restricted user, you must temporarily change the service settings to connect with a privileged user (a user able to modify a database schema).

### Notary migration

{{< note >}}
This step is only relevant for users migrating their CENM using a Helm chart Kubernetes deployment.
{{< /note >}}

The CENM Notary Docker image now uses Corda 4.11.1; if you are migrating from the Corda 4.5.11 Notary Docker image, you must specify the `serviceLegalName` in the notary node config file, for example:

```bash
notary {
  ...
  serviceLegalName = "O=Notary Service, C=GB, L=London"
}
```
