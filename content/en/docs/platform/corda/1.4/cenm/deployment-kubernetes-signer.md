---
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    parent: cenm-1-4-deployment-kubernetes
tags:
- config
- kubernetes
title: CENM Signing Service Helm chart
weight: 400
---

# CENM Signing Service Helm Chart

This Helm chart is to configure, deploy, and run the [CENM Signing Service](signing-service.md) on Kubernetes.

As the initial step this chart runs automatically PKI tool which creates and stores certificates necessary for correct Corda Network operation.
By default, the certificates have sample X.500 subject names (for example, the Identity Manager Service certificate has the subject name “CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US”). The subject name can be set by configuration options starting with `pki.certificates.` prefix.

Passwords to the security certificates keys and keystores cannot be configurable.

For more information about PKI Tool and Certificate Hierarchy refer to:

* [Certificate Hierarchy Guide](pki-guide.md)
* [PKI Tool](pki-tool.md)

## Example usage

In the example below, the default values are used:

```bash
helm install cenm-signer signer --set prefix=cenm --set acceptLicense=Y
```

In the example below, the default values are overwritten:

```bash
helm install cenm-signer signer --set idmanPublicIP=X.X.X.X --set prefix=cenm --set acceptLicense=Y --set volumeSizeSignerLogs=5Gi
```

Parameters starting with prefix "pki.certificates." allow to override the default subject/issuer X500 names of the Corda certificates.
The example command to bootstrap Signing Service with the X500 name "CN=Company A TLS Signer Certificate [...]" of the subject and the issuer of the certificate for signing the CRL:

```bash
helm install signer signer --set idmanPublicIP=13.71.57.219 --set pki.certificates.tlscrlsigner.subject="CN=Company A TLS Signer Certificate\, OU=HQ\, O=HoldCo LLC\, L=London\, C=UK" --set pki.certificates.tlscrlsigner.crl.issuer="CN=Company A TLS Signer Certificate\, OU=Corda\, O=R3 HoldCo LLC\, L=New York\, C=US"
```

The name needs to be a valid X500 name and commas need to be escaped by a backslash character "\\".

## Configuration variables

{{< table >}}
| Parameter                                    | Description                                              | Default value         |
| -------------------------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                                  | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `signerImage.repository`                     | URL to Signing Service Docker image repository           | `acrcenm.azurecr.io/signer/signer` |
| `signerImage.tag`                            | Docker image Tag | `1.4` |
| `signerImage.pullPolicy`                     | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `dockerImageCli.repository`                  | URL to CLI image repository | `acrcenm.azurecr.io/cli/cli` |
| `dockerImageCli.tag`                         | Docker image tag | `1.4` |
| `dockerImageCli.pullPolicy`                  | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `volumeSizeSignerEtc`                        | Volume size for the `etc/` directory | `1Mi` |
| `volumeSizeSignerLogs`                       | Volume size for the `logs/` directory | `10Gi` |
| `signerJar.xmx`                              | Value for java -Xmx memory settings | `1G` |
| `signerJar.path`                             | The directory where the Signing Service `.jar` file is stored | `bin` |
| `signerJar.configPath`                       | The directory where the Signing Service configuration is stored | `etc` |
| `signerJar.configFile`                       | The file name of the Signing Service configuration file  | `signer.conf` |
| `signers.CSR.schedule.interval`              | The schedule interval for the CSR signing process | `1m` |
| `signers.CRL.schedule.interval`              | The schedule interval for the CRL signing process | `1d` |
| `signers.NetworkMap.schedule.interval`       | The schedule interval for the Network Map signing process | `1m` |
| `signers.NetworkParameters.schedule.interval` | The schedule interval for the Network Parameters signing process | `1m` |
| `signingKeys.keyStore.keyVaultUrl`           | The Azure Key Vault URL, only applicable if using Azure Key Vault instead of local key store | `https://vault.vault.azure.net` |
| `signingKeys.credentials.keyStorePassword`   | The key store password, only applicable if using Azure Key Vault instead of local key store | `""` |
| `signingKeys.credentials.keyStoreAlias`      | The key store alias, only applicable if using Azure Key Vault instead of local key store | `1` |
| `signingKeys.credentials.clientId`           | The application client id to access the Azure Key Vault, only applicable if using Azure Key Vault instead of local key store | `abcdefgh-1234-5678-9012-123456789012` |
| `pki.certificates.tlscrlsigner.subject`      | Subject of the certificate for signing the CRL for the Corda Node’s TLS-level certificate (alias: tlscrlsigner) | `CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.tlscrlsigner.crl.issuer`   | Issuer of the certificate for signing the CRL for the Corda Node’s TLS-level certificate (alias tlscrlsigner) | `CN=Corda TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US` |
| `pki.certificates.cordarootca.subject`       | Subject of Corda Root certificate (alias: cordarootca) | `CN=Test Root CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.subordinateca.subject`     | Subject of Corda Subordinate certificate (alias: subordinateca) | `CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.identitymanagerca.subject` | Subject of Corda Identity Manager certificate (alias: identitymanagerca) | `CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.networkmap.subject`        | Subject of Corda Network Map certificate (alias: networkmap)  | `CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `sleepTimeAfterError`                        | Sleep time (in seconds) after an error occurred | `120` |
| `logsContainersEnabled`                      | Enable container displaying live logs | `true`
{{< /table >}}
