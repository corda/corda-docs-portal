---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Notary Helm chart
weight: 300
---

# CENM Notary Helm Chart

This Helm chart is to configure, deploy, and run a Corda Notary on Kubernetes.

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-notary notary --set notaryPublicIP=X.X.X.X --set prefix=cenm --set mpv=4 --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-notary notary --set notaryPublicIP=X.X.X.X --set prefix=cenm --set mpv=4 --set acceptLicense=Y --set volumeSizeNotaryLogs=20Gi
```

## Configuration

{{< table >}}
| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Notary Docker image                     | `acrcenm.azurecr.io/notary/notary` |
| `dockerImage.tag`             | Docker image Tag | `1.2` |
| `dockerImage.pullPolicy`      | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `volumeSizeNotaryBin`         | Volume size for the `bin/` directory                     | `2Gi` |
| `volumeSizeNotaryEtc`         | Volume size for the `etc/` directory                     | `10Mi` |
| `volumeSizeNotaryNodeinfo`    | Volume size for the `nodeinfo/` directory                | `1Mi` |
| `volumeSizeNotaryCertificate` | Volume size for the `certificate/` directory             | `5Mi` |
| `volumeSizeNotaryLogs`        | Volume size for the `notary/` directory                  | `10Gi` |
| `volumeSizeNotaryH2`          | Volume size for the `h2/` directory                      | `1Mi` |
| `p2pPort`                     | P2P port used to communicate with Corda nodes            | `10002` |
| `cordaJarMx`                  | Initial value for memory allocation (GB)                 | `3` |
| `devMode`                     | Flag to run the Notary in development mode               | `false` |
| `sshdPort`                    | SSH port for Notary                                      | `2222` |
| `jarPath`                     | Path to a folder which contains Notary `.jar` files      | `bin` |
| `configPath`                  | Path to a folder which contains Notary configuration file | `etc` |
| `sleepTimeAfterError`         | Sleep time (in seconds) after an error occurred          | `120` |
| `jksSource`                   | URL where the network-root-truststore.jks is or would be available from | `""` |
| `networkServices.doormanURL`  | URL for the Identity Manager Service (formerly Doorman)              | `idman-ip:10000` |
| `networkServices.networkMapURL` | URL for the Network Map Service                        | `nmap:10000` |
| `mpv`                         | Minimum platform version                                 | `3` |
| `dataSourceProperties.dataSource.password`    | Notary database connection details       | `ziAscD0MJnj4n4xkFWY6XuMBuw9bvYC7` |
| `dataSourceProperties.dataSource.url`    | Notary database connection details            | `jdbc:h2:file:./h2/notary-persistence;DB_CLOSE_ON_EXIT=FALSE;WRITE_DELAY=0;LOCK_TIMEOUT=10000` |
| `dataSourceProperties.dataSource.user`               | Notary database connection details | `sa` |
| `dataSourceProperties.dataSource.dataSourceClassName`   | Notary database connection details | `org.h2.jdbcx.JdbcDataSource` |
| `notary.validating`           | Type of Notary                                           | `false` |
| `rpcSettingsAddress`          | RPC settings for Notary                                  | `0.0.0.0` |
| `rpcSettingsAddressPort`      | RPC settings for Notary                                  | `10003` |
| `rpcSettingsAdminAddress`     | RPC settings for Notary                                  | `localhost` |
| `rpcSettingsAdminAddressPort` | RPC settings for Notary                                  | `10770` |
| `rpcSettingsStandAloneBroker` | RPC settings for Notary                                  | `false` |
| `rpcSettingsUseSsl`           | RPC settings for Notary                                  | `false` |
| `rpcUsers.username`           | Username for the built-in SSH service                    | `notary` |
| `rpcUsers.password`           | Password for the built-in SSH service                    | `notaryP` |
{{< /table >}}

For additional information on database connection details refer to the [Corda database documentation](../../corda-os/4.4/corda-configuration-file.md#configuration-file-fields).
