---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Working with Token Redemption"
    weight: 1200
    parent: digital-currencies
    identifier: digital-currencies-token-redemption
    description: "Digital Currencies documentation describing how to redeem tokens via the GUI"
title: "Working with Token Redemption"
---


A participant, such as a commercial bank, can perform a *redemption*: exchange the tokens they possess for their collateral. For example, the participant may [create a redemption request]({{< relref "creating-redemption-requests.md" >}}) to redeem their tokens with a central bank if they require an end-of-day settlement in order to gain overnight interest on their collateral. 

This redemption request is sent to both the {{< tooltip >}}issuer{{< definitiondc term="issuer" >}}{{< /tooltip >}} and {{< tooltip >}}custodian{{< definitiondc term="custodian" >}}{{< /tooltip >}}. Depending on the token definition, the issuer checks the {{< tooltip >}}RTGS{{< definitiondc term="RTGS" >}}{{< /tooltip >}} balance off-ledger. 

If the collateral required to be redeemed can be supported, the issuer and custodian [approve the redemption request]({{< relref "approving-or-rejecting-redemption-requests.md" >}}). The custodian then performs an off-ledger movement of collateral into the participant's RTGS account or bank account. Simultaneously, the tokens are moved from the participant's vault to the issuer's vault when the participant [completes the redemption]({{< relref "completing-redemptions.md" >}}).

The issuer then has the option to [burn the tokens]({{< relref "../burning/_index.md" >}}).

{{< childpages >}}
