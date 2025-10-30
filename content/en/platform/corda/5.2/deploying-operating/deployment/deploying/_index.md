---
description: "Learn how to deploy Corda 5."
date: '2023-05-11'
title: "Deploying"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-deploying
    weight: 2000
---
# Deploying

This page describes how to deploy Corda 5. All the necessary [prerequisites]({{< relref "../prerequisites.md" >}}) must have been satisfied before Corda is deployed.
In particular, PostgreSQL and {{< tooltip >}}Kafka{{< /tooltip >}} must be running. The mechanism to achieve that is up to you. For example, you can:

* run PostgreSQL and Kafka on {{< tooltip >}}Kubernetes{{< /tooltip >}}.
* use a managed service such as Amazon RDS for PostgreSQL, Amazon Managed Streaming for Apache Kafka, or Confluent Cloud.

This section contains the following:

* [Download and Push Container Images to a Registry]({{< relref "#download-and-push-container-images-to-a-registry">}})
* [Download the Corda Helm Chart]({{< relref "#download-the-corda-helm-chart">}})
* [Configure the Deployment]({{< relref "#configure-the-deployment">}})
* [Install the Corda Helm Chart]({{< relref "#install-the-corda-helm-chart">}})

## Download and Push Container Images to a Registry

The Corda container images must be in a registry that is accessible from the Kubernetes cluster in which Corda will run.
For more information, see the following sections:

* [Container Images for Corda]({{< relref "#container-images-for-corda" >}})
* [Container Images for Corda Enterprise]({{< relref "#container-images-for-corda-enterprise" >}})

### Container Images for Corda

The Corda images are available from Docker Hub.

### Container Images for Corda Enterprise {{< enterprise-icon >}}

To push the Corda Enterprise images:

1. Download `corda-ent-worker-images-{{<version-num>}}.0.tar.gz` from the [R3 Customer Hub](https://r3.force.com/).

2. Inflate and load the `corda-ent-worker-images-{{<version-num>}}.0.tar.gz` file into the local Docker engine with the following command:

   ```shell
   docker load -i corda-ent-worker-images-{{<version-num>}}.0.tar.gz
   ```

3. Retag each image using the name of the registry to be used and push the image. The following is an example script to automate this. It takes the target container registry as an argument. If the target registry requires authentication, you must perform a `docker login` against the registry before running the script.

   ```shell
   #!/bin/bash
   if [ -z "$1" ]; then
    echo "Specify target registry"
    exit 1
   fi

   declare -a images=(
    "corda-ent-rest-worker" "corda-ent-flow-worker"
    "corda-ent-member-worker" "corda-ent-p2p-gateway-worker"
    "corda-ent-p2p-link-manager-worker" "corda-ent-db-worker"
    "corda-ent-flow-mapper-worker" "corda-ent-verification-worker"
    "corda-ent-persistence-worker" "corda-ent-token-selection-worker"
    "corda-ent-crypto-worker" "corda-ent-uniqueness-worker"
    "corda-ent-plugins" )
   tag={{<version-num>}}.0.0
   target_registry=$1

   for image in "${images[@]}"; do
    source=corda/$image:$tag
    target=$target_registry/$image:$tag
    echo "Publishing image $source to $target"
    docker tag $source $target
    docker push $target
   done

   docker tag postgres:14.10 $target_registry/postgres:14.10
   docker push $target_registry/postgres:14.10
   docker tag 53c87e38a209 $target_registry/ingress-nginx-controller:v1.9.3
   docker push $target_registry/ingress-nginx-controller:v1.9.3
   ```

## Download the Corda Helm Chart

The following sections describe how to download the Corda {{< tooltip >}}Helm{{< /tooltip >}} chart:

* [Corda Helm chart]({{< relref "#corda-helm-chart" >}})
* [Corda Enterprise Helm chart]({{< relref "#corda-enterprise-helm-chart" >}})

### Corda Helm chart

You can download the Corda Helm chart from Docker Hub using the following command:

```shell
helm fetch oci://registry-1.docker.io/corda/corda --version {{<version-num>}}.0
```
### Corda Enterprise Helm chart {{< enterprise-icon >}}

You can download the `corda-enterprise-{{<version-num>}}.0.tgz` file from the the [R3 Customer Hub](https://r3.force.com/).

## Configure the Deployment

For each deployment, you should create a YAML file to define a set of Helm overrides to be used for that environment.
The following sections describe the minimal set of configuration options required for a deployment:

* [Image Registry]({{< relref "#image-registry" >}})
* [Replica Counts]({{< relref "#replica-counts" >}})
* [Token Selection Worker Sharding]({{< relref "#token-selection-worker-sharding" >}})
* [Resource Requests and Limits]({{< relref "#resource-requests-and-limits" >}})
* [REST API]({{< relref "#rest-api" >}})
* [P2P Gateway]({{< relref "#p2p-gateway" >}})
* [PostgreSQL]({{< relref "#postgresql" >}})
* [Kafka Message Bus]({{< relref "#kafka-message-bus" >}})
* [Encryption]({{< relref "#encryption" >}})
* [Bootstrapping]({{< relref "#bootstrapping" >}})
* [Worker Pods]({{< relref "#worker-pods" >}})
* [Node Affinities]({{< relref "#node-affinities" >}})
* [Ledger Repair]({{< relref "#ledger-repair" >}})
* [Pre-Install Checks]({{< relref "#pre-install-checks" >}})

You can extract a README containing the full set of options from the Helm chart using the following command:

```shell
helm show readme <HELM-CHART-TGZ-FILE>
```

You can extract a YAML file containing all of the default values using the following command:

```shell
helm show values <HELM-CHART-TGZ-FILE>
```

You can also view an [example configuration](#example-configuration).

### Image Registry

If you are not using the Corda container images from Docker Hub, define overrides specifying the name of the container registry to which you pushed the Corda, PostgreSQL, and NGINX Ingress Controller images:

```yaml
image:
  registry: <REGISTRY-NAME>
bootstrap:
  db:
    clientImage:
      registry: <REGISTRY-NAME>
workers:
  tokenSelection:
    sharding:
      image:
        registry: <REGISTRY-NAME>
        repository: "ingress-nginx-controller"
        tag: "v1.9.3"
```

If the registry requires authentication, create a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#docker-config-secrets) containing the container registry credentials, in the Kubernetes namespace where Corda is to be deployed. Specify an override with the name of the Kubernetes secret:

```yaml
imagePullSecrets:
  - <IMAGE-PULL-SECRET-NAME>
```

### Replica Counts

R3 suggest the following number of replicas for each type of worker:

* Database: 2
* Flow: 6
* All other types of workers: 3

For example:

```yaml
workers:
  crypto:
    replicaCount: 3
  db:
    replicaCount: 2
  flow:
    replicaCount: 6
  flowMapper:
    replicaCount: 3
  verification:
    replicaCount: 3
  membership:
    replicaCount: 3
  rest:
    replicaCount: 3
  p2pGateway:
    replicaCount: 3
  p2pLinkManager:
    replicaCount: 3
  persistence:
    replicaCount: 3
  tokenSelection:
    replicaCount: 3
  uniqueness:
    replicaCount: 3
```

{{< important >}}
These numbers are only suggestions and you should make your own decisions about scaling depending on your application workload.
{{< /important >}}

### Token Selection Worker Sharding

Where high throughput requires multiple token selection workers, sharding tokens across them can improve performance by making more efficient use of the cache. Setting `workers.tokenSelection.sharding.enabled` to `true` deploys NGINX in front of these workers. The `workers.tokenSelection.sharding.replicaCount` specifies the number of NGINX instances to deploy.

For high availability, starting with three replicas is a reasonable choice, with adjustments made as needed to address resource contention. However, the number of NGINX instances does not need to match the number of token selection workers. Typically, the `workers.tokenSelection.replicaCount` will be higher than the `workers.tokenSelection.sharding.replicaCount`.

For example:

```yaml
workers:
  tokenSelection:
    sharding:
      enabled: true
      replicaCount: 3
```


### Resource Requests and Limits

Specify a default set of resource requests and limits for the Corda containers. R3 recommends the following as a starting point:

```yaml
resources:
  requests:
    memory: 1500Mi
    cpu: 1000m
  limits:
    memory: 3000Mi
    cpu: 2000m
```
{{< note >}}
It is particularly important to specify resource requests when using a Kubernetes cluster with autoscaling, to ensure that it scales appropriately when the Corda cluster is deployed.
{{< /note >}}

You can also override the default resource requests and limits separately for each type of Corda worker.
For example, R3 recommends starting with higher memory limits for the database and flow workers:

```yaml
workers:
  db:
    resources:
      requests:
        memory: 2048Mi
      limits:
        memory: 2048Mi
  flow:
    resources:
      requests:
        memory: 2048Mi
      limits:
        memory: 2048Mi
```

As with the number of replicas, you may need to adjust these values based on testing with your actual application workload.

### REST API

The following configuration options are available for the [REST API]({{< relref "../../../reference/rest-api/_index.md" >}}):

* [Expose the REST API]({{< relref "#expose-the-rest-api" >}})
* [Install the REST Worker Certificate]({{< relref "#install-the-rest-worker-certificate" >}})

#### Expose the REST API

By default, the REST API is exposed on an internal Kubernetes service.
To enable access from outside the Kubernetes cluster, use one of the following:

* [Kubernetes Ingress](#kubernetes-ingress)
* [External Load Balancer](#external-load-balancer)

##### Kubernetes Ingress

R3 recommends configuring [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to provide the REST worker with HTTP load balancing.
For example, to use an [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/) deployed with the class name `nginx`:

```yaml
workers:
  rest:
    ingress:
      # optional annotations for the REST worker ingress
      annotations: {}
      # optional className for the REST worker ingress
      className: "nginx"
      # required hosts for the REST worker ingress
      hosts:
      - api.corda.example.com
```

The optional annotations enable additional integrations, such as [ExternalDNS](https://github.com/kubernetes-sigs/external-dns) or [cert-manager](https://cert-manager.io/).

##### External Load Balancer

Alternatively, the REST API service can be fronted directly by an external load balancer. The Helm chart allows annotations to be specified to
facilitate the creation of a load balancer by a cloud-platform specific controller.
For example, the following configuration specifies that the [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html)
fronts the REST API with a Network Load Balancer internal to the Virtual Private Cloud (VPC):

```yaml
workers:
  rest:
    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-scheme: internal
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        external-dns.beta.kubernetes.io/hostname: api.corda.example.com
```

The full set of service annotations available for the AWS Load Balancer Controller can be found in the controller's [documentation](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.6/guide/service/annotations/).

#### Install the REST Worker Certificate

The REST worker {{< tooltip >}}TLS{{< /tooltip >}} certificate is presented to a client any time a HTTPS connection is made.
If no specific parameters are provided, a self-signed certificate is used and the connection to the {{< tooltip >}}REST Worker{{< /tooltip >}} is always HTTPS. However, a warning will be emitted into the REST worker log explaining how to provide parameters for custom TLS certificates.
The following is required to install a valid TLS certificate:

* The TLS certificate itself must be signed by a Certification Authority ({{< tooltip >}}CA{{< /tooltip >}}) or an intermediary.
* A private key corresponding to the public key included in the TLS certificate.
* The Certification Chain must lead up to the CA.

{{< note >}}
If you configure the REST worker to use a trusted certificate, `-k` should be removed from the example curl commands given throughout this documentation.
{{< /note >}}

Custom certificate information can be provided in {{< tooltip >}}PEM{{< /tooltip >}} format as a Kubernetes secret.
You can either create a Kubernetes secret manually to hold the certificate information or allow Helm to generate a new secret.
You can specify the secret name manually as follows:

```yaml
workers:
  rest:
     tls:
      secretName: <PEM_TLS_CERT_SECRET_NAME>
```

If this optional value is not provided, Helm generates the certificate data at installation time and automatically creates a Kubernetes secret for the REST worker to use.

{{< note >}}
If the secret data is modified, the REST worker pod will not currently detect the change until the pod is restarted.
{{</ note >}}

### P2P Gateway

You can configure [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) to provide the P2P gateway worker with HTTP load balancing.

{{< note >}}

* Kubernetes Ingress makes the P2P gateway accessible from outside the Kubernetes cluster that the Corda cluster is deployed into. Your organization must own the domain name (`gateway.corda.example.com` in the example below) and that must resolve to the IP address of the Ingress-managed load balancer. The Network Operator must use one of the Ingress hosts when [registering a Member]({{< relref "../../../application-networks/creating/members/cpi.md#set-variables">}}) or [registering the MGM]({{< relref "../../../application-networks/creating/mgm/cpi.md#set-variables">}}).
* The gateway only supports TLS termination in the gateway and not inside the load balancer itself.
{{< /note >}}

R3 recommends using the [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/). For example:

```yaml
workers:
  p2pGateway:
    ingress:
      className: "nginx"
      hosts:
        - "gateway.corda.example.com"
      annotations:
        nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
        nginx.ingress.kubernetes.io/ssl-passthrough: "true"
        nginx.ingress.kubernetes.io/ssl-redirect: "true"
```

See the controller's [documentation](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/) for further details of the available annotations.

### PostgreSQL

The following configuration is required for the Corda databases:

* [Cluster Database](#cluster-database)
* [State Manager Databases](#state-manager-databases)

Corda supports using multiple databases in isolation to spread the load and improve horizontal scalability.
All databases must be defined only once within the deployment configuration and any dependant component can simply reference the database by `id`. This greatly simplifies maintenance and reduces redundant information.

{{< note >}}
A database with an `id` set as `default` is always mandatory. Corda uses this database if nothing else is configured.
{{< /note >}}

#### Cluster Database

The following Corda workers require access to the cluster database, and credentials must be specified for each one independently.

* Crypto Workers
* Database Workers
* Persistence Workers
* Token Selection Workers
* Uniqueness Workers

By default, Corda expects a database named `cordacluster`, but you can override this, as follows:

```yaml
databases:
  - id: "default"
    host: <POSTGRESQL_HOST1>
    name: <POSTGRESQL_CLUSTER_DATABASE_NAME>
    port: 5432
    type: "postgresql"
```

Credentials must be specified for each worker that requires access to the cluster database:

```yaml
workers:
  crypto:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_CRYPTO_WORKER_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_CRYPTO_WORKER_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_CRYPTO_WORKER_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_CRYPTO_WORKER_PASSWORD_SECRET_NAME>
  db:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_DB_WORKER_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_DB_WORKER_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_DB_WORKER_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_DB_WORKER_PASSWORD_SECRET_NAME>
  persistence:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_PERSISTENCE_WORKER_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_PERSISTENCE_WORKER_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_PERSISTENCE_WORKER_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_PERSISTENCE_WORKER_PASSWORD_SECRET_NAME>
  tokenSelection:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_TOKEN_SELECTION_WORKER_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_TOKEN_SELECTION_WORKER_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_TOKEN_SELECTION_WORKER_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_TOKEN_SELECTION_WORKER_PASSWORD_SECRET_NAME>
  uniqueness:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_UNIQUENESS_WORKER_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_UNIQUENESS_WORKER_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_UNIQUENESS_WORKER_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_UNIQUENESS_WORKER_PASSWORD_SECRET_NAME>
```

Note that, as elsewhere, credentials can be specified directly as part of the overrides using `value` instead of `valueFrom`:

```yaml
username:
  value: <USERNAME>
password:
  value: <USERNAME>
```

{{< note >}}
Although the password can be specified directly as a Helm override, R3 does not recommend this for security reasons.
Similarly, although all Corda workers can share the same set of credentials, R3 recommends you create a Kubernetes Secret per Corda worker containing the credentials.
{{< /note >}}

If required, the connection pool used when interacting with the database can also be independently configured at the `config` level within each worker, as an example:

```yaml
workers:
  crypto:
    config:
      connectionPool:
        minSize: <MIN_CONNECTION_POOL_SIZE>
        maxSize: <MAX_CONNECTION_POOL_SIZE>
        maxLifetimeSeconds: <MAX_CONNECTION_POOL_LIFE_TIME_SECONDS>
        idleTimeoutSeconds: <MAX_CONNECTION_POOL_IDLE_TIMEOUT_SECONDS>
        keepAliveTimeSeconds: <MAX_CONNECTION_POOL_KEEP_ALIVE_TIME_SECONDS>
        validationTimeoutSeconds: <MAX_CONNECTION_POOL_VALIDATION_TIME_OUT_SECONDS>
```

#### State Manager Databases

Corda requires one or more PostgreSQL database instances for persisting different state types. These are referred to as state manager databases.
Multiple Corda workers use, and sometimes share, these database instances and so, to improve both performance and scalability, R3 recommends deploying separate and isolated instances for each state type.
If not possible due to cost restrictions, consider at least isolating the following state types in production environments:

* Flow Mapping
* Flow Checkpoints
* Token Pool Cache (if [Token Selection Services]({{< relref "../../../developing-applications/api/ledger/utxo-ledger/token-selection/_index.md" >}}) are used)

The following table shows the relationship between Corda workers and state types and with the access type required by each one:

| <div style="width:100px">State Type </div> | <div style="width:100px">Worker Name </div> | <div style="width:100px">Access Type </div> | <div style="width:100px">Default Schema </div> |
|--------------------------------------------|---------------------------------------------|---------------------------------------------|------------------------------------------------|
| `flowCheckpoint`                           | `flow`                                      | READ/WRITE                                  | `sm_flow_checkpoint`                           |
| `flowMapping`                              | `flowMapper`                                | READ/WRITE                                  | `sm_flow_mapping`                              |
| `flowStatus`                               | `rest`                                      | READ/WRITE                                  | `sm_flow_status`                               |
| `keyRotation`                              | `rest`                                      | READ                                        | `sm_key_rotation`                              |
| `keyRotation`                              | `crypto`                                    | READ/WRITE                                  | `sm_key_rotation`                              |
| `p2pSession`                               | `p2pLinkManager`                            | READ/WRITE                                  | `sm_p2p_session`                               |
| `tokenPoolCache`                           | `tokenSelection`                            | READ/WRITE                                  | `sm_token_pool_cache`                          |

{{< note >}}
If you do not configure isolated state manager databases, by default, Corda deploys all of them to the `default` cluster database. R3 does not recommend this for production environments.
{{< /note >}}

Similarly to the cluster database, the configuration for these state manager database instances is defined using a combination of the `database` and `stateManager` sections.

{{< note >}}
The state manager partition values can contain only letters, underscores, and digits and must begin with a letter.
{{< /note >}}

The following is a full example of how to keep the cluster database and all of the state manager databases completely isolated from each other:

```yaml
databases:
  - id: "default"
    host: <POSTGRESQL_CLUSTER_DATABASE_HOST>
    name: <POSTGRESQL_CLUSTER_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "flow-checkpoint-state-manager"
    host: <POSTGRESQL_FLOW_CHECKPOINT_DATABASE_HOST>
    name: <POSTGRESQL_FLOW_CHECKPOINT_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "flow-mapping-state-manager"
    host: <POSTGRESQL_FLOW_MAPPING_DATABASE_HOST>
    name: <POSTGRESQL_FLOW_MAPPING_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "flow-status-state-manager"
    host: <POSTGRESQL_FLOW_STATUS_DATABASE_HOST>
    name: <POSTGRESQL_FLOW_STATUS_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "key-rotation-state-manager"
    host: <POSTGRESQL_KEY_ROTATION_DATABASE_HOST>
    name: <POSTGRESQL_KEY_ROTATION_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "p2p-session-state-manager"
    host: <POSTGRESQL_P2P_SESSION_DATABASE_HOST>
    name: <POSTGRESQL_P2P_SESSION_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "token-pool-cache-state-manager"
    host: <POSTGRESQL_TOKEN_POOL_CACHE_DATABASE_HOST>
    name: <POSTGRESQL_TOKEN_POOL_CACHE_DATABASE_NAME>
    port: 5432
    type: "postgresql"

stateManager:
  flowCheckpoint:
    type: Database
    storageId: "flow-checkpoint-state-manager"
    partition: "sm_flow_checkpoint"
  flowMapping:
    type: Database
    storageId: "flow-mapping-state-manager"
    partition: "sm_flow_mapping"
  flowStatus:
    type: Database
    storageId: "flow-status-state-manager"
    partition: "sm_flow_status"
  keyRotation:
    type: Database
    storageId: "key-rotation-state-manager"
    partition: "sm_key_rotation"
  p2pSession:
    type: Database
    storageId: "p2p-session-state-manager"
    partition: "sm_p2p_session"
  tokenPoolCache:
    type: Database
    storageId: "token-pool-cache-state-manager"
    partition: "sm_token_pool_cache"
```

In contrast to the above, and only recommended for development environments, the following example shows how a single database instance can be used for the cluster and another database instance, isolated, can be used for all state manager state types.

```yaml
databases:
  - id: "default"
    host: <POSTGRESQL_CLUSTER_DATABASE_HOST>
    name: <POSTGRESQL_CLUSTER_DATABASE_NAME>
    port: 5432
    type: "postgresql"
  - id: "state-manager"
    host: <POSTGRESQL_STATE_MANAGER_DATABASE_HOST>
    name: <POSTGRESQL_STATE_MANAGER_DATABASE_NAME>
    port: 5432
    type: "postgresql"

stateManager:
  flowCheckpoint:
    type: Database
    storageId: "state-manager"
  flowMapping:
    type: Database
    storageId: "state-manager"
  flowStatus:
    type: Database
    storageId: "state-manager"
  keyRotation:
    type: Database
    storageId: "state-manager"
  p2pSession:
    type: Database
    storageId: "state-manager"
  tokenPoolCache:
    type: Database
    storageId: "state-manager"
```
Even if state types share a database instance, each state type must define its own user and these users must not be the same as the `config` users. For example:

```yaml
workers:
  crypto:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_CRYPTO_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_CRYPTO_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_CRYPTO_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_CRYPTO_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      keyRotation:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_CRYPTO_KEY_ROTATION_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_CRYPTO_KEY_ROTATION_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_CRYPTO_KEY_ROTATION_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_CRYPTO_KEY_ROTATION_STATEMANAGER_PASSWORD_SECRET_NAME>
  flow:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_FLOW_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_FLOW_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_FLOW_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_FLOW_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      flowCheckpoint:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_CHECKPOINT_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_FLOW_CHECKPOINT_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_CHECKPOINT_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_FLOW_CHECKPOINT_STATEMANAGER_PASSWORD_SECRET_NAME>
  flowMapper:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_FLOW_MAPPER_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_FLOW_MAPPER_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_FLOW_MAPPER_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_FLOW_MAPPER_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      flowMapping:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_MAPPER_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_FLOW_MAPPER_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_MAPPER_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_FLOW_MAPPER_STATEMANAGER_PASSWORD_SECRET_NAME>
  p2pLinkManager:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_P2P_SESSION_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_P2P_SESSION_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_P2P_SESSION_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_P2P_SESSION_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      p2pSession:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_P2P_SESSION_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_P2P_SESSION_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_P2P_SESSION_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_P2P_SESSION_STATEMANAGER_PASSWORD_SECRET_NAME>
  tokenSelection:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_TOKEN_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_TOKEN_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_TOKEN_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_TOKEN_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      tokenPoolCache:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_TOKEN_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_TOKEN_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_TOKEN_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_TOKEN_STATEMANAGER_PASSWORD_SECRET_NAME>
  rest:
    config:
      username:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_REST_WORKER_CONFIG_USERNAME_SECRET_KEY>
            name: <POSTGRESQL_REST_WORKER_CONFIG_USERNAME_SECRET_NAME>
      password:
        valueFrom:
          secretKeyRef:
            key: <POSTGRESQL_REST_WORKER_CONFIG_PASSWORD_SECRET_KEY>
            name: <POSTGRESQL_REST_WORKER_CONFIG_PASSWORD_SECRET_NAME>
    stateManager:
      keyRotation:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_KEY_ROTATION_REST_WORKER_STATEMANAGER_USERNAME_SECRET_KEY>
              name: <POSTGRESQL_KEY_ROTATION_REST_WORKER_STATEMANAGER_USERNAME_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_KEY_ROTATION_REST_WORKER_STATEMANAGER_PASSWORD_SECRET_KEY>
              name: <POSTGRESQL_KEY_ROTATION_REST_WORKER_STATEMANAGER_PASSWORD_SECRET_NAME>
      flowStatus:
        username:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_STATUS_USERNAME_STATEMANAGER_SECRET_KEY>
              name: <POSTGRESQL_FLOW_STATUS_USERNAME_STATEMANAGER_SECRET_NAME>
        password:
          valueFrom:
            secretKeyRef:
              key: <POSTGRESQL_FLOW_STATUS_PASSWORD_STATEMANAGER_SECRET_KEY>
              name: <POSTGRESQL_FLOW_STATUS_PASSWORD_STATEMANAGER_SECRET_NAME>
```

Note that, as elsewhere, credentials can be specified directly as part of the overrides using `value` instead of `valueFrom`:

```yaml
username:
  value: <USERNAME>
password:
  value: <USERNAME>
```

{{< note >}}
Although the password can be specified directly as a Helm override, R3 does not recommend this for security reasons.
Similarly, R3 recommends that you create a Kubernetes Secret per Corda worker containing the credentials.
{{< /note >}}

If required, the connection pool used when interacting with the database can be independently configured for each state type within each worker. For example:

```yaml
workers:
  rest:
    stateManager:
      keyRotation:
        connectionPool:
          minSize: <MIN_CONNECTION_POOL_SIZE>
          maxSize: <MAX_CONNECTION_POOL_SIZE>
          maxLifetimeSeconds: <MAX_CONNECTION_POOL_LIFE_TIME_SECONDS>
          idleTimeoutSeconds: <MAX_CONNECTION_POOL_IDLE_TIMEOUT_SECONDS>
          keepAliveTimeSeconds: <MAX_CONNECTION_POOL_KEEP_ALIVE_TIME_SECONDS>
          validationTimeoutSeconds: <MAX_CONNECTION_POOL_VALIDATION_TIME_OUT_SECONDS>
```

### Kafka Message Bus

Specify the Kafka bootstrap servers as a comma-separated list:

```yaml
kafka:
  bootstrapServers: <KAFKA_BOOTSTRAP_SERVERS>
```

If desired, a prefix can be applied to all of the Kafka topics used by the Corda deployment. This enables multiple Corda clusters to share a Kafka cluster. For example:

```yaml
kafka:
  topicPrefix: <KAFKA_TOPIC_PREFIX>
```

Enable TLS if required by the Kafka client protocol:

```yaml
kafka:
  tls:
    enabled: true
```

If the broker certificate is self-signed or cannot be trusted for some other reason, create a Kubernetes secret containing the client {{< tooltip >}}trust store{{< /tooltip >}}. The trust store can be in PEM or {{< tooltip >}}JKS{{< /tooltip >}} format. If JKS format is used, you can supply a password for the trust store. The following example is for a trust store in PEM format stored against the `ca.crt` key in the Kubernetes secret:

```yaml
kafka:
  tls:
    truststore:
      valueFrom:
        secretKeyRef:
          name: <TRUST-STORE-SECRET-NAME>
          key: "ca.crt"
      type: "PEM"
```

Corda supports SASL for Kafka authentication. If your Kafka instance requires SASL authentication, enable the option in the overrides along with the required mechanism:

```yaml
kafka:
  sasl:
    enabled: true
    mechanism: "SCRAM-SHA-512"
```

A single set of credentials can be specified for use everywhere by reference to a Kubernetes secret containing the username and password:

```yaml
kafka:
  sasl:
    username:
      valueFrom:
        secretKeyRef:
          name: <SASL-SECRET-NAME>
          key: "username"
    password:
      valueFrom:
        secretKeyRef:
          name: <SASL-SECRET-NAME>
          key: "password"
```

Alternatively, for finer-grained access control, separate credentials can be specified for bootstrapping, and for each type of worker. For example:

```yaml
bootstrap:
  kafka:
    sasl:
      username:
        valueFrom:
          secretKeyRef:
            name: <SASL-SECRET-NAME>
            key: "bootstrap-username"
      password:
        valueFrom:
          secretKeyRef:
            name: <SASL-SECRET-NAME>
            key: "bootstrap-password"
workers:
  crypto:
    kafka:
      sasl:
        username:
          valueFrom:
            secretKeyRef:
              name: <SASL-SECRET-NAME>
              key: "crypto-username"
        password:
          valueFrom:
            secretKeyRef:
              name: <SASL-SECRET-NAME>
              key: "crypto-password"
```

Note that, here, as elsewhere, credentials can also be specified directly as part of the overrides using `value` instead of `valueFrom`.
For example:

```yaml
username:
  value: <USERNAME>
```

### Encryption

The Corda configuration system allows for any string configuration value to be marked as “secret”. This includes values passed dynamically using the REST API and also those defined in a manual deployment configuration. For more information see, [Configuration Secrets]({{< relref "../../config/secrets.md" >}}).

#### Default Secrets Service

The [Corda default secrets lookup service]({{< relref "../../config/secrets.md#default-secrets-service" >}}) uses a salt and passphrase specified in the deployment configuration. Specify these as follows:

```yaml
config:
   encryption:
      salt:
        valueFrom:
          secretKeyRef:
            name: <SALT_SECRET_NAME>
            key: <SALT_SECRET_KEY>
      passphrase:
        valueFrom:
          secretKeyRef:
            name: <PASSPHRASE_SECRET_NAME>
            key: <PASSPHRASE_SECRET_KEY>
```

#### External Secrets Service {{< enterprise-icon >}}

Corda Enterprise supports integration with HashiCorp Vault as an external secret management system. For more information, see [External Secrets Service]({{< relref "../../config/secrets.md#external-secrets-service" >}}) in the _Configuring Corda_ section.
To configure a Corda Enterprise deployment to connect to a running HashiCorp Vault instance, add the following:

```yaml
config:
  vault:
    url: "<vault-URL>"
    token: "<vault-token>"
    createdSecretPath: "<path-to-corda-created-secrets>"
```

* `<vault-URL>` — the full URL including the port at which the Vault instance is reachable, not including any path.
* `<vault-token>` — the token that Corda uses for accessing Vault. This must allow sufficient permissions to read from Vault at the Corda configured paths and also write to the `<path-to-corda-created-secrets>`. This requires your Vault administrator to grant more permissions than typically given to applications using Vault, but only for writing to one specific path. This is necessary to allow Corda to save encrypted database user passwords for the databases created for every new virtual node.

  The Vault token requires the following capabilities: `read`, `create`, `path`.
* `createdSecretPath` — the path on Vault where Corda writes new secrets. Secrets should be created at a point in the hierarchy that is specific to that particular Corda deployment, keeping keys for different Corda deployments separate.

R3 recommends injecting Vault secrets into Kubernetes pods using a sidecar technique. For more information, see the HashiCorp Vault Developer documentation. This provides a private channel for Corda worker containers to another container which in turn securely authenticates with Vault.

The passwords for the `RBAC` and `CRYPTO` schemas and `VNODES` database must be available in Vault before Corda is deployed. These must be available in the Vault path specified by `createdSecretPath`, under the keys `rbac`, `crypto`, and `vnodes` respectively.
{{< note >}}
These keys are not tied to the schema names. If the schema names change, the key names remain `rbac`, `crypto`, and `vnodes`.
{{< /note >}}
Additionally, a passphrase and salt for the Corda [wrapping keys]({{< relref "../../../key-concepts/cluster-admin/_index.md#key-management" >}}) must be added to the Vault `cryptosecrets` path under the keys `passphrase` and `salt` respectively.

### Bootstrapping

By default, the Helm chart automatically configures Kafka, PostgreSQL, and a default set of Corda RBAC roles as part of the deployment process.
If desired, each of these steps can be disabled and the necessary [configuration performed manually]({{< relref "manual-bootstrapping.md" >}}).

{{< note >}}
Bootstrap secrets are cleaned up automatically post-install with the exception of the `-rest-api-admin` secret. This secret should be manually deleted by the Administrator after retrieving the generated credentials.
{{< /note >}}

#### Kafka Topics

The Kafka bootstrapping creates the topics required by Corda.
If `kafka.topicPrefix` has been specified, the process uses this as a prefix for all of the topic names.
The bootstrap configuration enables the default number of topic partitions to be overridden.
You may need to increase this to support a larger number of Corda worker replicas.
It is also possible to override the default topic replica count; for example, if less than three Kafka brokers are available.
The following extract shows the default values:

```yaml
bootstrap:
  kafka:
    enabled: true
    partitions: 10
    replicas: 3
```

If SASL authentication is enabled, the bootstrapping also creates Access Control List (ACL) entries for producing and
consuming from the topics as appropriate for each worker.

#### Database

The database bootstrapping creates schemas in the cluster and state manager databases and populates them with the initial configuration. It is enabled by default:

```yaml
bootstrap:
  db:
    enabled: true
```
{{< note >}}
If you are deploying Corda Enterprise with HashiCorp Vault, you must disable automatic bootstrapping and manually configure the database. For more information, see the [Database]({{< relref "./manual-bootstrapping.md#database" >}}) section in the *Manual Bootstrapping* section.
{{< /note >}}

By default, the database bootstrapping uses the psql CLI from the Docker image `postgres:14.10` on Docker Hub.
If the Kubernetes cluster does not have access to Docker Hub, you must make this image available in an internal registry.
You can then specify the location of the image via overrides, as follows:

```yaml
db:
  clientImage:
    registry: <REGISTRY>
    repository: "postgres"
    tag: "14.10"
```

Part of the database bootstrapping involves populating the initial credentials for the REST API admin. You can specify these in one of the following ways:

* Pass the user name and password as Helm values:

  ```yaml
  bootstrap:
    restApiAdmin:
      username:
        value: <USERNAME>
      password:
        value: <PASSWORD>
  ```

* Leave the password field blank. A Kubernetes secret is created containing a generated password. The notes output
when the deployment completes contain instructions for how to retrieve this. This is the default behavior.

* Create a Kubernetes secret containing the user credentials:

  ```yaml
  bootstrap:
    restApiAdmin:
      username:
        valueFrom:
          secretKeyRef:
            name: <INITIAL_ADMIN_USER_SECRET_NAME>
            key: "username"
      password:
        valueFrom:
          secretKeyRef:
            name: <INITIAL_ADMIN_USER_SECRET_NAME>
            key: "password"
  ```

For security reasons, R3 recommends using separate bootstrap and runtime credentials for all databases. This is the default behaviour.
If required, you can change this at deployment time by overriding the Helm Chart values.

#### RBAC

The RBAC bootstrapping creates three default RBAC roles. It is enabled by default:

```yaml
bootstrap:
  rbac:
    enabled: true
```

For more information about these roles, see [Managing Roles and Permissions]({{< relref "../../config-users/managing-roles.md">}}).

### Service Accounts

If additional permissions are required, you can specify a service account for the Corda workers and bootstrap containers.

For example, when running with Red Hat OpenShift Container Platform, you must use a service account with the privileged security context constraint:

1. Create a file `sa.yaml` defining a custom service account bound to a role that provides the required security context constraint:

   ```yaml
   kind: ServiceAccount
   apiVersion: v1
   metadata:
     name: corda-privileged
   ---
   kind: Role
   apiVersion: rbac.authorization.k8s.io/v1
   metadata:
     name: corda-privileged
   rules:
     - verbs:
         - use
       apiGroups:
         - security.openshift.io
       resources:
         - securitycontextconstraints
       resourceNames:
         - privileged
   ---
   kind: RoleBinding
   apiVersion: rbac.authorization.k8s.io/v1
   metadata:
     name: corda-privileged
   subjects:
     - kind: ServiceAccount
       name: corda-privileged
   roleRef:
     apiGroup: rbac.authorization.k8s.io
     kind: Role
     name: corda-privileged
   ```

2. Create the service account, role, and role binding in the namespace where Corda is to be deployed:

   ```shell
   kubectl apply -f sa.yaml
   ```

3. In the configuration YAML for the Corda deployment, specify the service account to be used:

   ```yaml
   serviceAccount:
      name: "corda-privileged"
   bootstrap:
      serviceAccount:
        name: "corda-privileged"
   ```

### Worker Pods

The following configuration is possible for Corda worker pods:

* [Custom Annotations](#custom-annotations)
* [Istio Integration](#istio-integration)

#### Custom Annotations

You can define custom annotations for worker pods. You can add these globally or to individual workers. For example, to define `annotation-key-1` for all workers:

```yaml
annotations:
  annotation-key-1: "custom-value"
```

To define `annotation-key-2` for only the {{< tooltip >}}crypto worker{{< /tooltip >}}:

```yaml
workers:
  crypto:
    annotations:
      annotation-key-2: "some-value"
```

#### Istio Integration

You can integrate with Istio service mesh to secure communication between Corda workers. To enable this, add the following custom labels to worker pods:

```yaml
bootstrap:
  commonPodLabels:
    sidecar.istio.io/inject: !!str false # explicitly disable Istio integration from bootstrap pods
commonPodLabels:
  sidecar.istio.io/inject: !!str true # explicitly enable Istio integration for all Corda pods
```

### Ledger Repair

By default, the [Corda ledger repair functionality]({{< relref "../../../developing-applications/ledger/ledger-repair.md" >}}) runs every ten minutes. You can modify this schedule by adding the `net.corda.ledger.utxo.repair.schedulePeriod` system property to the Java options for each database worker. This property is set in seconds. For example, to modify the schedule to every 15 minutes:

```yaml
workers:
  db:
    javaOptions: "-XX:MaxRAMPercentage=75 -Dnet.corda.ledger.utxo.repair.schedulePeriod=900"
```

The window of transactions included in the repair process and the length of time the process can run for is defined by fields in the [corda.ledger.utxo configuration section]({{< relref "../../config/fields/ledger-utxo.md" >}}).

### Node Affinities

Corda uses node affinity to assign worker replicas across nodes. By default, for high availability, Corda attempts to deploy multiple replicas on different nodes. The following shows the default values:

```yaml
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app.kubernetes.io/component
              operator: In
              values:
              - membership-worker
          topologyKey: kubernetes.io/hostname
        weight: 1
```

### Pre-Install Checks

When deploying Corda, pre-install checks are performed automatically to check the configuration of Corda, to confirm that all of the [prerequisites]({{< relref "../prerequisites.md" >}}) are running and that the correct credentials and permissions are provided to install a running Corda cluster. The pre-install checks verify if:

* the resource limits have been assigned correctly.
* the PostgreSQL database is up and if the credentials work.
* Kafka is up and if the credentials work.

You can also run those checks manually using the Corda CLI <a href="../../reference/corda-cli/preinstall.html">`preinstall`</a>
command after you have deployed Corda.

If you want to disable the pre-install checks from running automatically (for example, to save time when testing the deployment), you can do it by adding the following property to your YAML file:

```yaml
bootstrap:
  preinstallCheck:
    enabled: false
```

If the pre-install checks fail (for example, if Kafka or PostgreSQL are not available), you can retrieve the logs for a single pod using `kubectl`. For more information on retrieving the logs, see the [Logs]({{< relref "../../observability/logs.md" >}}) section.

### Example Configuration

{{< warning >}}
The example in this section is included only for illustrative purposes. You must use the information provided to determine the correct configuration file for your environment.
{{< /warning >}}

The following example shows a complete configuration file for Corda deployment in an environment in which:
- the Cluster database is isolated from the State Manager database.
- all managed state types are stored within a single State Manager database.
- Kafka uses a trusted TLS certificate and SASL authentication is enabled.
- runtime credentials (unique per worker) to access cluster databases are automatically generated during deployment.
- runtime credentials (unique per worker and state type) to access state manager database are automatically generated during deployment.
- the REST API is exposed via an AWS Network Load Balancer, and the generated password for the initial admin user is retrieved from a secret.

```yaml
image:
  registry: "registry.example.com"

imagePullSecrets:
  - "registry-secret"

resources:
  requests:
    memory: 512Mi
    cpu: 250m
  limits:
    memory: 512Mi
    cpu: 2000m

serviceAccount:
  name: "corda-privileged"

databases:
  - id: "default"
    name: "cordacluster"
    port: 5432
    type: "postgresql"
    host: "postgres.example.com"
  - id: "state-manager"
    name: "statemanager"
    port: 5432
    type: "postgresql"
    host: "postgres-state-manager.example.com"

kafka:
  bootstrapServers: "kafka-1.example.com,kafka-2.example.com,kafka-3.example.com"
  tls:
    enabled: true
  sasl:
    enabled: true
    mechanism: "SCRAM-SHA-512"

bootstrap:
  db:
    clientImage:
      registry: "registry.example.com"
    databases:
      - id: "default"
        username:
          value: "user"
        password:
          valueFrom:
            secretKeyRef:
              key: "password"
              name: "postgres-secret"
      - id: "state-manager"
        username:
          value: "state-manager-user"
        password:
          valueFrom:
            secretKeyRef:
              key: "password"
              name: "state-manager-postgres-secret"
  kafka:
    sasl:
      username:
        value: "bootstrap"
      password:
        valueFrom:
          secretKeyRef:
            name: "kafka-credentials"
            key: "bootstrap"
  serviceAccount:
    name: "corda-privileged"

stateManager:
  flowCheckpoint:
    storageId: "state-manager"
  flowMapping:
    storageId: "state-manager"
  flowStatus:
    storageId: "state-manager"
  keyRotation:
    storageId: "state-manager"
  p2pSession:
    storageId: "state-manager"
  tokenPoolCache:
    storageId: "state-manager"

workers:
  crypto:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "crypto"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "crypto"
  db:
    replicaCount: 2
    resources:
      requests:
        memory: 2048Mi
      limits:
        memory: 2048Mi
    kafka:
      sasl:
        username:
          value: "db"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "db"
  flow:
    replicaCount: 6
    resources:
      requests:
        memory: 2048Mi
      limits:
        memory: 2048Mi
    kafka:
      sasl:
        username:
          value: "flow"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "flow"
  flowMapper:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "flowMapper"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "flowMapper"
  membership:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "membership"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "membership"
  p2pGateway:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "p2pGateway"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "p2pGateway"
  p2pLinkManager:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "p2pLinkManager"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "p2pLinkManager"
  persistence:
    replicaCount: 3
    resources:
      requests:
        memory: 2048Mi
      limits:
        memory: 2048Mi
    kafka:
      sasl:
        username:
          value: "persistence"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "persistence"
  rest:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "rest"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "rest"
    service:
      type: "LoadBalancer"
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
        service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
        external-dns.beta.kubernetes.io/hostname: "corda.example.com"
  tokenSelection:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "tokenSelection"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "tokenSelection"
  uniqueness:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "uniqueness"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "uniqueness"
  verification:
    replicaCount: 3
    kafka:
      sasl:
        username:
          value: "verification"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "verification"
```

## Install the Corda Helm Chart

Once the configuration for the environment has been defined in a YAML file, you can install the Helm chart:

```shell
helm install -n <NAMESPACE> <HELM-RELEASE-NAME> <HELM-CHART-TGZ-FILE> -f <PATH-TO-YAML-FILE>
```

For example, to create a Helm release called `corda` in the `corda` namespace using the overrides specified in a file called `values.yaml`, run the following:

```shell
helm install -n corda corda <HELM-CHART-TGZ-FILE> -f values.yaml
```

If you are using the Helm chart from Docker Hub, you can install directly from there rather than using `helm fetch` first. For example:

```shell
helm install -n corda corda oci://corda-os-docker.software.r3.com/helm-charts/release-{{<version-num>}}.0.0/corda --version {{<version-num>}}.0 -f values.yaml
```

Once the Helm install completes, all of the Corda workers are ready. A message is output containing instructions on how
to access the [Corda REST API]({{< relref "../../../reference/rest-api/_index.md" >}}).
If the Helm install fails, see the troubleshooting section on [observability]({{< relref "../../observability/_index.md" >}}).
