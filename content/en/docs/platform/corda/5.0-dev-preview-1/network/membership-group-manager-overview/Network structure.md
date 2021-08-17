---
date: '2021-08-16'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-test-directory-index
    name: Test Directory Child 2
title: Corda 5 Dev Preview Test Directory Child 2
weight: 200
---


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

**CorDapp Package (.cpk)**

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
The CPI is made up of three key elements.

- The `.cpk`. A `.cpk` file is essentially a `jar` file with a `.cpk` file extension. The file extension contains an OSGi bundle and its dependent bundles (excluding
  any bundles provided by Corda or other `.cpk`s). `.cpk`s have a `.zip` format, contain a `META-INF/MANIFEST.MF` file, and can be signed by Java's `jarsigner` tool. A CPK should contain a signed OSGi bundle at its root, containing the CorDapp's contracts, flows, and service classes. Designate this bundle as the main `.jar`. We designate this bundle as the "main" `.jar`. Any library dependencies are stored in the `.cpk`s `lib/` folder. These dependencies should also be OSGi bundles, and (as already mentioned) do not include any CPK dependencies that this CorDapp may have.

- **CPB**, as defined by https://github.com/corda/platform-eng-design/pull/330 - unsigned bundle without deployment specific information. The same bundle can be used for QA and production.
- **CPI** - bundle with deployment specific information in metadata. It contains MGM details JSON file, which content is described below. Group properties may be omitted when bootstrapping without MGM. Definition of other CPI metadata is outside the scope of this document.

### MGM details JSON
MGM details are represented as a JSON file. This file is distributed to group members only as a part of CPI.
- `identityTrustStore: KeyStore?` - Trust roots for identity certificates. Null for `NoPKI` option.
- `tlsTrustStore: KeyStore` - Trust roots for TLS.
- `mgmInfo: MemberInfo` - MGM member info.
- `identityPKI: String?` - which PKI to use for identities, see below. Values: `Standard`, `Corda4`, `NoPKI`. Default: `Standard`.
- `identityKeyPolicy: String?` - whether to use combined or distinct keys for ledger signing and end-to-end session authentication, see below. Values: `Combined`, `Distinct`. Default: `Combined`.
- `cipherSuite: Map<String, String>` - cipher suite parameters, see https://github.com/corda/platform-eng-design/blob/master/core/corda-5/corda-5.0/cipher-suite/cipher-suite-definition.md#definition-in-cpi for more details





