---
date: '2020-01-08T09:59:25Z'
menu:
  bankinabox:
    parent: bank-in-a-box-user-interface
    identifier: bank-in-a-box-admin-ui
tags:
- Bank in a Box
- UI
title: Admin user interface
weight: 300
---

# Admin user interface

The admin user interface of Bank in a Box allows an admin user to perform the tasks of a bank employee. Read on to familiarise yourself with the elements of the user interface. To learn how to perform tasks as an admin user, see the [How to guide](how-to.md#admin-tasks).

## Log in and home screen

When you have successfully started the Bank in a Box user interface, you will be prompted to log in with username and password.

The default Admin user name and password are as follows:

* User name: admin
* Password: password1!

After entering your username and password, you will arrive at the home screen. From the left sidebar navigation, you can access different screens depending on your role (Admin or Customer).

The descriptions below apply to the Admin user interface. See the [Customer user interface guide](customer-ui-guide.md) for information on that user interface.

## Navigation

When you open the navigation menu, you will see the following:

* **User Management**.
* **Customers**.
* **Accounts**.
* **Transactions**.
* **Recurring payments**.

## User management

When you click on **User management** in the navigation menu, you will be taken to the **User management** screen. Here you can [assign and revoke user permissions](how-to.md#assign-or-revoke-a-user-role).

## Customers screen

On the **Customers** screen you can view a list of existing customers with their associated email address and contact number displayed in a table.

To sort the table by a specific header (**Customer name**, **Email address**, or **Contact number**) click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

To find a specific customer, use the search bar. After typing three characters, the search will start. As you type more the search will update.

{{< note >}}
The search is case-sensitive.
{{< /note >}}

When you click on a customer name, you will be directed to the **Update Customer** screen where you can [view and update a customer profile](how-to.md#update-customer-profile).

You may also wish to [create a new customer](how-to.md#create-a-customer-profile). Click on the **Create New** button in the top right corner to be directed to the **Create Customer** screen.

## Accounts screen

On the Accounts screen you can view a complete list of existing accounts, with customer name, account type, balance, account status, and last transfer date displayed in a table.

To sort the table by a specific header, click on that header.

To find a specific account, use the search bar. After typing three characters, the search will start. As you type more the search will update.

Click on an account to go to the [Account screen](#account-page) and see all information related to a specific account.

### Account screen

Here you will find all relevant information for a specific account. You can view this information in four tabs: **Account**, **Customer**, **Transactions**, and **Recurring Payments**.

#### Account tab

The following elements are shown under the Account tab:

* **Account Key** - the ID of the account.
* **Currency** - the currency of the account.
* **Balance** - the amount of money in the account.
* **Type** - this tells you if it is a current, savings, loan or overdraft account.
* **Status** - this indicates the status of the account: pending, active, or suspended.
* **Last TX date** - the date of the last transaction on the account.
* **Withdrawal daily limit** - the maximum amount that can be withdrawn from the account daily.
* **Transfer daily limit** - maximum amount that can be transferred from the account daily.
* **Overdraft limit** - the overdraft limit that has been approved for the account.
* **Overdraft balance** - the amount of money currently remaining in overdraft.

You can also perform a series of actions on the Account screen, as described in the [How to guide](how-to.md).

#### Account states

As mentioned above, an account can be in three states:

* **Pending** An account is in this state when it is first created. Once the customer's supporting documentation has been reviewed and approved, the bank will change the state to active and the customer will be able to use your account.
* **Active** When an account is active the customer can use it to perform transactions including deposits, withdrawals, payments, and recurring payments.
* **Suspended** An account may be suspended due to reported suspicious activity.

#### Customers tab

On this tab, you can view customer information that is tied to the account. This includes:

* **Customer name**.
* **Phone number**.
* **Email address**.
* **Post code**.
* **Created on** - the date the customer was created.
* **Modified on** - the last date that the customer information was modified.
* **Attachments** - supporting documentation uploaded previously.


{{< note >}}
Customer information can be viewed but not modified from this tab. For instructions on modifying customer information, see the documentation on [updating a customer profile](how-to.md#update-customer-profile).
{{< /note >}}

#### Transactions tab

Here you can view the transactions that have occurred on this account.

Set the **From date**, **To date**, and times to see transactions that have occurred in a specific time frame. By default, the **To date** is set to today's date so you will see the most recent transactions first.

A table displays relevant information for each individual transaction:

* **Transaction ID** - the ID generated for the transaction.
* **Account from** - the ID of the account that sent the money.
* **Account to** - the ID of the account that received the money.
* **Amount** - the amount of money that was sent.
* **Type** - the type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - the date that the transaction occurred.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

If you wish to see all information for a specific transaction, click the transaction and you will be directed to the Transaction view.

{{< note >}}
A deposit will not display a 'From account' and a withdrawal will not display a 'To account'.
{{< /note >}}

##### Transaction view

Here you can see all information on a specific transaction.

Under the Transaction details tab:

* **Transaction ID** - the ID generated by the transaction.
* **Amount** - the amount of money that was transferred.
* **Currency** - the currency of the transaction.
* **Type** - the type of transaction that occurred.
* **Transaction date** - the date that the transaction occurred.
* **Currency** - the currency of the transaction.

Under the Accounts tab:

* **Account from** - the ID of the account that sent the money.
* **Type** - the type of the origin account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who sent the money.
* **Account to** - the ID of the account that received the money.
* **Type** - the type of the receiving account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who received the money.

#### Recurring payments tab

The Recurring payments tab is set up in the same way as the Transactions tab. Here you can view the recurring payments that have occurred on this account.

Set the **From date**, **To date**, and times to see transactions that have occurred in a specific time frame. By default, the **To date** is set to today's date so you will see the most recent recurring payments first.

A table shows displays relevant information for each recurring payment:

* **Period** - the period of the recurring payment.
* **Account from** - the ID of the account that sent the money.
* **Account to** - the ID of the account that received the money.
* **Amount** - the amount of money that was sent.
* **Iterations left** - the number of payments remaining.
* **Next payment date** - the date that the next payment will occur.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

If you wish to see all information for a specific payment, click the payment and you will be directed to the Recurring payment view.

##### Recurring payments view

Here you can see all information on a specific recurring payment.

Under the Recurring payment tab:

* **Recurring payment ID** - the ID generated for the transaction.
* **Amount** - the amount paid with each iteration.
* **Payment error** - any errors that occurred during the transaction.
* **Payment date** - the date the payment started.
* **Iterations remaining** - the number of payments remaining.
* **Period** - the period of the recurring payment in days.

Under the Accounts tab:

* **Account from** - the ID of the account that sent the money.
* **Account type** - the type of the origin account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who sent the money.
* **Account to** - the ID of the account that received the money.
* **Account type** - the type of the receiving account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who received the money.

## Transactions screen

On the Transactions screen you can view a complete list of transactions with the following information displayed in a table for each transaction:

* **Transaction ID** - the ID generated for the transaction.
* **Account from** - the ID of the account that sent the money.
* **Account to** - the ID of the account that received the money.
* **Amount** - the amount of money that was sent.
* **Type** - the type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - the date that the transaction occurred.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

To find a specific transaction, use the search bar. After typing three characters, the search will start. As you type more the search will update.

If you wish to see all relevant information for a specific transaction, click on the transaction and you will be directed to the Transfer view.

#### Transaction view

The transaction view displays all relevant information for a selected transaction.

Under the **Transaction tab**, you can view:

* **Transaction ID** - the ID generated for the transaction.
* **Amount** - the amount of money that was sent.
* **Currency** - the currency of the transaction.
* **Type** - the type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - the date that the transaction occurred.

Under the **Accounts tab**, you can view:

* **Account from** - the ID of the account that sent the money.
* **Type** - the type of the origin account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who sent the money.
* **Account to** - the ID of the account that received the money.
* **Type** - the type of the receiving account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who received the money.


## Recurring payments screen

Here you can view a complete list of recurring payments with the following information displayed in a table for each recurring payment:

* **Period** - the period of the recurring payment in months.
* **Account from** - the ID of the account that sent the money.
* **Account to** - the ID of the account that received the money.
* **Amount** - the amount of money that was sent.
* **Iterations left** - the number of payments remaining.
* **Next payment date** - the date that the next payment will occur.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

To find a specific recurring payment, use the search bar. After typing three characters, the search will start. As you type more the search will update.

If you wish to see all relevant information for a specific recurring payment, click on the recurring payment and you will be directed to the [Recurring payments view](#recurring-payments-view).

You may also wish to [create a new recurring payment](how-to.md#create-a-recurring-payment). Click on the Create New button in the top right corner to be directed to the **Create a recurring payment** screen.


### Recurring payments view

The recurring payment view displays all relevant information for a selected transaction.

Under the recurring payment tab this includes:

* **Recurring payment ID** - the ID generated for the payment when it was created.
* **Amount** - the amount of money to be sent.
* **Currency** - the currency of the recurring payment.
* **Error** - any errors occurring on the payment, such as an insufficient funds error.
* **Transaction date** - the date that recurring payment began.
* **Period** - the period of the recurring payment.
* **Amount** - the amount of money that was sent.
* **Iterations left** - the number of payments remaining.
* **Next payment date** - the date that the next payment will occur.


Under the Accounts tab this includes:

* **Account from** - the ID of the account that sent the money.
* **Type** - the type of the origin account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who sent the money.
* **Account to** - the ID of the account that received the money.
* **Type** - the type of the receiving account (current, savings, overdraft, or loan).
* **Customer name** - the name of the customer who received the money.
