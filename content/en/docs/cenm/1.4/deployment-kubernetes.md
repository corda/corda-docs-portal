---
aliases:
- /deployment-kubernetes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-deployment-kubernetes
    parent: cenm-1-4-operations
tags:
- config
- kubernetes
title: CENM Deployment with Docker, Kubernetes, and Helm charts
weight: 20
---

# CENM Deployment with Docker, Kubernetes, and Helm charts

## Introduction

This deployment guide provides a set of simple steps for deploying Corda Enterprise Network Manager (CENM)
on a Kubernetes cluster in Azure Cloud.
The deployment uses Bash scripts and Helm templates provided with CENM Docker images.

### Who is this deployment guide for?

This deployment guide is intended for use by either of the following types of CENM users:

* Any user with a moderate understanding of Kubernetes who wants to create a CENM network using default configurations.
* Software developers who wish to run a representative network in their development cycle.

### Prerequisites

The reference deployment for Corda Enterprise Network Manager runs on [Kubernetes](https://kubernetes.io/) hosted on Microsoft Azure Cloud.
Microsoft Azure provides a dedicated service to deploy a Kubernetes cluster - [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/).
You must have an active Azure subscription to be able to deploy CENM.
The next section [Deploy your network](#Deploy-your-network) contains links to the official Microsoft installation guide.
The Kubernetes cluster must have access to a private Docker repository to obtain CENM Docker images.

Your local machine operating system should be Linux, Mac OS, or a Unix-compatible environment for Windows
(for example, [Cygwin](https://www.cygwin.com/)) as the deployment uses Bash scripts.
The deployment process is driven from your local machine using a Bash script and several third-party tools:
[Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest),
[Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [Helm](https://helm.sh/).
The following section [Deploy your network](#Deploy-your-network) provides links to official installation guides of the required tools.
In addition, the CENM Command-Line Interface (CLI) tool is required so you can connect to, and manage CENM (however, this is not required for deployment).

### Compatibility

The deployment scripts are compatible with Corda Enterprise Network Manager version 1.3 only.
The deployed network runs on Kubernetes minimum version 1.16.9 and Helm minimum version 3.1.1.

## Deployment

### Deployment overview

The provided deployment runs all CENM services run inside a single, dedicated Kubernetes namespace (default name:`cenm`).
Each service runs in its own dedicated Kubernetes pod, with the exception of the [Angel Service](angel-service.md), which runs in the same pod as its managed service.

{{< note >}}
Naturally, the following command will not show a dedicated Angel Service pod:
kubectl get pods -o wide

The Angel Service and its managed service must both be healthy in order for the pod they are running on to healthy. This means that the pod has a status `RUNNING` if both services are running fine, and a status `DOWN` if **any** of the two services (or both) is down.
{{< /note >}}

The CENM network is bootstrapped with PKI certificates, and sample X.500 subject names are provided as defaults
(for example, the Identity Manager Service certificate subject is
“CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US”).
These can be configured in the [Signing Service Helm chart](deployment-kubernetes-signer.md).

There are two ways of bootstrapping a new CENM environment:

- Scripted (`bootstrap.cenm`) with **allocating new** public IP addresses.
- Scripted (`bootstrap.cenm`) with  **reusing** already allocated public IP addresses.

Use the first method for the initial bootstrap process, where there are no allocated endpoints for the services.
The bootstrapping process uses default values stored in the `values.yaml` file of each Helm chart.

{{< note >}}
The Identity Manager Service requires its public IP address or hostname to be known in advance of certificate generation, as its URL is set as the endpoint for the CRL in certificates.
{{< /note >}}

It could take a few minutes to allocate a new IP address. For subsequent deployments, you should be able to reuse existing external IP addresses.

The Network Map Service and the Signing Services have their public IP addresses allocated while bootstrapping and they do not need to be known ahead of time.

Public IP addresses are allocated as Kubernetes `LoadBalancer` services.

### Deploy your network

The deployment steps are given below:

#### 1. Install tools on your local machine

- Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

- Install [helm](https://helm.sh/docs/intro/install/)

    Ensure that the value in the `version` field for `helm version` is equal to or greater than 3.2,
    as shown in the example below:

    ```bash
    version.BuildInfo{Version:"v3.2.4", GitCommit:"0ad800ef43d3b826f31a5ad8dfbb4fe05d143688", GitTreeState:"clean", GoVersion:"go1.13.12"}
    ```

- Install [Docker](https://www.docker.com/get-started). Docker is required to run the CENM CLI tool.

- Download the Docker image with CENM [Command-Line Interface (CLI) tool](cenm-cli-tool.md) so you can manage CENM services:

    ```bash
    docker pull cenm-cli:1.3-zulu-openjdk8u242
    ```

#### 2. Set up the Kubernetes cluster

- Install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your machine.

- Create a cluster on Azure, following Microsoft's [quick start guide](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough).
  CENM requires a Kubernetes cluster with at least 10 GB of free memory available to all CENM services.

- Check that you have your cluster subscription [as your active subscription](https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-set).

- Connect to [your cluster](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough-portal#connect-to-the-cluster)
  from your local machine.

#### 3. Create storage class and namespace

Run the following instruction once the previous points have been cleared:

`All the examples below use the namespace **cenm**`

```bash
kubectl apply -f deployment/k8s/cenm.yaml
export nameSpace=cenm
kubectl config set-context $(kubectl config current-context) --namespace=${nameSpace}
```

You can verify this with the command `kubectl get ns`.

#### 4. Download CENM deployment scripts

You can find the files required for the following steps in [CENM deployment repo](https://github.com/corda/cenm-deployment).

#### 5. External database setup

CENM services are pre-configured to use embedded H2 databases by default.
You can skip this step if an H2 database is sufficient for your needs. Otherwise you need to install database(s), set up users and permissions,
and change database configuration options for CENM services before bootstrapping CENM.
For instructions on how to do that, refer to the "CENM configuration for external databases" section below, which contains a sample PostgreSQL installation guide
and an explanation of CENM database configuration options.

#### 6. Bootstrap CENM

**Option 1.** Bootstrap by allocating new external IP addresses

To bootstrap your network, run the `bootstrap.cenm` script from the `/k8s/helm` directory.
The script includes the `--ACCEPT_LICENSE Y` argument, which is mandatory and confirms that you have read and accepted the license agreement.

```bash
cd k8s/helm
./bootstrap.cenm --ACCEPT_LICENSE Y <options>
```

You can use the following bootstrap options when running bootstrap:

* `--ACCEPT_LICENSE [Y]` - confirms agreement to the Licenses for Components deployed by the Bootstrapper.
* `-h` - displays this help message and exits.
* `-i|--idman  [name]` - provides Identity Manager kubernetes service name.
* `-n|--notary [name]` - provides Notary kubernetes service name.
* `-p|--prefix [prefix]` - specifies the release prefix for all Helm charts.
* `-m|--mpv [version]` - specifies the minimum platform version for your network.
* `-a|--auto` - completes the script without further prompts to the user.

Usage:

```bash
cd network-services/deployment/k8s/helm
./bootstrap.cenm <option>
```

{{< note >}}
The allocation of a load balancer to provide a public IP can take a significant amount of time (for example, even 10 minutes).
{{< /note >}}

The script exits after all bootstrapping processes on the Kubernetes cluster have been started.
The process will continue to run on the cluster after the script has exited. You can monitor the completion of the deployment by running the following commands:

``` bash
kubectl get pods -o wide
```

 **Option 2.**  Bootstrap by reusing already allocated external IP addresses

If your external IPs have been already allocated you can reuse them by specifying their services names:

```bash
cd network-services/deployment/k8s/helm
./bootstrap.cenm -i idman-ip -n notary-ip
```

## Network operations

Use the CENM [Command Line Interface (CLI) Tool](cenm-cli-tool.md) to access the [Gateway Service](gateway-service.md) from your local machine.
To star CENM CLI Tool run Docker command starting Docker container with the tool:

  ```bash
  docker run  -it --env ACCEPT_LICENSE=Y --name=cenm-cli cenm-cli:1.3-zulu-openjdk8u242
  ```

The welcome message will appear:

  ```bash
  CORDA ENTERPRISE NETWORK MANAGER – SOFTWARE EVALUATION LICENSE AGREEMENT has been accepted, CORDA ENTERPRISE NETWORK MANAGER will now continue.   The Software Evaluation License Agreement for this product can be viewed from https://www.r3.com/corda-enterprise-network-manager-evaluation-license.
  A copy of the Software Evaluation License Agreement also exists within the /license directory in the container.

  Type "./cenm <COMMAND>" to run CENM CLI or "./cenm -h" to display help.
  cenm@5fdb0372b89b:~$
  ```

You can now use `cemn` commands from within the running Docker container:

  ```bash
  ./cenm context login -s -u <USER> -p <PASSWORD> http://<GATEWAY-SERVICE-IP>:8080
  ```

The [Gateway Service](gateway-service.md) is a gateway between the [Auth Service](auth-service.md) and front end services in CENM. It allows you to perform all network operations on the [Identity Manager Service](identity-manager.md), the [Network Map Service](network-map.md), and the [Signing Service](signing-service.md).
The IP address is dynamically allocated for each deployment and can be found with `kubectl get svc`.
Use the following command to ensure that you are pointing at the correct namespace:

  ```bash
  kubectl config current-context && kubectl config view --minify --output 'jsonpath={..namespace}' && echo`)
  ```

If you have exited the Docker container, you can reconnect again:

  ```bash
  docker container exec -it cenm-cli bash
  ```

If the Docker container was not running, you need to restart it by reconnecting:

  ```bash
  docker container start cenm-cli
   ```

## Assigning permissions to users

Login to web application ``http://<GATEWAY-SERVICE-IP>:8080/admin`` using admin user and credentials.
The CENM network has no permissions assigned to Main Zone by default, you need to assign them manually.

### Join your network

Edit the following properties in your `node.conf` file to configure Corda node to connect to the CENM services:

```bash
networkServices {
  doormanURL="http://<IDENTITY-MANAGER-IP>:10000"
  networkMapURL="http://<NETWORK-MAP-IP>:10000"
}
```

Replacing placeholder values as follows:
  * the `doormanURL` property is the public IP address and port of the Identity Manager Service
  * the `networkMapURL` is the pubic IP address and port of the Network Map Service.

Next, upload the `network-root-truststore.jks` to your Corda node.
You can download it locally from the CENM Signing Service, using the following command:

```bash
kubectl cp <namespace>/<signer-pod>:DATA/trust-stores/network-root-truststore.jks network-root-truststore.jks
```

Namespace is typically `cenm` for this deployment.

Run the following command to obtain public IPs of the Identity Manager Service and the Network Map Service:

```bash
kubectl get svc idman-ip notary-ip
```

Run the command below to obtain the pod name for the Signing Service:

```bash
kubectl get pods -o wide
```

You will find the truststore password in the `signer/files/pki.conf`, where the default value used in this Helm chart is `trust-store-password`.

{{< note >}} For more details about joining a CENM network, see:
[Joining an existing compatibility zone](../../corda-os/4.5/joining-a-compatibility-zone.md).
{{< /note >}}

### Display logs

Each CENM service has a dedicated sidecar to display live logs from the `log/` directory.

Use the following command to display logs:

  ```bash
  kubectl logs -c logs <pod-name>
  ```

Use the following command to display live logs:

  ```bash
  kubectl logs -c logs -f <pod-name>
  ```

Display configuration files used for each CENM service:

Each service stores configuration files in `etc/` directory in a pod.
Run the following commands to display what is in the Identity Manager Service `etc/` directory:

```bash
kubectl exec -it <pod name> -- ls -al etc/
Defaulting container name to main.

Use 'kubectl describe pod/idman-7699c544dc-bq9lr -n cenm' to see all of the containers in this pod.
total 10
drwxrwxrwx 2 corda corda    0 Feb 11 09:29 .
drwxr-xr-x 1 corda corda 4096 Feb 11 09:29 ..
-rwxrwxrwx 1 corda corda 1871 Feb 11 09:29 idman.conf

kubectl exec -it <pod name> -- cat etc/idman.conf
Defaulting container name to main.

Use 'kubectl describe pod/idman-7699c544dc-bq9lr -n cenm6' to see all of the containers in this pod.

address = "0.0.0.0:10000"
database {
...
```

### Update network parameters

Use the CENM [Command-Line (CLI) tool](cenm-cli-tool.md) to run commands to update the network parameters.

See the official CENM documentation for more information about the list of available [network parameters](./config-network-parameters.html)
and instructions on [updating network parameters](./updating-network-parameters.html).

### Run Flag Day

Use the following CENM Command-Line Interface (CLI) tool command to run a Flag Day:

{{< note >}} For the changes to be advertised to the nodes, the new network map must be signed by the Signing Service.
This operation is scheduled to take place at regular intervals (by default, once every 10 seconds), as defined in the network map configuration.
{{< /note >}}

### Signing Service configuration

The Signing Service is not managed by the [Angel Service](angel-service.md) in this deployment, therefore any CENM Command-Line Interface (CLI) tool commands trying to change the Signing Service configuration will take no effect.
To change the Singing Service configuration, you must log in to a Kubernetes pod, update the configuration file, and restart the service.

## Delete Network
There are two ways to delete your permissioned network (intended for development
environments, which are rebuilt regularly), as follows:

- delete the whole environment including IPs
- delete all CENM objects without deleting allocated external IP addresses

### Delete the whole environment including IPs

The environment can be deleted via Helm, by deleting each deployed chart individually. Note that the chart names include a prefix, which needs to match the prefix specified when setting up the environment.

```bash
export CENM_PREFIX=cenm
helm delete ${CENM_PREFIX}-auth ${CENM_PREFIX}-gateway ${CENM_PREFIX}-idman ${CENM_PREFIX}-nmap ${CENM_PREFIX}-notary ${CENM_PREFIX}-pki ${CENM_PREFIX}-hsm ${CENM_PREFIX}-signer ${CENM_PREFIX}-zone ${CENM_PREFIX}-idman-ip ${CENM_PREFIX}-notary-ip
```

### Delete the whole environment without deleting IPs

If you run several ephemeral test networks in your development cycle, you might want to keep your IP addresses to speed up the process:

```bash
export CENM_PREFIX=cenm
helm delete ${CENM_PREFIX}-auth ${CENM_PREFIX}-gateway ${CENM_PREFIX}-idman ${CENM_PREFIX}-nmap ${CENM_PREFIX}-notary ${CENM_PREFIX}-pki ${CENM_PREFIX}-hsm ${CENM_PREFIX}-signer ${CENM_PREFIX}-zone
```

## Deployment Customisation

The Kubernetes scripts provided are intended to be customised depending on customer requirements.
The following sections describes how to customise various aspects of the deployment.

### Using Azure Key Vault

The deployment process provides built-in support for Azure Key Vault in order to secure the key stores
generated by the PKI tool.

Once you have created an Azure Key Vault that you want to use, perform the following steps:

1. Modify the HSM pod configuration to contain the required library `.jar` files.
2. Modify PKI `values.yaml` configuration file.
3. Modify Signing Service `values.yaml` configuration file.
4. Start the deployment as normal. The deployment may take more time than usual this way, due to the communication with the key vault.

#### Modifying the HSM pod configuration

The HSM pod is a helper pod, which loads a defined Docker image and attempts to load the folder containing the HSM-related
files as a volume for the other pods to use. Follow the steps below:
1. [Create the library jar](#azure-key-vault).
2. Create a Docker image containing the `.jar` file and the `.pkcs12` file used as the key store path.

The Docker image and the directory where these files are stored must be specified in the relevant variables in the HSM `values.yaml` file.
Note that you may need to add permissions to your cluster to download the Docker image successfully.

#### Modify PKI configuration

You must modify the following values in the `values.yaml` file:

`pkiJar.configFile: pki-azure.conf`
`signingKeys.keyStore.keyVaultUrl: <your vault url>`
`signingKeys.credentials.clientId: <the client ID that will access the vault>`
`signingKeys.credentials.keyStorePassword: <the password of the .pkcs12 file>`
`signingKeys.credentials.keyStoreAlias: <the alias of the .pkcs12 file>`

#### Modify Signing Service configuration

You must modify the following values in the `values.yaml` file:

`signerJar.configFile: signer-azure.conf`
`signingKeys.keyStore.keyVaultUrl: <your vault url>`
`signingKeys.credentials.clientId: <the client ID that will access the vault>`
`signingKeys.credentials.keyStorePassword: <the password of the .pkcs12 file>`
`signingKeys.credentials.keyStoreAlias: <the alias of the .pkcs12 file>`

### Service Chart Settings

There are a number of settings provided on each Helm chart, which allow easy customisation of
common options. Each CENM service has its own dedicated page with more detailed documentation:

* [Auth Service](deployment-kubernetes-auth.md)
* [Gateway Service](deployment-kubernetes-gateway.md)
* [Identity Manager Service](deployment-kubernetes-idman.md)
* [Network Map Service](deployment-kubernetes-nmap.md)
* [Corda Notary](deployment-kubernetes-notary.md)
* [Signing Service](deployment-kubernetes-signer.md)
* [Zone Service](deployment-kubernetes-zone.md)

### Overriding Service Configuration

The default settings used in a CENM service's configuration values can be altered as described in
[Helm guide](https://helm.sh/docs/chart_template_guide/values_files/).
In brief this can be achieved by:
* Create a separate yaml file with new values and pass it with `-f` flag: `helm install -f myvalues.yaml idman`, or;
* Override individual parameters using `--set`, such as `helm install --set foo=bar idman`, or;
* Any combination of the above, for example ```helm install -f myvalues.yaml --set foo=bar idman```

You cannot override the passwords to security certificates keys and keystores.

### External database support

You can configure the services to use an external database. We strongly recommend this for production deployments.
A database can be installed as a pod inside the same Kubernetes cluster or as a separate installation outside the Kubernetes cluster.
The example below shows a PostgresSQL installation that runs inside the same Kubernetes cluster where CENM runs.

#### Example PostgreSQL database setup inside the Kubernetes cluster

A PostgreSQL database can be installed inside the Kubernetes cluster using a third-party [Bitami Helm chart](https://github.com/bitnami/charts/tree/master/bitnami/postgresql):

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install cenm-database bitnami/postgresql
```

Follow the instructions displayed by the script output to connect to the database server via `psql`.
You can create a separate database server for each CENM service by running the Helm script multiple times with different names
and then setting up the database user/schema, following the instructions in the [CENM database setup](database-set-up.md) section.
Alternatively, you can create several databases inside the single PostgresSQL server you have just deployed, by running
the following DDL commands:

```bash
CREATE DATABASE <DATABASE>;
CREATE USER <USER> WITH PASSWORD '<PASSWORD>';
GRANT ALL PRIVILEGES ON DATABASE <USER> to <DATABASE>;
```

For each service (Identity Manager, Network Map, Zone, and Auth), use different `<DATABASE>` name and `<USER>` -
for example, `idenamagerdb` / `identitymanageruser` for the Identity Manager Service.

#### CENM configuration for external databases

The database used by each service is configured via JDBC URL and is defined in the `values.yml` file for
the Helm chart of the respective service - for example, `idman/values.yml` for the Identity Manager Service.
In the `values.yml` file, edit the database section of the configuration to change the JDBC URL, user, and password.

The deployed service already contains JDBC drivers for PostgreSQL and SQLServer.
For an Oracle database, you need to extend the Docker images for the service by adding
the Oracle JDBC driver `.jar` file to the `/opt/${USER}/drivers/` directory.

{{< note >}}
The bootstrap script cannot be used with an external database.
 Instead, you should run each Helm chart manually by specifying the correct database URL.
{{< /note >}}

Example settings for connection to a PostgreSQL database follow below:

```guess
database:
  driverClassName: "org.postgresql.Driver"
  jdbcDriver: "/opt/cenm/drivers/postgresql-42.2.12.jar"
  url: "jdbc:postgresql://<HOST>:<PORT>/<DATABASE>"
  user: "<USER>"
  password: "<PASSWORD>"
  runMigration: "true"
```

In this example, `<HOST>` is a placeholder for the host name of the server, `<PORT>` is a placeholder for the port number the server is listening on (typically `5432` for PostgreSQL),
`<DATABASE>` is a placeholder for the database name, and `<USER>` and `<PASSWORD>` are placeholders for the access credentials of the database user.

### Memory Allocation

Default memory settings used should be adequate for most deployments, but may need to be increased for
networks with large numbers of nodes (over a thousand). The `cordaJarMx` value for each Helm chart
(in `values.yaml`) is passed to the JVM as the `-Xmx` value, and is specified in GB. Each Pod requests
memory sufficient for this value, with a limit 2GB higher than the value.

All services except the Notary use 1GB of RAM as their default `cordaJarMx`, while Notary defaults to 3GB.

## Manual bootstrap

For production deployments, you can use the bootstrap script to provide a baseline.
However, for additional flexibility you may wish to deploy each Helm chart individually.
There are several Helm commands which are used to bootstrap a new CENM environment,
where each command creates a CENM service consisting of the following:

* Signing Service
* Identity Manager Service
* Network Map Service
* Auth Service
* Gateway Service
* Corda Notary

They need to be run in the correct order, as shown below:

```bash
cd network-services/deployment/k8s/helm

# These Helm charts trigger public IP allocation
helm install idman-ip idman-ip
helm install notary-ip notary-ip
helm install gateway-ip gateway-ip

# Run these commands to display allocated public IP addresses:
kubectl get svc --namespace cenm idman-ip --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"   # step 1
kubectl get svc --namespace cenm notary-ip --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"  # step 2
kubectl get svc --namespace cenm gateway-ip --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"  # step 3

# These Helm charts bootstrap CENM
helm install cenm-auth auth --set prefix=cenm --set acceptLicense=YES
helm install cenm-zone zone --set prefix=cenm --set acceptLicense=YES
helm install cenm-nmap nmap --set prefix=cenm --set acceptLicense=YES
helm install cenm-signer signer --set prefix=cenm --set acceptLicense=YES
helm install cenm-idman idman --set prefix=cenm --set acceptLicense=Y --set idmanPublicIP=[use IP from step 1]
helm install notary notary --set prefix=cenm --set acceptLicense=YES --set notaryPublicIP=[use IP from step 2]
helm install cenm-nmap nmap --set prefix=cenm --set acceptLicense=YES
helm install cenm-gateway gateway --set prefix=cenm --set acceptLicense=YES --set idmanPublicIP=[use IP from step 3]

# Run these commands to display allocated public IP for Network Map Service:
kubectl get svc --namespace cenm nmap --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"
```

## Appendix A: Docker Images

The Docker images used for the Kubernetes deployment are listed below for reference:

{{< table >}}

| Service           | Image Name                         | Tag |
|-------------------|------------------------------------|-----|
| Identity Manager  | acrcenm.azurecr.io/nmap/nmap       | 1.3 |
| Network Map       | acrcenm.azurecr.io/nmap/nmap       | 1.3 |
| Signing           | acrcenm.azurecr.io/signer/signer   | 1.3 |
| Zone              | acrcenm.azurecr.io/zone/zone       | 1.3 |
| Auth              | acrcenm.azurecr.io/auth/auth       | 1.3 |
| Gateway              | acrcenm.azurecr.io/gateway/gateway       | 1.3 |
| PKI Tool          | acrcenm.azurecr.io/pkitool/pkitool | 1.3 |
| Notary            | acrcenm.azurecr.io/notary/notary   | 1.3 |

{{< /table >}}
