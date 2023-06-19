---
date: '2023-05-11'
version: 'Corda 5.0 Beta 4'
title: "Migrating to Corda Enterprise"
menu:
  corda5:
    parent: corda5-cluster-deploy
    identifier: corda5-cluster-enterprise
    weight: 4000
section_menu: corda5
---
# Migrating to Corda Enterprise {{< enterprise-icon >}} 

This section describes how to migrate an existing Corda deployment to Corda Enterprise by replacing the existing Corda Helm chart with the Enterprise Helm chart. 
{{< note >}}
The configuration used for the Corda Enterprise installation should be the same as that for the original Corda installation. In particular, the configuration must grant access to the same database instance and Kafka cluster so that it can pick up the state from the previous cluster. It also must use the same salt and passphrase so that Corda can decrypt the configuration stored in the database.
{{< /note >}}
The following steps migrate an existing Corda deployment to Corda Enterprise, where the existing deployment has a Helm release name of `HELM_RELEASE_NAME` in the namespace `KUBERNETES_NAMESPACE`, installed with the overrides in the file `values.yaml`:

{{< warning >}}
The migration process results in downtime for the Corda cluster. 
{{< /warning >}}

1. Uninstall the Corda Helm release:

   ```
   helm uninstall $HELM_RELEASE_NAME --namespace $KUBERNETES_NAMESPACE
   ```

2. Install the Corda Enterprise Helm release using the same values as the previous Corda installation but disabling automatic bootstrapping:

   ```
   helm install corda-enterprise corda-enterprise-5.0.0.tgz \
     --values values.yaml --namespace $KUBERNETES_NAMESPACE \
     --set bootstrap.db.enabled=false \
     --set bootstrap.kafka.enabled=false \
     --set bootstrap.rbac.enabled=false
   ```  

If the original Corda installation used automatic bootstrapping to generate the salt and passphrase, the installation of Corda Enterprise must also be configured with the location of the generated values in the Kubernetes secret `$HELM_RELEASE_NAME}-config`. For example:
```
helm install corda-enterprise corda-enterprise-5.0.0.tgz \
  --values values.yaml --namespace $KUBERNETES_NAMESPACE \
  --set bootstrap.db.enabled=false \
  --set bootstrap.kafka.enabled=false \
  --set bootstrap.rbac.enabled=false \
  --set config.encyption.salt.valueFrom.secretKeyRef.name="${HELM_RELEASE_NAME}-config" \
  --set config.encyption.salt.valueFrom.secretKeyRef.key="salt" \
  --set config.encyption.passphrase.valueFrom.secretKeyRef.name="${HELM_RELEASE_NAME}-config" \
  --set config.encyption.passphrase.valueFrom.secretKeyRef.key="passphrase"
  ```