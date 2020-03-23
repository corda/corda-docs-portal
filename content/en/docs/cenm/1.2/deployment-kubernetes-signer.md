# CENM Signer Helm Chart

This Helm chart is to configure, deploy and run CENM [Signing](signing-service.md) service.

As the initial step this chart runs automatically PKI tool which creates and stores certificates necessary for correct Corda Network operation.
By default the certificates have sample X.500 subject names (e.g. Identity Manager certificate has the subject name “CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US”). The subject name can be set by configuration options starting with `pki.certificates.` prefix.

For more information about PKI Tool and Certificate Hierarchy refer to:

* [Certificate Hierarchy Guide](pki-guide.md)
* [PKI Tool](pki-tool.md)

## Example usage

Using default values:

```bash
helm install signer signer
```

Overwriting default values with password for SSH console:

```bash
helm install signer signer --set shell.password="superDifficultPassword"
```

Parameters starting with prefix "pki.certificates." allow to override the default subject/issuer X500 names of the Corda certificates.
The example command to bootstrap Signer with the X500 name "CN=Company A TLS Signer Certificate [...]" of the subject and the issuer of the certificate for signing the CRL:

```bash
helm install signer signer --set idmanPublicIP=13.71.57.219 --set pki.certificates.tlscrlsigner.subject="CN=Company A TLS Signer Certificate\, OU=HQ\, O=HoldCo LLC\, L=London\, C=UK" --set pki.certificates.tlscrlsigner.crl.issuer="CN=Company A TLS Signer Certificate\, OU=Corda\, O=R3 HoldCo LLC\, L=New York\, C=US"
```

The name needs to be a valid X500 name and commas need to be escaped by backslash (\).

## Configuration variables

| Parameter                                    | Description                                              | Default value         |
| -------------------------------------------- | -------------------------------------------------------- | --------------------- |
| `bashDebug`                                  | Display additional information while running bash scripts (useful while investigating issues) | `false` |
| `dockerImage.name`                           | URL to Signer Docker image                     | `acrcenm.azurecr.io/signer/signer` |
| `dockerImage.tag`                            | Docker image Tag | `1.2` |
| `dockerImage.pullPolicy`                     | Image pull policy. Ref.: https://kubernetes.io/docs/concepts/containers/images/#updating-images | `Always` |
| `service.type`                               | Kubernetes service type, https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types | `LoadBalancer` |
| `service.port`                               | Kubernetes service port/targetPort for external communication | `10000` |
| `serviceInternal.type`                       | Kubernetes service type for internal communication between CENM components | `LoadBalancer` |
| `serviceInternal.port`                       | Kubernetes service port/targetPort | `5052` |
| `serviceRevocation.port`                     | Kubernetes service port to access Identity Manager's revocation endpoint (targetPort) | `5053` |
| `serviceSsh.type`                            | Kubernetes service type to access Signer ssh console | `LoadBalancer` |
| `shell.sshdPort`                             | Signer ssh port | `2222` |
| `shell.user`                                 | Signer ssh user | `signer` |
| `shell.password`                             | Signer ssh password | `signerP` |
| `cordaJarMx`                                 | Initial value for memory allocation | `1` |
| `jarPath`                                    | Path to a folder which contains Signer jar files | `bin` |
| `configPath`                                 | Path to a folder which contains Signer configuration file | `etc` |
| `pki.certificates.tlscrlsigner.subject`      | Subject of the certificate for signing the CRL for the Corda Node’s TLS-level certificate (alias: tlscrlsigner) | `CN=Test TLS Signer Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.tlscrlsigner.crl.issuer`   | Issuer of the certificate for signing the CRL for the Corda Node’s TLS-level certificate (alias tlscrlsigner) | `CN=Corda TLS Signer Certificate, OU=Corda, O=R3 HoldCo LLC, L=New York, C=US` |
| `pki.certificates.cordarootca.subject`       | Subject of Corda Root certificate (alias: cordarootca) | `CN=Test Root CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.subordinateca.subject`     | Subject of Corda Subordinate certificate (alias: subordinateca) | `CN=Test Subordinate CA Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.identitymanagerca.subject` | Subject of Corda Identity Manager certificate (alias: identitymanagerca) | `CN=Test Identity Manager Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
| `pki.certificates.networkmap.subject`        | Subject of Corda Network Map certificate (alias: networkmap)  | `CN=Test Network Map Service Certificate, OU=HQ, O=HoldCo LLC, L=New York, C=US` |
