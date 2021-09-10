---
date: '2021-09-08'
menu:
corda-5-dev-preview:
identifier: corda-5-dev-preview-1-network
weight: 100
project: corda-5
section_menu: release-notes
title: Release notes
---

The Corda 5 Developer Preview, released on 27 September 2021, showcases the core features of the upcoming Corda 5.0 release to invite feedback:

- A [Modular API](xxx). Corda's core API module has been split into packages and versioned. You can experiment with this using [updated code samples](xxx).

- [Dependency upgrades](xxx) to Gradle 6, Java 11, and Kotlin 1.4.

- Node interaction upgrades. You can [interface with a node using HTTP](xxx) and [auto-generate CorDapp endpoints](xxx).

- Upgrades to packaging:
   - A [Corda Package](xxx) (`.cpk`) is the unit of software that executes within a single sandbox.
  - [CorDapps](xxx) are a set of versioned `.cpks` that define a deployable application.

 - A new [integration test framework](xxx) that reflects real node behavior.

- An API for pluggable uniqueness service (notary). This is interface-only.


Some features available in Corda 4 have been deprecated. These are:

- `MockNetwork`. You can now [use off-the-shelf testing frameworks](xxx).
- Crash shell. This has been replaced with the [Node CLI](xxx).
- Driver DSL. This has been replaced with the [Corda CLI](xxx).

See the [Corda 5 Developer Preview overview](xxx) for more details.
