---
date: '2021-08-16'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-membership-group-manager-overview
    weight: 200
title: Network structure
---



Corda lets you create private networks of people who want to communicate. You can do this by creating a membership group, which is maintained by a membership group manager (MGM). The MGM then distributes a JSON file containing the list of members and other relevant details. All of the group members can then exchange messages or transact.


## Glossary

| Term                     |Definition
|-----------------------------|---------------------------------------------------------------|
| Membership group (or group) | A set of members who can communicate with each other.         |
| Membership group manager    | The member responsible for maintaining the membership group   |
| `MemberInfo`                | A data structure that represents an individual member.                                                               |
| `MembershipGroupCache`   | A service that stores information about group members.   |
| CorDapp Package (.cpk)   | A bundle of CorDapps, which includes a dependency tree and version information.   |
| CorDapp Packaged Installation file (CPI)  | A single distributable file, which contains `.cpk`s and group information.   |
| Corda Package Bundle (CPB) | A collection of versioned `.cpk`s that define a deployable application.   |



## Structure
All group members can communicate with each other. The membership group manager (MGM) determines who is in the group, and the group's rules. The MGM distributes this information to the group using flows.

The membership group information consists of:
- MGM details distributed in a `.json` file, as part of the CPI.
- Dynamically-updated data distributed by the MGM via flows:
  - The list of members (`memberinfo`)
  - The network parameters (`NetworkParameters`)

### Structure layout and namespace
`NetworkParameters`, `MemberInfo`, and the CPI are structured as loosely-coupled key-value pairs. Keys created by the Corda platform are always prefixed with `corda.`

You can define your own keys and namespaces.


### CPI structure
The CPI contains three key elements.

- The `.cpk`. A `.cpk` file is essentially a `jar` file with a `.cpk` file extension. The file extension contains an OSGi bundle and its dependent bundles (excluding
  any bundles provided by Corda or other `.cpk`s). `.cpk`s have a `.zip` format, contain a `META-INF/MANIFEST.MF` file, and can be signed by Java's `jarsigner` tool. A CPK should contain a signed OSGi bundle at its root, containing the CorDapp's contracts, flows, and service classes. Designate this bundle as the main `.jar`. Any library dependencies are stored in the `.cpk`s `lib/` folder. These dependencies should also be OSGi bundles, and (as already mentioned) do not include any `.cpk` dependencies that this CorDapp may have.

- The CPB. CPBs contain the definitions of the flow and ledger layer required to operate the application, such as MGM roles and network parameters. They also contain unique versions of the `.cpk`s that define the application as a whole. It is an unsigned bundle without deployment-specific information. The same bundle can be used for QA and production.

- The CPI bundle. This has deployment-specific information in the metadata. It contains MGM details in a JSON file, unless you are bootstrapping a network without MGM.

## CPI MGM contents
The CPI distributes MGM details to group members in a JSON file. These include:
- `identityTrustStore: KeyStore?` - Trust roots for identity certificates. If there is no public key infrastructure (PKI), you can use `null` for a `NoPKI` option.
- `tlsTrustStore: KeyStore` - Trust roots for the transport layer service (TLS).
- `mgmInfo: MemberInfo` - MGM member info.
- `identityPKI: String?` - which PKI to use for identities, see below. Values: `Standard`, `Corda4`, `NoPKI`. Default: `Standard`.
- `identityKeyPolicy: String?` - whether to use combined or distinct keys for ledger signing and end-to-end session authentication, see below. Values: `Combined`, `Distinct`. Default: `Combined`.
- `cipherSuite: Map<String, String>` - cipher suite parameters, see https://github.com/corda/platform-eng-design/blob/master/core/corda-5/corda-5.0/cipher-suite/cipher-suite-definition.md#definition-in-cpi for more details

## Version information
`MemberInfo` replaced `NodeInfo` in Corda 5.0.

## Related content
[Network parameters](network-parameters.md)
[TLS](tls.md)
[Identity](identity.md)

