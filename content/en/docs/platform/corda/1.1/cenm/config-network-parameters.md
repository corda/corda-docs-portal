---
aliases:
- /releases/release-1.1/config-network-parameters.html
- /config-network-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-1:
    identifier: cenm-1-1-config-network-parameters
    parent: cenm-1-1-configuration
    weight: 240
tags:
- config
- network
- parameters
title: Network Parameters
---


# Network Parameters

Allowed parameters are:


* **minimumPlatformVersion**: 
The minimum platform version that the nodes must be running. Any node which is below this will
not start.


* **notaries**: 
List of file paths to the node info files of the notaries which are permitted in the network. Notice that
notaries will be always added to the existing list (we don’t support notaries removal).


* **maxMessageSize**: 
Maximum allowed size in bytes of an individual message sent over the wire. Note that attachments are
a special case and may be fragmented for streaming transfer, however, an individual transaction or flow message
may not be larger than this value.


* **maxTransactionSize**: 
Maximum allowed size in bytes of a transaction. This is the size of the transaction object and its attachments.


* **eventHorizonDays**: 
Number of days after which nodes will be removed from the network map if they have not been seen during this period.


* **parametersUpdate**: 
Parameters update specific configuration (Optional).


* **description**: 
Brief description for this parameters update instance.


* **updateDeadline**: 
ISO-8601 time format indicating the deadline for this update. Example value: “2017-08-31T05:10:36.297Z”




* **whitelistContracts**: 
Contract whitelist specific configuration (Optional).


* **cordappsJars**: 
List of file paths referencing CorDapp JAR files that will be automatically scanned for contract classes to be included in the whitelist.


* **exclude**: 
List of contract class names (i.e. full package names) to be excluded from the whitelist.


* **contracts**: 
List of explicitly specified whitelisted contracts. Each element of the list has the following attributes:


* **className**: 
Full package class name of the contract to be whitelisted.


* **attachmentIds**: 
List of JAR file hashes (given as strings) containing the contract class.






* **packageOwnership**: 
List of the network-wide Java packages that have been claimed by their owners along with the owners
public keys. More information about this can be found here: [Package Ownership](https://docs.corda.net/design/data-model-upgrades/package-namespace-ownership.html)
(Optional) The list should consist of entries with the following parameters:


* **packageName**: 
The full package name in string format.


* **publicKeyPath**: 
The file path to the public key. Note: This public key needs to be in a pem file format.


* **algorithm**: 
The algorithm used to generate the public key (e.g. RSA or EC). (Optional - defaults to RSA).
*Note: Corda (and by association CENM) do not support DSA keys.*




* **epoch**: 
(Optional) The specified epoch for the set of network parameters. If set this should be greater than the
previous epoch (if exists) and always strictly positive (> 0). If not set then the previous epoch value will be
automatically incremented. This parameter is mainly used for ensuring uniqueness across multiple segregated
sub-zones. If only one network map is being run then it is best practice to omit this option.



