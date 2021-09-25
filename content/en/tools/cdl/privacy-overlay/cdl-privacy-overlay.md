---
title: Privacy Overlay
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-views"
    identifier: "cdl-privacy-overlay"
    weight: 16

tags:
- cdl
- cordapp design language
- ledger evolution
- cordapp diagram
---

# The Privacy Overlay

Privacy is a key consideration when designing CorDapps. In most use cases Parties on the ledger will want to keep their Corda states representing private deals, asset, permission tokens etc.. private. There are normally two aspects to this:

* Keeping states private from the network operator, this avoids one (centralised) node holding all information about the activity on the network.
* Keeping states private from other Parties on the network who are not entitled to see the states, ie they we're part of the deal.

In this section, you will discover how to use a Privacy Overlay over the Ledger Evolution view to highlight the privacy characteristics of a CorDapp design.

To illustrate the Privacy Overlay, a Billing mechanism is brought into the Agreement example explored in the Smart Contract and Ledger Evolution sections.
