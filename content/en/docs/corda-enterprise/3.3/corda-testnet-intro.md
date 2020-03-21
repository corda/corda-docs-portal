---
aliases:
- /releases/3.3/corda-testnet-intro.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-corda-testnet-intro
    parent: corda-enterprise-3-3-corda-networks-index
    weight: 1060
tags:
- corda
- testnet
- intro
title: The Corda Testnet
---


# The Corda Testnet


The Corda Testnet is an open public network of Corda nodes on the internet. It is designed to be a complement to *the* Corda Network where any entity can transact real world value with any other counterparty in the context of any application. The Corda Testnet is designed for “non-production” use in a genuine global context of Corda nodes, including but not limited to CorDapp development, multi-party testing, demonstration and showcasing of applications and services, learning, training and development of the Corda platform technology and specific applications of Corda.

The Corda Testnet is based on exactly the same technology as the main Corda Network, but can be joined on a self-service basis through the automated provisioning system described below.

The Corda Testnet is currently in private beta. Interested parties can request in invitation to join the Corda Testnet by completing a short request form (see below).


## Deploying a Corda node to the Corda Testnet

Access to the Corda Testnet is enabled by visiting [https://testnet.corda.network](https://testnet.corda.network).

[![testnet landing](/en/images/testnet-landing.png "testnet landing")](https://testnet.corda.network)
Click on “Join the Corda Testnet”.

Select whether you want to register a company or as an individual on the Testnet.

This will create you an account with the Testnet onboarding application which will enable you to provision and manage multiple Corda nodes on Testnet. You will log in to this account to view and manage you Corda Testnet identitiy certificates.

![testnet account type](/en/images/testnet-account-type.png "testnet account type")
Fill in the form with your details.

{{< note >}}
Testnet is currently invitation only. If your request is approved you will receive an email. Please fill in as many details as possible as it helps us prioritise. The approval process will take place daily by a member of the R3 operations team reviewing all invite requests and making a decision based on the current rate of onboarding of new customers.

{{< /note >}}
![testnet form](/en/images/testnet-form.png "testnet form")
{{< note >}}
We currently only support federated login using Google email accounts. Please ensure the email you use to register is a Gmail account or is set up as a Google account and that you use this email to log in.

Gmail is recommended. If you want to use a non-Gmail account you can enable your email for Google: [https://support.google.com/accounts/answer/176347?hl=en](https://support.google.com/accounts/answer/176347?hl=en)

{{< /note >}}
Once you have been approved, navigate to [https://testnet.corda.network](https://testnet.corda.network) and click on “I have an invitation”.

Sign in using the Google login service:

![testnet signin](/en/images/testnet-signin.png "testnet signin")
When prompted approve the Testnet application:

![testnet signin auth](/en/images/testnet-signin-auth.png "testnet signin auth")
{{< note >}}
At this point you may need to verify your email address is valid (if you are not using a Gmail address). If prompted check your email and click on the link to validate then return to the sign in page and sign in again.

{{< /note >}}
Next agree to the terms of service:

![testnet terms](/en/images/testnet-terms.png "testnet terms")
You can now copy the `ONE-TIME-KEY` and paste it into the parameter form of your cloud template.

![testnet platform clean](/en/images/testnet-platform-clean.png "testnet platform clean")
Your node will register itself with the Corda Testnet when it first runs and be added to the global network map and be visible to counterparties after approximately 5 minutes.


## A note on identities on Corda Testnet

Unlike the main Corda Network, which is designed for verified real world identities, The Corda Testnet automatically assigns a “distinguished name” as your identity on the network. This is to prevent name abuse such as the use of offensive language in the names or name squatting. This allows the provisioning of a node to be automatic and instantaneous. It also enables the same user to safely generate many nodes without accidental name conflicts. If you require a human readable name then please contact support and a partial organsation name can be approved.

