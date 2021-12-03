---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "payments"
    name: Payment Service
title: Payment Service
weight: 400
---
Use Payment Service flows to initiate payments and account management requests from a node on a Corda network. These requests can then be picked up by the [Payments Agent](payments-agent.md) on your network.

Use the Payment Service flows to:

* Create a request for a payment to be made. [MakePayment](#makepayment).
* Reinstate a stalled payment into the payment workflow. [ReinstatePayment](#reinstatepayment).
* Cancel a stalled payment. [CancelPayment](#cancelpayment).
* Update and reinstate a stalled payment into the payment workflow. [RemediatePayment](#remediatepayment).
* Return the list of payments stalled on an error. [StalledPayments](#stalledpayments).
* Return the payment state associated with a specific payment ID or provided transaction reference. [PaymentById](#paymentbyid).
* Return the PSPs that are configured on the system and available to use. [AvailablePSPs](#availablepsps).
* Return a PSP specification from the Payments Agent. [PspSpecification](#pspspecification).
* Add a payment account for an existing account on the PSP. [AddPaymentAccount](#addpaymentaccount).
* Create a customer account for an existing customer on the PSP. [CreateCustomerAccount](#createcustomeraccount).
* Add a beneficiary account for an external customer. [AddBeneficiaryAccount](#addbeneficiaryaccount).
* Update payment account details. [UpdatePaymentAccount](#updatepaymentaccount).
* Update a beneficiary account details. [UpdateBeneficiaryAccount](#updatebeneficiaryaccount).
* Return a list of payment accounts held by the owning party. [PaymentAccounts](#paymentaccounts).
* Return the payment account associated with a payment account ID. [PaymentAccountId](#paymentaccountbyid).
* Return a list of transactions made against this account. [Transactions](#transactions)
* Return a list of payments made on the system by a given payment account.
* Return the account balance for a given payment account ID. [AccountBalance](#accountbalance).
* Return the current default payment agent.

## `MakePayment`

Initiate a payment between participating nodes on the network.

### Parameters

* `amount`: Amount<`FiatCurrency`>. The amount and currency of the payment to make. In the Corda Payments Technical Preview, you can use GBP or EUR.
* `debtor`: String. A reference (signature) to debtor account (the account from which the payment is to be made - or the account from which `makePayment`is initiated) which is in turn resolved by the `AccountsResolver` service.
* `creditor`: String. A reference (signature) to creditor account (the account into which the payment is to be made) which is in turn resolved by the `AccountsResolver` service.
* `transactionRef`: String. Provided reference to the specified transaction. Bound to the externalId of the generated `PaymentState`'s `UniqueIdentifier`. Should be unique.

* `externalId`: String. Corresponds to the ID provided by the PSP.

### Return type

`PaymentState` - The object containing information regarding the requested payment.

## `ReinstatePayment`

Reinstate a stalled payment into the payment workflow.

### Parameters

* `paymentId` UUID. ID of the stalled payment to be reinstated.
* `comment` String. User supplied comment.  

### Return type

`PaymentState` - The object containing information regarding the requested payment.

## `CancelPayment`

Cancel a stalled payment.

### Parameters

* `paymentId` UUID. Payment ID of the stalled payment.
* `comment` String. User supplied comment.

### Return type

`PaymentState` - The object containing information regarding the requested payment.

## `RemediatePayment`

Update a stalled payment and reinstate into the payment workflow.

### Parameters

* `payment` The updated payment state.

### Return type

`PaymentState` - The object containing information regarding the requested payment.

## `StalledPayments`

Return a list of payments stalled on an error.

### Parameters

None.

### Return type

List of `PaymentState` objects for payments stalled on an error.

## `PaymentById`

Return the `PaymentState` associated with either a `paymentId` or `transactionRef`.

### Parameters

You can use either of the following:

* `paymentId`: UUID. The unique identifier component of the `PaymentState`.

* `transactionRef` UUID. The `externalId` component of the target `PaymentState`.

### Return type

* `PaymentState` - Object containing information regarding the requested payment.

## `AvailablePSPs`  

Get a list of the Payment Service Providers (PSPs) that are registered on the Payment Agent's node - making them available for payments on your network.

{{< note >}}
In Corda Payments Technical Preview the only possible available PSP is Modulr, and you connect with Modulr's sandbox environment - this is an in-memory mock PSP that is used for testing purposes only.
{{< /note >}}

### Parameters

None.

### Return type

`List<PSPSpecification>`. A list of PSP identifiers, such as "MODULR", that are available on the system to make payments against.

## `PspSpecification`

Return the PSP specification for the named PSP on the agent. In the Corda Payment Service Technical Preview, the PSP can only be Modulr.

### Parameters

* `name`. The name of the PSP.

### Return type

## `AddPaymentAccount`

Create a record of an existing payment account in the application. Without a payment account, you cannot make payments.

### Parameters

* `accountName`: String. Account name to be stored against the account details that are received from the PSP (Modulr).

* `currency`: FiatCurrency. The currency that the account should be created with.

* `psp`: String. The PSP to create the account with. In Corda Payments Technical Preview, this can only be Modulr.

* `agent`: Party [Optional]. The Payments Agent on your network. If not provided, the account will default to an agent configured via the node's Payment Service CorDapp config.

* `details`: Map<String, String> [Optional]. Additional Key-value data associated with the Payment Account. These details will be stored in the underlying `PaymentAccountDetailsState` shared between agent and node. They are not available through the returned `PaymentAccount` object.

### Return type

`PaymentAccount`: Object. The payment account details.

## `CreateCustomerAccount`

Create a record of payment account linked to a specific customer in the application.

### Parameters

* `accountName`. A common name for the account

* `currency`. The currency of the account

* `psp`. Payment Service Provider associated with this account

* `customerId`. ID of the customer who owns the account.

* `pspAccountId`. Original `accountId` on PSP for re-registered accounts.

### Return type

`PaymentAccount`: Object. The payment account details.

## `AddBeneficiaryAccount`

Create a local record of a beneficiary payment account for a party that is not present on the network.

### Parameters

* `accountName`. A common name for the account.
* `currency`. The currency required for the account.
* `psp`. Payment Service Provider associated with this account.
* `details`. Additional key-value data to be stored.

### Return type

`PaymentAccount`: Object. Contains details of the payment account.

## `UpdatePaymentAccount`

Send a request to update the underlying `PaymentAccountDetailsState` with the provided details.

### Parameters

* `details`: Map<String, String>. Additional Key-value data associated with the Payment Account. These details are stored in the underlying `PaymentAccountDetailsState` shared between agent and node - but are not available through the returned `PaymentAccount` object.

### Return type

`PaymentAccount`: Object. The payment account details.

## `UpdateBeneficiaryAccount`

Update a beneficiary payment account details. If an existing key is provided in `details`, the value will be updated. If a new key is provided, a new entry in the map will be created.

### Parameters

* `accountId`. The unique account identifier.
* `details`: Map<String, String>. Additional Key-value data associated with the Payment Account. These details are stored in the underlying `PaymentAccountDetailsState` shared between agent and node - but are not available through the returned `PaymentAccount` object.

### Return type

`PaymentAccount`: Object. The payment account details.

## `PaymentAccounts`

Get a list of `PaymentAccount`s for all the accounts owned by the party passed as a parameter.

The `AccountDetails` object captures the owning key for these details which could refer to a well known party or Corda account.

### Parameters

`owningParty`: `AbstractParty` - the owning party of the payment accounts.

### Return type

`List<PaymentAccount>` - The list of internal account references. Returns an empty list if none exist.

## `PaymentAccountById`

Get the `PaymentAccount` associated with a unique account identifier (signature).

### Parameters

`accountId`: String. A type of `PaymentAccountId`.

### Return type

`PaymentAccount`: The payment account object.


## `AccountBalance`

Get the account balance for a given payment account ID.

### Parameters

`accountId` : String. The payment account ID.

### Return type

`AccountBalance`. The balance of the requested account.

## `GetPaymentAgent`

Returns the current default payment agent, if it has been set. The default payment agent can be set through Cordapp config.

### Parameters

None.

### Return type

`AbstractParty`.
