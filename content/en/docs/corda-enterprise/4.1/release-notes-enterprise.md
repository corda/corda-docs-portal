---
aliases:
- /releases/4.1/release-notes-enterprise.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-release-notes-enterprise
    weight: 20
tags:
- release
- notes
- enterprise
title: Corda Enterprise 4.1 Release Notes
---

# Release notes

Corda Enterprise 4.1 is operationally compatible with Corda (open source) 4.x and 3.x, and Corda Enterprise 4.0 and 3.x, while providing enterprise-grade features and performance.

{{< note >}}
The compatibility and interoperability assurances apply to nodes running at the latest patch level for any given integer version.
For example, at the time of writing, the Corda Enterprise 4.1 interoperability and compatibility assurance is with respect to Corda 3.4, Corda Enterprise 3.3, Corda 4.1 and Corda Enterprise 4.0.
{{</ note >}}


## Key new features and components


* **Futurex Hardware Security Module (HSM) support**

  Support for node legal identity keys in `Futurex Excrypt SSP9000 <https://www.futurex.com/products/excrypt-ssp9000>`_ hardware security
  modules providing clients with increased security.
  HSMs are standard in many enterprise organizations to store and safeguard cryptographic keys in tamper-proof hardware.

* **HTTPS Proxy authentication support**

  Corda allows a node to use an HTTPS proxy when communicating with the Identity Manager (previously known as Doorman) and Network Map.
  This release improves security by adding username/password authentication configuration support for these proxies.
  Note: this security capability is already present for Corda Firewall SOCKS proxies.

## Further improvements, additions and changes

* Database schema generation fix and documentation clarifications: Corda Enterprise 4.1 should use the *runMigration* flag when running against non-H2
  databases and the *initialiseSchema* flag when running against an H2 database. See :ref:`Database properties <database_properties_ref>`.


{{< note >}}
In Corda Enterprise 4.0 the *initialiseSchema* migration flag was being used for both H2 and non-H2 databases (causing automatic updating
of the nodes database schema by default).
{{</ note >}}

* Improved error messages for non composable serialized types, to include *reason* and *remedy* information.

* Improved performance in attachments classloading, specifically in overlap checking across multiple versions of the same contract JAR.

* Improved firewall logging: log current active connection count.

* Disabled the default loading of `hibernate-validator` as a plugin by hibernate when a CorDapp depends on it. This change will in turn fix [this issue](https://github.com/corda/corda/issues/4444) because nodes will no longer need to add `hibernate-validator` to the `\libs` folder.

* Liquibase now creates custom CorDapp schemas in H2 databases.

* AMQP protocol handshake tuning: aligned timeouts for CRL retrieval and TLS handshaking.

* Improved exception handling and reporting around failed flows.

* Updated proton-j library to latest version.

* Improved logging around serialization evolution.

* Artemis producers and consumers now use separate sessions.

* Artemis now handles message executor thread being interrupted by tests.

* Notary healthcheck includes transaction network parameters hash checking.

* Improved Cloud and Docker documentation.

* Additional documentation on signature constraints.

* Database tables are now fully documented.

* Users of the (Percona cluster) HA Notary Service must now manually install the associated mySQL JDBC Driver for every worker node.

## Known issues


Please refer to same section in [Corda Enterprise 4](https://docs.corda.net/docs/corda-enterprise/4.0/release-notes-enterprise.html)

## Upgrade notes

As per previous major releases, we have provided a comprehensive upgrade notes (:doc:`app-upgrade-notes-enterprise`) to ease the upgrade
of CorDapps to Corda Enterprise 4.1. In line with our commitment to API stability, code level changes are fairly minimal.

For **developers**, switching CorDapps built using Corda (open source) 4.x to Corda Enterprise 4.1 is mostly effortless,
and simply requires making the Corda Enterprise binaries available to Gradle, and changing two variables in the build file:

```shell
    ext.corda_release_version = '4.1'
    ext.corda_release_distribution = 'com.r3.corda'
```

{{< note >}}
In a mixed-distribution network the open source finance contract CorDapp should be deployed on both Corda 4.x (open source) and Corda Enterprise 4.1 nodes.
{{</ note >}}

Visit [https://www.r3.com/corda-enterprise](https://www.r3.com/corda-enterprise/) for more information about Corda Enterprise.
Customers that have purchased support can access it online at  [https://support.r3.com](https://support.r3.com/).
