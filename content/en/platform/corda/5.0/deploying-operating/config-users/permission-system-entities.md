---
date: '2023-04-24'
title: "Permission System Entities"
menu:
  corda-5:
    parent: corda-5-cluster-config-users
    identifier: corda-5-cluster-permission-system-entities
    weight: 3000
section_menu: corda-5
---

R3's role-based access control (RBAC) permissions system is made up of multiple entities.
The following section describes those entities and relationships between them.

## User

This entity represents a human user or system user.

### Attributes

* `Full Name` is a human-readable name. This is a property which cannot be used to code any permissions against it.
  It also has a UUID identifier for a concrete reference to the instance of an entity.
* `Login Name` is the name used for authentication and authorization purposes. It can be in an email address
  in case of SSO. There can be only one `Enabled` user for a given `Login Name`.
* `Enabled` is a boolean flag to indicate whether the user is enabled or temporarily suspended.
* `E-mail` is an email address for the user account used for communication of any important information
  affecting this account. The same email address may be used for multiple accounts.
* `Salt value` is a randomly generated value used when hashing the password. It only makes sense when the password is
  assigned as well.
* `Hashed password` is a salted and hashed representation of the password.
 This property can be set to `null` for SSO-only accounts.
* `Password expiry` is only applicable when password is assigned and when it specifies the timestamp after which the password
  is deemed expire and needs changing.
* `Parent Group` is an optional identifier of the group to which the user belongs. This property can be se to `null`. In such
  case, the user is assumed to belong to the "root" group. In the current model, the user can belong to just a
  single group. However, groups can be nested.

### Relationships

* `User` can be associated one-to-one with a `Group`.
* `User` can have multiple roles associated with it.
* `Change Audit` entries may have one-to-one references to acting `User`.
* `User` can have multiple `Properties` assigned to it.

## Role

This entity represents a set of `Permissions`.

### Properties

* `Name` is a human-readable value for a role. It also has a UUID identifier for a concrete reference to
  the instance of an entity.

### Relationships

Each role can be associated with multiple `Permissions`. A given `Permission` can belong to multiple roles. Hence,
there is many-to-many relationship between `Role` and `Permission`.

## Permission

This entity represents an individual fine-grained permission.

### Properties

* `Virtual Node ID` is an optional identifier of the virtual node within physical node the permission applies to.
* `Permission type` defines whether this is an "allow" or "deny" type of permission. "Deny" permissions will always
  have advantage over "allow", no matter at which level (`User` or `Group`) they are granted.
* `Permission string` is a machine-parseable string representing individual permission. It can be an arbitrary string as
  long as authorization code could make a good use of it in the context where `User` permission to perform a certain
  operation is checked. For example, it can be in the form: `InvokeRpc:...`, or `StartFlow:...`, or `CreateUser:...`.

## Change Audit

This entity represents an audit log for every change to the permission data. This can be introduction of a new `User`,
assignment `User` to a `Group`, creation of a `Role`, and so on.

Writing to this entity's database table is performed atomically in the same transaction as the permission data change.
Once written, the rows of this table are never modified or deleted, so it is an append-only entity.

### Properties

* `Actor User` is the identifier of the user performing an action.
* `Change Type` means an enumerated set of actions defining the nature of the change done to the permission data. For example,
  `UserCreated`, or `PermissionToRoleAssignment`, and so on.
* `Details` means human-readable details giving more explanation about what was changed.
* `Timestamp` is the timestamp of when permission data change was performed.
