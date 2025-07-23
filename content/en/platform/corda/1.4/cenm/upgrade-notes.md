---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-upgrade-notes
    parent: cenm-1-4-cenm-releases
    weight: 180
    name: Upgrading CENM
tags:
- upgrade
- notes
title: Upgrading Corda Enterprise Network Manager
---


# Upgrading Corda Enterprise Network Manager

This topic describes how to upgrade CENM from v1.3.x version to v1.4, including the following services:

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

## 1.3.x to 1.4

CENM 1.4 includes a few changes and improvements that require some additional upgrade steps, as described below.

The general procedure for upgrading from CENM 1.3 to CENM 1.4 is as follows:

1. Stop all CENM 1.3 services.
2. To prevent picking up old Signing Service configurations by the Angel Service, remove or rename all configuration files that have to be updated (see the sections below).
3. Update Signing Service configuration files, as [described below](#manual-update-of-all-existing-signing-service-configurations). Note that there is a change in the way `subZoneID` is set in Signing Service configurations, as [described below](#signing-service-configuration-changes).
4. Replace the JAR files for all services with the latest CENM 1.4 JAR files. **Important** In CENM 1.4, the FARM Service has been renamed to "Gateway Service", so the FARM Service JAR file used in CENM 1.3 should be replaced with the Gateway Service JAR file used in CENM 1.4.
5. Start the Auth Service, the Zone Service, and the Gateway Service. **Important:** The Zone Service requires the `--run-migration` option to be set to `true`, as [described below](#zone-service-database-migration).
6. Submit the updated configurations to the Zone Service.
7. Start the Identity Manager Service, the Signing Service, and the Network Map Service.

### Zone Service database migration

If you are upgrading to CENM 1.4 from CENM 1.3, you **must** set `runMigration = true` in the database configuration. This is required due to a change in the Zone Service database schema - a new column in the database tables `socket_config` and `signer_config` called `timeout` is used to record the new optional `timeout` parameter values used in `serviceLocations` configuration blocks (Signing Services) and `identityManager` and `revocation` configuration blocks (Network Map Service). This value can remain `null`,
in which case the default 30 seconds timeout will be used wherever applicable.

An example follows below:

```
database = {
  driverClassName = "org.h2.Driver"
  user = "testuser"
  password = "password"
  url = "jdbc:h2:file:/etc/corda/db;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  runMigration = true
}
```

### Signing Service configuration changes

In CENM 1.3 (and older versions), `subZoneID` was defined in Signing Service configurations as part of the service location alias (`serviceLocationAlias`), as shown below:

```
serviceLocations.network-map-<subzone ID>
```

And:

```
signers.NetworkMap.serviceLocationAlias = "network-map-<subzone ID>"
signers.NetworkParameters.serviceLocationAlias = "network-map-<subzone ID>"
```

In CENM 1.4, you must define `subZoneID` as new property value, as follows:

```
signers.NetworkMap.subZoneId = <subzone ID>
signers.NetworkParameters.subZoneId = <subzone ID>
```

### Manual update of all existing Signing Service configurations

The SMR (Signable Material Retriever) Service, which prior to CENM 1.4 was used to handle plug-ins for signing data, has been replaced by a plug-in loading logic inside the Signing Service. As a result, **all users must update their existing Signing Service configuration** when upgrading to CENM 1.4.

To update your Signing Service configuration:

1. Remove the `serviceLocationAlias` property from the signing task.
2. Remove the `serviceLocations` property and move the locations defined there to `serviceLocation` properties inside each signing task. Note that as a result Network Parameters signing tasks and Network Map signing tasks will have the same `serviceLocation` property.
3. Remove the `caSmrLocation` property.
4. Remove the `nonCaSmrLocation` property.
5. Configure the `pluginClass` and `pluginJar` properties inside each signing task to use the following structure:

```
plugin {
pluginClass =
pluginJar
}
```