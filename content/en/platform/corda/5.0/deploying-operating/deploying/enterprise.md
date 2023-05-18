---
date: '2023-05-11'
title: "Migrating to Corda Enterprise"
menu:
  corda5:
    parent: corda5-cluster-deploy
    identifier: corda5-cluster-enterprise
    weight: 4000
section_menu: corda5
---
# Migrating to Corda Enterprise {{< enterprise-icon >}} 

To migrate an existing Corda Community deployment to Corda Enterprise, you must replace the existing Corda Community Helm chart with the Enterprise Helm chart. This replaces the standard container images with the Enterprise container images.

{{< note >}}
The migration process results in downtime for the Corda cluster. 
{{< /note >}}

The configuration used for the Corda Enterprise installation should be the same as that for the original Corda Community installation. In particular, it should be given access to the same database instance and Kafka cluster so that it can pick up the state from the previous cluster. It also must be provided with the same salt and passphrase so that it can decrypt the configuration stored in the database.

Assuming an existing Corda OS installation with a Helm release name of HELM_RELEASE_NAME in the namespace KUBERNETES_NAMESPACE installed with the overrides in the file values.yaml, the process is as follows: