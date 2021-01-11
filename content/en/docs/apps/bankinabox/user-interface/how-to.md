---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: bank-in-a-box-user-interface
    identifier: bank-in-a-box-how-to
tags:
- Bank in a Box
- UI
title: How to guide
weight: 300
---

# How to guide

When using the Bank in a Box application, you will be able to perform different tasks depending on your user role.

There are three user roles available in the application: Admin, Customer, and Guest.

As an Admin user, you can perform administrative tasks, managing user profiles and accounts:

* Create customer profiles.
* Create accounts.
* Change an account status.
* Assign and revoke user roles.
* Issue a loan.
* Approve an overdraft.
* Deposit money to an account.
* Register as a user on Bank in the Box.
* Update a Customer profile.
* Set withdrawal and transfer limits.

As a Customer user, you can perform all tasks related to your daily banking needs:

* Create an intrabank payment.
* Create a recurring payment.
* Register as a user on Bank in the Box.
* Update your profile.
* Set withdrawal and transfer limits.

As a Guest user, you can register as a user on Bank in a Box. However, you will not be able to perform any other tasks unless an Admin user assigns you the role of Customer.


## Admin tasks

### Create a customer profile

Follow these steps to create a new customer profile.

1. Navigate to the **Customers** screen. Click the **Create new** button in the top right corner.

2. Fill out all fields:
   * Customer name
   * Phone number
   * Email address
   * Post code

3. Attach supporting documentation (customer document) by clicking the **Add attachment** button. This attachment mimics a user identity verification and application process. These documents should be contained in a unique jar or zip file.

   {{< note >}}
   If the documentation that you upload is already attached to another customer profile, you will receive an error message. Upload a unique jar or zip file with the proper supporting documentation and try again.
   {{< /note >}}

4. Once you have entered all details, the **Save** button will be enabled. Click **Save**.

5. You are taken back to the **Customers** screen and a message will appear indicating that the customer was created successfully.

{{< note >}}
When the customer profile is created, they will not have any accounts - you will have to create them. Learn how under [Creating accounts](#create-a-current-account).
{{< /note >}}

{{< figure alt="Create customer profile" zoom="/en/gifs/create-customer-biab-1.0.gif" >}}


### Create a Current account

1. Navigate to the **Accounts** screen and click **Create New** in the top right corner of the page.

2. Select the **Account Type**: **Current Account**.

3. Search for an existing customer by name, email, customer ID, or phone number. The search will begin after you have typed three characters and will update as you add more characters. The search is case sensitive.

   A dropdown will appear with your search results. Scroll down until you find the customer profile you are looking for. Click to select the customer.

4. When you have selected a customer, the search box will turn green and the **Save** button will be enabled.

5. The remaining fields are optional but fill them in as necessary. These include:
   * **Currency** - The currency of the account.
   * **Withdrawal daily limit** - The maximum amount that can be withdrawn from the account daily.
   * **Transfer daily limit** - The maximum amount that can be transferred from the account daily.

6. When you have entered all information necessary for this account, click **Save**. A message will appear indicating that the account has been created successfully.

7. When an account is created, it is in **PENDING** status. This must be changed to **ACTIVE** for a customer to be able to interact with and use the account. See [Change an account status](#change-an-account-status) for more information.

{{< figure alt="Create account" zoom="/en/gifs/create-current-account-biab-1.0.gif" >}}

### Create a Savings account

{{< note >}}
In order to create a Savings account, the customer must have an existing current account.
{{< /note >}}

1. Navigate to the **Accounts** screen and click **Create New** in the top right corner of the page.

2. Select the **Account Type**: **Savings Account**.

3. Search for an existing customer by name, email, customer ID, or Phone number. The search will begin after you have typed three characters and will update as you add more characters. The search is case sensitive.

4. When you have selected a customer, the search box will turn green and a message will appear indicating the number of current accounts found for that customer.

5. Select the currency of the savings account.

   {{< note >}}
   If you plan to make transfer between your **Current account** and **Savings account**, note that these should be set to use the same currency.
   {{< /note >}}

6. Select the desired current account. All existing current accounts for that customer will be displayed in a dropdown.

7. Select a start date and time for the savings account.

8. Enter a savings period (in months) for the savings account.

9. When you have entered all information, click **Save**. A message will appear indicating that the account has been created successfully.

10. When an account is created, it is in **PENDING** status. This must be changed to **ACTIVE** for a customer to be able to interact with and use the account. See [Change an account status](#change-an-account-status) for instructions.



### Change an account status

An account has three statuses: **PENDING**, **ACTIVE**, and **SUSPENDED**. When the account is first created, it will be in **PENDING** status. You must change the status to **ACTIVE** so that the customer can use their account.

1. Go to the Account page. Click the Set Status button.

2. Select **ACTIVE** and click Save.

3. You will receive a message indicating that the account has been set to **ACTIVE**.

If the account needs to be suspended, follow the same steps but select **SUSPENDED**.

{{< figure alt="Set account status" zoom="/en/gifs/set-account-status-biab-1.0.gif" >}}


### Assign or revoke a user role

Once a customer profile has been created _and_ they have [registered as a user on Bank in a Box](#register-as-a-user-on-bank-in-a-box), an administrator must assign a user role.

**GUEST** is the default role registered users are given, but they cannot interact with their accounts until they are granted **CUSTOMER** permissions.

#### Assign a user role

To assign a user role, follow these steps:

1. Navigate to the User management page.

2. Select the **GUEST** Account type from the dropdown menu. You will see all users registered as **GUEST**.

3. Select the user whose role you would like to change.

4. Set the role to **CUSTOMER** for bank customers. Set to **ADMIN** for anyone needing administrator permissions.

5. Click **Revoke**. A message will appear indicating that the user role was assigned successfully.

{{< figure alt="Assign role" zoom="/en/gifs/assign-a-role-biab-1.0.gif" >}}

#### Revoke a user role

To revoke a user role, follow these steps:

1. Navigate to the User management page.

2. Select the Account type of the user whose role you wish to revoke.

3. Select the user whose role you would like to change.

4. Select the role you wish to revoke from the user.

5. Click **Save**. A message will appear indicating that the user role was revoked successfully.

{{< figure alt="Revoke role" zoom="/en/gifs/revoke-role-biab-1.0.gif" >}}

### Issue a loan

Once the account has been set to **ACTIVE**, you will have the ability to issue a loan. You can see that the **Issue Loan** button has now been enabled.

1. Go to the Account page. Click Issue Loan.

2. Enter the loan amount.

3. Enter the loan period in months.

4. Click **Save**. You will receive a message indicating that the loan has been issued successfully. You will now see the loan amount reflected in the Balance on the Account page.

A loan account is created when a loan has been issued successfully.

{{< figure alt="Issue loan" zoom="/en/gifs/issue-loan-biab-1.0.gif" >}}

### Approve overdrafts

You may wish to approve an overdraft amount for an account. This overdraft represents an extension of credit from the bank that is granted when a customer attempts to withdraw or transfer an amount higher than the amount they have in the account.

For example, a customer has $50 in their savings account. They have an approved overdraft limit of $20. The customer transfers $60 to pay a bill. The transfer goes through successfully and the customer has $10 remaining in their overdraft account.

To approve an overdraft, follow these steps.

1. Go to the Account page. Click **Approve Overdraft**.

2. Enter the amount the customer will be able to overdraw.

3. Click **Save**. A message will appear indicating that the overdraft has been successfully approved.

{{< note >}}
Overdrafts can be approved whether the account is **PENDING**, **ACTIVE**, or **SUSPENDED**.
{{< /note >}}

{{< figure alt="Approve overdraft" zoom="/en/gifs/approve-overdraft-biab-1.0.gif" >}}


### Deposit money to an account

Follow these steps to deposit money to a customer account.

1. Go to the Account page. Click **Depost**.

2. Enter the amount of money you wish to deposit.

3. Select the currency of the deposit you are making.

4. Click **Save**. You will receive a message indicating that the deposit was successful.

{{< figure alt="Deposit" zoom="/en/gifs/deposit-biab-1.0.gif" >}}


### Register as a user on Bank in a Box

You must be registered as a **Customer** or **Admin** on Bank in a Box to perform tasks. Follow these steps to register:

1. From the Home page, click the **Menu** and select **Register**.

2. Enter your desired user name.

   {{< note >}}
   If the user name that you enter is already taken, you will receive an error message and must enter a different user name.
   {{< /note >}}

3. Enter your email address.

4. Enter a password.

5. Click **Save**. A message will appear indicating that you have registered successfully.

{{< figure alt="Register user" zoom="/en/gifs/register-user-customer-biab-1.0.gif" >}}


### Update customer profile

As an Admin user, you can update customer profiles. You can also view existing attachments or add new attachments. These attachments mimic a user identity verification  and application process.

1. Navigate to the **Customers screen**. Click on the name of the customer whose profile you wish to update.

2. Update fields as necessary.

3. The **Save** button will be enabled once new information has been added. Click **Save**.

4. You are taken back to the Customers screen. A message will appear indicating that the customer profile was updated successfully.

{{< note >}}
A Customer will not be able to update their own **Post code** or upload a new **Attachment** as these changes must be verified by a bank employee.
{{< /note >}}


### Set withdrawal and transfer limits

Daily withdrawal and transfer limits can be applied to accounts. These are defined as:

* **Withdrawal daily limit** - The maximum amount that can be withdrawn from an account daily.
* **Transfer daily limit** - The maximum amount that can be transferred from an account daily.

An **Admin user** can set an account's **Withdrawal daily limit** or **Transfer daily limit** when they create an account, however this field is optional. If you wish to add or modify these limits later, follow these steps.

1. Enter an amount above zero in desired limit field (**Withdrawal daily limit** or **Transfer daily limit**). If "0" is entered or the field is left blank, the account will not have that limit applied.

2. Click **Save** when you've entered the desired limits. A message will appear indicating that the limits have been saved successfully.

{{< figure alt="Set withdrawal and transfer limits - admin" zoom="/en/gifs/set-limits-admin-biab-1.0.gif" >}}


## Customer tasks

### Create an intrabank payment

Follow these steps to create a new intrabank payment.

1. Go to the Intrabank payment screen.

   {{< note >}}
   You will only have access to this screen if you have at least one active current account.
  {{< /note >}}

2. In the **Account from** field, enter your account ID.

3. In the **Account to** field, enter the account ID of the receiving account.

4. Enter the amount of money you wish to transfer.

5. Select the currency of the payment.

6. Click **Save**. You will receive a notification indicating that the payment was created successfully. You will also receive notifications indicating any changes in your account balances.

{{< figure alt="Create intrabank payment" zoom="/en/gifs/create-intrabank-payment-biab-1.0.gif" >}}

After making a payment, you can view the details of this transaction on the Transactions screen.


{{< figure alt="View transaction" width="800" zoom="/en/gifs/view-transaction-biab-1.0.gif" >}}


### Create a recurring payment

Follow these steps to create a recurring payment:

1. Go to the Recurring payments screen. Click the **Create New** button.

   {{< note >}}
   You will only have access to this screen if you have at least one active current account.
   {{< /note >}}

2. Fill out all fields:
   * Account from - the ID of the account that sent the money.
   * Account to - the ID of the account that received the money.
   * Amount - the amount of money to be sent.
   * Start date - the date the recurring payment will begin.
   * Number of iterations - the number of payments that will occur.

2. Once you have completed the required fields, the **Save** button will be enabled. Click **Save**.

3. You will be taken back to the **Recurring payments screen** where you will receive a message indicating that the recurring payment was created successfully.

{{< figure alt="Recurring payment" zoom="/en/gifs/create-recurring-payment-biab-1.0.gif" >}}

{{< note >}}
This payment will not appear on the **Recurring payments screen** until the first iteration has occurred.
{{< /note >}}


### Register as a user on Bank in a Box

You must be registered as a Customer or Admin on Bank in a Box to perform tasks. Follow these steps to register:

1. From the Home page, click the **Menu** and select **Register**.

2. Enter your desired user name.

   {{< note >}}
   If the user name that you enter is already taken, you will receive an error message and must enter a different user name.
   {{< /note >}}

3. Enter your email address.

4. Enter a password.

5. Enter your Customer ID.

6. Upload the same customer document that the bank has associated to your account. This attachment mimics a user identity verification and application process.

7. Click **Save**. A message will appear indicating that you have registered successfully.

{{< figure alt="Register user" zoom="/en/gifs/register-user-customer-biab-1.0.gif" >}}


### Update a customer profile

Update your customer profile by following these steps:

1. Navigate to the **Update My Profile screen**.

2. Update fields as necessary.

3. The **Save** button will be enabled once new information has been added. Click **Save**.

4. You are taken back to the Customers screen and a message will appear indicating that the customer was updated successfully.

{{< note >}}
A Customer will not be able to update their own **Post code** or **Attachments** as these changes must be verified by a bank employee.
{{< /note >}}


### Set withdrawal and transfer limits

Daily withdrawal and transfer limits can be applied to accounts. These are defined as:

* **Withdrawal daily limit** - The maximum amount that can be withdrawn from an account daily.
* **Transfer daily limit** - The maximum amount that can be transferred from an account daily.

To set these limits as a **Customer**, follow these steps.

1. Go to the **Account** page.

2. Under the **Account** tab, click the **Set Limits** button in the upper right-hand corner of the page.

2. Enter the maximum amount you wish to be able to withdraw on a given day.

3. Enter the maximum amount you wish to be able to transfer on a given day.

4. Click **Save**. You will be taken back to the Account page where you will receive a message indicating that the limits have been updated successfully.

{{< figure alt="Set withdrawal and transfer limits - customer" zoom="/en/gifs/set-limits-customer-biab-1.0.gif" >}}
