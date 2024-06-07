---
description: "Learn how to create new RBAC users."
date: '2024-01-17'
title: "Managing Users and Roles"
menu:
  corda53:
    parent: corda53-cluster-users
    identifier: corda53-cluster-creating-users
    weight: 3000
---
# Managing Users and Roles

RBAC users are created and managed using the REST API. This section describes the following:

{{< toc >}}

## Creating Users

You can create a new user using the POST method of the [/api/v5_3/user endpoint](../../reference/rest-api/openapi.html#tag/RBAC-User-API/operation/post_user). You must include a login name, full name, and password and also specify if the account is enabled. Optionally, you can set the `passwordExpiry` to a past date, which will require the newly-created user to change their password on the first use. If the `passwordExpiry` is not specified or set to `null`, then the password does not expire. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"enabled": true, "fullName:" "Joe Bloggs", "loginName:" "jbloggs", "password:" "wx%ty23Q", "passwordExpiry:" "2022-06-24T10:15:30Z"}}' $REST_API_URL/user
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/user" -Method Post -Body (ConvertTo-Json @{
    request = @{
       enabled = true
       fullName = "Joe Bloggs"
       loginName = "jbloggs"
       password = "wx%ty23Q"
       passwordExpiry = "2022-06-24T10:15:30Z"
    }
})
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
You must have the `UserAdminRole` role to create new users.
{{< /note >}}

## Changing Passwords

You can change your own password using the POST method of the [/api/v5_3/user/selfpassword endpoint](../../reference/rest-api/openapi.html#tag/RBAC-User-API/operation/post_user_selfpassword). Use this endpoint if your password has expired, and you have the correct credentials (you cannot use any other endpoint if your password has expired). When you change your password yourself, its default expiry time is set to 90 days. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"password": "<new_password>"}}' $REST_API_URL/user/selfpassword
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/user/selfpassword" -Method Post -Body (ConvertTo-Json @{
    request = @{
       password = <new_password>
    }
})
```
{{% /tab %}}
{{< /tabs >}}

Users with the `UserAdminRole` role can change the password of other users using the POST method of the [/api/v5_3/user/otheruserpassword endpoint](../../reference/rest-api/openapi.html#tag/RBAC-User-API/operation/post_user_otheruserpassword). When a user with the `UserAdminRole` role changes another user's password, its default expiry time is set to 7 days. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"password": "<new_password>", "username": "<user_loginname>"}}' $REST_API_URL/user/otheruserpassword
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/user/otheruserpassword" -Method Post -Body (ConvertTo-Json @{
    request = @{
       password = <new_password>
       username = <user_loginname>
    }
})
```
{{% /tab %}}
{{< /tabs >}}

## Retrieving Roles

You can retrieve all roles in the system using the [/api/v5_2/role endpoint](../../reference/rest-api/openapi.html#tag/RBAC-Role-API/operation/get_role). For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/role
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/role"
```
{{% /tab %}}
{{< /tabs >}}

This request returns the following for each role:

* `id` — the unique identifier of the role.
* `version` — the version number of the role.
* `updateTimestamp` — the date and time when the role was last updated.
* `roleName` — the name of the role.
* `permissions` — a list of the permissions associated with the role.

## Assigning Roles

You can assign a role to a user using the [/api/v5_2/<login-name>/role/<role-id> endpoint](../../reference/rest-api/openapi.html#tag/RBAC-User-API/operation/put_user__loginname__role__roleid_). This endpoint requires the login name of the user and the ID of the role. To retrieve a list of the roles in the system, including their IDs, see [Retrieving Roles](#retrieving-roles).

For example, to assign a role with the ID bbcc4621-d88f-4a94-ae2f-b38072bf5087 to Joe Bloggs:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/user/jbloggs/rolebbcc4621-d88f-4a94-ae2f-b38072bf5087
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/user/jbloggs/rolebbcc4621-d88f-4a94-ae2f-b38072bf5087 -Method Put
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
You must have the `UserAdminRole` role to create new users.
{{< /note >}}

## Querying Permissions

You can retrieve the permissions in the system that match certain criteria, using the [/api/v5_2/permission endpoint](../../reference/rest-api/openapi.html#tag/RBAC-Permission-API/operation/get_permission). For example, to return 100 permissions that deny access:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD  $REST_API_URL/permission?limit=0&permissiontype=DENY
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)}`
   -Method Get -Uri "$REST_API_URL/permission`?limit=100&permissiontype=DENY"
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
Currently, Corda checks if a user can execute `startFlow` REST operations. No checks are made to whether the user can start a particular flow.
{{< /note >}}
