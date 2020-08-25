---
aliases:
- /head/contributing.html
- /HEAD/contributing.html
- /contributing.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-5:
    identifier: corda-os-4-5-contributing
    parent: corda-os-4-5-contributing-index
    weight: 1020
tags:
- contributing
title: How to contribute
---


# How to contribute



## Identifying an area to contribute

There are several ways to identify an area where you can contribute to Corda:


* The easiest is just to message one of the [Community Maintainers](contributing-philosophy.md#community-maintainers) saying “I want to help!”. They’ll work
with you to find an area for you to contribute
* If you have a specific contribution in mind, confirm whether the contribution is appropriate first by reaching out in the
`#contributing` channel of the [Corda Slack](http://slack.corda.net/) or contacting one of the
[Community Maintainers](contributing-philosophy.md#community-maintainers) directly
* If you do not have a specific contribution in mind, you can also browse the issues labelled as `help wanted` on the
[Corda GitHub issues](https://github.com/corda/corda/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22) page
    * Issues that additionally have the `good first issue` label are considered ideal for first-timers




## Contribution guidelines

We believe one of the things that makes Corda special is its coherent design and we seek to retain this defining characteristic. From the
outset we defined some guidelines to ensure new contributions only ever enhance the project:


* **Quality**: Code in the Corda project should meet the [Corda coding style guidelines](codestyle.md), with sufficient test-cases,
descriptive commit messages, evidence that the contribution does not break any compatibility commitments or cause adverse feature
interactions, and evidence of high-quality peer-review
* **Size**: The Corda project’s culture is one of small pull-requests, regularly submitted. The larger a pull-request, the more likely it
is that you will be asked to resubmit as a series of self-contained and individually reviewable smaller PRs
* **Scope**: We try to ensure the Corda project remains coherent and focused so we ask that the feature’s scope is within the definition
specified in the [Corda Technical Whitepaper](/en/pdf/corda-technical-whitepaper.pdf)
* **Maintainability**: If the feature will require ongoing maintenance (eg support for a particular brand of database), we may ask you to
accept responsibility for maintaining this feature
* **Non-duplicative**: If the contribution duplicates features that already exist or are already in progress, you may be asked to work with
the project maintainers to reconcile this. As the major contributor to Corda, many employees of [R3](https://r3.com) will be working on
features at any given time. To avoid surprises and foster transparency,
[our Jira work tracking system is public](https://r3-cev.atlassian.net/projects/CORDA/summary). If in doubt, reach out to one of the
[Community Maintainers](contributing-philosophy.md#community-maintainers)

In addition, there are a number of additional requirements that apply to ["large" contributions](contributing.md#large-contributions).

## Making the required changes

You should make your changes as follows:


* Create a fork of the [Corda repo](https://github.com/corda/corda)
* Clone the fork to your local machine
* Build Corda by following the instructions [here](building-corda.md)
* Be sure to work from the appropriate branch for your changes, as per the section below.
* Make the changes, in accordance with the [code style guide](codestyle.md)


### Selecting a development branch

Corda does not use the *master* branch for development. Instead, all development work is done on the branch named
according to the release that it represents. The following pattern is used for branch naming:
*release/os/{major version}.{minor version}*

Note that *release* is always part of the name of the branch, even for unreleased versions of Corda. The default
github branch will always be the current development branch of Corda. Development work should target the default branch
unless the work is needed in a specific version of Corda. In that case, development work should target the oldest version
of Corda for which the work would be appropriate. For instance, if a pull request would be applicable to Corda 4.1 and
Corda 4.3, it would be appropriate to open a pull request for *release/os/4.1*. That work would then be merged forward
from *release/os/4.1* to *release/os/4.3*. If the work is only applicable to Corda 4.3, a pull request need only be
opened against release/os/4.3.


### Things to check


* **Make sure your error handling is up to scratch:** Errors should not leak to the UI. When writing tools intended for end users, like the
node or command line tools, remember to add `try`/`catch` blocks. Throw meaningful errors. For example, instead of throwing an
`OutOfMemoryError`, use the error message to indicate that a file is missing, a network socket was unreachable, etc. Tools should not
dump stack traces to the end user
* **Look for API breaks:** We have an automated checker tool that runs as part of our continuous integration pipeline and helps a lot, but
it can’t catch semantic changes where the behavior of an API changes in ways that might violate app developer expectations
* **Suppress inevitable compiler warnings:** Compiler warnings should have a `@Suppress` annotation on them if they’re expected and can’t
be avoided
* **Remove deprecated functionality:** When deprecating functionality, make sure you remove the deprecated uses in the codebase
* **Avoid making formatting changes as you work:** In Kotlin 1.2.20, new style guide rules were implemented. The new Kotlin style guide is
significantly more detailed than before and IntelliJ knows how to implement those rules. Re-formatting the codebase creates a lot of
diffs that make merging more complicated
* **Things to consider when writing CLI apps:** Make sure any changes to CLI applications conform to the [CLI UX Guide](cli-ux-guidelines.md)


### Extending the flow state machine

If you are interested in extending the flow state machine, you can find instructions on how to do this
[here](contributing-flow-state-machines.md).


## Testing the changes

You should test your changes as follows:


* **Add tests**: Unit tests and integration tests for external API changes must cover Java and Kotlin. For internal API changes these
tests can be scaled back to Kotlin only
* **Run the tests**: Your changes must pass the tests described [here](testing.md)
* **Perform manual testing**: Before sending that code for review, spend time poking and prodding the tool and thinking, “Would the
experience of using this feature make my mum proud of me?”. Automated tests are not a substitute for dogfooding
* **Build against the selected development branch**: You can test your changes against CorDapps defined in other repos by following the instructions
[here](building-against-non-release.md)
* **Run the API scanner**: Your changes must also not break compatibility with existing public API. We have an API scanning tool which
runs as part of the build process which can be used to flag up any accidental changes, which is detailed [here](api-scanner.md)


## Updating the docs

You should document any changes to Corda’s public API as follows:


* Add comments and javadocs/kdocs. API functions must have javadoc/kdoc comments and sentences must be terminated
with a full stop. We also start comments with capital letters, even for inline comments. Where Java APIs have
synonyms (e.g. `%d` and `%date`), we prefer the longer form for legibility reasons. You can configure your IDE
to highlight these in bright yellow
* Update the relevant .rst file(s)
* Include the change in the [Release Notes](release-notes.md) if the change is external and therefore visible to CorDapp
developers and/or node operators
* [Build the docs locally](building-the-docs.md) and check that the resulting .html files (under `docs/build/html`) for the modified
render correctly
* If relevant, add a sample. Samples are one of the key ways in which users learn about what the platform can do.
If you add a new API or feature and don’t update the samples, your work will be much less impactful


## Merging the changes back into Corda

You should merge the changes back into Corda as follows:


* Create a pull request from your fork to the equivalent branch of the Corda repo
* In the PR comments box:



* Complete the pull-request checklist:
    * [ ] Have you run the unit, integration and smoke tests as described here? [https://docs.corda.net/head/testing.html](https://docs.corda.net/head/testing.html)
    * [ ] If you added/changed public APIs, did you write/update the JavaDocs?
    * [ ] If the changes are of interest to application developers, have you added them to the Release Notes?
    * [ ] If you are contributing for the first time, please read the agreement in CONTRIBUTING.md now and add to this
Pull Request that you agree to it.


* Add a clear description of the purpose of the PR
* Add the following statement to confirm that your contribution is your own original work: “I hereby certify that my contribution is in
accordance with the Developer Certificate of Origin ([https://developercertificate.org/](https://developercertificate.org/)).”



* Request a review by reaching out in the `#contributing` channel of the [Corda Slack](http://slack.corda.net/) or contacting one of
the [Community Maintainers](contributing-philosophy.md#community-maintainers) directly
* The reviewer will either:



* Accept and merge your PR
* Leave comments requesting changes via the GitHub PR interface
    * You should make the changes by pushing directly to your existing PR branch. The PR will be updated automatically





* (Optional) Open an additional PR to add yourself to the
[contributors list](https://github.com/corda/corda/blob/master/CONTRIBUTORS.md)

* The format is generally `firstname surname (company)`, but the company can be omitted if desired


## Large contributions

A “large” contribution is one that meets one or more of the following criteria:

* It would require users to modify or recompile their CorDapps.
* It would introduce a new user-facing feature or configuration option.
* It would negatively impact performance or security (e.g. by introducing a new dependency).
* It would take a long time to implement - two weeks or more.
* It would significantly increase the project’s QA or support costs.

Large contributions can be disruptive - both for users of the Corda platform, and for platform developers who are modifying the same parts of the software as part of the established product roadmap. In addition, the work of reviewing and maintaining these contributions diverts the team’s resources from other efforts. Generally, it is more effective to put in a feature request via the [corda-dev mailing list](https://groups.io/g/corda-dev) instead.

The process for contributing a large change to Corda is as follows:

1. Raise a discussion of your proposed contribution on the [corda-dev mailing list](https://groups.io/g/corda-dev).

    * Please search the [mailing list archives](https://groups.io/g/corda-dev/topics) first for similar proposals that may have been discussed and declined in the past.

    * You will need to provide evidence that you are capable of delivering a large change to the platform. This can be done by contributing smaller changes to Corda first, or by otherwise showing your ability and commitment to delivering large changes to complex, established projects.

2. The project maintainers will feed back on your proposal. Some of the criteria they will be evaluating the proposal against include:

    * The contribution is/is not aligned with Corda’s mission statement (as outlined in the [Corda Introductory Whitepaper](https://www.r3.com/white-papers/the-corda-platform-an-introduction-whitepaper/)).

    * The contribution will/will not negatively impact the ability of R3 and other project contributors to deliver improvements to the platform.

    * The contribution will/will not require the project maintainers to have access to proprietary hardware or software resources.

    * The contribution will/will not impact the project’s QA or support costs.

3. If the proposal is accepted, please raise a design PR on the [Corda GitHub project](https://github.com/corda/corda). The design should give the rationale for the change, how the change will be implemented, and what alternative designs were rejected. The engineering team will review your design and indicate any required changes.

4. Once the design is approved, please go ahead with the change according to the [guidelines for small and medium contributions](contributing.md#making-the-required-changes). In addition to those guidelines, we require that large contributions be fully exercised by tests, including any exception paths and error handling.


## Developer Certificate of Origin

All contributions to this project are subject to the terms of the Developer Certificate of Origin, available
[here](https://developercertificate.org/) and reproduced below:

```none
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
1 Letterman Drive
Suite D4700
San Francisco, CA, 94129

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
