---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Gateway Service Helm chart
weight: 60
---

# CENM Gateway Service Helm Chart

This Helm chart is to configure, deploy, and run the [CENM Gateway Service](gateway-service.md/) on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-gateway gateway --set prefix=cenm --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-gateway gateway --set prefix=cenm --set acceptLicense=Y --set volumeSizeGatewayLogs=5Gi
```

## Configuration
{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `gatewayPortImage.repository`        | URL to Gateway Docker image repository                      | `acrcenm.azurecr.io/auth/auth` |
| `gatewayImage.tag`               | Docker image tag | `1.4` |
| `gatewayImage.pullPolicy`        | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `volumeSizeGatewayEtc`           | Volume size for the `etc/` directory | `1Gi` |
| `volumeSizeGatewayLogs`          | Volume size for the `h2/` directory | `5Gi` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `authPort`                    | Auth Service port | `8081` |
| `gatewayPort`                    | Gateway Service port | `8080` |
| `zonePort`                    | Zone Service port | `12345` |
| `logsContainersEnabled`       | Enable container displaying live logs | `true`
{{< /table >}}

For additional information on database connection details refer to the official documentation: [database documentation](config-database.md/).
