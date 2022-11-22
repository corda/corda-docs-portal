---
date: '2021-11-14'
title: "Support Bundles"
menu:
  corda-5-beta:
    parent: corda-5-beta-deploy-troubleshoot
    identifier: corda-5-beta-deploy-support-bundles
    weight: 2000
section_menu: corda-5-beta
---
<!--https://r3-cev.atlassian.net/browse/CORE-7232-->

This page describes how to gather the information required by R3 to assist you with troubleshooting in the event of an issue with a Kubernetes deployment.

## Set Kubernetes Context

Set Kubernetes context to use the namespace where Corda is installed by default. Replace `$CORDA_NAMESPACE` in the following command with your namespace name:

```shell
kubectl config set-context --current --namespace=$CORDA_NAMESPACE
```

## Collect Helm Release Configuration

* Get Corda Helm chart release name, version, and app version: `helm ls`
* Get custom values from Helm release: `helm get values release_name`
* Get manifest files from Helm release: `helm get manifest release_name`

## Collect Kubernetes Configuration and Events

* Get information from all Corda pods: `kubectl describe pods --selector app.kubernetes.io/name=corda`
* Get information from all Corda services: `kubectl describe services --selector app.kubernetes.io/name=corda`
* Get events: `kubectl get events`

## Collect Corda Logs

* Get list of Corda pods: `kubectl get pods --selector app.kubernetes.io/name=corda`
* Get logs for each pod: `kubectl logs pod_name`
* Get logs from any previous container that have already been deleted: `kubectl logs pod_name -p`
* Get worker's status: `kubectl port-forward pod_name 7000 & curl localhost:7000/status`

### Modifying the Log Level

You may be directed by R3 to increase the level of logging to aid problem determination.
This is achieved by modifying the deployment configuration YAML.
The logging level can be modified for all workers, for example:

```yaml
logging:
  level: "debug"
```

Or the logging level can be modified for one type of worker, for example:

```yaml
workers:
  db:
    logging:
      level: "trace"
```

Apply the modified configuration by upgrading the Helm release.
For example:

```shell
helm upgrade corda --namespace corda -f updated-values.yaml
```
