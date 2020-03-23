# CENM Identity Manager Helm Chart

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

| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Identity Manager Docker image                     | `acrcenm.azurecr.io/idman/idman` |
| `dockerImage.tag`             | Docker image Tag | `1.2` |
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
| `cordaJarMx`                  | Initial value for memory allocation | `1` |
| `jarPath`                     | Path to a folder which contains Identity Manager jar files | `bin` |
| `configPath`                  | Path to a folder which contains Identity Manager configuration file | `etc` |

For additional information on database connection details refer to the official documentation: [database documentation](config-database.md).
