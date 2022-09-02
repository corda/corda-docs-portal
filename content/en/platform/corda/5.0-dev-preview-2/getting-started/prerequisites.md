---
date: '2020-07-15T12:00:00Z'
title: "Prerequisites"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-setup
    identifier: corda-5-dev-preview-prereqs
    weight: 1000
section_menu: corda-5-dev-preview
---

## Corda software prerequisites

Corda 5 DP 2 has been tested with the following:

| Software      | Description |
| ----------- | ----------- |
| Operating systems      | An operating system based on x86 architecture.      |
| Java   | Azul 11.0.12 as Java runtime environment.  |
| Kotlin    | Kotlin plugin version 1.4.    |
| A docker daemon    | A command-line tool or Docker Desktop 3.5.    |
| Node databases    | H2 and Postgres13 (driver version 42.2.22 JDBC 42) for node databases.  |

## Corda hardware prerequisites

Corda 5 DP 2 has been tested with the following:

| Hardware      | Description |
| ----------- | ----------- |
|       |      |



## CorDapp development software prerequisites

CorDapp development has been tested with the following:

| Software      | Description |
| ----------- | ----------- |
| Operating systems      | <li>Windows 10</li><li>MacOS Catalina</li><li>Linux (Ubuntu 20.04.04)</li>      |
| IDE      | For example, Intellij IDEA(from JetBrains) with Gradle.      |
| Java      | You can compile and test CorDapps against these JDKs:<li> Azul11.0.12</li> <li> AdoptOpenJDK-J9</li>     |
| Gradle    | Packaging and bundling CorDapps requires Gradle 6.0 or above.    |



Docker desktop/docker engine

To deploy our Corda cluster in this example Kubernetes is used, you will need to have installed:

Kubernetes (installed locally)

kubectl

Helm


##  CorDapp development hardware prerequisites

CorDapp development has been tested with the following:

| Hardware      | Description |
| ----------- | ----------- |
| CPU      | Intel/AMD CPU with 8 or virtual cores / threads      |
| RAM   | 32GiB         |
| Hard disk   | 30GiB        |
