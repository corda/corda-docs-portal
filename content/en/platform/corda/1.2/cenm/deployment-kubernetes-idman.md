---
aliases:
- /releases/release-1.2/deployment-kubernetes-idman.html
- /docs/cenm/head/deployment-kubernetes-idman.html
- /docs/cenm/deployment-kubernetes-idman.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    parent: cenm-1-2-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Identity Manager Helm chart
weight: 100
---

# CENM Identity Manager Helm chart

This Helm chart is to configure, deploy and run CENM [Identity Manager](identity-manager.md) service.

## Example usage

Using default values:

```bash
helm install idman idman
```

Overwriting default values:

```bash
helm install idman idman --set shell.password="superDifficultPassword"
```

## Configuration

{{< table >}}

| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Identity Manager Docker image                     | `corda/enterprise-identitymanager` |
| `dockerImage.tag`             | Docker image Tag | `1.2-zulu-openjdk8u242` |
| `dockerImage.pullPolicy`      | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `service.type`                | Kubernetes service type, https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types | `LoadBalancer` |
| `service.port`                | Kubernetes service port/targetPort for external communication | `10000` |
| `serviceInternal.type`        | Kubernetes service type for internal communication between CENM components | `LoadBalancer` |
| `serviceInternal.port`        | Kubernetes service port/targetPort | `5052` |
| `serviceRevocation.port`      | Kubernetes service port to access Identity Manager's revocation endpoint (targetPort) | `5053` |
| `serviceSsh.type`             | Kubernetes service type to access Identity Manager's ssh console | `LoadBalancer` |
| `shell.sshdPort`              | Identity Manager ssh port | `2222` |
| `shell.user`                  | Identity Manager ssh user | `idman` |
| `shell.password`              | Identity Manager ssh password | `idmanP` |
| `database.driverClassName`    | Identity Manager database connection details | `org.h2.Driver` |
| `database.url`                | Identity Manager database connection details | `jdbc:h2:file:./identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0; AUTO_SERVER_PORT=0` |
| `database.user`               | Identity Manager database connection details | `example-db-user` |
| `database.password`           | Identity Manager database connection details | `example-db-password` |
| `database.runMigration`       | Identity Manager database connection details | `true` |
| `cordaJarMx`                  | Initial value for memory allocation (GB) | `1` |
| `jarPath`                     | Path to a folder which contains Identity Manager jar files | `bin` |
| `configPath`                  | Path to a folder which contains Identity Manager configuration file | `etc` |

{{< /table >}}

For additional information on database connection details refer to the official documentation: [database documentation](config-database.md).
