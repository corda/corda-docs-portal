---
aliases:
- /releases/release-1.2/deployment-kubernetes.html
- /docs/cenm/head/deployment-kubernetes.html
- /docs/cenm/deployment-kubernetes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-deployment-kubernetes
    parent: cenm-1-2-operations
tags:
- config
- kubernetes
title: CENM Deployment with Docker, Kubernetes, and Helm charts
weight: 20
---

# CENM Deployment with Docker, Kubernetes and Helm charts

- [CENM Deployment with Docker, Kubernetes and Helm charts](#cenm-deployment-with-docker-kubernetes-and-helm-charts)
  - [Docker images and JDK supported](#docker-images-and-jdk-supported)
  - [Helm charts](#helm-charts)
  - [Kubernetes services supported](#kubernetes-services-supported)
  - [General information about this deployment](#general-information-about-this-deployment)
  - [Deploying your network](#deploying-your-network)
    - [Prerequisite](#prerequisite)
      - [(1) Install dependencies](#1-install-dependencies)
      - [(2) Set up and connect to a cluster on Azure](#2-set-up-and-connect-to-a-cluster-on-azure)
      - [(3) Create storage class and namespace](#3-create-storage-class-and-namespace)
      - [(4) Download helm charts and installation scripts](#4-download-helm-charts-and-installation-scripts)
    - [Option 1: Bootstrapping by allocating new external IP addresses](#option-1-bootstrapping-by-allocating-new-external-ip-addresses)
    - [Option 2: Bootstrapping by reusing already allocated external IP addresses](#option-2-bootstrapping-by-reusing-already-allocated-external-ip-addresses)
    - [Option 3: Bootstrapping manually](#option-3-bootstrapping-manually)
  - [Interacting with your network](#interacting-with-your-network)
    - [Access the interactive shell of the network services and notary](#access-the-interactive-shell-of-the-network-services-and-notary)
    - [How to join your network](#how-to-join-your-network)
    - [Display logs](#display-logs)
    - [Display configuration files used for each CENM service](#display-configuration-files-used-for-each-cenm-service)
      - [Overwriting default configuration](#overwriting-default-configuration)
    - [Unwinding your environnement](#unwinding-your-environnement)
      - [Unwinding the whole environment (including IPs)](#unwinding-the-whole-environment-including-ips)
  - [Managing your network](#managing-your-network)
    - [Updating network parameters](#updating-network-parameters)
    - [Running flag day](#running-flag-day)
    - [Canceling network parameters update](#canceling-network-parameters-update)

### Docker images and JDK supported

CENM docker images are based on `azul/zulu-openjdk:8u242`

Each CENM service has dedicated docker image. They are designed to be minimal and optimized to run on Kubernetes cluster.
They are **not** designed to run as standalone docker containers. They are stored in Docker Hub:

{{< table >}}

| CENM service     | Docker Hub                         | Tag                   |
| ---------------- | ---------------------------------- | --------------------- |
| Identity Manager | corda/enterprise-identitymanager   | 1.2-zulu-openjdk8u242 |
| Network Map      | corda/enterprise-networkmap        | 1.2-zulu-openjdk8u242 |
| PKI Tool         | corda/enterprise-pkitool           | 1.2-zulu-openjdk8u242 |
| Signer           | corda/enterprise-signer            | 1.2-zulu-openjdk8u242 |
| Notary           | corda/notary                       | 1.2-zulu-openjdk8u242 |

{{< /table >}}

All helm charts by default use CENM docker images with tag `1.2-zulu-openjdk8u242`.

{{< note >}}
The use of different CENM versions on the same network is not supported - all services on a given network must be on the same CENM version.
{{< /note >}}

### Helm charts

#### Requirements

The following requirements are needed in order to deploy CENM correctly:

- [Helm](https://helm.sh/) >=3.1.1
- [Kubernetes](https://kubernetes.io/) >=1.8

#### Usage notes

- These charts are supposed to be a reference installation.
- They allow to configure several variables related to each CENM service.

#### Compatibility

These charts are compatible with Corda Enterprise Network Manager (CENM) version 1.2. Earlier CENM releases are not supported.

Each CENM service has its own dedicated folder with more detailed documentation.

| Helm Chart                                         |
| -------------------------------------------------- |
| [Identity Manager](deployment-kubernetes-idman.md) |
| [Signer](deployment-kubernetes-signer.md)          |
| [Network Map](deployment-kubernetes-nmap.md)       |
| [Corda Notary](deployment-kubernetes-notary.md)    |

The charts are currently developed and tested against
[Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-gb/services/kubernetes-service/).

## General information about this deployment

All CENM 1.2 services run inside a single, dedicated Kubernetes namespace (the default name is `cenm`). Each service runs in its own dedicated Kubernetes pod.

The CENM network is bootstrapped with PKI certificates which default to sample
X.500 subject names (e.g. Identity Manager certificate subject is
“CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US”).
The subject names of the whole PKI Certificate Hierarchy can be configured in
the Signer Helm chart. For more information about Signer helm chart refer to
[Signer](deployment-kubernetes-signer.md).

There are three ways of bootstrapping a new CENM environment:

1. scripted (`bootstrap.cenm`) with **allocating new** public IP addresses
2. scripted (`bootstrap.cenm`) with  **reusing** already allocated public IP addresses
3. manually run each helm command

In case of initial bootstrap process it is recommended to use the first method.

The first two bootstrapping methods uses default values stored in values.yaml file in each helm chart. To fully customize new environment use third method.

Note: Identity Manager and Notary require their public IPs to be known in advance as this is required while running PKI Tool (part of Signer helm chart) and Notary registration.

Be aware that it might take a few minutes to allocate new IP address. In case of subsequent bootstrapping it is possible to reuse existing external IP addresses. NetworkMap and Signer have their public IP addresses allocated while bootstrapping and they don't need to be known in ahead of time.

Public IP addresses are allocated using Kubernetes `Service` defined with `type: LoadBalancer`

### Memory requirements

The following table represents memory requirements for each CENM component based on default value of `cordaJarMx` from `values.yaml` in each chart:

| Component         | cordaJarMx (GB) | max memory for service JVM (-Xmx) (GB) | K8s requests (GB) | K8s limits (GB) |
| ----------------- | --------------- | -------------------------------------- | ----------------- | --------------- |
| Identity Manager  |  1              | cordaJarMx                             | cordaJarMx        | cordaJarMx + 2  |
| Signer            |  1              | cordaJarMx                             | cordaJarMx        | cordaJarMx + 2  |
| Network Map       |  1              | cordaJarMx                             | cordaJarMx        | cordaJarMx + 2  |
| Notary            |  3              | cordaJarMx                             | cordaJarMx        | cordaJarMx + 2  |

Note: Kubernetes cluster should have at least 8 GB of **free memory** available to all CENM services.

## Deploying your network

### Prerequisite

Before proceeding you will need the following:

1. all required dependencies installed
2. an AKS cluster up and running and access to it from your local machine
3. a storage class (`cenm`) and new namespace (`cenm`) with the correct RBAC permissions.
4. obtain the helm charts and deployment scripts

#### (1) Install dependencies

- Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Install [helm](https://helm.sh/docs/intro/install/)

Ensure that `helm version` gives you `version` field with any value greater than or equal to 3.1.1 - for instance:

```bash
version.BuildInfo{Version:"v3.1.2", GitCommit:"afe70585407b420d0097d07b21c47dc511525ac8", GitTreeState:"clean", GoVersion:"go1.13.8"}
```

#### (2) Set up and connect to a cluster on Azure

- Create a cluster on Azure. Microsoft provide a [quick start guide](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough)
  although note you will need a Kubernetes cluster with at least 6 GB of free memory available to all CENM services.

- Ensure you have [Azure CLI installed](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) on your machine
- Ensure you have your cluster subscription [as your active subscription](https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest#az-account-set)
- [Connect to your cluster](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough-portal#connect-to-the-cluster)

#### (3) Create storage class, namespace and RBAC

Run the following instruction once the previous points have been cleared:

`All examples below are using namespace **cenm**`

> Note: edit k8s/cenm.yaml and modify RoleBinding/everything-in-cenm to include your user(s) Azure group

```bash
kubectl apply -f k8s/cenm.yaml  # Run as Kubernetes privileged user
export nameSpace=cenm
kubectl config set-context $(kubectl config current-context) --namespace=${nameSpace}
```

You can verify this with `kubectl get ns`

#### (4) Download helm charts and installation scripts

You can find the files required in the following steps on the [CENM deployment repo](https://github.com/corda/cenm-deployment).

----

### Option 1: Bootstrapping by allocating new external IP addresses

To bootstrap new CENM environment with allocating new, external IP run:

```bash
cd k8s/helm
./bootstrap.cenm
```

Note: obtaining IP addresses might take up to 10 minutes

The script exits after all bootstrapping processes on Kubernetes cluster have been started. The process will continue to run on the cluster after the script has exited. You can monitor the completion of the deployment with:

``` bash
kubectl get pods -o wide
```

### Option 2: Bootstrapping by reusing already allocated external IP addresses

It is possible that external IPs have been already allocated - in this case it is possible to reuse them by specifying their services names:

```bash
cd k8s/helm
./bootstrap.cenm -i idman-ip -n notary-ip
```

### Option 3: Bootstrapping manually

There are several helm commands used to bootstrap new CENM environment, each one creates one CENM service (signer, identity manager, etc). They need to be run in the correct order.

```bash
cd k8s/helm

# these helm charts trigger public IP allocation
helm install idman-ip idman-ip
helm install notary-ip notary-ip

# run these commands to display allocated public IP addresses:
kubectl get svc --namespace cenm idman-ip --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"   # step 1
kubectl get svc --namespace cenm notary-ip --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"  # step 2

# these helm charts bootstrap all CENM services
helm install signer signer --set idmanPublicIP=[use IP from step 1]
helm install idman idman
helm install notary notary --set notaryPublicIP=[use IP from step 2]
helm install nmap nmap

# run these commands to display allocated public IP addresses for Signer and NetworkMap:
kubectl get svc --namespace cenm signer --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"
kubectl get svc --namespace cenm nmap --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"
```

## Interacting with your network

### Access the interactive shell of the network services and notary

To access Identity Manager, Signer, Network Map or Notary use the following instruction:

```bash
ssh -p <shell.sshdPort> -l <shell.user> <IP Address>
```

- IP addresses are dynamically allocated for each deployment and can be found with `kubectl get svc`
- ssh port and user are specified in [Helm charts configurations](#Helm-charts) for each service
- you will be asked a password for each service, which can be found [Helm charts configurations](#Helm-charts) for each service

Note: make sure that you are pointing at the correct namespace - check with:

```bash
kubectl config current-context && kubectl config view --minify --output 'jsonpath={..namespace}' && echo`)
```

### How to join your network

To configure Corda node to connect to the CENM services, edit the following properties in your `node.conf` file:

```bash
networkServices {
  doormanURL="http://<IDENTITY-MANAGER-IP>:10000"
  networkMapURL="http://<NETWORK-MAP-IP>:10000"
}
```

- the `doormanURL` property is the public IP address and port of the Identity Manager service.
- the `networkMapURL` is the pubic IP address and port of the Network Map service.

Note: to obtain public IPs of Identity Manager and Network Map use:

```bash
kubectl get svc idman-ip notary-ip
```

Also upload the `network-root-truststore.jks` to your Corda node. You can download it locally from CENM Signer using the following command:

```bash
kubectl cp <name-space>/<signer-pod>:DATA/trust-stores/network-root-truststore.jks network-root-truststore.jks
```

Namespace is set to `cenm` in this deployment, to obtain the pod name for the signer use:

```bash
kubectl get pods -o wide`
```

Truststore password can be found in the `signer/files/pki.conf`, the default value used in this helm chart:  `trust-store-password`

For more details about joining CENM network see: [Joining an existing compatibility zone](https://docs.corda.net/releases/release-V4.3/joining-a-compatibility-zone.html?highlight=registration#joining-an-existing-compatibility-zone)

### Display logs

Each CENM service has dedicated sidecar to displays live logs from `log/` folder.

To display logs use the following command:

```bash
kubectl logs -c logs <pod-name>
```

To display live logs use the following command:

```bash
kubectl logs -c logs -f <pod-name>
```

### Display configuration files used for each CENM service

Each service stores configuration file in `etc/` folder in a pod. I.e.: to display what is in the Identity Manager `etc/` folder run these commands:

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

#### Overwriting default configuration

Default setting used in CENM services configuration values can be altered by:

1. changing values in values.yaml
1. preparing another yaml file with new values and passing it with `-f` flag (i.e.: `helm install -f myvalues.yaml idman`)
1. individual parameters passed with `--set` (such as `helm install --set foo=bar idman`)
1. any combination of the above (i.e.: `helm install -f myvalues.yaml --set foo=bar idman`)

For more information refer to the official helm documentation: https://helm.sh/docs/chart_template_guide/values_files/

### Unwinding your environnement

There are two ways to destroy CENM environment:

- destroy the whole environment
- destroy all CENM objects without deleting allocated external IP addresses

#### Unwinding the whole environment (including IPs)

```bash
helm delete nmap notary idman signer notary-ip idman-ip
```

#### Unwinding the whole environment without deleting IPs

If you run several ephemeral test network in your development cycle you might want to keep your IP addresses to speed up the process:

```bash
helm delete nmap notary idman signer
```

## Managing your network

### Updating network parameters

CENM 1.2 allows to update network parameters without restarting Network Map. Take the following steps to update network parameters:

- Login to Network Map pod and edit `etc/network-parameters-update-example.conf` file:

```bash
kubectl exec -it [name of nmap pod] bash
vim etc/network-parameters-update-example.conf
[update the file, save and exit]
```

- Connect to Network Map ssh console:

```bash
ssh -p [nmap ssh port] -l nmap [nmap public IP address]
```

and run the following commands:

```bash
run networkParametersRegistration networkParametersFile: etc/network-parameters-update-example.conf, \
networkTrustStore: DATA/trust-stores/network-root-truststore.jks, \
trustStorePassword: trust-store-password, \
rootAlias: cordarootca

```

### Running flag day

Once the set date/time has passed run the following in the Network Map ssh console:

```bash
run flagDay
```

Note: For the changes to be advertised to the nodes the new network map has to be signed by signer and it is scheduled according to its configuration.

### Canceling network parameters update

To cancel flag day:

```bash
run cancelUpdate
```

Note: The following files are part of the default deployment:

```bash
etc/network-parameters-update-example.conf
DATA/trust-stores/network-root-truststore.jks
```

Visit CENM official documentation for more information about network parameters:

- [Updating Network Parameters](updating-network-parameters.md)
- [Network Parameters List](config-network-parameters.md)
