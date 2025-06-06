---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-corda-nodes-configuring
    name: "Configuring a node"
    parent: corda-enterprise-4-12-corda-nodes
tags:
- node
- naming
title: Node identity
weight: 40
---

# Node identity

A node’s name must be a valid X.509 distinguished name. In order to be compatible with other implementations
(particularly TLS implementations), we constrain the allowed X.509 name attribute types to a subset of the minimum
supported set for X.509 certificates (specified in RFC 3280), plus the locality attribute:


* Organization (O)
* State (ST)
* Locality (L)
* Country (C)
* Organizational-unit (OU)
* Common name (CN)

Note that the serial number is intentionally excluded from Corda certificates in order to minimise scope for uncertainty in
the distinguished name format. The distinguished name qualifier has been removed due to technical issues; consideration was
given to “Corda” as qualifier, however the qualifier needs to reflect the Corda compatibility zone, not the technology involved.
There may be many Corda namespaces, but only one R3 namespace on Corda. The ordering of attributes is important.

`State` should be avoided unless required to differentiate from other `localities` with the same or similar names at the
country level. For example, London (GB) would not need a `state`, but St Ives would (there are two, one in Cornwall, one
in Cambridgeshire). As legal entities in Corda are likely to be located in major cities, this attribute is not expected to be
present in the majority of names, but is an option for the cases which require it.

The name must also obey the following constraints:


* The `organisation`, `locality`, and `country` attributes are present.
* The `state`, `organisational-unit`, and `common name` attributes are optional.
* The maximum number of characters in the whole x500 name string is 128 characters.
* The fields of the name have character lengths **less** than the following maximum values:

    * Common name: 64
    * Organisation: 128
    * Organisation unit: 64
    * Locality: 64
    * State: 64



* The `country` attribute is a valid *ISO 3166-1<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>* two letter code in upper-case. See the list of [defined country codes](https://github.com/corda/corda/blob/release/os/4.12/tools/worldmap/src/main/resources/net/corda/worldmap/cities.txt).
* The `organisation` field of the name obeys the following constraints:

    * Has at least two letters



* All data fields adhere to the following constraints:

    * Upper-case first letter
    * Does not include the following characters: `,`, `=`, `+`, `$`, `"`, `'`, `\`
    * Is in NFKC normalization form
    * Does not contain the null character
    * Only the Latin, common and inherited unicode scripts are supported
    * No double-spacing
    * No leading or trailing whitespace




This is to avoid right-to-left issues, debugging issues when we can’t pronounce names over the phone, and
character confusability attacks.

{{< note >}}
The network operator of a Corda Network may put additional constraints on node naming in place.

{{< /note >}}

## External identifiers

Mappings to external identifiers such as Companies House numbers, LEI, BIC, etc. should be stored in custom X.509
certificate extensions. These values may change for operational reasons, without the identity they’re associated with
necessarily changing, and their inclusion in the distinguished name would cause significant logistical complications.
The OID and format for these extensions will be described in a further specification.
