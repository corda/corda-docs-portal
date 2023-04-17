---
date: '2023-04-14'
title: "Authentication"
menu:
corda-5-beta:
identifier: corda-5-beta-authentication
parent: corda-5-beta-developing-and-operating
weight: 2000
section_menu: corda-5-beta
---

When we discuss R3's permissions model, we are referring to the authorization aspect of the problem.
However, before we can authorize a user request, we must first authenticate the user to ensure
that they are indeed the person or system account they claim to be.

Such authentication can be performed using user name and password credentials or via single sign-on (SSO).
In the case of SSO, we delegate the authentication of REST users to a trusted SSO provider that the REST gateway is configured to use.
