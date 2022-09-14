---
date: '2021-04-24T00:00:00Z'
title: "application"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-api-application
    parent: corda-5-dev-preview-api
    weight: 1000
section_menu: corda-5-dev-preview
---
The `corda-application` module provides the fundamental building blocks required to create a [flow](../../introduction/key-concepts.html#flows) and so all CorDapps use this module.

`corda-application` sits at a higher level in the module hiarachy and exposes the following modules as API dependencies:

- `corda-base`.
- `corda-crypto`.
- `corda-membership`.
- `corda-serialization`.

By depending on `corda-application`, your Cordapp does not need to directly depend on the modules listed above.
