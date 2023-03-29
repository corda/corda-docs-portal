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

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{border-color:black;border-style:solid;border-width:1px;font-family:"Poppins", -apple-system, blinkmacsystemfont; font-size:14px;
  overflow:hidden;padding:10px 5px;word-break:normal;}
.tg th{border-color:black;border-style:solid;border-width:1px;font-family:"Poppins", -apple-system, blinkmacsystemfont; font-size:14px;
  font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
.tg .tg-o7ty{background-color:#FFF;border-color:#c0c0c0;color:#1D2343;font-weight:bold;text-align:left;vertical-align:top}
.tg .tg-7ewn{background-color:#efefef;border-color:#c0c0c0;color:#1D2343;font-weight:bold;text-align:left;width: 30%;vertical-align:bottom}
</style>
<table>
<thead>
  <tr>
    <th class="tg-7ewn">Domain</th>
    <th class="tg-7ewn">Specific Change</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-o7ty" rowspan="4"><span style="font-weight:bolder">Cluster Administration</span></td>
    <td class="tg-o7ty"><span style="font-weight:bolder">Mutual TLS</span> <span style="background-color:unset">- It is now possible to configure Corda clusters to use</span> <a href="https://docs.r3.com/en/platform/corda/5.0-beta/operating/mutual-tls-connections.html"><span style="text-decoration:underline;color:#1D2343">mutual TLS</span></a><span style="background-color:unset">. The TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster, including all members in all groups hosted on the cluster. R3 recommend using the default non-mutual TLS mode as it is more extensible.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Gateway Address</span> <span style="background-color:unset">- It is now possible to use the IP address for gateway endpoints. Using the DNS name is also still supported.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Messaging Maximum Size</span> <span style="background-color:unset">- A new</span> <span style="color:#010101;background-color:#E7E7E7">messaging</span> <a href="https://docs.r3.com/en/platform/corda/5.0-beta/operating/configuration/config-overview.html"><span style="text-decoration:underline;color:#1D2343">configuration field</span></a><span style="background-color:unset">,</span> <span style="color:#010101;background-color:#E7E7E7">maxAllowedMessageSize</span><span style="background-color:unset">, enables you to specify the maximum size of a message sent from a Corda worker to the message bus. Corda breaks messages that exceed this size into smaller messages before sending.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty" rowspan="8"><span style="font-weight:bolder">CorDapp Development</span></td>
    <td class="tg-o7ty"><span style="font-weight:bolder">Java API</span> <span style="background-color:unset">- The Kotlin API has been replaced with a Java API. As a result, existing CorDapps must be adapted. Kotlin and Java developers can now use this API to build CorDapps.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Unauthenticated Message Logging</span> <span style="background-color:unset">- A message ID field was added to unauthenticated messages. This is logged if there are issues delivering a message to identify the message that was not sent.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Transaction Builder Signing</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">UtxoTransactionBuilder.toSignedTransaction(signatory: PublicKey)</span> <span style="background-color:unset">and</span> <span style="color:#010101;background-color:#E7E7E7">ConsensualTransactionBuilder.toSignedTransaction(signatory: PublicKey)</span> <span style="background-color:unset">have been removed. New versions of these methods without arguments are now available. These new versions sign using all of the available required keys when generating a transaction, removing the need to specify particular keys.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Transaction Notary Property</span> <span style="background-color:unset">- The</span> <span style="color:#010101;background-color:#E7E7E7">UtxoLedgerTransaction.notary</span> <span style="background-color:unset">property has been exposed. This is the notary used for notarising this transaction.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">UtxoLedgerService</span> <span style="background-color:unset">- The following functions have been added to resolve the specified</span> <span style="color:#010101;background-color:#E7E7E7">StateRef</span> <span style="background-color:unset">instances into</span> <span style="color:#010101;background-color:#E7E7E7">StateAndRef</span> <span style="background-color:unset">instances of the specified</span> <span style="color:#010101;background-color:#E7E7E7">ContractState</span> <span style="background-color:unset">type:</span><br><span style="color:#010101;background-color:#E7E7E7">UtxoLedgerService.resolve(StateRef)</span><br><span style="color:#010101;background-color:#E7E7E7">UtxoLedgerService.resolve(Iterable&lt;StateRef&gt;)</span><br></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Crypto API</span> <span style="background-color:unset">-</span> <span style="color:#010101;background-color:#E7E7E7">SignatureSpec</span> <span style="background-color:unset">is now an explicit field in</span> <span style="color:#010101;background-color:#E7E7E7">DigitalSignatureMetadata</span><span style="background-color:unset">. Previously, in order to add the signature spec, it was necessary to include it in</span> <span style="color:#010101;background-color:#E7E7E7">DigitalSignatureMetadata.properties</span> <span style="background-color:unset">map.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Find Signing Keys</span> <span style="background-color:unset">- A new function,</span> <span style="color:#010101;background-color:#E7E7E7">findMySigningKeys</span><span style="background-color:unset">, has been added to the</span> <span style="color:#010101;background-color:#E7E7E7">SigningService</span> <span style="background-color:unset">interface. This function checks a set of specified signing keys to find keys owned by the caller. In the case of</span> <span style="color:#010101;background-color:#E7E7E7">CompositeKey</span><span style="background-color:unset">, it checks the composite key leaves and returns the owned composite key leaf found first.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty" rowspan="4"><span style="font-weight:bolder">Network Operation</span></td>
    <td class="tg-o7ty"><span style="font-weight:bolder">Member Registration Approval</span> <span style="background-color:unset">- A network operator can now configure membership groups so that the operator is required to manually approve (or decline) member registration requests. For more information, see</span> <a href="https://docs.r3.com/en/platform/corda/5.0-beta/operating/registration-approval.html"><span style="text-decoration:underline;color:#1D2343">Member Registration Approval</span></a><span style="background-color:unset">.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Operational Statuses</span> <span style="background-color:unset">- Four new operational statuses have been added for virtual nodes to provide fine-grained control over their flows and what components they can interact with:</span><br><span style="color:#010101;background-color:#E7E7E7">flowOperationalStatus</span> — describes a virtual node’s ability to start new flows.<br><span style="color:#010101;background-color:#E7E7E7">flowP2pOperationalStatus</span> — describes a virtual node’s ability to communicate with peers.<br><span style="color:#010101;background-color:#E7E7E7">flowStartOperationalStatus</span> — describes a virtual node’s ability to run flows, to have checkpoints, and to continue in-progress flows.<br><span style="color:#010101;background-color:#E7E7E7">vaultDbOperationalStatus</span> — describes a virtual node’s ability to perform persistence operations on the virtual node’s vault.<span style="background-color:unset">These four statuses replace the existing</span> <span style="color:#010101;background-color:#E7E7E7">state</span> <span style="background-color:unset">field. The</span> <span style="color:#010101;background-color:#E7E7E7">GET virtualnode</span> <span style="background-color:unset">now returns the status of each of the four operational characteristics. Maintenance mode has been updated to disable all four of these new operational statuses. You can set this mode using the existing change virtual node state endpoint:</span> <span style="color:#010101;background-color:#E7E7E7">/api/v1/virtualnode/{virtualNodeShortHash}/state/{newState}</span><span style="background-color:unset">.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Upgrading a CPI</span> <span style="background-color:unset">- A new PUT method has been added to the</span> <span style="color:#010101;background-color:#E7E7E7">virtualnode</span> <span style="background-color:unset">resource to upgrade a virtual node’s CPI:</span> <span style="color:#010101;background-color:#E7E7E7">/api/v1/virtualnode/{virtualNodeShortHash}/cpi/{target-CPI-file-checksum}</span><span style="background-color:unset">. Before upgrading, the virtual node must be in maintenance mode with no other operations currently in progress. You can check the list of running flows using</span> <span style="color:#010101;background-color:#E7E7E7">GET /api/v1/flow/{virtualNodeShortHash}</span><span style="background-color:unset">. When the virtual node is in maintenance, and when no flows are running (that is, all flows have either “COMPLETED”, “FAILED” or “KILLED” status), it is safe to trigger a virtual node upgrade. The target CPI should have the same name, signer summary hash, and MGM group ID as the existing CPI.</span></td>
  </tr>
  <tr>
    <td class="tg-o7ty"><span style="font-weight:bolder">Corda CLI</span> <span style="background-color:unset">- Any worker and CLI long options that used camel case now use kebab case. This may require that existing scripts are updated.</span></td>
  </tr>
</tbody>
</table>

## Resolved Issues

| Domain  | Specific Change | 
| -------------------------------------------- | -------------------------------------------------- |
| **CorDapp Development**                      | **Flows with Transient Errors** - Flows did not correctly handle transient errors while sessions were in progress. In some cases, the 'error' flag was cleared early by other events, incorrectly indicating that the error had been resolved. This flag can now only be cleared when the event that caused the transient error is retried.  |

## Known Limitations and Issues

During the Beta process, R3 do not guarantee the stability of our user APIs. As a result, seemless upgrade between Beta versions is not supported.
