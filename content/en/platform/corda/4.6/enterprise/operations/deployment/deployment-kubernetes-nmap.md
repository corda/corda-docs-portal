---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes
    identifier: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes-nmap
tags:
- config
- kubernetes
title: CENM Network Map Helm chart
weight: 40
---

# CENM Network Map Service Helm Chart

This Helm chart is to configure, deploy, and run the [CENM Network Map Service](../../../../cenm/1.4/network-map.md) on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install nmap nmap
```

In the example below, the default values are overwritten:

```bash
helm install nmap nmap --set shell.password="superDifficultPassword"
```

## Configuration

{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `volumeSizeNmapEtc`           | Volume size for the `etc/` directory                     | `1Gi` |
| `volumeSizeNmapLogs`          | Volume size for the `logs/` directory                    | `10Gi` |
| `volumeSizeNmapH2`            | Volume size for the `h2/` directory                      | `10Gi` |
| `dockerImage.repository`      | URL to Network Map Docker image repository               | `acrcenm.azurecr.io/networkmap/networkmap` |
| `dockerImage.tag`             | Docker image tag | `1.4` |
| `dockerImage.pullPolicy`      | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `dockerImageCli.repository`   | URL to CLI image repository | `acrcenm.azurecr.io/cli/cli` |
| `dockerImageCli.tag`          | Docker image tag | `1.4` |
| `dockerImageCli.pullPolicy`   | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `nmapJar.xmx`                 | Value for java -Xmx memory settings | `1G` |
| `nmapJar.path`                | The directory where the Network Map Service `.jar` file is stored | `bin` |
| `nmapJar.configPath`          | The directory where the Network Map Service configuration is stored | `etc` |
| `database.driverClassName`    | Network Map Service database connection details | `org.h2.Driver` |
| `database.jdbcDriver`         | Network Map Service database connection details | `""`
| `database.url`                | Network Map Service database connection details | `jdbc:h2:file:./h2/networkmap-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0` |
| `database.user`               | Network Map Service database connection details | `example-db-user` |
| `database.password`           | Network Map Service database connection details | `example-db-password` |
| `database.runMigration`       | Network Map Service database connection details | `true` |
| `checkRevocation`             | Flag indicating whether or not the certificate revocation list status check should be performed | `true` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `authPort`                    | Auth Service port | `8081` |
| `networkRootTruststore.path`  | Path of the network trust store file | `DATA/trust-stores/network-root-truststore.jks` |
| `networkRootTruststore.password` | Password of the network trust store file | `trust-store-password` |
| `rootAlias`                   | The alias for the root certificate within the trust store | `cordarootca` |
| `logsContainersEnabled`       | Enable container displaying live logs | `true`
{{< /table >}}

For additional information on database connection details refer to the official documentation: [database documentation](../../../../cenm/1.4/config-database.md).
