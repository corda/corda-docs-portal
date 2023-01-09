---
date: '2021-09-21'
title: "Deploying"
menu:
  corda-5-beta:
    identifier: corda-5-beta-deploy
    weight: 3050
section_menu: corda-5-beta
---
Corda 5 Beta is intended for deployment to a Kubernetes cluster using Amazon Elastic Kubernetes Service (EKS).
As part of the release, R3 delivers Docker images and Helm charts to aid the deployment process.
For each deployment, you must create a YAML file to define a set of Helm overrides for that environment.
The deployment and its configuration process is described in the [Tutorials section](deployment-tutorials/deploy-corda-cluster.html).
{{< note >}}
For testing purposes, you can deploy locally to the [combined worker](../introduction/key-concpets.html#combined-worker), as described in the [Getting Started section](..developing/getting-started/running-your-first-cordapp/run-first-cordapp.html).
{{< /note >}}