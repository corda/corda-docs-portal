---
aliases:
- /enm-components.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-enm-components
    parent: cenm-1-3-concepts-and-overview
    weight: 30
tags:
- enm
- components
title: Components of the Corda Enterprise Network Manager
---


# Components of the Corda Enterprise Network Manager

At the highest level, the CENM suite is deployed as shown in the following diagram:

![enm high level](/en/images/enm-high-level.png "enm high level")
The three main components of the CENM suite are


* **The Identity Manager**
* **The Network Map**
* **The Signing Service**

These, in conjunction, allow for the operation of a Corda network, the Registration and Certificate
Authority that control access to the zone, and the operation of the location service
that allow nodes to find one another under the governance of an agreed set of consensus rules.


## The Identity Manager

The Identity Manager has two main aspects that control the identity of Nodes within a Corda Network. The
first is the issuance of that identity, essentially the provision of a certificate that pairs an X500 legal
name with a public key. The second is the revocation of those certificates when the controlling identity
requests it. Both aspects should have appropriate controls put in place that enforce the policies
of the Zone operator, these can be enabled through the use of Workflow Plugins that allow external
workflow management tools to be used to capture those processes in a formal way.

This can be thought of as the Registration Authority for the Corda network represented by the deployed CENM software.

{{< warning >}}
**The Identity Manager cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.**
{{< /warning >}}


## The Signing Service

The signing service is responsible for the actual signing of various materials within a Zone. These include


* Identity Certificates
* Revocation lists
* Network Parameters
* Network Maps

It is recommended that any keys utilised by the zone are stored within Hardware Security Modules (HSMs), with
the Signing Service configured to sign entities on either a schedule or on direct user access.

This can be thought of as the Certificate Authority for the Corda network represented by the deployed CENM software.


## The Network Map

Acts as a location service for nodes once they have an identity granted to them by the Zone Operator. Additionally,
by joining a network, a node is agreeing to a set of parameters that dictate the rules for how consensus over the
zone is achieved. As such,the most important of those is a list of trusted notary services.

A zone can play host to any number of these sets of consensus rules, each forming a distinct sub zone within the
main zone as a whole.

{{< warning >}}
**The Network Map cannot be redirected. Only HTTP OK (response code 200) is supported - any other kind of response codes, including HTTP redirects (for example, response code 301), are NOT supported.**
{{< /warning >}}

# The Workflow

The Identity Manager’s issuance and revocation services both support plugins to model the workflow of approving certificate issuance/revocation. This enables zone operators to use a provided workflow, such as JIRA, or develop their own workflow. Ultimately a request is either accepted or rejected. Certain
elements can only be signed once a request has been approved and put into an accepted state, such as a CSR request.

“Out of the box” the CENM suite supports either a Jira based workflow or one that “ApprovesAll”. However, the
latter should only be used under very strict testing scenarios as it blindly approves all requests made to
the services.

Accepting a CSR is a statement by the operator of a network that they agree the request is from the Legal
Identity it claims to be and that they are welcome to join the network. Once accepted, they will be issued a signed certificate that has a signing chain back to the trust root.

{{< note >}}
The policies put in place around this process are intentionally left to the discretion of a network operator
as they are best placed to work out the level to which they need to conduct legal identity verification.

{{< /note >}}
Accepting a CRR is the opposite of accepting a CSR, it is a request to revoke a Legal Identities issued certificate (
often at the request of that legal identity). Thus, checks must be in place to prevent abuse of this system.


# Databases

The Identity Manager and Network Map(s) require their own persistence layer. The CENM suite supports in production
environments:


* Oracle database
* Postgres
* SQL Server

For details of supported versions and configuration, see [CENM Databases](database-set-up.md).


# Public Key Infrastructure (PKI)

The certificates and keys that represent the network’s PKI will be stored within an HSM. To prevent any breach of the
systems integrity being able to generate a signed certificate the signers should be operated from an isolated network.
By design, they only have the ability to talk *to* the other CENM components, they can never be asked to sign something.

In addition, signing a CRR or CSR, and potentially the Network Parameters, *should* require a human to interact with
the HSM via some manual authentication mechanism.

See [Certificate Hierarchy Guide](pki-guide.md) for a detailed guide to PKI.


# The Node

Run by entities who wish to join the network, a node submits it’s Legal Identity to the Identity Manager for approval.
On success, it will receive a PKI certificate linking that legal identity with its public key. It will then use that
certificate to sign it’s Node Info (detailing it’s externally addressable location on the internet) and submit that to
the Network Map.
