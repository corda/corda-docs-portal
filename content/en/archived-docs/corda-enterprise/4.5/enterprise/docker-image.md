---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes
tags:
- docker
- image
title: Official Corda Docker image
weight: 120
---


# Official Corda Docker image

{{< note >}}
Note: Before running any Corda Docker images, you must accept the license agreement and indicate that you have done this by setting the environment variable `ACCEPT_LICENSE` to `YES` or `Y`. If you do not do this, none of the Docker containers will start.
{{< /note >}}

## Running a node connected to a Compatibility Zone in Docker

{{< note >}}
Requirements: A valid node.conf and a valid set of certificates - (signed by the CZ)
{{< /note >}}

In this example, the certificates are stored at `/home/user/cordaBase/certificates`, the node configuration is in `/home/user/cordaBase/config/node.conf` and the CorDapps to run are in `/path/to/cordapps`

```shell
docker run -ti \
        --memory=2048m \
        --cpus=2 \
        -v /home/user/cordaBase/config:/etc/corda \
        -v /home/user/cordaBase/certificates:/opt/corda/certificates \
        -v /home/user/cordaBase/persistence:/opt/corda/persistence \
        -v /home/user/cordaBase/logs:/opt/corda/logs \
        -v /path/to/cordapps:/opt/corda/cordapps \
        -p 10200:10200 \
        -p 10201:10201 \
        corda/corda-zulu-java1.8-4.5:latest
```

As the node runs within a container, several mount points are required:

* CorDapps - CorDapps must be mounted at location `/opt/corda/cordapps`
* Certificates - certificates must be mounted at location `/opt/corda/certificates`
* Config - the node config must be mounted at location `/etc/corda/node.config`
* Logging - all log files will be written to location `/opt/corda/logs`

If using the H2 database:

* Persistence - the folder to hold the H2 database files must be mounted at location `/opt/corda/persistence`

{{< note >}}
If there is no dataSourceProperties key in the node.conf, the docker container overrides the url for H2 to point to the persistence directory by default so that the database can be accessed outside the container

{{< /note >}}

## Running a node connected to a Bootstrapped Network

{{< note >}}
Requirements: A valid node.conf, a valid set of certificates, and an existing network-parameters file

{{< /note >}}
In this example, we have previously generated a network-parameters file using the bootstrapper tool, which is stored at `/home/user/sharedFolder/network-parameters`

```shell
docker run -ti \
        --memory=2048m \
        --cpus=2 \
        -v /home/user/cordaBase/config:/etc/corda \
        -v /home/user/cordaBase/certificates:/opt/corda/certificates \
        -v /home/user/cordaBase/persistence:/opt/corda/persistence \
        -v /home/user/cordaBase/logs:/opt/corda/logs \
        -v /home/TeamCityOutput/cordapps:/opt/corda/cordapps \
        -v /home/user/sharedFolder/node-infos:/opt/corda/additional-node-infos \
        -v /home/user/sharedFolder/network-parameters:/opt/corda/network-parameters \
        -p 10200:10200 \
        -p 10201:10201 \
        corda/corda-zulu-java1.8-4.5:latest
```

There is a new mount `/home/user/sharedFolder/node-infos:/opt/corda/additional-node-infos` which is used to hold the `nodeInfo` of all the nodes within the network.
As the node within the container starts up, it will place it’s own nodeInfo into this directory. This will allow other nodes also using this folder to see this new node.

## Generating configs and certificates

It is possible to utilize the image to automatically generate a sensible minimal configuration for joining an existing Corda network.

## Joining an existing Compatibility Zone

{{< note >}}
Requirements: A Compatibility Zone, the Zone Trust Root and authorisation to join said Zone.

{{< /note >}}
It is possible to use the image to automate the process of joining an existing Zone as detailed [here](network/joining-a-compatibility-zone.html#connecting-to-a-compatibility-zone)

The first step is to obtain the Zone Trust Root, and place it within a directory. In the below example, the Trust Root is stored at `/home/user/docker/certificates/network-root-truststore.jks`.
It is possible to configure the name of the Trust Root file by setting the `TRUST_STORE_NAME` environment variable in the container.

```shell
docker run -ti --net="host" \
        -e MY_LEGAL_NAME="O=EXAMPLE,L=Berlin,C=DE"     \
        -e MY_PUBLIC_ADDRESS="corda.example-hoster.com"       \
        -e NETWORKMAP_URL="https://map.corda.example.com"    \
        -e DOORMAN_URL="https://doorman.corda.example.com"      \
        -e NETWORK_TRUST_PASSWORD="trustPass"       \
        -e MY_EMAIL_ADDRESS="cordauser@r3.com"      \
        -e ACCEPT_LICENSE="YES"      \
        -e SSHPORT="2222"      \
        -e RPC_USER="PartyA"      \
        -v /home/user/docker/config:/etc/corda          \
        -v /home/user/docker/certificates:/opt/corda/certificates \
        corda/corda-zulu-java1.8-4.5:latest config-generator --generic --exit-on-generate
```

Several environment variables must also be passed to the container to allow it to register:

* `MY_LEGAL_NAME` - The X500 to use when generating the config. This must be the same as registered with the Zone.
* `MY_PUBLIC_ADDRESS` - The public address to advertise the node on.
* `NETWORKMAP_URL` - The address of the Zone’s network map service (this should be provided to you by the Zone).
* `DOORMAN_URL` - The address of the Zone’s doorman service (this should be provided to you by the Zone).
* `NETWORK_TRUST_PASSWORD` - The password to the Zone Trust Root (this should be provided to you by the Zone).
* `MY_EMAIL_ADDRESS` - The email address to use when generating the config. This must be the same as registered with the Zone.
* `ACCEPT_LICENSE` - Set to `YES` or `Y` to indicate that you have accepted the license agreement.
* `SSHPORT` - The port to use for SSH.
* `RPC_USER` - The RPC username.

There are some optional variables which allow customisation of the generated config:

* `MY_P2P_PORT` - The port to advertise the node on (defaults to 10200). If changed, ensure the container is launched with the correct published ports.
* `MY_RPC_PORT` - The port to open for RPC connections to the node (defaults to 10201). If changed, ensure the container is launched with the correct published ports.

Once the container has finished performing the initial registration, the node can be started as normal

```shell
docker run -ti \
        --memory=2048m \
        --cpus=2 \
        -v /home/user/docker/config:/etc/corda \
        -v /home/user/docker/certificates:/opt/corda/certificates \
        -v /home/user/docker/persistence:/opt/corda/persistence \
        -v /home/user/docker/logs:/opt/corda/logs \
        -v /home/user/corda/samples/bank-of-corda-demo/build/nodes/BankOfCorda/cordapps:/opt/corda/cordapps \
        -p 10200:10200 \
        -p 10201:10201 \
        corda/corda-zulu-java1.8-4.5:latest
```

# Performing Database Migrations

The image contains the database-migration tool. It is possible to run this in two modes within a container.

## Generating Migration Jars

In this mode, the database-migration tool will scan the provided CorDapps, and generate corresponding migration jars. These jars will be placed alongside
the source CorDapps. In this example, there are two CorDapps provided `corda-insurance.jar` and `corda-kyc.jar`

```shell
docker run -ti \
        -v /home/user/docker/docker/config:/etc/corda \
        -v /home/user/docker/docker/certificates:/opt/corda/certificates \
        -v /home/user/docker/docker/persistence:/opt/corda/persistence \
        -v /home/user/docker/docker/logs:/opt/corda/logs \
        -v /home/user/corda/samples/bank-of-corda-demo/build/nodes/BankOfCorda/cordapps:/opt/corda/cordapps \
        entdocker.software.r3.com/corda-enterprise-java1.8-4.5:latest db-migrate-create-jars
```

After the container has finished executing, there will be two new jars in `/home/user/corda/samples/bank-of-corda-demo/build/nodes/BankOfCorda/cordapps`: `migration-corda-insurance.jar` and `migration-corda-kyc.jar`.
These will then be loaded as normal CorDapps by the node on next launch.

## Executing Migrations on the Database

It is also possible to use the image to directly perform the migration of the database.

```shell
docker run -ti \
        -v $(pwd)/docker/config:/etc/corda \
        -v $(pwd)/docker/certificates:/opt/corda/certificates \
        -v $(pwd)/docker/persistence:/opt/corda/persistence \
        -v $(pwd)/docker/logs:/opt/corda/logs \
        -v $(pwd)/samples/bank-of-corda-demo/build/nodes/BankOfCorda/cordapps:/opt/corda/cordapps \
        entdocker.software.r3.com/corda-enterprise-java1.8-4.5:latest db-migrate-execute-migration
```

If the container is launched with the `db-migrate-execute-migration` command, the migration is directly applied to the database.
