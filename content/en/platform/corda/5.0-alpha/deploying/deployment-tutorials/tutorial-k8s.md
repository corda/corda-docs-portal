---
date: '2021-11-14'
title: "Deploying a Corda Cluster"
menu:
  corda-5-alpha:
    parent: corda-5-alpha-tutorials-deploy
    identifier: corda-5-alpha-tutorial-deploy-k8s
    weight: 1000
section_menu: corda-5-alpha
---

This page describes how to deploy Corda 5 Alpha. It assumes all necessary [prerequisites](../prerequisites.html) have been installed.

## Download and Push Docker Images to a Registry

The Corda Docker images must be in a Docker registry that is accessible from the Kubernetes cluster in which Corda will run. The images are provided in a `tar` file which can be loaded into a local Docker engine and then pushed from there to the registry.

1. Download `corda-worker-images.tar` from the [R3 Customer Hub](https://r3.force.com/).

2. Inflate and load the `corda-worker-images.tar` file into the local Docker engine with the following command:
   ```shell
   docker load -i corda-worker-images.tar
   ```

3. Retag each image using the name of the registry to be used and push the image. The following is an example script to automate this. It takes the target Docker registry as an argument.
   ```shell
   #!/bin/bash
   if [ -z "$1" ]; then
    echo "Specify target registry"
    exit 1
   fi

   declare -a images=(
    "corda-os-rpc-worker" "corda-os-flow-worker"
    "corda-os-member-worker" "corda-os-p2p-gateway-worker"
    "corda-os-p2p-link-manager-worker" "corda-os-db-worker"
    "corda-os-crypto-worker" "corda-os-plugins" )
   tag=5.0.0.0-BetaProgram-alpha.1-RC01
   target_registry=$1

   for image in "${images[@]}"; do
    source=corda/$image:$tag
    target=$target_registry/$image:$tag
    echo "Publishing image $source to $target"
    docker tag $source $target
    docker push $target
   done

   docker tag postgres:14.4 $target_registry/postgres:14.4
   docker push $target_registry/postgres:14.4
   ```

## Download Helm Charts

1. Download the Helm charts `tar` file from the [R3 Customer Hub](https://r3.force.com/).

## Configure the Deployment

For each deployment, you should create a YAML file to define a set of Helm overrides to be used for that environment.
The following sections describe the minimal set of configuration options required for a deployment.
You can extract a README containing the full set of options from the Helm chart using the following command:
```shell
helm show readme ************
```

You can extract a YAML file containing all of the default values using the following command:
```shell
helm show values ************
```

### Image Registry

Define an override for the name of the Docker registry containing the Corda Docker images:
```yaml
image:
  registry: <REGISTRY-NAME>
```

If the registry requires authentication, create a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#docker-config-secrets) containing the Docker registry credentials, in the Kubernetes namespace where Corda is to be deployed. Specify an override with the name of the Kubernetes secret:
```yaml
imagePullSecrets:
  - <IMAGE-PULL-SECRET-NAME>
```

### Replica Counts

For high-availability, specify at least three replicas for each type of Corda worker:
```yaml
workers:
  crypto:
    replicaCount: 3
  db:
    replicaCount: 3
  flow:
    replicaCount: 3
  membership:
    replicaCount: 3
  rpc:
    replicaCount: 3
  p2pGateway:
    replicaCount: 3
  p2pLinkManager:
    replicaCount: 3
```

{{< note >}}
Depending on your application workload, you may require additional replicas.
{{< /note >}}

### Resource Requests and Limits

Specify a default set of resource requests and limits for the Corda containers:
```yaml
resources:
  requests:
    memory: 512Mi
    cpu: 125m
  limits:
    memory: 2048Mi
    cpu: 1000m
```
{{< note >}}
It is particularly important to specify resource requests when using a Kubernetes cluster with auto-scaling to ensure that it scales appropriately when the Corda cluster is deployed.
{{< /note >}}

You can also override the default resource requests and limits separately for each type of Corda worker. For example, to increase the memory limit for flow workers:
```yaml
workers:
  flow:
    resource:
      limit:
        memory: 4096Mi
```
As with the number of replicas, you may need to adjust these values based on testing with your actual application workload.

### REST API Load Balancer

By default, the [REST API](../../developing/rest-api/rest-api.html) is exposed on an internal Kubernetes service. To enable access from outside the Kubernetes cluster, the API should be fronted by a load balancer. The Helm chart allows annotations to be specified to facilitate the creation of a load balancer by a cloud-platform specific controller. For example, the following configuration specifies that the [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html) fronts the REST API with a Network Load Balancer internal to the Virtual Private Cloud (VPC):
```yaml
workers:
  rpc:
    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: true
        service.beta.kubernetes.io/aws-load-balancer-scheme: internal
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        external-dns.alpha.kubernetes.io/hostname: corda.example.com
```

### PostgreSQL

The password for PostgreSQL can be specified directly as a Helm override but this is not recommended. Instead, create a Kubernetes secret containing the password with a key of password. By default, the install expects a database called `cordacluster` but this can be overridden. You can then define the PostgreSQL configuration as follows:
```yaml
db:
  cluster:
    host: <POSTGRESQL_HOST>
    port: 5432
    user: <POSTGRESQL_USER>
    database: <POSTGRESQL_CLUSTER_DB>
    existingSecret: <POSTGRESQL_PASSWORD_SECRET_NAME>
```

### Kafka

Specify the Kafka bootstrap servers as a comma-separated list:
```yaml
kafka:
  boostrapServers: <KAFKA_BOOTSTRAP_SERVERS>
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

If the broker certificate is self-signed or can not be trusted for some other reason, create a Kubernetes secret containing the client trust store. The trust store can be in PEM or JKS format. If JKS format is used, you can supply a password for the trust store. The following example is for a trust store in PEM format stored against the `ca.crt` key in the Kubernetes secret:
```yaml
kafka
  tls:
    secretRef:
      name: <TRUST-STORE-SECRET-NAME>
      key: "ca.crt"
    type: PEM   
```

Corda supports SASL for Kafka authentication. If your Kafka instance requires SASL authentication, create a secret containing the credentials with the username and password of the key and then specify the secret name, along with the required mechanism in the overrides:

```yaml
kafka:
  sasl:
    enabled: true
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
    mechanism: "SCRAM-SHA-512"
```

### Bootstrapping

By default, the Helm chart automatically configures Kafka, PostgreSQL, and a default set of Corda RBAC roles as part of the deployment process.
If desired, each of these steps can be disabled and the necessary [configuration performed manually](manual.html).

#### Kafka
The Kafka bootstrapping creates the topics required by Corda.
If `kafka.topicPrefix` has been specified, the process uses this as a prefix for all of the topic names.
The bootstrap configuration enables the default number of topic partitions to be overridden.
You may need to increase this to support a larger number of Corda worker replicas.
It is also possible to override the default topic replica count.
For example, if less than three Kafka brokers are available.
The following extract shows the default values:

```yaml
bootstrap:
  kafka:
    enabled: true
    partitions: 10
    replicas: 3
```

#### Database

The database bootstrapping creates schemas in the cluster database and populates them with the initial configuration. It is enabled by default:

```yaml
bootstrap:
  db:
    enabled: true
```
By default, the database bootstrapping uses the psql CLI from the Docker image `postgres:14.4` on Docker Hub. If the Kubernetes cluster does not have access to Docker Hub, this image must be made available in an internal registry. The location of the image can then be specified via overrides, as follows:

```yaml
db:
  clientImage:
    registry: <REGISTRY>
    repository: "postgres"
    tag: "14.4"
```
Part of the database bootstrapping involves populating the initial admin credentials. You can specify these in one of the following ways:

* Pass the username and password as Helm values:
  ```yaml
  bootstrap:
    initialAdminUser:
      username:
        value: <USERNAME>
      password:
        value: <PASSWORD>
  ```

* Leave the password field blank. A Kubernetes secret is created containing a generated password. The notes output when the deployment completes contain instructions for how to retrieve this. This is the default behavior.

* Create a Kubernetes secret containing the user credentials:
  ```yaml
  bootstrap:
    initialAdminUser:
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

#### RBAC

The RBAC bootstrapping creates three default RBAC roles. It is enabled by default:
```yaml
bootstrap:
  rbac:
    enabled: true
```

### Example configuration

{{< warning >}}
The example in this section is included only for illustrative purposes. You must use the information provided to determine the correct configuration file for your environment.
{{< /warning >}}

The following example shows a complete configuration file for Corda deployment in an environment in which Kafka is using a trusted TLS certificate, SASL authentication is enabled, the REST API is exposed via an AWS Network Load Balancer, and the generated password for the initial admin user is retrieved from a secret.

```yaml
image:
  registry: "registry.example.com"

imagePullSecrets:
  - "registry-secret"

workers:
  crypto:
    replicaCount: 3
  db:
    replicaCount: 3
  flow:
    replicaCount: 3
  membership:
    replicaCount: 3
  rpc:
    replicaCount: 3
  p2pGateway:
    replicaCount: 3
  p2pLinkManager:
    replicaCount: 3

resources:
  requests:
    memory: "512Mi"
    cpu: "125m"
  limits:
    memory: "2048Mi"
    cpu: "1000m"

workers:
  rpc:
    service:
      type: "LoadBalancer"
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
        service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
        external-dns.alpha.kubernetes.io/hostname: "corda.example.com"

db:
  cluster:
    host: "postgres.example.com"
    port: 5432
    database: "cordacluster"
    user:
      value: "user"
    password:
      valueFrom:
        secretKeyRef:
          name: "postgres-secret"
          key: "password"

kafka:
  boostrapServers: "kafka-1.example.com,kafka-2.example.com,kafka-3.example.com"
  tls:
    enabled: true
  sasl:
    enabled: true
    username:
      valueFrom:
        secretKeyRef:
          name: "kafka-secret"
          key: "username"
    password:
      valueFrom:
        secretKeyRef:
          name: "kafka-secret"
          key: "password"
    mechanism: "SCRAM-SHA-512"

bootstrap:
  db:
    clientImage:
      registry: "registry.example.com"
```

## Deployment

Once the configuration for the environment has been defined in a YAML file, you can install the Helm chart:
```shell
helm install -n <NAMESPACE> <HELM-RELEASE-NAME> ****** -f <PATH-TO-YAML-FILE>
```
For example, to create a Helm release called `corda` in the `corda` namespace using the overrides specified in a file called `values.yaml`, run the following:

```shell
helm install -n corda corda ****** -f values.yaml
```
Once the Helm install completes, all of the Corda workers are ready. A message is output containing instructions on how to access the [Corda REST API]().
