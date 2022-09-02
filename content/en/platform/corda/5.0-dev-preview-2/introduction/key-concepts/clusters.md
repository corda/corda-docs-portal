---
date: '2020-07-15T12:00:00Z'
title: "Clusters"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-key-concepts
    weight: 9500
section_menu: corda-5-dev-preview
---

Clusters allow members on multiple networks thanks to multi-tenancy support. Corda 5 supports multiple Corda identities operating in the same cluster via virtual nodes. A virtual node is linked to a CPI and acts as a single member in a network once registration has been completed. A cluster allocates resources on a per-virtual node basis and ensures that code executing in the context of a particular virtual node is sandboxed away from other virtual nodes and platform code.

*Note about what's available in DP 2 (no cloud deployments, no multi-cluster) and what's coming soon*
