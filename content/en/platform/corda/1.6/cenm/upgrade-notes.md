---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-6:
    identifier: cenm-1-6-upgrade-notes
    parent: cenm-1-6-cenm-releases
    weight: 180
    name: Upgrading CENM
tags:
- upgrade
- notes
title: Upgrading Corda Enterprise Network Manager
---

# Upgrading Corda Enterprise Network Manager

This topic describes how to upgrade CENM from v1.5.x to v1.6, including the following services:

- Identity Manager Service (formerly Doorman)
- Network Map Service
- Signing Service
- Zone Service
- Auth Service
- Angel Service

Also see the relevant [CENM Release Notes]({{< relref "release-notes.md" >}}) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the above release notes to confirm all changes between releases.
{{< /warning >}}

## 1.5.x to 1.6 

The Identity Manager Service, the Network Map Service, the Zone Service, and the Auth Service all require database migration. To enable database migration, set `runMigration` to true in the database configuration. If a service is connecting to a database with a restricted user, you must temporarily change the service settings to connect with a privileged user (that is, a user able to modify a database schema).