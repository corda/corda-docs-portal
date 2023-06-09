---
date: '2023-01-30'
version: 'Corda 5.0'
title: "net.corda.v5.ledger.utxo.token.selection"
menu:
  corda5:
    identifier: corda5-api-ledger-utxo-token-selection
    parent: corda5-api
    weight: 4000
section_menu: corda5
---
# net.corda.v5.ledger.utxo.token.selection
The Token Selection API enables a flow to exclusively select a set of states to potentially use as input states in a UTXO transaction. Although this can be achieved with simple vault queries, the selection API offers the following key features that improve the performance and reliability of the flows:

* **Exclusivity:** In an environment where multiple instances of a flow are running in parallel, it is important that each flow can exclusively claim states to spend. Without this, there is a high chance that multiple flows could attempt to spend the same states at the same time, causing transactions to fail during notarization, due to an attempt to spend a state that has already been spent.
* **Target Amount Selection:** When selecting fungible states to spend, it is usual to select multiple states that sum to at least the target value of the proposed transaction. The selection API provides an explicit model for achieving this, which would be difficult to achieve using standard vault queries.
* **Performance:** Providing a dedicated API for this specific type of state selection allows implementations that are not coupled to the vault query API and therefore can be optimized for the specific query patterns.
<!-->
{{< note >}}
To learn more about using the Token Selection API, see [Using the UTXO Ledger Token Selection API]() in the Tutorials section.
{{< /note >}}-->

## Token Selection Components

### Tokens

The API defines a generic token that is used to represent a state. The purpose of the token is to allow a consistent model for querying user-defined states. Attributes of the token are partly derived by the platform and partly derived by the CorDapp using an implementation of `UtxoLedgerTokenStateObserver` for the given state. The following table describes these attributes:
| <div style="width:100px">Attribute    </div>    | <div style="width:100px">Type       </div>      | <div style="width:100px">Provided By </div>| Description                                                                                                                                                                             |
| ---------------- | ---------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| StateRef         | StateRef         | Platform    | The reference to the state linked to this token.                                                                                                                                        |
| Notary X500 Name | MemberX500Name | Platform    | The notary of the state linked to this token.                                                                                                                                           |
| Token Type       | String           | Both        | By default, the platform sets this to the FQN name of the Java Type of the state class this token is linked to. As a CorDapp Developer, you can override this with your own definition. |
| Issuer Hash      | SecureHash       | User        | The hash of the issuer of the state, as defined by the CorDapp Developer.                                                                                                               |
| Symbol           | String           | User        | The user-defined symbol for the token.                                                                                                                                                  |
| Amount           | BigDecimal       | User        | The amount/value of the state linked to this token.                                                                                                                                     |
| Tag              | String           | User        | An optional string that can be searched using a regular expression when selecting tokens.                                                                                               |
| Owner Hash       | SecureHash       | User        | An optional hash of the owner of the state.                                                                                                                                             |

### Token Pools

Tokens are grouped into pools using the following fields as the key:
* Notary
* Type
* Symbol
* Issuer
The API allows a flow to claim tokens from a single pool of tokens for a given query. It is not possible to select tokens from multiple pools in a single query.

### Token Observers
A token observer converts a custom state into a token when a transaction is finalized and persisted in the vault. The CorDapp Developer implements the `UtxoLedgerTokenStateObserver` interface for a state type that is required for selection. The platform uses these observers to generate a token for each produced state when persisting a finalized transaction to the vault.

### Claim Query
When a flow needs to select fungible states to spend, it can execute a claim query using the `TokenSelection` API. The API supports a single method `tryClaim` that takes a `TokenClaimCriteria` describing the target amount required and the type of tokens required. 

### Token Claim
When a flow executes a successful query to select tokens via the selection API, it receives a Token Claim. The claim represents a list of tokens that have been exclusively claimed and can be used as inputs to a new transaction. Once the flow has completed (successfully or not), it should release the claim, signaling which tokens, if any, were consumed in a transaction. Any unused tokens are released back to the pool for others to use.

## Token Eligibility
As described, a token is a representation of state that is available to be spent. The following rules control the eligibility of a token/state for selection:

* **Consumed/Unconsumed Status:** Only tokens that are unconsumed are eligible for selection. When a transaction is finalized, all the input states for that transaction are considered consumed and immediately become ineligible for selection. Conversely, any output states of a finalized transaction, become available for selection, if the other criteria below are met.
* **Relevancy:** By default, a state is relevant if the holding identity (node) is a participant in the transaction. However, you can control the relevancy of a state by implementing the `isRelevant` method on the states' contract. Only output states marked as `isRelevant=true` are available for selection.
* **State Observer:** Only states that have an associated implementation of `UtxoLedgerTokenStateObserver` are available for selection.