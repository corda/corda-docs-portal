---
date: '2021-11-07'
title: "Support Bundles"
menu:
  corda-5-alpha:
    parent: corda-5-alpha-deploy-troubleshoot
    identifier: corda-5-alpha-deploy-support-bundles
    weight: 2000
section_menu: corda-5-alpha
---
<!--https://r3-cev.atlassian.net/browse/CORE-7232-->

In the event of an issue, you need to know what information R3 requires from you to be able to perform problem determination. This collection of information is referred to as a support bundle. The following document lists the steps to troubleshoot a Corda deployment in Kubernetes and collect the support material.

## Set Kubernetes Context

Set Kubernetes context to use the namespace where Corda is installed by default. Replace `$CORDA_NAMESPACE` in the following command by your namespace name:

```
kubectl config set-context --current --namespace=$CORDA_NAMESPACE
```

## Collect Helm Material

* Get Corda Helm chart release name, version, and app version: `helm ls`
* Get custom values from Helm release: `helm get values release_name`
* Get manifest files from Helm release: `helm get manifest release_name`

## Collect Kubernetes Material

* Get information from all Corda pods: `kubectl describe pods --selector app.kubernetes.io/name=corda`
* Get information from all Corda services: `kubectl describe services --selector app.kubernetes.io/name=corda`
* Get events: `kubectl get events`

## Collect Application Logs

* Get list of Corda pods: `kubectl get pods --selector app.kubernetes.io/name=corda`
* Get logs for each pod: `kubectl logs pod_name`
* Get logs from any previous container that have already been deleted: `kubectl logs pod_name -p`
* Get workers status: `kubectl port-forward pod_name 7000 & curl localhost:7000/status`
