# CENM Notary Helm Chart

This Helm chart is to configure, deploy and run a Corda Notary.

## Example usage

Using default values:

```bash
helm install notary notary
```

Overwriting default values:

```bash
helm install notary notary --set shell.password="superDifficultPassword"
```

## Configuration

| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Notary Docker image                     | `acrcenm.azurecr.io/notary/notary` |
| `dockerImage.tag`             | Docker image Tag | `1.2` |
| `dockerImage.pullPolicy`      | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `service.type`                | Kubernetes service type, https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types | `LoadBalancer` |
| `service.port`                | Kubernetes service port/targetPort for external communication | `10000` |
| `serviceInternal.type`        | Kubernetes service type for internal communication between CENM components | `LoadBalancer` |
| `serviceInternal.port`        | Kubernetes service port/targetPort | `5052` |
| `serviceSsh.type`             | Kubernetes service type to access Notary ssh console | `LoadBalancer` |
| `shell.sshdPort`              | Notary ssh port | `2222` |
| `shell.user`                  | Notary ssh user | `notary` |
| `shell.password`              | Notary ssh password | `notaryP` |
| `dataSourceProperties.dataSource.password`    | Notary database connection details | `ziAscD0MJnj4n4xkFWY6XuMBuw9bvYC7` |
| `dataSourceProperties.dataSource.url`    | Notary database connection details | `jdbc:h2:file:./h2/notary-persistence;DB_CLOSE_ON_EXIT=FALSE;WRITE_DELAY=0;LOCK_TIMEOUT=10000` |
| `dataSourceProperties.dataSource.user`               | Notary database connection details | `sa` |
| `dataSourceProperties.dataSource.dataSourceClassName`   | Notary database connection details | `org.h2.jdbcx.JdbcDataSource` |
| `cordaJarMx`                  | Initial value for memory allocation (GB) | `1` |
| `jarPath`                     | Path to a folder which contains Notary jar files | `bin` |
| `configPath`                  | Path to a folder which contains Notary configuration file | `etc` |

For additional information on database connection details refer to the [Corda database documentation](../../corda-os/4.4/corda-configuration-file.md#configuration-file-fields).
