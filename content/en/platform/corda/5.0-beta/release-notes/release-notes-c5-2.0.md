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


<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Domain | Specific Change                                    | 
| -------------------------------------------- | -------------------------------------------------- |
| **Cluster Administration**                   | **Mutual TLS** - It is now possible to configure Corda clusters to use [mutual TLS]({{< relref "../operating/mutual-tls-connections.md" >}}). The TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster, including all members in all groups hosted on the cluster. R3 recommend using the default non-mutual TLS mode as it is more extensible. |
|                                              | **Gateway Address** - It is now possible to use the IP address for gateway endpoints. Using the DNS name is also still supported.|
|                                              | **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. | 
|                                              | **Messaging Maximum Size** - A new `messaging` [configuration field]({{< relref "../operating/configuration/config-overview.md" >}}), `maxAllowedMessageSize`, enables you to specify the maximum size of a message sent from a Corda worker to the message bus. Corda breaks messages that exceed this size into smaller messages before sending. |                                           
| **CorDapp Development**                      | **Java API** - The Kotlin API has been replaced with a Java API. As a result, existing CorDapps must be adapted. Kotlin and Java developers can now use this API to build CorDapps. |
|                                              | **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. |
|                                              | **Unauthenticated Message Logging** - A message ID field was added to unauthenticated messages. This is logged if there are issues delivering a message to identify the message that was not sent. |
|                                              | **Transaction Builder Signing** - `UtxoTransactionBuilder.toSignedTransaction(signatory: PublicKey)` and `ConsensualTransactionBuilder.toSignedTransaction(signatory: PublicKey)` have been removed. New versions of these methods without arguments are now available. These new versions sign using all of the available required keys when generating a transaction, removing the need to specify particular keys. |
|                                              | **Transaction Notary Property** - The `UtxoLedgerTransaction.notary` property has been exposed. This is the notary used for notarising this transaction. |
|                                              | **UtxoLedgerService** - The following functions have been added to resolve the specified `StateRef` instances into `StateAndRef` instances of the specified `ContractState` type:<ul><li>`UtxoLedgerService.resolve(StateRef)`</li><li>`UtxoLedgerService.resolve(Iterable<StateRef>)`</li><ul>| 
|                                              | **Crypto API** - `SignatureSpec` is now an explicit field in `DigitalSignatureMetadata`. Previously, in order to add the signature spec, it was necessary to include it in `DigitalSignatureMetadata.properties` map. |
|                                              | **Find Signing Keys** - A new function, `findMySigningKeys`, has been added to the `SigningService` interface. This function checks a set of specified signing keys to find keys owned by the caller. In the case of `CompositeKey`, it checks the composite key leaves and returns the owned composite key leaf found first.  |
| **Network Operation**                        | **Member Registration Approval** - A network operator can now configure membership groups so that the operator is required to manually approve (or decline) member registration requests. For more information, see [Member Registration Approval]({{< relref "../operating/registration-approval.md" >}}). |     
|                                              | **Operational Statuses** - Four new operational statuses have been added for virtual nodes to provide fine-grained control over their flows and what components they can interact with: <ul><li>`flowOperationalStatus` — describes a virtual node's ability to start new flows. </li> <li>`flowP2pOperationalStatus` — describes a virtual node's ability to communicate with peers.</li> <li>`flowStartOperationalStatus` — describes a virtual node's ability to run flows, to have checkpoints, and to continue in-progress flows. </li> <li> `vaultDbOperationalStatus` —  describes a virtual node's ability to perform persistence operations on the virtual node's vault. </li> </ul>These four statuses replace the existing `state` field. The `GET virtualnode` now returns the status of each of the four operational characteristics. Maintenance mode has been updated to disable all four of these new operational statuses. You can set this mode using the existing change virtual node state endpoint: `/api/v1/virtualnode/{virtualNodeShortHash}/state/{newState}`. 
|                                              | **Upgrading a CPI** - A new PUT method has been added to the `virtualnode` resource to upgrade a virtual node's CPI: `/api/v1/virtualnode/{virtualNodeShortHash}/cpi/{target-CPI-file-checksum}`. Before upgrading, the virtual node must be in maintenance mode with no other operations currently in progress. You can check the list of running flows using `GET /api/v1/flow/{virtualNodeShortHash}`. When the virtual node is in maintenance, and when no flows are running (that is, all flows have either "COMPLETED", "FAILED" or "KILLED" status), it is safe to trigger a virtual node upgrade. The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI. 
|                                              | **Corda CLI** - Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated. |

## Resolved Issues

| Domain  | Specific Change | 
| -------------------------------------------- | -------------------------------------------------- |
| **CorDapp Development**                      | **Flows with Transient Errors** - Flows did not correctly handle transient errors while sessions were in progress. In some cases, the 'error' flag was cleared early by other events, incorrectly indicating that the error had been resolved. This flag can now only be cleared when the event that caused the transient error is retried.  |

## Known Limitations and Issues

During the Beta process, R3 do not guarantee the stability of our user APIs. As a result, seemless upgrade between Beta versions is not supported.
