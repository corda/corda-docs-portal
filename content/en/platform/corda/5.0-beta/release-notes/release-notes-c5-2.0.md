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

## New Features and Enhancements


| <div style="width:160px">Change Topic </div> | Specific Change | 
| --------------------------- | -------------------------------------------------- |
| **Deployment**    | **Mutual TLS** - It is now possible to configure Corda cluster gateways to connect with each other via [mutual TLS]({{< relref "../operating/mutual-tls-connections.md" >}}).<!--need more info about knock-on affect-->|
|  | **Gateway Address** - It is now possible to connect between peer gateways by IP address, as well as DNS name.  <!--reword "configure gateways to use IP address"-->|
| |**Messaging Maximum Size** - A new `messaging` [configuration field]({{< relref "../operating/configuration/config-overview.md" >}}), `maxAllowedMessageSize`, enables you to specify the maximum size of a message sent from a Corda worker to the message bus. Corda breaks messages that exceed this size into smaller messages before sending. <!-- should be added to schmea description: The `maxAllowedMessageSize` value must be lower than the maximum message size configured on the message bus itself; for example, Kafka. If the Corda configuration value is set to a value higher than that of the message bus, messages will not be sent.-->|     
|| **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. |                                       
| **CorDapp Development**      |    **Java API** - The Kotlin API has been replaced with a Java API. Kotlin and Java developers can now use this to build CorDapps. As a result, existing CorDapps must be written.|
|| **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. |
||  **Unauthenticated Message Logging** - A message ID field was added to unauthenticated messages. This will be logged when there are issues with delivering a message to identify the message that was not sent. |
||   **Sign Without Arguments** - `UtxoTransactionBuilder.toSignedTransaction(signatory: PublicKey)` and `ConsensualTransactionBuilder.toSignedTransaction(signatory: PublicKey)` have been removed. New versions without arguments are now available. These sign with all the available required keys. <!--needs more info--> |
|| **Transaction Notary** - `UtxoLedgerTx.notary` is now available. This is the notary used for notarising this transaction. <!--needs more info-->|
|| **UtxoLedgerService** - `UtxoLedgerService.resolve()` functions have been added to the API. <!--needs more info-->| 
|| **Crypto API** - `SignatureSpec` is now an explicit field in `DigitalSignatureMetadata`. Previously, in order to add the signature spec, it was necessary to include it in `DigitalSignatureMetadata.properties` map. |
|| **Find Signing Keys** - A new function, `findMySigningKeys`, has been added to the `SigningService` interface. This function checks a set of specified signing keys to find keys owned by the caller. In the case of `CompositeKey`, it checks the composite key leaves and returns the owned composite key leaf found first. </li>  |
| **Network Operation** | **Member Registration Approval** - A network operator can now configure a membership group so that the operator is required to manually approve (or decline) member registration requests. For more information, see [Member Registration Approval]({{< relref "../operating/registration-approval.md" >}}). |     
||**Operational Statuses** - Four fine-grained operational statuses have been added for virtual nodes: <li>`flowOperationalStatus`</li><li>`flowP2pOperationalStatus`</li><li>`flowStartOperationalStatus` </li><li> `vaultDbOperationalStatus` </li> <!--why?-->These four statuses replace the existing `state` field. The `GET virtualnode` now returns the status of each of the four operational characteristics. Maintenance mode has been updated to disable all four of these new operational statuses. You can set this mode using the existing change virtual node state endpoint: `/api/v1/virtualnode/{virtualNodeShortHash}/state/{newState}`. <!--Should be documented elsewhere - maintenance mode isn't new?: Possible states are: `maintenance` or `active`. A virtual node in maintenance mode does not allow starting or running flows. Any activity for existing flows cause the flow to be killed and marked with a flow status of "KILLED". Counterparty flows fail with an error message indicating that a peer is in maintenance. This state allows virtual node operators to have a static vault with which they can take backups before performing potentially destructive operations such as virtual node upgrade with migrations. Changing a virtual node's state back to active requires that the virtual node has executed all migrations in the currently associated CPI. This prevents a virtual node from becoming operational while migrations are in progress during a virtual node upgrade. -->
||**Upgrading a CPI** - A new PUT method has been added to the `virtualnode` resource to upgrade a virtual node's CPI: `/api/v1/virtualnode/{virtualNodeShortHash}/cpi/{target-CPI-file-checksum}`. Before upgrading, the virtual node must be in maintenance mode with no other operations currently in progress. You can check the list of running flows using `GET /api/v1/flow/{virtualNodeShortHash}`. When the virtual node is in maintenance, and when no flows are running (that is, all flows have either "COMPLETED", "FAILED" or "KILLED" status), it is safe to trigger a virtual node upgrade. The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI. 
|| **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. |


## Resolved Issues

|  <div style="width:160px">Change Topic </div> | Specific Changes | 
| --------------------------------------------- | -------------------------------------------------- |
| **CorDapp Development**                       | **Flows with Transient Errors** - Flows did not correctly handle transient errors while sessions were in progress. In some cases, the 'error' flag was cleared early by other events, incorrectly indicating that the error had been resolved. This flag can now only be cleared when the event that caused the transient error is retried.  |

## Known Limitations and Issues

There is no support for upgrades from the early access beta versions.
