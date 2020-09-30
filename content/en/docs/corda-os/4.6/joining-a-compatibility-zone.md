---
aliases:
- /head/joining-a-compatibility-zone.html
- /HEAD/joining-a-compatibility-zone.html
- /joining-a-compatibility-zone.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-joining-a-compatibility-zone
    parent: corda-os-4-6-corda-networks-index
    weight: 1050
tags:
- joining
- compatibility
- zone
title: Joining an existing compatibility zone
---




# Joining an existing compatibility zone

To connect to a compatibility zone you need to register with its certificate signing authority (or *doorman*) by
submitting a certificate signing request (CSR) to obtain a valid identity for the zone. This process is only necessary
when the node connects to the network for the first time, or when the certificate expires. You could do this out of
band, for instance via email or a web form, but there’s also a simple request/response utility built into the node.

Before using this utility, you must first have received the trust store file containing the root certificate from the
zone operator. For high security zones, this might be delivered physically.

Then run the following command:

`java -jar corda.jar --initial-registration --network-root-truststore-password <trust store password>`

{{< warning >}}

**Important note about running the initial node registration command**

In Corda 4.6, database schemas are no longer initialised/migrated automatically by running any command at the first run of the node - typically at the initial node registration. This is now done explicitly by running `run-migration-scripts`, so no other commands during the first node run would initialise/migrate the database schema. 

The exception to that is the `--initial-registration` command, which embeds `run-migration-scripts` and therefore runs the database migration scripts by default. 

So if you are using deployment automation you may need to adjust your scripts accordingly and exclude the database initialisation/migration task from the initial node registration command. To do so, use the `--skip-schema-creation` flag alongside the `--initial-registration` command.


{{< /warning >}}

By default, the utility expects the trust store file to be in the location `certificates/network-root-truststore.jks`.
This can be overridden using the additional `--network-root-truststore` flag.

The utility performs the following steps:


* It creates a certificate signing request based on the following information from the node’s configuration file (see
[Node configuration](corda-configuration-file.md)):
* **myLegalName** Your company’s legal name as an X.500 string. X.500 allows differentiation between entities with the same
name, as the legal name needs to be unique on the network. If another node has already been permissioned with this
name then the permissioning server will automatically reject the request. The request will also be rejected if it
violates legal name rules, see node_naming for more information. You can use the X.500 schema to disambiguate
entities that have the same or similar brand names
* **emailAddress** e.g. “[admin@company.com](mailto:admin@company.com)”
* **devMode** must be set to false
* **compatibilityZoneURL** or **networkServices** The address(es) used to register with the compatibility zone and
retrieve the network map. These should be provided to you by the operator of the zone. This must be either:
    * **compatibilityZoneURL** The root address of the network management service. Use this if both the doorman and the
network map service are operating on the same URL endpoint
    * **networkServices** The root addresses of the doorman and the network map service. Use this if the doorman and the
network map service are operating on the same URL endpoint, where:
        * **doormanURL** is the root address of the doorman. This is the address used for initial registration
        * **networkMapURL** is the root address of the network map service






* It generates a new private/public keypair to sign the certificate signing request
* It submits the request to the doorman server and polls periodically to retrieve the corresponding certificates
* It creates the node’s keystore and trust store using the received certificates
* It creates and stores the node’s TLS keys and legal identity key along with their corresponding certificate-chains

{{< note >}}
You can exit the utility at any time if the approval process is taking longer than expected. The request
process will resume on restart as long as the `--initial-registration` flag is specified.

{{< /note >}}
