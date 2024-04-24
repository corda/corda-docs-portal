---
description: "Learn the fundamental key concepts of Corda 5.3."
title: "Fundamentals"
date: 2023-04-21
menu:
  corda53:
    identifier: corda53-fundamentals
    parent: corda53-key-concepts
    weight: 1000
---
# Fundamentals

Corda offers a single, global, source of truth that can be shared by multiple untrusting individuals.
Corda provides this by utilizing a {{< tooltip >}}distributed ledger{{< /tooltip >}}.
{{< tooltip >}}DLT{{< /tooltip >}} has the following characteristics:

* A distributed ledger is a database of facts that are replicated, shared, and synchronized across multiple participants on a network.
* A participant is known as an {{< tooltip >}}identity{{< /tooltip >}} and represents a real-world {{< tooltip >}}entity{{< /tooltip >}} within the context of an {{< tooltip >}}application network{{< /tooltip >}}.
* Each identity has a different view of the ledger, depending on the facts it shares.
* Identities that share a fact must reach a {{< tooltip >}}consensus{{< /tooltip >}} before it is committed to the ledger.
* All identities always see the exact same version of any on-ledger facts they share.

You can learn more about the fundamental key concepts of Corda in the following sections:
{{< childpages >}}
