---
aliases:
- /config-network-parameters.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-config-network-parameters
    parent: cenm-1-3-configuration
    weight: 240
tags:
- config
- network
- parameters
title: Network parameters
---


# Network Parameters

Allowed parameters are:


* **minimumPlatformVersion**:
The minimum platform version that the nodes must be running on. Any node running a platform version below this will
not start.

* **notaries**:

Either the ordered list of file paths to the node info files, or the X.500 names, of the notaries which are permitted in the
network. Note that once a network has started, the only supported changes to notaries are to add new notaries at the end of the list.  

Notaries must be added to the end, as flows often use the ordering of notaries during selection ("pick the first" approach),
and therefore changing the order could cause errors elsewhere. Also note that you can provide only the file path to the node info file or the X.500 name of the notary, not both.

For guidance on using notaries in flows, see {{< cordalatestrelref "enterprise/cordapps/api-flows.md" "the API Flows page" >}}.

## Configuration parameters


* **minimumPlatformVersion**:
The minimum platform version that the nodes must be running. Any node running a platform version below this will
not start.

* **notaries**:
  An ordered list of file paths to the node info files, or X500 names, of the notaries, which are permitted on the
  network.

  * **validating**:
    A boolean value to determine whether the notary is a validating (`true`) or a non-validating (`false`) one.

  * **notaryNodeInfoFile**:
    The file path to the `node.info` file of the notary.

  * **notaryX500Name**:
    The X500 name of the notary, as an alternative to providing the node info. Only supported for HA notaries.

* **maxMessageSize**:
Maximum allowed size in bytes of an individual message sent over the wire. Note that attachments are
a special case and may be fragmented for streaming transfer, however, an individual transaction or flow message
may not be larger than this value.


* **maxTransactionSize**:
Maximum allowed size in bytes of a transaction. This is the size of the transaction object and its attachments.


* **eventHorizonDays**:
Number of days after which nodes will be removed from the network map if they have not been seen during this period.


* **parametersUpdate**:
Specific `parametersUpdate` configuration (optional).


  * **description**:
  A brief description of this instance of `parametersUpdate`.


  * **updateDeadline**:
  ISO-8601 time format indicating the deadline for this update. Example value: “2017-08-31T05:10:36.297Z”




* **whitelistContracts**:
Specific configuration for contracts whitelist (optional).


  * **cordappsJars**:
  The list of file paths referencing CorDapp JAR files that will be automatically scanned for contract classes to be included in the whitelist.


  * **exclude**:
  The list of contract class names (for instance, full package names) to be excluded from the whitelist.


  * **contracts**:
  The list of explicitly specified whitelisted contracts. Each element of the list has the following attributes:


    * **className**:
    The full package class name of the contract to be whitelisted.

    * **attachmentIds**:
    List of JAR file hashes (given as strings) containing the contract class.


* **packageOwnership**:
List of the network-wide Java packages that have been claimed by their owners along with the owners
public keys. Optionally, the list should consist of entries with the following parameters:

  * **packageName**:
  The full package name in string format.


  * **publicKeyPath**:
  The file path to the public key. Note that this public key needs to be in a `.pem` [file format](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail).


  * **algorithm**:
  The algorithm used to generate the public key (for example, RSA or EC). This parameter is optional and defaults to RSA.
  *Note: Corda (and by association CENM) do not support DSA keys.*


* **epoch**:
The specified epoch for the set of network parameters (optional). If set, this should be greater than the
previous epoch (if one exists) and always strictly positive (> 0). If not set, the previous epoch value will be
automatically incremented. This parameter is mainly used for ensuring uniqueness across multiple segregated
subzones. If only one network map is being run then it is best practice to omit this option.
