---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    parent: "bankinabox"
    identifier: bank-in-a-box-api-guide
tags:
- Bank in a Box
- API
title: Bank in a Box API guide
weight: 400
---


# Bank in a Box API guide

Bank in a Box uses a REST API to communicate with external systems, provide endpoints for all flows, and provide security to these flows.

These endpoints and their corresponding flows are described below, organised by controller (logical groupings of endpoints that provide a specific set of services).

## Base URL

As Bank in a Box is used for testing and learning, the base URL is `localhost` with the [port assigned during installation](getting-started.md/#service-endpoints-display-logs-and-exec-into-container) using the Kubernetes port forward feature.

For the examples shown below, the base URL is: `http://localhost:7777/`

## Roles

There are three roles in the Bank in a Box application.

- Admin - can perform all tasks that a bank employee would need to in their daily work.
- Customer - can perform the normal banking activities of a bank's customer.
- Guest - can register as a guest user on the application. A guest user can explore some screens on the application's user interface, but cannot perform any tasks or view banking details until an admin has assigned them the role of customer.

## Suggested order for sending requests to invoke flows

Many flows in Bank in a Box depend upon other flows being invoked first. After authenticating, follow the order recommended below to avoid errors.

1. [Upload a customer attachment](#upload-an-attachment).
2. [Create a customer](#create-a-customer) using the same attachment and secure hash pair from above.
3. [Register a user account](#register-a-user-account) using the customer ID and attachment from above steps.
4. [Assign a role to the user](#assign-a-role-to-a-user) account created above.
4. [Create a current account](#create-a-current-account) with the customer ID generated above.
5. [Set account status](#set-account-status) to `ACTIVE` for the created current account.

Once the flows above have been invoked, all other flows can also be invoked without issue.


## Authentication

Bank in a Box supports [OAuth 2.0](https://oauth.net/2/) authentication.

Send the sample request listed below (with default admin parameters) the first time you authenticate, with the appropriate base URL.

- Request type: `POST`.
- Path: `/oauth/token`.

{{< table >}}
| Param        | Description                                          | Type   | Required |
| ------------ | ---------------------------------------------------- | ------ | -------- |
| `grant_type` | Method for gaining access token. Set to: `password`. | string | Yes      |
| `username`   | The username of the user requesting an access token. | string | Yes      |
| `password`   | User's password.                                     | string | Yes      |
{{< /table >}}

Response: This request will return an `access_token` and `refresh_token`. Use the access token to authorize future requests. Use the refresh token to get a new access token, which is then valid for 30 minutes.

Sample request:
```
curl --location --request POST 'http://localhost:7777/oauth/token?grant_type=password&username=admin&password=password1!' \
--header 'Authorization: Basic YmFua19pbl90aGVfYm94X2FwcDpwYXNzd29yZDEh'
```

Sample response:
```
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAwNTQ3NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiYjBiZDRjMmYtMzQ4My00ZDBkLTgxOWMtNDJhYjE5Mzc4YTAwIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.HHL-8bxXjFKYvvEY8QivkrouFM83om3txRRUBAY7tO7PirxgoQlsIcJsgcG1-CJD-xRDlep4vbzdFkO13EpTmTx0Z5TVa1OBXtEXyKBGEw1MZ-viECPCjll32GHNduQm3df9E22w-iw2t4JuiWg-qpQuGEPlMm29xLHpnIkKKu7Xp-wKImOJzr70-bNxYwxwAlB2UZcROBvvAVtSvoVKvC0HltziKA9Y_Ye_ix4-erd3cr1y5CVVlElcuqFR_KMJiE_6Bznm70KeiimWP5ulvbFH6owlE26g0lNZ-qP9IuOuLF3Lrq2V1KvppXqnGKW2kAKYvo6420P1n1exu3Tldg",
    "token_type": "bearer",
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImF0aSI6ImIwYmQ0YzJmLTM0ODMtNGQwZC04MTljLTQyYWIxOTM3OGEwMCIsImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAwODE3NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiYzRkY2VkNWMtNTIyOC00ZmRjLTkxOTgtNDcyNDE3NWNhMzNjIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.LDvMvMYqizAQpFRGrWMwFq3KGINfL6Y90VA6RsopdH4aUfm0k5_-p1fMlwZWsyL6M75u2MVimJFgXkSFFDwoj2NwA6PyTRy3a17bV5o4lvSnhH_qftR7x8sPGmvy3LyraovDpkAn4Qk-rvsjA8n0CMmuS5oq417kVmaJ2HheJZ5eIuFA53saftq4V7G-fWKCXONqYDzl9RT8_34cI40GPy15iZ_DwzsDH3Ye_YQU13laF-ckTx4xXCELqumOvQlOxurqmAmUTW3fkyzvWnC-WV1F_uZStENHCDi_j52dOyuCGIOWvgtX4wwNCeNvmY3tgls1IcN-aWQ61y1j1_hUKQ",
    "expires_in": 899,
    "scope": "read write",
    "customerId": null,
    "jti": "b0bd4c2f-3483-4d0d-819c-42ab19378a00"
}
```

### Access token

Use the `access_token` from the authentication request response as a [bearer token](https://oauth.net/2/bearer-tokens/) in subsequent requests, as shown in the examples in later sections.

After initial authentication, additional `access_token`s can be created for [registered users](#register-a-user-account) following the process above, and substituting the username and password listed with the customer's username and password.

If a request can only be sent by an admin user, it requires an admin `access_token`. If it can only be sent by a customer, it requires that customer's `access_token`.

By default, the `access_token` is valid for 30 minutes. This value can be changed in the migration script.

### Refresh token

After the initial authentication request, you can also use the `refresh_token` from the response above to obtain a new access token that will be valid for an additional 30 minutes. This value can also be changed in the migration script.

- Request type: `POST`.
- Path: `/oauth/token`.

{{< table >}}
| Param        | Description                                               | Type   | Required |
| ------------ | --------------------------------------------------------- | ------ | -------- |
| `grant_type` | Method for gaining access token. Set to: `refresh_token`. | string | Yes      |
| `username`   | The username of the user requesting an access token.      | string | Yes      |
| `password`   | User's password.                                          | string | Yes      |
{{< /table >}}

Sample request:
```
curl --location --request POST 'http://localhost:7777/oauth/token?grant_type=refresh_token&refresh_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImF0aSI6ImM1MDVmMjliLTZlOWUtNDgwMy05ODJiLTIwOTM1MDk2NmJmMCIsImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMTM2NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNGQzYTgxNzMtY2FiNC00MWVhLWI5MzItYmQzNjRiY2U0MTFiIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.YQd9FIUG_-mMB4cJYTuPDTKrdUSBYgdJHMFg1whAktlntyWaqgdJoPXVl60cIGCRbzSmmTeZKi6Z4KVarb-xRAr2-AhJH4k-obuy5fofBenZ2JlHxjBtwG96BfgOYKTCC50__7RxCJ5z3vdD46ErLQgTpzjTCFckwwPyDa9Owj8Yy7mxv3RWcFF0yDFfVihBfT-sOdCfgF1xZ5Ol7ZcbbkGJ3FMRUYtqYJsx4JJRJbBwD0vOD52Ya6149TDzVL_EipR6itEsIYtmufm2ttfW8gKQy3y4XY5b4m3z2EOGnw--jPrJ2sFt8Ty2Ww-tGI2jk2SRL46zvPuW84gyhkhFuA' \
--header 'Authorization: Basic YmFua19pbl9hX2JveF9hcHA6cGFzc3dvcmQxIQ=='
```

Sample response:
```
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAxODc0MSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMTdhNzNhOTMtNmUxZS00OWQzLWFlMjEtNzc2NGVmNWFhNmM2IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.wiKppW1sKPUflBLsnfh0yOHdIEOJDR1gY9LE4XOZ0mqMJUzxgcLeAAzpVRi3H5aS150jzBhnpY1Mi-xnJrKcFU1KsO0NtGIUJMQnxmXlMbDioy0pGMmX9YKP8qAqXadTIvHtxgpPZVsTiKPhHedJpLcuvr2JB21k3xfzImFxGG3WrLMqbV83alRX7B_4cpEQAWcDaMKmDsriCfsa3gDMOKW-KNCuNXoy4oTtj97nxlyIuz1pFiBU05c_vvJywXqzU8vaBL9cWFOOAPjdt_9V92y5X_RSdX3FcIIqNK8LLPKTOQE8BK57_Gq_H5Fx_DVv0tLOHJfeQ-vksbE-7k25-w",
    "token_type": "bearer",
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImF0aSI6IjE3YTczYTkzLTZlMWUtNDlkMy1hZTIxLTc3NjRlZjVhYTZjNiIsImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMTM2NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNGQzYTgxNzMtY2FiNC00MWVhLWI5MzItYmQzNjRiY2U0MTFiIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.LXVGymuLS_qGh9mTiJlLDMwcq2AC7hmXKWvrN88FCx8rygcd5GG31CDOFl5K-9cOUc2uzz0latuhuF5BuK9h-Xp_oa2ftKK3zaS2kXo2KoRCoiw9aLlchlZ9kWTsgQGz2Pq5LkqvU5oyICukODfdE6j9pI5WihenuI8h3SKbj2OmUZrFolZ2r-cAzwgjQoLV6HzAGo2yrrXz05-ZgyHSz9b1AkjwRA_VyTV4vDpbf7fh_2b-k0ddlClXCt8vr1U82mQjaVnYx0lmf4emi3Q6n5-53pqua6dXg-7IJ7CGDgTA9N6ho7EgLAGrR7urh2P5Sjl-p1lmPNqR2gaPhUdDsA",
    "expires_in": 899,
    "scope": "read write",
    "customerId": null,
    "jti": "17a73a93-6e1e-49d3-ae21-7764ef5aa6c6"
}
```

## Registration Controller

The Registration Controller includes API endpoints that handle authorization for the Bank in a Box. Requests sent to these endpoints allow a user to register a user account, add a role to a user, see all users with a specified role, and revoke a role from a user.

### Register a user account

Send a `POST` request to the `/register/guest` endpoint to register a new user account with a guest role and optionally link a customer account with an existing customer ID. If linking to a customer account, the same attachment that was uploaded when the customer account was created must be attached now as a file in the body of the request.

This request does not require authorization. It can be performed by admin, customer, and guest users.

- Request type: `POST`.
- Path: `/register/guest`.

{{< table >}}
| Param        | Description                                     | Type   | Required |
| ------------ | ----------------------------------------------- | ------ | --------- |
| `username`   | Unique identifier of the user to be registered. | string | Yes       |
| `password`   | User's password.                                | string | Yes       |
| `email`      | User's email address.                           | string | Yes       |
| `customerId` | Associated customer ID for this account.        | string | No        |
{{< /table >}}

If linking the customer account to an existing customer ID, include the same customer attachment as provided when creating the customer. Add the attachment as a file in the body of the request, as shown in the sample request below.

Response: `200` - request successful.

Sample request:
```
curl --location --request POST 'http://localhost:7777/register/guest?username=alice.smith&password=test2&email=alice.smith@email.com&customerId=0fcf24fd-9297-4ffe-9ba2-c6ddfa0cfee7' \
--header 'X-XSRF-TOKEN: 567899a7-322d-4d65-b506-5dfffeb5ce42' \
--form 'file=@"/Users/Admin/Documents/alice-smith-attachment.zip"'
```


#### Add role to user

When a user account is created, it is given the default role of guest. Send a `POST` request to the `/register/admin/addRole` endpoint to assign a different role to an existing user account. A user may be assigned an admin or customer role. This request requires authorization. It can be sent by admin users.

- Request type: `POST`.
- Path: `/register/admin/addRole`.

{{< table >}}
| Param      | Description                                              | Type   | Required |
| ---------- | -------------------------------------------------------- | ------ | -------- |
| `username` | Unique identifier of the user name.                      | string | Yes      |
| `roleName` | Name of the new role to be added (`ADMIN` or `CUSTOMER`) | string | Yes      |
{{< /table >}}

Response: `200` - request successful.

Sample request:
```
curl --location --request POST 'http://localhost:7777/register/admin/addRole?username=alice.smith&roleName=CUSTOMER' \
--header 'X-XSRF-TOKEN: 4833d5dd-164e-4ba7-8abb-bea3096b27f0' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzA5NDU4MCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiYjFlMTZhYmYtNTUyZi00ZGQzLTk2ZjItYzI4NWEwMDg4YzA3IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.ntIhTDV805ftM_emquArorDa4RuHOo6pWLbZGTX4sqEFY1zdO_Y0NDnGV3-fMN2swHIW-Vu-M0ohk0tn2SpNJIU0177iYB7BIq7FpCiMWT0s8ETsKfTQpMreRT1WZnDSp7WTxzj9X1rPwzPocPtofE3-OVemqznonmi3rOlfmVkFN9kqPoY0SeA_KIDh_MuXmZoMxwY5ocBQuze5t9tgjuSh4Bptb65uJHhkaanOlzOON3SupH38V3h3E7nomEzXs-dq3-6chay0s5ZzySc-kJdmZu86gG_jBDlJfc9ovfqBKSbLsWpI99nRwu1sPKvGU0wqhUQKpv9038JqTIpolQ'
```


#### Get users in role

Send a `GET` request to the  `/register/admin/users` endpoint to return a list of all users assigned to a specified role (customer, admin, or guest) matching the given search criteria. This request requires authorization. It can be sent by admin users.

- Request type: `GET`.
- Path: `/register/admin/users`.

{{< table >}}
| Param       | Description                                              | Type   | Required |
| ----------- | -------------------------------------------------------- | ------ | -------- |
| `roleName`  | Name of the new role to be added (`ADMIN` or `CUSTOMER`) | string | Yes      |
| `startPage` | Position of the start page to return.                    | int    | Yes      |
| `pageSize`  | The maximum number of results in a page.                 | int    | Yes      |
| `sortField` | Sort results by `username` or `email`.                   | string | No       |
| `sortOrder` | Order of the sort (`ASC` or `DESC`)                      | string | No       |
{{< /table >}}

Response: A paginated list of all users assigned to the specified role - `PaginatedResponse<UserResponse>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/register/admin/users?roleName=CUSTOMER&startPage=1&pageSize=10&sortField=email&sortOrder=ASC' \
--header 'X-XSRF-TOKEN: 4833d5dd-164e-4ba7-8abb-bea3096b27f0' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzEwMzQ4NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNWU2YTQ2OGEtZTYzNi00Y2VmLTkxN2EtMTI1MjVhMmFhZTg2IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.oWz7S-SN60m-tFWu1kW96gTxJ3mJfaG6IKig2HcDxcJL4saiVisufCfhkfFvhqSLeLSiLaTI60C87OG-KBJp_9G2tYRXmJINXm20KfPuo0BkQASHupO7KydATFeIjot4sYhY0pYxY9dCBoCkQ_QkBFp9nQw0ryQDOOBWvtlHB8bMgttNZxSUVzTpKiuH4irWA7-yOw3Uog65sJBXUXJMsOz4iNIdxavLrSYKgAMKtxQQwUeabeEQAsGdDHGGHnniLf2LhRz8Tr8GHJS0hZCGuN3epEvQZhRVsh3SEOwOLN3uL8_xBUWR02SqB4BpT0X6bXKPWzUpbXFrdY8K41mPAg'
```

Sample response:
```
{
    "result": [
        {
            "username": "alice.smith",
            "email": "alice.smith@email.com",
            "roles": "CUSTOMER, GUEST"
        },
        {
            "username": "josh.smith",
            "email": "josh.smith@email.com",
            "roles": "CUSTOMER, GUEST"
        }
    ],
    "totalResults": 2,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 1
}
```


#### Revoke user role

Send a `POST` request to the `/register/admin/revokeRole` endpoint to revoke a role from a user account. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/register/admin/revokeRole`.

{{< table >}}
| Param      | Description                                         | Type   | Required |
| ---------- | --------------------------------------------------- | ------ | -------- |
| `username` | Unique identifier of the user account.              | string | Yes      |
| `roleName` | Name of the role to revoke (`ADMIN` or `CUSTOMER`). | string | Yes      |
{{< /table >}}

Response: `200` - request successful.

Sample request:
```
curl --location --request POST 'http://localhost:7777/register/admin/revokeRole?username=alice.smith&roleName=CUSTOMER' \
--header 'X-XSRF-TOKEN: 4833d5dd-164e-4ba7-8abb-bea3096b27f0' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzEwMzQ4NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNWU2YTQ2OGEtZTYzNi00Y2VmLTkxN2EtMTI1MjVhMmFhZTg2IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.oWz7S-SN60m-tFWu1kW96gTxJ3mJfaG6IKig2HcDxcJL4saiVisufCfhkfFvhqSLeLSiLaTI60C87OG-KBJp_9G2tYRXmJINXm20KfPuo0BkQASHupO7KydATFeIjot4sYhY0pYxY9dCBoCkQ_QkBFp9nQw0ryQDOOBWvtlHB8bMgttNZxSUVzTpKiuH4irWA7-yOw3Uog65sJBXUXJMsOz4iNIdxavLrSYKgAMKtxQQwUeabeEQAsGdDHGGHnniLf2LhRz8Tr8GHJS0hZCGuN3epEvQZhRVsh3SEOwOLN3uL8_xBUWR02SqB4BpT0X6bXKPWzUpbXFrdY8K41mPAg'
```

## Account Controller

The Account Controller includes API endpoints that manage user accounts in the Bank in a Box. Requests sent to these endpoints allow an admin user to create a current account, create a savings account, issue a loan, set account limits, approve overdrafts, and list all accounts or account by account or customer ID.

### Create a Current Account

Send a `POST` request to the `/accounts/create-current-account` endpoint to invoke the [`CreateCurrentAccountFlow`](back-end-guide.md#createcurrentaccountflow). This flow creates a zero balance current account for a customer with the provided customer ID. The user also has the option to specify a withdrawal and/or transfer daily limit. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/accounts/create-current-account`.

{{< table >}}
| Param                  | Description                                                          | Type   | Required |
| ---------------------- | -------------------------------------------------------------------- | ------ | -------- |
| `customerId`           | Unique identifier of the customer who will own the account.          | int    | Yes      |
| `tokenType`            | The currency of the account balance (for example, `EUR`.)            | string | Yes      |
| `withdrawalDailyLimit` | Sets a limit for the maximum daily withdrawal amount on the account. | int    | No       |
| `transferDailyLimit`   | Sets a limit for the max daily transfer amount on the account.       | int    | No       |
{{< /table >}}

If the `withdrawalDailyLimit` and `transferDailyLimit` are not set, there will be no limit applied to the current account.

Response: the newly-created current account object - `CurrentAccountState`.

Sample request:
```
curl --location --request POST 'http://localhost:7777/accounts/create-current-account?customerId=34b439bf-5ec9-4788-b384-012e33a11845&tokenType=EUR&withdrawalDailyLimit&transferDailyLimit' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMjQ0NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZjdjMjhhYzYtODc1NS00N2FkLTg2M2YtZTc5MmM4MGRhYWMzIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.tCU4EQfnyQCDcWOUQe4Wnyck_luGY7ElboIfYzeE7VCvd0jKCZCk0sCjphx2fYIFjVgEZVwHOGdTogUe1tHyplCa8pOwfgnx-zL0ttHilDvPfpoDtzdE8Tu5vpcQg7erwPxqJ2CTlGlV0NJzMcYsHgjx_rcCU-ljVEJRjaldItNCpVTywBm0QejIZ_8rcGfUnkMuBY_JQ3Wf21pEtXO-U_-5pTxuoYNfbcXOHmR9zhMbKIUCodjFdWbgFv8WYl6eZi1OaIqunGmcsW50QE2T1Xfl32zKz5_aNMCgH4NQ6789ufLAWFEOiArz0HEb1bSL6G4TFL4JOXUrQPrCg6bJXA'
```

Sample response:
```
{
    "accountData": {
        "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
        "accountInfo": {
            "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "0.00 of EUR",
        "txDate": "2020-12-03T18:56:52.358Z",
        "status": "PENDING"
    },
    "approvedOverdraftLimit": null,
    "linearId": {
        "externalId": null,
        "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
    },
    "overdraftBalance": null,
    "transferDailyLimit": null,
    "withdrawalDailyLimit": null,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Create a Savings Account

Send a `POST` request to the `/accounts/create-savings-account` endpoint to invoke the []`CreateSavingsAccountFlow`](back-end-guide.md#createsavingsaccountflow). This flow creates a zero balance savings account for a customer with the provided customer ID. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/accounts/create-savings-account`.

{{< table >}}
| Param              | Description                                                 | Type   | Required |
| ------------------ | ----------------------------------------------------------- | ------ | -------- |
| `customerId`       | Unique identifier of the customer who will own the account. | int    | Yes      |
| `tokenType`        | The currency of the account balance (for example, `EUR`.)   | string | Yes      |
| `currentAccountId` | The ID of the current account to transfer savings from.     | int    | Yes      |
| `savingsAmount`    | Monthly amount to be transferred.                           | int    | Yes      |
| `savingsStartDate` | Start date of the first savings payment.                    | string | Yes      |
| `savingsPeriod`    | Duration in months of the savings plan.                     | int    | Yes      |
{{< /table >}}

Response: The newly-created savings account object - `SavingsAccountState`.

Sample request:
```
curl --location --request POST 'http://localhost:7777/accounts/create-savings-account?customerId=34b439bf-5ec9-4788-b384-012e33a11845&tokenType=EUR&currentAccountId=20cc3fbb-ba68-4ac6-856e-dda2159bcd82&savingsAmount=100&savingsStartDate=2020-12-09T14:47:00Z&savingsPeriod=1' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMjQ0NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZjdjMjhhYzYtODc1NS00N2FkLTg2M2YtZTc5MmM4MGRhYWMzIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.tCU4EQfnyQCDcWOUQe4Wnyck_luGY7ElboIfYzeE7VCvd0jKCZCk0sCjphx2fYIFjVgEZVwHOGdTogUe1tHyplCa8pOwfgnx-zL0ttHilDvPfpoDtzdE8Tu5vpcQg7erwPxqJ2CTlGlV0NJzMcYsHgjx_rcCU-ljVEJRjaldItNCpVTywBm0QejIZ_8rcGfUnkMuBY_JQ3Wf21pEtXO-U_-5pTxuoYNfbcXOHmR9zhMbKIUCodjFdWbgFv8WYl6eZi1OaIqunGmcsW50QE2T1Xfl32zKz5_aNMCgH4NQ6789ufLAWFEOiArz0HEb1bSL6G4TFL4JOXUrQPrCg6bJXA'
```

Sample response:
```
{
    "accountData": {
        "accountId": "880df321-3259-4778-9486-2accb1a2b840",
        "accountInfo": {
            "name": "493a514f-1f6d-467a-953e-e9efae418573",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "880df321-3259-4778-9486-2accb1a2b840"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "0.00 of EUR",
        "txDate": "2020-12-03T18:59:44.246Z",
        "status": "PENDING"
    },
    "linearId": {
        "externalId": null,
        "id": "81fa04c0-1e3c-41f8-a11c-7f52805f0c9a"
    },
    "period": "P1M",
    "savingsEndDate": "2021-01-09T14:47:00Z",
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "savings"
}
```


### Approve overdraft

Send a `PUT` request to the `/accounts/approve-overdraft-account` endpoint to invoke the [`ApproveOverdraftFlow`](back-end-guide.md#approveoverdraftflow). This flow is used to approve an overdraft limit for an account with the specified account ID. This request requires authorization. It can be sent by an admin user.

- Request type: `PUT`.
- Path: `/accounts/approve-overdraft-account`.

{{< table >}}
| Param              | Description                                                           | Type   | Required |
| ------------------ | --------------------------------------------------------------------- | ------ | -------- |
| `currentAccountId` | Unique identifier of the current account receiving overdraft approval. | int    | Yes      |
| `amount`           | Overdraft limit amount.                                               | int    | Yes      |
| `tokenType`        | The currency of the account balance (for example, `EUR`.)             | string | Yes      |
{{< /table >}}

Response: This request returns a `CurrentAccountState` with an overdraft limit of `amount`.

Sample request:
```
curl --location --request PUT 'http://localhost:7777/accounts/approve-overdraft-account?currentAccountId=20cc3fbb-ba68-4ac6-856e-dda2159bcd82&tokenType=EUR&amount=200' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMzQxMSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMWYwYmU2ZWItZjAxZi00M2FmLWI0YWEtYWJlMjk1MGFlNTM1IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.orXLAHjySCi28I-MgHYHfaNIf4xqSd7aWEyG0cxIoYFMXe40sfUgyy16IHkHmcJU1WfzIcm2QsEmqubzNsfnCojNRYODK6dVpaP_ZK9nOx5mZH4aHN574geF11vMtdqdDEAaJSFtd0EJAZQUCXcXFDkzh2l9xGRafSgL_GzXCRr0HyX2E-u-euCgnQmAo1irs5TumIrb0SOHt5YUYhu-GRyI5kNrbKsS23SankQN6Yn5uT-QrzyN8zqPOoJn121z_sx8_QpHLV96YqU-ccaypTDrWjpkckMPQ3cHNvzbHqjwg-EKgTOw3MZe2_5duc281KBMvktnQQJUpmlrNs_t_g'
```

Sample response:

```
{
    "accountData": {
        "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
        "accountInfo": {
            "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "10.00 of EUR",
        "txDate": "2020-12-03T19:05:27.709Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": 200,
    "linearId": {
        "externalId": null,
        "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
    },
    "overdraftBalance": 0,
    "transferDailyLimit": 500,
    "withdrawalDailyLimit": 500,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```

### Issue a loan

Send a `POST` request to the `/accounts/issue-loan` endpoint to invoke the [`IssueLoanFlow`](back-end-guide.md#issueloanflow). The `IssueLoanFlow` issues a new loan to a customer with the repayment account referenced by the account ID. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/accounts/issue-loan`.

{{< table >}}
| Param        | Description                                                                                            | Type   | Required |
| ------------ | ------------------------------------------------------------------------------------------------------ | ------ | -------- |
| `accountId`  | Unique identifier of the current account to deposit loan amount to and to transfer repayments from. | int    | Yes      |
| `loanAmount` | Principal of the loan.                                                                                 | int    | Yes      |
| `tokenType`  | The currency of the loan balance (for example, `EUR`.)                                                 | string | Yes      |
| `period`     | Repayment period in months.                                                                            | int    | Yes      |
{{< /table >}}

Response: This request returns a reference to the payment - `IssueLoanResponse`. It also returns the current account and the issued loan account information.

Sample request:
```
curl --location --request POST 'http://localhost:7777/accounts/issue-loan?accountId=20cc3fbb-ba68-4ac6-856e-dda2159bcd82&tokenType=EUR&loanAmount=1000&period=12' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMjQ0NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZjdjMjhhYzYtODc1NS00N2FkLTg2M2YtZTc5MmM4MGRhYWMzIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.tCU4EQfnyQCDcWOUQe4Wnyck_luGY7ElboIfYzeE7VCvd0jKCZCk0sCjphx2fYIFjVgEZVwHOGdTogUe1tHyplCa8pOwfgnx-zL0ttHilDvPfpoDtzdE8Tu5vpcQg7erwPxqJ2CTlGlV0NJzMcYsHgjx_rcCU-ljVEJRjaldItNCpVTywBm0QejIZ_8rcGfUnkMuBY_JQ3Wf21pEtXO-U_-5pTxuoYNfbcXOHmR9zhMbKIUCodjFdWbgFv8WYl6eZi1OaIqunGmcsW50QE2T1Xfl32zKz5_aNMCgH4NQ6789ufLAWFEOiArz0HEb1bSL6G4TFL4JOXUrQPrCg6bJXA'
```

Sample response:
```
{
    "currentAccount": {
        "accountData": {
            "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
            "accountInfo": {
                "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
                "host": "O=Bank, L=London, C=GB",
                "identifier": {
                    "externalId": null,
                    "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
                }
            },
            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
            "balance": "10.00 of EUR",
            "txDate": "2020-12-03T19:05:27.709Z",
            "status": "ACTIVE"
        },
        "approvedOverdraftLimit": null,
        "linearId": {
            "externalId": null,
            "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
        },
        "overdraftBalance": null,
        "transferDailyLimit": null,
        "withdrawalDailyLimit": null,
        "participants": [
            "O=Bank, L=London, C=GB"
        ],
        "type": "current"
    },
    "loanAccount": {
        "accountData": {
            "accountId": "045985c9-b6e7-47ca-ae3e-361e1e6b3eba",
            "accountInfo": {
                "name": "ce7a2ba0-fec8-4fe5-9638-63b1c5f6530c",
                "host": "O=Bank, L=London, C=GB",
                "identifier": {
                    "externalId": null,
                    "id": "045985c9-b6e7-47ca-ae3e-361e1e6b3eba"
                }
            },
            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
            "balance": "10.00 of EUR",
            "txDate": "2020-12-03T19:05:27.779Z",
            "status": "ACTIVE"
        },
        "linearId": {
            "externalId": null,
            "id": "c736e3e0-cda2-4090-b899-2c358bb3ea78"
        },
        "participants": [
            "O=Bank, L=London, C=GB"
        ],
        "type": "loan"
    }
}
```


### Set Account Status

Send a `PUT` request to the `/accounts/set-status` endpoint to invoke the [`SetAccountStatusFlow`](back-end-guide.md#setaccountstatusflow). The `SetAccountStatusFlow` updates the status of an account with a specified account ID. This request requires authorization. It can be sent by an admin user.

- Request type: `PUT`.
- Path: `/accounts/set-status`.

{{< table >}}
| Param       | Description                                              | Type   | Required |
| ----------- | -------------------------------------------------------- | ------ | -------- |
| `accountId` | Unique identifier of the account.                        | int    | Yes      |
| `status`    | The new status of the account (`ACTIVE` or `SUSPENDED`). | string | Yes      |
{{< /table >}}

Response: This request returns the account information - `Account`.

Sample request:
```
curl --location --request PUT 'http://localhost:7777/accounts/set-status?accountId=20cc3fbb-ba68-4ac6-856e-dda2159bcd82&status=ACTIVE' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMjQ0NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZjdjMjhhYzYtODc1NS00N2FkLTg2M2YtZTc5MmM4MGRhYWMzIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.tCU4EQfnyQCDcWOUQe4Wnyck_luGY7ElboIfYzeE7VCvd0jKCZCk0sCjphx2fYIFjVgEZVwHOGdTogUe1tHyplCa8pOwfgnx-zL0ttHilDvPfpoDtzdE8Tu5vpcQg7erwPxqJ2CTlGlV0NJzMcYsHgjx_rcCU-ljVEJRjaldItNCpVTywBm0QejIZ_8rcGfUnkMuBY_JQ3Wf21pEtXO-U_-5pTxuoYNfbcXOHmR9zhMbKIUCodjFdWbgFv8WYl6eZi1OaIqunGmcsW50QE2T1Xfl32zKz5_aNMCgH4NQ6789ufLAWFEOiArz0HEb1bSL6G4TFL4JOXUrQPrCg6bJXA'
```

Sample response:
```
{
    "accountData": {
        "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
        "accountInfo": {
            "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "0.00 of EUR",
        "txDate": "2020-12-03T18:56:52.358Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": null,
    "linearId": {
        "externalId": null,
        "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
    },
    "overdraftBalance": null,
    "transferDailyLimit": null,
    "withdrawalDailyLimit": null,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Set account limits

Send a `PUT` request to the `/accounts/set-limits` endpoint to invoke the `SetAccountLimitsFlow`. The `SetAccountLimitsFlow` changes the daily withdrawal and transfer limits, or maximum spending, for the provided account ID. This request requires authorization. It can be set by an admin or customer user.

- Request type: `PUT`.
- Path: `/accounts/set-limits`.

{{< table >}}
| Param                  | Description                                                          | Type | Required |
| ---------------------- | -------------------------------------------------------------------- | ---- | -------- |
| `accountId`            | Unique identifier of the account.                                    | int  | Yes      |
| `withdrawalDailyLimit` | Sets a limit for the maximum daily withdrawal amount on the account. | int  | No       |
| `transferDailyLimit`   | Sets a limit for the max daily transfer amount on the account.       | int  | No       |
{{< /table >}}

Response: `CurrentAccountState`.

Sample request:
```
curl --location --request PUT 'http://localhost:7777/accounts/set-limits?accountId=20cc3fbb-ba68-4ac6-856e-dda2159bcd82&withdrawalDailyLimit=500&transferDailyLimit=500' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMzQxMSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMWYwYmU2ZWItZjAxZi00M2FmLWI0YWEtYWJlMjk1MGFlNTM1IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.orXLAHjySCi28I-MgHYHfaNIf4xqSd7aWEyG0cxIoYFMXe40sfUgyy16IHkHmcJU1WfzIcm2QsEmqubzNsfnCojNRYODK6dVpaP_ZK9nOx5mZH4aHN574geF11vMtdqdDEAaJSFtd0EJAZQUCXcXFDkzh2l9xGRafSgL_GzXCRr0HyX2E-u-euCgnQmAo1irs5TumIrb0SOHt5YUYhu-GRyI5kNrbKsS23SankQN6Yn5uT-QrzyN8zqPOoJn121z_sx8_QpHLV96YqU-ccaypTDrWjpkckMPQ3cHNvzbHqjwg-EKgTOw3MZe2_5duc281KBMvktnQQJUpmlrNs_t_g'
```

Sample response:
```
{
    "accountData": {
        "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
        "accountInfo": {
            "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "10.00 of EUR",
        "txDate": "2020-12-03T19:05:27.709Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": null,
    "linearId": {
        "externalId": null,
        "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
    },
    "overdraftBalance": null,
    "transferDailyLimit": 500,
    "withdrawalDailyLimit": 500,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Get account by account ID

Send a `GET` request to the `/accounts/{accountId}` endpoint to invoke the [`GetAccountFlow`](back-end-guide.md#getaccountflow). This flow returns the account information for a given account ID. This request requires authorization. It can be sent by an admin user or the customer who owns the account.

- Request type: `GET`.
- Path: `/accounts/{accountId}`.

Response: Account information - `Account`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/accounts/20cc3fbb-ba68-4ac6-856e-dda2159bcd82' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMzQxMSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMWYwYmU2ZWItZjAxZi00M2FmLWI0YWEtYWJlMjk1MGFlNTM1IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.orXLAHjySCi28I-MgHYHfaNIf4xqSd7aWEyG0cxIoYFMXe40sfUgyy16IHkHmcJU1WfzIcm2QsEmqubzNsfnCojNRYODK6dVpaP_ZK9nOx5mZH4aHN574geF11vMtdqdDEAaJSFtd0EJAZQUCXcXFDkzh2l9xGRafSgL_GzXCRr0HyX2E-u-euCgnQmAo1irs5TumIrb0SOHt5YUYhu-GRyI5kNrbKsS23SankQN6Yn5uT-QrzyN8zqPOoJn121z_sx8_QpHLV96YqU-ccaypTDrWjpkckMPQ3cHNvzbHqjwg-EKgTOw3MZe2_5duc281KBMvktnQQJUpmlrNs_t_g'
```

Sample response:
```
{
    "accountData": {
        "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
        "accountInfo": {
            "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
            }
        },
        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
        "balance": "10.00 of EUR",
        "txDate": "2020-12-03T19:05:27.709Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": 200,
    "linearId": {
        "externalId": null,
        "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
    },
    "overdraftBalance": 0,
    "transferDailyLimit": 500,
    "withdrawalDailyLimit": 500,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Get accounts

Send a `GET` request to the `/accounts` endpoint to invoke the [`GetAccountsPaginatedFlow`](back-end-guide.md#getaccountspaginatedflow). This flows displays a list of accounts and their associated customer information that match the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/accounts`.

{{< table >}}
| Param        | Description                                      | Type   | Required |
| ------------ | ------------------------------------------------ | ------ | -------- |
| `startPage`  | Position of the start page to return.            | int    | No       |
| `pageSize`   | The maximum number of results in a page.         | int    | No       |
| `sortField`  | Sort results by `username` or `email`.           | string | No       |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`)              | string | No       |
| `searchTerm` | Term to partially match against multiple fields. | string | No       |
| `dateFrom`   | Filter accounts with `txDate` after this date.   | string | No       |
| `dateTo`     | Filter accounts with `txDate` before this date.  | string | No       |
{{< /table >}}

Response: This request returns a paginated response with the account information and customer information of all accounts matching the search criteria. - `PaginatedResponse<Pair<Account, CustomerSchemaV1.Customer>>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/accounts' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMzQxMSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMWYwYmU2ZWItZjAxZi00M2FmLWI0YWEtYWJlMjk1MGFlNTM1IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.orXLAHjySCi28I-MgHYHfaNIf4xqSd7aWEyG0cxIoYFMXe40sfUgyy16IHkHmcJU1WfzIcm2QsEmqubzNsfnCojNRYODK6dVpaP_ZK9nOx5mZH4aHN574geF11vMtdqdDEAaJSFtd0EJAZQUCXcXFDkzh2l9xGRafSgL_GzXCRr0HyX2E-u-euCgnQmAo1irs5TumIrb0SOHt5YUYhu-GRyI5kNrbKsS23SankQN6Yn5uT-QrzyN8zqPOoJn121z_sx8_QpHLV96YqU-ccaypTDrWjpkckMPQ3cHNvzbHqjwg-EKgTOw3MZe2_5duc281KBMvktnQQJUpmlrNs_t_g'
```

Sample response:
```
{
    "result": [
        {
            "first": {
                "accountData": {
                    "accountId": "880df321-3259-4778-9486-2accb1a2b840",
                    "accountInfo": {
                        "name": "493a514f-1f6d-467a-953e-e9efae418573",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "880df321-3259-4778-9486-2accb1a2b840"
                        }
                    },
                    "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
                    "balance": "0.00 of EUR",
                    "txDate": "2020-12-03T18:59:44.246Z",
                    "status": "PENDING"
                },
                "linearId": {
                    "externalId": null,
                    "id": "81fa04c0-1e3c-41f8-a11c-7f52805f0c9a"
                },
                "period": "P1M",
                "savingsEndDate": "2021-01-09T14:47:00Z",
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "savings"
            },
            "second": {
                "createdOn": "2020-12-03T18:10:49.907Z",
                "modifiedOn": "2020-12-03T18:10:49.907Z",
                "customerName": "Alice Smith",
                "contactNumber": "1234567890",
                "emailAddress": "alice.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7",
                        "name": "alice-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:10:49.907Z",
                            "modifiedOn": "2020-12-03T18:10:49.907Z",
                            "customerName": "Alice Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "alice.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
                        },
                        "id": 7
                    }
                ],
                "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
            }
        },
        {
            "first": {
                "accountData": {
                    "accountId": "045985c9-b6e7-47ca-ae3e-361e1e6b3eba",
                    "accountInfo": {
                        "name": "ce7a2ba0-fec8-4fe5-9638-63b1c5f6530c",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "045985c9-b6e7-47ca-ae3e-361e1e6b3eba"
                        }
                    },
                    "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
                    "balance": "10.00 of EUR",
                    "txDate": "2020-12-03T19:05:27.779Z",
                    "status": "ACTIVE"
                },
                "linearId": {
                    "externalId": null,
                    "id": "c736e3e0-cda2-4090-b899-2c358bb3ea78"
                },
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "loan"
            },
            "second": {
                "createdOn": "2020-12-03T18:10:49.907Z",
                "modifiedOn": "2020-12-03T18:10:49.907Z",
                "customerName": "Alice Smith",
                "contactNumber": "1234567890",
                "emailAddress": "alice.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7",
                        "name": "alice-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:10:49.907Z",
                            "modifiedOn": "2020-12-03T18:10:49.907Z",
                            "customerName": "Alice Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "alice.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
                        },
                        "id": 7
                    }
                ],
                "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
            }
        },
        {
            "first": {
                "accountData": {
                    "accountId": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82",
                    "accountInfo": {
                        "name": "e2c9bc1e-fed4-4ebb-bbd1-eb84b86551d6",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
                        }
                    },
                    "customerId": "34b439bf-5ec9-4788-b384-012e33a11845",
                    "balance": "10.00 of EUR",
                    "txDate": "2020-12-03T19:05:27.709Z",
                    "status": "ACTIVE"
                },
                "approvedOverdraftLimit": 200,
                "linearId": {
                    "externalId": null,
                    "id": "20cc3fbb-ba68-4ac6-856e-dda2159bcd82"
                },
                "overdraftBalance": 0,
                "transferDailyLimit": 500,
                "withdrawalDailyLimit": 500,
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "current"
            },
            "second": {
                "createdOn": "2020-12-03T18:10:49.907Z",
                "modifiedOn": "2020-12-03T18:10:49.907Z",
                "customerName": "Alice Smith",
                "contactNumber": "1234567890",
                "emailAddress": "alice.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7",
                        "name": "alice-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:10:49.907Z",
                            "modifiedOn": "2020-12-03T18:10:49.907Z",
                            "customerName": "Alice Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "alice.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
                        },
                        "id": 7
                    }
                ],
                "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
            }
        },
        {
            "first": {
                "accountData": {
                    "accountId": "9f490e5b-d789-47d2-a55d-91bfd940de5f",
                    "accountInfo": {
                        "name": "e8ec2ff6-568a-4762-b59f-9807e544202c",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "9f490e5b-d789-47d2-a55d-91bfd940de5f"
                        }
                    },
                    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3",
                    "balance": "0.00 of EUR",
                    "txDate": "2020-12-03T19:19:09.793Z",
                    "status": "PENDING"
                },
                "approvedOverdraftLimit": null,
                "linearId": {
                    "externalId": null,
                    "id": "9f490e5b-d789-47d2-a55d-91bfd940de5f"
                },
                "overdraftBalance": null,
                "transferDailyLimit": null,
                "withdrawalDailyLimit": null,
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "current"
            },
            "second": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T18:42:10.902Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
                        "name": "josh-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:42:10.902Z",
                            "modifiedOn": "2020-12-03T18:42:10.902Z",
                            "customerName": "Josh Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "josh.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
                        },
                        "id": 8
                    }
                ],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            }
        },
        {
            "first": {
                "accountData": {
                    "accountId": "5f7a3fc0-02b7-478c-964f-b05c7fe8f28f",
                    "accountInfo": {
                        "name": "0a711324-489d-43d2-887a-ae1f8ce1e96e",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "5f7a3fc0-02b7-478c-964f-b05c7fe8f28f"
                        }
                    },
                    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3",
                    "balance": "0.00 of EUR",
                    "txDate": "2020-12-03T19:20:06.191Z",
                    "status": "PENDING"
                },
                "linearId": {
                    "externalId": null,
                    "id": "f9dbbf19-de79-4505-8480-ad336237286b"
                },
                "period": "P1M",
                "savingsEndDate": "2021-01-09T14:47:00Z",
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "savings"
            },
            "second": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T18:42:10.902Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
                        "name": "josh-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:42:10.902Z",
                            "modifiedOn": "2020-12-03T18:42:10.902Z",
                            "customerName": "Josh Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "josh.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
                        },
                        "id": 8
                    }
                ],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            }
        }
    ],
    "totalResults": 5,
    "pageSize": 100,
    "pageNumber": 1,
    "totalPages": 1
}
```


### Get accounts for a specific customer ID

Send a `GET` request to the `/accounts/customer/{customerId}` endpoint to invoke the [`GetAccountsForCustomerPaginatedFlow`](back-end-guide.md#getaccountsforcustomerpaginatedflow). The `GetAccountsForCustomerPaginatedFlow` displays a list of accounts for the given customer ID. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/accounts/customer/{customerId}`.

{{< table >}}
| Param        | Description                                      | Type   | Required |
| ------------ | ------------------------------------------------ | ------ | -------- |
| `startPage`  | Position of the start page to return.            | int    | No       |
| `pageSize`   | The maximum number of results in a page.         | int    | No       |
| `sortField`  | Sort results by `username` or `email`.           | string | No       |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`)              | string | No       |
| `searchTerm` | Term to partially match against multiple fields. | string | No       |
| `dateFrom`   | Filter accounts with `txDate` after this date.   | string | No       |
| `dateTo`     | Filter accounts with `txDate` before this date.  | string | No       |
{{< /table >}}

Response: This request returns a paginated response with the account information and customer information of all accounts matching the customer ID and given search criteria. - `PaginatedResponse<Pair<Account, CustomerSchemaV1.Customer>>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/accounts/customer/0cd7363b-66f7-4064-a8c8-527ce1eba8f3' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMzQxMSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMWYwYmU2ZWItZjAxZi00M2FmLWI0YWEtYWJlMjk1MGFlNTM1IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.orXLAHjySCi28I-MgHYHfaNIf4xqSd7aWEyG0cxIoYFMXe40sfUgyy16IHkHmcJU1WfzIcm2QsEmqubzNsfnCojNRYODK6dVpaP_ZK9nOx5mZH4aHN574geF11vMtdqdDEAaJSFtd0EJAZQUCXcXFDkzh2l9xGRafSgL_GzXCRr0HyX2E-u-euCgnQmAo1irs5TumIrb0SOHt5YUYhu-GRyI5kNrbKsS23SankQN6Yn5uT-QrzyN8zqPOoJn121z_sx8_QpHLV96YqU-ccaypTDrWjpkckMPQ3cHNvzbHqjwg-EKgTOw3MZe2_5duc281KBMvktnQQJUpmlrNs_t_g'
```

Sample response:
```
{
    "result": [
        {
            "first": {
                "accountData": {
                    "accountId": "9f490e5b-d789-47d2-a55d-91bfd940de5f",
                    "accountInfo": {
                        "name": "e8ec2ff6-568a-4762-b59f-9807e544202c",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "9f490e5b-d789-47d2-a55d-91bfd940de5f"
                        }
                    },
                    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3",
                    "balance": "0.00 of EUR",
                    "txDate": "2020-12-03T19:19:09.793Z",
                    "status": "PENDING"
                },
                "approvedOverdraftLimit": null,
                "linearId": {
                    "externalId": null,
                    "id": "9f490e5b-d789-47d2-a55d-91bfd940de5f"
                },
                "overdraftBalance": null,
                "transferDailyLimit": null,
                "withdrawalDailyLimit": null,
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "current"
            },
            "second": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T18:42:10.902Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
                        "name": "josh-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:42:10.902Z",
                            "modifiedOn": "2020-12-03T18:42:10.902Z",
                            "customerName": "Josh Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "josh.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
                        },
                        "id": 8
                    }
                ],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            }
        },
        {
            "first": {
                "accountData": {
                    "accountId": "5f7a3fc0-02b7-478c-964f-b05c7fe8f28f",
                    "accountInfo": {
                        "name": "0a711324-489d-43d2-887a-ae1f8ce1e96e",
                        "host": "O=Bank, L=London, C=GB",
                        "identifier": {
                            "externalId": null,
                            "id": "5f7a3fc0-02b7-478c-964f-b05c7fe8f28f"
                        }
                    },
                    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3",
                    "balance": "0.00 of EUR",
                    "txDate": "2020-12-03T19:20:06.191Z",
                    "status": "PENDING"
                },
                "linearId": {
                    "externalId": null,
                    "id": "f9dbbf19-de79-4505-8480-ad336237286b"
                },
                "period": "P1M",
                "savingsEndDate": "2021-01-09T14:47:00Z",
                "participants": [
                    "O=Bank, L=London, C=GB"
                ],
                "type": "savings"
            },
            "second": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T18:42:10.902Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith@email.com",
                "postCode": "12345",
                "attachments": [
                    {
                        "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
                        "name": "josh-smith-attachment.zip",
                        "customer": {
                            "createdOn": "2020-12-03T18:42:10.902Z",
                            "modifiedOn": "2020-12-03T18:42:10.902Z",
                            "customerName": "Josh Smith",
                            "contactNumber": "1234567890",
                            "emailAddress": "josh.smith@email.com",
                            "postCode": "12345",
                            "attachments": [],
                            "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
                        },
                        "id": 8
                    }
                ],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            }
        }
    ],
    "totalResults": 2,
    "pageSize": 100,
    "pageNumber": 1,
    "totalPages": 1
}
```


## Customer Controller

The Customer Controller includes API endpoints that handle customer tasks for Bank in a Box. Requests sent to these endpoints allow users to upload attachments, create customer profiles, return lists of customers matching given search parameters, and update customer profiles.


### Upload an attachment

Send a `POST` request to the `/customers/upload-attachment` endpoint to upload an attachment that will later be used to create a customer profile. This attachment mimics a user identity verification and application process. These documents should be contained in a unique jar or zip file. The contents of the file do not matter, as long as they are unique when compared to other customer attachments. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/customers/upload-attachment`.

{{< table >}}
| Param      | Description                       | Type   | Required |
| ---------- | --------------------------------- | ------ | -------- |
| `file`     | `.zip` or `.jar` file attachment. | string | Yes      |
| `uploader` | Name of the uploader.             | string | Yes      |
{{< /table >}}

Response: This request returns a `String` secure hash of the attachment (`JSON: {"secureHash": "$hash"`).

Sample request:
```
curl --location --request POST 'http://localhost:7777/customers/upload-attachment?uploader=admin' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAxODY2NSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiYzUwNWYyOWItNmU5ZS00ODAzLTk4MmItMjA5MzUwOTY2YmYwIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.Ef5rGwCw7RswzLFc98K87Qg0TnWaFo-kjLRjN5B0gF59-soY0whv7puhq3iwacolAqhym1WWN7mjjv-hu-gJlgFRyiGY1F4ys2iI2Yv3u44Ax54_mhfvHVNVRoPoysYXAjt11BCgs80uPDhwPuCxwqyG57ek0mWyWnO3PnV54LZZgHGaC_Hr7ZsJKTdwxLwabU31YMqf86pofXbhaE_vTQF61NnTbC5iui_pU39KzWu5TiAx8Z2II09Rkucb-KA5X3DxcWjnnYc1UbAMVuoIgP29RHhJJLPuSjZC0qarNoP7s3cu_MKdtiye3xY7D_8v-X7x1gP-eku06Tzb2ITjpQ' \
--form 'file=@"/Users/Admin/Documents/alice-smith-attachment.zip"'
```

Sample response:
```
{
    "secureHash": "DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7"
}
```


### Create a customer

Send a `POST` request to the `/customers/create` endpoint to invoke the [`CreateCustomerFlow`](back-end-guide.md#createcustomerflow). This flow creates a customer profile that includes personal details and contact information, and returns the customer ID. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/customers/create`.

{{< table >}}
| Param           | Description                                                                                                              | Type   | Required |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | ------ | -------- |
| `customerName`  | The new customer's name.                                                                                                 | string | Yes      |
| `contactNumber` | The new customer's phone number.                                                                                         | int    | Yes      |
| `emailAddress`  | The new customer's email address.                                                                                        | string | Yes      |
| `postCode`      | The post code of the new customer's address.                                                                             | int    | Yes      |
| `attachments`   | A list of attachments containing the supporting documentation for the customer (attachment hash, attachment name pairs). | string | yes      |
{{< /table >}}

The `attachments` parameter is composed of the secure hash returned when an [attachment is uploaded](#upload-an-attachment) and the name of the attachment file, separated by a colon. In the sample below, this is: `alice-smith-attachment.zip:DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7`.

Response: This request returns a `String` customer ID for the created customer profile.

Sample request:
 ```
 curl --location --request POST 'http://localhost:7777/customers/create?customerName=Alice%20Smith&contactNumber=1234567890&emailAddress=alice.smith@email.com&postCode=12345&attachments=alice-smith-attachment.zip:DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAxOTkzMywiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZGU5NGRmNmItN2YwMi00NTFlLTljMjItY2E5MDEzZDQzYTA4IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.Vd9RPhZoSfgglqsZHtX1HwCmv7AuHZjM9zKvabjjCNf2sEMAZ1ZlLL9dnUvMgYT2XO9Z1GqDP7q8W9A0XojrrmPR-dGJgcxvyBi7Huv9nwvdztLwqtge6p78SCgTb47FD76vhcRQPC7dxXVvnNKDvunWe2Jv8wefbuMOloc3RFNSFR5erAOw3XkuGXQ6MnpGVfQv5CqAC53fm_MBQTN35l0s4vWW1r-xi5oE0wlv7bZYaiID3zGIREyB4YQvsI_kVqPASTJy344NnZWrcf8Cy6fenElkT7bez6Mh83-cazvY-gJero14tjcd5Q2_NDH15iCKszqFmCWwPB3pwhGgQw'
 ```

Sample response:
```
{
    "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
}
```


### Get customers

Send a `GET` request to the `/customers` endpoint to invoke the [`GetCustomersPaginatedFlow`](back-end-guide.md#getcustomerspaginatedflow). This flow returns a paginated list of all customers matching the given search crtieria. This request requires authorization. It can be sent by an admin user.

 - Request type: `GET`.
 - Path: `/customers`.

{{< table >}}
| Param        | Description                                      | Type   | Required |
| ------------ | ------------------------------------------------ | ------ | -------- |
| `startPage`  | Position of the start page to return.            | int    | No       |
| `pageSize`   | The maximum number of results in a page.         | int    | No       |
| `sortField`  | Sort results by `username` or `email`.           | string | No       |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`)              | string | No       |
| `searchTerm` | Term to partially match against multiple fields. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing customers matching the given search criteria - `PaginatedResponse<CustomerSchemaV1.Customer>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/customers' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyMTQ2MywiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiYzRmZThkNzctZDU4Yy00Mjc2LTg1NzYtNzMxMzdmYTY1Y2Y2IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.fOU2h8FeQuE1fRew2sN8DT3CG9dvpBVD1R5GdKy0_jzPGiFNflgAuBw3ANzZn0Z8KwEti-xwoVFGpjpOxH2mh48nu5hfTw0C_V4qdRfW0oNOYaMRh4qxZpjs6BW6WmU-hnuVxdZyb-oIYKqUJujzyF83a2gJXAMv9UQj2uW4gbVmbTbU-vu0hyUoTkdP1jSfX0kuhZXjn-SArbwI1vxBUe1vHX2Vqk1wZ43fQo3ixCIGJLNu2jXeHZn-15Oh739ZQWZ8Mpu_zYD-oHzyavA0yrPPvuc5SPFqJ2Kw2Jyj6P3sc3SMCr4aALbb1eiNkcoxPZo2Gri8Z0RWHXXfvdrsnA'
```

Sample response:
```
{
    "result": [
        {
            "createdOn": "2020-12-03T18:10:49.907Z",
            "modifiedOn": "2020-12-03T18:10:49.907Z",
            "customerName": "Alice Smith",
            "contactNumber": "1234567890",
            "emailAddress": "alice.smith@email.com",
            "postCode": "12345",
            "attachments": [
                {
                    "attachmentHash": "DCD5148BEDB42510D15BFA971D845CC3FC18932E5ECFB13158364A1487E2B7F7",
                    "name": "alice-smith-attachment.zip",
                    "customer": {
                        "createdOn": "2020-12-03T18:10:49.907Z",
                        "modifiedOn": "2020-12-03T18:10:49.907Z",
                        "customerName": "Alice Smith",
                        "contactNumber": "1234567890",
                        "emailAddress": "alice.smith@email.com",
                        "postCode": "12345",
                        "attachments": [],
                        "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
                    },
                    "id": 7
                }
            ],
            "customerId": "34b439bf-5ec9-4788-b384-012e33a11845"
        },
        {
            "createdOn": "2020-12-03T18:42:10.902Z",
            "modifiedOn": "2020-12-03T18:42:10.902Z",
            "customerName": "Josh Smith",
            "contactNumber": "1234567890",
            "emailAddress": "josh.smith@email.com",
            "postCode": "12345",
            "attachments": [
                {
                    "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
                    "name": "josh-smith-attachment.zip",
                    "customer": {
                        "createdOn": "2020-12-03T18:42:10.902Z",
                        "modifiedOn": "2020-12-03T18:42:10.902Z",
                        "customerName": "Josh Smith",
                        "contactNumber": "1234567890",
                        "emailAddress": "josh.smith@email.com",
                        "postCode": "12345",
                        "attachments": [],
                        "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
                    },
                    "id": 8
                }
            ],
            "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
        }
    ],
    "totalResults": 2,
    "pageSize": 100,
    "pageNumber": 1,
    "totalPages": 1
}
```

### Get customer by customer ID

Send a `GET` request to the `/customers/{customerId}` endpoint to invoke the [`GetCustomerByIdFlow`](back-end-guide.md#getcustomerbyidflow). This flow retrieves the `CustomerSchemaV1.Customer`, which stores personal details and contact information along with creation and modification timestamps, for a given `customerId`. This request requires authorization. It can be sent by an admin user.

 - Request type: `GET`.
 - Path: `/customers/{customerId}`.

Response: This request returns the customer profile information for the specified customer ID - `CustomerSchemaV1.Customer`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/customers/0cd7363b-66f7-4064-a8c8-527ce1eba8f3' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyNDgxNCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiY2Q0NzE1ZTUtOTVmMS00NTllLTg3NDItMDZiNDQ2MTNlNmYxIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.galmmVFpqrzy-HiwaFq1uvSaR8h7v_TsVu1u2gcv_oekk8S3Be0Qc-gJe12ZsnITvk3qFj5sSmunHOj3RWMASqFC8nBCsLOYHE9WlQDH4qrsnGpfhAoGR0OLUWkoiIJebKkD8oujn9SVxQ0JIGhvTFcpoATi53UOvI27xKWzw9lpz6G_3Giovl9Dy22cFP2eulAAhPwNFD--YFUubuR9k26IT0hKLIGiWob71ASv6Fo9tK7u1WPvajmcf47ywsCc88HW8K4aqXtLle9MWX5qZ13EotwKlj-t1WxK0fYXpoBoH1F7Nxof8KClpZvQvpyT51IPYSUWRz84Ns3hcG9nJQ'
```

Sample response:
```
{
    "createdOn": "2020-12-03T18:42:10.902Z",
    "modifiedOn": "2020-12-03T18:42:10.902Z",
    "customerName": "Josh Smith",
    "contactNumber": "1234567890",
    "emailAddress": "josh.smith@email.com",
    "postCode": "12345",
    "attachments": [
        {
            "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
            "name": "josh-smith-attachment.zip",
            "customer": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T18:42:10.902Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith@email.com",
                "postCode": "12345",
                "attachments": [],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            },
            "id": 8
        }
    ],
    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
}
```


### Get customer name for account ID

Send a `GET` request to the `/customers/name/{accountId}` endpoint to return a customer's name when searching by an account ID. This request requires authorization. It can be sent by an admin user.

 - Request type: `GET`.
 - Path: `/customers/name/{accountId}`.

Response: This request returns the account owner's customer name for the specified account ID - `CustomerNameResponse`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/customers/name/20cc3fbb-ba68-4ac6-856e-dda2159bcd82' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyNDgxNCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiY2Q0NzE1ZTUtOTVmMS00NTllLTg3NDItMDZiNDQ2MTNlNmYxIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.galmmVFpqrzy-HiwaFq1uvSaR8h7v_TsVu1u2gcv_oekk8S3Be0Qc-gJe12ZsnITvk3qFj5sSmunHOj3RWMASqFC8nBCsLOYHE9WlQDH4qrsnGpfhAoGR0OLUWkoiIJebKkD8oujn9SVxQ0JIGhvTFcpoATi53UOvI27xKWzw9lpz6G_3Giovl9Dy22cFP2eulAAhPwNFD--YFUubuR9k26IT0hKLIGiWob71ASv6Fo9tK7u1WPvajmcf47ywsCc88HW8K4aqXtLle9MWX5qZ13EotwKlj-t1WxK0fYXpoBoH1F7Nxof8KClpZvQvpyT51IPYSUWRz84Ns3hcG9nJQ'
```

Sample response:
```
{
    "customerName": "Alice Smith"
}
```


### Update customer

Send a `PUT` request to the `/customers/update/{customerId}` endpoint to invoke the [`UpdateCustomerFlow`](back-end-guide.md#updatecustomerflow). This flow adds personal details and contact information, and returns the customer ID. This request requires authorization. It can be sent by an admin user or the customer user.

- Request type: `PUT`.
- Path: `/customers/update/{customerId}`.

{{< table >}}
| Param           | Description                                                                                         | Type   | Required |
| --------------- | --------------------------------------------------------------------------------------------------- | ------ | -------- |
| `contactNumber` | The customer's new phone number.                                                                    | int    | No       |
| `emailAddress`  | The customer's new email address.                                                                   | string | No       |
| `attachments`   | A list of attachments to append to the customer's profile (attachment hash, attachment name pairs). | string | No       |
{{< /table >}}

The customer will only be able to update the `contactNumber` and `emailAddress` parameters.

Response: The updated customer information of the specified customer ID is returned - `CustomerSchemaV1.Customer`.

Sample request:
```
curl --location --request PUT 'http://localhost:7777/customers/update/0cd7363b-66f7-4064-a8c8-527ce1eba8f3?emailAddress=josh.smith1@email.com' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzAyNDgxNCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiY2Q0NzE1ZTUtOTVmMS00NTllLTg3NDItMDZiNDQ2MTNlNmYxIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.galmmVFpqrzy-HiwaFq1uvSaR8h7v_TsVu1u2gcv_oekk8S3Be0Qc-gJe12ZsnITvk3qFj5sSmunHOj3RWMASqFC8nBCsLOYHE9WlQDH4qrsnGpfhAoGR0OLUWkoiIJebKkD8oujn9SVxQ0JIGhvTFcpoATi53UOvI27xKWzw9lpz6G_3Giovl9Dy22cFP2eulAAhPwNFD--YFUubuR9k26IT0hKLIGiWob71ASv6Fo9tK7u1WPvajmcf47ywsCc88HW8K4aqXtLle9MWX5qZ13EotwKlj-t1WxK0fYXpoBoH1F7Nxof8KClpZvQvpyT51IPYSUWRz84Ns3hcG9nJQ'
```

Sample response:
```
{
    "createdOn": "2020-12-03T18:42:10.902Z",
    "modifiedOn": "2020-12-03T19:40:11.981Z",
    "customerName": "Josh Smith",
    "contactNumber": "1234567890",
    "emailAddress": "josh.smith1@email.com",
    "postCode": "12345",
    "attachments": [
        {
            "attachmentHash": "12C1F444A083E0AC48CBEF49BD4A11D6929F047CF2513097AF1279268E08AB94",
            "name": "josh-smith-attachment.zip",
            "customer": {
                "createdOn": "2020-12-03T18:42:10.902Z",
                "modifiedOn": "2020-12-03T19:40:11.981Z",
                "customerName": "Josh Smith",
                "contactNumber": "1234567890",
                "emailAddress": "josh.smith1@email.com",
                "postCode": "12345",
                "attachments": [],
                "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
            },
            "id": 8
        }
    ],
    "customerId": "0cd7363b-66f7-4064-a8c8-527ce1eba8f3"
}
```


## Payments Controller

The Payments Controller includes API endpoints that manage payments in Bank in a Box. Requests sent to these endpoints allow customer users to withdraw money, deposit money, make an intrabank payment, create a recurring payment, and cancel a recurring payment.

### Withdraw money

Send a `POST` request to the `/payments/withdraw-fiat` endpoint to invoke the [`WithdrawFiatFlow`](back-end-guide.md#withdrawfiatflow). The `WithdrawFiatFlow` withdraws a specified amount from an account with the provided account ID. This request requires authorization. It can be sent by an admin user.

 - Request type: `POST`.
 - Path: `/payments/withdraw-fiat`.

{{< table >}}
| Param       | Description                                           | Type   | Required |
| ----------- | ----------------------------------------------------- | ------ | -------- |
| `accountId` | ID of the account from which money will be withdrawn. | string | Yes      |
| `tokenType` | The currency of the withdrawal (for example, `EUR`.)  | string | Yes      |
| `amount`    | The amount of money being withdrawn, in the base unit of the assigned currency.                  | int    | Yes      |
{{< /table >}}

Response: This request returns the account information for the specified account ID with the updated balance. See the `balance` field in the sample response below.

Sample request:
```
curl --location --request POST 'http://localhost:7777/payments/withdraw-fiat?accountId=56e3fe14-7062-4b5e-8563-4df32cbb4485&tokenType=EUR&amount=1000' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzI3MjM5MCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiMjljOWI3YzItOWJlZS00YzgzLWIyODMtNmQyN2U1OGU2MzNiIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.rpy3T3u0kuvor8KRqAm4atBa81kF_NWCy7hkxMeQ0UMOGYCBlIXY90guY7jorHlop5b83iKZxEUi0L3lTyGgdPKLZIEp92yodBNhlzG2lODC56zn5ivv_oBPVkaGYROKVES5Bu6Rud0N8j2-dtoHTAi7S5h1u7qqOZXX6TgtvNwYXD6mUryPINkQs86yvMqV_7cPbTJnBm3XyyOMEBSjkdQ_wtXWZH_AKBJVbdyAqsg5AJ8u9KNyrNfJFupJew5X7JCannttkNNyJMBGJaQCj3MCMC7XKPUX_NIUXLy8iiIE-sFiLTbVGrEc9cVgXkpA5U8OTjWNqpaoV0V4XwtIXA'
```

Sample response:
```
{
    "accountData": {
        "accountId": "56e3fe14-7062-4b5e-8563-4df32cbb4485",
        "accountInfo": {
            "name": "5122b607-85d4-4e0f-89ea-1ca221113a46",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "56e3fe14-7062-4b5e-8563-4df32cbb4485"
            }
        },
        "customerId": "0e1cd5f8-e2a6-4d29-9e69-abc8c27a8d5a",
        "balance": "4090.00 of EUR",
        "txDate": "2020-12-06T16:19:40.357Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": null,
    "linearId": {
        "externalId": null,
        "id": "56e3fe14-7062-4b5e-8563-4df32cbb4485"
    },
    "overdraftBalance": null,
    "transferDailyLimit": null,
    "withdrawalDailyLimit": null,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Deposit money

Send a `POST` request to the `/payments/deposit-fiat` endpoint to invoke the [`DepositFiatFlow`](back-end-guide.md#depositfiatflow). The `DepositFiatFlow` is used to deposit a specified amount to an account with the provided account ID. This request requires authorization. It can be sent by an admin user.

- Request type: `POST`.
- Path: `/payments/deposit-fiat`.

{{< table >}}
| Param       | Description                                       | Type   | Required |
| ----------- | ------------------------------------------------- | ------ | -------- |
| `accountId` | ID of the account where money will be deposited.  | string | Yes      |
| `tokenType` | The currency of the deposit (for example, `EUR`.) | string | Yes      |
| `amount`    | The amount of money being deposited, in the base unit of the assigned currency.             | int    | Yes      |
{{< /table >}}

{{< note >}}
The deposit must have the same `tokenType` as the account. For example - if an account has a `tokenType` of `EUR`, the admin user will not be able to make a deposit in `USD`.
{{< /note >}}

Response: This request returns the account information for the specified account ID with the updated balance. See the `balance` field in the sample response below.

Sample request:
```
curl --location --request POST 'http://localhost:7777/payments/deposit-fiat?accountId=56e3fe14-7062-4b5e-8563-4df32cbb4485&tokenType=EUR&amount=10000' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzI3MTMyMywiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNjFlMGExOGQtNzU1Ni00NGI0LTk0NDYtYThlOWJhYzU2NGNhIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.w16b6QJjAbioxLxRi3ePiyiCe4MB-YUNdLnjHN7X61-WUbkTCuoau0HYdpPJ2u-yksAHSh7i6AZWp7kelDdNkSWpiAELEk8gZATcKAU-hrCyRQitVWoiPL16MKHzeNj-3gFi7H5UGdlbzxABoTwzeroRM-LyHuLZnnnFtcf-0iv5wXGyquU9AmR0CD-hmqgukSiAk1V6izss5CDLe7ypnnpE15PqYimqSXfoMp-B8U1AkoY3iIJn6emLyC2rF7VgC27UPu0zewH1GfV95ggm7jtOswe-gj5swUUKBRZoGtYlttxkl6HRcTfkRCzPLUAFSNHwyl3Tx_qKzv8TCgmLzg'
```

Sample response:
```
{
    "accountData": {
        "accountId": "56e3fe14-7062-4b5e-8563-4df32cbb4485",
        "accountInfo": {
            "name": "5122b607-85d4-4e0f-89ea-1ca221113a46",
            "host": "O=Bank, L=London, C=GB",
            "identifier": {
                "externalId": null,
                "id": "56e3fe14-7062-4b5e-8563-4df32cbb4485"
            }
        },
        "customerId": "0e1cd5f8-e2a6-4d29-9e69-abc8c27a8d5a",
        "balance": "100.00 of EUR",
        "txDate": "2020-12-06T16:00:40.912Z",
        "status": "ACTIVE"
    },
    "approvedOverdraftLimit": null,
    "linearId": {
        "externalId": null,
        "id": "56e3fe14-7062-4b5e-8563-4df32cbb4485"
    },
    "overdraftBalance": null,
    "transferDailyLimit": null,
    "withdrawalDailyLimit": null,
    "participants": [
        "O=Bank, L=London, C=GB"
    ],
    "type": "current"
}
```


### Make an intrabank payment

Send a `POST` request to the `/payments/intrabank-payment` endpoint to invoke the [`IntrabankPaymentFlow`](back-end-guide.md#intrabankpaymentflow). The `IntrabankPaymentFlow` is used to transfer a specified amount of money from a current account to another account. It can be sent by a customer user.

This request can only be performed by the customer who owns the `fromAccount`. This requires authorization from a **customer** bearer token. Use a customer's [Bank in a Box username](#register-a-user-account) to [request a token](#authentication) for this request.

- Request type: `POST`.
- Path: `/payments/intrabank-payment`.

{{< table >}}
| Param           | Description                                             | Type   | Required |
| --------------- | ------------------------------------------------------- | ------ | -------- |
| `fromaccountId` | ID of the account from which money will be transferred. | string | Yes      |
| `toAccountId`   | ID of the account to which money will be transferred.   | string | Yes      |
| `tokenType`     | The currency of the payment (for example, `EUR`.)       | string | Yes      |
| `amount`        | The amount of money being transferred, in the base unit of the assigned currency.                  | int    | Yes      |
{{< /table >}}

{{< note >}}
Accounts involved in an intrabank transfer must have the same `tokenType`. The intrabank payment `tokenType` must also be the same.
{{< /note >}}

Response: This request returns a reference to the current account the funds were transferred from and the account the funds were transferred to - `IntrabankPaymentResponse`.

Sample request:
```
curl --location --request POST 'http://localhost:7777/payments/intrabank-payment?fromAccountId=378774a1-d18a-4b00-84f0-3e58b34091fa&toAccountId=bde1c40a-cf68-4311-b972-56e155497f8b&tokenType=EUR&amount=1000' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFsaWNlLnNtaXRoMSIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJjdXN0b21lcklkIjoiNTA0ODBhZDctYjcwYS00NTc5LTkzMWUtMGQ4NzMwZTM2NmU5IiwiZXhwIjoxNjA3MzM2ODcwLCJhdXRob3JpdGllcyI6WyJHVUVTVCIsIkNVU1RPTUVSIl0sImp0aSI6IjJmYjlmN2Y5LTQ0OTUtNGZkZS04YmViLWYwNzc3ZDRlMzA1MiIsImNsaWVudF9pZCI6ImJhbmtfaW5fYV9ib3hfYXBwIn0.WcIMDX2HgqkMzSRfRyVAUKP_Pxk5ON5SdXpRgXjQDbS1XUg9BELc8bX3-gljUhEyYuO5l7lyCq7I5bPXAafsSRtESssI1zUfBhaM_E8GSgj9o75JwOd8wTE9vI59VlKOwONnuAAb_vdJsJbqPO7nNumEmwfElU2SwwdsV9d5Z1hLXNulMsY2coSO-bUe_o3OMdPpGBVp1_EN7_FVx26lMTYGmFAh7FrGR71K0oSPJP5ULkozmW6ilUb1Ucoo3NDit0pOIyH90RFH-BK_MjeSadMLFO4Iyo8SYwRufmHiWepHqRl92Yxx6DP-LzGFup9fEzeHKhQNXoujb_ATIUSKtw'
```

Sample response:
```
{
    "fromAccount": {
        "accountData": {
            "accountId": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountInfo": {
                "name": "c9715144-0535-4e64-acdd-14a6eb81039f",
                "host": "O=Bank, L=London, C=GB",
                "identifier": {
                    "externalId": null,
                    "id": "378774a1-d18a-4b00-84f0-3e58b34091fa"
                }
            },
            "customerId": "50480ad7-b70a-4579-931e-0d8730e366e9",
            "balance": "1990.00 of EUR",
            "txDate": "2020-12-07T10:13:44.846Z",
            "status": "ACTIVE"
        },
        "approvedOverdraftLimit": null,
        "linearId": {
            "externalId": null,
            "id": "378774a1-d18a-4b00-84f0-3e58b34091fa"
        },
        "overdraftBalance": null,
        "transferDailyLimit": null,
        "withdrawalDailyLimit": null,
        "participants": [
            "O=Bank, L=London, C=GB"
        ],
        "type": "current"
    },
    "toAccountId": "bde1c40a-cf68-4311-b972-56e155497f8b",
    "toAccountCustomerId": "3b46262b-8aa0-45fc-a4d7-3aa629e29a52",
    "toAccountCustomerName": "Dan Allen"
}
```


### Create a recurring payment

Send a `POST` request to the `/payments/create-recurring-payment` endpoint to invoke the [`CreateRecurringPaymentFlow`](back-end-guide.md#createrecurringpaymentflow). The `CreateRecurringPaymentFlow` creates a recurring payment for the specified amount of money to be transferred from a current account to another account. It can be sent by a customer user.

This request can only be performed by the customer who owns the `fromAccount`. This requires authorization from a **customer** bearer token. Use a customer's [Bank in a Box username](#register-a-user-account) to [request a token](#authentication) for this request.

- Request type: `POST`.
- Path: `/payments/create-recurring-payment`.

{{< table >}}
| Param           | Description                                             | Type   | Required |
| --------------- | ------------------------------------------------------- | ------ | -------- |
| `fromaccountId` | ID of the account from which money will be transferred. | string | Yes      |
| `toAccountId`   | ID of the account to which money will be transferred.   | string | Yes      |
| `tokenType`     | The currency of the payment (for example, `EUR`.)       | string | Yes      |
| `amount`        | The amount of money being transferred, in the base unit of the assigned currency.                | int    | Yes      |
| `dateStart`     | Start date of the recurring payment                     | string | Yes      |
| `period`        | Duration of the payment period.                         | string | Yes      |
| `iterationNum`  | Number of payment iterations.                           | int    | No       |
{{< /table >}}

{{< note >}}
The `period` between payments is serialized as `java.util.Duration`. If the `period` is set to `P30D`, the recurring payment will start 30 days after the start date (`dateStart`). The sample request below sets the `period` to  `PT1M`, so that the recurring payment would start 1 minute after the start date.
{{< /note >}}

Response: This request returns information on the newly-created recurring payment - `RecurringPaymentState`.

Sample request:
```
curl --location --request POST 'http://localhost:7777/payments/create-recurring-payment?fromAccountId=0129dd07-2582-4458-948a-aa7de548d083&toAccountId=378774a1-d18a-4b00-84f0-3e58b34091fa&tokenType=EUR&amount=3000&dateStart=2020-12-07T16:15:42.974Z&period=PT1M&iterationNum=10' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImRhbi5hbGxlbiIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJjdXN0b21lcklkIjoiM2I0NjI2MmItOGFhMC00NWZjLWE0ZDctM2FhNjI5ZTI5YTUyIiwiZXhwIjoxNjA3MzU4MTY4LCJhdXRob3JpdGllcyI6WyJHVUVTVCIsIkNVU1RPTUVSIl0sImp0aSI6IjI1ZmZiYzEyLWQ5MTctNDYyZC1hZDVhLTVlMDVhYjdlZjJjNSIsImNsaWVudF9pZCI6ImJhbmtfaW5fYV9ib3hfYXBwIn0.vuxu3jYhoUhYTSFk5WX_RR537UT8dQfbnuAQ11bGrYVFU1-znA4KqIgP9fvHO_wcEIyQEWSqz6vditYcyrhk6sCiUVe2XIGZb3hgYMGiHK1Z656h1WcHjG0ww8d10mPQ6AW_HdCRTjfEgDAI4YFKemzxtdORYnW3LnAgHwsmXPp4Dncr2SGKXttr3mMB_Zm_kZfZqlcAmyjb6wT16qQfG_P9zxQBPT90C8himNFtTu37P92UqrYkts9HFP6J34hMQfaNUpTzsrsPNkYD_7zs1CZ70SRQtlbguw3rCMedVCCTxyauEQICLk_9WtHmyDw1D_WDk6kS6beqSUe8Wa9fNw'
```

Sample response:
```
{
    "accountFrom": "0129dd07-2582-4458-948a-aa7de548d083",
    "accountTo": "378774a1-d18a-4b00-84f0-3e58b34091fa",
    "amount": "30.00 EUR",
    "dateStart": "2020-12-07T16:15:42.974Z",
    "period": "PT1M",
    "iterationNum": 10,
    "owningParty": "O=Bank, L=London, C=GB",
    "linearId": {
        "externalId": null,
        "id": "47db70ef-9bb6-4541-b32d-4d9a96770097"
    }
}
```

### Cancel recurring payment

Send a `POST` request to the `/payments/cancel-recurring-payment` endpoint to invoke the [`CancelRecurringPaymentFlow`](back-end-guide.md#cancelrecurringpaymentflow). The `CancelRecurringPaymentFlow` cancels a recurring payment specified by its recurring payment ID. It can be sent by an admin user or a customer user.

This request can only be performed by the customer who owns the `fromAccount`. This requires authorization from a **customer** bearer token. Use a customer's [Bank in a Box username](#register-a-user-account) to [request a token](#authentication) for this request.

{{< note >}}
Recurring payments for loans can only be cancelled by an admin user. An admin `access_token` must be used to authorize this specific type of request.
{{< /note >}}

- Request type: `POST`.
- Path: `/payments/cancel-recurring-payment`.

{{< table >}}
| Param                | Description                            | Type   | Required |
| -------------------- | -------------------------------------- | ------ | -------- |
| `recurringPaymentId` | ID of the recurring payment to cancel. | string | Yes      |
{{< /table >}}

Response: This request returns a message indicating that the recurring payment has been cancelled in the format of a `MessageResponse`, which wraps a message response from an endpoint.

Sample request:
```
curl --location --request POST 'http://localhost:7777/payments/cancel-recurring-payment?recurringPaymentId=637de768-97a7-4014-be42-f5d849b0969d' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImRhbi5hbGxlbiIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJjdXN0b21lcklkIjoiM2I0NjI2MmItOGFhMC00NWZjLWE0ZDctM2FhNjI5ZTI5YTUyIiwiZXhwIjoxNjA3MzM4MTE0LCJhdXRob3JpdGllcyI6WyJHVUVTVCIsIkNVU1RPTUVSIl0sImp0aSI6IjQyMWVlMmU1LTlmNTctNDg5MC1iNmExLTAwN2QxMGMyZGZiMyIsImNsaWVudF9pZCI6ImJhbmtfaW5fYV9ib3hfYXBwIn0.ugFUOip-Q2xNxw2V3ZIzhLzTybLXadIGVh7f74rX4FUvoi41ibFKphSRCsW1z4Sm2GjxP1nWZ1gGFw1oRsxlGW07u0idNZMZFe3dsXAXOgUDrgMp8HOFZ9WnB0agWv5BmQ9mEfp_gduZEBsYb9Lsbv89QoXyVXTrI2jNH00X5zVm1omvuRWBer1KhcETJ6r_p7eHYmdVz95yuRXVpjvB1rxnDx5p6VUUHay_9TWcpG57jyzAqyod5docHrHOyh6sYmllb1LeCZ126Zz99xTt64UOVc1mrmb5CdZ2ILn6_duRFN_9W_xfWg14rO22oVopXephQf9HAM0dCgOC7MA1KA'
```

Sample response:
```
Recurring payment 637de768-97a7-4014-be42-f5d849b0969d cancelled
```

## Recurring Payments Controller

The Recurring Payments Controller includes API endpoints that reference recurring payments in Bank in a Box. Requests sent to these endpoints return lists of existing recurring payments that match the given search parameters.

### Get recurring payment by ID

Send a `GET` request to the `/recurring-payments/{recurringPaymentId}` endpoint to invoke the [`GetRecurringPaymentByIdFlow`](back-end-guide.md#getrecurringpaymentsbyidflow). The `GetRecurringPaymentByIdFlow` returns information for a recurring payment, specified by its recurring payment ID. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/recurring-payments/{recurringPaymentId}`.

Response: This request returns a data transfer object that stores details of a recurring payment - `RecurringPaymentResponse`.

 Sample request:
 ```
 curl --location --request GET 'http://localhost:7777/recurring-payments/2cb772ff-8e5f-4c4a-8261-ea7ee1c2ef0e' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzMzOTAxNiwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiZTRmMDMxYzUtOTA0Yi00MjI5LThhNzctNjk0OTBhODAzZGYwIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.IC_sAE8Tv7Z9QnlfmRnL6PSj-dwZl4DKcEwIG2GLf6n3Vfej2skNCm_Q8gMaWKZVMDHmaOGgDHbGz8XXdePnMHjex_EvLc3iEJNN_dsoSBjEgeih3XzLng4vI4oQ4hzA0-Q8tQQ628HJenlsyalIgQJ5cptrsNaOkzdw0HK2LPZCnqkHZuwV8c26sdw6EwGx3yg_1AEJAt9qv90Dw5Qa2LiEMi5eQkjR9MNITvleKPfKdjJYEq84fnStAn2XWOkxcghMZ1FBZg_N38XlpIuIQImFD1XTEt7oTGv4J5jKoQLcFBEZyeOKvS0kkss3ChgutJP6N67LBur2m-7nni2ARw'
 ```

 Sample response:
 ```
 {
    "accountFrom": "bde1c40a-cf68-4311-b972-56e155497f8b",
    "accountTo": "378774a1-d18a-4b00-84f0-3e58b34091fa",
    "amount": 10000,
    "currencyCode": "EUR",
    "dateStart": "2020-12-08T09:09:42.974Z",
    "period": "30 days",
    "iterationNum": 10,
    "recurringPaymentId": "2cb772ff-8e5f-4c4a-8261-ea7ee1c2ef0e",
    "error": null,
    "logId": null,
    "txDate": null
}
 ```

### Get recurring payments paginated

Send a `GET` request to the `/recurring-payments` endpoint to invoke the [`GetRecurringPaymentsPaginatedFlow`](back-end-guide.md#getrecurringpaymentspaginatedflow). The `GetRecurringPaymentsPaginatedFlow` returns a list of recurring payments that match the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/recurring-payments`.

{{< table >}}
| Param        | Description                                               | Type   | Required |
| ------------ | --------------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.                     | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.                  | int    | Yes      |
| `sortField`  | Sort results on this field.                               | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                      | string | No       |
| `searchTerm` | Term to partially match against multiple fields.          | string | No       |
| `dateFrom`   | Filter recurring payments with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter recurring payments with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing recurring payments matching the given search criteria - `PaginatedResponse<RecurringPaymentResponse>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/recurring-payments/?startPage=1&pageSize=10&sortField=amount&sortOrder=ASC&searchTerm=&dateFrom=2020-11-07T07:49:32.882Z&dateTo=2021-12-07T10:49:32.882Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM1ODEyOCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNjY5OTViMGMtYzQwZS00YjQ4LTg0YmUtY2Y2MjlkYjE2NzRiIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.UwAoVf2fd7j1HV1q7VTwzEMrjsmjLdkJRD9unYPzhcsFgtnis31158ynzpBT4RwTQLfZjSHC6cOSUlyIN8bstfRVoe4sszT_sqTcHB_QkgiUddnCn3v4GImctZQSwMqqAWswsplDU1CI_rF0dSTIoQWfzB1SlzyNyq9TIMVxn2cQV8We85LZX_-Er__uCydFxYfxFakaY1QchNJrL7rfpeqCHVYNrz8zeoKqb4QizT8oun04h3qgz_J_ENbq-pkvPWG7SKywijQVuPuexTg2cWtkx09J9x0q1uSYsTNEP39Qfnw-pCAJ0nn_eu_0YdeRzHFIiqAh3CZObpjXhf4tWA'
```
Sample response:
```
{
    "result": [
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:13:42.974Z",
            "period": "0 days",
            "iterationNum": 8,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[991b0cc5-5f51-440c-a61c-5da6ecd3fd50]:5",
            "txDate": "2020-12-07T16:14:43.727Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:12:42.974Z",
            "period": "0 days",
            "iterationNum": 9,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[3b0cb522-4d6a-4917-aa9e-f01c0a4beb2e]:5",
            "txDate": "2020-12-07T16:13:43.550Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:11:42.974Z",
            "period": "0 days",
            "iterationNum": 10,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[1446c655-9540-4679-ab67-44525b3c04e1]:5",
            "txDate": "2020-12-07T16:12:43.780Z"
        }
    ],
    "totalResults": 3,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 1
}
```


### Get recurring payments for a specified account

Send a `GET` request to the `/recurring-payments/account/{accountId}` endpoint to invoke the [`GetRecurringPaymentsForAccountPaginatedFlow`](back-end-guide.md#getrecurringpaymentsforaccountpaginatedflow). The `GetRecurringPaymentsForAccountPaginatedFlow` returns a list of recurring payments for a specified account that match the given search criteria. This request requires authorization. It can be sent by an admin user.

 - Request type: `GET`.
 - Path: `/recurring-payments/account/{accountId}`.

{{< table >}}
| Param        | Description                                               | Type   | Required |
| ------------ | --------------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.                     | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.                  | int    | Yes      |
| `sortField`  | Sort results on this field.                               | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                      | string | No       |
| `searchTerm` | Term to partially match against multiple fields.          | string | No       |
| `dateFrom`   | Filter recurring payments with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter recurring payments with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing recurring payments for the specified account, matching the given search criteria - `PaginatedResponse<RecurringPaymentResponse>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/recurring-payments/account/378774a1-d18a-4b00-84f0-3e58b34091fa?startPage=1&pageSize=10&sortField=amount&sortOrder=ASC&searchTerm=&dateFrom=2020-12-07T08:12:54.289Z&dateTo=2021-12-07T11:12:54.289Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM1ODEyOCwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNjY5OTViMGMtYzQwZS00YjQ4LTg0YmUtY2Y2MjlkYjE2NzRiIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.UwAoVf2fd7j1HV1q7VTwzEMrjsmjLdkJRD9unYPzhcsFgtnis31158ynzpBT4RwTQLfZjSHC6cOSUlyIN8bstfRVoe4sszT_sqTcHB_QkgiUddnCn3v4GImctZQSwMqqAWswsplDU1CI_rF0dSTIoQWfzB1SlzyNyq9TIMVxn2cQV8We85LZX_-Er__uCydFxYfxFakaY1QchNJrL7rfpeqCHVYNrz8zeoKqb4QizT8oun04h3qgz_J_ENbq-pkvPWG7SKywijQVuPuexTg2cWtkx09J9x0q1uSYsTNEP39Qfnw-pCAJ0nn_eu_0YdeRzHFIiqAh3CZObpjXhf4tWA'
```

Sample response:
```
{
    "result": [
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:17:42.974Z",
            "period": "0 days",
            "iterationNum": 4,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[ca8850bd-32f2-44ab-8698-511a8dcdd9f0]:5",
            "txDate": "2020-12-07T16:18:43.597Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:13:42.974Z",
            "period": "0 days",
            "iterationNum": 8,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[991b0cc5-5f51-440c-a61c-5da6ecd3fd50]:5",
            "txDate": "2020-12-07T16:14:43.727Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:15:42.974Z",
            "period": "0 days",
            "iterationNum": 6,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[ff206327-ea51-489e-a2fd-ed254868a21b]:5",
            "txDate": "2020-12-07T16:16:43.644Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:16:42.974Z",
            "period": "0 days",
            "iterationNum": 5,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[d7381d17-7ad9-462e-bc3a-7b7897aa45d2]:5",
            "txDate": "2020-12-07T16:17:43.472Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:11:42.974Z",
            "period": "0 days",
            "iterationNum": 10,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[1446c655-9540-4679-ab67-44525b3c04e1]:5",
            "txDate": "2020-12-07T16:12:43.780Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:14:42.974Z",
            "period": "0 days",
            "iterationNum": 7,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[365840d3-1ff0-4750-a3d3-eec58ae07111]:5",
            "txDate": "2020-12-07T16:15:43.658Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:12:42.974Z",
            "period": "0 days",
            "iterationNum": 9,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[3b0cb522-4d6a-4917-aa9e-f01c0a4beb2e]:5",
            "txDate": "2020-12-07T16:13:43.550Z"
        }
    ],
    "totalResults": 7,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 1
}
```

### Get recurring payments for a specified customer

Send a `GET` request to the `/recurring-payments/customer/{customerId}` endpoint to invoke the [`GetRecurringPaymentsForCustomerPaginatedFlow`](back-end-guide.md#getrecurringpaymentsforcustomerpaginatedflow). The `GetRecurringPaymentsForCustomerPaginatedFlow` returns a list of recurring payments for the specified customer ID that match the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/recurring-payments/customer/{customerId}`.

{{< table >}}
| Param        | Description                                               | Type   | Required |
| ------------ | --------------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.                     | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.                  | int    | Yes      |
| `sortField`  | Sort results on this field.                               | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                      | string | No       |
| `searchTerm` | Term to partially match against multiple fields.          | string | No       |
| `dateFrom`   | Filter recurring payments with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter recurring payments with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing recurring payments for the specified customer ID, matching the given search criteria - `PaginatedResponse<RecurringPaymentResponse>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/recurring-payments/customer/50480ad7-b70a-4579-931e-0d8730e366e9?startPage=1&pageSize=10&sortField=amount&sortOrder=ASC&searchTerm=&dateFrom=2020-12-07T08:12:54.289Z&dateTo=2021-12-07T11:12:54.289Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM1OTA0OSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNTFhODY0ODQtMWE2MC00ZGIzLWIwMGMtZDA1ZjNmNWY4ZDZkIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.NtnTN2ojjlRMwCK66B0TnOSXKmy2C98T-C-NJQLL842d86Qt2P4QZl5qgYaZV1U69V-pqY29k9q_ovwWHHWmhm4UP30BAQ_TLg-FOJv4jRpxEaiOTfU7WAJ4gut_BxkoRAyRXVcpuufUndyaTKeLq_AgCBcxfWQsE2xZQlGYONzmSQlecKK0NqD0I3PC9C8EsEpiXCHyIWcQv_yPwJOVy9ha-AoaBiguU_GzYDT9PpuTGZuHFc3xa82xtbNwvRjYzTA8Q3XDtu_l7wpMzlpvpfqB9KYhRxjlbqONgi94fnvt8TN5fI8PhD_bBlvDhsWSsFaTfjjoI6WviAgiD71Ztg'
```

Sample response:
```
{
    "result": [
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:17:42.974Z",
            "period": "0 days",
            "iterationNum": 4,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[ca8850bd-32f2-44ab-8698-511a8dcdd9f0]:5",
            "txDate": "2020-12-07T16:18:43.597Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:13:42.974Z",
            "period": "0 days",
            "iterationNum": 8,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[991b0cc5-5f51-440c-a61c-5da6ecd3fd50]:5",
            "txDate": "2020-12-07T16:14:43.727Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:18:42.974Z",
            "period": "0 days",
            "iterationNum": 3,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[d124591a-bbc9-43d6-b3b9-8479c0546dc4]:5",
            "txDate": "2020-12-07T16:19:43.645Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:16:42.974Z",
            "period": "0 days",
            "iterationNum": 5,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[d7381d17-7ad9-462e-bc3a-7b7897aa45d2]:5",
            "txDate": "2020-12-07T16:17:43.472Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:15:42.974Z",
            "period": "0 days",
            "iterationNum": 6,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[ff206327-ea51-489e-a2fd-ed254868a21b]:5",
            "txDate": "2020-12-07T16:16:43.644Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:19:42.974Z",
            "period": "0 days",
            "iterationNum": 2,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[06ce6981-9146-42b9-8808-92e73b68377e]:5",
            "txDate": "2020-12-07T16:20:43.415Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:11:42.974Z",
            "period": "0 days",
            "iterationNum": 10,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[1446c655-9540-4679-ab67-44525b3c04e1]:5",
            "txDate": "2020-12-07T16:12:43.780Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:14:42.974Z",
            "period": "0 days",
            "iterationNum": 7,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[365840d3-1ff0-4750-a3d3-eec58ae07111]:5",
            "txDate": "2020-12-07T16:15:43.658Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:20:42.974Z",
            "period": "0 days",
            "iterationNum": 1,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[1b65f641-44f6-43c2-9317-c9cfbdd98017]:5",
            "txDate": "2020-12-07T16:21:43.665Z"
        },
        {
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currencyCode": "EUR",
            "dateStart": "2020-12-07T16:12:42.974Z",
            "period": "0 days",
            "iterationNum": 9,
            "recurringPaymentId": "f16e16a0-8cd5-4631-8194-57eb73d29d0c",
            "error": null,
            "logId": "[3b0cb522-4d6a-4917-aa9e-f01c0a4beb2e]:5",
            "txDate": "2020-12-07T16:13:43.550Z"
        }
    ],
    "totalResults": 10,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 1
}
```

## Transaction Controller

The Transaction Controller includes API endpoints that reference transactions in Bank in a Box. Requests sent to these endpoints return lists of exisiting transactions that match the given search parameters.

### Get transactions

Send a `GET` request to the `/transactions` endpoint to invoke the [`GetTransactionsPaginatedFlow`](back-end-guide.md#gettransactionspaginatedflow). The `GetTransactionsPaginatedFlow` returns a list of all transactions matching the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/transactions`.

{{< table >}}
| Param        | Description                                         | Type   | Required |
| ------------ | --------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.               | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.            | int    | Yes      |
| `sortField`  | Sort results on this field.                         | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                | string | No       |
| `searchTerm` | Term to partially match against multiple fields.    | string | No       |
| `dateFrom`   | Filter transactions with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter transactions with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing transactions matching the given search criteria - `PaginatedResponse<TransactionLogSchemaV1.TransactionLog>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/transactions?startPage=1&pageSize=10&sortOrder=ASC&searchTerm&dateFrom=2020-12-03T10:43:24.642Z&dateTo=2021-12-04T10:43:24.642Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM0MDE2MywiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNzU2NDQ4MGYtNGZiMy00ZmZhLTk1NGItYWRmOWU0OTZhZDk5IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.ZCG4HJTX7x_4VbqRmDSowgCiVMxIhFDprAAgYZ_Cr4TXwTNZF7xEtwoiytQBwcVjed2m0yI_8iLiqgOzHSEmcs2u6yibGgITPcKEQKUS7pKBPCJM-TkcZjQfCi-JB4T4CrqcTt-9kO0YQRQF9u3jNFWR6MSBao987KhJA3RDT5L7j0gfFiqat5WgqEx3pmcNGRjcA6pg99XQJNqovNu2PRxjK1oDbre0LX7ID705J03PLkwDf_BgiinuygCWsuQQGIRB2rSTTa88DzH5znHJbyUJdlpNihCHOxl2DAYf9dW9l1S_a7FvuwW2UBKBT-XfOEm1cdINmbQm_5VlkluywQ'
```

Sample response:
```
{
    "result": [
        {
            "txId": "1C8075378CAFBB315A1722660B8A319D70C7EE74A9A20A2F2B5570F07EDA8F0E",
            "accountFrom": null,
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 200000,
            "currency": "EUR",
            "txDate": "2020-12-07T09:14:53.697Z",
            "txType": "DEPOSIT"
        },
        {
            "txId": "5859855F2D3C8AF107659F9AC405D54A3F207FAC6B898153722BF6B455210EB0",
            "accountFrom": null,
            "accountTo": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "amount": 200000,
            "currency": "EUR",
            "txDate": "2020-12-07T09:28:13.096Z",
            "txType": "DEPOSIT"
        },
        {
            "txId": "7E12CC264D512BC411CE0527E05031B9D39CCEAF765258F5D269BA9F94D9EF83",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T11:06:35.482Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "C8A916625F7298F6E58C57C4567965FC72FA1B9305FD30C47742B6DEB992833C",
            "accountFrom": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "accountTo": null,
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T11:19:22.530Z",
            "txType": "WITHDRAWAL"
        },
        {
            "txId": "EF29E160CF7B2A528DBD61DA0592E4CD47B36DBF9ED7CD4D6AAF566BBFAF7795",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T10:13:44.846Z",
            "txType": "TRANSFER"
        }
    ],
    "totalResults": 5,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 1
}
```


### Get transactions for a specified account

Send a `GET` request to the `/transactions/account/{accountId}` endpoint to invoke the [`GetTransactionsForAccountPaginatedFlow`](back-end-guide.md#gettransactionsforaccountpaginatedflow). The `GetTransactionsForAccountPaginatedFlow` returns a list of transactions for a specified account ID, matching the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/transactions/account/{accountId}`.

{{< table >}}
| Param        | Description                                         | Type   | Required |
| ------------ | --------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.               | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.            | int    | Yes      |
| `sortField`  | Sort results on this field.                         | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                | string | No       |
| `searchTerm` | Term to partially match against multiple fields.    | string | No       |
| `dateFrom`   | Filter transactions with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter transactions with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing transactions for a specified account ID, matching the given search criteria - `PaginatedResponse<TransactionLogSchemaV1.TransactionLog>`.


Sample request:
```
curl --location --request GET 'http://localhost:7777/transactions/account/378774a1-d18a-4b00-84f0-3e58b34091fa?startPage=1&pageSize=10&sortField=amount&sortOrder=ASC&searchTerm=&dateFrom=2020-12-07T08:12:54.289Z&dateTo=2021-12-07T11:12:54.289Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM1OTA0OSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNTFhODY0ODQtMWE2MC00ZGIzLWIwMGMtZDA1ZjNmNWY4ZDZkIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.NtnTN2ojjlRMwCK66B0TnOSXKmy2C98T-C-NJQLL842d86Qt2P4QZl5qgYaZV1U69V-pqY29k9q_ovwWHHWmhm4UP30BAQ_TLg-FOJv4jRpxEaiOTfU7WAJ4gut_BxkoRAyRXVcpuufUndyaTKeLq_AgCBcxfWQsE2xZQlGYONzmSQlecKK0NqD0I3PC9C8EsEpiXCHyIWcQv_yPwJOVy9ha-AoaBiguU_GzYDT9PpuTGZuHFc3xa82xtbNwvRjYzTA8Q3XDtu_l7wpMzlpvpfqB9KYhRxjlbqONgi94fnvt8TN5fI8PhD_bBlvDhsWSsFaTfjjoI6WviAgiD71Ztg'
```

Sample response:
```
{
    "result": [
        {
            "txId": "7E12CC264D512BC411CE0527E05031B9D39CCEAF765258F5D269BA9F94D9EF83",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T11:06:35.482Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "EF29E160CF7B2A528DBD61DA0592E4CD47B36DBF9ED7CD4D6AAF566BBFAF7795",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T10:13:44.846Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "EDE99FBF55DA20E56CA474CEFBC83489706A416CABABFEF270E504A10BFE4E73",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:12:43.004Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "BD67563169579781AC3228CE9746733A6BA9EBA358319A53140896CF7D595705",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:20:42.989Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "A329B87B4A49840A77B486E7E4E4D5C270DA607B0F9540338569C6B5EFC2A204",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:18:42.991Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "A3EE08C7C16BDE3ABA6CC76B3A40AB7B30080C114277FE801F985112D77BB70F",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:14:43.032Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "A00FB5ABAA75FF9BF56D85BB4EFA5C71CE6A1441670F12F37C94AB8D4126931A",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:13:42.993Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "1CBAC6F1C4A90D67F620A613FA2CA290C1DB0A93CA85287989676220FCB74032",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:16:43.012Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "289D0C014118DCE337AE092B429960A6E23AB164BA266C2B7D4F4A4E02910706",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:17:42.992Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "93E1D7568B08D6FE00BC3C17287A12EA4B840109DA177B7C460767CE1ED4BB87",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:21:42.988Z",
            "txType": "TRANSFER"
        }
    ],
    "totalResults": 13,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 2
}
```

### Get transactions for a specified customer

Send a `GET` request to the `/transactions/customer/{customerId}` endpoint to invoke the [`GetTransactionsForCustomerPaginatedFlow`](back-end-guide.md#gettransactionsforcustomerpaginatedflow). The `GetTransactionsForCustomerPaginatedFlow` returns a list of transactions for a specified customer ID, matching the given search criteria. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/transactions/customer/{customerId}`.

{{< table >}}
| Param        | Description                                         | Type   | Required |
| ------------ | --------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.               | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.            | int    | Yes      |
| `sortField`  | Sort results on this field.                         | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                | string | No       |
| `searchTerm` | Term to partially match against multiple fields.    | string | No       |
| `dateFrom`   | Filter transactions with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter transactions with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns a paginated response containing transactions for a specified customer ID, matching the given search criteria - `PaginatedResponse<TransactionLogSchemaV1.TransactionLog>`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/transactions/customer/50480ad7-b70a-4579-931e-0d8730e366e9?startPage=1&pageSize=10&sortField=amount&sortOrder=ASC&searchTerm&dateTo=2021-12-07T08:12:54.289Z&dateFrom=2020-12-07T08:12:54.289Z' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM1OTA0OSwiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNTFhODY0ODQtMWE2MC00ZGIzLWIwMGMtZDA1ZjNmNWY4ZDZkIiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.NtnTN2ojjlRMwCK66B0TnOSXKmy2C98T-C-NJQLL842d86Qt2P4QZl5qgYaZV1U69V-pqY29k9q_ovwWHHWmhm4UP30BAQ_TLg-FOJv4jRpxEaiOTfU7WAJ4gut_BxkoRAyRXVcpuufUndyaTKeLq_AgCBcxfWQsE2xZQlGYONzmSQlecKK0NqD0I3PC9C8EsEpiXCHyIWcQv_yPwJOVy9ha-AoaBiguU_GzYDT9PpuTGZuHFc3xa82xtbNwvRjYzTA8Q3XDtu_l7wpMzlpvpfqB9KYhRxjlbqONgi94fnvt8TN5fI8PhD_bBlvDhsWSsFaTfjjoI6WviAgiD71Ztg'
```

Sample response:
```
{
    "result": [
        {
            "txId": "7E12CC264D512BC411CE0527E05031B9D39CCEAF765258F5D269BA9F94D9EF83",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T11:06:35.482Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "EF29E160CF7B2A528DBD61DA0592E4CD47B36DBF9ED7CD4D6AAF566BBFAF7795",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
            "amount": 1000,
            "currency": "EUR",
            "txDate": "2020-12-07T10:13:44.846Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "A329B87B4A49840A77B486E7E4E4D5C270DA607B0F9540338569C6B5EFC2A204",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:18:42.991Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "A00FB5ABAA75FF9BF56D85BB4EFA5C71CE6A1441670F12F37C94AB8D4126931A",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:13:42.993Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "BD67563169579781AC3228CE9746733A6BA9EBA358319A53140896CF7D595705",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:20:42.989Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "93E1D7568B08D6FE00BC3C17287A12EA4B840109DA177B7C460767CE1ED4BB87",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:21:42.988Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "EDE99FBF55DA20E56CA474CEFBC83489706A416CABABFEF270E504A10BFE4E73",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:12:43.004Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "359CD77E0B36A1E3C01A72BC05601D91EF57042A9381861E141EDF56294589E2",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:19:42.989Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "1CBAC6F1C4A90D67F620A613FA2CA290C1DB0A93CA85287989676220FCB74032",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:16:43.012Z",
            "txType": "TRANSFER"
        },
        {
            "txId": "289D0C014118DCE337AE092B429960A6E23AB164BA266C2B7D4F4A4E02910706",
            "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
            "accountTo": "87cb6fa7-6839-4c95-a50b-e634119fdf01",
            "amount": 10000,
            "currency": "EUR",
            "txDate": "2020-12-07T16:17:42.992Z",
            "txType": "TRANSFER"
        }
    ],
    "totalResults": 13,
    "pageSize": 10,
    "pageNumber": 1,
    "totalPages": 2
}
```

### Get transactions by transaction ID

Send a `GET` request to the `/transactions/{transactionId}` endpoint to invoke the [`GetTransactionByIdFlow`](back-end-guide.md#gettransactionbyidflow. The `GetTransactionByIdFlow` returns the transaction information for a specified transaction ID. This request requires authorization. It can be sent by an admin user.

- Request type: `GET`.
- Path: `/transactions/{transactionId}`.

{{< table >}}
| Param        | Description                                         | Type   | Required |
| ------------ | --------------------------------------------------- | ------ | -------- |
| `startPage`  | Position of the start page to return.               | int    | Yes      |
| `pageSize`   | The maximum number of results in a page.            | int    | Yes      |
| `sortField`  | Sort results on this field.                         | string | Yes      |
| `sortOrder`  | Order of the sort (`ASC` or `DESC`.)                | string | No       |
| `searchTerm` | Term to partially match against multiple fields.    | string | No       |
| `dateFrom`   | Filter transactions with `txDate` after this date.  | string | No       |
| `dateTo`     | Filter transactions with `txDate` before this date. | string | No       |
{{< /table >}}

Response: This request returns the transaction information for a specified transaction ID - `TransactionLogSchemaV1.TransactionLog`.

Sample request:
```
curl --location --request GET 'http://localhost:7777/transactions/EF29E160CF7B2A528DBD61DA0592E4CD47B36DBF9ED7CD4D6AAF566BBFAF7795' \
--header 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiVVNFUl9DTElFTlRfUkVTT1VSQ0UiLCJVU0VSX0FETUlOX1JFU09VUkNFIl0sInVzZXJfbmFtZSI6ImFkbWluIiwic2NvcGUiOlsicmVhZCIsIndyaXRlIl0sImN1c3RvbWVySWQiOm51bGwsImV4cCI6MTYwNzM0MDE2MywiYXV0aG9yaXRpZXMiOlsiQURNSU4iXSwianRpIjoiNzU2NDQ4MGYtNGZiMy00ZmZhLTk1NGItYWRmOWU0OTZhZDk5IiwiY2xpZW50X2lkIjoiYmFua19pbl9hX2JveF9hcHAifQ.ZCG4HJTX7x_4VbqRmDSowgCiVMxIhFDprAAgYZ_Cr4TXwTNZF7xEtwoiytQBwcVjed2m0yI_8iLiqgOzHSEmcs2u6yibGgITPcKEQKUS7pKBPCJM-TkcZjQfCi-JB4T4CrqcTt-9kO0YQRQF9u3jNFWR6MSBao987KhJA3RDT5L7j0gfFiqat5WgqEx3pmcNGRjcA6pg99XQJNqovNu2PRxjK1oDbre0LX7ID705J03PLkwDf_BgiinuygCWsuQQGIRB2rSTTa88DzH5znHJbyUJdlpNihCHOxl2DAYf9dW9l1S_a7FvuwW2UBKBT-XfOEm1cdINmbQm_5VlkluywQ'
```

Sample response:
```
{
    "txId": "EF29E160CF7B2A528DBD61DA0592E4CD47B36DBF9ED7CD4D6AAF566BBFAF7795",
    "accountFrom": "378774a1-d18a-4b00-84f0-3e58b34091fa",
    "accountTo": "bde1c40a-cf68-4311-b972-56e155497f8b",
    "amount": 1000,
    "currency": "EUR",
    "txDate": "2020-12-07T10:13:44.846Z",
    "txType": "TRANSFER"
}
```


## Errors

Bank in a Box uses conventional HTTP response codes to indicate whether an API request has succeeded or failed. A summary of these status codes is provided below.

{{< table >}}
| HTTP Code                   | Summary                                                                                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200 - OK                    | The request has worked as expected.                                                                                                                                                 |
| 400 - Bad Request           | The request was not accepted. This is likely due to a missing or malformed required parameter.                                                                                      |
| 401 - Unauthorized          | No valid API key provided.                                                                                                                                                          |
| 403 - Forbidden             | The API key does not have the correct permissions to perform the request. This can occur if using an admin `access_token` when a customer `access_token` is required or vice versa. |
| 500 - Internal Server Error | Something went wrong with Bank in a Box.                                                                                                                                            |
{{< /table >}}
