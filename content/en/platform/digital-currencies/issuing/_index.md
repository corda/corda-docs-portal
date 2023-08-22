---
date: '2023-07-04'
lastmod: '2023-07-04'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Working with Token Issuance"
    weight: 700
    identifier: digital-currencies-token-issuance
    description: "Digital Currencies documentation describing how to issue token definitions via the GUI"
title: "Working with Token Issuance"
---

Once [tokens have been minted]({{< relref "../minting/_index.md" >}}), tokens of that type can be issued. Issuing tokens involves transferring them to the relevant entities.  

The general process of issuance, and the on-ledger actions involved will be very similar, if not identical, for both CBDCs and for stablecoins. However, the permissions of these on-ledger actions may be divided differently based on implementation. For example, in {{< tooltipdc >}}CBDC{{< /tooltipdc >}} issuance, the custodian and the token issuing entity will both be a central bank, while these roles may be divided for a stablecoin.

This section describes the actions associated with token issuance. It contains the following:

{{< childpages >}}