---
date: '2023-01-26'
title: "Deploying a Corda Cluster"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorials-deploy
    identifier: corda-5-beta-tutorial-deploy-k8s
    weight: 1000
section_menu: corda-5-beta
---

This page describes how to deploy Corda 5 Beta. It assumes all necessary [prerequisites](../prerequisites.html) have been installed.

## Download and Push Container Images to a Registry

The Corda container images must be in a registry that is accessible from the Kubernetes cluster in which Corda will run.
By default, the images are made available via Docker Hub.
If your Kubernetes cluster can pull images from Docker Hub, you can skip this section.
If not, then the following instructions describe how to push the images from the provided `tar` file into a container registry that is accessible from the cluster.

1. Download `corda-worker-images-Fox.tar` from the [R3 Customer Hub](https://r3.force.com/).

2. Inflate and load the `corda-worker-images-Fox.tar` file into the local Docker engine with the following command:
   ```shell
   docker load -i corda-worker-images-Fox.tar
   ```

3. Retag each image using the name of the registry to be used and push the image. The following is an example script to automate this. It takes the target container registry as an argument. If the target registry requires authentication, you must perform a `docker login` against the registry before running the script.
   ```shell
   #!/bin/bash
   if [ -z "$1" ]; then
    echo "Specify target registry"
    exit 1
   fi

   declare -a images=(
    "corda-os-rest-worker" "corda-os-flow-worker"
    "corda-os-member-worker" "corda-os-p2p-gateway-worker"
    "corda-os-p2p-link-manager-worker" "corda-os-db-worker"
    "corda-os-crypto-worker" "corda-os-plugins" )
   tag=5.0.0.0-Gecko2.0
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

## Download the Corda Helm Chart

If you have access to Docker Hub, you can download the Corda Helm chart using the following command:

```shell
helm fetch oci://registry-1.docker.io/corda/corda --version 5.0.0-Fox.1.1
```

If you do not have access to Docker Hub, you can download the `corda-5.0.0-Gecko2.0.tgz` file from the [R3 Customer Hub](https://r3.force.com/).

## Configure the Deployment

For each deployment, you should create a YAML file to define a set of Helm overrides to be used for that environment.
The following sections describe the minimal set of configuration options required for a deployment.
You can extract a README containing the full set of options from the Helm chart using the following command:
```shell
helm show readme corda-5.0.0-Gecko2.0.tgz
```

You can extract a YAML file containing all of the default values using the following command:
```shell
helm show values corda-5.0.0-Gecko2.0.tgz
```

### Image Registry

If you are not using the Corda container images from Docker Hub, define an override specifying the name of the container registry to which you pushed the images:
```yaml
image:
  registry: <REGISTRY-NAME>
```

If the registry requires authentication, create a [Kubernetes secret](https://kubernetes.io/docs/concepts/configuration/secret/#docker-config-secrets) containing the container registry credentials, in the Kubernetes namespace where Corda is to be deployed. Specify an override with the name of the Kubernetes secret:
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
  rest:
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
It is particularly important to specify resource requests when using a Kubernetes cluster with auto-scaling, to ensure that it scales appropriately when the Corda cluster is deployed.
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

By default, the [REST API](../../operating/operating-tutorials/rest-api.html) is exposed on an internal Kubernetes service. To enable access from outside the Kubernetes cluster, the API should be fronted by a load balancer. The Helm chart allows annotations to be specified to facilitate the creation of a load balancer by a cloud-platform specific controller. For example, the following configuration specifies that the [AWS Load Balancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html) fronts the REST API with a Network Load Balancer internal to the Virtual Private Cloud (VPC):
```yaml
workers:
  rest:
    service:
      type: LoadBalancer
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: true
        service.beta.kubernetes.io/aws-load-balancer-scheme: internal
        service.beta.kubernetes.io/aws-load-balancer-type: nlb
        external-dns.beta.kubernetes.io/hostname: corda.example.com
```

### PostgreSQL

The password for PostgreSQL can be specified directly as a Helm override, but this is not recommended. Instead, create a Kubernetes secret containing the password with a key of `password`. By default, the install expects a database called `cordacluster`, but this can be overridden. You can then define the PostgreSQL configuration as follows:
```yaml
db:
  cluster:
    host: <POSTGRESQL_HOST>
    port: 5432
    username:
      value: <POSTGRESQL_USER>
    password:
      valueFrom:
        secretKeyRef:
          name: <POSTGRESQL_PASSWORD_SECRET_NAME>
          key: <POSTGRESQL_PASSWORD_SECRET_KEY>
    database: <POSTGRESQL_CLUSTER_DB>
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

If the broker certificate is self-signed or cannot be trusted for some other reason, create a Kubernetes secret containing the client trust store. The trust store can be in PEM or JKS format. If JKS format is used, you can supply a password for the trust store. The following example is for a trust store in PEM format stored against the `ca.crt` key in the Kubernetes secret:
```yaml
kafka
  tls:
    secretRef:
      name: <TRUST-STORE-SECRET-NAME>
      key: "ca.crt"
    type: PEM   
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

### Bootstrapping

By default, the Helm chart automatically configures Kafka, PostgreSQL, and a default set of Corda RBAC roles as part of the deployment process.
If desired, each of these steps can be disabled and the necessary [configuration performed manually](manual.html).

#### Kafka
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

If SASL authentication is enabled, the bootstrapping also creates Access Control List (ACL) entries for producing and consuming from the topics as appropriate for each worker.

#### Database

The database bootstrapping creates schemas in the cluster database and populates them with the initial configuration. It is enabled by default:

```yaml
bootstrap:
  db:
    enabled: true
```
By default, the database bootstrapping uses the psql CLI from the Docker image `postgres:14.4` on Docker Hub. If the Kubernetes cluster does not have access to Docker Hub, you must make this image available in an internal registry. You can then specify the location of the image via overrides, as follows:

```yaml
db:
  clientImage:
    registry: <REGISTRY>
    repository: "postgres"
    tag: "14.4"
```
Part of the database bootstrapping involves populating the initial admin credentials. You can specify these in one of the following ways:

* Pass the user name and password as Helm values:
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

### Service Accounts

If additional permissions are required, you can specify a service account for the Corda workers and bootstrap containers.

For example, when running with Red Hat OpenShift Container Platform, you must use a service account with the priviliged security context constraint:

1. Create a file `sa.yaml` defining a custom service account bound to a role that provides the required security context constraint:

   ```yaml
   kind: ServiceAccount
   apiVersion: v1
   metadata:
     name: corda-privileged

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
   serviceAccount: "corda-privileged"
   bootstrap:
     serviceAccount: "corda-privileged"
   ```

### Custom Annotations for Worker Pods

You can define custom annotations for worker pods. You can add these globally or to individual workers. For example, to define `annotation-key-1` for all workers:

```yaml
annotations:
  annotation-key-1: "custom-value"
```

To define `annotation-key-2` for only the crypto worker:

```yaml
workers:
  crypto:
    annotations:
      annotation-key-2/is-safe: "true" 
```

### Example Configuration

{{< warning >}}
The example in this section is included only for illustrative purposes. You must use the information provided to determine the correct configuration file for your environment.
{{< /warning >}}

The following example shows a complete configuration file for Corda deployment in an environment in which Kafka is using a trusted TLS certificate, SASL authentication is enabled, the REST API is exposed via an AWS Network Load Balancer, and the generated password for the initial admin user is retrieved from a secret.

```yaml
image:
  registry: "registry.example.com"

imagePullSecrets:
  - "registry-secret"

resources:
  requests:
    memory: "512Mi"
    cpu: "125m"
  limits:
    memory: "2048Mi"
    cpu: "1000m"

serviceAccount: "corda-privileged"

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
    mechanism: "SCRAM-SHA-512"

bootstrap:
  db:
    clientImage:
      registry: "registry.example.com"
  kafka:
    sasl:
      username:
        value: "bootstrap"
      password:
        valueFrom:
          secretKeyRef:
            name: "kafka-credentials"
            key: "bootstrap"
  serviceAccount: "corda-privileged"

workers:
  crypto:
    kafka:
      sasl:
        username:
          value: "crypto"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "crypto"
    replicaCount: 3
  db:
    kafka:
      sasl:
        username:
          value: "db"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "db"
    replicaCount: 3
  flow:
    kafka:
      sasl:
        username:
          value: "flow"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "flow"
    replicaCount: 3
  membership:
    kafka:
      sasl:
        username:
          value: "membership"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "membership"
    replicaCount: 3
  p2pGateway:
    kafka:
      sasl:
        username:
          value: "p2pGateway"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "p2pGateway"
    replicaCount: 3
  p2pLinkManager:
    kafka:
      sasl:
        username:
          value: "p2pLinkManager"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "p2pLinkManager"
    replicaCount: 3
  rest:
    kafka:
      sasl:
        username:
          value: "rest"
        password:
          valueFrom:
            secretKeyRef:
              name: "kafka-credentials"
              key: "rest"
    replicaCount: 3
    service:
      type: "LoadBalancer"
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
        service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
        external-dns.beta.kubernetes.io/hostname: "corda.example.com"
```

## Deployment

Once the configuration for the environment has been defined in a YAML file, you can install the Helm chart:
```shell
helm install -n <NAMESPACE> <HELM-RELEASE-NAME> corda-5.0.0-Gecko2.0.tgz -f <PATH-TO-YAML-FILE>
```
For example, to create a Helm release called `corda` in the `corda` namespace using the overrides specified in a file called `values.yaml`, run the following:

```shell
helm install -n corda corda corda-5.0.0-Fox1.1.tgz -f values.yaml
```

If you are using the Helm chart from Docker Hub, you can install directly from there rather than using `helm fetch` first. For example:

```shell
helm install -n corda corda oci://registry-1.docker.io/corda/corda --version 5.0.0-Fox.1.1 -f values.yaml
```

Once the Helm install completes, all of the Corda workers are ready. A message is output containing instructions on how to access the [Corda REST API](../../operating/operating-tutorials/rest-api.html). If the Helm install fails, see the troubleshooting section on [Cluster Health](../troubleshooting/cluster-health.html).
