---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "bankinabox"
    identifier: bank-in-a-box-installation-guide
tags:
- Bank in a Box
- installation
title: Getting started with Bank in a Box
weight: 100
---

# Getting started with Bank in a Box

Follow this guide to set up Bank in a Box so you can start testing its features and see how a banking application can be implemented on Corda.

## Prerequisites

Testing the Bank in a Box CorDapp or building your own banking CorDapp both require some Corda programming knowledge. If you are new to Corda, read about [Corda key concepts](../../corda-os/4.7/key-concepts.md) and [CorDapps](../../corda-os/4.7/cordapp-overview.md) to get up to speed.

Follow the general instructions for [Getting set up](../../corda-os/4.7/getting-set-up.md) to develop CorDapps once you are ready to get started with Bank in a Box.

You will also need the following to work on Bank in a Box:

* A basic [Kubernetes](https://kubernetes.io/docs/setup/) cluster configured, either hosted locally or in a cloud provider environment. The Kubernetes cluster must have access to a private Docker repository to obtain Bank in a Box Docker images.
* Your local operating system should be Linux, macOS, or a Unix-compatible environment for Windows (for example, [Cygwin](https://www.cygwin.com/install.html)) as the deployment uses Bash scripts.
* [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/) / [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/).
  {{< note >}}
  This is only required if you are running the deployment in a local Kubernetes cluster. If you do install Docker Desktop, this process will also automatically install kubectl and Docker.
  {{< /note >}}
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
* [Docker](https://www.docker.com/get-started).
* [Helm](https://helm.sh/docs/intro/install/).

Bank in a Box has the following computational requirements:

* Memory: 6 Gibibytes
* CPU: 2000m (2 full cores)

### Notes on Kubernetes cluster setup

If you are new to working with Kubernetes, we strongly recommend using Docker Desktop to run the deployment in a local Kubernetes cluster. This will simplify the deployment process and allow you to get Bank in a Box up and running quickly.

If you have intermediate experience working with Kubernetes and wish to set up your own Kubernetes cluster using Minikube, the `volumeHost` value must be set to `minikube`. Memory requirements must also be adjusted for [MiniKube](https://minikube.sigs.k8s.io/docs/faq/).

## Compatibility

The deployed network runs on:

* Kubernetes - version 1.16.9 or higher.
* Helm - ensure that the value in the version field for `helm
 version` is **3.2** or higher, as shown in the example below:

 ```
 version.BuildInfo{Version:"v3.3.4", GitCommit:"a61ce5633af99708171414353ed49547cf05013d", GitTreeState:"dirty", GoVersion:"go1.15.2"}
```

{{< note >}}
Corda version is enforced in the Docker file used later.
{{< /note >}}


## Deployment

The provided deployment runs all Bank in a Box services inside a single, dedicated Kubernetes namespace (default `name:default`). Each service runs in its own dedicated Kubernetes pod:

 * `bank` (Corda node with Bank in a Box CorDapp).
 * `oracle` (Corda node with Bank in a Box CorDapp).
 * `notary` (Corda notary node).
 * `credit-rating-server` (Spring Boot dummy credit rating server).
 * `web-api-server` (Bank in a Box Web API exposed via Spring Boot).
 * `bank-in-a-box` FE (Bank in a Box front end React application).

The Bank in a Box Corda network is bootstrapped with PKI certificates, and sample X.500 subject names are provided as defaults (for example, the Bank certificate subject is `O=Bank,L=London,C=GB`).

Follow the steps below to run your deployment.

### Clone the Bank in a Box repository

Run the following command to clone the [Bank in a Box repository](https://github.com/corda/bank-in-a-box).

```
git clone https://github.com/corda/bank-in-a-box
```


### Set up your database

Bank in a Box services are pre-configured to use embedded H2 databases by default. No further setup is needed if an H2 database is sufficient for your needs.

You may wish to use an external database configuration if you want to check database changes while you are running the application. In this case you will need to install a database (or databases), set up users and permissions, and change database configuration options for Bank in a Box services before starting those services. See the sample PostgreSQL installation guide and explanation of Bank in a Box external database support configuration options below for instructions.

#### External database support
You can configure the services to use an external database. A database can be installed as a pod inside the same Kubernetes cluster or as a separate installation outside the Kubernetes cluster. The example below shows a PostgresSQL installation that runs inside the same Kubernetes cluster where Bank in a Box runs.

You can install a PostgreSQL database inside the Kubernetes cluster using a third-party Bitnami Helm chart:

```
$ helm repo add bitnami https://charts.bitnami.com/bitnami
helm install bank-in-a-box-database bitnami/postgresql
```

Follow the instructions displayed by the script output to connect to the database server via PSQL. You can create a separate database server for each Bank in a Box service by running the Helm script multiple times with different names and then setting up the database user/schema, following the instructions in the [Corda database setup documentation](../../corda-enterprise/4.7/node-database-intro.md).
Alternatively, you can create several databases inside the single PostgresSQL server you have just deployed, by running the following DDL commands:

```
CREATE DATABASE <DATABASE>;
CREATE USER <USER> WITH PASSWORD '<PASSWORD>';
GRANT ALL PRIVILEGES ON DATABASE <USER> to <DATABASE>;
```
For each service (Bank, Web API server), use different `<DATABASE>` name and `<USER>` - for example, `bankdb` / `bankuser`
for the Bank node.

The database used by each service is configured via JDBC URL and is defined in the `values-<service-name>.yml` file for
the Helm chart of the respective service - for example, `helm/bank-in-a-box/values-bank.yaml` for the Bank node. In the
`values-bank.yaml.yml` file, edit the database section of the configuration to change the JDBC URL, user, and password.

The deployed service already contains JDBC drivers for PostgreSQL. For other RDBMS's, you need to extend
the Docker images for the service by adding the database JDBC driver `.jar` file to the `/opt/corda/drivers/` directory.

Example settings for connection to a PostgreSQL database follow below:

```
dataSource:
 className: "org.postgresql.Driver"
 url: "jdbc:postgresql://<HOST>:<PORT>/<DATABASE>"
 user: "<USER>"
 password: "<PASSWORD>"
```

In this example, `<HOST>` is a placeholder for the host name of the server, `<PORT>` is a placeholder for the port number the server is listening on (typically 5432 for PostgreSQL), `<DATABASE>` is a placeholder for the database name, and `<USER>` and `<PASSWORD>` are placeholders for the access credentials of the database user.


#### Database troubleshooting

Persistent volume creation is configured to occur in the `/tmp` directory by default. If you do not have write access to this directory, persistent volume creation will fail. To resolve this, open the `volume-corda-node.yaml` file (full path: `helm/bank-in-a-box/templates/volume-corda-node.yaml`) and edit the `path` value to a directory where you do have write access.


### Build `.jar` files

The following projects must be built to run Bank in a Box:

- `workflows`
- `contracts`
- `credt-rating-oracle`
- `clients`
- `webservices`


To build your `.jar` files from source code, `cd` into the root of [the repository cloned above](#clone-the-bank-in-a-box-repository) and execute the following commands:

`./gradlew workflows:jar`

`./gradlew contracts:jar`

`./gradlew credit-rating-oracle:jar`

`./gradlew clients:bootJar`

`./gradlew webservices:bootJar`

If the builds were successful, you will receive a message similar to the following after each command is run:

```
BUILD SUCCESSFUL in 6s
9 actionable tasks: 2 executed, 7 up-to-date
```


### Set up Docker images

To build your images from source code, `cd` into the root of [the repository cloned above](#clone-the-bank-in-a-box-repository) and execute the following commands to build a Corda node, the credit rating server, web api server, and front-end images:

```
docker build -t bank-in-a-box:0.0.1 -f docker/corda-node/Dockerfile .
```

```
docker build -t credit-rating-server:0.0.1 -f docker/credit-rating-server/Dockerfile .
```

```
docker build -t web-api-server:0.0.1 -f docker/web-api-server/Dockerfile .
```

```
docker build -t front-end:0.0.1 clients/FrontEnd/bank-in-a-box/.
```

Each of the commands should produce successful logs when they have finished running, which should look similar to:

```
Successfully built b968bc83a185
Successfully tagged bank-in-a-box:0.0.1
```

To verify that images are present in the Docker repository execute the ```docker images``` command which will produce the following response if all images have been built:

```
$ refapp user$ docker images
REPOSITORY                                  TAG                                              IMAGE ID            CREATED             SIZE
bank-in-a-box                               0.0.1                                            b968bc83a185        6 hours ago         785MB
web-api-server                              0.0.1                                            1e4ee85b2232        7 hours ago         507MB
credit-rating-server                        0.0.1                                            e879850b7b0f        7 hours ago         459MB
front-end                                   0.0.1                                            52d04dea84f2        7 minutes ago      27MB
```

### `helm install`

To install Bank in a Box services to the Kubernetes cluster, use the `helm install` command. The installation command must be triggered from the `helm` directory of the [the repository cloned above](#clone-the-bank-in-a-box-repository).

1. Navigate to the `helm` directory.
```
cd helm
```

2. Install the Corda Bank node by invoking `helm install bank bank-in-a-box -f bank-in-a-box/values-bank.yaml`.
```
$ helm install bank bank-in-a-box -f bank-in-a-box/values-bank.yaml
NAME: bank
LAST DEPLOYED: Tue Oct 27 10:14:28 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

3. Install the Corda Notary node by invoking `helm install notary bank-in-a-box -f bank-in-a-box/values-notary.yaml`.
```
$ helm install notary bank-in-a-box -f bank-in-a-box/values-notary.yaml
NAME: notary
LAST DEPLOYED: Tue Oct 27 10:14:47 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

4. Install the Corda Oracle node by invoking `helm install oracle bank-in-a-box -f bank-in-a-box/values-oracle.yaml`.
```
$ helm install oracle bank-in-a-box -f bank-in-a-box/values-oracle.yaml
NAME: oracle
LAST DEPLOYED: Tue Oct 27 10:14:38 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

5. Install the Spring Boot Credit Rating Server `helm install credit-rating-server web-server -f web-server/values-credit-rating.yaml`.
```
$ helm install credit-rating-server web-server -f web-server/values-credit-rating.yaml
NAME: credit-rating-server
LAST DEPLOYED: Tue Oct 27 09:30:42 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

6. Install the Spring Boot Web API Server by invoking `helm install web-api-server web-server -f web-server/values-web-api.yaml`.
```
$ helm install web-api-server web-server -f web-server/values-web-api.yaml
NAME: web-api-server
LAST DEPLOYED: Tue Oct 27 09:33:01 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

7. Install the front end by invoking `helm install front-end frontend -f frontend/values.yaml`.
```
$ helm install front-end frontend -f frontend/values.yaml
NAME: front-end
LAST DEPLOYED: Wed Nov 11 15:42:59 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

To verify that all deployments have executed successfully and that all services are up and running, execute the `kubectl get pods` command, which should produce an output similar to the output shown below:
```
$ kubectl get pods
NAME                                              READY   STATUS    RESTARTS   AGE
corda-bank-deployment-7dd7cf6dff-6kvcm            1/1     Running   0          28m
corda-notary-deployment-6566db95f5-wrxlj          1/1     Running   0          28m
corda-oracle-deployment-68d4f7c94d-pzp5w          1/1     Running   0          28m
credit-rating-server-deployment-9448869d5-mcwrw   1/1     Running   0          23m
front-end-deployment-89789b549-6bpzl              1/1     Running   0          13s
web-api-server-deployment-6d8c46c966-8dv79        1/1     Running   1          28m
```

Depending on when the command is executed exactly, some pods may still be in `PENDING` status (approximately one minute is required for node initialisation).

### Service endpoints, display logs, and `exec` into container

At this point all Bank in a Box services are up. To expose ports for the services, use the `kubectl get svc` command:

```
$ kubectl get svc
NAME                             TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                                          AGE
corda-bank-service               LoadBalancer   10.110.157.133   localhost     40000:32731/TCP,30000:31319/TCP,2223:30535/TCP   90s
corda-notary-service             LoadBalancer   10.98.61.35      localhost     40004:30518/TCP,30003:32120/TCP,2224:32737/TCP   54s
corda-oracle-service             LoadBalancer   10.107.138.217   localhost     40007:32277/TCP,30005:32520/TCP,2224:31810/TCP   37s
credit-rating-server-service     LoadBalancer   10.110.82.80     localhost     8090:32172/TCP                                   14s
front-end-service                NodePort       10.108.228.92    <none>        3003:31270/TCP                                   21s
web-api-server-service           LoadBalancer   10.105.120.252   localhost     7777:31939/TCP                                   26s
```

In the output you can see all the exposed ports - for example, `corda-bank-service` has exposed port 40000 as the p2p port, port 30000 as rpc port, and port 2223 as the ssh port. All of the ports will be accessible to other services within the Kubernetes namespace. If you are accessing from outside of standard AWS or Azure clusters, you can use load balancers.

For local testing, the Kubernetes port forward feature can be used to forward ports to localhost `kubectl port-forward
 <pod_name> <local-ip>:<pod-ip>` :

```
$ kubectl port-forward web-api-server-deployment-6584b5fb97-gxtlp 7777:7777
```

In this example port 7777 is forwarded from pod `web-api-server-deployment-6584b5fb97-gxtlp` to localhost port 7777. In this way we can access all the endpoints from `web-api-server` pod on localhost.

After using the port forward feature, visit the corresponding `localhost` port in your browser to access the user interface (`front-end-service`).

To access the application logs, the Kubernetes tail log feature can be used `kubectl logs -f <pod_name>` :

```
$ kubectl logs -f web-api-server-deployment-6584b5fb97-zwwbj
I 10:30:39 1 ServerKt.logStartupProfileInfo - The following profiles are active: prod,pg
I 10:30:46 1 RepositoryConfigurationDelegate.registerRepositoriesIn - Bootstrapping Spring Data repositories in DEFAULT mode.
I 10:30:46 1 RepositoryConfigurationDelegate.registerRepositoriesIn - Finished Spring Data repository scanning in 581ms. Found 2 repository interfaces.
```

To `exec` into the running pod execute command `kubectl exec -it <pod_name> -- /bin/bash`
```
$ kubectl exec -it corda-bank-deployment-6cd6bbffd6-tlg4q   -- /bin/bash
corda@corda-bank-deployment-6cd6bbffd6-tlg4q:~$ ls
additional-node-infos  bin	certificates	     cordapps  drivers	network-parameters							   persistence	      persistence.trace.db  shell-commands  starting-node.conf
artemis		       brokers	config-exporter.jar  djvm      logs	nodeInfo-5D9023BC20666D632B1382B53A3AFF7874B1F14870BC841BFB2C70397665D126  persistence.mv.db  process-id	    ssh		    workspace
corda@corda-bank-deployment-6cd6bbffd6-tlg4q:~$
```
Once in the container, you can explore the contents of the running node file system, access log files, and evaluate environment variables.

### Delete deployment

You can list all Helm deployments using the following command:

```
$ helm list
NAME                 	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART                 	APP VERSION
bank                 	default  	1       	2020-10-27 16:44:56.637319 +0000 UTC	deployed	corda-0.0.1
credit-rating-server 	default  	1       	2020-10-27 16:46:12.616537 +0000 UTC	deployed	corda web server-0.0.1
web-api-server        default   1         2020-10-27 16:47:12.616546 +0000 UTC  deployed  corda web server-0.0.1
notary               	default  	1       	2020-10-27 16:45:32.606978 +0000 UTC	deployed	corda-0.0.1
oracle               	default  	1       	2020-10-27 16:45:49.806812 +0000 UTC	deployed	corda-0.0.1
```

You can delete each deployment via Helm:
```
$ helm delete web-api-server
release "web-api-server" uninstalled
```

You can also use a single command to delete all deployments:
```
$ helm delete bank credit-rating-server web-api-server notary oracle front-end
release "bank" uninstalled
release "credit-rating-server" uninstalled
release "web-api-server" uninstalled
release "notary" uninstalled
release "oracle" uninstalled
release "front-end" uninstalled
```

## Deployment customisation

The Kubernetes scripts provided are intended to be customised depending on customer requirements. The following sections describe how to customise various aspects of the deployment.

### Overriding service configuration

There are a number of settings provided on each Helm chart which allow easy customisation of common options.

To change the default settings used in the Bank in a Box service configuration, follow the [Helm guide](https://helm.sh/docs/chart_template_guide/values_files/).

In brief, you can achieve this in one of the following ways:

* Create a separate `yaml` file with new values and pass it with `-f` flag:
```
$ helm install oracle bank-in-a-box -f myvalues.yaml
```
* Override individual parameters using `--set`, for example:
```
$ helm install oracle bank-in-a-box -f bank-in-a-box/values-oracle.yaml --set foo=bar
```
* Any combination of the two options above, for example:
```
$ helm install oracle bank-in-a-box -f myvalues.yaml --set foo=bar
```

### Notes on front end deployment

When the front end is deployed with Docker and helm, helm values will override `config.js` values.

You can use `config.js` for environment variables if running the front end source code or performing testing.

In `config.js`, the `reccuringpaymentperiod` value is serialized as `Java.util.duration` and can be used for testing recurring payments in the application. By default this value is set to `P1D`, which will make the recurring payments occur daily. If this value is set to `PT1M`, the recurring payment will occur every minute, which will provide faster results when testing. Other intervals can of course be set following the appropriate `P{period}D` or `PT{period}M` value format to make the payment occur after the specified number of days or minutes respectively.
