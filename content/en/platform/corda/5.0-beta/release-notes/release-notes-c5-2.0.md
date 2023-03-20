---
date: '2023-02-21'
title: "Corda 5.0 Beta 2.0 Release Notes"
menu:
  corda-5-beta:
    parent: corda-5-beta-release-notes
    identifier: corda-5-beta-release-notes-2.0
    weight: 1000
section_menu: corda-5-beta
---

Corda 5.0 Beta is a pre-release version for testing purposes only.
{{< note >}}
If you are not part of the current beta program, the Corda 5.0 Beta documentation is for information only.
Please contact R3 if you are interested in joining the Beta program.
{{< /note >}}

## Enhancements

This section describes the new features in Corda 5.0 Beta 2.0.

### Cluster Configuration

#### Mutual TLS
It is now possible to configure Corda cluster gateways to connect with each other via [mutual TLS]({{< relref "../operating/mutual-tls-connections.md" >}}).

#### Messaging Maximum Size
A new `messaging` [configuration field]({{< relref "../operating/configuration/config-overview.md" >}}), `maxAllowedMessageSize`, enables you to specify the maximum size of a message sent from a Corda worker to the message bus. Corda breaks messages that exceed this size into smaller messages before sending.
The `maxAllowedMessageSize` value must be lower than the maximum message size configured on the message bus itself, for example, Kafka. If the Corda configuration value is set to a value higher than that of the message bus, the messages will not send.

#### Registration Approval
A network operator can now configure a membership group to require that the operator must manually approve (or decline) member registration requests. Requests satisfying specific criteria require manual approval, while others are approved automatically. The operator can also pre-authenticate specific members, allowing them to bypass the standard approval rules defined for the group. The operator can further configure pre-authentication to specify that certain changes to the member’s context must be manually reviewed. For more information, see [Manual Registration Approval]({{< relref "../operating/manual-registration-approval.md" >}}).

### CorDapp Development

#### Java API
The Kotlin API has been replaced with a Java API. Kotlin and Java developers can now use this to build CorDapps.

#### Sign Without Arguments
`UtxoTransactionBuilder.toSignedTransaction(signatory: PublicKey)` and `ConsensualTransactionBuilder.toSignedTransaction(signatory: PublicKey)` have been removed. New versions without arguments are now available. These sign with all the available required keys.

#### Transaction Notary
`UtxoLedgerTx.notary` is now available. This is the notary used for notarising this transaction.

#### UtxoLedgerService
`UtxoLedgerService.resolve()` functions have been added to the API.

#### Crypto API
`SignatureSpec` is now an explicit field in `DigitalSignatureMetadata`. In previous versions, it was necessary to add it in the `DigitalSignatureMetadata.properties` map.

#### P2P Avro Types
Avro types for the peer-to-peer communications layer were moved from the `net.corda.p2p` namespace to the `net.corda.data.p2p namespace`.

#### Find Signing Keys
A new function, `findMySigningKeys`, has been added to the `SigningService` interface. This function checks if the specified set of keys are owned by the caller. It returns a mapping from the requested key to the same key if it is owned by the caller or to null if the key is not owned by the caller.
In the case of a composite key, it maps the composite key to the firstly found composite key leaf.

### P2P

#### Gateway Address
It is now possible to connect between peer gateways by IP address, as well as DNS name.

### Virtual Nodes

#### Maintenance
A new PUT method has been added to the `virtualnode` resource to update the state of a virtual node: `/api/v1/virtualnode/{virtualNodeShortHash}/state/maintenance`.
Setting the state to `IN_MAINTENANCE` prevents the virtual node from starting new flows and running existing flows.
{{< note >}}
This is a total “stop-the-world” virtual node operation. A virtual node in the maintenance state can not start or run flows. Any activity arriving for in-progress flows result in the flows being killed.
{{< /note >}}
You can check the list of running flows using the get multiple flow status endpoint, `GET /api/v1/flow/{virtualNodeShortHash}`. After all flows have terminated, you can safely perform a virtual node upgrade using the [new upgrade endpoint]({{< relref "#upgrading-a-cpi" >}}).

### Upgrading a CPI
A new PUT method has been added to the `virtualnode` resource to upgrade a virtual node's CPI: `/api/v1/virtualnode/{virtualNodeShortHash}/cpi/{target-CPI-file-checksum}`.
Before upgrading, the virtual node must be in maintenance mode with no other operations currently in progress. The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI.

### Corda CLI
#### Kebab Case
Any worker and CLI long options that used camel case now use kebab case.

### Logging
#### Message ID
A message ID field was added to unauthenticated messages. This will be logged when there are issues with delivering a message to identify the message that was not sent.

## Resolved Issues

This section describes the issues resolved in Corda 5.0 Beta 2.0.

### Flows

#### Flows with Transient Errors
Flows did not correctly handle transient errors while sessions were in progress.

## Known Limitations and Issues

* Corda 4 CorDapps will not run on Corda 5; it is a different set of incompatible APIs.
* Upgrade from Corda 4 to Corda 5 is not supported; a future version will provide migration guidance and tooling.
* There is no support for the Corda 4 Accounts SDK.
* There is no support for the Corda 4 Tokens SDK.
* There is no support for upgrades from the early access beta versions.