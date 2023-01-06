---
date: '2023-01-05'
title: "Support Bundles"
menu:
  corda-5-beta:
    parent: corda-5-beta-deploy-troubleshoot
    identifier: corda-5-beta-deploy-support-bundles
    weight: 2000
section_menu: corda-5-beta
---
<!--https://r3-cev.atlassian.net/browse/CORE-7232-->

This page describes how to gather the information required by R3 to assist you with troubleshooting in the event of an issue with a Corda deployment on Kubernetes.

1. Set the Kubernetes context to use the namespace where Corda is installed by default.

    ```shell
    kubectl config set-context --current --namespace=$CORDA_NAMESPACE
    ```

    Where `$CORDA_NAMESPACE` is the name of the namespace into which Corda is deployed.

2. Gather the required information either:

    * [via the provided scripts](#creating-a-support-bundle-using-scripts), or
    * [manually](#manually-gathering-information-for-support).

## Creating a Support Bundle Using Scripts

1. Obtain the bundle creation script [support_bundle.sh](https://raw.githubusercontent.com/corda/corda-runtime-os/release/os/5.0/support_bundle.sh)(Bash) or [support_bundle.ps1](https://raw.githubusercontent.com/corda/corda-runtime-os/release/os/5.0/support_bundle.ps1)(PowerShell) from GitHub, or from Customer Hub.

2. Execute the script to generate a `.tar` or a `.zip` file containing the support information in the current directory:

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```shell
   ./support_bundle.sh
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   .\support_bundle.ps1
   {{% /tab %}}
   {{< /tabs >}}

## Manually gathering information for support

1. Collect the Corda Helm chart release name, version, and app version:

    ```shell
    helm ls
    ```

2. Collect custom values and the manifest for the Helm release for Corda:

    ```shell
    helm get values $RELEASE_NAME
    helm get manifest $RELEASE_NAME
    ```

    Where `$RELEASE_NAME` is the name of the Helm release for Corda.

3. Collect information from all Corda pods:

    ```shell
    kubectl describe pods --selector app.kubernetes.io/name=corda
    ```

4. Collect information from all Corda services:

    ```shell
    kubectl describe services --selector app.kubernetes.io/name=corda
    ```

5. Collect Kubernetes events:

    ```shell
    kubectl get events
    ```

6. Collect logs and status for the Corda pods:

    1. Get the list of Corda pods:

        ```shell
        kubectl get pods --selector app.kubernetes.io/name=corda
        ```

    2. For each pod in the list, collect logs, previous logs, and worker status:

        ```shell
        kubectl logs $POD_NAME
        kubectl logs -p $POD_NAME
        kubectl port-forward $POD_NAME 7000 &
        curl localhost:7000/status
        ```

        Where `$POD_NAME` is a Corda pod name from the list.

## Modifying the Log Level

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
