---
aliases:
- /head/testing.html
- /HEAD/testing.html
- /testing.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-enterprise
    parent: corda-enterprise-4-13-cordapps
    weight: 1040
tags:
- testing
title: Testing your changes
---


# Testing your changes


## Automated tests

Corda has a suite of tests that any contributing developers must maintain and extend when adding new code.

There are several test suites:


* **Unit tests**: These are traditional unit tests that should only test a single code unit, typically a method or class.
* **Integration tests**: These tests should test the integration of small numbers of units, preferably with mocked out services.
* **Smoke tests**: These are full end to end tests which start a full set of Corda nodes and verify broader behaviour.
* **Other**: These include tests such as performance tests, stress tests, etc, and may be in an external repo.


### Running the automated tests

These tests are mostly written with JUnit and can be run via `gradle`:

   {{< tabs name="tabs-2" >}}
   {{% tab name="Unix" %}}
   ```shell
   ./gradlew test integrationTest smokeTest
   ```
   {{% /tab %}}
   {{% tab name="macOS" %}}
   ```shell
   ./gradlew test integrationTest smokeTest
   ```
   {{% /tab %}}
   {{% tab name="Windows" %}}
   ```shell
   gradlew test integrationTest smokeTest
   ```
   {{% /tab %}}
   {{< /tabs >}}
Before creating a pull request please make sure these pass.


## Manual testing

You should manually test anything that would be impacted by your changes. The areas that usually need to be manually tested and when are
as follows:


- **Node startup:** Changes in the `node` or `node:capsule` project in both the Kotlin or Gradle or the `cordformation` gradle plugin.
- **Sample project:** Changes in the `samples` project; for example, changing the IRS demo means you should manually test the IRS demo.
- **Explorer:** Changes to the `tools/explorer` project.

How to manually test each of these areas differs and is currently not fully specified. For now the best thing to do is to ensure the
program starts, that you can interact with it, and that no exceptions are generated in normal operation.


## Running tests in IntelliJ

R3 recommends editing your IntelliJ preferences so that you use the Gradle runner - this means that the quasar utils
plugin will make sure that some flags (like `-javaagent` - see below) are
set for you.

To switch to using the Gradle runner:

1. Navigate to **Build, Execution, Deployment -> Build Tools -> Gradle -> Runner** (or search for **runner**).
    * Windows: This is in “Settings”
    * macOS: This is in “Preferences”
2. Set **Delegate IDE build/run actions to gradle** to true.
3. Set **Run test using:** to **Gradle Test Runner**.


If you would prefer to use the built-in IntelliJ JUnit test runner, you can add some code to your `build.gradle` file and
it will copy your quasar JAR file to the lib directory.

{{< note >}}
Before creating the IntelliJ run configurations for these unit tests
go to Run -> Edit Configurations -> Defaults -> JUnit, add
`-javaagent:lib/quasar.jar`
to the VM options, and set Working directory to `$PROJECT_DIR$`
so that the `Quasar` instrumentation is correctly configured.

{{< /note >}}
Add the following to your `build.gradle` file - ideally to a `build.gradle` that already contains the quasar-utils plugin line:

```groovy
apply plugin: 'net.corda.plugins.quasar-utils'

task installQuasar(type: Copy) {
    destinationDir rootProject.file("lib")
    from(configurations.quasar) {
        rename 'quasar-core(.*).jar', 'quasar.jar'
    }
}
```

and then you can run `gradlew installQuasar`.
