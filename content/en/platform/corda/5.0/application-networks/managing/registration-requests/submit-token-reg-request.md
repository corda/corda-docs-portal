---
date: '2023-04-07'
title: "Submitting a Token in a Registration Request"
menu:
  corda-5:
    identifier: corda-5-submit-token
    parent: corda-5-networks-pre-auth
    weight: 3000
section_menu: corda-5
---

After you have [generated a pre-auth token]({{< relref "pre-auth/preauthenticating-tokens.md#creating-a-token" >}}), you can distribute this to a registering member through offline channels, outside of Corda. 
The registering member must then include this pre-auth token in the registration request they submit when registering. To do this, an additional key must be set in the registration context. This key is `corda.auth.token`, and the value of this key must be the pre-auth token that the MGM provided.

For example, taking this sample registration request context as a base:

```bash
 {
 "corda.session.key.id": "CD432EA37B69",
 "corda.session.key.signature.spec": "SHA256withECDSA",
 "corda.ledger.keys.0.id": "4A37E41B63A7",
 "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
 "corda.endpoints.0.connectionURL": "https://alice.corda.com:8080",
 "corda.endpoints.0.protocolVersion": "1"
}
```

If the MGM operator generated and distributed the token `8d738966-07f0-456b-bc0e-19e61d7b90a3`, the member submits the following registration context:

```bash
 {
 "corda.session.key.id": "CD432EA37B69",
 "corda.session.key.signature.spec": "SHA256withECDSA",
 "corda.ledger.keys.0.id": "4A37E41B63A7",
 "corda.ledger.keys.0.signature.spec": "SHA256withECDSA",
 "corda.endpoints.0.connectionURL": "https://alice.corda.com:8080",
 "corda.endpoints.0.protocolVersion": "1",
 "corda.auth.token": "8d738966-07f0-456b-bc0e-19e61d7b90a3"
}
```