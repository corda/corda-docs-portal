---
date: '2020-07-15T12:00:00Z'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-test-directory-index
    name: Test Directory Child 2
title: Corda 5 Dev Preview Test Directory Child 2
weight: 200
---

**Temporary draft file while waiting for approval of directory PR**

#Network structure

Overview text


## Glossary

**Member**

Someone wishing to communicate with a selected group of peers.

**Membership Group** (or **Group**)

A set of members who can communicate with each other.

**Membership Group Manager (MGM)**

The member responsible for maintaining the membership group.

**MemberInfo**

A data structure that represents an individual member.

**MembershipGroupCache**

A service that stores information about group members.

**CorDapp Package (CPK)**

A bundle of CorDapps, which includes a dependency tree and version information.

**Cordapp Packaged Installation file (CPI)**
A single distributable file, which contains CPKs and group information.


## Structure
The membership group information consists of:
- MGM details distributed in a `.json` file, as part of the CPI.
- Dynamically-updated data distributed by the MGM via flows:
  - The list of members (`memberinfo`)
  - The network parameters (`NetworkParameters`)

### Structure layout and namespace
`NetworkParameters`, `MemberInfo`, and the CPI are structured as loosely-coupled key-value pairs. Keys created by the Corda platform are always prefixed with `corda.`

You can define your own keys and define your own namespaces.


### CPI structure
The CPI has three key elements.
- The CPK. A CPK file is essentially a `jar` file with a `.cpk` file extension. The file extension contains an OSGi bundle and its dependent bundles (excluding
  any bundles provided by Corda or other CPKs). CPKs have a ZIP format, contains a `META-INF/MANIFEST.MF` file and can be signed by Java's `jarsigner` tool.

A CPK should contain a signed OSGi bundle at its root, that contains the CorDapp's
contract, flow, service classes etc. We designate this bundle as the "main" jar.
Any library dependencies that this CorDapp may have are stored in the CPK's `lib/`
folder. These dependencies should also be OSGi bundles, and (as already mentioned)
do not include any CPK dependencies that this CorDapp may have.

- **CPB**, as defined by https://github.com/corda/platform-eng-design/pull/330 - unsigned bundle without deployment specific information. The same bundle can be used for QA and production. Definition of CPB metadata is outside the scope of this document.
- **CPI** - bundle with deployment specific information in metadata. It contains MGM details JSON file, which content is described below. Group properties may be omitted when bootstrapping without MGM. Definition of other CPI metadata is outside the scope of this document.

### MGM details JSON
MGM details are represented as a JSON file. This file is distributed to group members only as a part of CPI.
- `identityTrustStore: KeyStore?` - Trust roots for identity certificates. Null for `NoPKI` option.
- `tlsTrustStore: KeyStore` - Trust roots for TLS.
- `mgmInfo: MemberInfo` - MGM member info.
- `identityPKI: String?` - which PKI to use for identities, see below. Values: `Standard`, `Corda4`, `NoPKI`. Default: `Standard`.
- `identityKeyPolicy: String?` - whether to use combined or distinct keys for ledger signing and end-to-end session authentication, see below. Values: `Combined`, `Distinct`. Default: `Combined`.
- `cipherSuite: Map<String, String>` - cipher suite parameters, see https://github.com/corda/platform-eng-design/blob/master/core/corda-5/corda-5.0/cipher-suite/cipher-suite-definition.md#definition-in-cpi for more details

### NetworkParameters

#### Proposal
As in C4, NetworkParameters are still represented as monolithic structure, which is attached to ledger transaction via hash.

**NetworkParameters** (C5 proposal):
- `modifiedTime` - Last modification time of network parameters set.
- `epoch: Int` - Version number of the network parameters. Starting from 1, this will always increment on each new set of parameters.
- `minimumPlatformVersion: Int` - Minimum version of Corda platform that is required for nodes to join the group.
- `notaries : List<NotaryInfo>` - List of trusted notary service information, like identities, historical service keys, notary type.
- List of supported versions of CPI. To be defined outside this document.

**Network parameters are published by MGM and must be automatically accepted by members.** Flag Day operation is removed.

Each `MemberInfo` will contain `platformVersion` and `cpiVersion`, so MGM can also monitor versions and suspend members via RPC.
Member should be also automatically blocked when receiving network parameters update with unsupported CPI or platform version.

#### NetworkParameter comparison with C4

| Parameter                          | C4 hot-loading | C4 acceptance | Backchain check | C5                 | Comment                                                      |
| ---------------------------------- | -------------- | ------------- | --------------- | ------------------ | ------------------------------------------------------------ |
| modifiedTime                       | YES            | auto          | NO              | :heavy_check_mark: | Meta-parameter with no impact on functionality. Useful for tracing. |
| epoch                              | YES            | auto          | YES             | :heavy_check_mark: | Meta-parameter to enforce version check in transaction chain. |
| minimumPlatformVersion             | NO             | manual        | YES             | :heavy_check_mark: |                                                              |
| notaries                           | YES            | manual        | YES             | :heavy_check_mark: |                                                              |
| maxTransactionSize                 | NO             | manual        | YES             | :x:                | Constant in C5. |
| maxMessageSize                     | NO             | manual        | NO              | :x:                | Flow layer will eventually implement message fragmentation using the value exposed by P2P layer, which will be negotiated bilaterally between peers. TBC re C5.0 (until fragmentation is properly implemented): the value can be either hardcoded to Kafka defaults (~1M) or configured in CPI. |
| packageOwnership                   | NO             | auto          | YES             | :x:                | Used by `AttachmentsClassLoader`. Replaced by CPI/CPK. |
| whitelistedContractImplementations | NO             | auto          | YES             | :x:                | OCTO-12 suggests to deprecate.                               |
| eventHorizon                       | NO             | manual        | NO              | :x:                | Hardcode to 30 days as per OCTO-12 (if needed). C5 P2P resend logic may not use it. |
| cpiVersions                        | -              | -             | -               | :heavy_check_mark: | New in C5. |

### MemberInfo
The member info consist of two parts:
- *Member provided context*: Parameters added and signed by member as a part of initial `MemberInfo` proposal.
- *MGM provided context*: Parameters added by MGM as a part of member acceptance.

The entire structure must be signed by MGM.

There will be a lind of "_virtual class hierarchy_" where the member info will describe differet types of members (MGM. Notary, Member) but instead of having different subclasses some properties will be optional and their presense will indicate the type of the member.

Structure:
- **memberProvidedContext**
  - `groupId: String`: Group identifier: UUID as a String.
  - `party: Party`: Member *identity*, which includes X.500 name and identity key. Party name is unique within the group and cannot be changed while the membership exists.
  - `certificate: CertPath?` -  Identity certificate or `null` for non-PKI option. Certificate subject should match `party.name`.
  - `keys: List<PublicKey>` - List of current and previous (rotated) identity keys, which member can still use to sign unspent transactions on ledger.
  - `endpoints: List<EndpointInfo>` - List of P2P endpoints for member's node.
    - `url: String`: Endpoint base URL.
    - `protocolVersion: Int` - Version of end-to-end authentication protocol. If multiple versions are supported, the same URL should be listed multiple times.
  - `platformVersion: Int`
  - `softwareVersion: String` - Corda-Release-Version
  - `serial: Long` - An arbitrary number incremented each time the MemberInfo is changed.
  - `sessionKey: PublicKey?` - Key used to establish end-to-end authenticated session, set if different from identity key.
  - Version of CPI used by member.  To be defined outside this document.
  - `notaryServiceParty: Party?` - Notary service identity. Non null value denotes that the member is a notary worker. The service may consist of a single or multiple wprkers worker. The service identity must be shared between its workers if the notary is represented by the HA cluster. There is no expectation that the X500 name and the owning key will have to be the same as in the `party` property. It may or may not be the same. However it's expected that all notary workers representing the same cluster will share the same service party. Filtering the member list by the `notaryServiceParty` will yield all workers for that service.
  - `ecdhKey: PublicKey?` - Only set for MGM. Static DH key for ECIES encryption used during member registration.
- **mgmProvidedContext**
  - `creationTime: Instant`: Time of creation.
  - `modificationTime: Instant`: Time of last modification.
  - `expiryTime: Instant`: Expiry time after which the structure is considered as invalid.
  - `status: MemberStatus`: Status of the member. Values:
    - `PENDING`: Member registration is in progress. This state is hidden from other group members.
    - `ACTIVE`: Member can communicate to other members.
    - `SUSPENDED`: Member is temporarily suspended.
  - `trackingNumber: Long?`: Sequentially incremented global number per group, which is used for group data synchronization.
  - `mgm: Boolean?`: True for MGM.

## Keys and certificates
Every public/private key pair used in the group must belong to particular member, i.e. bound to certain X.500 name during entire key life. The same key can be present in different groups.

Member key can have the following roles:
- *Identity*: to represent peer's identity in a flow session.
- *Ledger*: to sign ledger transactions.
- *Session*: to sign handshake messages when establishing end-to-end session.

By default each member has a *single* key which combines all 3 roles.

CPI contains `identityKeyPolicy` setting with the following options:
- `Combined`: Ledger key is also used as a session key. This is a default option.
- `Distinct`: Requires to have distinct ledger and session keys.

The following `MemberInfo` properties are used for each key type:
| identityKeyPolicy | Combined | Distinct |
| ----------------- | -------- | -------- |
| Identity key      | `party` | `party` |
| Default ledger key | `party` | `party` |
| Additional ledger keys | `keys` | `keys` |
| Session key       | `party` | `sessionKey` |

### Identity certificate
Type of used PKI is defined by CPI `identityPki` setting:
- `Standard`: members (including MGM) must obtain a valid certificate for their identity keys. This is a default option.
- `StandardEV3` (not for 5.0 GA): same as `Standard`, but with additional EV3 (Extended Validation) certificate checks.
- `Corda4`: same as `Standard`, but certificates have to be generated by C4 CENM.
- `NoPKI`: certificates are not used for identity keys. CPI `identityTrustStore` has to be set to `null`.

Certificate subject must be equal to member's X.500 name. Identity certificate is verified in the following cases:
- When establishing end-to-end authenticated session. This check includes CRL, as well as verification of peer's `MemberInfo.status` and `MemberInfo.expiryTime`.
- When adding (updating) `MemberInfo` into `MembershipGroupCache`. CRL check is not performed here.

> Similarly to C4, certificates are not checked in ledger operations (transaction signing etc).

With `Distinct` key policy, *a certificate is bound to a session key*. This is because certificate check is strictly related to end-to-end session lifecycle, similarly to how TLS certificate is checked in TLS session.

> To use certificate for ledger key, one must choose `Combined` key policy. As a future enhancement, we can consider adding support for ledger certificates with `Distinct` key policy. At the moment it's out of the scope because:
> - Having 3 PKIs looks too excessive.
> - It's unclear whether ledger certificate should be verified by platform (and, if yes, when exactly) or by application.

### Ledger keys
Identity key is a default ledger key. After rotation of identity key, member can choose whether to use it as additional ledger key (by default) or to remove it. Rotated ledger key doesn't have a certificate and should be treated in the same way, as Confidential Identity key.

> Platform doesn't check the validity of rotated ledger keys: it's up to application to decide whether to accept them or not.

### Key lifecycle
![Identity key lifecycle](identity-key-lifecycle.png "Identity key lifecycle")

### Key rotation
Rotation of identity or session key (and certificate) is performed simply by updating and republishing `MemberInfo` via RPC command.

By default old key and certificate should remain in the keystore, while old identity key should be listed in `MemberInfo.keys`. This can help to achieve smooth transition, because other peers may still see older `MemberInfo` version for a short time.

Owner should manually cleanup keystore and/or `MemberInfo.keys`, whenever appropriate (change of `MemberInfo.keys` will require another republishing).

### IdentityService
`IdentityService` remains conceptually the same as in latest C4 version:
- Key to name mapping is immutable: entry remains even if key is removed from `MemberInfo`.
- Name to key mapping is mutable: it's updated according to the latest `MemberInfo`.
- If `MemberInfo` is suspended or removed from `MembershipGroupCache`, `IdentityService` still keeps latest name to key mapping.
- CI with certificates are removed from C5.
- CI without certificates remain the same as in C4.

### MGM keys
- MGM `MemberInfo` can be only distributed via CPI (`mgmInfo`).
- MGM should provide a valid certificate for it's identity key (`mgmInfo.party`).

| Key type             | C4 equivalent                | Property         | Comment                                                      |
| -------------------- | ---------------------------- | -----------------| ------------------------------------------------------------ |
| Member info          | NETWORK_MAP cert role        | `mgmInfo.party`  | Signing MemberInfo and other top level structures, e.g. list of members. |
| Network parameters   | NETWORK_PARAMETERS cert role | `mgmInfo.party`  | Default key for signing network parameters.                  |
| Network parameters   | NETWORK_PARAMETERS cert role | `mgmInfo.keys`   | All historical network parameters keys.                      |
| End-to-end session   | no                           | `mgmInfo.sessionKey` (or `mgmInfo.party`) | To establish end-to-end authenticated session. |
| ECIES authentication | no                           | `mgmInfo.ecdhKey`| Authentication for registration of new members.              |

> The same key will be used to sign MemberInfo and NetworkParameters.

### Signatures
Member context of the `MemberInfo` must be signed by **every** key listed in `MemberInfo` - to provide proof of ownership.
Entire `MemberInfo` structure must be signed by MGM member info key.

### Notary
Notary must explicitly advertize `MemberInfo.notaryServiceParty` when registering to MGM. `notaryServiceParty` is an equivalent of notary service identity in C4. Upon approval, MGM should update `NetworkParameters.notaries` accordingly.

Service identity may not be equal to primary identity and can be shared between multiple members (notary workers). There will no dedicated `MemberInfo` for service identity in this case. API must provide member lookup by `notaryServiceParty.owningKey`.

> The is no dedicated certificate for notary service identity. Only notary workers have certificates for their identities.

C5 will no longer support notary cluster on P2P layer. Instead, application layer (`NotaryFlow.Client`) should establish flow session directly to desired notary worker and implement balancing between notary workers.

> From P2P perspective, notary worker is just a regular group member, which can establish end-to-end communications with other members.

`notaryServiceParty.owningKey` should be a regular key. `NetworkParameters.notaries` will list the notary service parties with the keys being regular keys and matching `notaryServiceParty.owningKey` (one entry for each notary service, for notary services which consist od several workers the workers will be listed in the member list).

## API

### MemberInfo
| Field            | Flow API | RPC API |
| ---------------- | -------- | ------- |
| groupId          | YES      | YES     |
| party            | YES      | YES     |
| keys             | YES      | YES     |
| certificate      | NO       | YES     |
| endpoints        | NO       | YES     |
| platformVersion  | YES      | YES     |
| softwareVersion  | YES      | YES     |
| serial           | YES      | YES     |
| creationTime     | YES      | YES     |
| modificationTime | YES      | YES     |
| expiryTime       | YES      | YES     |
| status           | YES      | YES     |
| trackingNumber   | NO       | NO      |
| mgm              | NO       | NO      |
| ecdhKey          | NO       | NO      |
| sessionKey       | NO       | NO      |
| cpiVersion | NO | NO |
| notaryServiceParty | YES (ledger) | YES |
| roles | YES | YES |

## Signed structures (internal)

Signed structures are sent in internal flows between MGM and member. They are not exposed over API.

### SignedNetworkParameters
Similar to C4, but without certificate.

|      |                                                              |
| ---- | ------------------------------------------------------------ |
| C4   | `typealias SignedNetworkParameters = SignedDataWithCert<NetworkParameters>` |
| C5   | `typealias SignedNetworkParameters = SignedData<NetworkParameters>` |

**All signatures are over AMQP serialization format, as in C4.**

### SignedMemberInfo
`@CordaSerializable` structure similar to C4, but with different verification logic:

- Member key signatures are verified against member context, so you need to deserialize the whole structure and then serialize member context separately.
- Other signature(s) are considered as MGM and must be verified against the whole structure.

|      |                                                              |
| ---- | ------------------------------------------------------------ |
| C4   | `class SignedNodeInfo(val raw: SerializedBytes<NodeInfo>, val signatures: List<DigitalSignature>)` |
| C5   | `class SignedMemberInfo(val raw: SerializedBytes<MemberInfo>, val signatures: List<DigitalSignature.WithKey>)` |
