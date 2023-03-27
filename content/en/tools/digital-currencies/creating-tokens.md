---
date: '2023-03-21'
lastmod: '2023-03-21'
section_menu: tools
menu:
  tools:
    name: "Creating Tokens"
    weight: 900
    parent: digital-currencies-tokens-overview
    identifier: digital-currencies-creating-token-types
    description: "Digital Currencies documentation describing how to create tokens via the GUI"
title: "Creating Tokens"
---

Once a token definition has been created, new tokens of that type can be issued. Such tokens can then be used as for currency or utility purposes and allows the issuing party to maintain monetary policy and provide easily accessible digital currency tokens to specific entities.

<!-- Wholesale banks and financial institutions can deposit assets in exchange for tokens minted on the network. This process involves:

* A bank or financial institution requests a deposit in exchange for tokens, as described in *[Requesting Deposits](#requesting-deposits)*.
* A custodian approves the deposit request, as described in *[Accepting or Rejecting Deposit Requests](#accepting-or-rejecting-deposit-requests)*.
* The bank issues a payment to transfer collateral (off-ledger assets) to the custodian in exchange for the issuance of tokens, as described in *[Issuing Payments](#issuing-payments)*.
* The custodian accepts the payment, as described in *[Accepting or Rejecting Payments](#accepting-or-rejecting-payments)*.

-->

1. Click **Create Tokens** in the left-hand sidebar.

   The **Create Token** page is displayed:
   
   {{< 
      figure
	  src="images/create-tokens-page.png"
      width=40%
	  figcaption="Create Tokens Page"
	  alt="Create Tokens Page"
   >}}
   
   {{< note >}} If there are currently not active token definitions, then a message is displayed stating this. 
   {{</ note >}}
   
4. Specify the following values:

   * **Token Definition:** Select the relevant token definition (previously created as described in [Creating Token Definitions]({{< relref "creating-token-definitions.md" >}})).
   * **Amount:** Enter the number of token you want; for example *100*.
   
5. Click **Create**.
  

   The *Successfully submitted the creation of new tokens* message is displayed:
   
   {{< figure src="images/create-tokens-success-message.png" width=58% figcaption="'Successfully created tokens' Message" alt="'Successfully created tokens' Message" >}}

  
  