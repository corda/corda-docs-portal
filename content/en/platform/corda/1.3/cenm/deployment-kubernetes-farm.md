---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    parent: cenm-1-3-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM FARM Service Helm chart
weight: 60
---

# CENM FARM Service Helm Chart

This Helm chart is to configure, deploy, and run the [CENM FARM Service]({{< relref "gateway-service.md" >}}) on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-farm farm --set prefix=cenm --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-farm farm --set prefix=cenm --set acceptLicense=Y --set volumeSizeFarmLogs=5Gi
```

## Configuration
{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `farmImage.repository`        | URL to Farm Docker image repository                      | `corda/enterprise-farm` |
| `farmImage.tag`               | Docker image tag | `1.0.2-zulu-openjdk8u242` |
| `farmImage.pullPolicy`        | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `volumeSizeFarmEtc`           | Volume size for the `etc/` directory | `1Gi` |
| `volumeSizeFarmLogs`          | Volume size for the `h2/` directory | `5Gi` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `authPort`                    | Auth Service port | `8081` |
| `farmPort`                    | FARM Service port | `8080` |
| `zonePort`                    | Zone Service port | `12345` |
| `logsContainersEnabled`       | Enable container displaying live logs | `true`
{{< /table >}}
For additional information on database connection details refer to the official documentation: [database documentation]({{< relref "config-database.md" >}}).
