---
aliases:
- /releases/release-V3.2/contributing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-2:
    identifier: corda-os-3-2-contributing
    parent: corda-os-3-2-release-process-index
    weight: 1030
tags:
- contributing
title: Contributing
---


# Contributing

Corda is an open-source project and we welcome contributions. This guide explains how to contribute back to Corda.



## Identifying an area to contribute

There are several ways to identify an area where you can contribute to Corda:


* Browse issues labelled as `HelpWanted` on the
[Corda JIRA board](https://r3-cev.atlassian.net/issues/?jql=labels%20%3D%20HelpWanted)
    * Any issue with a `HelpWanted` label is considered ideal for open-source contributions
    * If there is a feature you would like to add and there isn’t a corresponding issue labelled as `HelpWanted`, that
doesn’t mean your contribution isn’t welcome. Please reach out on the Corda Slack channel (see below) to clarify


* Check the [Corda GitHub issues](https://github.com/corda/corda/issues)
    * It’s always worth checking in the Corda Slack channel (see below) whether a given issue is a good target for your
contribution. Someone else may already be working on it, or it may be blocked by an on-going piece of work


* Ask in the [Corda Slack channel](https://slack.corda.net/)


## Making the required changes


* Create a fork of the master branch of the [Corda repo](https://github.com/corda/corda)
* Clone the fork to your local machine
* Make the changes, in accordance with the [code style guide](codestyle.md)


## Testing the changes


### Running the tests

Your changes must pass the tests described [here](testing.md).


### Building against the master branch

You may also want to test your changes against a CorDapp defined outside of the Corda repo. To do so, please follow the
instructions [here](building-against-master.md).


## Merging the changes back into Corda


* Create a pull request from your fork to the master branch of the Corda repo
* Complete the pull-request checklist in the comments box:> 

* State that you have run the tests
* State that you have included JavaDocs for any new public APIs
* State that you have included the change in the [changelog](changelog.md) and
[release notes](release-notes.md) where applicable
* State that you are in agreement with the terms of
[CONTRIBUTING.md](https://github.com/corda/corda/blob/master/CONTRIBUTING.md)



* Request a review from a member of the Corda platform team via the [Corda Slack channel](https://slack.corda.net/)
* Wait for your PR to pass all four types of continuous integration tests (integration, API stability, build and unit)
* Currently, external contributors cannot see the output of these tests. If your PR fails a test that passed
locally, ask the reviewer for further details


* Once a reviewer has approved the PR and the tests have passed, squash-and-merge the PR as a single commit

