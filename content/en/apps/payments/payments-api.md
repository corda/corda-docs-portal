---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: Corda Payments API
title: Corda Payments API
weight: 400
---
Use the Payment Service API to initiate payments from a node on a Corda network.

The methods listed below are triggered by flows within Corda.


## `makePayment`

Initiate a payment between participating nodes on the network.

### Parameters

* `amount`: Amount<`FiatCurrency`> - the amount and currency of the payment to make.

* `debtor`: String - a reference (signature) to debtor account (the account from which the payment is to be made - or the account from which `makePayment`is initiated) which is in turn resolved by the `AccountsResolver` service.

* `creditor`: String - a reference (signature) to creditor account (the account into which the payment is to be made) which is in turn resolved by the `AccountsResolver` service.

* `transactionRef`: String - provided reference to the specified transaction. Bound to the externalId of the generated `PaymentState`'s `UniqueIdentifier`. Should be unique.

* `externalId`: String - should correspond to the ID provided by the PSP.

### Return Type

PaymentState - This method will return the persisted `PaymentState` object containing information regarding the requested payment.

## `paymentById`

Find a payment with the provided payment id.

### Parameters

* `paymentId`: UUID - the UUID component of the PaymentState UniqueIdentifier

### Return Type

* `PaymentState` - This method will return the persisted PaymentState object\
containing information regarding the requested payment.

## `availablePSPs`

This method returns a list of the PSPs that are configured on the system.

### Return Type

List<String> - the list of PSP identifiers eg "MODULR" that are available on the system to make payments against.

## `createPaymentAccount`

Create a record of an existing payment account details in the application.

### Parameters

* `accountName`: String - Account name to be stored against the account details that are received from the PSP.

* `currency`: FiatCurrency - The currency that the account should be created with.

* `psp`: String - The PSP to create the account with.

* `agent`: Party [Optional] - the Agent which runs the Payment Service for operating on the account. If not provided, the account will default to an agent configured via the node's Payment Service CorDapp config.

* `details`: Map<String, String> - [OPTIONAL] additional Key-value data associated with the Payment Account. These details will be stored in the underlying PaymentAccountDetailsState shared between agent and node - but are NOT available through the returned PaymentAccount object.

### Return Type

`AccountDetails` - The payment account details.

## `updatePaymentAccount`

Send a request to the given PSP to update the underlying `PaymentAccountDetailsState` with the provided details.

### Parameters

details: Map<String, String> - additional Key-value data associated with the Payment Account. These details are stored in the underlying `PaymentAccountDetailsState` shared between agent and node - but are not available through the returned `PaymentAccount` object.

### Return Type

`AccountDetails` - The payment account details

## `paymentAccounts`

Get a list of `PaymentAccount`s for all the accounts owned by the party passed as a parameter.

The `AccountDetails` object captures the owning key for these details which could refer to a well known party or Corda account.

#### Parameters

`owningParty`: `AbstractParty` - the owning party of the payment accounts.

#### Return Type

`List<PaymentAccount>` - The list of internal account references. Returns an empty list if none exist.

## `paymentAccountById`

Get the `PaymentAccount` associated with a unique account identifier (signature).

#### Parameters

`accountSignature`: String - the signature matching the target's `PaymentAccount.signature`

#### Return Type

`PaymentAccount` - The payment account object.


## `localTransactions`

This method returns the PaymentState for all payments made on the payment service for a given account while restricting the results to local transactions - those made only through the Corda Payments Service and which were requested by this node. (For a set of all payments related to the account see [transactions].

### Parameters

*  `accountSignature`: String - the account reference to query the vault against

*  `fromTime`: Instant - start of time-window

*  `toTime`: Instant - end of time-window

*  `queryCriteria`: QueryCriteria.VaultQueryCriteria? - [Optional] additional query constraints

*  `paging`: PageSpecification? - [Optional]

### Return Type

`List<PaymentState>` - the list of completed transactions made by the account

## `accountBalance`

This method is called to get the balance of an account.

### Parameters

`accountSignature` : String - payment account reference

### Return Type

`Amount<FiatCurrency>`- This method will return the balance of the account in a given currency
