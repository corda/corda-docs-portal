---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: bank-in-a-box-user-interface
    identifier: bank-in-a-box-customer-ui
tags:
- Bank in a Box
- UI
title: Customer and guest user interface
weight: 300
---

# Customer and guest user interface

The customer user interface of Bank in a Box allows a customer user to perform all of their daily banking activities with ease. Read on to familiarise yourself with the elements of the user interface. To learn how to perform tasks as a customer user, see the [How to guide](how-to.md#customer-tasks).

## Log in and home screen

When you have successfully started the Bank in a Box user interface, you will be prompted to log in with username and password.

The descriptions below apply to the customer user interface. See the [Admin user interface guide](admin-ui-guide.md) for information on that user interface.

## Navigation

The navigation on the left-hand side allows a Customer to access the following:

* **Update My Profile**.
* **Accounts**.
* **Transactions**.
* **Intrabank payment**.
* **Recurring payments**.

{{< note >}}
The guest user interface has the same log in screen and navigation menu as the customer user role. However, a guest user will not have access to these screens until an Admin user has assigned them the role of Customer.
{{< /note >}}

## Update My Profile screen

When you access the **Update My Profile** screen, you will see your customer information displayed. Here you can [make changes to your customer profile](how-to.md#update-a-customer-profile) as necessary in the following fields:

* **Customer name** - The customer's name.
* **Contact number** - The customer's phone number.
* **Email address** - The customer's email address.

Under the **Attachments** dropdown you can view attachments uploaded to your Customer profile.

{{< note >}}
You cannot make changes to your **Post Code** or upload new **Attachments**. Contact a bank administrator to do so.
{{< /note >}}

Two additional fields are generated automatically and cannot be modified. **Created on** indicates the date and time that your customer profile was created. **Modified on** indicates the last date and time that your profile was modified.

## Accounts screen

On the **Accounts** screen you can view a complete list of the customer's existing accounts displayed in a table. This table shows the following information for each account:

* **Account ID** - The identification number of the account.
* **Customer name** - Your name or any other names tied to the account.
* **Account type** - The type of account (current, savings, or loan).
* **Currency** - The currency of the account.
* **Balance** - The amount of money in the account.
* **Account status** - The status of the account (pending, active, or suspended).
* **Last transaction date** -The date of the last transaction performed on the account.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

Use the search bar to find a specific account. After typing three characters, the search will start. As you type more the search will update.

Click on an account to go to the [Account screen](#account-page) and see all information related to a specific account.

### Account states

As mentioned above, the customer account can be in three states:

* **Pending** The account is in this state when it is first created. Once customer supporting documentation has been reviewed and approved, an Admin user will change the state to active and the account can be used.
* **Active** When the customer account is active, the customer can use it to perform transactions including deposits, withdrawals, payments, and recurring payments.
* **Suspended** The account can be suspended, which may be done by a bank when suspicious activity on the account has been reported.

### Account screen

The Account screen displays all relevant information for your selected account in four separate tabs: **Account**, **Customer**, **Transactions**, and **Recurring payments**. Read more about these tabs below.

#### Account tab

On this tab you can view the following information:

* **Account ID** - The identification number of the account.
* **Account type** - The type of account (current, savings, or loan).
* **Currency** - The currency of the account.
* **Balance** - The amount of money in the account.
* **Account status** - The status of the account (pending, active, or suspended).
* **Withdrawal daily limit** - The maximum amount that you can withdraw from the account daily.
* **Transfer daily limit** - The maximum account that you can transfer from the account daily.
* **Last transaction date** - The date of the last transaction performed on the account.
* **Overdraft limit** - The overdraft limit that has been approved for the account.
* **Overdraft balance** - The amount of money currently remaining in overdraft.

On this tab you also have the option to [set withdrawal and transfer daily limits on the customer's account](how-to.md#set-withdrawal-and-transfer-limits).


#### Customer tab

On this tab you can view customer information that is tied to the customer's account. This includes:

* **Customer name** - The customer's legal name.
* **Contact number** - The customer's phone number.
* **Email address** - The customer's email address.
* **Post code** - The post code of the customer's address.
* **Created on** - The date the customer was created.
* **Modified on** - The last date that the customer information was modified.
* **Attachments** - Supporting documentation uploaded previously.

#### Transactions tab

On this tab you can view transactions that have occurred on this customer account.

A table displays relevant information for each individual transaction:

* **Transaction ID** - The ID generated for the transaction.
* **Account from** - The ID of the account that sent the money.
* **Account to** - The ID of the account that received the money.
* **Amount** - The amount of money that was sent.
* **Type** - The type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - The date that the transaction occurred.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

{{< note >}}
A deposit will not display a **From account** and a withdrawal will not display a **To account**.
{{< /note >}}

#### Recurring payments tab

The recurring payments tab is set up in the same way as the transactions tab. Here you can view the recurring payments that have occurred on this customer account.

Set the **From date**, **To date**, and times to see transactions that have occurred in a specific time frame. By default, the **To date** is set to today's date so you will see the most recent recurring payments first.

A table displays relevant information for each recurring payment:

* **Period** - The period of the recurring payment.
* **Account from** - The ID of the account that sent the money.
* **Account to** - The ID of the account that received the money.
* **Amount** - The amount of money that was sent.
* **Iterations left** - The number of payments remaining.
* **Next payment date** - The date that the next payment will occur.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

## Transactions screen

On this screen you can view transactions that have occurred on this customer account.

A table displays relevant information for each individual transaction:

* **Transaction ID** - The ID generated for the transaction.
* **Account from** - The ID of the account that sent the money.
* **Account to** - The ID of the account that received the money.
* **Amount** - The amount of money that was sent.
* **Type** - The type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - The date that the transaction occurred.

To sort the table by a specific header, click on that header. The first time you click, the column will sort in ascending order. If you click again, it will sort in descending order.

Click on a transaction to go to the [transaction screen](#transaction-page) and see all information related to that specific transaction.

### Transaction screen

The transaction screen displays all relevant information for a selected transaction in two tabs: **Transaction** and **Accounts**. Read more about these tabs below.

#### Transaction tab

Under the **Transaction** tab, you can view:

* **Transaction ID** - The ID generated for the transaction.
* **Amount** - The amount of money that was sent.
* **Currency** - The currency of the transaction.
* **Type** - The type of transaction that occurred (transfer, deposit, or withdrawal).
* **Transaction date** - The date that the transaction occurred.

#### Accounts tab

Under the **Accounts** tab, you can view:

* **Account from** - The ID of the account that sent the money.
* **Type** - The type of the origin account (current, savings, overdraft, or loan).
* **Customer name** - The name of the customer who sent the money.
* **Account to** - The ID of the account that received the money.
* **Type** - The type of the receiving account (current, savings, overdraft, or loan).
* **Customer name** - The name of the customer who received the money.

## Intrabank payment screen

On this screen you can create a new intrabank payment. This is a transfer that can be made between a customer's accounts or to another bank client's account.

See the documentation on [creating an intrabank payment](how-to.md#create-an-intrabank-payment) to learn more.


## Recurring payments screen

On this screen you can create a new recurring payment. Recurring payments can be used for any payment that a customer makes periodically - for example, bills or loan payments.

See the documentation on [creating a recurring payment](how-to.md#create-a-recurring-payment) to learn more.
