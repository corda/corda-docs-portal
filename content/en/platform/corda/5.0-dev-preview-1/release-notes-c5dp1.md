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

The Corda 5 Developer Preview, released on 28 September 2021, showcases the core features of the upcoming Corda 5.0 release to invite feedback, and give you a chance to experiment with some of the new aspects of future Corda 5 releases.

{{< note >}}
**Your feedback helps.** Please [send the Documentation Team an e-mail](mailto:docs@r3.com) with your feedback so we can make the upcoming versions of Corda work harder for you than ever.
{{< /note >}}

## Corda 5 Developer Preview 1.0.1

Corda 5 Developer Preview 1.0.1 fixes the security issue caused by the Apache Log4j 2 dependency. In this fix, the Log4j dependency is updated to version v2.17.1.

### Fixed issues

* The Log4j dependency has been updated to version 2.17.1 to fix pre-existing Log4j issues.

## Corda 5 Developer Preview 1.0

Intended for local deployment, experimental development, and testing only, this preview includes:

- A [modular API](../../../../en/api-ref.html). Corda's core API module has been split into packages and versioned. Learn about [key APIs](../../../../en/platform/corda/5.0-dev-preview-1/cordapps/overview.md) and [Corda Services](../../../../en/platform/corda/5.0-dev-preview-1/cordapps/corda-services/overview.md), and find new [API reference documentation](../../../../en/api-ref.html). Test it out with [updated code samples](../../../../en/samples.html).

- [Dependency upgrades](../../../../en/platform/corda/5.0-dev-preview-1/getting-started/prerequisites.md) to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.

- Node interaction upgrades. You can [interface with a node using HTTP](../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/operating-nodes-homepage.md) and [auto-generate CorDapp endpoints](../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/openapi.md).

- Upgrades to packaging:
  - A [Corda Package](../../../../en/platform/corda/5.0-dev-preview-1/packaging/overview.html#corda-package-files) (`.cpk`) is the unit of software that executes within a single sandbox.
  - [CorDapps](../../../../en/platform/corda/5.0-dev-preview-1/packaging/overview.html#corda-package-bundles) are a set of versioned `.cpb` (Corda package bundle) files that define a deployable application.

- A new [integration test framework](../../../../en/platform/corda/5.0-dev-preview-1/cordapps/integration-tests.md) that reflects real node behavior.

## Changes from Corda 4

Some features available in Corda 4 have been replaced with new functionality. These are:

- `MockNetwork`. You can now [use off-the-shelf testing frameworks](../../../../en/platform/corda/5.0-dev-preview-1/cordapps/integration-tests.md).
- Crash shell. This has been replaced with the [Corda Node CLI](../../../../en/platform/corda/5.0-dev-preview-1/nodes/operating/cli-curl/cli-curl.md).
- Driver DSL. This has been replaced with the [Corda CLI](../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md).
- Network Bootstrapper. This has been replaced by the [Corda CLI](../../../../en/platform/corda/5.0-dev-preview-1/corda-cli/overview.md).

{{< warning >}}

IMPORTANT NOTE

The Corda 5 Developer Preview is not feature complete and is not intended for commercial deployment, so it does not contain the functionality to create live networks.

Please do not try to migrate Corda 4 CorDapps to the Corda 5 Developer Preview - this release is only intended as a means for testing CorDapps development as a proof of concept.

R3 does not and will not provide official support for this release.

{{< /warning >}}

See the [Corda 5 Developer Preview overview](../../../../en/platform/corda/5.0-dev-preview-1.html) for more details.

## Known issues

There is a known issue with use of **anonymous classes in Java** when extending a flow.

{{< note >}}
This issue only has an impact when starting a subflow in Java, where the flow is an anonymous class.
{{< /note >}}

When extending a flow, such as `SignTransactionFlow` you may typically use an anonymous class, like:

```Java
SignedTransaction signedTransaction = flowEngine.subFlow(new SignTransactionFlow(counterpartySession) {

    @Override
    protected void checkTransaction(SignedTransaction stx) throws FlowException {

    }
});
```
However, there is an issue which prevents this from working.


To work around this issue, use static classes in Java when starting subflows that require extending a flow.

For example, in the above case, use:

```Java
@Suspendable
@Override
public SignedTransaction call() throws FlowException {
    SignedTransaction signedTransaction = flowEngine.subFlow(new MySignTransactionFlow(counterpartySession));
    return flowEngine.subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
}

public static class MySignTransactionFlow extends SignTransactionFlow {

    MySignTransactionFlow(FlowSession counterpartySession) {
        super(counterpartySession);
    }

    @Override
    protected void checkTransaction(@NotNull SignedTransaction stx) {

    }
}
```
