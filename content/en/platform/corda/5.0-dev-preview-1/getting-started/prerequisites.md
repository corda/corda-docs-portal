---
date: '2020-07-15T12:00:00Z'
title: "Third-party software prerequisites"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-gettingstarted
    weight: 100
project: corda-5
section_menu: corda-5-dev-preview
---

The following third-party software is required to build and run the Corda 5 Developer Preview.

## Operating systems

The Corda 5 Developer Preview requires an operating system based on x86 architecture.

## Java

The Corda 5 Developer Preview requires [Azul11.0.12](https://www.azul.com/downloads/?package=jdk) as Java runtime environment.

As a CorDapp developer, you can compile and test your Corda 5 Developer Preview CorDapps against these JDKs:

* [Azul11.0.12](https://www.azul.com/downloads/?package=jdk)
* [AdoptOpenJDK-J9](https://adoptopenjdk.net/releases.html?variant=openjdk11&jvmVariant=openj9)

## Deployment

You can deploy the Corda 5 Developer Preview locally using the [Corda CLI](../corda-cli/overview.md) tool and a docker daemon, such as a command-line tool or Docker Desktop 3.5.

## Packaging CorDapps

You can package and bundle CorDapps with the Corda CPK (Corda package file - `.cpk`) and CPB (Corda package bundle - `.cpb`) [plugins](../packaging/gradle-plugin/overview.md), which require Gradle 6.0 or above. Alternatively, you can create CorDapp package bundles (`.cpb` files) with the [CorDapp Builder](../packaging/cordapp-builder.md).

## Node databases

You can use H2 and Postgres13 (driver version 42.2.22 JDBC 42) for node databases in the Corda 5 Developer Preview.
