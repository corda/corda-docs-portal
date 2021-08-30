---
date: '2020-07-15T12:00:00Z'
title: "Technology overview"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-technology
    weight: 100
project: corda-5
section_menu: corda-5-dev-preview
---

# Technology overview

This page outlines the technologies required to run Corda 5 Developer Preview.

## Operating systems

Corda 5 Developer Preview can be run on the following operating systems.

* MacOS 10.15 and above (Intel processors only)
* Windows 10
* Ubuntu 20.04

## Java

Corda 5 Developer Preview can be run with the following Java versions.

* [Azul11.0.12](https://www.azul.com/downloads/?package=jdk)
* [AdoptOpenJDK-J9](https://adoptopenjdk.net/releases.html?variant=openjdk11&jvmVariant=openj9)

## Deployment

Deployment can be performed using the [corda-cli](XXX) tool and Docker Desktop 3.5.

## Packaging

CorDapps can be packaged and bundled with the [Corda CPK and CPB plugins](XXX), which require Gradel 6.6 or above. [CorDapp Builder](XXX) can also be used to create bundles.

## Node databases

H2 and Postgres13 (driver version 42.2.22 JDBC 42 for Postgress) can be used for node databases in Corda 5 Developer Preview.
