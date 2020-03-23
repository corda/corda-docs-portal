# CENM Network Map Helm Chart

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

| Parameter                     | Description                                              | Default value         |
| ----------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                   | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`            | URL to Network Map Docker image                     | `acrcenm.azurecr.io/nmap/nmap` |
| `dockerImage.tag`             | Docker image tag | `1.2` |
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

For additional information on database connection details refer to the official documentation: [database documentation](config-database.md).
