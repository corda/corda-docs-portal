---
date: '2020-09-08T12:00:00Z'
title: "Release notes"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-release-notes
    weight: 001
project: corda-5
section_menu: corda-5-dev-preview
---

The Corda 5 Developer Preview, released on 27 September 2021, showcases the core features of the upcoming Corda 5.0 release to invite feedback. Intended for local deployment, experimental development, and testing only, this preview includes:

- A [Modular API](xxx). Corda's core API module has been split into packages and versioned. Learn about [key APIs](xxx) and [Corda Services](xxx), and find new [API reference documentation](xxx). Test it out with [updated code samples](xxx).

- [Dependency upgrades](xxx) to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.

- Node interaction upgrades. You can [interface with a node using HTTP](xxx) and [auto-generate CorDapp endpoints](xxx).

- Upgrades to packaging:
  - A [Corda Package](xxx) (`.cpk`) is the unit of software that executes within a single sandbox.
  - [CorDapps](xxx) are a set of versioned `.cpks` that define a deployable application.

- A new [integration test framework](xxx) that reflects real node behavior.

- An API for pluggable uniqueness service (notary). This is interface-only.


Some features available in Corda 4 have been replaced with new functionality. These are:

- `MockNetwork`. You can now [use off-the-shelf testing frameworks](xxx).
- Crash shell. This has been replaced with the [Node CLI](xxx).
- Driver DSL. This has been replaced with the [Corda CLI](xxx).

This preview is not intended for commercial deployment, so it does not contain the functionality to create live networks.

See the [Corda 5 Developer Preview overview](xxx) for more details.
