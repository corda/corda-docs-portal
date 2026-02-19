---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-nodes-notary-config
tags:
- ha
- notary
- service
- setup
title: Setting up the notary service as highly available
weight: 110
---


# Setting up the notary service as highly available

The Corda notary service can be configured in high-availability (HA) mode. For the notary
service to operate in HA mode, a high-availability database is required. See [Notary service overview]({{< relref "ha-notary-service-overview.md" >}}) for more information.

Running an HA notary requires the following:

- JPA or MySQL notary implementations
- A database supported by the notary implementation, configured in high-availability mode

For a list of databases supported by each of the above notary implementations, see [Platform support]({{< relref "../platform-support-matrix.md" >}}).


## Prerequisites

Before setting up an HA notary, your Corda Enterprise distribution should contain all the following `.JAR` files,
configuration information, and capabilities:

* The notary worker and database machines need to be configured to use reliable and trusted time servers. The time
source has to be monotonic and support leap second smearing.
* Java runtime
* Corda Enterprise JAR
* [Notary health check]({{< relref "../notary-healthcheck.md" >}}) tool
* HA Utilities JAR to run [notary registration]({{< relref "../ha-utilities.md#notary-registration" >}})
* Root access to a Linux machine or VM to install the selected database
* The private IP addresses of your database hosts
* The public IP addresses of your notary hosts
* The database driver in the form of a `.JAR` file, located inside the "drivers" folder
* The relevant HSM library `.JAR` (if storing keys inside a HSM). See [cryptoservice configuration]({{ ref "../node/operating/cryptoservice-configuration.md" >}}) for more information.
* Database root password, used to create the Corda user, setting up the database and tables (only required for some installation methods)
* Corda database user password, used by the notary service to access the database
* State snapshot transfer (SST) database user password, used by the Percona cluster for data replication
* Network root truststore password
* Node keystore password
* Network root truststore
* Notary worker configuration files

If you are setting up a local network to test the HA notary setup process, use the [Network Bootstrapper]({{< relref "../network-bootstrapper.md" >}})
instead of the [HA Utilities Tool]({{< relref "../ha-utilities.md#notary-registration" >}}). In all other implementations, the Network Bootstrapper is not required.

Ensure that the notary worker P2P ports are reachable from any nodes that might join the network. Each notary worker also
needs access to its individual node database, and communicates with the underlying database cluster using JDBC.

When writing the notary worker’s `node.conf` file, the notary worker must have both a `myLegalName` and a `notary.serviceLegalName`
property. The `myLegalName` property must be unique to each notary worker, however, all notary workers in a cluster
must share the same `notary.serviceLegalName`. For more information, see [Node configuration]({{< relref "../node/setup/corda-configuration-file.md" >}}).


## Registering a HA notary

Before a HA notary cluster can be run:
- Each worker needs a valid certificate to join the network
- The HA notary service must be included in the network parameters.

The steps below assume the network includes an Identity Manager and
Network Map, and that the above prerequisites have been met.


### Step 1: Register the notary service identity

Before any workers can be started up, the HA notary service identity must be registered with the network's Identity Manager.
To do this:

- Run the [HA Utilities tool]({{< relref "../ha-utilities.md" >}}) using the notary workers `node.conf` file.

  The HA Utilities tool will generate the notary service key pair, and submit a corresponding certificate submission
request (CSR) to the Identity Manager, then poll until it receives a successful response.

  Once successful, a local `.jks`
file is created containing the key pair and certificate chain if using a local key store, or just the certificate
chain if using an HSM.

See [Notary registration]({{< relref "../ha-utilities.md#notary-registration" >}}) for more information on using the HA Utilities tool.


### Step 2: Register the notary workers

After the notary service is registered with the Identity Manager, each notary worker must be registered with the Identity
Manager. This process is similar to registering a standard Corda node, but the notary workers also require access to the
notary service key and certificate.

1. Copy the `.jks` file created when registering the notary service identity.
2. Create a copy in the `certificates/nodekeystore.jks`
directory for each notary worker.
3. If using a shared HA HSM, each notary worker must have a unique key alias to ensure
that there are no identity clashes between notary workers.
4. Register each notary worker using the Corda `initial-registration` command.

   After registration, the notary worker
identity and node CA entries will be added to the `certificates/nodekeystore.jks` store alongside the notary service
entry. If configured to use an HSM, the generated keys are stored in the HSM and not in the `.jks` file.

### Step 3: Add the notary service to the network parameters

In order for network participants to use the new HA notary the notary service must be present in the network parameters. This involves
configuring and setting the initial network parameters (if setting up a new network), or modifying the existing parameters and performing a
flag day (if using an existing network). See the {{< cenmlatestrelref "cenm/_index.md" "CENM documentation" >}} for more information on this
process.

{{< note >}}
CENM version 1.2+ supports setting of a notary within the network parameters solely via the X500 name. In this case it is possible to
add the HA notary to the network parameters before registering any worker nodes (that is, steps 2 and 3 can be done in any order). If a
CENM with version < 1.2 is being run then the HA notary can only be added to the parameters using a signed node info file, meaning that
at least one worker node needs to be registered first, and the resulting signed node info file should be copied over the to the Network
Map service.
{{< /note >}}
