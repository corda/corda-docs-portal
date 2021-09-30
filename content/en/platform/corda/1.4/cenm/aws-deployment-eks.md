---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-aws-deployment-guide
tags:
- config
- AWS
title: CENM Deployment AWS/EKS
weight: 100
---

# CENM Deployment with AWS/EKS

You can use the [PKI tool](pki-tool.md) to create a set of keys and certificates, which must be shared between all CENM services through the use of a shared file system.

In AWS this is achieved via the AWS Elastic Filesystem (EFS).

## Steps

There are three main steps to complete this deployment:

1. Create an EKS cluster.
2. Create an EFS.
3. Deploy EFS Provisioner on the EKS cluster.

Once complete, you can continue with your CENM deployment tasks, such as establishing your network services.

## Create EKS

Create an EKS cluster with at least 10-12 GB of free RAM.

{{< note >}}
CENM has been tested on the following EKS cluster option: `Managed nodes – Linux`
{{< /note >}}

## Create EFS

For performance reasons, you should use the same region as the one used for the EKS cluster.

{{< note >}}
The following steps are guidelines. Your bespoke network may require additional options and details - please adjust the steps according to your requirements.
{{< /note >}}

1. Click `Create file system`
2. Click `Customize`
    1. Choose the name of your file system
    2. Encryption: disable
    3. Adjust all the other options according to your needs
    4. Click `Next`
3. Network
    1. Virtual Private Cloud (VPC)
        1. VPC: select the one used for the EKS cluster
    1. Mount targets
        1. Availability zone: default
        1. Subnet ID: default
        1. IP address: default
        1. Security groups: add the main primary Security Group which is shown as "Cluster security group" in the Cluster configuration, "Networking" tab within the AWS UI management console
    1. Click `Next`
1. File system policy (optional)
    1. Leave empty
    1. Click `Next`
1. Review and create
    1. Click `Create`

Once the EFS has been created, click on it and choose "Access points".

1. Click `Create access point`
    1. Details
        1. Choose `Name` (optional)
        1. Root directory path: `/`
    1. POSIX user:
        1. User ID: 1000
        1. Group ID: 1000
        1. Secondary group IDs: leave empty
    1. Root directory creation permissions:
        1. Owner User ID: 1000
        1. Owner Group ID: 1000
        1. Permissions: 0777
    1. Click `Create access point`

## Deploy EFS Provisioner on the EKS cluster

### Modify efs.yaml

Use the command line for the following steps:

1. Provide a correct value for the EFS file system ID field.
2. Specify the correct region of your EFS file system:

```bash
...
kind: ConfigMap
...
data:
  file.system.id: [EFS file system ID]
  aws.region: [REGION]

...

kind: Deployment
...
      volumes:
        - name: pv-volume
          nfs:
            server: [EFS file system ID].efs.[REGION].amazonaws.com

```

```bash
kubectl create -f efs.yaml
```

Wait until the EFS provisioner gets bootstrapped - the example command is as follows:

```bash
kubectl get pods -o wide
```

### Create storage classes

For Azure, use the following file:

```bash
kubectl create -f storage-class-azure.yaml
```

For AWS use this file:

```bash
kubectl create -f storage-class-aws.yaml
```

## Complete CENM deployment

Your AWS deployment is complete. You can now [complete the rest of your CENM deployment process](_index.md).
