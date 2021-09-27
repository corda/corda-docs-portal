---
date: '2020-09-08T12:00:00Z'
title: "Corda 5 Developer Preview release notes"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-release-notes
    weight: 50
    name: "Release notes"
section_menu: corda-5-dev-preview
---

The Corda 5 Developer Preview, released on 28 September 2021, showcases the core features of the upcoming Corda 5.0 release to invite feedback.

{{< note >}}
**Your feedback helps** -
Please [give us feedback](https://r3dev.zendesk.com/hc/en-us/requests/new) so we can make the upcoming versions of Corda work harder for you than ever.
{{< /note >}}

Intended for local deployment, experimental development, and testing only, this preview includes:

- A [modular API](../../../api-ref/_index.md). Corda's core API module has been split into packages and versioned. Learn about [key APIs](cordapps/overview.md) and [Corda Services](cordapps/corda-services/overview.md), and find new [API reference documentation](../../../api-ref/_index.md). Test it out with [updated code samples](../../../samples/_index.md).

- [Dependency upgrades](getting-started/prerequisites.md) to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.

- Node interaction upgrades. You can [interface with a node using HTTP](nodes/operating/operating-nodes-homepage.md) and [auto-generate CorDapp endpoints](nodes/operating/openapi.md).

- Upgrades to packaging:
  - A [Corda Package](packaging/overview.md#corda-package-files) (`.cpk`) is the unit of software that executes within a single sandbox.
  - [CorDapps](packaging/overview.md#corda-package-bundles) are a set of versioned `.cpks` that define a deployable application.

- A new [integration test framework](cordapps/integration-tests.md) that reflects real node behavior.

- An API for pluggable uniqueness service (notary). This is interface-only.


Some features available in Corda 4 have been replaced with new functionality. These are:

- `MockNetwork`. You can now [use off-the-shelf testing frameworks](cordapps/integration-tests.md).
- Crash shell. This has been replaced with the [Corda Node CLI](nodes/operating/cli-curl).
- Driver DSL. This has been replaced with the [Corda CLI](corda-cli/overview.md).

This preview is not intended for commercial deployment, so it does not contain the functionality to create live networks.

See the [Corda 5 Developer Preview overview](../5.0-dev-preview-1) for more details.

