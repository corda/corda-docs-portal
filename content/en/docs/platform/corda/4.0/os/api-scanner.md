---
aliases:
- /releases/release-V4.0/api-scanner.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-api-scanner
    parent: corda-os-4-0-contributing-index
    weight: 1050
tags:
- api
- scanner
title: Checking API stability
---


# Checking API stability

We have committed not to alter Corda’s API so that developers will not have to keep rewriting their CorDapps with each
new Corda release. The stable Corda modules are listed [here](corda-api.md#internal-apis-and-stability-guarantees). Our CI process runs an “API Stability”
check for each GitHub pull request in order to check that we don’t accidentally introduce an API-breaking change.


## Build Process

As part of the build process the following commands are run for each PR:

```shell
$ gradlew generateApi
$ .ci/check-api-changes.sh
```

This `bash` script has been tested on both MacOS and various Linux distributions, it can also be run on Windows with the
use of a suitable bash emulator such as git bash. The script’s return value is the number of API-breaking changes that it
has detected, and this should be zero for the check to pass. The maximum return value is 255, although the script will still
correctly report higher numbers of breaking changes.

There are three kinds of breaking change:


* Removal or modification of existing API, i.e. an existing class, method or field has been either deleted or renamed, or
its signature somehow altered.
* Addition of a new method to an interface or abstract class. Types that have been annotated as `@DoNotImplement` are
excluded from this check. (This annotation is also inherited across subclasses and sub-interfaces.)
* Exposure of an internal type via a public API. Internal types are considered to be anything in a `*.internal.` package
or anything in a module that isn’t in the stable modules list [here](corda-api.md#internal-apis-and-stability-guarantees).

Developers can execute these commands themselves before submitting their PR, to ensure that they haven’t inadvertently
broken Corda’s API.


## How it works

The `generateApi` Gradle task writes a summary of Corda’s public API into the file `build/api/api-corda-<version>.txt`.
The `.ci/check-api-changes.sh` script then compares this file with the contents of `.ci/api-current.txt`, which is a
managed file within the Corda repository.

The Gradle task itself is implemented by the API Scanner plugin. More information on the API Scanner plugin is available [here](https://github.com/corda/corda-gradle-plugins/tree/master/api-scanner).


## Updating the API

As a rule, `api-current.txt` should only be updated by the release manager for each Corda release.

We do not expect modifications to `api-current.txt` as part of normal development. However, we may sometimes need to adjust
the public API in ways that would not break developers’ CorDapps but which would be blocked by the API Stability check.
For example, migrating a method from an interface into a superinterface. Any changes to the API summary file should be
included in the PR, which would then need explicit approval from R3.

{{< note >}}
If you need to modify `api-current.txt`, do not re-generate the file on the master branch. This will include new API that
hasn’t been released or committed to, and may be subject to change. Manually change the specific line or lines of the
existing committed API that has changed.

{{< /note >}}
