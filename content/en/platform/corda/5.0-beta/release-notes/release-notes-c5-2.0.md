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

| Topic | Specific Change                                    | 
| -------------------------------------------- | -------------------------------------------------- |
| **Deployment**                               | **Mutual TLS** - It is now possible to configure Corda cluster gateways to connect with each other using [mutual TLS]({{< relref "../operating/mutual-tls-connections.md" >}}). The TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster, including all members in all groups hosted on the cluster. R3 recommend using the default non-mutual TLS mode as it is more extensible. |
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

| Topic  | Specific Change | 
| -------------------------------------------- | -------------------------------------------------- |
| **CorDapp Development**                      | **Flows with Transient Errors** - Flows did not correctly handle transient errors while sessions were in progress. In some cases, the 'error' flag was cleared early by other events, incorrectly indicating that the error had been resolved. This flag can now only be cleared when the event that caused the transient error is retried.  |

## Known Limitations and Issues

There is no support for upgrades from the early access beta versions.

## Test: Table in HTML Format

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:"Poppins", -apple-system, blinkmacsystemfont;font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:"Poppins", -apple-system, blinkmacsystemfont;font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-g9j2{background-color:##efefef;border-color:#c0c0c0;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-f58o{background-color:##efefef;border-color:#c0c0c0;font-weight:bold;text-align:left;vertical-align:bottom}
.tg .tg-wo29{border-color:#c0c0c0;text-align:left;vertical-align:top}
</style>
<table class="tg" style="undefined;table-layout: fixed; width: 920px">
<colgroup>
<col style="width: 201px">
<col style="width: 719px">
</colgroup>
<thead>
  <tr>
    <th class="tg-g9j2">Change Topic</th>
    <th class="tg-f58o">Specific Change</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-wo29" rowspan="4"><span style="font-weight:bolder">Deployment</span></td>
    <td class="tg-wo29"><span style="font-weight:bolder">Mutual TLS</span> <span style="background-color:unset">- It is now possible to configure Corda cluster gateways to connect with each other using</span> <a href="http://localhost:1313/en/platform/corda/5.0-beta/operating/mutual-tls-connections.html"><span style="text-decoration:underline;color:#1D2343">mutual TLS</span></a><span style="background-color:unset">. The TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster, including all members in all groups hosted on the cluster. R3 recommend using the default non-mutual TLS mode as it is more extensible.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Gateway Address</span> <span style="background-color:unset">- It is now possible to use the IP address for gateway endpoints. Using the DNS name is also still supported.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Messaging Maximum Size</span> <span style="background-color:unset">- A new</span> <span style="color:#010101;background-color:#E7E7E7">messaging</span> <a href="http://localhost:1313/en/platform/corda/5.0-beta/operating/configuration/config-overview.html"><span style="text-decoration:underline;color:#1D2343">configuration field</span></a><span style="background-color:unset">,</span> <span style="color:#010101;background-color:#E7E7E7">maxAllowedMessageSize</span><span style="background-color:unset">, enables you to specify the maximum size of a message sent from a Corda worker to the message bus. Corda breaks messages that exceed this size into smaller messages before sending.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29" rowspan="8"><span style="font-weight:bolder">CorDapp Development</span></td>
    <td class="tg-wo29"><span style="font-weight:bolder">Java API</span> <span style="background-color:unset">- The Kotlin API has been replaced with a Java API. As a result, existing CorDapps must be adapted. Kotlin and Java developers can now use this API to build CorDapps.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Unauthenticated Message Logging</span> <span style="background-color:unset">- A message ID field was added to unauthenticated messages. This is logged if there are issues delivering a message to identify the message that was not sent.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Sign Without Arguments</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">UtxoTransactionBuilder.toSignedTransaction(signatory: PublicKey)</span> <span style="background-color:unset">and</span> <span style="color:#010101;background-color:#E7E7E7">ConsensualTransactionBuilder.toSignedTransaction(signatory: PublicKey)</span> <span style="background-color:unset">have been removed. New versions without arguments are now available. These sign with all the available required keys.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Transaction Notary</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">UtxoLedgerTx.notary</span> <span style="background-color:unset">is now available. This is the notary used for notarising this transaction.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">UtxoLedgerService</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">UtxoLedgerService.resolve()</span> <span style="background-color:unset">functions have been added to the API.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Crypto API</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">SignatureSpec</span> <span style="background-color:unset">is now an explicit field in</span> <span style="color:#010101;background-color:#E7E7E7">DigitalSignatureMetadata</span><span style="background-color:unset">. Previously, in order to add the signature spec, it was necessary to include it in</span> <span style="color:#010101;background-color:#E7E7E7">DigitalSignatureMetadata.properties</span> <span style="background-color:unset">map.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Find Signing Keys</span> <span style="background-color:unset">- A new function,</span> <span style="color:#010101;background-color:#E7E7E7">findMySigningKeys</span><span style="background-color:unset">, has been added to the</span> <span style="color:#010101;background-color:#E7E7E7">SigningService</span> <span style="background-color:unset">interface. This function checks a set of specified signing keys to find keys owned by the caller. In the case of</span> <span style="color:#010101;background-color:#E7E7E7">CompositeKey</span><span style="background-color:unset">, it checks the composite key leaves and returns the owned composite key leaf found first.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29" rowspan="4"><span style="font-weight:bolder">Network Operation</span></td>
    <td class="tg-wo29"><span style="font-weight:bolder">Member Registration Approval</span> <span style="background-color:unset">- A network operator can now configure membership groups so that the operator is required to manually approve (or decline) member registration requests. For more information, see</span> <a href="http://localhost:1313/en/platform/corda/5.0-beta/operating/registration-approval.html"><span style="text-decoration:underline;color:#1D2343">Member Registration Approval</span></a><span style="background-color:unset">.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Operational Statuses</span> <span style="background-color:unset">- Four new operational statuses have been added for virtual nodes to provide fine-grained control over their flows and what components they can interact with:</span><br><span style="color:#010101;background-color:#E7E7E7">flowOperationalStatus</span> — describes a virtual node’s ability to start new flows.<br><span style="color:#010101;background-color:#E7E7E7">flowP2pOperationalStatus</span> — describes a virtual node’s ability to communicate with peers.<br><span style="color:#010101;background-color:#E7E7E7">flowStartOperationalStatus</span> — describes a virtual node’s ability to run flows, to have checkpoints, and to continue in-progress flows.<br><span style="color:#010101;background-color:#E7E7E7">vaultDbOperationalStatus</span> — describes a virtual node’s ability to perform persistence operations on the virtual node’s vault.<span style="background-color:unset">These four statuses replace the existing</span> <span style="color:#010101;background-color:#E7E7E7">state</span> <span style="background-color:unset">field. The</span> <span style="color:#010101;background-color:#E7E7E7">GET virtualnode</span> <span style="background-color:unset">now returns the status of each of the four operational characteristics. Maintenance mode has been updated to disable all four of these new operational statuses. You can set this mode using the existing change virtual node state endpoint:</span> <span style="color:#010101;background-color:#E7E7E7">/api/v1/virtualnode/{virtualNodeShortHash}/state/{newState}</span><span style="background-color:unset">.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Upgrading a CPI</span> <span style="background-color:unset">- A new PUT method has been added to the</span> <span style="color:#010101;background-color:#E7E7E7">virtualnode</span> <span style="background-color:unset">resource to upgrade a virtual node’s CPI:</span> <span style="color:#010101;background-color:#E7E7E7">/api/v1/virtualnode/{virtualNodeShortHash}/cpi/{target-CPI-file-checksum}</span><span style="background-color:unset">. Before upgrading, the virtual node must be in maintenance mode with no other operations currently in progress. You can check the list of running flows using</span> <span style="color:#010101;background-color:#E7E7E7">GET /api/v1/flow/{virtualNodeShortHash}</span><span style="background-color:unset">. When the virtual node is in maintenance, and when no flows are running (that is, all flows have either “COMPLETED”, “FAILED” or “KILLED” status), it is safe to trigger a virtual node upgrade. The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI.</span></td>
  </tr>
  <tr>
    <td class="tg-wo29"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
</tbody>
</table>