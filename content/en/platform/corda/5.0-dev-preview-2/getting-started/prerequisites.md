---
date: '2020-07-15T12:00:00Z'
title: "Prerequisites"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-prereqs
    weight: 1000
section_menu: corda-5-dev-preview
---

## Software prerequisites

Corda 5 DP 2 has been tested with the following:

| Software      | Description |
| ----------- | ----------- |
| Operating systems      | <li>Mac OS (intel and ARM)</li><li>Windows 10/11</li><li>Linux</li>     |
| Java   | Azul Zulu JDK 11 (Other versions should work but have not been extensively tested.)  |
| Intellij    | ~v2021.X.Y community edition   |
| git | ~v2.24.1    |
| Docker | Docker Engine ~v20.X.Y or Docker Desktop ~v3.5.X    |
| Gradle |  7.0+   |


If you want to experiment with multi-worker cluster deployments, you will also need:

* Kubernetes (incl. kubectl)
* Helm

However, Developer Preview 2 focuses on the developer rather than operator experience so [Kubernetes deployments](../../deploying/local-deployment) are not required to use Developer Preview 2.

## Hardware prerequisites

Most of the computers that we use to develop, build, and test Corda 5 have:

| Hardware      | Description |
| ----------- | ----------- |
| CPU      | Gen 9 Intel (6 cores / 12 threads)      |
| RAM   | 32GiB         |
| Hard disk   | At least 30GiB.        |

These are not minimum specifications.
This what is known to work with the code as of Developer Preview 2.
