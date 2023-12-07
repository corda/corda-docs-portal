---
date: '2023-06-23'
lastmod: '2023-06-23'
section_menu: digitalcurrencies
menu:
  digitalcurrencies:
    name: "Working with Token Transfers"
    weight: 1200
    identifier: digital-currencies-tokens-transferring
    description: "Digital Currencies documentation describing how to transfer tokens via the GUI"
title: "Working with Token Transfers"
---

Once a participant has been [issued tokens]({{< relref "../issuing/_index.md" >}}), they can be involved in transfers. A transfer is the movement of tokens (value) between two or more entities (for example, wholesale banks, bank branches, retailers, retailer branches or franchises) on a Corda network to exchange goods and services. The transfer process can work both ways: both *push requests* and *pull requests* can be made.

* **Push request:** Participant A requests to send Participant B a number of tokens. Participant B confirms the amount and Participant A completes the transfer by signing the transaction which, in turn, alters the ownership of the tokens to Participant B. 
* **Pull request:** Participant A requests that Participant B send them a number of tokens. Participant B confirms, and transfers the tokens by signing the transaction which in turn alters the ownership of the tokens to Participant A.  

The following transfer methods are available:

* [Push transfer requests]({{< relref "creating-push-transfer-requests.md" >}})
* [Pull transfer requests]({{< relref "creating-pull-transfer-requests.md" >}})
* [Push transfers]({{< relref "performing-push-transfers.md" >}}) (send tokens without requiring approval)
  