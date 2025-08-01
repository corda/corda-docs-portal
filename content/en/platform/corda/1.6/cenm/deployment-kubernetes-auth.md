---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-6:
    parent: cenm-1-6-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Auth Service Helm chart
weight: 20
---

# CENM Auth Service Helm Chart

This Helm chart is to configure, deploy, and run the [Auth Service]({{< relref "../../4.11/enterprise/node/auth-service.md" >}}) on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-auth auth --set prefix=cenm --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-auth auth --set prefix=cenm --set acceptLicense=Y --set volumeSizeAuthLogs=5Gi
```

## Configuration

{{< table >}}
| Parameter  | Description   | Default value    |
| ---------- | ------------- | -----------------|
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `authImage.repository`        | URL to Network Map Docker image repository | `corda/enterprise-auth` |
| `authImage.tag`               | Docker image tag | `1.6-zulu-openjdk8u392` |
| `authImage.pullPolicy`        | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `database.driverClassName`    | Auth Service database connection details | `org.h2.Driver` |
| `database.jdbcDriver`         | Auth Service database connection details | `""`
| `database.url`                | Auth Service database connection details | `jdbc:h2:file:./h2/networkmap-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0` |
| `database.user`               | Auth Service database connection details | `example-db-user` |
| `database.password`           | Auth Service database connection details | `example-db-password` |
| `database.runMigration`       | Auth Service database connection details | `true` |
| `volumeSizeAuthEtc`           | Volume size for the `etc/` directory | `1Gi` |
| `volumeSizeAuthH2`            | Volume size for the `h2/` directory | `5Gi` |
| `volumeSizeAuthLogs`          | Volume size for the `logs/` directory | `5Gi` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `logsContainersEnabled`       | Enable container displaying live logs | `true`
{{< /table >}}
For additional information on database connection details refer to the official documentation: [database documentation]({{< relref "config-database.md" >}}).
