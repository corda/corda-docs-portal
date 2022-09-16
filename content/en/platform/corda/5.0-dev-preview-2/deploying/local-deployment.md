---
date: '2022-09-13'
title: "Local Kubernetes cluster"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-deploy-local
    parent: corda-5-dev-preview-deploy-options
    weight: 2000
section_menu: corda-5-dev-preview
---

This section describes how to build and deploy Corda to a Kubernetes cluster on your local development machine.

## Create a Kubernetes cluster

The following instructions assume that you have a single-node Kubernetes cluster running with a Docker daemon.
Two options that meet these requirements and have been tested with these instructions are:

* [Docker Desktop](#install-and-configure-docker-desktop)
* [minikube](#install-minikube)

Docker Desktop provides a simpler user experience but commerical use in larger enterprises requires a paid subscription.
See [Do I need to pay to use Docker Desktop?](https://docs.docker.com/desktop/faqs/general/#do-i-need-to-pay-to-use-docker-desktop) for more details.

### Install and configure Docker Desktop

1. Install Docker Desktop.
   * [macOS](https://docs.docker.com/desktop/mac/install/)
   * [Windows](https://docs.docker.com/desktop/windows/install/)
   * [Linux](https://docs.docker.com/desktop/install/linux-install/)
2. [Enable Kubernetes](https://docs.docker.com/desktop/kubernetes/#enable-kubernetes) in Preferences.
3. Configure your Kubernetes cluster with at least 6 CPU and 8 GB RAM.
   * For macOS, configure the [resources](https://docs.docker.com/desktop/settings/mac/#resources) in the Docker Desktop Preferences.
   * For Linux, configure the [resources](https://docs.docker.com/desktop/settings/linux/#resources) in the Docker Desktop Preferences.
   * For Windows, configure the WSL settings in the [.wslconfig](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configuration-setting-for-wslconfig) file.

### Install minikube

1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/).
2. Start minikube with at least 8 GB memory and 6 CPUs:

    ```sh
    minikube start --memory 8000 --cpus 6
    ```

3. If you don't already have the `kubectl` CLI installed, set up the following alias:

    ```sh
    alias kubectl="minikube kubectl --"
    ```

## Setup for Helm installation

The Kubernetes configuration for Corda is packaged in a Helm chart.
The chart is installed into a Kubernetes namespace using the Helm CLI.

### Install Helm

1. [Install the Helm CLI](https://helm.sh/docs/intro/install/).

### Create a Kubernetes namespace

1. If you have multiple Kubernetes clusters, ensure that you are targeting the `kubectl` context for the correct cluster.
    You can list contexts you have defined with:

    ```sh
    kubectl config get-contexts
    ```

    The current context is marked with an asterisk.
    You can switch context, for example:

    ```sh
    kubectl config use-context docker-desktop
    ```

    If you are using Docker Desktop, you can also switch context via the Kubernetes sub-menu.

2. Create a namespace to contain your Corda deployment.
    For example, to create a namespace called `corda` run the command:

    ```sh
    kubectl create namespace corda
    ```

{{< note >}}
The commands that follow all assume that you are using a namespace called `corda`.
Modify the `-n corda` option on each `kubectl` command if you use a different namespace.
{{< /note >}}

## Install Corda pre-requisites

Corda requires a PostgreSQL and Kafka instance as pre-requisites.
One option to obtain these in a local development environment is via the umbrella Helm chart in the [corda/corda-dev-helm](https://github.com/corda/corda-dev-helm) GitHub repository.

1. Clone the GitHub repository:

    ```sh
    git clone https://github.com/corda/corda-dev-helm.git
    cd corda-dev-helm
    ```

2. Pull the child Kafka and PostgreSQL charts provided by Bitnami:

    ```sh
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm dependency build charts/corda-dev
    ```

3. Install the Helm chart:

    ```sh
    helm install prereqs -n corda charts/corda-dev --render-subchart-notes --timeout 10m --wait
    ```

    The `--wait` option ensures all of the pods are ready before returning. The `--render-subchart-notes` option gives you a brief overview of the connection details.
    The timeout is set to 10 minutes to allow time to pull the images from Docker Hub.
    The process should take significantly less time than this on subsequent installs.

## Build the Corda Docker images

The Corda Docker images must be built from source.

1. If you’re using minikube, configure your shell to use the Docker daemon inside minikube so that built images are available directly to the cluster:

    {{< tabs name="Setting Docker environment for minikube">}}
    {{% tab name="Bash"%}}

```bash
eval $(minikube docker-env)

    {{% /tab %}}

    {{% tab name="PowerShell" %}}

```pwsh
minikube docker-env --shell=powershell | Invoke-Expression

    {{% /tab %}}
    {{< /tabs >}}

2. Clone the [corda/corda-cli-plugin-host](https://github.com/corda/corda-cli-plugin-host) repository:

    ```sh
    git clone https://github.com/corda/corda-cli-plugin-host.git
    git -C corda-cli-plugin-host checkout release/version-1.0.0-DevPreview2
    ```

3. Clone the [corda/corda-api](https://github.com/corda/corda-api) repository:

    ```sh
    git clone https://github.com/corda/corda-api.git
    git -C corda-api checkout release/os/5.0-DevPreview2
    ```

4. Clone the [corda/corda-runtime-os](https://github.com/corda/corda-runtime-os) repository:

    ```sh
    git clone https://github.com/corda/corda-runtime-os.git
    git -C corda-runtime-os checkout release/os/5.0-DevPreview2
    ```

5. Build all of the Corda Docker images with Gradle in the `corda-runtime-os` repository:

    ```sh
    cd corda-runtime-os
    ./gradlew clean publishOSGiImage -PcompositeBuild=true
    ```

## Install Corda

There is a `values.yaml` file at the root of the `corda-runtime-os` repository that overrides the default values in the Corda Helm chart.
These values configure the chart to use the images you just built and specify the location of the Kafka and PostgreSQL instances created by the `corda-dev` Helm chart.
They also set the initial admin user password to `admin`.

1. Install the chart as follows by running from the root of the `corda-runtime-os` repository:

   ```sh
   helm install corda -n corda charts/corda --values values.yaml --wait
   ```

When the commmand completes, the RPC endpoint should be ready to access.

### Troubleshooting

If the install times out, it indicates that not all of the worker pods reached ready state.
Use the following command to list the pods and their current state:

```sh
kubectl get pods -n corda
```

If a particular pod is failing to start, run the following command to get more details using the name of the pod from the previous output:

```sh
kubectl describe pod -n corda corda-rpc-worker-8f9f5565-wkzgq
```

If the pod is continually restarting, it is likely that Kubernetes is killing it because it does not reach a healthy state. Check the pod logs, for example:

```sh
kubectl logs -n corda corda-rpc-worker-8f9f5565-wkzgq
```

## Access the Corda cluster

1. To access the RPC endpoint, forward the port by running the following command in a second terminal window:

   ```sh
   kubectl port-forward -n corda deploy/corda-rpc-worker 8888
   ```

2. The Swagger documentation for the RPC endpoint can then be accessed at [https://localhost:8888/api/v1/swagger](https://localhost:8888/api/v1/swagger).
Note that the RPC endpoint is protected by a self-signed certificate.

3. The RPC endpoint can be invoked through the Swagger UI using the username `admin` and password `admin` or via curl, for example:

   ```sh
   curl -u admin:admin -k https://localhost:8888/api/v1/hello
   ```

## Clean up

The quickest route to clean up is to delete the entire Kubernetes namespace:

```sh
kubectl delete ns corda
```
