---
date: '2021-11-14'
title: "CorDapp Packaging"
menu:
  corda-5-alpha:
    parent: corda-5-alpha-tutorials-deploy
    identifier: corda-5-alpha-tutorial-deploy-cordapp-packaging
    weight: 2000
section_menu: corda-5-alpha
---

This section describes how to package your CorDapp as CPKs, CPBs, and CPIs.

## Before You Start

You will need a working copy of the Corda CLI with the MGM and package plugins installed. 
<!-- See the [Corda CLI Plugin Host](https://github.com/corda/corda-cli-plugin-host#setupbuild). -->

## Configuring the Gradle Plugin

To convert an existing CorDapp project to the new Gradle plugin:

1. Add a new version number to `gradle.properties`:
    ```groovy
    cordaGradlePluginsVersion2=7.0.0-SNAPSHOT
    ```
2. Add this repository to pluginManagement/repositories in `settings.gradle`:
    ```groovy
    maven {
        url "${artifactoryContextUrl}/corda-dev"
        content {
            includeGroupByRegex 'net\\.corda\\.plugins(\\..*)?'
        }
    }
    ```
3. Add the plugin to the plugins section of `settings.gradle`:
    ```groovy
    id 'net.corda.plugins.cordapp-cpk2' version cordaGradlePluginsVersion2
    id 'net.corda.plugins.cordapp-cpb2' version cordaGradlePluginsVersion2
    ```
4. Inside the CorDapp project, change the plugins block at the top of the file:
    ```groovy
    id 'net.corda.plugins.cordapp-cpk2'
    // or
    id 'net.corda.plugins.cordapp-cpb2'
    ```

## Generating a Code Signing Key

To generate a code signing key for signing the CPI:

1. Generate a signing key:
    ```shell
    keytool -genkeypair -alias "signing key 1" -keystore signingkeys.pfx -storepass "keystore password" -dname "cn=CPI Plugin Example - Signing Key 1, o=R3, L=London, c=GB" -keyalg RSA -storetype pkcs12 -validity 4000
    ```
2. If you are using the default Gradle plugin signing key, you must import it into our key store. Save the following text into a file named `gradle-plugin-default-key.pem`:
    ```text
    -----BEGIN CERTIFICATE-----
    MIIB7zCCAZOgAwIBAgIEFyV7dzAMBggqhkjOPQQDAgUAMFsxCzAJBgNVBAYTAkdC
    MQ8wDQYDVQQHDAZMb25kb24xDjAMBgNVBAoMBUNvcmRhMQswCQYDVQQLDAJSMzEe
    MBwGA1UEAwwVQ29yZGEgRGV2IENvZGUgU2lnbmVyMB4XDTIwMDYyNTE4NTI1NFoX
    DTMwMDYyMzE4NTI1NFowWzELMAkGA1UEBhMCR0IxDzANBgNVBAcTBkxvbmRvbjEO
    MAwGA1UEChMFQ29yZGExCzAJBgNVBAsTAlIzMR4wHAYDVQQDExVDb3JkYSBEZXYg
    Q29kZSBTaWduZXIwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAQDjSJtzQ+ldDFt
    pHiqdSJebOGPZcvZbmC/PIJRsZZUF1bl3PfMqyG3EmAe0CeFAfLzPQtf2qTAnmJj
    lGTkkQhxo0MwQTATBgNVHSUEDDAKBggrBgEFBQcDAzALBgNVHQ8EBAMCB4AwHQYD
    VR0OBBYEFLMkL2nlYRLvgZZq7GIIqbe4df4pMAwGCCqGSM49BAMCBQADSAAwRQIh
    ALB0ipx6EplT1fbUKqgc7rjH+pV1RQ4oKF+TkfjPdxnAAiArBdAI15uI70wf+xlL
    zU+Rc5yMtcOY4/moZUq36r0Ilg==
    -----END CERTIFICATE-----
    ```
3. Import `gradle-plugin-default-key.pem` into the keystore:
    ```shell
    keytool -importcert -keystore signingkeys.pfx -storepass "keystore password" -noprompt -alias gradle-plugin-default-key -file gradle-plugin-default-key.pem
    ```
{{< note >}}
This key can be generated once and kept for reuse.
{{< /note >}}

## Generating a Group Policy File

If you intend to run a basic [static network](../network-types.html#static-networks) setup, you can use the Corda CLI to generate a group policy file. For example, you could run the following command to generate the file:
```shell
./corda-cli.sh mgm groupPolicy > GroupPolicy.json
```

Refer to the [Group Policy](../../../../../../en/platform/corda/5.0-alpha/deploying/group-policy.html) section to learn more about the `GroupPolicy.json` file.

<!-- For more information on this plugin, refer to the [README.md](https://github.com/corda/corda-runtime-os/blob/release/os/5.0/tools/plugins/mgm/README.md). -->

If you are running a dynamic network, you will need to export the group policy file from the MGM using the HTTP API. To learn how to do this, see the [MGM Onboarding](../deployment-tutorials/onboarding/mgm-onboarding.html) tutorial for more information.

## Building a CPI

The Gradle plugin builds the CPB. Run the following command to turn a CPB into a CPI:
```shell 
./corda-cli.sh package create-cpi \
    --cpb mycpb.cpb \
    --group-policy TestGroupPolicy.json \
    --cpi-name "cpi name" \
    --cpi-version "1.0.0.0-SNAPSHOT" \
    --file output.cpi \
    --keystore signingkeys.pfx \
    --storepass "keystore password" \
    --key "signing key 1"
```

## Importing Trusted Code Signing Certificates

Corda validates that uploaded CPIs are signed with a trusted key. To trust your signing keys, upload them with these commands:

1. Import the Gradle plugin default key into Corda:
    ```shell
    curl --insecure -u admin:admin -X PUT -F alias="gradle-plugin-default-key" -F certificate=@gradle-plugin-default-key.pem https://localhost:8888/api/v1/certificates/cluster/code-signer
    ```
2. Export the signing key certificate from the key store:
    ```shell
    keytool -exportcert -rfc -alias "signing key 1" -keystore signingkeys.pfx -storepass "keystore password" -file signingkey1.pem
    ```
3. Import the signing key into Corda:
    ```shell
    curl --insecure -u admin:admin -X PUT -F alias="signingkey1-2022" -F certificate=@signingkey1.pem https://localhost:8888/api/v1/certificates/cluster/code-signer
    ```

{{< note >}}
Use an alias that will be unique over time. Consider how certificate expiry will require new certificates with the same X.500 name as existing certificates, and define a naming convention that covers that use case.
{{< /note >}}