---
date: '2023-04-14'
title: "Permissions System Entities"
menu:
corda-5-beta:
identifier: corda-5-beta-permissions-system-entities
parent: corda-5-beta-developing-and-operating
weight: 3000
section_menu: corda-5-beta
---

The R3's role-based access control (RBAC) permissions system is made up of multiple entities.
The following diagram presents those entities and relationships between them:

{{< figure src="images/entities.png" figcaption="Permissions System Entities" width="55% length="55%">}}

## User

This entity represents a human user or system user.

### Properties

* `Full Name` is a human-readable name. This is a property which will cannot be used to code any permissions against it.
  It also has a UUID identifier for a concrete reference to the instance of an entity.
* `Login Name` is the name used for authentication and authorization purposes. It can be in an email address
  in case of SSO. There can be only one `Enabled` user for a given `Login Name`.
* `Enabled` is a boolean flag to indicate whether the user is enabled or temporarily suspended.
* `E-mail` is an email address for the user account used for communication of any important information
  affecting this account. Same email address may be used for multiple accounts.
* `Salt value` is a randomly generated value used when hashing the password. It only makes sense when password is
  assigned as well. For more details, see [Password Salting](#password-salting).
* `Hashed password` ia a salted and hashed representation of the password. For more details on how to do it,
 see [Choosing Hash Function to Use](#choosing-hash-function-to-use).
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

### Password Salting

Password salting is used during one-way encryption of the `User`'s password.
This mitigates a brute force attack on user passwords in case an entire RBAC database is in possession of an adversary.

As an additional benefit, it also obscures the data from the legitimate holder of the database, and helps to mask the fact
that some users may have the same password.

If `H` is a one-way hash function, then password encrypted value is as follows:
`HashedPassword = H(Salt, ClearTextPassword)`.

New randomly generated `Salt` is produced every time password is assigned or changed.

Random `Salt` generation as well as hashing is always be performed on the server side.

### Choosing Hash Function to Use

For `H` hashing function, do not use SHA-family functions. Use PBKDF2, or BCrypt, or SCrypt type hashes instead.

R3 does not provide any custom implementation of the hashing algorithm. A well-established security library
is used for the implementation of one-way hashing function.

### Properties

Properties here mean a set of `Key` and `Value` pairs associated with either `User` or `Group`.
Users of the RBAC database are able to retrieve these properties and make decisions depending on the context.

* `Key` is a string representing a value. Only one unique key is allowed for a given `User` or `Group`.
* `Value` is a string representing a value associated with a `Key`.

## Group

This entity represents a group of `Users`.

### Properties

* `Name` is a human-readable name of the group.
  It also has a UUID identifier for a concrete reference to the instance of an entity.
* `Parent group` is an optional property which specifies parent group for the current instance of the entity. This value
  can be `null` which means it is a root-level group. Each group can have at most one parent.

### Relationships

* `Group` may have a one-to-one reference to itself for parent/child group relationships.
* `Group` can have multiple roles associated with it.
* `Group` can have multiple `Properties` assigned to it.

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
