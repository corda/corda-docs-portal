firewallMode = BridgeInner

// Public SSL settings
keyStorePassword = "bridgeKeyStorePassword"
sslKeystore = "nodesCertificates/nodesUnitedSslKeystore.jks"
trustStorePassword = "trustpass"
trustStoreFile = "nodesCertificates/network-root-truststore.jks"

outboundConfig {
    artemisBrokerAddress = "<node-machine-address>:11005" // NB: for vmInfra2 swap artemisBrokerAddress and alternateArtemisBrokerAddresses.
    alternateArtemisBrokerAddresses = ["<node-machine-backup-address>:11005"]
    socksProxyConfig {
       version = SOCKS5
       proxyAddress = "<socks-server>:1080"
       username = "proxyuser"
       password = "password"
    }

}
bridgeInnerConfig {
    floatAddresses = ["<float-machine-address>:12005", "<float-machine-backup-address>:12005"] // NB: for vmInfra2 change the ordering.
    expectedCertificateSubject = "CN=float, O=Corda, L=London, C=GB" // This X.500 name should match to the name of the Float component which was used during Tunnel keystore generation above.
    tunnelSSLConfiguration {
        keyStorePassword = "tunnelStorePass"
        keyStorePrivateKeyPassword = "tunnelPrivateKeyPassword"
        trustStorePassword = "tunnelTrustpass"
        sslKeystore = "./tunnel/bridge.jks"
        trustStoreFile = "./tunnel/tunnel-truststore.jks"
        crlCheckSoftFail = true
    }
}
haConfig {
    haConnectionString = "bully://localhost" // Magic URL enabling master via Artemis messaging, not Zookeeper
}
networkParametersPath = network-parameters // The network-parameters file is expected to be copied from the node registration phase and here is expected in the workspace folder.
