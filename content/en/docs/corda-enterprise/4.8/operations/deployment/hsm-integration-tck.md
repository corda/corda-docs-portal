---
date: '2020-12-16T01:00:00Z'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-operations-guide-deployment-hsm-testing
    parent: corda-enterprise-4-8-operations-guide-deployment-hsm
    name: "Testing an HSM integration"
tags:
- operations
- deployment
- hsm
- testing
- integration
title: Testing an HSM integration
weight: 70
---

# Testing an HSM integration

To test an HSM implementation both Corda Enterprise and the HSM must be deployed. This guide will run through testing
an example HSM using the Technical Compatibility Kit (TCK) when deployed virtually to AWS.

This is an example configuration to demonstrate running the TCK and showing the results.

## Before you begin

For this process you must have completed the following tasks:

- Install Git Bash and OpenSSL.
- Create a signing key and certificate using OpenSSL.
- Have access to an AWS instance.
- Download Corda Enterprise utilities `.jar` file from [Artifactory](https://software.r3.com/artifactory/r3-corda-releases).

## Steps

1. Create a virtual private cloud (VPC).
2. Create the HSM cluster.
3. Create signed certificates.
4. Initialise the cluster using the signed certificates.
5. Create the EC2 instance.
6. Log in to the EC2 host and set up the security group.
7. Install and configure the local client.
8. Authenticate the HSM client.
9. Install the JCE provider.
10. Activate the HSM cluster and set user passwords.
11. Set up Corda Enterprise and the TCK.
12. Run the TCK tests.

### Step One: Create the virtual private cloud

1. Sign in to AWS.

2. Open the management console and ensure you are in the correct region.

3. Search for VPC and click **Launch VPC Wizard**. The VPC should be created with the following configuration:
    - VPC with Public and Private Subnets.
    - No IPv6 CIDR Block.
    - Name the VPC and subnets.
    - Enable DNS hostnames.

4. Click **Create VPC** then click **OK**.

### Step Two: Create the HSM cluster in the subnet

1. Navigate to the CloudHSM page: [https://console.aws.amazon.com/cloudhsm](https://console.aws.amazon.com/cloudhsm/).

    {{<note>}}
    Ensure that your region is correctly set.
    {{</note>}}

2. Click **Create cluster**.

3. Configure the cluster with the following information:
    - Select the VPC created earlier.
    - Select the availability zone created earlier.

    Click **Next**.

4. Add a tag that you can search for later, and click **Review**.

5. Click **Create cluster**. This may take several minutes.

6. After the cluster has been created, select it in the cluster list and click **Initialize**.

7. Select the correct private subnet in the list, and click **Create**. This may take several minutes.

8. Click **Cluster CSR**. This will download the certificate signing request associated with the HSM to a local directory.

   Next, the CSR must be used to create certificates locally.

### Step Three: Create signed certificates

1. Move the downloaded CSR to the same directory as your private key.

2. Create the signed certificates using the following command, replacing `<ClusterID>` with the cluster identifier:

    ```
    openssl x509 -req -days 3652 -in <clusterID>_ClusterCsr.csr \
                                  -CA customerCA.crt \
                                  -CAkey customerCA.key \
                                  -CAcreateserial \
                                  -out <clusterID>_CustomerHsmCertificate.crt
    ```

### Step Four: Initialise the cluster with the signed certificate

1. Navigate to the CloudHSM page: [https://console.aws.amazon.com/cloudhsm/](https://console.aws.amazon.com/cloudhsm/).

2. Click the **Actions** drop-down list, and select **Initialize**.

3. Click **Next**.

4. Upload the `customerHSMCertificate` as the cluster certificate, and the `customerCA` certificate as the issuing certificate.

5. Click **Upload and initialize**.

### Step Five: Create the EC2 instance

At this point there is one HSM user, defined as a _Precrypto Officer_ (PRECO). You must update the password for this user,
which will change the user type to _Crypto Officer_ (CO).

1. Open the AWS command-line console here: [https://console.aws.amazon.com/ec2](https://console.aws.amazon.com/ec2/).

2. Click **Launch Instance** and select **Amazon Linux 2**.

3. Select the large instance type, and click **Configure Instance Details**.

4. Select the VPC and public subnet created earlier, and enable **Auto-assign Public IP**.

5. Click **Review and Launch**, then click **Launch**.

6. Select **Create Keypair**, enter a name for the keypair, and click **Download Keypair**.

7. After downloading the keypair, click **Launch instances**.

### Step Six: Log in to the EC2 host and set up the security group

1. Select the new instance. Select **Actions** then click **Connect**.

2. Copy the example command and run it to connect to the EC2 host.

3. In the same menu select **Actions** then **Networking** then **Change Security Groups**.

4. Select the HSM security group and click **Assign Security Groups**.

### Step Seven: Install and configure the local client

1. Connect to the EC2 instance.

2. Download the cloud HSM package using the following command:

    ```
    wget https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL7/cloudhsm-client-latest.el7.x86_64.rpm
    ```

3. Install the cloud HSM package using the following command:

    ```
    sudo yum install -y ./cloudhsm-client-latest.el7.x86_64.rpm
    ```

4. Navigate to the [clusters tab](https://eu-west-1.console.aws.amazon.com/cloudhsm/).

5. Select the HSM cluster created earlier.

6. Copy the **ENI IP address**, and run the following command to set the configuration for the local client:

    ```
    sudo /opt/cloudhsm/bin/configure -a <IP Address>
    ```

### Step Eight: Authenticate the HSM client

1. Using a Git Bash shell on the local host, copy the signed certificate created earlier to the EC2 host:

    ```
    cd sign
    scp -i "sign/nickd-keypair-4.pem" customerCA.crt ec2-user@ec2-3-249-200-193.eu-west-1.compute.amazonaws.com:~
    ```

2. Move the certificate to the correct directory on the EC2 host:

    ```
    ssh -i "nickd-keypair-4.pem" ec2-user@ec2-3-249-200-193.eu-west-1.compute.amazonaws.com
    ls -ltr
    pwd
    sudo -i
    ls -ltr /opt/cloudhsm/etc
    whoami
    cp /home/ec2-user/customerCA.crt /opt/cloudhsm/etc
    exit
    ls -ltr /opt/cloudhsm/etc
    ```

### Step Nine: Install the JCE provider

1. Connect to the EC2 instance.

2. Download the cloud JCE package using the following command:

    ```
    wget https://s3.amazonaws.com/cloudhsmv2-software/CloudHsmClient/EL7/cloudhsm-client-jce-latest.el7.x86_64.rpm
    ```

3. Install the cloud JCE using the following command:

    ```
    sudo yum install -y ./cloudhsm-client-jce-latest.el7.x86_64.rpm
    ```

### Step Ten: Activate the HSM cluster and set user passwords

1. Connect to the EC2 instance.

2. Start the local client using the following command:

    ```
    sudo service cloudhsm-client start
    ```

3. Activate the cluster using the following command:

    ```
    /opt/cloudhsm/bin/cloudhsm_mgmt_util /opt/cloudhsm/etc/cloudhsm_mgmt_util.cfg
    ```

4. Change the password for the _Precrypto Officer_ user, and create a new _Crypto Officer_ user:

    ```
    enable_e2e
    listUsers
    loginHSM PRECO admin password
    changePswd PRECO admin corda
    createUser CO user password
    quit
    ```

### Step Eleven: Setting up Corda Enterprise and TCK

1. Navigate to the **HSM** directory.

2. Navigate to the `samples-hsm` directory and build the `sample-hsm` code:

    ```
    ./gradlew clean build -x test
    ```

3. Create a new local directory to contain the files to be hosted on AWS, in this example the directory is called `hsmtest`:

    ```
    cd hsmtest
    cp <PATH_TO_TCK_JAR> .
    cp /hsm/samples-hsm/build/libs/hsm-root-1.0-SNAPSHOT.jar .
    cp /hsm/samples-hsm/hsm-aws-java/cloud-test/runHSMTests.sh .
    cp /hsm/samples-hsm/hsm-aws-java/cloud-test/runHSMTimeoutTests.sh .
    cp /hsm/samples-hsm/hsm-aws-java/src/test/resources/*.conf .
    ```

4. Create a `utilities` subdirectory in `hsmtest`:

   ```
   mkdir utils
   cd utils
   cp /hsm/samples-hsm/hsm-aws-java/cloud-test/runHSMCommand.sh .
   cp /hsm/samples-hsm/hsm-aws-java/cloud-test/deleteAllKeys.sh .
   ```

5. Create a `drivers` subdirectory in `hsmtest`:

   ```
   mkdir drivers
   mv hsm-root-1.0-SNAPSHOT.jar drivers/
   cp /n/hsm/samples-hsm/hsm-aws-java/lib/cloudhsm-3.2.1.jar drivers/
   ```

6. Create a `.tar` file containing the `hsmtest` directory:

    ```
    tar cvfz hsmtest.tar.gz hsmtest/
    ls -ltr hsmtest.tar.gz
    ```

7. Deploy the compressed `.tar` file to the AWS EC2 host:

    ```
    cd sign
    ssh -i <keypair-certificate> <AWS-ec2-address>
    hostname
    scp  -i "<keypair-certificate>" hsmtest.tar.gz <AWS-ec2-address>:~
    ```

8. Unzip the `.tar` file on the EC2 host:

    ```
    tar xvf hsmtest.tar.gz
    ```


### Step Twelve: Running the TCK tests

1. To run the tests you must configure the credentials of the HSM. These credentials should match the username and password
 of the _Crypto Officer_ earlier. Additionally, you must specify the `partition` field of the HSM. The three files that
 must have credentials updated are:

    ```
    service.tls.conf
    service.legal.conf
    service.confidential.conf
    ```

2. Before you run the TCK tests, you must clear any extraneous keys from the HSM using the following command:

    ```
    cd /home/ec2-user/hsmtest/utils/
    ./deleteAllKeys.sh
    ```

3. Run the standard TCK tests by running the following command:

    ```
    cd /home/ec2-user/hsmtest/
    ./runHSMTests.sh | tee out
    ```

   The tests will take approximately 10 minutes to run. If any tests fail, the logs will be saved in a date- and time-stamped subdirectory.

4. If the standard tests pass, delete the keys as described in Step Two, and run the timeout tests by running the following command:

    ```
    cd /home/ec2-user/hsmtest/utils/
    ./deleteAllKeys.sh
    cd /home/ec2-user/hsmtest/
    ./runHSMTimeoutTests.sh | tee out
    ```

    The timeout tests may take over an hour to complete. The tests are designed to hang for up to 20 minutes in order to ensure that connections can be successfully re-established.
