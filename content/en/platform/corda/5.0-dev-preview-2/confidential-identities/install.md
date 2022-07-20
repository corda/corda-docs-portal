---
date: '2020-09-10'
title: "Installation"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-confidential-identities-install
    weight: 100
    parent: corda-5-dev-preview-1-confidential-identities
section_menu: corda-5-dev-preview

---

To install Confidential Identities, build the Confidential Identities SDK against the master branch with the following commands:

```console
git clone https://github.com/corda/corda5-confidential-identities.git
git fetch
git checkout origin release/2.0
```

{{< note >}}
Checkout the version of Confidential Identities you wish to install. In the example above `release/2.0` is used.
{{< /note >}}

Then run `./gradlew clean install` from the root directory.

## What's inside Confidential Identities

The Confidential Identities SDK is a single `.cpk`:

* **ci-workflows**, which contains the flows for creating and syncing confidential identities.
