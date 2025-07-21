---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-7:
    identifier: cenm-1-7-upgrade-notes
    parent: cenm-1-7-operations
    weight: 170
tags:
- upgrade
- notes
title: Upgrading the Network Manager
---


# Upgrading Corda Enterprise Network Manager

This document provides instructions for upgrading your network management suite — Identity Manager Service, Network Map Service, Signing Service, Zone Service, Auth Service, Angel Service — from previous versions to the newest version. Please consult the relevant [release notes]({{< relref "release-notes.md" >}}) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the [CENM Release Notes]({{< relref "release-notes.md" >}}) to confirm all changes between releases.
{{< /warning >}}

## 1.5.x to 1.6

### Database migration

The Identity Manager Service, the Network Map Service, the Zone Service, and the Auth Service all require database migration. To enable database migration, set `runMigration = true` in the database configuration. If a service is connecting to a database with a restricted user, you must temporarily change the service settings to connect with a privileged user (that is, a user able to modify a database schema).
