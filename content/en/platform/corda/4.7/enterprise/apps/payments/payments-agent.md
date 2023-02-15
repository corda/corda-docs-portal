---
title: "Payments agent"
date: '2023-02-14'
menu:
  corda-enterprise-4-7:
    parent: payments
    weight: 500
    name: "Payments agent"
section_menu: corda-enterprise-4-7
---

The Payments Agent CorDapp is hosted by a trusted member of a network, such as the Business Network Operator (BNO). In this technical preview, you can assign the role of Payments Agent to a node on your local network by adding the CorDapp to that node.

## Payments Agent and the PSP

In the role of Payments Agent on a network, you are responsible for the connection between your node and the Payment Service Provider (PSP) you are using—in the technical preview, this is Modulr. You must have an account with Modulr in order to act as the Payments Agent, and to make use of this technical preview.

## Customers of the Payments Agent

As the Payments Agent, you can consider members of your network who wish to make payments as your **customers**. In this documentation, any reference to a customer or customer ID refers to members of a network who wish to make payments using Corda Payments with you as their Payments Agent.

Before you can create accounts for a party on your network, you must add them as a customer.

Using the Payments Agent CorDapp, you can manage your customers' payment accounts and payment requests. You can use the Payments Agent CorDapp endpoints to connect to a UI to perform tasks as required.

## Payments Agent flows

The Payments Agent CorDapp provides flows that correspond to API endpoints. You can use these flows to:

* Close an account. [CloseAccountDetails](#closeaccountdetails).
* Close down the customer details on the vault. [CloseCustomerDetails](#closecustomerdetails).
* Create a customer account state object in the vault. [CreateAccountDetails](#createaccountdetails).
* Create a customer details state in the vault. [CreateCustomerDetails](#createcustomerdetails).
* Get the balance of an account. [GetAccountBalance](#getaccountbalance).
* Get a list of available PSPs. [GetAvailablePSPs](#getavailablepsps).
* Get a list of available currencies available to the Payments Agent. [GetCurrenciesOnAgent](#getcurrenciesonagent).
* Get a list of customer accounts. [GetCustomerAccounts](#getcustomeraccounts).
* Get a payment account. [GetPaymentAccount](#getpaymentaccount).
* Get a list of customers that you manage on the PSP. [GetPSPAccounts](#getpspaccounts).
* Return a page of customers managed by the agent on the PSP. [GetPSPCustomers](#getpspcustomers).
* Return the specification of the PSP. [GetPSPSpecification](#getpspspecification).
* Return a list of transactions based on specified criteria. [GetTransactions](#gettransactions).
* Update details of a customer by updating the details state object in the vault. [UpdateCustomerDetails](#updatecustomerdetails).

## `CloseAccountDetails`

Close an account state on the vault.

### Parameters

`accountId`. The account ID in the vault.


### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class CloseAccountDetails(
    private val accountId: PaymentAccountId
) : CloseAccountDetailsInitiator()
```

### Return type

```
FlowLogic<Unit>
```

### Example

```
startFlow(
    ::CloseAccountDetails,
    accountId
)
```

## `CloseCustomerDetails`

Close a customer details state on the vault.

### Parameters

`customerId: PaymentCustomerId`

### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class CloseCustomerDetails(
    private val customerId: PaymentCustomerId
) : CloseCustomerDetailsInitiator()
```

### Return type

```
FlowLogic<CustomerDetailsState>
```

### Example

```
startFlow(::CloseCustomerDetails, customerId)
```

## `CreateAccountDetails`

Create a customer account state object in the vault.

### Parameters

* `accountName`. Account name.
* `currency`. Account currency.
* `customerId`. Existing customer who will own the account.
* `pspAccountId`. Optional. Existing Modulr account to link to.

### Flow signature

```
@StartableByRPC
@Suppress("unused")
class CreateAccountDetails(
    private val accountName: String,
    private val currency: String,
    private val customerId: String,
    private val pspAccountId: String?
) : CreateAccountDetailsInitiator()
```

### Return type

`FlowLogic<PaymentAccountDetailsState>`

### Example

```
startFlow(
    ::CreateAccountDetails,
    accountName,
    currency,
    customerId,
    pspAccountId
)
```

## `CreateCustomerDetails`

Create a payment customer details state object in the vault. If the customer already exists then a flow exception is thrown.

### Parameters

* `paymentCustomer`. Customer name.
* `details`. Customer details.

### Flow signature

```
@StartableByRPC
@Suppress("unused")
class CreateCustomerDetails(
    private val paymentCustomer: PaymentCustomer,
    private val details: Map<String, Any>
) : CreateCustomerDetailsInitiator()
```
### Return type
```
FlowLogic<CustomerDetailsState>
```
### Example
```
startFlow(::CreateCustomerDetails, customer, details)
```

## `GetAccountBalance`

Return the `AccountBalance` for a given `accountId`. Internal flow logic for use by responder and direct for agent UI interactions.

### Parameters

* `accountId`. The ID associated with the account.

### Flow signature

```
@StartableByRPC
class GetAccountBalance(
    private val accountId: PaymentAccountId
) : FlowLogic<AccountBalance>()
```
### Return type

```
FlowLogic<AccountBalance>
```

### Example

```
startFlow(
    ::GetAccountBalance,
    accountId
)
```

## `GetAvailablePSPs`

Returns a list of the PSPs that are configured on the Payments application.

### Parameters

None.

### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class GetAvailablePSPs : FlowLogic<List<String>>()
```

### Return type

```
FlowLogic<List<String>>
```
### Example

```
startFlow(::GetAvailablePSPs)
```

## `GetCurrenciesOnAgent`

Return all currencies provided by the Payments Agent's PSPs integrations.

### Parameters

None.


### Flow signature

```
@StartableByRPC
class GetCurrenciesOnAgent() : FlowLogic<Set<FiatCurrency>>()
```

### Return type

```
FlowLogic<Set<FiatCurrency>>
```
### Example

```
startFlow(::GetCurrenciesOnAgent)
```

## `GetCustomerAccounts`

Return a list of accounts associated with a customer.

### Parameters

```
private val customerId: String
```

### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class GetCustomerAccounts(private val customerId: String) : FlowLogic<List<PaymentAccount>>() {
```
### Return type

```
FlowLogic<List<PaymentAccount>>
```
### Example

```
startFlow(::GetCustomerAccounts, customerId)
```

## `GetPaymentAccount`

Return the `PaymentAccount` for a given `PaymentAccountId`. Internal flow logic for use by responder and direct for agent UI interactions.

Will return from local cache map if available; else fetches from vault query, adds to cache, then returns.

### Parameters

`paymentAccountId: PaymentAccountId`

### Flow signature

```
@StartableByRPC
class GetPaymentAccount(private val paymentAccountId: PaymentAccountId) : FlowLogic<PaymentAccount>()
```
### Return type

```
FlowLogic<PaymentAccount>
```
### Example

```
startFlow(::GetPaymentAccount, paymentAccountId)
```

## `GetPSPAccounts`

Return a page of customers managed by the agent on the PSP.

### Parameters

Search criteria.

### Flow signature

```
@StartableByRPC
class GetPSPAccounts(
    private val criteria: AccountDetailsCriteria
) : FlowLogic<PagedResponse<AccountDetails>>()
```
### Return type

```
FlowLogic<PagedResponse<AccountDetails>>
```
### Example

```
startFlow(::GetPSPAccounts, criteria)
```

## `GetPSPCustomers`

Return a page of customers managed by the agent on the PSP.

### Parameters

Search criteria.

### Flow signature

```
@StartableByRPC
class GetPSPCustomers(
    private val criteria: CustomerDetailsCriteria
) : FlowLogic<PagedResponse<CustomerDetails>>()
```
### Return type

```
FlowLogic<PagedResponse<CustomerDetails>>
```
### Example

```
startFlow(::GetPSPCustomers, criteria)
```

## `GetPSPSpecification`

Returns a PSP specification.

### Parameters

```
private val psp: String
```
### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class GetPSPSpecification(private val psp: String) : FlowLogic<PSPSpecification>()
```
### Return type

```
FlowLogic<PSPSpecification>
```
### Example

```
startFlow(::GetPSPSpecification, psp.toUpperCase())
```

## `GetTransactions`

Return the transaction history of an account.

### Parameters

* `accountId:` String. The account ID.
* `criteria: PaymentTransactionCriteria`.

### Flow signature

```
@StartableByRPC
@StartableByService
@Suppress("unused")
class GetTransactions(
    private val accountId: String,
    private val criteria: PaymentTransactionCriteria
) : FlowLogic<PagedResponse<PaymentTransaction>>()
```
### Return type

```
FlowLogic<PagedResponse<PaymentTransaction>>
```
### Example

```
startFlow(::GetTransactions, accountId, criteria)
```

## `UpdateCustomerDetails`

Update a payment customer details state object in the vault.

### Parameters

`customerId`. Customer Id.
`details`. Customer details.
`deleted`. Customer details to be deleted.

### Flow signature

```
@StartableByRPC
@Suppress("unused")
class UpdateCustomerDetails(
    private val customerId: PaymentCustomerId,
    private val details: Map<String, Any>,
    private val deleted: List<String> = emptyList()
) : UpdateCustomerDetailsInitiator()
```
### Return type

```
FlowLogic<CustomerDetailsState>
```
### Example

```
startFlow(
  ::UpdateCustomerDetails,
  customerId,
  details,
  deleted
)
```
