---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: The Payments Agent
title: Learn more about the Payments Agent CorDapp
weight: 300
---

The Payments Agent CorDapp is hosted by a trusted member of a network, such as the Business Network Operator (BNO). In this technical preview, you can assign the role of Payments Agent to a node on your local network.

## Payments Agent and the PSP

In the role of Payments Agent on a network, you are responsible for the connection between your node and the Payment Service Provider (PSP) you are using—in the technical preview, this is Modulr. You must have an account with Modulr in order to act as the Payments Agent, and to make use of this technical preview.

## Customers of the Payments Agent

As the Payments Agent, you can consider members of your network who wish to make payments as your **Customers**. In this documentation, any reference to a customer or customer ID refers to members of a network who wish to make payments using Corda Payments with you as their Payments Agent.

Before you can create accounts for a party on your network, you must add them as a customer.

Using the Payments Agent CorDapp, you can manage your customers' payment accounts and payment requests. You can use the Payments Agent CorDapp endpoints to connect to a UI to perform tasks as required.

## Payments Agent flows

The Payments Agent CorDapp provides flows that correspond to API endpoints. You can use these flows to:

* Return a list of accounts based on defined search criteria. [Accounts](#accounts).
* Return a list of accounts based on payment IDs.
* Create customer accounts.
* Close accounts.
* Reinstate failed or incomplete payments.
* Review all payments from the network.
* Find payments by ID.

## `Accounts`

Returns set of accounts on the calling agent filtered by optional search predicates.

### Parameters

* `pageSpecification`. Set the page number and page size for returned query.
* `accountName`. Optional. The name of an account.
* `cordaX500Name`. Name of party in format "O=organisation, L=location, C=country".
* `currency`. Three letter ISO designation of the Fiat currency. For Modulr, this can be GBP or EUR.
* `customerId`. Unique reference based on hash of `customerName`, `owningParty`, `agentParty`, and `psp`.
* `psp`. Payment Service Provider for the accounts.
* `accountId`. Optional. The UUID for an account.
* `wildcard`. Optional catch-all for partial matches against any query-param.

### Return type

`PaymentAccountDetailsState`. A paged response according to `pageSpecification` parameter.

## `AccountsByPaymentID`

Return debtor and creditor account details for a `PaymentID`, or null if no matches are found.


### Parameters

`paymentId`. Either a customer supplied external ref or UUID portion of the payment `UniqueIdentifier`.

### Return type

`Pair<PaymentAccount, PaymentAccount>`. Two `PaymentAccounts` representing the debtor and the creditor involved in the payment.

## `AccountsOnPsp`

Return a page of accounts managed by the agent on a PSP. In Corda Payments Technical Preview, the only available PSP is Modulr, with payments simulated in the Modulr Sandbox.

### Parameters

None.

### Return type

`PagedResponse<AccountDetails>`. A paged response containing account details of the relevant accounts.

## `AccountSummary`

Return a summary of accounts for a specified account ID.

### Parameters

`accountID`. The UUID for the account.

### Return type

`AccountSummary` object containing:

* `accountName`. The name of an account.
* `currency`. Three letter ISO designation of the Fiat currency. For Modulr, this can be GBP or EUR.
* `psp`. Payment Service Provider for the account.
* `balance: Amount<FiatCurrency>`. The balance recorded in the appropriate currency for the account.
* `customerId`. Your UUID for your customer on the network.
* `details: Map<String, String>`. Optional details of your customer or their account.
* `accountId`. The UUID for an account.
* `accountType`.

## `CreateCustomer`

Set up a member of your network as a customer.

### Parameters

* `customerName`
* `ownerName`
* `psp`
* `pspCustomerId`
* `details`

### Return type

`CustomerDetails`.

## `CreateAccount`

Allow an administrator on the Payments Agent node to create an account on behalf of a customer.

### Parameters

* `accountName`. The account name.
* `currency`. The currency to be used for the account.
* `customerId`. Your UUID for your customer on the network.
* `pspAccountId`. The account ID as on the PSP.

### Return type

`PaymentAccountDetailsState`.

## `CloseAccount`

Close an account. The account must have zero balance. The flow may block if the account's node is unavailable, so a timeout is set.

### Parameters

`accountId`. Account ID in the vault.

### Return type

`AccountSummary`.

## `Currencies`

Get a set of all currencies the agent's provided PSPs allow.

### Parameters

None.

### Return type

`Set<FiatCurrency>`.

## `Customer`

Return a customer managed by the agent.

### Parameters

`customerId`. Your UUID for your customer on the network.

### Return type

`CustomerDetails`.

## `CustomerAccounts`

Return a list of accounts owned by a specified customer.

### Parameters

`customerId`. Your UUID for your customer on the network.

### Return type

`PagedResponse<PaymentAccount>`.

## `CustomersOnPSP`

Return a page of customers managed by the agent on a PSP.

### Parameters

`CustomerDetailsCriteria`.

### Return type

`PagedResponse<CustomerDetails>`. A paged response containing account details of the relevant accounts.

## `CustomersOnVault`

Return a page of customers managed by the agent.

### Parameters

`CustomerDetailsCriteria`.

### Return type

`PagedResponse<CustomerDetails>`. A paged response containing account details of the relevant accounts.

## `Parties`

Return parties from network map.

### Parameters

None.

### Return type

`List<CordaX500Name>`. List of parties on the network.

## `PaymentById`

Return the most current payment from ID or null.

### Parameters

`paymentId`. Either a customer supplied external ref or UUID portion of the payment `UniqueIdentifier`.

### Return type

`PaymentState`.

## `PaymentMessages`

List the agent and system messages for a `paymentId`.

### Parameters

`paymentId`. Payments unique or external identifier.

### Return type

`List<String>`.

## `PaymentRequestMessages`

Return comments and messages linked to a payment request via `paymentId`.

### Parameters

`paymentId`. Payments unique or external identifier.

### Return type

`PaymentRequestMessage`.

## `RecordUser`

Register a user's credentials once they have been authenticated.

### Parameters

`user`. User credentials.

### Return type

No return - the user's credentials are registered.

## `ReinstatePayment`

Cancel or reinstate a payment onto the workflow after an error. The command must be one of the `PaymentCommands` types.

### Parameters

* `paymentId`. Payments unique or external identifier.
* `command`. Command used for reinstatement or cancellation.
* `comment`. Reason for reinstatement or cancellation.

### Return type

## `RetrieveUser`

Retrieve a user from the node service cache.

### Parameters

`username`. RPC username for the required user.

### Return type

`AgentUIService.AgentUser`.

## `RetrieveUserRole`

Retrieves the role for a named user.

### Parameters

`username`. RPC username.
`password`. RPC password.

### Return type

`string`.

## `StalledPayments`

Return a paged list of stalled payments from the vault.

### Parameters

* `stallStatuses`.
* `psp`.
* `paymentId`.

### Return type

`PagedResponse<StalledPayment>`.

## `Transactions`

Return the transaction for `accountId` based on the criteria.

### Parameters

* `accountId: PaymentAccountId`.
* `criteria: PaymentTransactionCriteria`.

### Return type

`PagedResponse<PaymentTransaction>`.

## `UpdateCustomer`

Update a customer on the agent.

### Parameters

* `customerId: String`.
* `details: Map<String, Any>`.
* `deleted: List<String>`.

### Return type

`CustomerDetails`
