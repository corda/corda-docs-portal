---
aliases:
- /releases/release-1.0/release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-release-notes
    parent: cenm-1-0-enm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---


# Release notes

## Unreleased

Unbundled the JDBC Driver, this will require those of you running SQL Server to download the JDBC driver jar
and configure your CENM services to use it.

Separated the Network Map Protocol REST endpoint from the debugging endpoints that provide human readable
information formatted as JSON. This was done to better draw distinction between the protocol itself as
required by Corda nodes, and the more free-form functionality offered to users. This will allow for future
versioned changes to the protocol without changing that which the Corda nodes depend upon.

The two top-level endpoints are now

* `/network-map`
* `/network-map-user`

see [Network Map Overview](network-map-overview.md) for more information.

* Signing Service -> Doorman socket based communication added.

Added support for overriding the default “increment previous value by 1” behaviour for epoch values during network
parameter updates/initialisation. This allows a user to specify the epoch within the parameter config file and it
facilitates arbitrary jumps in epoch values. This is necessary for the day-to-day management of multiple sub-zones as
well as the merging of one sub-zone into another.

Migrated the private network management utility tool into the Network Map interactive shell. The new command within the
shell is an interactive command, allowing a user to run the same management tools without having to worry about passing
in a configuration file or remembering the correct start up flag.

Added multi-phase parsing of config files. Parsing and validation errors are now batched before being presented to
the user, eliminating the frustration from having to address errors one by one.

## Release 0.3

The newest release introduces some large changes to the way the Network Management services operate, and lays the ground
work for some exciting changes and streamlining in the future.

### Support For Segregated Sub Zones

Due to the database schema separation outlined below, the 0.3 release now supports segregated sub zones. That is,
sub-zones of nodes that operate in what appear to the nodes to be isolated networks, with their own notary(ies) and
network parameters. Critically, however, their certificate governance remains under the jurisdiction of a global
Doorman. This way, temporary benefits such as higher privacy, differential network parameters upgrade schedules or use
of temporary private notaries can be delivered whilst retaining the option (in some cases) for the nodes in the sub zone
to merge into the ‘main’ zone and gain the benefit of being able to transact with a far broader pool of peers. Note that
this merging functionality is not currently supported but is planned for a future release. See the [Sub Zones](sub-zones.html)
documentation for more information.

### Schema Separation

As mentioned above, one of the biggest the changes in the release is the database schema separation of the Doorman and
Network Map service. Previously, although the services could be run as separate processes on different machines, they
both needed to speak to the same database and schema. This tight coupling has now been broken.

To facilitate this schema separation and remove the need for multiple direct database connections, inter-service
communication was introduced. Most notably, a Network Map service can be configured to communicate with both the Doorman
and Revocation service and the Signing Service can request and sign Certificate Revocation Lists, Network Parameters and
Network Maps without having to speak to the database directly. For secure communication between the services, SSL
support was also introduced.

See the [Upgrading Corda Enterprise Network Manager](upgrade-notes.md) documentation for a more detailed list of the changes as a result of the schema separation,
as well as the knock on effects for a zone operator.

### Embedded Shell

Another change that is introduced in the newest release is the ability to interact with the Doorman and Network Map
services via a shell. The commands available currently mainly allow an operator to inspect the state of the service,
for example by viewing the current set of nodes within the public network, or viewing the list of Certificate Signing
Requests that are awaiting approval. This will be built upon in the next release, allow for more advanced interactions
with the services. See the [Embedded Shell](shell.md) documentation for more information.

### Upgrading & Data Migration

Because this release contains changes that will likely require modifications in existing infrastructure (adding a new
database schema or instance), a data migration tool has been provided to facilitate the upgrade path from a 0.2
environment. See the [Upgrading Corda Enterprise Network Manager](upgrade-notes.md) documentation for more information.

### Private Network Functionality

The way that private networks are created and managed has also been improved. The private network management tool has
been built upon and is now the defacto management method for a zone operator. It has been built upon and enables private
network support on a per Network Map service basis, as well as introduces new “Move back into public” functionality.
*Note that managing private networks directly via the database is now strongly discouraged*. See the
[Private Network Map](private-network-map.md) documentation for more information.

### Service Monitoring

The service-based architecture requires tooling around service state monitoring. Currently (i.e. with the 0.3 release),
there is no dedicated utility that would address that issue. As for now, the network operator needs to rely only on service logs and manual service endpoint pinging in order to
assess in what state the service is. Better tooling around service health-check is planned to be added in the next release of the ENM.

* Doorman: `http://<<DOORMAN_ADDRESS>>/status`
* Network Map: `http://<<NETWORK_MAP_SERVICE_ADDRESS>>/network-map/my-hostname`
* Revocation Service (currently part of Doorman): `http://<<REVOCATION_SERVICE_ADDRESS>>/status`

### Documentation

The entire documentation for the Network Services has been redone and published in the [Networking and messaging](../../../../../en/platform/corda/4.5/open-source/messaging.md) section.

### Issues Fixed

* Added missing *my-hostname* endpoint missing in the Network Map Server.
* Revert network parameters constraints on the *maxTransactionSize*.
* JIRA client inaccessible from the maven repo.
* Running master (just post 0.2.1) Norman with Revocation Service also embedded gets serialization exceptions.
* If DB gets overloaded If local signing slows then timed execution does not back off.
* Fix hanging tests in Network Services code base.
* Fix docs isCa -> issuesCertificates.
* run-all.sh script for example cert generation doesn’t work when multiple utils jars exist in the build directory.
* Cert generator isn’t backward compatible with 0.2 config.
* Doorman doesn’t exit when it can’t locate cert stores, needs to be CTRL-C’d.
* Doorman doesn’t exit on exception when creating local signer whilst initialising.
* Improve error logging within the private network utility tool.
* Minor doc fix.
* Minor doc fix.

## Release 0.2.2

### Issues Fixed

* Add the migration script for the allowAutoEnrollment column addition to the private networks table.

## Release 0.2.1

### Backward Compatibility

The major addition in the 0.2.1 release is backward compatibility, which was absent in the 0.2.0 release due to time
constraints. This release of the Network Services fully supports old V0.1 PKI key stores and configuration files. See
[Upgrading Corda Enterprise Network Manager](upgrade-notes.md) for more information.

### Config Upgrade Tool

Together with automated support for the 0.1 config files, the 0.2.1 release brings the Config Upgrade Tool. This
translates any 0.1 or 0.2.0 config file to 0.2.1 format.

### Certificate Hierarchy Verifier

Moreover, utilities have been added that facilitate management of the new PKI. In particular the Certificate Hierarchy
Verifier, which ensures correctness of the generated certificate hierarchy with respect to the Corda Network deployment.
See [Certificates Validator](tool-certificates-validator.md) for more details regarding this tool and [Tools and Utilities](tools-index.md) for a comprehensive
list of all available tools.

### Documentation

The entire documentation for the Network Services has been redone and published in the [Networking and messaging](../../../../../en/platform/corda/4.5/open-source/messaging.md) section.

### Issues Fixed

* Fix error logging when exception during Jira workflow plugin creation.
* Fix keyPassword field for the revocation section in the configuration upgdrader.
* Add cert chain validation for local signer certificate chain construction.
* Print error message for signing service exception.
* Wrong log line in the CertificateSigningRequestSigner.
* Throw an explicit error when exception during local signer creation.
* Fix error logging within config parsing.
* Remove stack trace from the error logging.

## Release 0.2.0

The major change in 0.2.0 is modification of the PKI used throughout the network. In previous (prototype) versions the
PKI hierarchy had been fixed, meaning that the option to have an intermediate CA that sat between the Doorman and the
Root was not available.

This is now possible! There is support for arbitrary length certificate chains.

The new PKI is *not* backwards compatible with the old PKI. Hence anyone running a Doorman/Network Map with the new PKI
needs to ensure that nodes running an outdated (old PKI) version of Corda are gracefully rejected. The new PKI is
supported in versions *Corda OS 3.3+* and *Corda ENT 3.2+*. This can be achieved by adding the following to the doorman
or network map configuration:

```guess
doorman {
    ...
    versionInfoValidation {
        minimumPlatformVersion = 3
        newPKIOnly = true
    }
    ...
}
```

```guess
networkMap {
    ...
    versionInfoValidation {
        minimumPlatformVersion = 3
        newPKIOnly = true
    }
    ...
}
```
