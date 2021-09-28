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
**Your feedback helps** -
Please [give us feedback](https://r3dev.zendesk.com/hc/en-us/requests/new) so we can make the upcoming versions of Corda work harder for you than ever.
{{< /note >}}

## In this developer preview

Intended for local deployment, experimental development, and testing only, this preview includes:

- A [modular API](../../../api-ref.html). Corda's core API module has been split into packages and versioned. Learn about [key APIs](cordapps/overview.md) and [Corda Services](cordapps/corda-services/overview.md), and find new [API reference documentation](../../../api-ref.html). Test it out with [updated code samples](../../../samples.html).

- [Dependency upgrades](getting-started/prerequisites.md) to Gradle 6, Java 11, and Kotlin 1.4. This enables the latest Gradle CorDapp packaging plugins, letting you create CorDapps faster.

- Node interaction upgrades. You can [interface with a node using HTTP](nodes/operating/operating-nodes-homepage.md) and [auto-generate CorDapp endpoints](nodes/operating/openapi.md).

- Upgrades to packaging:
  - A [Corda Package](packaging/overview.html#corda-package-files) (`.cpk`) is the unit of software that executes within a single sandbox.
  - [CorDapps](packaging/overview.html#corda-package-bundles) are a set of versioned `.cpks` that define a deployable application.

- A new [integration test framework](cordapps/integration-tests.md) that reflects real node behavior.

- An API for pluggable uniqueness service (notary). This is interface-only.

## Changes from Corda 4

Some features available in Corda 4 have been replaced with new functionality. These are:

- `MockNetwork`. You can now [use off-the-shelf testing frameworks](cordapps/integration-tests.md).
- Crash shell. This has been replaced with the [Corda Node CLI](nodes/operating/cli-curl/cli-curl.md).
- Driver DSL. This has been replaced with the [Corda CLI](corda-cli/overview.md).

This preview is not intended for commercial deployment, so it does not contain the functionality to create live networks.

See the [Corda 5 Developer Preview overview](../5.0-dev-preview-1.html) for more details.

## Known issues

There is a known issue with use of **anonymous classes in Java** when extending a flow.

{{< note >}}
This issue only has an impact when starting a subflow in Java, where the flow is an anonymous class.
{{< /note >}}

When extending a flow, such as `SignTransactionFlow` you may typically use an anonymous class, like:

```Java
SignedTransaction signedTransaction = flowEngine.subFlow(new SignTransactionFlow(counterpartySession) {
2
3            @Override
4            protected void checkTransaction(SignedTransaction stx) throws FlowException {
5
6            }
7        });
```
However, there is an issue which prevents this from working.


To work around this issue, use static classes in Java when starting subflows that require extending a flow.

For example, in the above case, use:

```Java
@Suspendable
2    @Override
3    public SignedTransaction call() throws FlowException {
4        SignedTransaction signedTransaction = flowEngine.subFlow(new MySignTransactionFlow(counterpartySession));
5        //Stored the transaction into data base.
6        return flowEngine.subFlow(new ReceiveFinalityFlow(counterpartySession, signedTransaction.getId()));
7    }
8
9    public static class MySignTransactionFlow extends SignTransactionFlow {
10
11        MySignTransactionFlow(FlowSession counterpartySession) {
12            super(counterpartySession);
13        }
14
15        @Override
16        protected void checkTransaction(@NotNull SignedTransaction stx) {
17
18        }
19    }
```

