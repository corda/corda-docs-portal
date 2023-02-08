---
title: "Injectable Corda Services"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 1100
section_menu: corda-5-dev-preview
description: >
  A list of injectable platform Corda Services.
expiryDate: '2022-09-28'  
---

The following services are available for injection into flows and other Corda Services. You can also create custom Corda Services for injection.

{{< table >}}
|Class|Methods|Inject into|
|-|-|-|
|`net.corda.v5.application.flows.flowservices.FlowAuditor`|`checkFlowPermission`, `recordAuditEvent`|Flow|
|`net.corda.v5.application.flows.flowservices.FlowEngine`|`getRunId`, `isKilled`, `subFlow`, `checkFlowIsNotKilled`, `sleep`, `await`|Flow|
|`net.corda.v5.application.flows.flowservices.FlowIdentity`|`getOurIdentity`|Flow|
|`net.corda.v5.application.flows.flowservices.FlowMessaging`|`initiateFlow`, `receiveAllMap`, `receiveAll`, `sendAll`, `sendAllMap`, `close`|Flow|
|`net.corda.v5.ledger.flowservices.FlowLedger`|`waitForLedgerCommit`, `waitForStateConsumption`|Flow|
|`net.corda.impl.core.TopLevelFlow`|`currentTopLevel`|Flow, Corda Service|
|`net.corda.v5.application.cordapp.CordappProvider`|`appConfig`|Flow, Corda Service|
|`net.corda.v5.application.crypto.HashingService`|`hash`|Flow, Corda Service|
|`net.corda.v5.application.node.CordaClock`|`delegateClock`, `token`, `toToken`, `instant`, `getZone`, `withZone`|Flow, Corda Service|
|`net.corda.v5.application.node.NetworkParameters`|`get`, `keys`|Flow, Corda Service|
|`net.corda.v5.application.node.services.IdentityService`|`nameFromKey`, `anonymousPartyFromKey`, `partyFromName`, `partyFromAnonymous`, `registerKey`, `externalIdForPublicKey`, `publicKeysForExternalId`|Flow, Corda Service|
|`net.corda.v5.application.node.services.KeyManagementService`|`freshKey`, `filterMyKeys`, `sign`|Flow, Corda Service|
|`net.corda.v5.application.node.services.NetworkParametersService`|`currentHash`, `defaultHash`, `lookup`|Flow, Corda Service|
|`net.corda.v5.application.node.services.PersistenceService`|`persist`, `merge`, `remove`, `find`, `query`|Flow, Corda Service|
|`net.corda.v5.application.node.services.diagnostics.DiagnosticsService`|`nodeVersionInfo`|Flow, Corda Service|
|`net.corda.v5.application.serialization.SerializationService`|`serialize`, `deserialize`|Flow, Corda Service|
|`net.corda.v5.ledger.services.AttachmentStorage`|`openAttachment`, `importAttachment`, `queryAttachments`, `hasAttachment`, `getLatestContractAttachments`|Flow, Corda Service|
|`net.corda.v5.ledger.services.StateLoaderService`|`load`, `loadOrdered`|Flow, Corda Service|
|`net.corda.v5.ledger.services.TransactionMappingService`|`toLedgerTransaction`|Flow, Corda Service|
|`net.corda.v5.ledger.services.TransactionResolverService`|`resolve`, `resolveBaseTransaction`, `resolveTransactionWithSignatures`, `resolveNotaryChangeTransaction`, `resolveStateRefBinaryComponent`|Flow, Corda Service|
|`net.corda.v5.ledger.services.TransactionService`|`record`, `sign`, `createSignature`, `addNote`, `getNotes`|Flow, Corda Service|
|`net.corda.v5.ledger.services.TransactionStorage`|`getTransaction`|Flow, Corda Service|
|`net.corda.v5.ledger.services.TransactionVerificationService`|`verify`, `verifyRequiredSignatures`, `verifySignaturesExcept`|Flow, Corda Service|
|`net.corda.v5.ledger.transactions.TransactionBuilderFactory`|`create`|Flow, Corda Service|
|`net.corda.v5.ledger.services.vault.events.VaultStateEventService`|`subscribe`|Corda Service|
{{< /table >}}
