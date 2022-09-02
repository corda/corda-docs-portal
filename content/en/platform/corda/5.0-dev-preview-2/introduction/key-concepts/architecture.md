---
date: '2020-07-15T12:00:00Z'
title: "Layered architecture"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 900
section_menu: corda-5-dev-preview
---

High availability – Being able to operate Corda in a hot/hot, reliable way to provide high uptime.

Multi-tenancy – Support for ‘Virtual Corda Nodes’ to share a single Corda Installation to improve the Total Cost of Ownership (TCO) in certain scenarios. - two instances of same identity on the SAME instance Corda
a Corda instance can take part in multiple, unrelated, ‘Application Networks’,

* layer cake model - Corda 5 breaks the operational and developmental power of Corda into layers. Allowing you to choose the technologies that matter to you.
   * As a developer you can incrementally (bottom up) build your application by engaging with the appropriate layer when it is needed, this mental model is now more directly represented through our APIs.
   * As a developer you can test specific parts of your application independently (for example, mock a workflow).
   * As a developer you can decide not to use our implementation of the ledger model and go with your own persistence model etc. opening the platform up to new use cases.
   * Cherry on top, is our own development velocity as this gives us the ability to develop more rapidly (behind the interfaces and in parallel), introduce new implementations of the layers down the line etc.
* db schmema - enables persistance
* p2p
* Diagrams!!
