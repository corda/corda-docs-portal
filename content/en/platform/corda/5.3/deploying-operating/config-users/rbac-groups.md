---
description: "Learn about the RBAC groups and how to manage them."
date: '2024-08-20'
title: "Managing RBAC Groups"
menu:
  corda53:
    parent: corda53-cluster-users
    identifier: corda53-cluster-rbac-groups
weight: 1500
---

# Managing RBAC Groups

RBAC groups are organizational structures used to manage user permissions efficiently. They function similarly to folders in a file system:

Groups can be nested within one another, creating a hierarchical structure.
Roles are assigned to groups and inherited by all users within that group and its subgroups.
Users can have one parent group, allowing for flexible permission management.

By setting a user's parent group, you can easily assign roles and permissions based on group membership. This approach allows for streamlined management of access rights across your organization.

RBAC groups are created and managed using the REST API. This section describes the following:

{{< toc >}}

## Creating Groups

You can create a new group using the POST method of the /api/v5_3/group endpoint. You must include a name for the group and optionally specify a parent group ID. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -d '{"request": {"name": "Marketing", "parentGroupId": "parent-group-id-123"}}' $REST_API_URL/group
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group" -Method Post -Body (ConvertTo-Json @{
    request = @{
       name = "Marketing"
       parentGroupId = "parent-group-id-123"
    }
})
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
You must have the UserAdminRole role to create new groups.
{{< /note >}}

## Changing Parent Groups

You can change the parent group of an existing group using the PUT method of the /api/v5_3/group/{groupId}/parent/changeparentid/{newParentGroupId} endpoint. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/group/group-id-123/parent/changeparentid/new-parent-group-id-456
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group/group-id-123/parent/changeparentid/new-parent-group-id-456" -Method Put
```
{{% /tab %}}
{{< /tabs >}}

## Assigning Roles to Groups

You can assign a role to a group using the PUT method of the /api/v5_3/group/{groupId}/role/{roleId} endpoint. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT $REST_API_URL/group/group-id-123/role/role-id-789
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group/group-id-123/role/role-id-789" -Method Put
```
{{% /tab %}}
{{< /tabs >}}

## Removing Roles from Groups

You can remove a role from a group using the DELETE method of the /api/v5_3/group/{groupId}/role/{roleId} endpoint. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X DELETE $REST_API_URL/group/group-id-123/role/role-id-789
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group/group-id-123/role/role-id-789" -Method Delete
```
{{% /tab %}}
{{< /tabs >}}

## Retrieving Group Content

You can retrieve the content of a group, including its users and subgroups, using the GET method of the /api/v5_3/group/{groupId} endpoint. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD $REST_API_URL/group/group-id-123
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group/group-id-123"
```
{{% /tab %}}
{{< /tabs >}}

This request returns the following for the group:

* `id` — the unique identifier of the group.
* `version` — the version number of the group.
* `updateTimestamp` — the date and time when the group was last updated.
* `name` — the name of the group.
* `parentGroupId` — the ID of the parent group.
* `properties` — a set of key/value properties associated with the group.
* `roleAssociations` — a set of roles associated with the group.
* `users` — a set of users which have this group as their parent group.
* `subgroups` — a set of groups which have this group as their parent group.

## Deleting Groups

You can delete an empty group (a group with no users or subgroups) using the DELETE method of the /api/v5_3/group/{groupId} endpoint. For example:

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X DELETE $REST_API_URL/group/group-id-123
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/group/group-id-123" -Method Delete
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
You can only delete groups that are empty (have no users or subgroups).
{{< /note >}}
