---
aliases:
- /releases/release-1.2/deployment-kubernetes-nmap.html
- /docs/cenm/head/deployment-kubernetes-nmap.html
- /docs/cenm/deployment-kubernetes-nmap.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    parent: cenm-1-2-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Network Map Helm chart
weight: 300
---

# CENM Network Map Helm chart

This Helm chart is to configure, deploy and run CENM [Network Map](network-map.md) service.

## Example usage

Using default values:

```bash
helm install nmap nmap
```

Overwriting default values:

```bash
helm install nmap nmap --set shell.password="superDifficultPassword"
```

## Configuration

{{< table >}}

| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Network Map Docker image                     | `corda/enterprise-networkmap` |
| `dockerImage.tag`             | Docker image tag | `1.2-zulu-openjdk8u242` |
| `dockerImage.pullPolicy`      | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `service.type`                | Kubernetes service type, https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types | `LoadBalancer` |
| `service.port`                | Kubernetes service port/targetPort for external communication | `10000` |
| `serviceInternal.type`        | Kubernetes service type for internal communication between CENM components | `LoadBalancer` |
| `serviceInternal.port`        | Kubernetes service port/targetPort | `5052` |
| `serviceRevocation.port`      | Kubernetes service port to access Identity Manager's revocation endpoint (targetPort) | `5053` |
| `serviceSsh.type`             | Kubernetes service type to access Network Map ssh console | `LoadBalancer` |
| `shell.sshdPort`              | Network Map ssh port | `2222` |
| `shell.user`                  | Network Map ssh user | `nmap` |
| `shell.password`              | Network Map ssh password | `nmapP` |
| `database.driverClassName`    | Network Map database connection details | `org.h2.Driver` |
| `database.url`                | Network Map database connection details | `jdbc:h2:file:./h2/networkmap-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0` |
| `database.user`               | Network Map database connection details | `example-db-user` |
| `database.password`           | Network Map database connection details | `example-db-password` |
| `database.runMigration`       | Network Map database connection details | `true` |
| `cordaJarMx`                  | Initial value for memory allocation (GB) | `1` |
| `jarPath`                     | Path to a folder which contains Network Map jar files | `bin` |
| `configPath`                  | Path to a folder which contains Network Map configuration file | `etc` |

{{< /table >}}

For additional information on database connection details refer to the official documentation: [database documentation](config-database.md).
