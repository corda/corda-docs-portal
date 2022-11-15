---
date: '2022-14-11'
title: "Kubernetes Cluster"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-deploy-local
    parent: corda-5-alpha-deploy-options
    weight: 2000
section_menu: corda-5-alpha
---
Corda 5 Alpha is intended for deployment to a Kubernetes cluster using Amazon Elastic Kubernetes Service (EKS).
As part of the release, R3 delivers Docker images and Helm charts to aid the deployment process.
For each deployment, you must create a YAML file to define a set of Helm overrides for that environment. 
The deployment and its configuration process is described [here](../deployment-tutorials/tutorial-k8s.html) in the Tutorials section.
