---
title: "Release notes"
date: 2020-01-08T09:59:25Z
---


# Release notes

## Corda Enterprise 4.1
This release extends [Corda Enterprise 4](https://docs.corda.r3.com/releases/4.0/release-notes-enterprise.html) with additional
                support for Futurex HSM (hardware security module) signing devices, and improved security for HTTPS proxy configurations.

Corda Enterprise 4.1 supports Linux for production deployments, with Windows and macOS support for development and demonstration purposes only. Please refer to product documentation for details.

Corda Enterprise 4.1 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.0 and 3.x, while providing enterprise-grade features and performance.


{{< note >}}
The compatibility and interoperability assurances apply to nodes running at the latest patch level for any given integer version.
                    For example, at the time of writing, the Corda Enterprise 4.1 interoperability and compatibility assurance is with respect to Corda 3.4, Corda Enterprise 3.3, Corda 4.1 and Corda Enterprise 4.0.


{{< /note >}}

### Key new features and components

* **Futurex Hardware Security Module (HSM) support**

Support for node legal identity keys in [Futurex Excrypt SSP9000](https://www.futurex.com/products/excrypt-ssp9000) hardware security
                            modules providing clients with increased security.
                            HSMs are standard in many enterprise organizations to store and safeguard cryptographic keys in tamper-proof hardware.

See [Futurex HSM support](cryptoservice-configuration.md#hsm-futurex-ref) for more information.


* **HTTPS Proxy authentication support**

Corda allows a node to use an HTTPS proxy when communicating with the Identity Manager (previously known as Doorman) and Network Map.
                            This release improves security by adding username/password authentication configuration support for these proxies.
                            Note: this security capability is already present for Corda Firewall SOCKS proxies.

Please refer to the [Network Services configuration](corda-configuration-file.md#corda-configuration-file-networkservices) section within the general
                            [Node Configuration](corda-configuration-file.md) document for further details.



### Further improvements, additions and changes

* Database schema generation fix and documentation clarifications: Corda Enterprise 4.1 should use the *runMigration* flag when running against non-H2
                            databases and the *initialiseSchema* flag when running against an H2 database. See [Database properties](corda-configuration-file.md#database-properties-ref).



{{< note >}}
in Corda Enterprise 4.0 the *initialiseSchema* migration flag was being used for both H2 and non-H2 databases (causing automatic updating
                        of the nodes database schema by default).


{{< /note >}}

* Improved error messages for non composable serialized types, to include *reason* and *remedy* information.


* Improved performance in attachments classloading, specifically in overlap checking across multiple versions of the same contract JAR.


* Improved firewall logging: log current active connection count.


* Disabled the default loading of `hibernate-validator` as a plugin by hibernate when a CorDapp depends on it. This change will in turn fix
                            [this issue](https://github.com/corda/corda/issues/4444) because nodes will no longer need to add `hibernate-validator` to the `\libs` folder.


* Liquibase now creates custom CorDapp schemas in H2 databases.


* AMQP protocol handshake tuning: aligned timeouts for CRL retrieval and TLS handshaking.


* Improved exception handling and reporting around failed flows.


* Updated proton-j library to latest version.


* Improved logging around serialization evolution.


* Artemis producers and consumers now use separate sessions.


* Artemis now handles message executor thread being interrupted by tests.


* Notary healthcheck includes transaction network parameters hash checking.


* Improved Cloud and Docker documentation. See [Corda Enterprise cloud images](node-cloud.md) and [Official Corda Docker Image](docker-image.md).


* Additional documentation on signature constraints. See [Signature Constraints](api-contract-constraints.md#signature-constraints).


* Database tables are now fully documented. See [Database tables](node-database-tables.md).


* Users of the (Percona cluster) HA Notary Service must now manually install the associated mySQL JDBC Driver for every worker node. See
                            [notary installation page](running-a-notary-cluster/installing-the-notary-service.md#mysql-driver) for more information.



### Known issues
Please refer to same section in [Corda Enterprise 4](https://docs.corda.r3.com/releases/4.0/release-notes-enterprise.html)


### Upgrade notes
As per previous major releases, we have provided a comprehensive upgrade notes ([Upgrading CorDapps to Corda Enterprise 4.1](app-upgrade-notes-enterprise.md)) to ease the upgrade
                    of CorDapps to Corda Enterprise 4.1. In line with our commitment to API stability, code level changes are fairly minimal.

For **developers**, switching CorDapps built using Corda (open source) 4.x to Corda Enterprise 4.1 is mostly effortless,
                    and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
ext.corda_release_version = '4.1'
ext.corda_release_distribution = 'com.r3.corda'
```
For **node operators**, it is advisable to follow the instructions outlined in [Upgrading a Corda Node](node-upgrade-notes.md).


{{< note >}}
In a mixed-distribution network the open source finance contract CorDapp should be deployed on both Corda 4.x (open source) and Corda Enterprise 4.1 nodes.


{{< /note >}}
Visit the [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
                    Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).


