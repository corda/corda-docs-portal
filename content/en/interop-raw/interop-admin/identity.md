---
date: '2023-09-01'
title: "Interoperability Identities Endpoint"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-identity
    parent: corda5-interop-admin
    weight: 3000
section_menu: corda5
---

# The Interoperability Identities Endpoint

You can use the `getInterOpIdentities` endpoint to return a list of Interoperability identities visible to the specified holding identity.

The endpoint is invoked by calling the `GET` method on `/interop/{holdingIdentityShortHash}/interopidentities` where the
`holdingIdentityShortHash` is the short hash of the holding identity for which you want to return the Interoperability
identities. The response is a list of Interoperability identity objects.

Response message example:

```json
[
   {
      "x500Name":"O=CpiGroup1, L=London, C=GB",
      "groupId":"c0686ae6-a3c0-4c20-aeb2-233235322e4f",
      "owningVirtualNodeShortHash":"1750C7ECD7B4",
      "facadeIds":[
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v1.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         },
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v2.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         },
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v3.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         }
      ],
      "applicationName":"CpiGroup1",
      "endpointUrl":"<https://corda-p2p-gateway-worker.corda:8080>",
      "endpointProtocol":"1"
   },
   {
      "x500Name":"O=Gold, L=London, C=GB",
      "groupId":"13fae7c9-a234-4a7a-8613-375d663b158f",
      "owningVirtualNodeShortHash":"1750C7ECD7B4",
      "facadeIds":[
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v1.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         },
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v2.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         },
         {
            "owner":"org.corda.interop",
            "name":[
               "platform",
               "tokens"
            ],
            "version":"v3.0",
            "unversionedName":"org.corda.interop/platform/tokens"
         }
      ],
      "applicationName":"Gold",
      "endpointUrl":"<https://corda-p2p-gateway-worker.corda:8080>",
      "endpointProtocol":"1"
   }
]
```
