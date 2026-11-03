firewallMode = FloatOuter
inboundConfig {
    listeningAddress = "<float-external-facing-address>:10002"
}
floatOuterConfig {
    floatAddress = "<float-bridge-facing-address>:12005"
    expectedCertificateSubject = "CN=bridge, O=Corda, L=London, C=GB" // This X.500 name must align with name that Bridge received at the time of internal certificates generation.
    tunnelSSLConfiguration {
           keyStorePassword = "tunnelStorePass"
           keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
           trustStorePassword = "tunnelTrustpass"
           sslKeystore = "./tunnel/float.jks"
           trustStoreFile = "./tunnel/tunnel-truststore.jks"
           crlCheckSoftFail = true
    }
}
networkParametersPath = network-parameters // The network-parameters file is expected to be copied from the node registration phase and here is expected in the workspace folder.
