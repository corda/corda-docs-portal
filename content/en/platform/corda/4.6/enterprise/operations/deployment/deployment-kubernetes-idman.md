---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes
    identifier: corda-enterprise-4-6-operations-guide-deployment-cenm-kubernetes-idman
tags:
- config
- kubernetes
title: CENM Identity Manager Helm chart
weight: 30
---

# CENM Identity Manager Helm Chart

This Helm chart is to configure, deploy, and run the CENM [Identity Manager Service](../../../../cenm/1.4/identity-manager.md) on Kubernetes.

## Example usage

The example below shows a command that triggers the Helm chart for the [Zone Service](../../../../cenm/1.4/zone-service.md):

```bash
helm install cenm-idman idman --set prefix=cenm --set acceptLicense=Y
```

The example below shows a command that specifies the size of the volume dedicated for logs:

```bash
helm install cenm-idman idman --set idmanPublicIP=X.X.X.X --set prefix=cenm --set acceptLicense=Y --set volumeSizeIdmanLogs=5Gi
```

## Configuration

{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Identity Manager Docker image used by the Identity Manager Service Helm chart | `acrcenm.azurecr.io/identitymanager/identitymanager` |
| `dockerImage.tag`             | Docker image Tag for the Docker image used by the Identity Manager Service Helm chart | `1.4` |
| `dockerImage.pullPolicy`      | Docker image pull policy for the Docker image used by the Identity Manager Service Helm chart. More info: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `dockerImageCli.name`            | URL to Identity Manager Docker image used by the CENM Command-Line (CLI) tool Helm chart | `acrcenm.azurecr.io/cli/cli` |
| `dockerImageCli.tag`             | Docker image Tag for the Docker image used by the CENM Command-Line (CLI) tool Helm chart | `1.4` |
| `dockerImageCli.pullPolicy`      | Docker image pull policy for the Docker image used by the CENM Command-Line (CLI) tool Helm chart. More info: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `volumeSizeIdmanEtc`          | Volume size for the `etc/` directory | `1Gi` |
| `volumeSizeIdmanLogs`         | Volume size for `logs/` directory | `10Gi` |
| `volumeSizeIdmanH2`           | Volume size for h2/ directory | `10Gi` |
| `database.driverClassName`    | Identity Manager database connection details | `org.h2.Driver` |
| `database.jdbcDriver`         | Identity Manager database connection details |  |
| `database.url`                | Identity Manager database connection details | `jdbc:h2:file:./h2/identity-manager-persistence;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0` |
| `database.user`               | Identity Manager database connection details | `example-db-user` |
| `database.password`           | Identity Manager database connection details | `example-db-password` |
| `database.runMigration`       | Identity Manager database connection details | `true` |
| `acceptLicense`               | Required parameter |  |
| `cordaJarMx`                  | Memory size allocated to the main Identity Manager Service container (in GB) | `1` |
| `idmanJar.xmx`                | Value for java `-Xmx` parameter | `1G` |
| `idmanJar.path`               | The directory where the Identity Manager Service `.jar` file is stored | `bin` |
| `idmanJar.configPath`         | The directory where the Identity Manager Service configuration is stored | `etc` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred | `120` |
| `authPort`                    | Auth Service port | `8081` |
| `serviceRevocation.port`      | Kubernetes service port to access Identity Manager's revocation endpoint (targetPort) | `5053` |
| `logsContainersEnabled`       | Defines whether the container displaying live logs is enabled or disabled | `true` |
{{< /table >}}

For additional information on database connection details refer to the official documentation: [database documentation](../../../../cenm/1.4/config-database.md).
