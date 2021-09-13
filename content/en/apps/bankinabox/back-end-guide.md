---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "bankinabox"
    identifier: bank-in-a-box-back-end-guide
tags:
- Bank in a Box
- back end
title: Back end guide
weight: 200
---

# Back end guide

The Bank in a Box application allows a user to replicate standard banking application services on Corda. These services include:

- Accounts.
- Deposits and withdrawals.
- Loans.
- Reports and views.

These services are implemented utilising specific Corda features, demonstrating best practices for how a banking application should be built on Corda. Below you can read more on how the following features are implemented:

- Flows.
- Accounts SDK.
- Scheduled states.
- Oracles.
- CorDapp integration with external systems.

## Accounts

The Bank in a Box application utilises the [Accounts SDK](https://github.com/corda/accounts/blob/master/docs.md) to implement current and savings accounts for bank customers. The Accounts SDK is a library which allows a Corda node to partition the vault into a number of subsets, where each subset represents an account. Bank in a Box shows you how to implement this feature in your own banking application.

### Business logic

The business logic behind Bank in a Box accounts is explained below, addressing:

- [Account status](#account-status) - how account statuses are implemented in the application.
- [Extending the mapped schema](#extending-the-mapped-schema) - how the the account schema is returned using the `generateMappedObject` method.
- [Implementing the withdraw method with overdraft support](#implementing-the-withdraw-method-with-overdraft-support) - how overdraft support is implemented in the application.
- [Custom serialization](#custom-serialization) - how custom serializers are implemented to generate the serialization for Kryo.

#### Account Status

The status of an account can be `PENDING`, when an account is first created and is awaiting approval, `ACTIVE` or `SUSPENDED`, where all account activity is frozen. There is a limit to status transitions, for example, an account that has been approved can never be set to status pending. An extension function has been implemented to verify the status transitions.

```kotlin
fun AccountStatus.canProgressToStatus(accountStatus: AccountStatus) =
    when(this) {
        AccountStatus.SUSPENDED -> accountStatus == AccountStatus.ACTIVE
        AccountStatus.PENDING -> accountStatus == AccountStatus.ACTIVE || accountStatus == AccountStatus.SUSPENDED
        AccountStatus.ACTIVE -> accountStatus == AccountStatus.SUSPENDED
    }
```

#### Extending the mapped schema

The `generateMappedObject` method returns a representation of the given schema, and for the Account interface it is implemented as follows:

```kotlin
override fun generateMappedObject(schema: MappedSchema): PersistentState {
    return when (schema) {
        is AccountStateSchemaV1 -> AccountStateSchemaV1.PersistentBalance(
                this.accountInfo.identifier.id,
                this.balance.quantity,
                this.txDate,
                this.status,
                this.customerId,
                this.linearId.id)
        else -> throw IllegalArgumentException("Unrecognised schema $schema")
    }
}
```

The CreditAccount interface adds the additional properties `withdrawalDailyLimit` and `transferDailyLimit`, and the above method needs to be overridden in order for these properties to be accessible within the schema.

The following shows how these properties can be added to the mapped object listed above:

```kotlin
override fun generateMappedObject(schema: MappedSchema): PersistentState {
    val persistentState = super.generateMappedObject(schema)
    if (persistentState !is AccountStateSchemaV1.PersistentBalance) {
        throw IllegalArgumentException("Schema $schema is not a AccountStateSchemaV1.PersistentBalance schema type")
    }

    persistentState.withdrawalDailyLimit = withdrawalDailyLimit
    persistentState.transferDailyLimit = transferDailyLimit

    return persistentState
}
```

#### Implementing the withdraw method with overdraft support

The `CurrentAccountState` extends the `CreditAccount` to support overdrawn balances up to an approved limit, and is facilitated with the following properties: `overdraftBalance` and `approvedOverdraftLimit`. The `overdraftBalance` property tracks the debit amount on the account and the `approvedOverdraftLimit` sets the maximum debited amount allowed. The withdraw method can be adapted as follows to allow overdraft withdrawals:

```kotlin
override fun withdraw(amount: Amount<TokenType>): CurrentAccountState {
    verifyHasSufficientFunds()
    verifyIsActive()

    return if(accountData.balance >= amount) {
        val updatedAccountData = accountData.copy(
                balance = accountData.balance - amount,
                txDate = Instant.now())
            copy(accountData = updatedAccountData)
        } else {
            val updatedOverdraftBalance = (overdraftBalance ?: 0L) + amount.quantity - accountData.balance.quantity
            val updatedAccountData = accountData.copy(
                    balance = 0 of accountData.balance.token,
                    txDate = Instant.now())
            copy(overdraftBalance = updatedOverdraftBalance, accountData = updatedAccountData)
        }
}
```

The method checks that the account has sufficient funds - in either the account balance or the `approvedOverdraftLimit` - and also that the account is active. If there are sufficient funds on the account balance, the account is debited as normal. Otherwise, `balance` is set to zero and `overdraftBalance` is set to the withdrawal amount with the available account balance deducted.

#### Custom serialization

Corda uses the [Kryo serializer](../../corda-os/4.7/serialization-index.md) to serialize objects on the call stack when suspending flows. There are known issues serializing JPA entity objects, particularly if they use one to many relationships or other complex structures. One approach to overcome this is to map entity objects to data classes, referred to as Data Transfer Objects (DTOs), for use within flows. Another approach is to implement custom serializers that generate the serialization for Kryo.

A custom serializer for a JPA entity can be specified with the `DefaultSerializer` annotation:

```kotlin
@Entity
@Table(name = "customer")
@DefaultSerializer(CustomerSchemaSerializer::class)
@CordaSerializable
class Customer (
)
```

A custom serializer should extend the Kryo `Serializer` abstract class, and implement the `read` and `write` methods. The following is a modified example of the `CustomerSchemaSerializer` class:

```kotlin
class CustomerSchemaSerializer : Serializer<CustomerSchemaV1.Customer>() {
    override fun write(kryo: Kryo, output: Output, `object`: CustomerSchemaV1.Customer) {
        output.writeString(`object`.createdOn.toString())
    }

    override fun read(
        kryo: Kryo,
        input: Input,
        type: Class<CustomerSchemaV1.Customer>?
    ): CustomerSchemaV1.Customer? {

        val createdOn = Instant.parse(input.readString())
        return CustomerSchemaV1.Customer(
            createdOn = createdOn,
            modifiedOn = Instant.now(),
            customerName = "",
            contactNumber = "",
            emailAddress = "",
            postCode = "",
            attachments = listOf())
    }
```

The above shows the serialization of the `createdOn` property in the Customer schema class. The write method tells Kryo explicitly how to serialize the object of type `CustomerSchemaV1.Customer`, and in this case, it simply converts the `createdOn` property into a string and writes it to the output. Similarly, the `read` method tells Kryo how to deserialize the stored properties and recreate an instance of `CustomerSchemaV1.Customer`. The `createdOn` property value is set by reading a single string from the input and uses the `Instant.parse` method to parse the string into an `Instant` type. An instance of the `Customer` schema class is created using the deserialized `createdOn` value (and in this example using empty values for the other properties that were not serialized), and is returned.

## Flows for accounts

Using the flows in this section, several account-related tasks can be accomplished. You can:

* Create a new customer [`CreateCustomerFlow`](#createcustomerflow).
* Update customer information [(`UpdateCustomerFlow`)](#updatecustomerflow).
* Create a current account for a customer [(`CreateCurrentAccountFlow`)](#createcurrentaccountflow).
* Create a savings account for a customer [(`CreateSavingsAccountFlow`)](#createsavingsaccountflow).
* Set an account status of active or suspended [(`SetAccountStatusFlow`)](#setaccountstatusflow).
* Set a limit on daily transfers or withdrawals from an account [(`SetAccountLimitsFlow`)](#setaccountlimitsflow).
* Approve an overdraft limit for an account [(`ApproveOverdraftFlow`)](#approveoverdraftflow).

### `CreateCustomerFlow`

To create a new customer, use the `CreateCustomerFlow`. This flow also adds personal details and contact information, and returns the customer ID.

`CreateCustomerFlow(customerName: String, contactNumber: String, emailAddress: String, postCode: String, attachments: List<Pair<SecureHash, String>>): UUID`

* `customerName`: Customer name.
* `contactNumber`: Customer phone number.
* `emailAddress`: Customer email address.
* `postCode`: Post code of customer's address.
* `attachments`: List of `SecureHash`, `String` pairs with references to the Corda attachments of additional customer documentation. For more information on the standard process for uploading attachments to Corda, see the documentation on [CorDapp Contract Attachments](../../corda-os/4.7/cordapp-build-systems.md#cordapp-contract-attachments).

This flows returns `UUID`, the customer ID.


### `UpdateCustomerFlow`

Use `UpdateCustomerFlow` to update customer information including customer name, post code, contact number, and email address. You can also append a new attachment used for identity verification.

`UpdateCustomerFlow(customerId: UUID, customerName: String?, postCode: String?, contactNumber: String?, emailAddress: String?, attachments: List<Pair<SecureHash, String>>?)`

* `customerId`: `UUID` - The ID of the customer's profile.
* `customerName`: Customer name.
* `contactNumber`: Customer phone number.
* `emailAddress`: Customer email address.
* `postCode`: Post code of customer's address.
* `attachments`: List of `SecureHash`, `String` pairs with references to the Corda attachments of additional customer documentation.

This flow returns a merged attachments list, comprised of `customer.attachments` and `this.attachment`.


### `CreateCurrentAccountFlow`

Use `CreateCurrentAccountFlow` to create a zero balance current account for the customer with ID `customerId`, optionally specifying a withdrawal and/or transfer daily limit.

`CreateCurrentAccountFlow(customerId: UUID, tokenType: Currency, withdrawalDailyLimit: Long?, transferDailyLimit: Long?): SignedTransaction`

* `customerId: UUID` - The ID of the customer's profile.
* `tokenType`: `Currency` - The currency of the customer's profile.
* `withdrawalDailyLimit`(optional): This sets a daily limit on withdrawal amount.
* `transferDailyLimit`(optional): This sets a daily limit on transfer amount.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the account has been created.


### `CreateSavingsAccountFlow`

To create a savings account, use `CreateSavingsAccountFlow`. This creates a zero balance savings account for a customer with ID `customerId`.

`CreateSavingsAccountFlow(customerId: UUID, tokenType: Currency): SignedTransaction`

* `customerId: UUID` - The ID of the customer's profile.
* `tokenType: Currency` - The currency of the customer's profile.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the savings account has been created.


### `SetAccountStatusFlow`

`SetAccountStatusFlow` updates the status of the account with ID `accountId`. You can use this flow to manually approve a pending account by setting the status to `ACTIVE`, or to suspend or reactivate an account, by setting the status to `SUSPENDED` or `ACTIVE`, respectively.

`SetAccountStatusFlow(accountId: UUID, accountStatus: AccountStatus): SignedTransaction`

* `accountId: UUID` - The ID of a customer account.
* `accountStatus: AccountStatus` - `Active` or `Suspended`.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the status of the account has been updated.


### `SetAccountLimitsFlow`

Use `SetAccountLimitsFlow` to change the daily limits, or maximum spending, for the provided account.

`SetAccountLimitsFlow(accountId: UUID, withdrawalDailyLimit: Long?, transferDailyLimit: Long?): SignedTransaction`

* `accountId: UUID` of a current account.
* `withdrawalDailyLimit`: Daily limit on amount the customer can withdraw.
* `transferDailyLimit`: Daily limit on amount the customer can transfer.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the account limits are changed.


### `ApproveOverdraftFlow`

Use `ApproveOverdraftFlow` to approve an overdraft limit for the account with ID `accountId`.

`ApproveOverdraftFlow(accountId: UUID, amount: Amount<Currency>): SignedTransaction`

* `accountId: UUID` - The ID of a current account.
* `amount`: Overdraft amount approved.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the overdraft limit has been set.


### Examples

#### Create a new customer account

```kotlin
val supportingDocumentationPath = File("/path/to/supportDocumentation.zip")

val attachment = serviceHub.attachments.importAttachment(
        supportingDocumentationPath.inputStream(),
        ourIdentity.toString(),
        supportingDocumentationPath.name)

val attachments = listOf(Pair(attachment, "Supporting documentation"))

val customerId = subFlow(
    CreateCustomerFlow(
        customerName = "AN Other",
        contactNumber = "5551234",
        emailAddress = "another@r3.com",
        postCode = "ZIP 1234",
        attachments = attachments))
```

#### Create a new current account

```kotlin
val signedTx = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = Currency.getInstance("EUR"),
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val accountId = signedTx.tx.outputsOfType<CurrentAccountState>().single().accountId
```

#### Set account to active

```kotlin
subFlow(SetAccountStatusFlow(accountId, AccountStatus.ACTIVE))
```

#### Approve overdraft

```kotlin
val amount = Amount(10000, Currency.getInstance("EUR")) // 100 euro
subFlow(ApproveOverdraftFlow(accountId, amount))
```

{{< note >}}
`amount` values are in the base unit of the selected currency. In the example above, the currency is set to euros so the base unit is cents. This is why an `amount` of `10000` in this flow approves an overdraft of 100 euros.
{{< /note >}}


## Loans

The Bank in a Box application uses [Oracles](../../corda-os/4.7/key-concepts-oracles.md#oracles) in various contexts, one of which is in the issuance of loans. A dummy Oracle is used to call external services based on a customer ID and sign off on the loan. The response is then embedded in the transaction that issues the loan. This mimics a real-life scenario where a bank calls a rating provider before giving a customer a loan.

Oracle signatures use [partial Merkle tree signing](../../corda-os/4.7/key-concepts-tearoffs.md#hiding-data), which provides privacy for the transaction. In this way, the external party present in the loan issuance transaction can only see the contents of the transaction that they must confirm before signing the transaction.

When a loan is issued, money is transferred to the customer's current account. In the background, this transaction uses [Corda scheduled states](../../corda-os/4.7/event-scheduling.md#implementing-scheduled-events) to create a recurring payment for that loan, into the loan account.

### Business logic

The business logic behind Bank in a Box loans is explained below, addressing:

- [Accessing web services within flows](#accessing-web-services-within-flows) - how off-ledger web services are accessed within flows.
- [Implementing an Oracle](#implementing-an-oracle) - how Oracles are implemented and used in transactions in Bank in a Box.

#### Accessing web services within flows

The off-ledger credit rating web service implements a REST API and the following describes the approach to query this service within a flow.

The web service request is blocking and needs to be executed outside of the flow execution thread. Flow external operations are designed for this purpose and its `execute` method can be overridden with the desired blocking behaviour. The following is a skeleton implementation of the credit rating request class:

```kotlin
class CreditRatingRequestOperation(
    val customerId: UUID,
    private val creditRatingServiceAddr: String): FlowExternalOperation<CreditRatingInfo> {

    companion object {
        val httpClient: OkHttpClient =  OkHttpClient.Builder().build()
    }

    @Suspendable
    override fun execute(deduplicationId: String): CreditRatingInfo {
        // implement REST API client request
    }
}
```
The REST API URL is generated from the credit rating service server address and the customer ID to query. The request is made using the `httpClient` and the response is deserialized into a `CreditRatingInfo` instance using the `objectMapper`.

The above request can then be called within a flow:

```kotlin
@StartableByRPC
class GetCustomerCreditRatingFlow(val customerId: UUID) : FlowLogic<CreditRatingInfo>() {

    @Suspendable
    override fun call(): CreditRatingInfo {
        return await(CreditRatingRequestOperation(customerId, serviceHub))
    }
}
```

#### Implementing an Oracle

A node can request a command asserting a fact from an Oracle. The following shows an example implementation of a request flow:

```kotlin
@InitiatingFlow
class OracleSignCreditRatingRequestFlow(
    val tx: TransactionBuilder,
    val oracle: Party,
    val partialMerkleTx: FilteredTransaction) : FlowLogic<TransactionSignature>() {

    @Suspendable
    override fun call(): TransactionSignature {
        val oracleSession = initiateFlow(oracle)
        val resp = oracleSession.sendAndReceive<TransactionSignature>(partialMerkleTx)

        return resp.unwrap { sig ->
            check(oracleSession.counterparty.owningKey.isFulfilledBy(listOf(sig.by)))
            tx.toWireTransaction(serviceHub).checkSignature(sig)
            sig
        }
    }
}
```

The flow initiates a session with the Oracle and the filtered transaction containing the command to be verified is sent. The Oracle verifies the filtered transaction and returns a signature (see below). The request receives the signature and it is checked against the transaction `tx` to ensure the signature is valid for that transaction.

The Oracle implements the responder flow. The following is an example of a skeleton implementation:

```kotlin
@InitiatedBy(OracleSignCreditRatingRequestFlow::class)
class OracleSignCreditRatingRequestFlowResponder(val otherSession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val filteredTx = otherSession.receive<FilteredTransaction>().unwrap { it }

        // Here the method performs two checks:
        // Verifies that the command information is visible and that it has the appropriate signer

        // Verifies the command

        val signatureMetadata = SignatureMetadata(
            serviceHub.myInfo.platformVersion,
            Crypto.findSignatureScheme(ourIdentity.owningKey).schemeNumberID)

        val signableData = SignableData(filteredTx.id, signatureMetadata)
        val signature = serviceHub.keyManagementService.sign(signableData, ourIdentity.owningKey)

        otherSession.send(signature)
    }
}
```

The Oracle receives the filtered transaction and checks that the command to be verified is visible and that the Oracle is a requested signer (implementation not shown). The command is verified (again, implementation not shown), a signature is created and returned to the requesting flow. It is possible to send the signed transaction, however only the signature is required in this case.

##### Using Oracles in transactions

The credit rating Oracle verifies the credit rating of a customer contained within the `VerifyCreditRating` command, and signs the transaction if the rating is valid. The command is created as follows:

```kotlin
val oracle: Party = ConfigurationUtils.getConfiguredOracle(serviceHub)

val creditRatingInfo = subFlow(GetCustomerCreditRatingFlow(customerId))

val creditRatingThreshold = ConfigurationUtils.getCreditRatingThreshold(serviceHub)
val creditRatingValidityDuration = ConfigurationUtils.getCreditRatingValidityDuration(serviceHub)

val verifyCreditRatingCommand = Command(
    VerifyCreditRating(
        creditRatingInfo = creditRatingInfo,
        creditRatingThreshold = creditRatingThreshold,
        oracleKey = oracle.owningKey,
        dateStart = Instant.now(),
        validityPeriod = creditRatingValidityDuration),
    listOf(ourIdentity.owningKey, oracle.owningKey))
```

The command is added to the transaction and the transaction is filtered to tear-off transaction details unrelated to the Oracle. In this case, only details related to the `VerifyCreditRating` command are kept.

```kotlin
val mtx = partStx.buildFilteredTransaction(
    Predicate {
        it is Command<*> && it.value is VerifyCreditRating && oracle.owningKey in it.signers
    })
```

The above creates a filtered transaction containing only a `VerifyCreditRating` command where the Oracle is a signer. The Oracle can now be requested to sign the transaction.

```kotlin
val txtSignature = subFlow(OracleSignCreditRatingRequestFlow(txBuilder, oracle, mtx))
val oracleSignedTxt = partStx.withAdditionalSignature(txtSignature)

val tx =  subFlow(FinalityFlow(oracleSignedTxt, emptyList()))
```

And the contract can check that the Oracle has signed:

```kotlin
val commandCreditRating = tx.commandsOfType<Commands.VerifyCreditRating>().single()

commandCreditRating.signers.contains(commandCreditRating.value.oracleKey)
```

## Flows for loans

Use the flows in this section to perform loan-related tasks. You can:

* Issue a new loan to a customer [(`IssueLoanFlow`)](#issueloanflow).
* Get a customer's credit rating [(`GetCustomerCreditRatingFlow`)](#getcustomercreditratingflow).

### `IssueLoanFlow`

Use `IssueLoanFlow` to issue a new loan to a customer with the repayment account referenced by `accountId`. The loan amount is deposited into the repayment account given by `accountId`, and a new loan account is created. A recurring payment is created from the repayment account to the loan account, and the repayment amount is calculated so that the loan amount is repaid over the loan term `periodInMonths`. The repayment account must be a current account.

`IssueLoanFlow(accountId: UUID, loan: Amount<Currency>, periodInMonths: Long): SignedTransaction`

* `accountId: UUID` - Customer account ID.
* `loan: amount`: Loan amount.
* `periodInMonths: Long`: Loan term in months.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when a new loan is issued to a customer.

### `GetCustomerCreditRatingFlow`

`GetCustomerCreditRatingFlow` queries the credit rating of customer with ID `customerId` from the credit rating REST web server and returns a `CreditRatingInfo` object.

`GetCustomerCreditRatingFlow(customerId: UUID): CreditRatingInfo`

* `customerId: UUID` - ID of a customer.

### Examples

#### Create a new customer account

```kotlin
val supportingDocumentationPath = File("/path/to/supportDocumentation.zip")

val attachment = serviceHub.attachments.importAttachment(
        supportingDocumentationPath.inputStream(),
        ourIdentity.toString(),
        supportingDocumentationPath.name)

val attachments = listOf(Pair(attachment, "Supporting documentation"))

val customerId = subFlow(
    CreateCustomerFlow(
        customerName = "AN Other",
        contactNumber = "5551234",
        emailAddress = "another@r3.com",
        postCode = "ZIP 1234",
        attachments = attachments))
```

#### Create a new current account and set the status to active

```kotlin
val signedTx = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = Currency.getInstance("EUR"),
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val account = signedTx.tx.outputsOfType<CurrentAccountState>().single()
subFlow(SetAccountStatusFlow(account.accountId, AccountStatus.ACTIVE))
```

#### Issue a loan for 1000 euro with account as the receiving/repayment account and a repayment period of 24 months

```kotlin
val amount = Amount(100000, Currency.getInstance("EUR")) // 1000 euro
subFlow(IssueLoanFlow(accountId, amount, 24))
```

{{< note >}}
`amount` values are in the base unit of the selected currency. In the example above, the currency is set to euros so the base unit is cents. This is why an `amount` of `100000` in this flow issues a loan for 1000 euros.
{{< /note >}}

## Account deposits and withdrawals

Account deposits and withdrawals are handled by the flows described below, which are unique to the Bank in a Box CorDapp.

### Business logic

The business logic behind Bank in a Box withdrawals and deposits is explained below, addressing how withdrawals and deposits are implemented in the application.

#### Withdrawal

After an account is fetched from the ledger, a flow calls the withdraw function on a `CreditAccount` object:

```kotlin
fun withdraw(amount: Amount<Currency>): CreditAccount
```

Implementation of the `withdraw` function is specific for each account type. For a savings account, the operation is allowed only when the account is ACTIVE, has sufficient funds, and is not within the savings period:

```kotlin
override fun withdraw(amount: Amount<Currency>): SavingsAccountState {
    verifyHasSufficientFunds(amount)
    verifyIsActive()
    verifyWithdrawalAllowed()
    return copy(accountData = accountData.copy(balance = accountData.balance - amount))
}
```

For current accounts, the operation is allowed only when the account is `ACTIVE` and has sufficient funds. The application supports an overdraft facility, and the `approvedOverdraftLimit` and `overdraftBalance` fields are considered when verifying that sufficient funds are available.

```kotlin
override fun withdraw(amount: Amount<Currency>): CurrentAccountState {
    verifyHasSufficientFunds(amount)
    verifyIsActive()

    return if(accountData.balance >= amount) {
        val updatedAccountData = accountData.copy(
                balance = accountData.balance - amount,
                txDate = Instant.now())
        copy(accountData = updatedAccountData)
    } else {
        val updatedOverdraftBalance = (overdraftBalance ?: 0L) + amount.quantity - accountData.balance.quantity
        val updatedAccountData = accountData.copy(
                balance = 0 of accountData.balance.token,
                txDate = Instant.now())
        copy(overdraftBalance = updatedOverdraftBalance, accountData = updatedAccountData)
    }
}
```

If the `withdraw` function for a specific account type passes all the verification methods and returns the account object with the amount deducted from the account's balance, the flow then verifies that the daily withdrawal limit is not exceeded. This verification is the same for all account types, and it is implemented as an extension function on the `AbstractAccountState` object. It uses the `transaction_log` table to get the sum of all withdrawals for the account for a day and compares it with `withdrawalDailyLimit` if a limit has been set for the account in question. Once the Corda transaction is signed, an appropriate entry is saved to the `transaction_log` table.


#### Deposit

After an account is fetched from the ledger, this flow calls the deposit function on the `Account` object:

```kotlin
fun deposit(amount: Amount<Currency>): Account
```

The deposit function is implemented in a similar way for the savings and loan account types, however the savings account type credits the amount to a credit balance (and should be summed) while the loan account type credits the amount to a debit balance (and should be subtracted). The following example shows the implementation of the `deposit` function for the savings account:

```kotlin
override fun deposit(amount: Amount<Currency>): SavingsAccountState {
    verifyIsActive()
    return CurrentAccountState(accountData.copy(balance = accountData.balance + amount, txDate = Instant.now()),
        withdrawalDailyLimit, transferDailyLimit, linearId)
}
```
The `deposit` function for the loan account also needs to check the balance on the account to ensure that the balance does not go into credit. The implementation is as follows:

```kotlin
override fun deposit(amount: Amount<Currency>): LoanAccountState {
    verifyHasSufficientFunds(amount)
    verifyIsActive()
    return copy(accountData = accountData.copy(balance = accountData.balance - amount))
}
```

As mentioned previously, the current account supports an overdraft balance and this should be credited prior to crediting any balance on the main account. There are three scenarios to consider:

 - The account is not overdrawn and the main balance is credited.
 - The overdraft balance is less than the deposit amount and the main balance is credited with the difference.
 - The overdraft balance is credited with the deposit amount.

This is implemented as follows:

```kotlin
override fun deposit(amount: Amount<Currency>): CurrentAccountState {
    verifyIsActive()

    return when {
        (overdraftBalance ?: 0L == 0L) -> {
            val updatedAccountData = accountData.copy(
                    balance = accountData.balance + amount,
                    txDate = Instant.now())
            copy(accountData = updatedAccountData)
        }
        ((overdraftBalance ?: 0L) < amount.quantity) -> {
            val updatedAccountData = accountData.copy(
                    balance = Amount((amount.quantity - (overdraftBalance ?: 0)), amount.token),
                    txDate = Instant.now())
            copy(overdraftBalance = 0L, accountData = updatedAccountData)
        }
        else -> {
            val updatedAccountData = accountData.copy(txDate = Instant.now())
            copy(overdraftBalance = (overdraftBalance ?: 0L) - amount.quantity, accountData = updatedAccountData)
        }
    }
}
```

Once the Corda transaction is signed, an appropriate entry is saved to the `transaction_log` table.

## Flows for account deposits and withdrawals

Use the flows in this section to perform tasks related to account deposits and withdrawals. You can:

* Withdraw money from an account [(`WithdrawFiatFlow`)](#withdrawfiatflow).
* Deposit money into an account [(`DepositFiatFlow`)](#depositfiatflow).


### `WithdrawFiatFlow`

Use `WithdrawFiatFlow` to withdraw a specified amount from an account with the provided `accountId`.

`WithdrawFiatFlow(val accountId: UUID, val amount: Amount<Currency>) : FlowLogic<SignedTransaction>()``

* `accountId`: `UUID` - The ID of an account.
* `amount`: amount to be withdrawn

This operation will fail if any of the following conditions is true:

* The provided `accountId` is a reference to a loan account or savings account in savings period.
* The specified account doesn't have sufficient funds on accounts balance.
* The specified account has reached daily withdrawal limit.
* The specified account is not in `ACTIVE` status.

In all other cases, the operation will be successful and the specified amount will be deducted from the account's balance. An entry will be recorded in the `transaction_log` table.


### `DepositFiatFlow`

Using `DepositFiatFlow`, you can deposit a specified amount to an account with the provided `accountId`.

`DepositFiatFlow(val accountId: UUID, val amount: Amount<Currency>) : FlowLogic<SignedTransaction>()`

* `accountId`: `UUID` - The ID of an account.
* `amount`: amount to be deposited

This operation will fail if the specified account is not in `ACTIVE` status. In all other cases, the operation will be successful and the specified amount will be added to the account's balance. An entry will be recorded in the `transaction_log` table.


### Examples

For account creation examples, see [account creation examples](#examples).

#### Execute withdrawal from an account

```kotlin
val amount = Amount(3000, Currency.getInstance("EUR")) // 30 euro
val signedTx = subFlow(WithdrawFiatFlow(accountId, amount))
```

#### Execute deposit to an account

```kotlin
val amount = Amount(3000, Currency.getInstance("EUR")) // 30 euro
val signedTx = subFlow(DepositFiatFlow(accountId, amount))
```

{{< note >}}
`amount` values are in the base unit of the selected currency. In the examples above, the currency is set to euros so the base unit is cents.
{{< /note >}}

## Payments

As noted in the [Loans](#loans) section, [Corda scheduled states](../../corda-os/4.7/event-scheduling.md#implementing-scheduled-events) are utilised in Bank in a Box to create recurring payments that start on a given date and are executed in a specific time period.

Payments in Bank in a Box are also a good example of how CorDapps can be integrated with external systems.

### Business logic

The business logic behind Bank in a Box payments is explained below, addressing:

- [Deduplicating payment logs](#deduplicating-payment-logs) - how double spending is prevented when off-ledger systems are involved.
- [Checking if a recurring payment can be cancelled using reference states](#checking-if-a-recurring-payment-can-be-cancelled-using-reference-states) - how recurring payments may or may not be cancelled, depending on how the recurring payment was set up.

#### Deduplicating payment logs

In Corda, notaries prevent the double spending of contract states but this naturally excludes off-ledger systems. Instead, Corda provides a [`FlowExternalOperation`](../../corda-os/4.7/api-flows.md#flowexternalasyncoperation) that is executed with a `deduplicationId`, allowing for custom handling of duplicate runs. Each recurring payment execution is logged and duplicate logs can be avoided by creating the payment log instance within a subclass of `FlowExternalOperation`.

The skeleton `CreateRecurringPaymentLogOperation` is as follows:

```kotlin
class CreateRecurringPaymentLogOperation(
    private val recurringPaymentStateAndRef: StateAndRef<RecurringPaymentState>,
    private val recurringPaymentLogRepository: RecurringPaymentLogRepository,
    private val exception: Exception? = null): FlowExternalOperation<RecurringPaymentLogSchemaV1.RecurringPaymentLog> {

}
```

Subclasses of the `FlowExternalOperation` must override the execute method, which receives the `deduplicationId` parameter. Payment logs are stored with the `deduplicationId` (in the `logId` column) and a new payment log is only created if the `deduplicationId` does not exist in the `RecurringPaymentLog` schema.

```kotlin
override fun execute(deduplicationId: String): RecurringPaymentLogSchemaV1.RecurringPaymentLog {
    var recurringPaymentLog: RecurringPaymentLogSchemaV1.RecurringPaymentLog? = null

    try {
        recurringPaymentLog = recurringPaymentLogRepository.getRecurringPaymentLogById(deduplicationId)
    } catch (e: IllegalArgumentException) {
        contextLogger().info("Recurring payment logs not found for deduplicationId: $deduplicationId, new entry will be added.")
    }
    return recurringPaymentLog?: createRecurringPaymentLog(deduplicationId)
}
```

#### Checking if a recurring payment can be cancelled using reference states

Recurring payments created by the customer should be cancellable by the customer. This excludes loan repayments and savings plan payments, which are created and owned by the bank. Checking if a customer owns and can cancel a recurring payment could be accomplished with authentication. However another solution is needed in the current scope: add the destination account as a reference state to the transaction that cancels the recurring payment, and check if the account type is a `LoanAccountState` or a `SavingsAccountState`.

1. Add the destination account to the transaction as a reference state.

```kotlin
val accountTo = accountRepository.getAccountStateById(recurringPayment.state.data.accountTo)

val txBuilder = TransactionBuilder(notary)
        .addInputState(recurringPayment)
        .addCommand(command)
        .addReferenceState(ReferencedStateAndRef(accountTo))
        .setTimeWindow(TimeWindow.fromOnly(Instant.now()))
```

2. This state can now be referenced in the contract.

`val referencedToAccount = tx.referenceInputRefsOfType<AbstractAccountState>().single().state.data`

3. Check that the destination account is not a loan account.

```kotlin
requireThat {
    "Recurring payment cannot be cancelled for loan repayments" using (referencedToAccount !is LoanAccountState)
}
```

4. Check that the destination account is not a savings account that is still part of a savings plan.

```kotlin
requireThat {
    if (referencedToAccount is SavingsAccountState) {
        "Recurring payment cannot be cancelled for saving repayments during savings period" using
                (referencedToAccount.savingsEndDate.isBefore(tx.timeWindow!!.fromTime!!))
    }
}
```

## Flows for payments

Use the flows in this section to perform tasks related to payments. You can:

* Transfer funds from one account to another [(`IntrabankPaymentFlow`)](#intrabankpaymentflow).
* Create a recurring payment [(`CreateRecurringPaymentFlow`)](#createrecurringpaymentflow).
* Cancel a recurring payment [(`CancelRecurringPaymentFlow`)](#cancelrecurringpaymentflow).
* Schedule a recurring payment [(`ExecuteRecurringPaymentFlow`)](#executerecurringpaymentflow).


### `IntrabankPaymentFlow`

Use `IntrabankPaymentFlow` to transfer a specified `amount` of money from a credit account to another account.

`IntrabankPaymentFlow(accountFrom: UUID, accountTo: UUID, amount: Amount<Currency>): SignedTransaction`

* `accountFrom`: The account the transfer originates from, identified by its `accountId` (`UUID`).
* `accountTo`: The account the transfer is directed to, identified by its `accountId` (`UUID`).
* `amount`: Amount specified to transfer.

This flow verifies that both accounts exist on the ledger, that `accountFrom` is a credit account, and that it has sufficient funds for the transfer to take place. If the `accountFrom` account has a transfer limit in place, this check is also done prior to the signing of the transaction.

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when money is transferred from one account to the other.


### `CreateRecurringPaymentFlow`

Use `CreateRecurringPaymentFlow` to create a recurring payment for the specified `amount` of money to be transferred from a credit account to another account.

`CreateRecurringPaymentFlow(accountFrom: UUID, accountTo: UUID, amount: Amount<Currency>, dateStart: Instant, period: Duration, iterationNum: Int?): SignedTransaction`

* `accountFrom`: The account the transfer originates from, identified by its `accountId` (`UUID`).
* `accountTo`: The account the transfer is directed to, identified by its `accountId` (`UUID`).
* `amount`: Amount specified to transfer.
* `dateStart: Instant`: The date payments begins.
* `period: Duration`: The duration of the recurring payment.
* `iterationNum: Int?`: Number of iterations, or recurring payments, that should occur.

`SignedTransaction` is returned when a flow has successfully updated the ledger. In this case when the recurring payment has been created.


### `CancelRecurringPaymentFlow`

`CancelRecurringPaymentFlow` cancels a recurring payment with the ID `recurringPaymentId` by consuming the `RecurringPaymentState` schedulable state.

`CancelRecurringPaymentFlow(recurringPaymentId: UniqueIdentifier): SignedTransaction`

* `recurringPaymentId: UniqueIdentifier`


### `ExecuteRecurringPaymentFlow`

You can schedule `ExecuteRecurringPaymentFlow` to execute a recurring payment occurrence. The flow is initiated by the `StateRef` of the `RecurringPaymentState` schedulable state, and is executed using the `IntrabankPaymentFlow`. The result is logged to the `RecurringPaymentLogSchema`.

`ExecuteRecurringPaymentFlow(recurringPaymentStateRef): SignedTransaction`

`SignedTransaction` is returned when a flow has successfully updated the ledger, in this case when the recurring payment has been scheduled.


### Examples

#### Create a new customer account

```kotlin
val supportingDocumentationPath = File("/path/to/supportDocumentation.zip")

val attachment = serviceHub.attachments.importAttachment(
        supportingDocumentationPath.inputStream(),
        ourIdentity.toString(),
        supportingDocumentationPath.name)

val attachments = listOf(Pair(attachment, "Supporting documentation"))

val customerId = subFlow(
    CreateCustomerFlow(
        customerName = "AN Other",
        contactNumber = "5551234",
        emailAddress = "another@r3.com",
        postCode = "ZIP 1234",
        attachments = attachments))
```

#### Create two new current accounts and set their status to active

```kotlin
val signedTxFromAccount = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = Currency.getInstance("EUR"),
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val signedTxToAccount = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = Currency.getInstance("EUR"),
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val accountFrom = signedTxFromAccount.tx.outputsOfType<CurrentAccountState>().single()
val accountTo = signedTxToAccount.tx.outputsOfType<CurrentAccountState>().single()

subFlow(SetAccountStatusFlow(accountFrom.accountId, AccountStatus.ACTIVE))
subFlow(SetAccountStatusFlow(accountTo.accountId, AccountStatus.ACTIVE))
```


#### Deposit funds into the from account

```kotlin
val amount = Amount(100000, Currency.getInstance("EUR")) // 1000 euro
subFlow(DepositFiatFlow(accountFrom, amount))
```

#### Execute a one-off payment of 100 euro from `accountFrom` to `accountTo`

```kotlin
val amount = Amount(10000, Currency.getInstance("EUR")) // 100 euro
subFlow(IntrabankPaymentFlow(accountFrom, accountTo, amount))
```

#### Create a recurring payment of 100 euro every 10 seconds, starting now, for 5 repayments

```kotlin
val amount = Amount(10000, Currency.getInstance("EUR")) // 100 euro
subFlow(CreateRecurringPaymentFlow(accountFrom, accountTo, amount, Instant.now(), Duration.ofSeconds(10), 5))
```

#### Create a recurring payment of 10 euro every day, starting now, with no expiry

```kotlin
val signedTx = subFlow(CreateRecurringPaymentFlow(accountFromId, accountToId, 10 of EUR, Instant.now(), Duration.ofDays(1)))
```

#### Cancel the recurring payment

```kotlin
val amount = Amount(1000, Currency.getInstance("EUR")) // 10 euro
val signedTx = subFlow(CreateRecurringPaymentFlow(accountFrom, accountTo, amount, Instant.now(), Duration.ofDays(1)))
```

{{< note >}}
`amount` values are in the base unit of the selected currency. In the examples above, the currency is set to euros so the base unit is cents.
{{< /note >}}


## Reports and views

Reports and views are used in Bank in a Box to display individual account and customer information when queried as well as lists of accounts, customers, transactions, and recurring payments.

The flows in this section are an integral part of the user interface design as they create paginated responses that are returned for searches that users can perform via the user interface.


### Business logic

The business logic behind Bank in a Box reports and views is explained below, addressing how mapped schemas are implemented and used to display information in Bank in a Box.

#### Creating a mapped schema

A contract state implementing the `QueryableState` interface indicates that a custom table should be created for it in the node's database and made accessible using SQL. The following shows an example of the `RecurringPaymentState` class with several unrelated properties and methods removed for clarity:

```kotlin
@BelongsToContract(RecurringPaymentContract::class)
data class RecurringPaymentState(
    val accountFrom: UUID,
    val accountTo: UUID,
    val amount: Amount<Currency>,
    val dateStart: Instant,
    val period: Duration,
    val iterationNum: Int?,
    val owningParty: AbstractParty,
    override val linearId: UniqueIdentifier = UniqueIdentifier()
) : QueryableState {

    override fun generateMappedObject(schema: MappedSchema): PersistentState {
        return when (schema) {
            is RecurringPaymentSchemaV1 -> RecurringPaymentSchemaV1.RecurringPayment(
                    this.accountFrom,
                    this.accountTo,
                    this.amount.quantity,
                    this.dateStart,
                    this.period,
                    this.iterationNum,
                    this.linearId.id)
            else -> throw IllegalArgumentException("Unrecognised schema $schema")
        }
    }

    override fun supportedSchemas(): Iterable<MappedSchema> = listOf(RecurringPaymentSchemaV1)
}
```

The `QueryableState` interface requires the `generateMappedObject` and `supportedSchemas` methods to be implemented. The `supportedSchemas` method returns a list of relational schemas supported by the state and the `generateMappedObject` method returns a generated instance of a schema from the current state's context.

A concise representation of the associated `RecurringPaymentSchemaV1` class is shown below:

```kotlin
object RecurringPaymentSchemaV1 : MappedSchema(
    schemaFamily = RecurringPaymentSchema.javaClass,
    version = 1,
    mappedTypes = listOf(RecurringPayment::class.java)) {

    @Entity
    @Table(name = "recurring_payment")
    class RecurringPayment(

        @Column(name="account_from")
        @Type(type = "uuid-char")
        var accountFrom: UUID,

        @Column(name="account_to")
        @Type(type = "uuid-char")
        var accountTo: UUID,

        @Column(name="amount")
        var amount: Long,

        @Column(name="date_start")
        var dateStart: Instant,

        @Column(name="period")
        var period: Duration,

        @Column(name="iteration_num", nullable = true)
        var iterationNum: Int?,

        @Column(name="linear_id")
        @Type(type = "uuid-char")
        var linearId: UUID

) : PersistentState()
```

The `RecurringPaymentSchemaV1` class defines a single entity to represent a recurring payment database table. It uses JPA annotations to define the table name, column names, and types. The schema contains properties to store the relevant properties of the state, including `accountFrom`, `accountTo`, `amount`, `dateStart`, `period`, `iterationNum`, and `linearId`.

An off-ledger schema can be defined in a similar manner to the above `MappedSchema` class but will obviously not have an associating contract state.

#### Querying transactions

The Corda Node provides services to query and persist mapped schemas. The following is an example query for the transaction log schema:

```kotlin
fun getTransactionLogByTransactionType(accountId: UUID, txType: TransactionType)
    : List<TransactionLogSchemaV1.TransactionLog> {

    return serviceHub.withEntityManager {
        val query = createQuery(
            "SELECT tl FROM TransactionLogSchemaV1\$TransactionLog tl " +
            "WHERE (tl.accountFrom = :accountId OR tl.accountTo = :accountId) " +
            "AND tl.txType = :txType ",
            TransactionLogSchemaV1.TransactionLog::class.java
        )
        query.setParameter("accountId", accountId)
        query.setParameter("txType", txType)
        query.resultList
    }
}
```

The above queries all transactions for account with ID `accountId` and of type `transactionType` (deposit, withdrawal, transfer). The `withEntityManager` method of the Corda Node services (`serviceHub`) provides access to the JPA API. An HQL query is constructed, selecting all fields from the transaction log schema, where the "from" or "to" account is equal to the given account parameter, and the transaction type is equal to the given transaction type parameter.


## Flows for reports and views

Use the flows in this section to perform tasks related to reports and views. These flows are all tied to the Bank in a Box front end. You can:

* See a list of accounts for a customer [(`GetBalancesFlow)`](#getbalancesflow).
* See a list of transactions for a customer [(`GetCustomerTransactionsFlow`)](#getcustomertransactionsflow).
* See a list of recurring payments for a customer [(`GetRecurringPaymentsFlow`)](#getrecurringpaymentsflow).
* See the status of an account [(`GetAccountFlow`)](#getaccountflow).
* See a list of accounts and associated customers [(`GetAccountsPaginatedFlow`)](#getaccountspaginatedflow).
* See a customer's information when searching by their customer ID [(`GetCustomerByIdFlow`)](#getcustomerbyidflow).
* See a list of all customers [(`GetCustomersPaginatedFlow`)](#getcustomerspaginatedflow).
* See the state of a recurring payment [(`GetRecurringPaymentsByIdFlow`)](#getrecurringpaymentsbyidflow).
* See a list of recurring payments for an account [(`GetRecurringPaymentsForAccountPaginatedFlow`)](#getrecurringpaymentsforaccountpaginatedflow).
* See a list of recurring payments for a customer [(`GetRecurringPaymentsForCustomerPaginatedFlow`)](#getrecurringpaymentsforcustomerpaginatedflow).
* See a list of recurring payments [(`GetRecurringPaymentsPaginatedFlow`)](#getrecurringpaymentspaginatedflow).
* See a list of transactions for an account [(`GetTransactionsForCustomerPaginatedFlow`)](#gettransactionsforcustomerpaginatedflow).
* See a list of transactions for a customer in a specified time frame [(`GetTransactionsPaginatedFlow`)](#gettransactionspaginatedflow).


### `GetBalancesFlow`

Use `GetBalancesFlow` to return a list of accounts for a customer with `customerId`.

`GetBalancesFlow(customerId: UUID): List<AbstractAccountState>`

* `customerId`: `UUID` - The ID of the customer's profile.


### `GetCustomerTransactionsFlow`

Use `GetCustomerTransactionsFlow` to return a list of transactions for a customer with `customerId`.

`GetCustomerTransactionsFlow(customerId: UUID, dateStart: Instant, dateEnd: Instant): List<TransactionLogSchemaV1.TransactionLog>`

* `customerId`: `UUID` - The ID of the customer's profile.
* `dateStart` / `dateEnd`: The date range for which the flow returns transactions.


### `GetRecurringPaymentsFlow`

Use `GetRecurringPaymentsFlow` to return a list of recurring payments for a customer with `customerId`.

`GetRecurringPaymentsFlow(customerId: UUID): List<RecurringPaymentState>`

* `customerId`: `UUID` - The ID of the customer's profile.


### `GetAccountFlow`

Use `GetAccountFlow` to retrieve the 'AbstractAccountState' for a given `accountId`. This shows you if the account is `PENDING`, `ACTIVE`, or `SUSPENDED`.

* `customerId`: ID of the account.

An exception is thrown if the account cannot be found.


### `GetAccountsPaginatedFlow`

Use `GetAccountsPaginatedFlow`, a Public API flow, to retrieve accounts and associated customers in a paginated list for given `repositoryQueryParams` and (optionally) `dateFrom` and `dateTo`.

* `repositoryQueryParams`: This object holds `searchTerm`, pagination, and sorting data.
* `dateFrom` (optional): Filters accounts with `txDate` after a given date.
* `dateTo` (optional): Filters accounts with `txDate` before a given date.

`RepositoryQueryParams.searchTerm` can be matched in LIKE fashion against multiple fields. The result set can be sorted based on `RepositoryQueryParams.sortField` and `RepositoryQueryParams.sortOrder` values against all fields in `AbstractAccountState` and `CustomerSchemaV1.Customer`.


### `GetCustomerByIdFlow`

Use the `GetCustomerByIdFlow` to retrieve the `CustomerSchemaV1.Customer`, which stores personal details and contact information along with creation and modification timestamps, for a given `customerId`.

* `customerId`: ID of the customer.

An exception is thrown if the customer cannot be found.


### `GetCustomersPaginatedFlow`

Use the `GetCustomersPaginatedFlow` to return a paginated list of all customers matching the given criteria.

* `repositoryQueryParams`: This objects holds a repository query's possible parameters along with sort and pagination information.


### `GetRecurringPaymentsByIdFlow`

Use `GetRecurringPaymentsByIdFlow`, a public API flow, to retrieve the `RecurringPaymentState` for a given `LinearId`.

The `RecurringPaymentState` stores the following information.

* Transfer information:
  * `accountFrom`
  * `accountTo`
  * `amount`
* Scheduling information:
  * `dateStart`
  * `period`
  * `iterationNum`


### `GetRecurringPaymentsForAccountPaginatedFlow`

Use the `GetRecurringPaymentsForAccountPaginatedFlow`, a public API flow, to retrieve recurring payments in a paginated list for a specific account with `accountId`.

* `repositoryQueryParams`: This object holds `searchTerm`, pagination, and sorting data.
* `accountId`: The ID of the account that will be matched against the `accountFrom` and `accountTo` fields of the `RecurringPaymentSchemaV1.RecurringPayment`.
* `dateFrom` (optional): Filters accounts with `txDate` after a given date.
* `dateTo` (optional): Filters accounts with `txDate` before a given date.

The `RepositoryQueryParams.searchTerm` can be matched in LIKE fashion against multiple fields. The result set can be sorted based on `RepositoryQueryParams.sortField` and `RepositoryQueryParams.sortOrder` values against all fields in `RecurringPaymentLogSchemaV1.RecurringPaymentLog` and `RecurringPaymentSchemaV1.RecurringPayment`.


### `GetRecurringPaymentsForCustomerPaginatedFlow`

Use `GetRecurringPaymentsForCustomerPaginatedFlow`, a public API flow, to retrieve recurring payments in a paginated list for a specific customer with `customerId`.

* `repositoryQueryParams`: This object holds the `searchTerm`, pagination, and sorting data.
* `customerId`: The ID of the customer which will be matched against the `accountFrom` and `accountTo` owner fields of the `RecurringPaymentSchemaV1.RecurringPayment`.
* `dateFrom` (optional): Filters accounts with `txDate` after a given date.
* `dateTo` (optional): Filters accounts with `txDate` before a given date.


### `GetRecurringPaymentsPaginatedFlow`

Use `GetRecurringPaymentsPaginatedFlow`, a public API flow, to retrieve recurring payments in a paginated list.

* `repositoryQueryParams`: This object holds `searchTerm`, pagination, and sorting data.
* `dateFrom` (optional): Filters accounts with `txDate` after a given date.
* `dateTo` (optional): Filters accounts with `txDate` before a given date.


### `GetTransactionsForCustomerPaginatedFlow`

Use `GetTransactionsForCustomerPaginatedFlow`, a public API flow, to retrieve transactions in a paginated list for a specific account with `accountId`.

* `repositoryQueryParams`: This object holds `searchTerm`, pagination, and sorting data.
* `accountId`: The ID of the account that will be matched against the `accountFrom` and `accountTo` fields of the `RecurringPaymentSchemaV1.RecurringPayment`.
* `dateFrom` (optional): Filters accounts with `txDate` after a given date.
* `dateTo` (optional): Filters accounts with `txDate` before a given date.


### `GetTransactionsPaginatedFlow`

Use `GetTransactionsPaginatedFlow` to retrieve all transactions for a given `customerId` in a specified time frame.

* `queryParams`: Pagination parameters.
* `customerId`: The ID of the customer.
* `dateFrom`: Filters accounts with `txDate` after a given date.
* `dateTo`: Filters accounts with `txDate` before a given date.


### `GetCustomerNameByAccountFlow`

Use `GetCustomerNameByAccountFlow` to return the associated customer name for a specified `accountId`.

* `accountId`


### `GetAccountsForCustomerPaginatedFlow`

Use `GetAccountsForCustomerPaginatedFlow` to return a list of accounts for a specified `customerId`.

* `queryParams`: Pagination parameters.
* `customerId`: The ID of a customer.


### `GetRecurringPaymentByIdFlow`

Use `GetRecurringPaymentByIdFlow` to return the information on a recurring payment, specified by its `linearId`.

* `linearId: UUID`


### `GetTransactionByIdFlow`

Use `GetTransactionByIdFlow` to return the information of a transaction, specified by its `txId` (transaction ID).


### `GetTransactionsForAccountPaginatedFlow`

Use `GetTransactionsForAccountPaginatedFlow` to return a list of transactions for an account, specified by the `accountId`.

* `queryParams`: Pagination parameters.
* `accountId`: The ID of a customer.


### Examples

#### Create a new customer account

```kotlin
val supportingDocumentationPath = File("/path/to/supportDocumentation.zip")

val attachment = serviceHub.attachments.importAttachment(
        supportingDocumentationPath.inputStream(),
        ourIdentity.toString(),
        supportingDocumentationPath.name)

val attachments = listOf(Pair(attachment, "Supporting documentation"))

val customerId = subFlow(
    CreateCustomerFlow(
        customerName = "AN Other",
        contactNumber = "5551234",
        emailAddress = "another@r3.com",
        postCode = "ZIP 1234",
        attachments = attachments))
```

#### Create two new current accounts and set their status to active

```kotlin
val signedTxFromAccount = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = Currency.getInstance("EUR"),
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val signedTxToAccount = subFlow(
    CreateCurrentAccount(
        customerId = customerId,
        tokenType = EUR,
        withdrawalDailyLimit = 500,
        transferDailyLimit = 1000))

val accountFrom = signedTxFromAccount.tx.outputsOfType<CurrentAccountState>().single()
val accountTo = signedTxToAccount.tx.outputsOfType<CurrentAccountState>().single()

subFlow(SetAccountStatusFlow(accountFrom.accountId, AccountStatus.ACTIVE))
subFlow(SetAccountStatusFlow(accountTo.accountId, AccountStatus.ACTIVE))
```


#### Create some transactions

```kotlin
val amountOneThousandOfEuro = Amount(100000, Currency.getInstance("EUR"))
val amountOneHundredOfEuro = Amount(10000, Currency.getInstance("EUR"))
subFlow(DepositFiatFlow(accountFrom, amountOneThousandOfEuro))
subFlow(IntrabankPaymentFlow(accountFrom, accountTo, amountOneHundredOfEuro))
```

#### Query the balance on the accounts

```kotlin
val accountFromBalance = subFlow(GetBalancesFlow(accountFrom.accountData.customerId).single())
val accountToBalance = subFlow(GetBalancesFlow(accountTo.accountData.customerId).single())
```

#### Query the transactions on the accounts

```kotlin
val transactionLogAccountFrom = subFlow(GetCustomerTransactionsFlow(accountFrom.accountData.customerId)).single()
val transactionLogAccountTo = subFlow(GetCustomerTransactionsFlow(accountTo.accountData.customerId)).single()
```

#### Create a recurring payment

```kotlin
val amount = Amount(10000, Currency.getInstance("EUR")) // 100 euro
subFlow(CreateRecurringPaymentFlow(accountFrom, accountTo, amount, Instant.now(), Duration.ofDays(30), 5))
```

#### Query the recurring payment

```kotlin
val recurringPaymentsFrom = subFlow(GetRecurringPaymentsFlow(accountFrom.accountData.customerId))
```
