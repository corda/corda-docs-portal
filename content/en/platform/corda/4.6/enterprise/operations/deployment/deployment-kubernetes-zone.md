---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes
    identifier: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes-zone
tags:
- config
- kubernetes
title: CENM Zone Service Helm chart
weight: 70
---

# CENM Zone Service Helm Chart

This Helm chart is to configure, deploy, and run the [CENM Zone Service](../../../../cenm/1.4/zone-service.md) on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-zone zone --set prefix=cenm --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-zone auth --set idmanPublicIP=X.X.X.X --set prefix=cenm --set acceptLicense=Y --set volumeSizeZoneLogs=5Gi
```

## Configuration

{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `image.repository`            | URL to Zone Service Docker image repository              | `acrcenm.azurecr.io/zone/zone` |
| `image.tag`                   | Docker image Tag | `1.4` |
| `image.pullPolicy`            | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `database.driverClassName`    | Zone Service database connection details | `org.h2.Driver` |
| `database.jdbcDriver`         | Zone Service database connection details | `""`
| `database.url`                | Zone Service database connection details | `jdbc:h2:file:./h2/zone-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0` |
| `database.user`               | Zone Service database connection details | `example-db-user` |
| `database.password`           | Zone Service database connection details | `example-db-password` |
| `database.runMigration`       | Zone Service database connection details | `true` |
| `volumeSizeZoneH2`            | Volume size for the `h2/` directory | `1Gi` |
| `volumeSizeZoneLogs`          | Volume size for the `logs/` directory | `5Gi` |
| `zoneJar.xmx`                 | Value for java -Xmx flag | `1Gi` |
| `zoneJar.path`                | The directory where the Zone Service `.jar` is stored | `bin` |
| `zoneJar.configPath`          | The directory where the Zone Service configuration is stored | `etc` |
| `authService.host`            | Definition of the Auth Service | `auth`
| `authService.port`            | Definition of the Auth Service | `8081`
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `logsContainersEnabled`       | Enable container displaying live logs | `true`
{{< /table >}}

For additional information on database connection details, refer to the official documentation: [database documentation](../../../../cenm/1.4/config-database.md).
