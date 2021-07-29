---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-aws-deployment-guide
tags:
- config
- AWS
title: Creating a new HSM using the AWS Console
weight: 200
---
# Creating a new HSM using the AWS Console

You can use the AWS Console - available online - to create a new HSM for generating encryption keys. To complete this process you will require login credentials for the AWS Console.

There are nine steps to create a new HSM:

1. Create a VPC (Virtual Private Cloud).
2. Create subnets under the VPC.
3. Create an Internet Gateway.
4. Create route tables per subnet.
5. Create, initialise, and activate the HSM.
6. Create security groups.
7. Create the EC2 instance.
8. Activate the HSM.
9. Code configuration.

{{< note >}}
This document follows the same steps as [the Amazon guide](https://docs.aws.amazon.com/cloudhsm/latest/userguide/getting-started.html)
and provides a lot of additional details. Please consult both documents for completeness.
{{< /note >}}

## Create a VPC

A VPC is basically a virtual network. The CloudHSM deployment resources will be created under this network.
To create a VPC:

1. Open the [AWS console](http://console.aws.amazon.com).
2. Log in.
3. Click **VPCs**.
4. Select the **Create VPC** option.
5. Provide an IP range for the network. At a later point you will split this network into subnetworks (at least 2), so make sure that you provide a sufficiently wide range for the IP addresses - for example, `10.0.0.0/16` should be fine.

## Create subnets under the VPC

For the CloudHSM to work, you need to create at least 2 subnets under the VPC (according to the AWS documentation).
These subnets will split the network into different groups.

To create subnets under the VPC:
1. Click **Create subnet**.
2. Provide the VPC - use the one already created.
3. Provide an Availability Zone (AZ), which determines where the subnet will reside. Choose one for now, but make sure that the two subnets are in different AZs.

4. Provide the IP range for the subnet. This should be a subset of the VPC's range (for example, `10.0.0.0/19`).

5. Once this subnet is created, repeat the steps above to create a second one with another IP subset of the VPC's range (for example, `10.0.128.0/20`).

## Create an Internet Gateway

An Internet Gateway enables communication between your VPC and the outside world (Internet).

At this stage of the setup, there are two subnets. They are in the same VPC so they can communicate with each other. As a result, only one of them needs to allow an SSH connection.

To create an Internet Gateway:

1. In the AWS console, go to **Internet Gateways**.
2. Create a new Internet Gateway with a new name.
3. Attach it to the VPC created earlier.

## Create route tables per subnet

A route table is required for each subnet. One of these route tables needs an explicit routing configuration - the rest can use the default settings.

By default, a route table is configured to have the VPC's IP range as *Destination*, and the local IP range as *Target*.
To ensure access to one of the subnets, add a new row that specifies `Destination` as your public IP (or `0.0.0.0/32` for all IPs),
and *Target* as the newly created Internet Gateway.

Leave the default settings for the rest of the route tables, and attach them to the subnets under the **Subnets** menu.

## Create, initialise, and activate the HSM

1. Go to [CloudHSM console](https://console.aws.amazon.com/cloudhsm/).
2. Create a cluster.
3. For VPC, provide the VPC created earlier.
4. For AZ, provide the subnet that does not have public access! This is **important** because the cluster should be accessible from the other subnet only, not from the Internet.
5. To proceed further, follow the
   [Official AWS documentation](https://docs.aws.amazon.com/cloudhsm/latest/userguide/getting-started.html)
   from the *Create an HSM* step onward.
6. This stage of the process is complete when the cluster UI shows **Initialized**.

## Create security groups

Security groups are used when EC2 Instances are created for subnets.
When creating HSM clusters, the connection on ports 2223 to 2225 will be open.
These ports will be used from the other subnet (the public one) to connect.
In addition, you must create one more Security Group where:
1. Port 22 is opened for a SSH connection.
2. **Type** is set to `SSH`.
3. **Protocol** is set to `TCP`.
4. **Source** can be set to `0.0.0.0/0`.

*Type* should be SSH, *Protocol* should be TCP and *Source* can be *0.0.0.0/0*

## Create the EC2 instance

At this stage of the setup, you need to create an EC2 instance
so that you can access the public subnet via this EC2 instance through SSH.

To do so:
1. Open the EC2 management console on AWS.
2. Click **Instances**.
3. Click **Launch Instance**.
4. Select an instance type - for example, Amazon Linux.
5. Set **VPC** to be the VPC you created.
6. Set **Subnet ID** to be the *PUBLIC SUBNET* you configured.
7. Set **Security Groups** to the one using SSH, and the one that the cluster created (its name is typically `cloudhsm-<clusterid>`).
   **IMPORTANT**: You must create an EC2 (virtual machine) for the *PUBLIC SUBNET* only! The *PRIVATE SUBNET*
   (which runs the HSM cluster) must be left as is - it is accessed via this machine.
8. When prompted, create a new key. Make sure that you download and save it - it is the only way to SSH to the box.
9. Launch the new EC2 instance.
10. Click **Connect**.
11. Run a command in the format shown below (replace the `<keyFile>` and `<publicIp>` placeholder parts):
    ```
    ssh -i "<keyFile>.pem" ec2-user@<publicIp>
    ```
12. You are now connected. In case of an error, make sure that the security groups, Internet Gateway, and routing are in place, and try again.


## Activate the HSM

The last stage in the setup process is to download the HSM tools.

To do so:
1. Run the following command:

```
wget https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL6/cloudhsm-client-latest.el6.x86_64.rpm
```

2. Then run:

```
sudo yum install -y ./cloudhsm-client-latest.el6.x86_64.rpm
```

3. The CloudHSM utility has now been created. At this point you need to find out the IP of the HSM instance.
To do so, open the HSM console on the AWS UI and copy the **ENI IP address**.

4. Configure the utility by running:

```
sudo /opt/cloudhsm/bin/configure -a <ENI IP address>
```

5. Your `customerCA.crt` key file still needs to be copied to the EC2 instance. The CloudHSM utility will look for this key file in the
`/opt/cloudhsm/etc/` directory, however you do not have direct access to it.

    5.1. First copy the `customerCA.crt` key file to your home directory:
    ```
    scp -i "<keyFile>.pem" customerCA.crt ec2-user@<publicIp>:~/
    ```

    5.2. Then copy it to the `/opt` directory using `sudo`:

    ```
    sudo cp customerCA.crt /opt/cloudhsm/etc/customerCA.crt
    ```

6. The CloudHSM utility should start up with console output like the one in the example below:

```
[ec2-user@ip-10-0-3-174 ~]$ /opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
Ignoring E2E enable flag in the configuration file
Connecting to the server(s), it may take time
depending on the server(s) load, please wait...
Connecting to server '10.0.140.211': hostname '10.0.140.211', port 2225...
Connected to server '10.0.140.211': hostname '10.0.140.211', port 2225.
E2E enabled on server 0(10.0.140.211)
```

7. Change your password, as advised in [https://docs.aws.amazon.com/cloudhsm/latest/userguide/manage-hsm-users.html](https://docs.aws.amazon.com/cloudhsm/latest/userguide/manage-hsm-users.html).

## Code configuration

The `AmazonCloudHsmCryptoService` class implements the communication with the CloudHSM cluster.  
The configuration must include your credentials for the given cluster: a **CU** type user name, a password, and the partition name.  
In addition, a local certificate store must be present since CloudHSM does **not** store certificates due to safety precautions.

The relevant parts of an example PKI Tool configuration is shown below for reference:

```
   hsmLibraries = [
       {
           type = AMAZON_CLOUD_HSM
           jars = ["/opt/cloudhsm/java/cloudhsm-3.0.0.jar"]
           sharedLibDir = "/opt/cloudhsm/lib"
       }
   ]
   keyStores = {
       "example-hsm-key-store" = {
           type = AMAZON_CLOUD_HSM
           credentialsAmazon = {
                   partition = "<partition_name>"
                   userName = "<user_name>"
                   password = "<password>"
           }
   	localCertificateStore = {
                   file = "./certificate-store2.jks"
                   password = "password"
           }
       }
   }
   certificates = {
       "cordatlscrlsigner" = {
           isSelfSigned = true
           subject = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=U"
           includeIn = ["network-trust-store", "certificate-store"]
           crl = {
               crlDistributionUrl = "http://127.0.0.1:10000/certificate-revocation-list/tls"
               file = "./crl-files/tls.crl"
               indirectIssuer = true
               issuer = "CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=U"
           }
           key = {
               alias = "cordatlscrlsigner"
               includeIn = ["example-hsm-key-store"]
               type = AMAZON_CLOUD_HSM
           }
       }
   }
```

To find the partition name, log in the EC2 machine, run:

```
/opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
```

Log in the admin account with `listUsers` and then `loginHSM`.

{{< note >}}
If you experience any issues, follow the instructions in
[https://docs.aws.amazon.com/cloudhsm/latest/userguide/activate-cluster.html](https://docs.aws.amazon.com/cloudhsm/latest/userguide/activate-cluster.html).
{{< /note >}}

Get the cluster info:

```
aws-cloudhsm>getClusterInfo
Cluster info from server 0(10.0.140.211):
```

| Node Id | Hostname    | Port       |
|---------|-------------|------------|
| 1       | 10.0.140.211| 2225       |

The server ID will be "server X" - in this case, `server 0`.
Call info on the server:

```
info server X
aws-cloudhsm>info server 0
```

| Id | Name         | Hostname    | Port | State     | Partition       | LoginState    |
|----|--------------|-------------|------|-----------|-----------------|---------------|
| 1  | 10.0.140.211 | 0.0.140.211 | 2225 | Connected | hsm-w4b6nnfio7z | Not logged in |

{{< note >}}
You can only log in to the CloutHSM with `CU` type accounts.
{{< /note >}}

To list the users in the tool:

```
aws-cloudhsm>listUsers
Users on server 0(10.0.140.211):
Number of users found:5
```

| User Id | User Type | MofnPubKey | LoginFailureCnt | 2FA |
|---------|-----------|------------|-----------------|-----|
| 1       | CO        | admin      | 0               | NO  |
| 2       | AU        | app_user   | 0               | NO  |
| 3       | AU        | test       | 0               | NO  |
| 4       | CU        | test2      | 0               | NO  |

{{< note >}}
Make sure to log in with a `CU` account.
{{< /note >}}
